#!/usr/bin/env node
/**
 * Start Reigh against the already-managed neutral workspace.v1 runtime.
 *
 * The runtime owns its endpoint and credential; this launcher only reads the
 * published profile and validates its product-scoped credential before passing
 * it to Vite's server-side proxy. The token is never printed or exposed as a
 * VITE_ value.
 */
import { existsSync, readFileSync, realpathSync } from 'node:fs';
import { randomBytes } from 'node:crypto';
import { spawn } from 'node:child_process';
import { homedir } from 'node:os';
import { delimiter, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createConnection } from 'node:net';
import { request as httpRequest } from 'node:http';
import { readGeneratedSchemaDigest, schemaDigestMismatch } from './runtime-schema-guard.mjs';
import {
  parseDevLocalWorkspaceArgs,
  validatePreviewOutputDirectory,
  viteChildArgs,
  resolveWorkspaceDiscoveryPath,
  gatewayChildArgs,
  resolveLoopbackPort,
} from './dev-local-workspace-options.mjs';

// What the person sees is a few friendly lines. Everything technical is behind `--verbose` (or ASTRID_VERBOSE=1), and every
// error carries one `Details:` line for an agent. Declared first: `fail()` runs before the rest of the file is evaluated.
const verbose = process.argv.includes('--verbose') || process.env.ASTRID_VERBOSE === '1';
const bold = (text) => (process.stdout.isTTY ? `\x1b[1m${text}\x1b[22m` : text);
const dim = (text) => (process.stderr.isTTY ? `\x1b[2m${text}\x1b[22m` : text);

const INSTALL_GUIDE_URL = 'https://github.com/peteromallet/astrid-agent/blob/main/docs/setup/local-source-install.md';
const NOT_SET_UP = `Astrid isn't set up on this computer yet. Install guide: ${INSTALL_GUIDE_URL}`;
const ENGINE_STOPPED = "Astrid's engine isn't running. Start it first: banodoco-local up --profile astrid";
const PROGRAM_IN_THE_WAY = "Another program is in the way, so Astrid can't start. Close it and try again.";
const OTHER_ASTRID_RUNNING = 'Another Astrid is already running in another window. Stop it there with Ctrl+C first.';
const ASTRID_STOPPED = 'Astrid stopped. Start it again with npm run dev:local.';
const AGENT_CHAT_STOPPED = 'Agent chat stopped. Start Astrid again with npm run dev:local.';
const BAD_HOSTED_ORIGIN = '--hosted-origin must be an https:// address, like https://astrid.haus';
const ENGINE_CHANGED = 'Astrid changed on this computer. Restart its engine: banodoco-local up --profile astrid';
const CANT_START = "Astrid can't start with the setup on this computer.";

/**
 * One friendly line, then one `Details:` line with the technical message. Returns null so callers can `return fail(...)`.
 * The line says who is speaking ("Astrid: ") only when the message does not already begin with the name.
 */
function fail(friendly, details) {
  console.error(friendly.startsWith('Astrid') ? friendly : `Astrid: ${friendly}`);
  if (details) console.error(dim(`Details: ${String(details).replace(/\s*\n\s*/g, ' ')}`));
  process.exitCode = 1;
  return null;
}

const configuredAstridCheckout = process.env.ASTRID_CHECKOUT?.trim();
const siblingAstridCheckout = resolve(process.cwd(), '..', 'Astrid');
const astridCheckout = configuredAstridCheckout
  || (existsSync(resolve(siblingAstridCheckout, '.astrid-data', 'runtime', 'discovery.json'))
    ? siblingAstridCheckout
    : null);
