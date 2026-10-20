/**
 * Journey harness for the same-machine "direct" transport (Plan A, F4).
 *
 *   hosted-style HTTPS origin (production build)  ->  the Runtime's browser door  ->  real Runtime daemon (SQLite)
 *
 * The door is the Runtime's own second listener (astrid-runtime `runtime_protocol/door.py`): nothing from this repo runs
 * between the page and the Runtime.
 *
 * Everything lives in one throwaway temp directory that `stop()` removes. Child processes
 * run in their own process groups and are killed by group.
 */
import { spawn, execFileSync, type ChildProcess } from 'node:child_process';
import { createHash, randomBytes, randomUUID, X509Certificate } from 'node:crypto';
import { createReadStream, existsSync, mkdirSync, mkdtempSync, readFileSync, renameSync, rmSync, statSync, writeFileSync } from 'node:fs';
import { createServer as createHttpsServer, type Server as HttpsServer } from 'node:https';
import { request as httpRequest, type IncomingHttpHeaders } from 'node:http';
import { createServer as createNetServer } from 'node:net';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { deflateSync } from 'node:zlib';
import type { TimelineClip } from '@banodoco/timeline-schema';

const here = path.dirname(fileURLToPath(import.meta.url));
export const REPO_ROOT = path.resolve(here, '../../../..');

/** The door's well-known port (Plan A D1). Override with ASTRID_APP_DIRECT_DOOR_PORT. */
export const DOOR_PORT = Number(process.env.ASTRID_APP_DIRECT_DOOR_PORT ?? 17340);
export const HOSTED_HOST = 'astrid.test';
export const OTHER_HOST = 'evil.test';
export const PRODUCT_ACTOR = 'astrid-e2e-product';
/** The second client of the three-product journey (the Astrid CLI) is its own actor, so the Runtime's history says who wrote what. */
export const ASTRID_ACTOR = 'astrid-f2';
export const PRODUCT_SCOPES = ['handshake', 'projects:read', 'projects:write', 'tasks:read', 'tasks:write', 'objects:read', 'objects:write'];
export const BIG_DOWNLOAD_BYTES = 60 * 1024 * 1024;
export const BIG_UPLOAD_BYTES = 200 * 1024 * 1024;

export const RUNTIME_CHECKOUT = path.resolve(process.env.ASTRID_RUNTIME_CHECKOUT
  ?? [path.join(REPO_ROOT, '..', 'astrid-runtime'), path.join(REPO_ROOT, '../..', 'runtime')]
    .find((dir) => existsSync(path.join(dir, 'runtime_protocol', 'cli.py')))
  ?? path.join(REPO_ROOT, '..', 'astrid-runtime'));
const DIST_DIR = path.resolve(process.env.ASTRID_APP_DIRECT_DIST ?? path.join(REPO_ROOT, 'dist'));

export function runtimePython(): string | null {
  const python = process.env.ASTRID_RUNTIME_PYTHON
    ?? [path.join(RUNTIME_CHECKOUT, '.venv/bin/python'), path.join(RUNTIME_CHECKOUT, '../venv-runtime/bin/python')].find(existsSync);
  return python && existsSync(python) ? python : null;
}

/** Why the harness cannot run here, or null when it can. */
export function harnessUnavailableReason(): string | null {
  if (!runtimePython()) return `Runtime venv not found at ${RUNTIME_CHECKOUT}/.venv (set ASTRID_RUNTIME_CHECKOUT)`;
  if (!existsSync(path.join(DIST_DIR, 'index.html'))) return `no production build at ${DIST_DIR} (run npm run build, or use npm run test:e2e:direct)`;
  try { execFileSync('openssl', ['version'], { stdio: 'ignore' }); } catch { return 'openssl is required to make the test certificate'; }
  return null;
}

export const sha256Hex = (data: Uint8Array) => `sha256:${createHash('sha256').update(data).digest('hex')}`;

// ---------------------------------------------------------------------------------------------
// Process helpers

async function freePort(): Promise<number> {
  return new Promise((resolve, reject) => {
    const server = createNetServer();
    server.once('error', reject);
    server.listen(0, '127.0.0.1', () => {
      const { port } = server.address() as { port: number };
      server.close(() => resolve(port));
    });
  });
}

async function assertPortFree(port: number, what: string): Promise<void> {
  await new Promise<void>((resolve, reject) => {
    const server = createNetServer();
    server.once('error', (error: NodeJS.ErrnoException) => reject(new Error(`${what} port ${port} is not free (${error.code}); stop whatever uses it or set ASTRID_APP_DIRECT_DOOR_PORT`)));
    server.listen(port, '127.0.0.1', () => server.close(() => resolve()));
  });
}

const liveGroups = new Set<number>();
function killGroupSync(pid: number) {
  try { process.kill(-pid, 'SIGKILL'); } catch { /* already gone */ }
}
process.on('exit', () => { for (const pid of liveGroups) killGroupSync(pid); });

export interface Managed {
  child: ChildProcess;
  stdout: string;
  stderr: string;
  exited: Promise<number | null>;
  /** Resolves once the process has ended and its stdout and stderr are fully read (`exited` can come first). */
  closed: Promise<void>;
}

/** Starts `command` in its own process group. `exactEnv` gives it `options.env` alone; otherwise that is laid over this process's environment. */
export function spawnGroup(command: string, args: string[], options: { cwd: string; env?: NodeJS.ProcessEnv; exactEnv?: boolean }): Managed {
  const child = spawn(command, args, { cwd: options.cwd, env: options.exactEnv ? { ...options.env } : { ...process.env, ...options.env }, detached: true, stdio: ['ignore', 'pipe', 'pipe'] });
  if (!child.pid) throw new Error(`could not start ${command}`);
  liveGroups.add(child.pid);
  const managed: Managed = {
    child,
    stdout: '',
    stderr: '',
    exited: new Promise((resolve) => child.once('exit', (code) => { liveGroups.delete(child.pid!); resolve(code); })),
    closed: new Promise((resolve) => child.once('close', () => resolve())),
  };
  child.stdout!.on('data', (chunk) => { managed.stdout += chunk; });
  child.stderr!.on('data', (chunk) => { managed.stderr += chunk; });
  return managed;
}

