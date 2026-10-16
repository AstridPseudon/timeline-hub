#!/usr/bin/env tsx
/**
 * Hosted UI -> loopback gateway -> fixed loopback Runtime. No remote media relay.
 *
 * The gateway serves the same `/api/runtime/*` and `/api/astrid/*` paths as local dev, on 127.0.0.1:17340. There is no
 * secret in the path: the only credential the browser has is its Origin (exactly the hosted origin), and the Host must be
 * exactly `127.0.0.1:<port>`. The product token stays here and is attached to upstream requests.
 *
 * The Runtime is not fixed at start. Its endpoint and token are read from the discovery and credential files on every request
 * (`currentRuntime()`), so a Runtime that restarts on a new port, or a rotated token, is followed without restarting the
 * gateway. When either changes, the Runtime's identity is checked once (concurrent requests share the check) and a different
 * realm is refused with 503 `realm_changed`. A Runtime that is down is 503 `runtime_unavailable` while the gateway keeps listening.
 */
import { createServer, request as httpRequest, type ClientRequest, type IncomingMessage } from 'node:http';
import { readFileSync, appendFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
import { classifyPairedRoute } from '../config/vite/pairedRoutePolicy';
import { objectCacheControl } from '../config/vite/objectCachePolicy.mjs';
import { currentRuntime } from './runtime-discovery-proxy.mjs';

/** The gateway's well-known port (Plan A D1). Tests pass `--port 0` or listen on 0 themselves. */
export const DEFAULT_GATEWAY_PORT = 17340;
export const DEFAULT_MAX_OBJECT_BYTES = 5 * 1024 ** 3;
export function resolveMaxObjectBytes(raw: string | undefined): number {
  if (raw === undefined) return DEFAULT_MAX_OBJECT_BYTES;
  if (!/^[1-9]\d*$/.test(raw) || !Number.isSafeInteger(Number(raw)) || Number(raw) > DEFAULT_MAX_OBJECT_BYTES) {
    throw new Error('RUNTIME_MAX_OBJECT_BYTES must be an integer from 1 to 5368709120');
  }
  return Number(raw);
}
export const PRODUCT_SCOPES = ['handshake', 'projects:read', 'projects:write', 'tasks:read', 'tasks:write', 'objects:read', 'objects:write'];
const REQUEST_HEADERS = new Set(['accept', 'content-type', 'content-length', 'range', 'if-match', 'if-none-match', 'idempotency-key', 'x-filename', 'x-original-name', 'x-expected-digest', 'x-media-width', 'x-media-height', 'x-media-duration-seconds']);
const RESPONSE_HEADERS = new Set(['content-type', 'content-length', 'content-range', 'accept-ranges', 'etag', 'last-modified']);
const ACP_PROTOCOL_HEADER = 'X-Astrid-Bridge-Version';
const ACP_PROTOCOL_VERSION = 'v1';
type GatewayService = 'runtime' | 'astrid';
// One route table and one canonicalisation, shared with the paired relay.
function classify(service: GatewayService, upstreamPath: string, method: string) {
  return classifyPairedRoute(`/api/${service}${upstreamPath}`, method);
}
export function allowedRoute(path: string, method: string, service: GatewayService = 'runtime'): boolean {
  const route = classify(service, path, method);
  return Boolean(route) && route!.service !== 'acp';
}
export function allowedAcpRoute(path: string, method: string): boolean {
  return classify('astrid', path, method)?.service === 'acp';
}
export function loopbackEndpoint(raw: string): URL {
  const url = new URL(raw);
  if (url.protocol !== 'http:' || url.hostname !== '127.0.0.1' || !url.port || url.username || url.password || url.pathname !== '/' || url.search || url.hash) throw new Error('Runtime must be a fixed http://127.0.0.1:PORT origin');
  return url;
}
/** The Runtime base under the gateway origin (the App's `runtimeApiBase()`). */
export const GATEWAY_RUNTIME_PREFIX = '/api/runtime';
export type RuntimeRefusalCode = 'runtime_unavailable' | 'realm_changed' | 'runtime_identity_mismatch' | 'runtime_discovery_invalid';
/** Why the Runtime cannot be used right now. Always answered as 503, with `code` as the body's `error`. */
export class RuntimeRefusal extends Error {
  constructor(readonly code: RuntimeRefusalCode, message: string) { super(message); }
}
export interface RuntimeTarget { endpoint: URL; token: string }
/** Where the gateway finds its Runtime: read on every request, verified whenever the result changes. */
export interface RuntimeSource {
  /** The Runtime's current endpoint and token. Throws when the discovery or credential file is missing, malformed or not loopback. */
  read(): { endpoint: string; token: string };
  /** Throws a `RuntimeRefusal` when this endpoint and token are not the Runtime the gateway was started for. */
  verify(target: RuntimeTarget): Promise<void>;
  /** The target that was verified at start, so the first request does not repeat the check. */
  verified?: RuntimeTarget;
}
const targetKey = (target: RuntimeTarget) => `${target.endpoint.origin}\n${target.token}`;
const refusalCode = (error: unknown): RuntimeRefusalCode => error instanceof RuntimeRefusal ? error.code : 'runtime_unavailable';

/**
 * Resolves the Runtime for a request. A changed endpoint or token is verified once; requests that arrive during that check
 * wait for the same answer. Failures are never remembered, so the next request checks again.
 */
function createRuntimeResolver(config: { endpoint?: string; token?: string; runtime?: RuntimeSource }) {
  const source = config.runtime;
  if (!source) {
    if (!config.endpoint || !config.token) throw new Error('A Runtime endpoint and token, or a Runtime source, are required');
    const fixed: RuntimeTarget = { endpoint: loopbackEndpoint(config.endpoint), token: config.token };
    return { retries: false, current: async () => fixed, changedFrom: async (_failed: RuntimeTarget): Promise<RuntimeTarget | null> => null, refused: (_target: RuntimeTarget) => {} };
  }
  let verifiedKey = source.verified ? targetKey(source.verified) : null;
  let inflight: { key: string; promise: Promise<void> } | null = null;
  const read = (): RuntimeTarget => {
    try {
      const raw = source.read();
      return { endpoint: loopbackEndpoint(String(raw.endpoint)), token: raw.token };
    } catch (error) {
      throw new RuntimeRefusal('runtime_discovery_invalid', error instanceof Error ? error.message : String(error));
    }
  };
  const verified = async (target: RuntimeTarget) => {
    const key = targetKey(target);
    if (key === verifiedKey) return;
    if (inflight?.key !== key) {
      const check: { key: string; promise: Promise<void> } = { key, promise: Promise.resolve() };
      check.promise = source.verify(target).then(() => { verifiedKey = key; }).finally(() => { if (inflight === check) inflight = null; });
      inflight = check;
    }
    await inflight.promise;
  };
  return {
    retries: true,
    async current() { const target = read(); await verified(target); return target; },
    /** The target to retry on after a refused connection, or null when discovery still names the one that just failed. */
    async changedFrom(failed: RuntimeTarget) {
      const target = read();
      if (targetKey(target) === targetKey(failed)) return null;
      await verified(target);
      return target;
    },
    /** Nothing listened at this target: whatever answers there next is checked again, even on the same port. */
    refused(target: RuntimeTarget) { if (targetKey(target) === verifiedKey) verifiedKey = null; },
  };
}

export function createLoopbackGateway(config: { endpoint?: string; token?: string; runtime?: RuntimeSource; origin: string; acpEndpoint?: string; acpToken?: string; maxObjectBytes?: number; audit?: (entry: Record<string, unknown>) => void }) {
  const maxObjectBytes = resolveMaxObjectBytes(config.maxObjectBytes === undefined ? undefined : String(config.maxObjectBytes));
  const resolver = createRuntimeResolver(config);
  const acpEndpoint = config.acpEndpoint ? loopbackEndpoint(config.acpEndpoint) : null;
  if (acpEndpoint && !config.acpToken) throw new Error('ACP endpoint requires a dedicated ACP bridge token');
  const origin = new URL(config.origin);
  if (origin.protocol !== 'https:' || origin.origin !== config.origin) throw new Error('An exact hosted HTTPS origin is required');
  const server = createServer((req, res) => {
    const reject = (status: number, error: string) => { res.writeHead(status, { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' }); res.end(JSON.stringify({ error })); };
    const address = server.address();
    if (!address || typeof address === 'string' || req.headers.host !== `127.0.0.1:${address.port}`) return reject(403, 'invalid_host');
    const path = req.url ?? '';
    const method = req.method ?? 'GET';
    // Decoded once; this canonical path is both what is judged and what is forwarded. Compose is a local-Vite route and is never served here.
    const route = classifyPairedRoute(path, method);
    const isAcp = route?.service === 'acp';
    const upstreamPath = route?.upstreamPath ?? path;
    const targetPath = isAcp ? upstreamPath.slice('/acp'.length) : upstreamPath;
    const allowed = Boolean(route) && (isAcp ? Boolean(acpEndpoint) : route!.service === 'runtime' || route!.service === 'astrid');
    let responseBytes = 0;
    res.once('finish', () => config.audit?.({ at: new Date().toISOString(), method, path: upstreamPath.split('?', 1)[0], origin: req.headers.origin ?? null, upstream_hostname: '127.0.0.1', status: res.statusCode, response_bytes: responseBytes }));
    // The Origin is judged before the route, so a foreign page learns nothing about which paths exist.
    let acceptedOrigin = req.headers.origin === origin.origin;
    // Native media elements may omit Origin; their browser-generated Referer must match. Removed by A3.R once media sends Origin.
    if (!req.headers.origin && ['GET', 'HEAD'].includes(method)) {
      try { acceptedOrigin = typeof req.headers.referer === 'string' && new URL(req.headers.referer).origin === origin.origin; } catch { acceptedOrigin = false; }
    }
    if (!acceptedOrigin) return reject(403, 'hosted_origin_required');
    res.setHeader('Access-Control-Allow-Origin', origin.origin);
    res.setHeader('Vary', 'Origin');
    res.setHeader('Cache-Control', 'no-store');
    res.setHeader('Access-Control-Expose-Headers', [...RESPONSE_HEADERS].join(', '));
    // The page may read a refusal from its own origin, so a missing route is a 404 for it and not an opaque network error.
    if (method !== 'OPTIONS' && !allowed) return reject(404, 'route_not_allowed');
    if (method === 'OPTIONS') {
      const requestedMethod = String(req.headers['access-control-request-method'] ?? '');
      const preflight = classifyPairedRoute(path, requestedMethod);
      const preflightAllowed = Boolean(preflight) && (preflight!.service === 'acp' ? Boolean(acpEndpoint) : preflight!.service === 'runtime' || preflight!.service === 'astrid');
      if (!preflightAllowed) return reject(404, 'route_not_allowed');
      const requestedHeaders = String(req.headers['access-control-request-headers'] ?? '').toLowerCase().split(',').map(x => x.trim()).filter(Boolean);
      if (requestedHeaders.some(header => !REQUEST_HEADERS.has(header))) return reject(403, 'header_not_allowed');
      res.setHeader('Access-Control-Allow-Methods', requestedMethod);
      res.setHeader('Access-Control-Allow-Headers', requestedHeaders.join(', '));
      res.setHeader('Access-Control-Allow-Private-Network', 'true');
      res.setHeader('Access-Control-Max-Age', '300');
      res.writeHead(204); res.end(); return;
    }
    if (req.headers.authorization || req.headers.cookie) return reject(403, 'browser_credentials_forbidden');
    const binaryUpload = method === 'POST' && /\/(objects|media-imports)(?:\?|$)/.test(upstreamPath);
    const maxBytes = isAcp ? 128 * 1024 : binaryUpload ? maxObjectBytes : 1024 * 1024;
    const declared = req.headers['content-length'];
    if (declared && (!/^\d+$/.test(declared) || Number(declared) > maxBytes)) return reject(413, 'payload_too_large');
    if (isAcp && (!acpEndpoint || !config.acpToken)) return reject(503, 'acp_unavailable');
    const baseHeaders: Record<string, string> = {};
    if (isAcp) {
      baseHeaders[ACP_PROTOCOL_HEADER] = ACP_PROTOCOL_VERSION;
      // Authenticated gateway calls always select hosted local-only ACP policy.
      baseHeaders['X-Reigh-Local-Media-Only'] = '1';
    }
    for (const [key, value] of Object.entries(req.headers)) if (REQUEST_HEADERS.has(key) && typeof value === 'string') baseHeaders[key] = value;
    // A request without a body can be sent again to a Runtime that moved while it was being sent. One with a body never is:
    // its bytes are a stream that has already been consumed.
    const bodyless = ['GET', 'HEAD'].includes(method) && !req.headers['transfer-encoding'] && (!declared || declared === '0');
    let upstream: ClientRequest | undefined;
    let upstreamResponse: IncomingMessage | undefined;
    let failed = false;
    function fail(status: number, error: string) {
      if (failed) return;
      failed = true;
      if (upstream) req.unpipe(upstream);
      req.resume();
      upstreamResponse?.destroy();
      upstream?.destroy();
      if (!res.headersSent) {
        res.removeHeader('Content-Length');
        reject(status, error);
      } else res.destroy();
    }
    const send = (target: RuntimeTarget, retryable: boolean) => {
      const attempt = httpRequest({ hostname: '127.0.0.1', port: target.endpoint.port, path: targetPath, method, headers: { Authorization: `Bearer ${target.token}`, ...baseHeaders } }, response => {
        if (attempt !== upstream) { response.destroy(); return; }
        upstreamResponse = response;
        // Never permit an upstream redirect to move a media request off machine.
        if (response.statusCode && response.statusCode >= 300 && response.statusCode < 400 && response.statusCode !== 304) {
          fail(502, 'upstream_redirect_forbidden');
          return;
        }
        for (const [key, value] of Object.entries(response.headers)) if (RESPONSE_HEADERS.has(key) && value !== undefined) res.setHeader(key, value);
        res.statusCode = response.statusCode ?? 502;
        // Digest-addressed object bytes never change; every other response stays no-store.
        const cacheControl = objectCacheControl(method, upstreamPath, res.statusCode);
        if (cacheControl) res.setHeader('Cache-Control', cacheControl);
        response.on('data', chunk => { responseBytes += chunk.length; });
        response.on('error', () => res.destroy());
        response.on('aborted', () => res.destroy());
        response.pipe(res);
      });
      upstream = attempt;
      // Idle (no bytes in either direction), not wall clock: a flowing media stream is never capped.
      attempt.setTimeout(isAcp ? 5 * 60_000 : 60_000, () => { if (attempt === upstream) fail(504, 'upstream_timeout'); });
      attempt.on('error', (error: NodeJS.ErrnoException) => {
        if (attempt !== upstream || failed) return;
        // Nothing is listening: the Runtime is down (503), not a transport that broke part-way (502).
        const refused = error.code === 'ECONNREFUSED';
        if (refused && !isAcp) resolver.refused(target);
        if (refused && retryable) {
          upstream = undefined;
          attempt.destroy();
          resolver.changedFrom(target).then(
            next => { if (res.destroyed) return; if (next) send(next, false); else reject(503, 'runtime_unavailable'); },
            problem => { if (!res.destroyed) reject(503, refusalCode(problem)); },
          );
          return;
        }
        fail(isAcp ? 503 : refused ? 503 : 502, isAcp ? 'acp_unavailable' : 'runtime_unavailable');
      });
      if (bodyless) attempt.end(); else req.pipe(attempt);
    };
    const begin = (target: RuntimeTarget) => {
      // The request's own listeners start the body flowing, so they are attached only once there is somewhere to send it.
      let bytes = 0;
      req.on('data', chunk => { bytes += chunk.length; if (bytes > maxBytes) fail(413, 'payload_too_large'); });
      req.on('error', () => fail(400, 'incomplete_request'));
      req.on('aborted', () => fail(400, 'incomplete_request'));
      res.on('close', () => {
        upstreamResponse?.destroy();
        upstream?.destroy();
      });
      // Both pipes use Node's bounded stream buffers and propagate backpressure.
      send(target, resolver.retries && !isAcp && bodyless);
    };
    if (isAcp) return begin({ endpoint: acpEndpoint!, token: config.acpToken! });
    // The Runtime is read now, not at start. The body stays unread until it is known where it goes.
    resolver.current().then(
      target => { if (!res.destroyed) begin(target); },
      problem => { if (!res.destroyed) reject(503, refusalCode(problem)); },
    );
  });
  return { server, prefix: GATEWAY_RUNTIME_PREFIX };
}
/** Terminal-safe, bounded text from another local process. */
const printable = (value: unknown) => String(value ?? '').replace(/[^\x20-\x7e]/g, '?').slice(0, 80);
/**
 * One sentence for a taken port. The holder is asked who it serves the way the hosted page would (health and realm under
 * `/api/runtime`, with this gateway's Origin), so a second `dev:local`, or a gateway left over from another profile, is named.
 */
export async function describePortHolder(port: number, hostedOrigin: string): Promise<string> {
  const realm = await new Promise<Record<string, unknown> | null>((resolve) => {
    const probe = httpRequest({ hostname: '127.0.0.1', port, path: `${GATEWAY_RUNTIME_PREFIX}/v1/realm`, method: 'GET', headers: { Origin: hostedOrigin }, timeout: 2000 }, (response) => {
      const chunks: Buffer[] = [];
      response.on('data', (chunk) => { if (chunks.length < 64) chunks.push(chunk); });
      response.on('end', () => {
        try { resolve(response.statusCode === 200 ? JSON.parse(Buffer.concat(chunks).toString('utf8')) : null); } catch { resolve(null); }
      });
      response.on('error', () => resolve(null));
    });
    probe.on('timeout', () => { probe.destroy(); resolve(null); });
    probe.on('error', () => resolve(null));
    probe.end();
  });
  if (realm && typeof realm.realm_id === 'string') {
    const name = typeof realm.display_name === 'string' && realm.display_name ? `"${printable(realm.display_name)}" (${printable(realm.realm_id)})` : printable(realm.realm_id);
    return `port ${port} is already served by a Reigh gateway for realm ${name}; stop that one first, or pass --port to use another`;
  }
  return `port ${port} is already in use by a program that is not a Reigh gateway for ${hostedOrigin}; stop it, or pass --port to use another`;
}
/** Asks a Runtime who it is, the way the gateway's own start does. A Runtime that does not answer is `runtime_unavailable`. */
type Handshake = { protocol?: unknown; actor_id?: unknown; realm_id?: unknown; scopes?: unknown };
async function handshake(target: RuntimeTarget): Promise<Handshake> {
  let response: Response;
  try {
    response = await fetch(new URL('/v1/handshake', target.endpoint), { method: 'POST', headers: { Authorization: `Bearer ${target.token}`, 'Content-Type': 'application/json' }, body: JSON.stringify({ protocol: 'workspace.v1', client_name: 'reigh-loopback-gateway', client_version: '1', requested_scopes: PRODUCT_SCOPES }), signal: AbortSignal.timeout(3000) });
  } catch (error) {
    throw new RuntimeRefusal('runtime_unavailable', `Runtime did not answer the handshake: ${error instanceof Error ? error.message : String(error)}`);
  }
  const identity = await response.json().catch(() => null);
  if (!response.ok || !identity || typeof identity !== 'object') throw new RuntimeRefusal('runtime_unavailable', `Runtime handshake answered ${response.status}`);
  return identity;
}
/** Whether the handshake is the scoped product identity this gateway serves (never an owner or pack-host actor, exactly the product scopes). */
function productIdentityMatches(identity: Handshake, actor: string): boolean {
  return identity.protocol === 'workspace.v1' && identity.actor_id === actor && !['owner', 'astrid-pack-host'].includes(actor)
    && Array.isArray(identity.scopes) && JSON.stringify([...identity.scopes].sort()) === JSON.stringify([...PRODUCT_SCOPES].sort());
}
/**
 * The Runtime named by a discovery file and a product credential file, both read on every call (`currentRuntime()`).
 * `verify` accepts only the realm the gateway started with, under the same scoped product identity.
 */
export function fileRuntimeSource(files: { discoveryPath: string; tokenFile: string; realmId: string; actor: string }): RuntimeSource {
  return {
    read() {
      const { endpoint, token } = currentRuntime(files.discoveryPath, { credentialFile: files.tokenFile });
      return { endpoint: endpoint.href, token };
    },
    async verify(target) {
      const identity = await handshake(target);
      if (identity.realm_id !== files.realmId) throw new RuntimeRefusal('realm_changed', 'The Runtime now answering belongs to a different realm');
      if (!productIdentityMatches(identity, files.actor)) throw new RuntimeRefusal('runtime_identity_mismatch', 'Scoped runtime product identity did not match');
    },
  };
}
async function main() {
  const args = new Map<string, string>();
  for (let i = 2; i < process.argv.length; i += 2) args.set(process.argv[i].replace(/^--/, ''), process.argv[i + 1]);
  for (const name of ['discovery', 'token-file', 'origin']) if (!args.get(name)) throw new Error(`--${name} is required`);
  const discoveryPath = args.get('discovery')!;
  const tokenFile = args.get('token-file')!;
  // Start-up reads the same way every request will; any problem here is a configuration error and ends the process (exit 1).
  const discovery = JSON.parse(readFileSync(discoveryPath, 'utf8')) as Record<string, unknown>;
  const { endpoint: discovered, token } = currentRuntime(discoveryPath, { credentialFile: tokenFile });
  const initial: RuntimeTarget = { endpoint: loopbackEndpoint(discovered.href), token };
  const raw = readFileSync(tokenFile, 'utf8').trim();
  const credential = raw.startsWith('{') ? JSON.parse(raw) as Record<string, unknown> : {};
  const actor = args.get('actor') || (typeof credential.actor_id === 'string' ? credential.actor_id : typeof discovery.actor_id === 'string' ? discovery.actor_id : process.env.REIGH_PAIRED_PRODUCT_ACTOR);
  if (!actor) throw new Error('A scoped product actor is required (--actor or credential actor_id)');
  const identity = await handshake(initial);
  if (!productIdentityMatches(identity, actor) || (discovery.realm_id && discovery.realm_id !== identity.realm_id)) throw new Error('Scoped runtime product identity did not match');
  if (typeof identity.realm_id !== 'string' || !identity.realm_id) throw new Error('Scoped runtime product identity did not match');
  const realmId = identity.realm_id;
  const runtime = { ...fileRuntimeSource({ discoveryPath, tokenFile, realmId, actor }), verified: initial };
  const acpEndpointRaw = args.get('acp-endpoint');
  const acpTokenFile = args.get('acp-token-file');
  let acpToken = process.env.ASTRID_ACP_BRIDGE_TOKEN?.trim();
  if (acpTokenFile) {
    const acpRaw = readFileSync(acpTokenFile, 'utf8').trim();
    const acpCredential = acpRaw.startsWith('{') ? JSON.parse(acpRaw) as Record<string, unknown> : {};
    acpToken = typeof acpCredential.token === 'string' ? acpCredential.token : acpRaw;
  }
  if (acpEndpointRaw && !acpToken) throw new Error('ACP endpoint requires ASTRID_ACP_BRIDGE_TOKEN or --acp-token-file');
  const auditPath = args.get('audit-log');
  const gateway = createLoopbackGateway({ runtime, origin: args.get('origin')!, maxObjectBytes: resolveMaxObjectBytes(process.env.RUNTIME_MAX_OBJECT_BYTES), ...(acpEndpointRaw ? { acpEndpoint: acpEndpointRaw, acpToken } : {}), ...(auditPath ? { audit: (entry: Record<string, unknown>) => appendFileSync(auditPath, `${JSON.stringify(entry)}\n`, { mode: 0o600 }) } : {}) });
  const port = Number(args.get('port') ?? String(DEFAULT_GATEWAY_PORT));
  if (!Number.isInteger(port) || port < 0 || port > 65535) throw new Error('Invalid port');
  gateway.server.once('error', (error: NodeJS.ErrnoException) => {
    void (error.code === 'EADDRINUSE' ? describePortHolder(port, args.get('origin')!) : Promise.resolve(error.message)).then((message) => {
      console.error(message);
      process.exitCode = 1;
    });
  });
  gateway.server.listen(port, '127.0.0.1', () => {
    const address = gateway.server.address();
    if (!address || typeof address === 'string') throw new Error('No loopback address');
    // `base` is the App's Runtime base (`runtimeApiBase()`) under the gateway origin.
    console.log(JSON.stringify({ base: `http://127.0.0.1:${address.port}${gateway.prefix}`, realm_id: realmId, acp: Boolean(acpEndpointRaw) }));
  });
  for (const signal of ['SIGINT', 'SIGTERM'] as const) process.on(signal, () => { gateway.server.close(); gateway.server.closeAllConnections(); });
}
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) main().catch(error => { console.error(error.message); process.exitCode = 1; });