const configuredAstridPublicCheckout = process.env.ASTRID_PUBLIC_CHECKOUT?.trim();
let discoveryPath;
try {
  discoveryPath = resolveWorkspaceDiscoveryPath({
    discovery: process.env.ASTRID_WORKSPACE_DISCOVERY,
    supportRoot: process.env.ASTRID_SUPPORT_ROOT,
    dataRoot: process.env.BANODOCO_LOCAL_DATA_ROOT,
    home: homedir(),
  });
} catch (error) {
  process.exit(fail(CANT_START, error instanceof Error ? error.message : String(error)) ? 1 : 1);
}
const buildOnly = process.argv.includes('--build');
const port = process.env.PORT ?? '2222';
let launcherOptions;
try {
  launcherOptions = parseDevLocalWorkspaceArgs(process.argv.slice(2));
} catch (error) {
  process.exit(fail(CANT_START, error instanceof Error ? error.message : String(error)) ? 1 : 1);
}
const checkOnly = launcherOptions.checkOnly;
if (buildOnly && launcherOptions.preview) {
  process.exit(fail(CANT_START, '--build and --preview are separate rebuild and launch steps') ? 1 : 1);
}
const paired = launcherOptions.paired;
const resetPairing = launcherOptions.resetPairing;
let previewDirectory = null;
if (launcherOptions.preview) {
  try {
    previewDirectory = validatePreviewOutputDirectory(launcherOptions.previewDir);
  } catch (error) {
    process.exit(fail(CANT_START, error instanceof Error ? error.message : String(error)) ? 1 : 1);
  }
}
const pairedRelayOrigin = process.env.REIGH_PAIRED_RELAY_ORIGIN?.trim();
const hostedOriginArgumentIndex = process.argv.indexOf('--hosted-origin');
const hostedOriginArgument = hostedOriginArgumentIndex >= 0
  ? process.argv[hostedOriginArgumentIndex + 1]?.trim()
  : undefined;
if (hostedOriginArgumentIndex >= 0 && (!hostedOriginArgument || hostedOriginArgument.startsWith('--'))) {
  fail(BAD_HOSTED_ORIGIN, '--hosted-origin requires an exact HTTPS origin');
  process.exit(1);
}
const hostedOriginEnvironment = process.env.REIGH_LOOPBACK_ORIGIN?.trim() || undefined;
if (hostedOriginEnvironment === 'off' && hostedOriginArgument !== undefined) {
  fail('Choose one: turn the hosted address off, or give one.', 'REIGH_LOOPBACK_ORIGIN=off and --hosted-origin cannot both be set');
  process.exit(1);
}
const hostedOrigin = resolveHostedOrigin({
  explicit: hostedOriginEnvironment ?? hostedOriginArgument,
  configPath: process.env.REIGH_HOSTED_ORIGIN_CONFIG?.trim() || fileURLToPath(new URL('../config/hosted-origin.json', import.meta.url)),
});
const loopbackPort = resolveLoopbackPort(process.env.REIGH_LOOPBACK_PORT);
const generatedMetadataPath = resolve(process.cwd(), 'src/integrations/runtime/generated-contract-metadata.ts');

function requireExactHttpsOrigin(value, details, friendly = BAD_HOSTED_ORIGIN) {
  let parsed;
  try {
    parsed = new URL(value);
  } catch {
    fail(friendly, details);
    process.exit(1);
  }
  if (parsed.protocol !== 'https:' || parsed.origin !== value) {
    fail(friendly, details);
    process.exit(1);
  }
  return value;
}

/**
 * The gateway's origin. An explicit REIGH_LOOPBACK_ORIGIN or --hosted-origin wins, and `off` opts out. Otherwise the
 * origin in config/hosted-origin.json is the default, or null for no gateway. A broken config stops the launch.
 */
function resolveHostedOrigin({ explicit, configPath }) {
  if (explicit === 'off') return null;
  if (explicit !== undefined) return requireExactHttpsOrigin(explicit, 'hosted origin must be an exact HTTPS origin');
  const message = `hosted origin in ${configPath} must be {"origin": "<exact HTTPS origin>"} or {"origin": null}`;
  let config;
  try {
    config = JSON.parse(readFileSync(configPath, 'utf8'));
  } catch (error) {
    fail(CANT_START, `cannot read the hosted origin at ${configPath}: ${error instanceof Error ? error.message : String(error)}`);
    process.exit(1);
  }
  const configured = config?.origin;
  if (configured === null) return null;
  if (typeof configured !== 'string') {
    fail(CANT_START, message);
    process.exit(1);
  }
  return requireExactHttpsOrigin(configured, message, CANT_START);
}