export async function stopGroup(managed: Managed | undefined, graceMs = 8000): Promise<void> {
  if (!managed) return;
  const { pid, exitCode } = managed.child;
  if (!pid) return;
  if (exitCode === null) {
    try { process.kill(-pid, 'SIGTERM'); } catch { /* already gone */ }
    const timer = setTimeout(() => killGroupSync(pid), graceMs);
    await managed.exited;
    clearTimeout(timer);
  }
  // Reap stragglers (tsx/python helper children) of the group.
  killGroupSync(pid);
  liveGroups.delete(pid);
}

async function waitFor<T>(label: string, probe: () => Promise<T | null | undefined | false>, timeoutMs: number, abort?: () => string | null): Promise<T> {
  const deadline = Date.now() + timeoutMs;
  for (;;) {
    const value = await probe().catch(() => null);
    if (value) return value;
    const aborted = abort?.();
    if (aborted) throw new Error(`${label}: ${aborted}`);
    if (Date.now() > deadline) throw new Error(`${label}: timed out after ${timeoutMs} ms`);
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
}

// ---------------------------------------------------------------------------------------------
// Raw HTTP (so tests can control Host, Origin and Referer exactly)

export interface RawResponse { status: number; headers: IncomingHttpHeaders; body: Buffer; text: string; json: () => any }

export function rawRequest(options: { port: number; path: string; method?: string; headers?: Record<string, string>; body?: Buffer | string; host?: string }): Promise<RawResponse> {
  return new Promise((resolve, reject) => {
    // Content-Length like a browser's fetch (chunked bodies are not what the hosted page sends), one connection per request.
    const headers: Record<string, string> = { Host: options.host ?? `127.0.0.1:${options.port}`, ...(options.body === undefined ? {} : { 'Content-Length': String(Buffer.byteLength(options.body)) }), ...options.headers };
    const req = httpRequest({ hostname: '127.0.0.1', port: options.port, path: options.path, method: options.method ?? 'GET', headers, agent: false }, (res) => {
      const chunks: Buffer[] = [];
      res.on('data', (chunk) => chunks.push(chunk));
      res.on('end', () => {
        const body = Buffer.concat(chunks);
        resolve({ status: res.statusCode ?? 0, headers: res.headers, body, get text() { return body.toString('utf8'); }, json: () => JSON.parse(body.toString('utf8')) });
      });
      res.on('error', reject);
    });
    req.on('error', reject);
    req.end(options.body);
  });
}

// ---------------------------------------------------------------------------------------------
// Certificate and hosted-style static server

function makeCertificate(dir: string) {
  const key = path.join(dir, 'tls.key');
  const cert = path.join(dir, 'tls.crt');
  execFileSync('openssl', ['req', '-x509', '-newkey', 'rsa:2048', '-nodes', '-keyout', key, '-out', cert, '-days', '2', '-subj', `/CN=${HOSTED_HOST}`,
    '-addext', `subjectAltName=DNS:${HOSTED_HOST},DNS:${OTHER_HOST}`], { stdio: 'ignore' });
  const x509 = new X509Certificate(readFileSync(cert));
  const spki = createHash('sha256').update(x509.publicKey.export({ type: 'spki', format: 'der' })).digest('base64');
  return { key: readFileSync(key), cert: readFileSync(cert), spki };
}

const MIME: Record<string, string> = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.mjs': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.ico': 'image/x-icon',
  '.woff': 'font/woff', '.woff2': 'font/woff2', '.mp4': 'video/mp4', '.webm': 'video/webm', '.wasm': 'application/wasm', '.map': 'application/json', '.txt': 'text/plain',
};

/** What the hosted site's `/runtime-config/v1/extensions.json` answers (the deployment writes it; extensionReleaseControls.ts parses it, and any drift closes every extension). */
export type ExtensionsConfigMode = 'on' | 'missing';
export const EXTENSIONS_CONFIG_PATH = '/runtime-config/v1/extensions.json';
export const EXTENSIONS_CONFIG = {
  schemaVersion: 1,
  revision: 'direct-journey',
  extensions: { hostEnabled: true, transcriptCaptionFoundryEnabled: true, runawayTypedTimelineEnabled: false },
} as const;

function startHostedServer(tls: { key: Buffer; cert: Buffer }, port: number, extensionsConfig: () => ExtensionsConfigMode): Promise<HttpsServer> {
  const root = DIST_DIR;
  const server = createHttpsServer(tls, (req, res) => {
    const url = new URL(req.url ?? '/', 'https://placeholder.invalid');
    const send = (status: number, type: string, body: string) => { res.writeHead(status, { 'Content-Type': type, 'Cache-Control': 'no-store' }); res.end(body); };
    // The deployed site serves the release config as a static file; a missing file is the closed posture (every extension off).
    if (url.pathname === EXTENSIONS_CONFIG_PATH && extensionsConfig() === 'on') return send(200, 'application/json', JSON.stringify(EXTENSIONS_CONFIG));
    // The hosted origin has no Runtime proxy; same-origin API paths do not exist there.
    if (url.pathname.startsWith('/api/') || url.pathname.startsWith('/runtime-config/')) return send(404, 'application/json', '{"error":"no_proxy_on_hosted_origin"}');
    if (url.pathname === '/__blank.html') return send(200, 'text/html; charset=utf-8', '<!doctype html><title>blank</title><body></body>');
    let file = path.join(root, decodeURIComponent(url.pathname));
    if (!file.startsWith(root + path.sep) && file !== root) return send(403, 'text/plain', 'forbidden');
    const isFile = () => { try { return statSync(file).isFile(); } catch { return false; } };
    if (!isFile()) {
      if (path.extname(url.pathname)) return send(404, 'text/plain', 'not found');
      file = path.join(root, 'index.html'); // SPA fallback
    }
    const cacheable = file.includes(`${path.sep}assets${path.sep}`);
    res.writeHead(200, { 'Content-Type': MIME[path.extname(file)] ?? 'application/octet-stream', 'Content-Length': statSync(file).size, 'Cache-Control': cacheable ? 'public, max-age=3600' : 'no-store' });
    createReadStream(file).pipe(res);
  });
  return new Promise((resolve, reject) => { server.once('error', reject); server.listen(port, '127.0.0.1', () => resolve(server)); });
}