function readJson(path, label, friendly = CANT_START) {
  try {
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch (error) {
    return fail(friendly, `cannot read ${label} at ${path}: ${error instanceof Error ? error.message : String(error)}`);
  }
}

const RUNTIME_SCOPES = Object.freeze([
  'handshake',
  'projects:read',
  'projects:write',
  'objects:read',
  'objects:write',
  'tasks:read',
  'tasks:write',
]);
const FORBIDDEN_ACTORS = new Set(['owner', 'astrid-pack-host', 'admin', 'worker']);

function readProductCredential(path, label) {
  let raw;
  try {
    raw = readFileSync(path, 'utf8').trim();
  } catch (error) {
    return fail(CANT_START, `cannot read ${label} at ${path}: ${error instanceof Error ? error.message : String(error)}`);
  }

  if (!raw) return fail(CANT_START, `${label} at ${path} is empty`);
  if (!raw.startsWith('{')) return fail(CANT_START, `${label} at ${path} is not a scoped Astrid product credential`);

  try {
    const credential = JSON.parse(raw);
    const token = typeof credential.token === 'string' ? credential.token.trim() : '';
    const actorId = typeof credential.actor_id === 'string' ? credential.actor_id.trim() : '';
    if (credential.version !== 1 || credential.scope !== 'astrid') {
      return fail(CANT_START, `${label} at ${path} must identify the version 1 astrid product scope`);
    }
    if (!actorId || FORBIDDEN_ACTORS.has(actorId)) {
      return fail(CANT_START, `${label} at ${path} has a forbidden or missing product actor`);
    }
    if (!token) return fail(CANT_START, `${label} at ${path} has no token`);
    return { actorId, token };
  } catch (error) {
    return fail(CANT_START, `cannot read ${label} at ${path}: ${error instanceof Error ? error.message : String(error)}`);
  }
}

function exactStringList(actual, expected) {
  return Array.isArray(actual)
    && actual.every((value) => typeof value === 'string')
    && actual.length === expected.length
    && [...actual].sort().every((value, index) => value === [...expected].sort()[index]);
}

function requireIdentity(discovery, discoveryFile, credential) {
  const runtimeInstanceId = typeof discovery.runtime_instance_id === 'string' ? discovery.runtime_instance_id.trim() : '';
  const realmId = typeof discovery.active_realm === 'string' ? discovery.active_realm.trim() : '';
  const realmRoot = typeof discovery.realm_root === 'string' ? discovery.realm_root.trim() : '';
  if (!runtimeInstanceId || !realmId || !realmRoot) {
    return fail(CANT_START, 'runtime discovery is missing its Astrid profile instance, selected realm, or realm root');
  }

  const catalog = readJson(resolve(dirname(discoveryFile), 'catalog.json'), 'Runtime profile catalog');
  if (!catalog) return null;
  if (catalog.selected_realm_id !== realmId || !Array.isArray(catalog.realms)) {
    return fail(CANT_START, 'Runtime discovery does not match the selected realm in catalog.json');
  }
  const matches = catalog.realms.filter((row) => row && row.realm_id === realmId);
  if (matches.length !== 1 || matches[0].source_profile !== 'astrid' || typeof matches[0].data_root !== 'string') {
    return fail(CANT_START, 'selected Runtime catalog row is not one Astrid profile with a data root');
  }
  try {
    const discoveredRoot = realpathSync(realmRoot);
    const catalogRoot = realpathSync(matches[0].data_root);
    if (discoveredRoot !== catalogRoot) return fail(CANT_START, 'Runtime discovery realm root does not match the selected Astrid catalog root');
  } catch (error) {
    return fail(CANT_START, `cannot resolve the selected Astrid realm root: ${error instanceof Error ? error.message : String(error)}`);
  }
  return { actorId: credential.actorId, realmId, realmRoot, runtimeInstanceId };
}

function requireLoopbackEndpoint(raw) {
  let endpoint;
  try {
    endpoint = new URL(raw);
  } catch {
    return fail(CANT_START, `runtime endpoint is not a valid URL: ${String(raw)}`);
  }
  if (endpoint.protocol !== 'http:' || !['127.0.0.1', 'localhost', '[::1]'].includes(endpoint.hostname)) {
    return fail(CANT_START, 'runtime endpoint must be an http loopback URL');
  }
  if (!endpoint.port || !/^\d+$/.test(endpoint.port)) {
    return fail(CANT_START, 'runtime endpoint must include an explicit port');
  }
  return endpoint;
}

async function verifyRuntime(endpoint, token, expectedIdentity) {
  let expectedSchemaDigest;
  try {
    expectedSchemaDigest = readGeneratedSchemaDigest(generatedMetadataPath);
  } catch (error) {
    return fail(CANT_START, error instanceof Error ? error.message : String(error));
  }

  try {
    const response = await fetch(new URL('/v1/health', endpoint), {
      headers: { Authorization: `Bearer ${token}`, Accept: 'application/json' },
      signal: AbortSignal.timeout(3000),
    });
    if (!response.ok) return fail(ENGINE_STOPPED, `runtime health check returned HTTP ${response.status}`);
    const health = await response.json();
    if (health?.status !== 'ok' || health?.protocol !== 'workspace.v1') {
      return fail(CANT_START, 'runtime health check did not report workspace.v1/ok');
    }
    if (health?.runtime_instance_id !== expectedIdentity.runtimeInstanceId) {
      return fail(ENGINE_CHANGED, 'Runtime health instance does not match the selected Astrid profile');
    }
    const digestError = schemaDigestMismatch(health?.schema_digest, expectedSchemaDigest);
    if (digestError) return fail(CANT_START, digestError);

    const handshakeResponse = await fetch(new URL('/v1/handshake', endpoint), {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, Accept: 'application/json', 'Content-Type': 'application/json' },
      body: JSON.stringify({
        protocol: 'workspace.v1',
        client_name: 'reigh-local-launcher',
        client_version: '1',
        requested_scopes: RUNTIME_SCOPES,
      }),
      signal: AbortSignal.timeout(3000),
    });
    if (!handshakeResponse.ok) return fail(CANT_START, `Runtime identity handshake returned HTTP ${handshakeResponse.status}`);
    const handshake = await handshakeResponse.json();
    const handshakeDigestError = schemaDigestMismatch(handshake?.schema_digest, expectedSchemaDigest);
    if (handshakeDigestError) return fail(CANT_START, handshakeDigestError);
    if (handshake?.protocol !== 'workspace.v1'
      || handshake?.actor_id !== expectedIdentity.actorId
      || FORBIDDEN_ACTORS.has(handshake?.actor_id)
      || handshake?.realm_id !== expectedIdentity.realmId
      || !exactStringList(handshake?.scopes, RUNTIME_SCOPES)) {
      return fail(CANT_START, 'Runtime handshake actor, realm, protocol, or product scopes do not match the selected Astrid profile');
    }

    const realmResponse = await fetch(new URL('/v1/realm', endpoint), {
      headers: { Authorization: `Bearer ${token}`, Accept: 'application/json' },
      signal: AbortSignal.timeout(3000),
    });
    if (!realmResponse.ok) return fail(CANT_START, `Runtime realm check returned HTTP ${realmResponse.status}`);
    const realm = await realmResponse.json();
    if (realm?.realm_id !== expectedIdentity.realmId) {
      return fail(CANT_START, 'Runtime realm does not match the selected Astrid profile');
    }
    return true;
  } catch (error) {
    return fail(ENGINE_STOPPED, `runtime is unavailable at ${endpoint.origin} (run banodoco-local up --profile astrid): ${error instanceof Error ? error.message : String(error)}`);
  }
}

const discovery = readJson(discoveryPath, 'runtime discovery', NOT_SET_UP);
if (!discovery) process.exit(process.exitCode ?? 1);
const endpoint = requireLoopbackEndpoint(discovery.endpoint);
if (!endpoint) process.exit(process.exitCode ?? 1);
const credentialPath = discovery.credential_file;
if (typeof credentialPath !== 'string' || !credentialPath.trim()) process.exit(fail(CANT_START, 'discovery has no credential_file') ? 1 : 1);
const credential = readProductCredential(credentialPath, 'runtime credential');
if (!credential) process.exit(process.exitCode ?? 1);
const expectedIdentity = requireIdentity(discovery, discoveryPath, credential);
if (!expectedIdentity) process.exit(process.exitCode ?? 1);
if (!(await verifyRuntime(endpoint, credential.token, expectedIdentity))) process.exit(process.exitCode ?? 1);
if (paired && !pairedRelayOrigin) process.exit(fail(CANT_START, '--paired requires REIGH_PAIRED_RELAY_ORIGIN') ? 1 : 1);

const acpToken = process.env.ASTRID_ACP_BRIDGE_TOKEN?.trim() || randomBytes(32).toString('base64url');
const acpPort = process.env.VITE_ASTRID_ACP_BRIDGE_PORT ?? '17335';
const runtimeProxyPort = process.env.VITE_ASTRID_DYNAMIC_PROXY_PORT?.trim() || '17336';
if (!/^\d+$/.test(runtimeProxyPort) || Number(runtimeProxyPort) < 1 || Number(runtimeProxyPort) > 65535) {
  process.exit(fail(CANT_START, 'VITE_ASTRID_DYNAMIC_PROXY_PORT must be an integer from 1 to 65535') ? 1 : 1);
}