// ---------------------------------------------------------------------------------------------
// Fixture media

function crc32(buffer: Buffer): number {
  let crc = ~0;
  for (const byte of buffer) { crc ^= byte; for (let k = 0; k < 8; k++) crc = (crc >>> 1) ^ (0xedb88320 & -(crc & 1)); }
  return ~crc >>> 0;
}

/** A real, decodable gradient PNG. */
export function makePng(width = 64, height = 48): Buffer {
  const chunk = (type: string, data: Buffer) => {
    const head = Buffer.alloc(4); head.writeUInt32BE(data.length);
    const body = Buffer.concat([Buffer.from(type), data]);
    const tail = Buffer.alloc(4); tail.writeUInt32BE(crc32(body));
    return Buffer.concat([head, body, tail]);
  };
  const ihdr = Buffer.alloc(13); ihdr.writeUInt32BE(width, 0); ihdr.writeUInt32BE(height, 4); ihdr[8] = 8; ihdr[9] = 2;
  const rows: Buffer[] = [];
  for (let y = 0; y < height; y++) {
    const row = Buffer.alloc(1 + width * 3);
    for (let x = 0; x < width; x++) { row[1 + x * 3] = (x * 255 / width) | 0; row[2 + x * 3] = (y * 255 / height) | 0; row[3 + x * 3] = 128; }
    rows.push(row);
  }
  return Buffer.concat([Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]), chunk('IHDR', ihdr), chunk('IDAT', deflateSync(Buffer.concat(rows))), chunk('IEND', Buffer.alloc(0))]);
}

/** A few-second VP8 clip when ffmpeg exists (decodable in stock Chromium); otherwise a repo MP4 that only exercises bytes and Range. */
function makeVideo(dir: string): { data: Buffer; mediaType: string; decodable: boolean } {
  const out = path.join(dir, 'clip.webm');
  try {
    execFileSync('ffmpeg', ['-loglevel', 'error', '-y', '-f', 'lavfi', '-i', 'testsrc=size=320x180:rate=15:duration=12', '-c:v', 'libvpx', '-b:v', '600k', '-g', '15', out], { stdio: 'ignore', timeout: 60_000 });
    return { data: readFileSync(out), mediaType: 'video/webm', decodable: true };
  } catch {
    return { data: readFileSync(path.join(REPO_ROOT, 'src/pages/Home/light-study-assets/first-light.mp4')), mediaType: 'video/mp4', decodable: false };
  }
}

// ---------------------------------------------------------------------------------------------

export interface SeededObject { objectId: string; digest: string; size: number; mediaType: string }
export interface Seed {
  projectId: string;
  projectName: string;
  timelineId: string;
  headRevisionId: string;
  image: SeededObject;
  video: SeededObject & { decodable: boolean };
  big: SeededObject;
}

export function compositionPublication(seed: { projectId: string; timelineId: string }, expectedHead: string | null, name: string, fps: number) {
  return {
    project_id: seed.projectId,
    timeline_id: seed.timelineId,
    expected_head: expectedHead,
    parent_revision_id: randomUUID(),
    parent_composition: {
      slug: 'main',
      name,
      config: { output: { resolution: '1280x720', fps, file: 'out.mp4' }, clips: [] as TimelineClip[], tracks: [{ id: 'V1', kind: 'visual', label: 'V1' }] },
      registry: { assets: {} },
      clips: [] as TimelineClip[],
      occurrences: [],
    },
    shot_revisions: [],
    internal_timeline_revisions: [],
  };
}

/** One timeline that shows what the bundled pack extensions draw: a transcript lane over a media clip, and a live-scene clip. */
export interface ExtensionsSeed {
  projectSlug: string;
  timelineId: string;
  /** The transcript segments' text, in time order (the lane shows each as a chip). */
  transcriptTexts: string[];
  sceneClipId: string;
  /** The media clip that carries the transcript (its asset is the seeded video). */
  speechClipId: string;
  /** Text the scene's own page draws; the case reads it back from inside the sandboxed iframe. */
  sceneMarker: string;
  /** The live-scene package as a Runtime project object (the clip carries its inline copy). */
  scenePackage: SeededObject;
  sceneEntry: SeededObject;
}

/** One timeline whose clips are the seeded image and the seeded video, so the editor draws both through the door. */
export interface MediaSeed {
  projectSlug: string;
  timelineId: string;
  imageClipId: string;
  videoClipId: string;
}

/** The fields of `<support>/discovery.json` the journeys read (the Runtime writes more). The credential files named here are the owner's and the worker's, never the product's. */
export interface RuntimeDiscovery {
  endpoint: string;
  active_realm: string;
  runtime_instance_id: string;
  worker_credential_file: string;
  /** The actor the worker credential belongs to; an executor registered with it must carry this id. */
  worker_actor: string;
  [key: string]: unknown;
}

/** What `seedThreeProducts` made. */
export interface ThreeProductsSeed {
  projectSlug: string;
  /** The harness's own seeded timeline: the seed is published onto it, so the editor still opens the only project and timeline. */
  timelineId: string;
  /** The head the seed produced; `seed.headRevisionId` stays the empty timeline it was published onto. */
  headRevisionId: string;
  appClipId: string;
  agentClipId: string;
  transitionClipId: string;
  agentClearClipId: string;
  /** The shot the agent's clips live in, and its occurrence in the parent composition (the App draws it as one block). */
  shotId: string;
  occurrenceId: string;
  /** The key the agent names for a task output (`--swap-asset f2-marker=task:T/marker#0`). It is new: the CLI refuses a key that already names other media. */
  markerAssetKey: string;
  /** Opaque data neither client models; every later revision must carry both unchanged. */
  opaque: { config: Record<string, unknown>; clip: Record<string, unknown> };
}

export const THREE_PRODUCTS_OPAQUE = {
  config: { owner: 'f2', nested: [1, { k: 'v' }], flag: true },
  clip: { owner: 'f2', nested: [1, { k: 'v' }] },
} as const;

/** Keep the App's reference sibling clear of the A5/B7 moves on the same track. */
export const THREE_PRODUCTS_REFERENCE_AT = 15;

const SCENE_MARKER = 'journey-scene';

/** The smallest entry page the validator accepts: a `<head>` for the CSP, a `<body>` for the bridge, and `window.astridScene`. */
function sceneEntryHtml(): string {
  return `<!doctype html><html><head><meta charset="utf-8"><title>journey scene</title></head><body style="margin:0;background:#123"><div id="scene" style="color:#fff;font:16px monospace"></div><script>
window.astridScene = {
  async initialize() {},
  async render(frame) { document.getElementById('scene').textContent = '${SCENE_MARKER} t=' + frame.sourceTime.toFixed(2); },
  dispose() {},
};
</script></body></html>`;
}

export class DirectHarness {
  tmp = '';
  origin = '';
  originPort = 0;
  otherOrigin = '';
  spki = '';
  runtimePort = 0;
  runtimeInstanceId = '';
  realmId = '';
  seed!: Seed;
  productToken = '';
  readonly doorPort = DOOR_PORT;
  private runtime?: Managed;
  private https?: HttpsServer;
  private stopped = false;
  private extensionsMode: ExtensionsConfigMode = 'on';
  private extensionsSeed?: ExtensionsSeed;
  private mediaSeed?: MediaSeed;
  private threeProductsSeed?: ThreeProductsSeed;
  private timelineAuthoring = false;
  private authoringPython?: string;

  /** The hosted site's extension release config: on by default, as deployed; a case sets 'missing' to see the closed posture. */
  get extensionsConfig(): ExtensionsConfigMode { return this.extensionsMode; }
  set extensionsConfig(mode: ExtensionsConfigMode) { this.extensionsMode = mode; }

  get realmDir() { return path.join(this.tmp, 'realm'); }
  get supportDir() { return path.join(this.tmp, 'support'); }
  get auditPath() { return path.join(this.tmp, 'door-audit.jsonl'); }
  /** The product credential the door acts with, as `astrid-runtime up` would provision it. */
  get credentialPath() { return path.join(this.tmp, 'product-credential.json'); }
  /** The App's Runtime base (`runtimeApiBase()`) under the door's origin. */
  get doorBase() { return `http://127.0.0.1:${this.doorPort}${this.doorPrefix}`; }
  get doorPrefix() { return '/api/runtime'; }

  /** Browser context options: the local-network permission is granted (the prompt itself is a manual-checklist item). */
  get contextOptions() {
    return { permissions: ['local-network-access'] as string[] };
  }

  /** Chromium arguments: host mapping, a pinned test certificate, and the hosted origin treated as a public address. */
  get chromiumArgs(): string[] {
    return [
      '--no-sandbox',
      '--disable-dev-shm-usage',
      '--no-proxy-server', // the sandbox's HTTPS_PROXY must not capture the hosted-style origin
      `--host-resolver-rules=MAP ${HOSTED_HOST} 127.0.0.1, MAP ${OTHER_HOST} 127.0.0.1, MAP *.supabase.co 127.0.0.1:1, MAP *.supabase.in 127.0.0.1:1`,
      `--ignore-certificate-errors-spki-list=${this.spki}`,
      // The hosted origin resolves to loopback here, so without this override Chromium would treat the page as
      // local and skip the public -> loopback (Private Network Access / local network) checks that production hits.
      `--ip-address-space-overrides=127.0.0.1:${this.originPort}=public`,
    ];
  }

  async start(): Promise<this> {
    process.on('SIGTERM', () => { void this.stop().finally(() => process.exit(143)); });
    try {
      this.tmp = mkdtempSync(path.join(tmpdir(), 'astrid-direct-'));
      await assertPortFree(this.doorPort, 'door');
      const tls = makeCertificate(this.tmp);
      this.spki = tls.spki;
      this.originPort = Number(process.env.ASTRID_APP_DIRECT_ORIGIN_PORT ?? 0) || await freePort();
      this.https = await startHostedServer(tls, this.originPort, () => this.extensionsMode);
      this.origin = `https://${HOSTED_HOST}:${this.originPort}`;
      this.otherOrigin = `https://${OTHER_HOST}:${this.originPort}`;

      mkdirSync(this.supportDir, { recursive: true, mode: 0o700 });
      this.realmId = await this.createRealm();
      await this.startRuntime();
      // The door listens from the start and answers `runtime_unavailable` until the product credential exists.
      this.productToken = await this.provisionCredential(PRODUCT_ACTOR, path.basename(this.credentialPath));
      this.seed = await this.seedRuntime();
    } catch (error) {
      await this.stop();
      throw error;
    }
    return this;
  }

  // -- Runtime -------------------------------------------------------------------------------

  private runtimeEnv(): NodeJS.ProcessEnv {
    const agent = path.resolve(process.env.ASTRID_CHECKOUT
      ?? [path.join(REPO_ROOT, '..', 'astrid-agent'), path.join(REPO_ROOT, '../..', 'agent')]
        .find((dir) => existsSync(path.join(dir, 'astrid', '__init__.py')))
      ?? path.join(REPO_ROOT, '..', 'astrid-agent'));
    return { PYTHONDONTWRITEBYTECODE: '1', PYTHONUNBUFFERED: '1', PYTHONPATH: [RUNTIME_CHECKOUT, agent].join(path.delimiter) };
  }

  /** Seed with main's APIs first; startup verifies their original publication provenance. */
  async enableTimelineAuthoring(python: string): Promise<void> {
    if (this.timelineAuthoring) return;
    await this.stopRuntime();
    if (!existsSync(python)) throw new Error(`Authoring Python not found at ${python}`);
    this.authoringPython = python;
    this.timelineAuthoring = true;
    await this.startRuntime();
  }