/** Resolves true once something listens on the port, false at the deadline or when `aborted()` turns true. */
function waitForPort(portValue, timeoutMs = 3000, aborted = () => false) {
  const deadline = Date.now() + timeoutMs;
  return new Promise((resolveReady) => {
    const attempt = () => {
      const socket = createConnection({ host: '127.0.0.1', port: Number(portValue) });
      socket.once('connect', () => {
        socket.destroy();
        resolveReady(true);
      });
      socket.once('error', () => {
        socket.destroy();
        if (aborted() || Date.now() >= deadline) resolveReady(false);
        else setTimeout(attempt, 50);
      });
    };
    attempt();
  });
}

const env = {
  ...process.env,
  ...(astridCheckout ? { ASTRID_CHECKOUT: astridCheckout } : {}),
  ...(configuredAstridPublicCheckout ? { ASTRID_PUBLIC_CHECKOUT: configuredAstridPublicCheckout } : {}),
  PORT: port,
  VITE_ASTRID_WORKSPACE_V1: '1',
  VITE_ASTRID_BRIDGE_PORT: runtimeProxyPort,
  ASTRID_BRIDGE_TOKEN: credential.token,
  ASTRID_ACP_BRIDGE_TOKEN: acpToken,
  ...(hostedOrigin ? { ASTRID_ACP_LOCAL_MEDIA_ONLY: '1' } : {}),
  ...(hostedOrigin && process.env.ASTRID_ACP_COMMAND?.startsWith('/')
    ? { PATH: `${dirname(process.env.ASTRID_ACP_COMMAND)}${delimiter}${process.env.PATH ?? ''}` }
    : {}),
  // The editor's RuntimeDataProvider talks to `/api/runtime`, which is a
  // separate Vite proxy from the historical `/api/astrid` bridge. Keep the
  // Runtime endpoint and credential server-side so the browser never sees the
  // owner token.
  VITE_WORKSPACE_RUNTIME_URL: `http://127.0.0.1:${runtimeProxyPort}`,
  WORKSPACE_RUNTIME_TOKEN_FILE: credentialPath,
  // Fallback for builds without a live workspace config endpoint. Local preview
  // refreshes these non-secret identifiers from discovery on each page load.
  VITE_WORKSPACE_RUNTIME_EXPECTED_ACTOR_ID: expectedIdentity.actorId,
  VITE_WORKSPACE_RUNTIME_EXPECTED_REALM_ID: expectedIdentity.realmId,
  VITE_WORKSPACE_RUNTIME_EXPECTED_INSTANCE_ID: expectedIdentity.runtimeInstanceId,
  ASTRID_LOCAL_COMPOSE_URL: `http://127.0.0.1:${port}/api/astrid/generation/compose`,
  // The ACP bridge is a sibling user-machine process. Keep its cwd explicit so
  // OMP owns one stable session store and the browser cannot redirect it.
  ASTRID_ACP_CWD: process.env.ASTRID_ACP_CWD ?? process.cwd(),
  // Omit the profile by default so ACP uses the same model/auth configuration
  // as the user's normal OMP installation. An explicit profile remains a
  // supported escape hatch for isolated deployments.
  ...(process.env.ASTRID_ACP_PROFILE?.trim()
    ? { ASTRID_ACP_PROFILE: process.env.ASTRID_ACP_PROFILE.trim() }
    : {}),
  ASTRID_ACP_BRIDGE_PORT: acpPort,
};

const healthyLine = `workspace.v1 runtime healthy at ${endpoint.origin}; Reigh will use ${launcherOptions.preview ? `preview output ${previewDirectory} on port ${port}` : `port ${port}`}`;
if (checkOnly) {
  if (verbose) console.log(healthyLine);
  console.log('Astrid is ready.');
  process.exit(0);
}