  private async createRealm(): Promise<string> {
    const output = execFileSync(runtimePython()!, ['-m', 'runtime_protocol.cli', 'create', '--root', this.realmDir, '--display-name', 'Direct Journey'], { cwd: this.tmp, env: { ...process.env, ...this.runtimeEnv() }, encoding: 'utf8' });
    return JSON.parse(output.trim().split('\n').pop()!).realm_id;
  }

  /**
   * Starts the daemon the way `astrid-runtime up` does: port 0, so every start gets a new port (discovery is rewritten by the
   * Runtime), and the browser door for the hosted origin on its fixed port, acting with the product credential.
   */
  async startRuntime(port = 0): Promise<void> {
    if (this.runtime) throw new Error('Runtime already running');
    const managed = spawnGroup(this.authoringPython ?? runtimePython()!, ['-m', 'runtime_protocol.cli', 'start', '--root', this.realmDir, '--support-root', this.supportDir, '--port', String(port), '--display-name', 'Direct Journey',
      '--door-origin', this.origin, '--door-port', String(this.doorPort), '--door-credential-file', this.credentialPath, '--door-audit-log', this.auditPath,
      ...(this.timelineAuthoring ? ['--authoring-profile', 'astrid'] : [])], { cwd: this.tmp, env: this.runtimeEnv() });
    this.runtime = managed;
    const endpoint = await waitFor<string>('Runtime start', async () => {
      const line = managed.stdout.split('\n').find((candidate) => candidate.trim().startsWith('{') && candidate.includes('"endpoint"'));
      return line ? JSON.parse(line).endpoint : null;
    }, 60_000, () => (managed.child.exitCode !== null ? `Runtime exited ${managed.child.exitCode}: ${managed.stdout.slice(-800)}${managed.stderr.slice(-800)}` : null));
    this.runtimePort = Number(new URL(endpoint).port);
    const health = await waitFor<any>('Runtime health', async () => {
      const response = await fetch(`${endpoint}/v1/health`);
      return response.ok ? response.json() : null;
    }, 30_000);
    this.runtimeInstanceId = health.runtime_instance_id;
  }

  async stopRuntime(): Promise<void> {
    await stopGroup(this.runtime);
    this.runtime = undefined;
  }

  /** Stops the daemon and starts it again on a different port, as the launcher's fresh start does. */
  async restartRuntime(): Promise<{ oldPort: number; oldInstanceId: string }> {
    const previous = { oldPort: this.runtimePort, oldInstanceId: this.runtimeInstanceId };
    await this.stopRuntime();
    let port = await freePort();
    while (port === previous.oldPort) port = await freePort();
    await this.startRuntime(port);
    return previous;
  }

  get runtimeRunning() { return Boolean(this.runtime && this.runtime.child.exitCode === null); }

  get runtimeUrl() { return `http://127.0.0.1:${this.runtimePort}`; }

  /** A request straight to the Runtime with the product credential (the "direct" side of every comparison). */
  async runtimeFetch(pathAndQuery: string, init: RequestInit & { headers?: Record<string, string> } = {}): Promise<Response> {
    return fetch(`${this.runtimeUrl}${pathAndQuery}`, { ...init, headers: { Authorization: `Bearer ${this.productToken}`, ...init.headers } });
  }

  async runtimeJson<T = any>(method: string, pathAndQuery: string, body?: unknown, extra: Record<string, string> = {}): Promise<{ status: number; body: T }> {
    const response = await this.runtimeFetch(pathAndQuery, {
      method,
      headers: { ...(body === undefined ? {} : { 'Content-Type': 'application/json' }), ...(method === 'GET' ? {} : { 'Idempotency-Key': randomUUID() }), ...extra },
      body: body === undefined ? undefined : JSON.stringify(body),
    });
    return { status: response.status, body: await response.json().catch(() => null) as T };
  }

  /**
   * A credential for `actorId`, minted through the Runtime's own route with the owner credential and written to
   * `<tmp>/<file>` as `{token, actor_id}`, mode 0600 (the shape the door's `--door-credential-file` and Astrid's reader accept).
   * Returns the token; it never leaves Node memory and that file, and the hosted server serves neither.
   */
  async provisionCredential(actorId: string, file: string): Promise<string> {
    const owner = readFileSync(path.join(this.supportDir, 'credentials', 'owner.token'), 'utf8').trim();
    const token = `${actorId.slice(0, 8)}-${randomBytes(24).toString('base64url')}`;
    const response = await fetch(`${this.runtimeUrl}/v1/credentials`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${owner}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ actor_id: actorId, credential: token, scope: 'astrid' }),
    });
    if (response.status !== 201) throw new Error(`credential provisioning for ${actorId} failed: ${response.status} ${await response.text()}`);
    writeFileSync(path.join(this.tmp, file), JSON.stringify({ version: 1, scope: 'astrid', token, actor_id: actorId }), { mode: 0o600 });
    return token;
  }

  /**
   * What the Runtime last published about itself (`<support>/discovery.json`, rewritten on every start). Every Astrid call
   * re-reads it, so a restarted Runtime on a new port is followed with no special case. Throws when it is absent or unparsable.
   */
  discovery(): RuntimeDiscovery {
    const parsed = JSON.parse(readFileSync(path.join(this.supportDir, 'discovery.json'), 'utf8'));
    for (const key of ['endpoint', 'active_realm', 'runtime_instance_id', 'worker_credential_file', 'worker_actor'] as const) {
      if (typeof parsed[key] !== 'string' || !parsed[key]) throw new Error(`discovery.json has no ${key}`);
    }
    return parsed as RuntimeDiscovery;
  }

  private async seedRuntime(): Promise<Seed> {
    const projectName = `Direct Journey ${randomBytes(3).toString('hex')}`;
    const project = await this.runtimeJson('POST', '/v1/projects', { name: projectName });
    if (project.status !== 201) throw new Error(`seed project: ${project.status} ${JSON.stringify(project.body)}`);
    const projectId: string = project.body.data.project_id;
    const timelineId = randomUUID();
    const published = await this.runtimeJson('POST', `/v1/projects/${projectId}/timelines/${timelineId}/composition-revisions`, compositionPublication({ projectId, timelineId }, null, 'Main', 30));
    if (published.status !== 200) throw new Error(`seed timeline: ${published.status} ${JSON.stringify(published.body)}`);
    const ingest = async (data: Buffer, mediaType: string, filename: string): Promise<SeededObject> => {
      const response = await this.runtimeFetch(`/v1/projects/${projectId}/objects`, { method: 'POST', headers: { 'Content-Type': mediaType, 'Idempotency-Key': randomUUID(), 'X-Original-Name': filename }, body: new Uint8Array(data) });
      if (response.status !== 201 && response.status !== 200) throw new Error(`seed ${filename}: ${response.status} ${await response.text()}`);
      const body = await response.json();
      if (body.data.digest !== sha256Hex(data)) throw new Error(`seed ${filename}: Runtime digest differs from local digest`);
      return { objectId: body.data.object_id, digest: body.data.digest, size: data.length, mediaType };
    };
    const video = makeVideo(this.tmp);
    const big = randomBytes(BIG_DOWNLOAD_BYTES);
    return {
      projectId, projectName, timelineId,
      headRevisionId: published.body.data.new_head,
      image: await ingest(makePng(), 'image/png', 'gradient.png'),
      video: { ...(await ingest(video.data, video.mediaType, `clip.${video.mediaType === 'video/webm' ? 'webm' : 'mp4'}`)), decodable: video.decodable },
      big: await ingest(big, 'application/octet-stream', 'big-60mb.bin'),
    };
  }

  /**
   * A second timeline in the seeded project for the pack extensions, made on first use (after the cases that open the
   * seeded timeline, so none of them sees a second timeline): one media clip with a transcript lane over it, and one
   * live-scene clip whose package is a Runtime project object, published as one composition revision.
   */
  async seedExtensions(): Promise<ExtensionsSeed> {
    if (this.extensionsSeed) return this.extensionsSeed;
    const { projectId, video } = this.seed;
    const project = await this.runtimeJson('GET', `/v1/projects/${projectId}`);
    if (project.status !== 200) throw new Error(`seed extensions project: ${project.status} ${JSON.stringify(project.body)}`);
    const ingest = async (text: string, mediaType: string, filename: string): Promise<SeededObject & { filename: string }> => {
      const data = Buffer.from(text, 'utf8');
      const response = await this.runtimeFetch(`/v1/projects/${projectId}/objects`, { method: 'POST', headers: { 'Content-Type': mediaType, 'Idempotency-Key': randomUUID(), 'X-Original-Name': filename }, body: new Uint8Array(data) });
      if (response.status !== 201 && response.status !== 200) throw new Error(`seed ${filename}: ${response.status} ${await response.text()}`);
      const body = await response.json();
      if (body.data.digest !== sha256Hex(data)) throw new Error(`seed ${filename}: Runtime digest differs from local digest`);
      return { objectId: body.data.object_id, digest: body.data.digest, size: data.length, mediaType, filename };
    };
    const html = sceneEntryHtml();
    const entry = await ingest(html, 'text/html', 'scene.html');
    // The package object: validateScenePackage (ui/live-scenes/runtime.ts) wants the manifest, the entry's object metadata and an assets array.
    const packageBody = JSON.stringify({
      manifest: { formatVersion: 1, entry: 'scene.html', duration: 5, authoredFps: 30 },
      entry: { object_id: entry.objectId, digest: entry.digest, media_type: entry.mediaType, size: entry.size, filename: entry.filename },
      assets: [],
    });
    const scenePackage = await ingest(packageBody, 'application/json', 'scene.package.json');
    const liveScene = { revision: scenePackage.digest, source: { objectId: scenePackage.objectId, revision: scenePackage.digest }, packageBody, html };

    const transcriptTexts = ['Words arrive through the door', 'then the lane draws them', 'one chip for each segment'];
    const assetKey = 'journey-speech';
    const bundle = {
      schema_version: 1,
      itemsBySchemaRef: {
        'astrid.transcript_segment/v1': transcriptTexts.map((text, index) => ({
          id: `transcript-source:${assetKey}:segment:${index}`,
          shape: 'interval', domain: 'source_seconds', extent: { start: index * 2, end: index * 2 + 2 },
          schemaRef: 'astrid.transcript_segment/v1',
          payload: { text },
          sourceArtifactRef: { assetId: assetKey },
          provenance: { adapterId: 'astrid.adaptTranscript', adapterVersion: '2' },
        })),
      },
    };
    const sceneClipId = 'journey-scene-clip';
    const speechClipId = 'journey-speech-clip';
    const clips = [
      // The scene fills the first five seconds; the media clip (the transcript's carrier) follows it on the same track.
      { id: sceneClipId, at: 0, track: 'V1', clipType: 'haus.astrid.liveScene', from: 0, to: 5, speed: 1, app: { liveScene } },
      { id: speechClipId, at: 5, track: 'V1', clipType: 'media', asset: assetKey, from: 0, to: 6, speed: 1 },
    ];
    const registry = { assets: { [assetKey]: { file: 'journey-speech.webm', type: 'video', duration: 12, media_id: video.objectId, content_sha256: video.digest } } };
    const timelineId = randomUUID();
    const publication = compositionPublication({ projectId, timelineId }, null, 'Extensions', 30);
    publication.parent_composition.config = { ...publication.parent_composition.config, clips, bundle } as typeof publication.parent_composition.config;
    publication.parent_composition.clips = clips as unknown as typeof publication.parent_composition.clips;
    publication.parent_composition.registry = registry as unknown as typeof publication.parent_composition.registry;
    const published = await this.runtimeJson('POST', `/v1/projects/${projectId}/timelines/${timelineId}/composition-revisions`, publication);
    if (published.status !== 200) throw new Error(`seed extensions timeline: ${published.status} ${JSON.stringify(published.body)}`);
    this.extensionsSeed = { projectSlug: (project.body.data ?? project.body).slug, timelineId, transcriptTexts, sceneClipId, speechClipId, sceneMarker: SCENE_MARKER, scenePackage, sceneEntry: entry };
    return this.extensionsSeed;
  }

  /**
   * A timeline in the seeded project whose two clips use the seeded image and video objects (registry `media_id`), made on first
   * use after the cases that open the seeded timeline (like `seedExtensions`, so none of them sees another timeline). The editor
   * resolves each asset to a door object URL and draws the image clip's thumbnail from it.
   */
  async seedMedia(): Promise<MediaSeed> {
    if (this.mediaSeed) return this.mediaSeed;
    const { projectId, image, video } = this.seed;
    const project = await this.runtimeJson('GET', `/v1/projects/${projectId}`);
    if (project.status !== 200) throw new Error(`seed media project: ${project.status} ${JSON.stringify(project.body)}`);
    const imageKey = 'journey-image';
    const videoKey = 'journey-video';
    const imageClipId = 'journey-image-clip';
    const videoClipId = 'journey-video-clip';
    const clips = [
      { id: imageClipId, at: 0, track: 'V1', clipType: 'media', asset: imageKey, from: 0, to: 5, speed: 1 },
      { id: videoClipId, at: 5, track: 'V1', clipType: 'media', asset: videoKey, from: 0, to: 5, speed: 1 },
    ];
    const registry = {
      assets: {
        [imageKey]: { file: 'journey-image.png', type: 'image/png', media_id: image.objectId, content_sha256: image.digest },
        [videoKey]: { file: `journey-video.${video.mediaType === 'video/webm' ? 'webm' : 'mp4'}`, type: video.mediaType, duration: 12, media_id: video.objectId, content_sha256: video.digest },
      },
    };
    const timelineId = randomUUID();
    const publication = compositionPublication({ projectId, timelineId }, null, 'Media', 30);
    publication.parent_composition.config = { ...publication.parent_composition.config, clips } as typeof publication.parent_composition.config;
    publication.parent_composition.clips = clips as unknown as typeof publication.parent_composition.clips;
    publication.parent_composition.registry = registry as unknown as typeof publication.parent_composition.registry;
    const published = await this.runtimeJson('POST', `/v1/projects/${projectId}/timelines/${timelineId}/composition-revisions`, publication);
    if (published.status !== 200) throw new Error(`seed media timeline: ${published.status} ${JSON.stringify(published.body)}`);
    this.mediaSeed = { projectSlug: (project.body.data ?? project.body).slug, timelineId, imageClipId, videoClipId };
    return this.mediaSeed;
  }

  /**
   * The three-product seed, made once on first use: the next revision of the harness's own seeded timeline (so the editor still
   * opens the only project and timeline by itself), with one clip per writer so a correct merge never touches the same clip twice,
   * and two opaque fields neither client models (`config.x_f2_opaque`, and `app.f2Opaque` on the agent's clip).
   *
   * Two kinds of clip, because the two products reach different ones. The App edits the parent composition's own clips
   * (`f2-app-clip`, `f2-transition-clip`, track `V1`, drawn as clips). The Astrid CLI addresses only clips inside a placed shot's
   * internal timeline (astrid/sdk/timeline/lookup.py `clips`), so the agent's clips (`f2-agent-clip`, `f2-agent-clear-clip`) live in
   * the shot `f2-shot` (occurrence on parent track `S1`, 0 s to 12 s), which the App draws as one block, not as its clips. The shot
   * also holds a full-length `f2-plate` so the film stays covered when the agent clears an asset (Astrid refuses to publish a gap).
   */
  async seedThreeProducts(referenceAt = THREE_PRODUCTS_REFERENCE_AT): Promise<ThreeProductsSeed> {
    if (this.threeProductsSeed) return this.threeProductsSeed;
    const { projectId, timelineId, image, video, headRevisionId } = this.seed;
    const project = await this.runtimeJson('GET', `/v1/projects/${projectId}`);
    if (project.status !== 200) throw new Error(`seed three products project: ${project.status} ${JSON.stringify(project.body)}`);
    const ids = { appClipId: 'f2-app-clip', agentClipId: 'f2-agent-clip', transitionClipId: 'f2-transition-clip', agentClearClipId: 'f2-agent-clear-clip' };
    const markerAssetKey = 'f2-marker';
    const videoExtension = video.mediaType === 'video/webm' ? 'webm' : 'mp4';
    const imageAsset = (name: string) => ({ file: `${name}.png`, type: 'image/png', media_id: image.objectId, content_sha256: image.digest });
    const videoAsset = { file: `f2-video.${videoExtension}`, type: video.mediaType, duration: 12, media_id: video.objectId, content_sha256: video.digest };
    // The App's clips are the parent composition's own (the editor changes only the parent). The Astrid CLI reaches clips only
    // inside a placed shot's internal timeline (astrid/sdk/timeline/lookup.py `clips`), so the agent's two clips live in a shot
    // placed independently: 0 s to 12 s on the film, clips at 3 s and 6 s inside it.
    const shotId = 'f2-shot';
    const internalRevisionId = randomUUID();
    const shotRevisionId = randomUUID();
    const parentClips = [
      { id: ids.appClipId, at: 0, track: 'V1', clipType: 'media', asset: 'f2-app', from: 0, to: 3, speed: 1 },
      { id: ids.transitionClipId, at: referenceAt, track: 'V1', clipType: 'media', asset: 'f2-video', from: 0, to: 3, speed: 1, transition: { type: 'crossfade', duration: 0.5 } },
    ];
    const shotClips = [
      { id: 'f2-plate', at: 0, track: 'plate', clipType: 'media', asset: 'f2-plate', hold: 12 },
      { id: ids.agentClipId, at: 3, track: 'V2', clipType: 'media', asset: 'f2-placeholder', hold: 3, app: { f2Opaque: THREE_PRODUCTS_OPAQUE.clip } },
      { id: ids.agentClearClipId, at: 6, track: 'V2', clipType: 'media', asset: 'f2-clear', hold: 3 },
    ];
    const publication = compositionPublication({ projectId, timelineId }, headRevisionId, 'Main', 30);
    publication.parent_composition.config = { ...publication.parent_composition.config, clips: parentClips, tracks: [{ id: 'V1', kind: 'visual', label: 'V1' }, { id: 'S1', kind: 'visual', label: 'S1' }], x_f2_opaque: THREE_PRODUCTS_OPAQUE.config } as unknown as typeof publication.parent_composition.config;
    publication.parent_composition.clips = parentClips as unknown as typeof publication.parent_composition.clips;
    publication.parent_composition.registry = { assets: { 'f2-app': imageAsset('f2-app'), 'f2-video': videoAsset } } as unknown as typeof publication.parent_composition.registry;
    Object.assign(publication, {
      internal_timeline_revisions: [{
        timeline_id: timelineId,
        revision_id: internalRevisionId,
        payload: {
          tracks: [{ id: 'plate', kind: 'visual', label: 'plate' }, { id: 'V2', kind: 'visual', label: 'V2' }],
          clips: shotClips, effects: [], audio: [], layout: {},
          registry: { assets: { 'f2-plate': imageAsset('f2-plate'), 'f2-placeholder': imageAsset('f2-placeholder'), 'f2-clear': imageAsset('f2-clear') } },
          assets: [],
        },
      }],
      shot_revisions: [{
        shot_id: shotId,
        revision_id: shotRevisionId,
        internal_timeline_revision_id: internalRevisionId,
        payload: { metadata: { title: 'F2 agent shot' }, items: [], pools: [], selected_variants: {}, provenance: {}, generation_inputs: {}, audio_bindings: [], text_bindings: [] },
      }],
    });
    (publication.parent_composition as Record<string, unknown>).occurrences = [{
      occurrence_id: 'f2-occurrence', shot_id: shotId, shot_revision_id: shotRevisionId,
      placement: { start_ms: 0 }, source_offset: 0, duration_ms: 12000, speed: 1, track: 'S1', transform: {}, gain: 1, mute: false, provenance: {},
    }];
    const published = await this.runtimeJson('POST', `/v1/projects/${projectId}/timelines/${timelineId}/composition-revisions`, publication);
    if (published.status !== 200) throw new Error(`seed three products timeline: ${published.status} ${JSON.stringify(published.body)}`);
    this.threeProductsSeed = {
      projectSlug: (project.body.data ?? project.body).slug, timelineId, headRevisionId: published.body.data.new_head,
      ...ids, shotId, occurrenceId: 'f2-occurrence', markerAssetKey, opaque: { config: { ...THREE_PRODUCTS_OPAQUE.config }, clip: { ...THREE_PRODUCTS_OPAQUE.clip } },
    };
    return this.threeProductsSeed;
  }

  // -- Door ----------------------------------------------------------------------------------

  /**
   * Takes the product credential away from the door, so it listens but is not ready (`runtime_unavailable`), as before
   * `astrid-runtime up` has provisioned it. `restoreProductCredential` gives it back; nothing restarts.
   */
  withdrawProductCredential(): void {
    renameSync(this.credentialPath, `${this.credentialPath}.withdrawn`);
  }

  restoreProductCredential(): void {
    if (existsSync(`${this.credentialPath}.withdrawn`)) renameSync(`${this.credentialPath}.withdrawn`, this.credentialPath);
  }

  /** Resident memory of the Runtime process, which serves the door, in bytes (Linux). */
  runtimeRssBytes(): number {
    try {
      const status = readFileSync(`/proc/${this.runtime?.child.pid}/status`, 'utf8');
      return Number(/VmRSS:\s+(\d+) kB/.exec(status)?.[1] ?? 0) * 1024;
    } catch { return 0; }
  }

  /** Samples the Runtime's RSS while `work` runs; returns its result and the peak growth over the starting RSS. */
  async withRssSampling<T>(work: () => Promise<T>): Promise<{ result: T; baselineBytes: number; peakBytes: number; growthBytes: number }> {
    const baselineBytes = this.runtimeRssBytes();
    let peakBytes = baselineBytes;
    const timer = setInterval(() => { peakBytes = Math.max(peakBytes, this.runtimeRssBytes()); }, 25);
    try {
      const result = await work();
      peakBytes = Math.max(peakBytes, this.runtimeRssBytes());
      return { result, baselineBytes, peakBytes, growthBytes: peakBytes - baselineBytes };
    } finally { clearInterval(timer); }
  }

  /** What the door judged and served, from its own audit log. */
  audit(): Array<{ method: string; path: string; origin: string | null; status: number; response_bytes: number }> {
    try { return readFileSync(this.auditPath, 'utf8').split('\n').filter(Boolean).map((line) => JSON.parse(line)); } catch { return []; }
  }

  /**
   * A request to the door as the hosted page would send it (the hosted Origin, Host 127.0.0.1:<port>); nothing else is needed.
   * `pathUnderBase` is appended to the Runtime base `/api/runtime`; with `fromRoot` it is the whole path (for `/api/astrid/...` and paths outside both).
   */
  doorRequest(pathUnderBase: string, init: { method?: string; headers?: Record<string, string>; body?: Buffer | string; host?: string; origin?: string | null; fromRoot?: boolean } = {}) {
    const headers: Record<string, string> = { ...init.headers };
    if (init.origin !== null) headers.Origin = init.origin ?? this.origin;
    return rawRequest({ port: this.doorPort, path: init.fromRoot ? pathUnderBase : `${this.doorPrefix}${pathUnderBase}`, method: init.method, headers, body: init.body, host: init.host });
  }

  /** Brings the Runtime and its door back to a serving state after a test that stopped it or took its credential away. */
  async resetToHealthy(): Promise<void> {
    this.restoreProductCredential();
    if (!this.runtimeRunning) { this.runtime = undefined; await this.startRuntime(); }
    const probe = await this.doorRequest('/v1/health').catch(() => null);
    if (!probe || probe.status !== 200) { await this.stopRuntime(); await this.startRuntime(); }
  }

  // -- Teardown ------------------------------------------------------------------------------

  async stop(): Promise<void> {
    if (this.stopped) return;
    this.stopped = true;
    await stopGroup(this.runtime).catch(() => {});
    await new Promise<void>((resolve) => { if (!this.https) return resolve(); this.https.closeAllConnections?.(); this.https.close(() => resolve()); });
    if (this.tmp) rmSync(this.tmp, { recursive: true, force: true });
  }
}

export async function startDirectHarness(): Promise<DirectHarness> {
  return new DirectHarness().start();
}