// The build retains this identity for hosted/paired fallback. Local preview
// serves a fresh discovery-backed binding on each page load.
if (buildOnly) {
  if (verbose) console.log(healthyLine);
  const build = spawn('npm', ['run', 'build'], { stdio: 'inherit', env });
  process.on('SIGINT', () => build.kill('SIGINT'));
  process.on('SIGTERM', () => build.kill('SIGTERM'));
  build.on('error', (error) => { fail(CANT_START, `could not build Reigh: ${error.message}`); process.exitCode = 1; });
  build.on('exit', async (code, signal) => {
    if (code === 0 && !signal && !(await verifyRuntime(endpoint, credential.token, expectedIdentity))) {
      process.exitCode = 1;
      return;
    }
    process.exitCode = code ?? 1;
  });
} else {

const COULDNT_START = "Astrid couldn't start. Run npm run dev:local -- --verbose to see why.";
/** How long Vite may take to listen, and the gateway after it printed that it does. */
const VITE_START_TIMEOUT_MS = 60_000;
const GATEWAY_START_TIMEOUT_MS = 15_000;

/** The one block that tells a person where to go. Printed only once Astrid is reachable, never before. */
function printOpenBlock() {
  console.log('');
  console.log(bold(`  Open ${hostedOrigin}`));
  console.log('');
  console.log('Keep this window open while you work. Press Ctrl+C to stop.');
}

/**
 * Who answers on the gateway's port? The holder is asked who it serves the way the hosted page would (its realm, with the
 * hosted Origin). Nothing listening is `free`; this realm is `ours` (a second launcher in another window); a gateway for
 * another realm is `other_astrid`; anything else is `program`.
 */
function probeGatewayPort(portValue, origin, realmId) {
  return new Promise((resolveProbe) => {
    const request = httpRequest({ hostname: '127.0.0.1', port: Number(portValue), path: '/api/runtime/v1/realm', method: 'GET', headers: { Origin: origin }, timeout: 2000 }, (response) => {
      const chunks = [];
      response.on('data', (chunk) => { if (chunks.length < 64) chunks.push(chunk); });
      response.on('error', () => resolveProbe({ kind: 'program', details: `port ${portValue} answered and then dropped the connection` }));
      response.on('end', () => {
        let body = null;
        try { body = JSON.parse(Buffer.concat(chunks).toString('utf8')); } catch { /* not a gateway */ }
        if (response.statusCode === 200 && typeof body?.realm_id === 'string') {
          resolveProbe(body.realm_id === realmId
            ? { kind: 'ours' }
            : { kind: 'other_astrid', details: `port ${portValue} is already served by a gateway for another realm` });
        } else if (response.statusCode === 503 && ['realm_changed', 'runtime_identity_mismatch'].includes(body?.error)) {
          resolveProbe({ kind: 'other_astrid', details: `port ${portValue} is already served by a gateway for another realm (${body.error})` });
        } else {
          resolveProbe({ kind: 'program', details: `port ${portValue} is already in use by a program that is not the gateway for ${origin} (HTTP ${response.statusCode})` });
        }
      });
    });
    request.on('timeout', () => { request.destroy(); resolveProbe({ kind: 'program', details: `port ${portValue} did not answer in time` }); });
    request.on('error', (error) => resolveProbe(error.code === 'ECONNREFUSED'
      ? { kind: 'free' }
      : { kind: 'program', details: `port ${portValue} is not usable: ${error.message}` }));
    request.end();
  });
}

if (hostedOrigin && loopbackPort !== '0') {
  const holder = await probeGatewayPort(loopbackPort, hostedOrigin, expectedIdentity.realmId);
  if (holder.kind === 'ours') {
    // A second launcher for the same Astrid: the first one is serving, so start nothing and point to the same place.
    console.log('Astrid is already running in another window.');
    printOpenBlock();
    process.exit(0);
  }
  if (holder.kind === 'other_astrid') process.exit(fail(OTHER_ASTRID_RUNNING, holder.details) ? 1 : 1);
  if (holder.kind === 'program') process.exit(fail(PROGRAM_IN_THE_WAY, holder.details) ? 1 : 1);
}

// The app's own port, checked the way the gateway's was: if anything already listens there, Vite (`--strictPort`) cannot
// start, and whatever answers would otherwise look like Astrid's app. Nothing has been started yet, so nothing needs stopping.
if (port !== '0' && await waitForPort(port, 0)) {
  process.exit(fail(PROGRAM_IN_THE_WAY, `port ${port} is in use`) ? 1 : 1);
}

// With a hosted address, the technical lines are held back (`--verbose` prints them after the Open block). Without one
// there is no Open block, so the launcher prints what it always did.
const showTechnical = verbose || !hostedOrigin;
let opened = !hostedOrigin;
let shuttingDown = false;
const held = [];
const emit = (text, toStderr = false) => {
  if (opened) (toStderr ? process.stderr : process.stdout).write(text);
  else held.push([text, toStderr]);
};
const flushHeld = () => {
  opened = true;
  for (const [text, toStderr] of held.splice(0)) (toStderr ? process.stderr : process.stdout).write(text);
};
const technical = (line) => { if (showTechnical) emit(`${line}\n`); };

/** Reads a service's output: kept (the last few lines) for a `Details:` line, shown only for `showTechnical`. */
function watch(child, onStdoutLine) {
  const state = { tail: '', pending: '' };
  const read = (toStderr) => (chunk) => {
    const text = chunk.toString('utf8');
    state.tail = (state.tail + text).slice(-4000);
    if (!toStderr && onStdoutLine) {
      state.pending += text;
      let newline;
      while ((newline = state.pending.indexOf('\n')) >= 0) {
        onStdoutLine(state.pending.slice(0, newline));
        state.pending = state.pending.slice(newline + 1);
      }
    }
    if (showTechnical) emit(text, toStderr);
  };
  child.stdout.on('data', read(false));
  child.stderr.on('data', read(true));
  return state;
}
const lastLine = (state) => state.tail.split('\n').map((line) => line.trim()).filter(Boolean).pop() ?? '';
const withLast = (state) => (lastLine(state) ? `: ${lastLine(state)}` : '');
const serviceEnvironment = (extra = {}) => ({
  ...env,
  ...(process.stdout.isTTY && showTechnical ? { FORCE_COLOR: '1' } : {}),
  ...extra,
});
const piped = ['ignore', 'pipe', 'pipe'];
const npmQuiet = showTechnical ? [] : ['--silent'];

if (hostedOrigin) console.log('Starting Astrid…');
technical(healthyLine);

let connector;
const runtimeProxy = spawn(process.execPath, ['scripts/runtime-discovery-proxy.mjs'], {
  stdio: piped,
  env: serviceEnvironment({ ASTRID_RUNTIME_PROXY_PORT: runtimeProxyPort, ASTRID_WORKSPACE_DISCOVERY: discoveryPath }),
});
const proxyOutput = watch(runtimeProxy);
if (!(await waitForPort(runtimeProxyPort))) {
  runtimeProxy.kill('SIGTERM');
  flushHeld();
  process.exit(fail(COULDNT_START, `runtime discovery proxy did not start on port ${runtimeProxyPort}${withLast(proxyOutput)}`) ? 1 : 1);
}
const acpBridge = spawn('npm', [...npmQuiet, 'run', 'dev:astrid-acp'], { stdio: piped, env: serviceEnvironment() });
const acpOutput = watch(acpBridge);
const gateway = hostedOrigin
  ? spawn(process.execPath, gatewayChildArgs({
    discoveryPath,
    credentialPath,
    hostedOrigin,
    loopbackPort,
    acp: launcherOptions.acp,
    acpPort,
    appPort: port,
    auditLog: process.env.REIGH_LOOPBACK_AUDIT_LOG?.trim(),
    actor: process.env.REIGH_PAIRED_PRODUCT_ACTOR?.trim(),
  }), { stdio: piped, env: serviceEnvironment() })
  : null;
// The gateway prints one JSON line once it listens; that line carries the port it actually got (`--port 0` in tests).
let gatewayListening = () => {};
const gatewayReady = new Promise((resolveReady) => { gatewayListening = resolveReady; });
const gatewayOutput = gateway
  ? watch(gateway, (line) => {
    if (!line.startsWith('{')) return;
    try {
      const { base } = JSON.parse(line);
      if (typeof base === 'string') gatewayListening(Number(new URL(base).port));
    } catch { /* not the ready line */ }
  })
  : null;
if (hostedOrigin) technical(`loopback gateway starting on 127.0.0.1:${loopbackPort} for ${hostedOrigin}${launcherOptions.acp ? ' (ACP on)' : ''}`);
if (paired) {
  connector = spawn('npx', ['tsx', 'scripts/reigh-local-connector.ts', '--discovery', discoveryPath, '--relay-origin', pairedRelayOrigin, ...(resetPairing ? ['--reset-pairing'] : [])], {
    stdio: 'inherit',
    env,
  });
}

const child = spawn('npm', [...npmQuiet, ...viteChildArgs({
  preview: launcherOptions.preview,
  previewDir: previewDirectory,
  quiet: !showTechnical,
})], {
  stdio: piped,
  // The local Vite process is the connector's fixed compose/ACP destination;
  // it must not install another relay and accidentally loop back to itself.
  env: serviceEnvironment(paired ? { REIGH_PAIRED_RELAY_ENABLED: '0', ASTRID_LOCAL_COMPOSE_URL: `http://127.0.0.1:${port}/api/astrid/generation/compose` } : {}),
});
const viteOutput = watch(child);

const shutdown = (signal) => {
  if (shuttingDown) return;
  shuttingDown = true;
  if (child.exitCode === null) child.kill(signal);
  if (connector?.exitCode === null) connector.kill(signal);
  if (acpBridge.exitCode === null) acpBridge.kill(signal);
  if (gateway?.exitCode === null) gateway.kill(signal);
  if (runtimeProxy.exitCode === null) runtimeProxy.kill(signal);
  gatewayListening(null);
};
/** A failure: the technical output held back so far is shown, then the friendly line and its details. */
const stopWith = (friendly, details) => {
  if (shuttingDown) return;
  flushHeld();
  fail(friendly, details);
  shutdown('SIGTERM');
};
process.on('SIGINT', () => shutdown('SIGINT'));
process.on('SIGTERM', () => shutdown('SIGTERM'));
child.on('error', (error) => stopWith(COULDNT_START, `could not start Vite: ${error.message}`));
child.on('exit', (code, signal) => {
  if (!shuttingDown && !opened && (code ?? 1) !== 0) {
    // Vite never listened: usually the app's port is taken (`--strictPort`).
    stopWith(/already in use|EADDRINUSE/i.test(viteOutput.tail) ? PROGRAM_IN_THE_WAY : COULDNT_START, `Vite exited${signal ? ` with ${signal}` : ` with code ${code}`}${withLast(viteOutput)}`);
  }
  if (connector?.exitCode === null) connector.kill('SIGTERM');
  if (acpBridge.exitCode === null) acpBridge.kill('SIGTERM');
  if (gateway?.exitCode === null) gateway.kill('SIGTERM');
  if (runtimeProxy.exitCode === null) runtimeProxy.kill('SIGTERM');
  if (signal && !shuttingDown) process.kill(process.pid, signal);
  else process.exitCode = process.exitCode || (code ?? 0);
});
connector?.on('error', (error) => { fail(CANT_START, `could not start paired connector: ${error.message}`); });
acpBridge.on('error', (error) => stopWith(AGENT_CHAT_STOPPED, `could not start Astrid ACP bridge: ${error.message}`));
acpBridge.on('exit', (code, signal) => {
  stopWith(AGENT_CHAT_STOPPED, `Astrid ACP bridge exited${signal ? ` with ${signal}` : ` with code ${code}`}; ACP is offline${withLast(acpOutput)}`);
});
gateway?.on('error', (error) => stopWith(ASTRID_STOPPED, `could not start loopback gateway: ${error.message}`));
gateway?.on('exit', (code, signal) => {
  gatewayListening(null);
  // Before Open, a gateway that never listened usually found its port taken (`describePortHolder`); after it, Astrid stopped.
  const tail = gatewayOutput.tail;
  const friendly = opened ? ASTRID_STOPPED
    : /already served by/.test(tail) ? OTHER_ASTRID_RUNNING
      : /already in use/.test(tail) ? PROGRAM_IN_THE_WAY
        : ASTRID_STOPPED;
  stopWith(friendly, `loopback gateway exited${signal ? ` with ${signal}` : ` with code ${code}`}; the hosted app cannot reach this computer${withLast(gatewayOutput)}`);
});

// Astrid is reachable when the gateway listens and the app answers. Only then does a person get the Open block.
if (hostedOrigin) {
  const gatewayPort = await gatewayReady;
  if (gatewayPort !== null && !shuttingDown) {
    const aborted = () => shuttingDown;
    const reachable = await waitForPort(gatewayPort, GATEWAY_START_TIMEOUT_MS, aborted) && await waitForPort(port, VITE_START_TIMEOUT_MS, aborted);
    // Something answering on the app's port is not enough: it has to be our own Vite, still running. A Vite that already
    // exited (its port taken after the check above) leaves another program answering, and that is not Astrid's app.
    const viteAlive = child.exitCode === null && child.signalCode === null;
    if (reachable && viteAlive && !shuttingDown) {
      printOpenBlock();
      flushHeld();
    } else {
      stopWith(COULDNT_START, `nothing listened on 127.0.0.1:${gatewayPort} and 127.0.0.1:${port} in time`);
    }
  }
}

}
