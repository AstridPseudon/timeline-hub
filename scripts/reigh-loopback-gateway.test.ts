// @vitest-environment node
import { test } from 'vitest';
import assert from 'node:assert/strict';
import { createServer, request } from 'node:http';
import { connect } from 'node:net';
import { networkInterfaces } from 'node:os';
import { spawn } from 'node:child_process';
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { createLoopbackGateway, fileRuntimeSource, allowedAcpRoute, allowedRoute, loopbackEndpoint, DEFAULT_GATEWAY_PORT, PRODUCT_SCOPES, type RuntimeSource } from './reigh-loopback-gateway.ts';

test('closed method/path table rejects traversal, admin, remote endpoints', () => {
  assert(allowedRoute('/v1/projects/p/timelines/t/inspect', 'POST'));
  assert(allowedRoute('/v1/projects/p/timelines/t/composition-revisions/r', 'GET'));
  for (const path of ['/v1/doctor', '/v1/backup', '/v1/tasks/claim', '/v1/objects/../secret', '/v1/objects/a%2fb', '/v1/objects/a%252fb', '//remote.test/x']) assert(!allowedRoute(path, 'POST'));
  assert(!allowedRoute('/v1/projects/p/timelines/t/inspect', 'DELETE'));
  // renameTimeline: PATCH on the timeline itself, and nothing wider.
  assert(allowedRoute('/v1/projects/p/timelines/t', 'PATCH'));
  assert(!allowedRoute('/v1/projects/p/timelines/t', 'DELETE'));
  assert(!allowedRoute('/v1/projects/p/timelines/t', 'PUT'));
  assert(!allowedRoute('/v1/projects/p/timelines/t/inspect', 'PATCH'));
  assert(!allowedRoute('/v1/projects/p/timelines', 'PATCH'));
  assert.throws(() => loopbackEndpoint('https://remote.test'));
  assert.throws(() => loopbackEndpoint('http://127.0.0.1:1234/redirect'));
});

test('gateway serves /api/runtime and /api/astrid for the hosted origin only, and streams media directly with range headers', async () => {
  const hits: Array<{ path?: string; auth?: string; range?: string }> = [];
  const runtime = createServer((req, res) => {
    hits.push({ path: req.url, auth: req.headers.authorization, range: req.headers.range });
    if (req.url === '/v1/objects/redirect') { res.writeHead(302, { Location: 'https://remote.test/media' }); res.end(); return; }
    if (req.url === '/v1/health') { res.writeHead(200, { 'Content-Type': 'application/json' }); res.end('{"status":"ok"}'); return; }
    res.writeHead(206, { 'Content-Type': 'image/png', 'Content-Range': 'bytes 0-2/6', ETag: '"local"', 'Set-Cookie': 'secret=bad' }); res.end('PNG');
  });
  await new Promise<void>(resolve => runtime.listen(0, '127.0.0.1', resolve));
  const runtimeAddress = runtime.address() as { port: number };
  const audit: Array<Record<string, unknown>> = [];
  const origin = 'https://hosted.test';
  const g = createLoopbackGateway({ endpoint: `http://127.0.0.1:${runtimeAddress.port}`, token: 'only-local-product-token', origin, audit: entry => audit.push(entry) });
  await new Promise<void>(resolve => g.server.listen(0, '127.0.0.1', resolve));
  const port = (g.server.address() as { port: number }).port;
  const call = (path: string, method = 'GET', headers: Record<string, string> = {}) => new Promise<{ status: number; headers: import('node:http').IncomingHttpHeaders; body: string }>((resolve, reject) => {
    const r = request({ hostname: '127.0.0.1', port, path, method, headers }, res => { const chunks: Buffer[] = []; res.on('data', chunk => chunks.push(chunk)); res.on('end', () => resolve({ status: res.statusCode!, headers: res.headers, body: Buffer.concat(chunks).toString() })); }); r.on('error', reject); r.end();
  });
  try {
    assert.equal(g.prefix, '/api/runtime');
    const path = '/api/runtime/v1/objects/card';
    // Refusals: no Origin, another Origin, and a Host that is not exactly 127.0.0.1:<port>.
    assert.equal((await call(path)).status, 403);
    assert.equal((await call(path, 'GET', { Origin: 'https://evil.test' })).status, 403);
    for (const host of ['evil.test', `localhost:${port}`, `[::1]:${port}`, `127.0.0.1:${port + 1}`, '127.0.0.1', `127.0.0.1.evil.test:${port}`]) {
      assert.equal((await call(path, 'GET', { Origin: origin, Host: host })).status, 403, `Host ${host}`);
    }
    // The Origin is judged before the route: a foreign page gets 403 for an unlisted path too, never a 404 that maps the paths.
    for (const unlisted of ['/session/abc/api/runtime/v1/health', '/v1/health', '/api/runtime/v1/doctor', '/api/astrid/generation/compose', '/api/astrid/acp/connect', '/api/other/v1/health', '/']) {
      const foreign = await call(unlisted, 'GET', { Origin: 'https://evil.test' });
      assert.equal(foreign.status, 403, `evil origin ${unlisted}`);
      assert.equal(JSON.parse(foreign.body).error, 'hosted_origin_required');
      assert.equal(foreign.headers['access-control-allow-origin'], undefined);
      assert.equal((await call(unlisted, 'GET')).status, 403, `no origin ${unlisted}`);
      // The control: the same path from the hosted origin is a plain 404, so the 403 above is the Origin check and not a missing route.
      assert.equal((await call(unlisted, 'GET', { Origin: origin })).status, 404, `hosted origin ${unlisted}`);
    }
    assert.equal((await call(path, 'GET', { Origin: origin, Authorization: 'Bearer browser' })).status, 403);
    assert.equal(hits.length, 0, 'nothing reached the Runtime');
    // Allowed: both prefixes, the exact origin, the exact Host.
    const health = await call('/api/runtime/v1/health', 'GET', { Origin: origin });
    assert.equal(health.status, 200); assert.equal(health.headers['access-control-allow-origin'], origin);
    assert.equal((await call('/api/astrid/v1/health', 'GET', { Origin: origin })).status, 200);
    const preflight = await call(path, 'OPTIONS', { Origin: origin, 'Access-Control-Request-Method': 'GET', 'Access-Control-Request-Headers': 'range', 'Access-Control-Request-Private-Network': 'true' });
    assert.equal(preflight.status, 204); assert.equal(preflight.headers['access-control-allow-private-network'], 'true');
    assert.equal((await call(path, 'OPTIONS', { Origin: 'https://evil.test', 'Access-Control-Request-Method': 'GET' })).status, 403);
    const result = await call(path, 'GET', { Origin: origin, Range: 'bytes=0-2' });
    assert.equal(result.status, 206); assert.equal(result.body, 'PNG'); assert.equal(result.headers.etag, '"local"');
    assert.equal(result.headers['access-control-allow-origin'], origin); assert.equal(result.headers['set-cookie'], undefined);
    assert.deepEqual(hits.at(-1), { path: '/v1/objects/card', auth: 'Bearer only-local-product-token', range: 'bytes=0-2' });
    // A Referer is not a credential: a media request without Origin is refused even from the hosted page, before the route is judged.
    const reached = hits.length;
    assert.equal((await call(path, 'GET', { Referer: origin + '/tools/video-editor' })).status, 403);
    assert.equal((await call(path, 'HEAD', { Referer: `${origin}/` })).status, 403);
    assert.equal(hits.length, reached, 'a Referer alone never reaches the Runtime');
    // Not served: the old session paths, compose, and ACP when the gateway was started without it.
    assert.equal((await call('/session/abc/api/runtime/v1/health', 'GET', { Origin: origin })).status, 404);
    assert.equal((await call('/api/astrid/generation/compose', 'POST', { Origin: origin })).status, 404);
    assert.equal((await call('/api/astrid/acp/connect', 'POST', { Origin: origin })).status, 404);
    assert.equal((await call('/api/astrid/acp/health', 'GET', { Origin: origin })).status, 404);
    assert(audit.some(entry => entry.path === '/v1/objects/card' && entry.response_bytes === 3));
    assert(!JSON.stringify(audit).includes('only-local-product-token'));
    const digestPath = `/api/runtime/v1/objects/sha256:${'c'.repeat(64)}`;
    assert.equal((await call(digestPath, 'GET', { Origin: origin })).headers['cache-control'], 'private, max-age=31536000, immutable');
    assert.equal(result.headers['cache-control'], 'no-store', 'non-digest object id stays no-store');
    assert.equal((await call('/api/runtime/v1/projects', 'GET', { Origin: origin })).headers['cache-control'], 'no-store');
    assert.equal((await call('/api/runtime/v1/objects/redirect', 'GET', { Origin: origin })).status, 502);
  } finally { g.server.closeAllConnections(); runtime.closeAllConnections(); await Promise.all([new Promise<void>(resolve => g.server.close(() => resolve())), new Promise<void>(resolve => runtime.close(() => resolve()))]); }
});

test('gateway forwards only typed ACP lifecycle routes with its dedicated bridge credential', async () => {
  const calls: Array<{ path?: string; auth?: string; protocol?: string; body: string }> = [];
  const acp = createServer(async (req, res) => {
    const chunks: Buffer[] = [];
    for await (const chunk of req) chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk));
    calls.push({ path: req.url, auth: req.headers.authorization, protocol: typeof req.headers['x-astrid-bridge-version'] === 'string' ? req.headers['x-astrid-bridge-version'] : undefined, body: Buffer.concat(chunks).toString() });
    res.setHeader('Content-Type', 'application/json');
    if (req.url === '/connect') return res.end(JSON.stringify({ connection_id: 'connection-1', initialize: {} }));
    if (req.url === '/connection-1/rpc') return res.end(JSON.stringify({ result: { ok: true } }));
    res.statusCode = 404;
    res.end(JSON.stringify({ error: 'not_found' }));
  });
  await new Promise<void>(resolve => acp.listen(0, '127.0.0.1', resolve));
  const acpPort = (acp.address() as { port: number }).port;
  const runtime = createServer((_req, res) => { res.writeHead(200, { 'Content-Type': 'application/json' }); res.end('{}'); });
  await new Promise<void>(resolve => runtime.listen(0, '127.0.0.1', resolve));
  const runtimePort = (runtime.address() as { port: number }).port;
  const origin = 'https://hosted.test';
  const g = createLoopbackGateway({
    endpoint: `http://127.0.0.1:${runtimePort}`,
    token: 'runtime-token',
    origin,
    acpEndpoint: `http://127.0.0.1:${acpPort}`,
    acpToken: 'acp-token',
  });
  await new Promise<void>(resolve => g.server.listen(0, '127.0.0.1', resolve));
  const port = (g.server.address() as { port: number }).port;
  const base = '/api/astrid';
  const call = (path: string, method: string, body?: string, headers: Record<string, string> = {}) => new Promise<{ status: number; body: string }>((resolve, reject) => {
    const requestHeaders = { Origin: origin, ...headers, ...(body === undefined ? {} : { 'Content-Length': String(Buffer.byteLength(body)) }) };
    const requestBody = request({ hostname: '127.0.0.1', port, path, method, headers: requestHeaders }, response => {
      const chunks: Buffer[] = [];
      response.on('data', chunk => chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk)));
      response.on('end', () => resolve({ status: response.statusCode!, body: Buffer.concat(chunks).toString() }));
    });
    requestBody.on('error', reject);
    if (body !== undefined) requestBody.end(body);
    else requestBody.end();
  });
  try {
    assert(allowedAcpRoute('/acp/connect', 'POST'));
    assert(!allowedAcpRoute('/acp/connection-1/rpc', 'GET'));
    assert.equal((await call(`${base}/acp/connect`, 'OPTIONS', undefined, {
      'Access-Control-Request-Method': 'POST',
      'Access-Control-Request-Headers': 'content-type',
    })).status, 204);
    const connected = await call(`${base}/acp/connect`, 'POST', '{}', { 'Content-Type': 'application/json' });
    assert.equal(connected.status, 200);
    assert.deepEqual(JSON.parse(connected.body), { connection_id: 'connection-1', initialize: {} });
    const rpc = await call(`${base}/acp/connection-1/rpc`, 'POST', JSON.stringify({ method: 'session/list', params: {} }), { 'Content-Type': 'application/json' });
    assert.equal(rpc.status, 200);
    assert.deepEqual(JSON.parse(rpc.body), { result: { ok: true } });
    assert.equal((await call(`${base}/acp/connect`, 'POST', '{}', { Authorization: 'Bearer browser', 'Content-Type': 'application/json' })).status, 403);
    assert.deepEqual(calls.map(call => ({ path: call.path, auth: call.auth, protocol: call.protocol })), [
      { path: '/connect', auth: 'Bearer acp-token', protocol: 'v1' },
      { path: '/connection-1/rpc', auth: 'Bearer acp-token', protocol: 'v1' },
    ]);
  } finally {
    g.server.closeAllConnections();
    acp.closeAllConnections();
    runtime.closeAllConnections();
    await Promise.all([
      new Promise<void>(resolve => g.server.close(() => resolve())),
      new Promise<void>(resolve => acp.close(() => resolve())),
      new Promise<void>(resolve => runtime.close(() => resolve())),
    ]);
  }
});

test('renameTimeline PATCH reaches the Runtime with the hosted Origin and is refused without it', async () => {
  const hits: Array<{ method?: string; path?: string; auth?: string; body: string }> = [];
  const runtime = createServer((req, res) => {
    const chunks: Buffer[] = [];
    req.on('data', chunk => chunks.push(chunk));
    req.on('end', () => {
      hits.push({ method: req.method, path: req.url, auth: req.headers.authorization, body: Buffer.concat(chunks).toString() });
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end('{}');
    });
  });
  await new Promise<void>(resolve => runtime.listen(0, '127.0.0.1', resolve));
  const origin = 'https://hosted.test';
  const g = createLoopbackGateway({ endpoint: `http://127.0.0.1:${(runtime.address() as { port: number }).port}`, token: 'runtime-token', origin });
  await new Promise<void>(resolve => g.server.listen(0, '127.0.0.1', resolve));
  const port = (g.server.address() as { port: number }).port;
  const patch = (path: string, headers: Record<string, string>) => new Promise<number>((resolve, reject) => {
    const body = JSON.stringify({ name: 'Renamed' });
    const req = request({ hostname: '127.0.0.1', port, path, method: 'PATCH', headers: { 'Content-Type': 'application/json', 'Content-Length': String(Buffer.byteLength(body)), 'Idempotency-Key': 'k1', ...headers } }, res => { res.resume(); res.on('end', () => resolve(res.statusCode!)); });
    req.on('error', reject);
    req.end(body);
  });
  try {
    const path = '/api/runtime/v1/projects/p1/timelines/t1';
    assert.equal(await patch(path, { Origin: origin }), 200);
    assert.deepEqual(hits.map(hit => ({ method: hit.method, path: hit.path, auth: hit.auth, body: hit.body })), [
      { method: 'PATCH', path: '/v1/projects/p1/timelines/t1', auth: 'Bearer runtime-token', body: '{"name":"Renamed"}' },
    ]);
    assert.equal(await patch(path, {}), 403);
    assert.equal(await patch(path, { Origin: 'https://evil.test' }), 403);
    assert.equal(hits.length, 1, 'a refused request never reaches the Runtime');
  } finally {
    g.server.closeAllConnections();
    runtime.closeAllConnections();
    await Promise.all([
      new Promise<void>(resolve => g.server.close(() => resolve())),
      new Promise<void>(resolve => runtime.close(() => resolve())),
    ]);
  }
});

test('binary streams exceed old 64MiB cap without buffering; lowered caps reject fixed and chunked bodies', async () => {
  const { DEFAULT_MAX_OBJECT_BYTES, resolveMaxObjectBytes } = await import('./reigh-loopback-gateway.ts');
  assert.equal(DEFAULT_MAX_OBJECT_BYTES, 5368709120);
  assert.equal(resolveMaxObjectBytes('4096'), 4096);
  for (const bad of ['0', '-1', '5368709121', '1.5', 'NaN']) assert.throws(() => resolveMaxObjectBytes(bad));
  let received = 0;
  const runtime = createServer(async (req, res) => {
    let size = 0;
    try {
      for await (const chunk of req) { size += chunk.length; await new Promise(r => setImmediate(r)); }
      received += size;
      res.end(JSON.stringify({ size }));
    } catch { /* cancellation is expected */ }
  });
  await new Promise<void>(r => runtime.listen(0, '127.0.0.1', r));
  const endpoint = `http://127.0.0.1:${(runtime.address() as { port: number }).port}`;
  const g = createLoopbackGateway({ endpoint, token: 'local', origin: 'https://hosted.test' });
  const small = createLoopbackGateway({ endpoint, token: 'local', origin: 'https://hosted.test', maxObjectBytes: 4096 });
  await Promise.all([new Promise<void>(r => g.server.listen(0, '127.0.0.1', r)), new Promise<void>(r => small.server.listen(0, '127.0.0.1', r))]);
  const upload = (gateway: typeof g, size: number, declared: boolean) => new Promise<{ status: number; body: string }>((resolve, reject) => {
    const r = request({ hostname: '127.0.0.1', port: (gateway.server.address() as { port: number }).port, path: gateway.prefix + '/v1/projects/p/objects', method: 'POST', headers: { Origin: 'https://hosted.test', 'Content-Type': 'video/mp4', ...(declared ? { 'Content-Length': String(size) } : {}) } }, res => {
      let body = ''; res.on('data', c => { body += c; }); res.on('end', () => resolve({ status: res.statusCode!, body }));
    });
    r.on('error', reject);
    const chunk = Buffer.alloc(64 * 1024);
    let remaining = size;
    const write = () => {
      while (remaining > 0 && !r.destroyed) {
        const amount = Math.min(remaining, chunk.length); remaining -= amount;
        if (!r.write(chunk.subarray(0, amount))) { r.once('drain', write); return; }
      }
      r.end();
    };
    write();
  });
  try {
    const size = 65 * 1024 * 1024;
    const result = await upload(g, size, false);
    assert.equal(result.status, 200); assert.equal(JSON.parse(result.body).size, size); assert.equal(received, size);
    assert.equal((await upload(small, 4097, true)).status, 413);
    const chunked = await upload(small, 4097, false);
    assert.equal(chunked.status, 413); assert.equal(JSON.parse(chunked.body).error, 'payload_too_large');
    assert.equal((await fetch(`http://127.0.0.1:${(g.server.address() as { port: number }).port}${g.prefix}/v1/projects`, { method: 'POST', headers: { Origin: 'https://hosted.test', 'Content-Length': '1048577' }, body: 'x'.repeat(1048577) })).status, 413);
  } finally {
    for (const server of [g.server, small.server, runtime]) server.closeAllConnections();
    await Promise.all([g.server, small.server, runtime].map(server => new Promise<void>(r => server.close(() => r()))));
  }
});

test('cancelled uploads and playback disconnect close upstream streams; transport failures are truthful', async () => {
  let uploadClosed!: () => void;
  let playbackClosed!: () => void;
  const uploadDone = new Promise<void>(r => { uploadClosed = r; });
  const playbackDone = new Promise<void>(r => { playbackClosed = r; });
  const runtime = createServer((req, res) => {
    if (req.method === 'POST') { req.on('data', () => {}); req.on('aborted', uploadClosed); return; }
    if (req.url === '/v1/health') { req.socket.destroy(); return; }
    res.writeHead(200, { 'Content-Type': 'video/mp4' });
    const timer = setInterval(() => res.write(Buffer.alloc(4096)), 5);
    res.on('close', () => { clearInterval(timer); playbackClosed(); });
  });
  await new Promise<void>(r => runtime.listen(0, '127.0.0.1', r));
  const g = createLoopbackGateway({ endpoint: `http://127.0.0.1:${(runtime.address() as { port: number }).port}`, token: 'local', origin: 'https://hosted.test' });
  await new Promise<void>(r => g.server.listen(0, '127.0.0.1', r));
  const options = { hostname: '127.0.0.1', port: (g.server.address() as { port: number }).port, headers: { Origin: 'https://hosted.test' } };
  const bounded = (promise: Promise<void>) => Promise.race([promise, new Promise<never>((_, reject) => { const timer = setTimeout(() => reject(new Error('upstream did not close')), 1500); timer.unref(); })]);
  try {
    const uploading = request({ ...options, path: g.prefix + '/v1/projects/p/objects', method: 'POST' });
    uploading.on('error', () => {}); uploading.write(Buffer.alloc(4096));
    await new Promise(r => setTimeout(r, 40)); uploading.destroy();
    await bounded(uploadDone);
    await new Promise<void>((resolve, reject) => {
      const playing = request({ ...options, path: g.prefix + '/v1/objects/movie' }, res => { res.once('data', () => { res.destroy(); resolve(); }); });
      playing.on('error', reject); playing.end();
    });
    await bounded(playbackDone);
    const failure = await fetch(`http://127.0.0.1:${options.port}${g.prefix}/v1/health`, { headers: options.headers });
    assert.equal(failure.status, 502); assert.equal((await failure.json()).error, 'runtime_unavailable');
  } finally {
    g.server.closeAllConnections(); runtime.closeAllConnections();
    await Promise.all([g.server, runtime].map(server => new Promise<void>(r => server.close(() => r()))));
  }
});

// Idle timeout (design §3 guard): a Runtime that accepts the request and never answers is 504 `upstream_timeout`, not a hang.
test('a Runtime that accepts a request and never answers is a 504 upstream_timeout, and the same gateway still serves the others', async () => {
  const hosted = 'https://hosted.test';
  const stalled: Array<() => void> = [];
  const runtime = createServer((req, res) => {
    if (req.url === '/v1/objects/stall') { req.resume(); req.socket.once('close', () => stalled.forEach(done => done())); return; }
    res.writeHead(200, { 'Content-Type': 'application/json' }); res.end('{"status":"ok"}');
  });
  await new Promise<void>(resolve => runtime.listen(0, '127.0.0.1', resolve));
  const g = createLoopbackGateway({ endpoint: `http://127.0.0.1:${(runtime.address() as { port: number }).port}`, token: 'local', origin: hosted, idleTimeoutMs: 150 });
  await new Promise<void>(resolve => g.server.listen(0, '127.0.0.1', resolve));
  const port = (g.server.address() as { port: number }).port;
  const upstreamClosed = new Promise<void>(resolve => stalled.push(resolve));
  try {
    // The control: an answering route through the same gateway is 200.
    const healthy = await fetch(`http://127.0.0.1:${port}/api/runtime/v1/health`, { headers: { Origin: hosted } });
    assert.equal(healthy.status, 200);
    // The stalled route gets a readable 504 with the CORS header, and the gateway drops its upstream request.
    const stalledResponse = await fetch(`http://127.0.0.1:${port}/api/runtime/v1/objects/stall`, { headers: { Origin: hosted } });
    assert.equal(stalledResponse.status, 504);
    assert.equal((await stalledResponse.json()).error, 'upstream_timeout');
    assert.equal(stalledResponse.headers.get('access-control-allow-origin'), hosted);
    await Promise.race([upstreamClosed, new Promise<never>((_, reject) => { const timer = setTimeout(() => reject(new Error('the stalled upstream request was not closed')), 5000); timer.unref(); })]);
    assert.equal((await fetch(`http://127.0.0.1:${port}/api/runtime/v1/health`, { headers: { Origin: hosted } })).status, 200, 'the gateway serves again after a timeout');
  } finally {
    g.server.closeAllConnections(); runtime.closeAllConnections();
    await Promise.all([g.server, runtime].map(server => new Promise<void>(resolve => server.close(() => resolve()))));
  }
});

// The command-line gateway against a fake Runtime: what it prints, who it names on a taken port, and that ACP is opt-in.
async function withFakeRuntimeFiles<T>(work: (files: { discovery: string; tokenFile: string; realmId: string }) => Promise<T>): Promise<T> {
  const realmId = 'realm-gateway-cli';
  const token = 'cli-product-token-not-for-output';
  const runtime = createServer((req, res) => {
    res.setHeader('Content-Type', 'application/json');
    if (req.url === '/v1/handshake') return res.end(JSON.stringify({ protocol: 'workspace.v1', actor_id: 'cli-actor', realm_id: realmId, scopes: PRODUCT_SCOPES }));
    if (req.url === '/v1/realm') return res.end(JSON.stringify({ realm_id: realmId, display_name: 'Gateway CLI \u001b[31mrealm' }));
    res.end(JSON.stringify({ status: 'ok' }));
  });
  await new Promise<void>(resolve => runtime.listen(0, '127.0.0.1', resolve));
  const dir = mkdtempSync(join(tmpdir(), 'reigh-gateway-cli-'));
  try {
    const discovery = join(dir, 'discovery.json');
    const tokenFile = join(dir, 'credential.json');
    writeFileSync(discovery, JSON.stringify({ endpoint: `http://127.0.0.1:${(runtime.address() as { port: number }).port}`, realm_id: realmId }));
    writeFileSync(tokenFile, JSON.stringify({ token, actor_id: 'cli-actor' }), { mode: 0o600 });
    return await work({ discovery, tokenFile, realmId });
  } finally {
    rmSync(dir, { recursive: true, force: true });
    runtime.closeAllConnections();
    await new Promise<void>(resolve => runtime.close(() => resolve()));
  }
}

function runGateway(args: string[], env: Record<string, string> = {}) {
  const child = spawn(process.execPath, ['--import', 'tsx', 'scripts/reigh-loopback-gateway.ts', ...args], { env: { ...process.env, ...env }, stdio: ['ignore', 'pipe', 'pipe'] });
  const state = { stdout: '', stderr: '', child, exited: new Promise<number | null>(resolve => child.once('close', code => resolve(code))) };
  child.stdout!.on('data', chunk => { state.stdout += chunk; });
  child.stderr!.on('data', chunk => { state.stderr += chunk; });
  const printed = () => new Promise<Record<string, unknown>>((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error(`gateway printed nothing: ${state.stderr}`)), 30_000);
    const check = () => {
      const line = state.stdout.split('\n').find(candidate => candidate.trim().startsWith('{'));
      if (line) { clearTimeout(timer); resolve(JSON.parse(line)); } else if (child.exitCode !== null) { clearTimeout(timer); reject(new Error(`gateway exited ${child.exitCode}: ${state.stderr}`)); } else setTimeout(check, 50);
    };
    check();
  });
  return { child, exited: state.exited, get stdout() { return state.stdout; }, get stderr() { return state.stderr; }, printed };
}

test('the well-known port is 17340', () => {
  assert.equal(DEFAULT_GATEWAY_PORT, 17340);
});

test('the gateway prints {base, realm_id, acp} with no link or secret; a taken port names the realm that holds it', async () => {
  await withFakeRuntimeFiles(async ({ discovery, tokenFile, realmId }) => {
    const origin = 'https://hosted.test';
    const common = ['--discovery', discovery, '--token-file', tokenFile, '--origin', origin];
    const first = runGateway([...common, '--port', '0']);
    try {
      const line = await first.printed();
      const port = Number(new URL(String(line.base)).port);
      assert.deepEqual(Object.keys(line).sort(), ['acp', 'base', 'realm_id']);
      assert.equal(line.base, `http://127.0.0.1:${port}/api/runtime`);
      assert.equal(line.realm_id, realmId);
      assert.equal(line.acp, false, 'ACP is off unless --acp-endpoint is passed');
      assert(!first.stdout.includes('cli-product-token-not-for-output'));
      assert.equal((await fetch(`http://127.0.0.1:${port}/api/runtime/v1/health`, { headers: { Origin: origin } })).status, 200);

      const second = runGateway([...common, '--port', String(port)]);
      assert.equal(await second.exited, 1);
      for (const part of [`port ${port} is already served by a Reigh gateway for realm`, 'Gateway CLI ?[31mrealm', `(${realmId})`]) assert(second.stderr.includes(part), `${part} in: ${second.stderr}`);
      assert(!second.stderr.includes('\u001b'), 'terminal escapes from the holder are not printed');
      assert(!second.stderr.includes('cli-product-token-not-for-output'));
      assert.equal(second.stdout, '');
    } finally {
      first.child.kill('SIGTERM');
      await first.exited;
    }
    // Something that is not a gateway holds the port.
    const squatter = createServer((_req, res) => { res.statusCode = 404; res.end('nope'); });
    await new Promise<void>(resolve => squatter.listen(0, '127.0.0.1', resolve));
    try {
      const taken = (squatter.address() as { port: number }).port;
      const result = runGateway([...common, '--port', String(taken)]);
      assert.equal(await result.exited, 1);
      assert.match(result.stderr, new RegExp(`port ${taken} is already in use by a program that is not a Reigh gateway`));
    } finally { squatter.closeAllConnections(); await new Promise<void>(resolve => squatter.close(() => resolve())); }
  });
});

// Bind guard (design §3): the spawned gateway listens on 127.0.0.1 only. Needs another local address (a LAN or container
// interface) to prove the refusal; a machine with none (loopback only) skips this case.
const nonLoopbackAddress = Object.values(networkInterfaces()).flat().find(entry => entry && entry.family === 'IPv4' && !entry.internal)?.address;
const connectResult = (host: string, port: number) => new Promise<string>(resolve => {
  const socket = connect({ host, port });
  socket.once('connect', () => { socket.destroy(); resolve('connected'); });
  socket.once('error', (error: NodeJS.ErrnoException) => { socket.destroy(); resolve(error.code ?? error.message); });
});
test.skipIf(!nonLoopbackAddress)('the spawned gateway listens on 127.0.0.1 only: a non-loopback local address refuses the connection', async () => {
  await withFakeRuntimeFiles(async ({ discovery, tokenFile }) => {
    const origin = 'https://hosted.test';
    const gateway = runGateway(['--discovery', discovery, '--token-file', tokenFile, '--origin', origin, '--port', '0']);
    try {
      const port = Number(new URL(String((await gateway.printed()).base)).port);
      // The control: the same port answers on 127.0.0.1.
      assert.equal(await connectResult('127.0.0.1', port), 'connected');
      assert.equal((await fetch(`http://127.0.0.1:${port}/api/runtime/v1/health`, { headers: { Origin: origin } })).status, 200);
      // The refusal: the machine's own non-loopback address has nothing listening on that port.
      assert.equal(await connectResult(nonLoopbackAddress!, port), 'ECONNREFUSED', `${nonLoopbackAddress}:${port} must refuse`);
    } finally {
      gateway.child.kill('SIGTERM');
      await gateway.exited;
    }
  });
});

// ---------------------------------------------------------------------------------------------
// The Runtime is read for every request: it moves, rotates its token, changes realm or stops, and the gateway keeps serving.

const HOSTED = 'https://hosted.test';
type FakeRuntime = { server: ReturnType<typeof createServer>; port: number; url: string; handshakes: number; hits: string[]; tokens: string[]; token: string; stop(): Promise<void> };

/** A Runtime that answers the handshake (after a short delay, so concurrent requests overlap it) only for its own token. */
async function fakeRuntime(options: { realmId?: string; token?: string; actor?: string; port?: number; label?: string } = {}): Promise<FakeRuntime> {
  const fake = { handshakes: 0, hits: [] as string[], tokens: [] as string[], token: options.token ?? 'token-1' } as FakeRuntime;
  fake.server = createServer((req, res) => {
    res.setHeader('Content-Type', 'application/json');
    const authorised = req.headers.authorization === `Bearer ${fake.token}`;
    req.resume();
    if (req.url === '/v1/handshake') {
      fake.handshakes += 1;
      if (!authorised) { res.statusCode = 401; res.end('{}'); return; }
      setTimeout(() => res.end(JSON.stringify({ protocol: 'workspace.v1', actor_id: options.actor ?? 'actor', realm_id: options.realmId ?? 'realm-a', scopes: PRODUCT_SCOPES })), 60);
      return;
    }
    fake.hits.push(`${req.method} ${req.url}`);
    fake.tokens.push(String(req.headers.authorization));
    if (!authorised) { res.statusCode = 401; res.end('{}'); return; }
    res.end(JSON.stringify({ status: 'ok', runtime: options.label ?? 'a' }));
  });
  await new Promise<void>(resolve => fake.server.listen(options.port ?? 0, '127.0.0.1', resolve));
  fake.port = (fake.server.address() as { port: number }).port;
  fake.url = `http://127.0.0.1:${fake.port}`;
  fake.stop = async () => { fake.server.closeAllConnections(); await new Promise<void>(resolve => fake.server.close(() => resolve())); };
  return fake;
}

async function withMovingRuntime<T>(work: (context: {
  dir: string; discovery: string; tokenFile: string; point(runtime: FakeRuntime): void; rotate(token: string): void; gatewayCall(path: string, init?: { method?: string; body?: string }): Promise<{ status: number; body: Record<string, string>; headers: import('node:http').IncomingHttpHeaders }>;
  gateway: ReturnType<typeof createLoopbackGateway>; first: FakeRuntime;
}) => Promise<T>): Promise<T> {
  const first = await fakeRuntime({ label: 'first' });
  const dir = mkdtempSync(join(tmpdir(), 'reigh-gateway-moving-'));
  const discovery = join(dir, 'discovery.json');
  const tokenFile = join(dir, 'credential.json');
  const point = (runtime: FakeRuntime) => writeFileSync(discovery, JSON.stringify({ endpoint: runtime.url, realm_id: 'realm-a' }));
  const rotate = (token: string) => writeFileSync(tokenFile, JSON.stringify({ token, actor_id: 'actor' }), { mode: 0o600 });
  point(first); rotate(first.token);
  const source = fileRuntimeSource({ discoveryPath: discovery, tokenFile, realmId: 'realm-a', actor: 'actor' });
  const gateway = createLoopbackGateway({ runtime: { ...source, verified: { endpoint: new URL(first.url), token: first.token } }, origin: HOSTED });
  await new Promise<void>(resolve => gateway.server.listen(0, '127.0.0.1', resolve));
  const port = (gateway.server.address() as { port: number }).port;
  const gatewayCall = (path: string, init: { method?: string; body?: string } = {}) => new Promise<{ status: number; body: Record<string, string>; headers: import('node:http').IncomingHttpHeaders }>((resolve, reject) => {
    const r = request({ hostname: '127.0.0.1', port, path: `/api/runtime${path}`, method: init.method ?? 'GET', headers: { Origin: HOSTED, ...(init.body === undefined ? {} : { 'Content-Type': 'application/json', 'Content-Length': String(Buffer.byteLength(init.body)) }) }, agent: false }, res => {
      const chunks: Buffer[] = [];
      res.on('data', chunk => chunks.push(chunk));
      res.on('end', () => { const text = Buffer.concat(chunks).toString(); resolve({ status: res.statusCode!, headers: res.headers, body: text ? JSON.parse(text) : null }); });
    });
    r.on('error', reject);
    r.end(init.body);
  });
  try {
    return await work({ dir, discovery, tokenFile, point, rotate, gatewayCall, gateway, first });
  } finally {
    gateway.server.closeAllConnections();
    await new Promise<void>(resolve => gateway.server.close(() => resolve()));
    await first.stop();
    rmSync(dir, { recursive: true, force: true });
  }
}

test('the gateway follows a Runtime that moved to a new port or rotated its token, checking its identity once per change', async () => {
  await withMovingRuntime(async ({ point, rotate, gatewayCall, first }) => {
    const second = await fakeRuntime({ label: 'second' });
    const third = await fakeRuntime({ label: 'third', token: 'token-2' });
    try {
      // The Runtime the gateway started with was verified at start: its first request asks nothing.
      assert.deepEqual((await gatewayCall('/v1/health')).body, { status: 'ok', runtime: 'first' });
      assert.equal(first.handshakes, 0);
      // A new port: every one of eight concurrent requests lands on it, and it is asked who it is exactly once.
      point(second);
      const burst = await Promise.all(Array.from({ length: 8 }, () => gatewayCall('/v1/health')));
      assert(burst.every(reply => reply.status === 200 && reply.body.runtime === 'second'), JSON.stringify(burst.map(reply => reply.status)));
      assert.equal(second.handshakes, 1);
      await gatewayCall('/v1/health');
      assert.equal(second.handshakes, 1, 'an unchanged Runtime is not asked again');
      assert.equal(first.hits.length, 1, 'the old port gets nothing more');
      // A rotated token, on the same endpoint: the new token is the one sent upstream, after one more check.
      second.token = 'token-2';
      rotate('token-2');
      const rotated = await Promise.all([gatewayCall('/v1/health'), gatewayCall('/v1/health')]);
      assert(rotated.every(reply => reply.status === 200));
      assert.equal(second.handshakes, 2);
      assert.equal(second.tokens.at(-1), 'Bearer token-2');
      // Both changing at once.
      point(third);
      assert.equal((await gatewayCall('/v1/health')).body.runtime, 'third');
      assert.equal(third.handshakes, 1);
    } finally { await second.stop(); await third.stop(); }
  });
});

test('a Runtime that is down, moved to another realm, or unreadable is a 503 the page can read, and each recovers to 200', async () => {
  await withMovingRuntime(async ({ discovery, tokenFile, point, rotate, gatewayCall, first }) => {
    const holdsPage = (reply: { headers: import('node:http').IncomingHttpHeaders }) => assert.equal(reply.headers['access-control-allow-origin'], HOSTED, 'the page may read the refusal');
    // Down, and the gateway is still listening: nothing answers at the port discovery names.
    await first.stop();
    const down = await gatewayCall('/v1/health');
    assert.equal(down.status, 503); assert.equal(down.body.error, 'runtime_unavailable'); holdsPage(down);
    assert.equal((await gatewayCall('/v1/health')).status, 503);
    // The same port comes back: the Runtime is asked once who it is, then served.
    const again = await fakeRuntime({ port: first.port, label: 'again' });
    try {
      assert.equal((await gatewayCall('/v1/health')).body.runtime, 'again');
      assert.equal(again.handshakes, 1);
    } finally { await again.stop(); }

    // Another realm answers: refused every time, and none of its routes is reached.
    const stranger = await fakeRuntime({ realmId: 'realm-b', label: 'stranger' });
    try {
      point(stranger);
      for (let attempt = 0; attempt < 2; attempt += 1) {
        const changed = await gatewayCall('/v1/health');
        assert.equal(changed.status, 503); assert.equal(changed.body.error, 'realm_changed'); holdsPage(changed);
      }
      assert.deepEqual(stranger.hits, []);
    } finally { await stranger.stop(); }
    // The same realm under a different actor is not this gateway's Runtime either.
    const impostor = await fakeRuntime({ actor: 'someone-else' });
    try {
      point(impostor);
      const mismatch = await gatewayCall('/v1/health');
      assert.equal(mismatch.status, 503); assert.equal(mismatch.body.error, 'runtime_identity_mismatch');
      assert.deepEqual(impostor.hits, []);
    } finally { await impostor.stop(); }

    // A discovery file or credential that cannot be read (half-written, truncated, deleted) is 503, and the next good one is served.
    const good = await fakeRuntime({ label: 'good' });
    try {
      for (const broken of ['{"endpoint": "http://127.0.0.1:', '{}', JSON.stringify({ endpoint: 'http://example.test:80' }), JSON.stringify({ endpoint: 'http://localhost:1234' })]) {
        writeFileSync(discovery, broken);
        const reply = await gatewayCall('/v1/health');
        assert.equal(reply.status, 503, broken); assert.equal(reply.body.error, 'runtime_discovery_invalid', broken); holdsPage(reply);
        point(good);
        assert.equal((await gatewayCall('/v1/health')).status, 200, `recovers after ${broken}`);
      }
      writeFileSync(tokenFile, '{"token": ');
      assert.equal((await gatewayCall('/v1/health')).body.error, 'runtime_discovery_invalid');
      rmSync(tokenFile);
      assert.equal((await gatewayCall('/v1/health')).status, 503);
      rotate(good.token);
      assert.equal((await gatewayCall('/v1/health')).status, 200);
    } finally { await good.stop(); }
  });
});

test('a request with a body is never sent twice; one without is sent again only to a Runtime that moved', async () => {
  const live = await fakeRuntime({ label: 'live' });
  const stale = await fakeRuntime();
  const stalePort = stale.port;
  await stale.stop();
  const staleTarget = { endpoint: new URL(`http://127.0.0.1:${stalePort}`), token: 'token-1' };
  // discovery names a closed port first, then the live Runtime (a restart between reading it and connecting).
  const movingSource = () => {
    const state = { reads: 0, verifies: 0 };
    const source: RuntimeSource = {
      read: () => { state.reads += 1; return { endpoint: state.reads === 1 ? staleTarget.endpoint.href : live.url, token: 'token-1' }; },
      verify: async () => { state.verifies += 1; },
      verified: staleTarget,
    };
    return { state, source };
  };
  const serve = async (source: RuntimeSource) => {
    const gateway = createLoopbackGateway({ runtime: source, origin: HOSTED });
    await new Promise<void>(resolve => gateway.server.listen(0, '127.0.0.1', resolve));
    const port = (gateway.server.address() as { port: number }).port;
    const call = (method: string, body?: string) => fetch(`http://127.0.0.1:${port}/api/runtime/v1/projects`, { method, headers: { Origin: HOSTED, ...(body === undefined ? {} : { 'Content-Type': 'application/json' }) }, ...(body === undefined ? {} : { body }) });
    return { call, close: async () => { gateway.server.closeAllConnections(); await new Promise<void>(resolve => gateway.server.close(() => resolve())); } };
  };
  try {
    const moved = movingSource();
    const gatewayA = await serve(moved.source);
    try {
      const reply = await gatewayA.call('GET');
      assert.equal(reply.status, 200);
      assert.deepEqual(live.hits, ['GET /v1/projects']);
      assert.equal(moved.state.verifies, 1, 'the Runtime it moved to was checked before it was used');
      assert.equal(moved.state.reads, 2);
    } finally { await gatewayA.close(); }

    live.hits.length = 0;
    const posted = movingSource();
    const gatewayB = await serve(posted.source);
    try {
      const reply = await gatewayB.call('POST', JSON.stringify({ name: 'once' }));
      assert.equal(reply.status, 503); assert.equal((await reply.json()).error, 'runtime_unavailable');
      assert.equal(posted.state.reads, 1, 'discovery was not consulted again for the body');
      assert.deepEqual(live.hits, [], 'the POST reached no Runtime');
    } finally { await gatewayB.close(); }

    // Discovery still names the closed port: there is nothing to retry on, so one attempt and a 503.
    const still = { reads: 0 };
    const gatewayC = await serve({ read: () => { still.reads += 1; return { endpoint: staleTarget.endpoint.href, token: 'token-1' }; }, verify: async () => {}, verified: staleTarget });
    try {
      assert.equal((await gatewayC.call('GET')).status, 503);
      assert.equal(still.reads, 2, 'one read for the request, one to see whether it moved');
    } finally { await gatewayC.close(); }
  } finally { await live.stop(); }
});

test('the gateway process keeps listening while the Runtime is down and serves again when discovery names a live one; bad configuration exits 1', async () => {
  await withFakeRuntimeFiles(async ({ discovery, tokenFile }) => {
    const common = ['--discovery', discovery, '--token-file', tokenFile, '--origin', HOSTED];
    const running = runGateway([...common, '--port', '0']);
    try {
      const line = await running.printed();
      const base = String(line.base);
      const health = () => fetch(`${base}/v1/health`, { headers: { Origin: HOSTED } });
      assert.equal((await health()).status, 200);
      const original = JSON.parse(readFileSync(discovery, 'utf8'));
      // Discovery names a port nothing listens on (a Runtime that stopped).
      const closed = createServer(); await new Promise<void>(resolve => closed.listen(0, '127.0.0.1', resolve));
      const closedPort = (closed.address() as { port: number }).port; await new Promise<void>(resolve => closed.close(() => resolve()));
      writeFileSync(discovery, JSON.stringify({ ...original, endpoint: `http://127.0.0.1:${closedPort}` }));
      const down = await health();
      assert.equal(down.status, 503); assert.equal((await down.json()).error, 'runtime_unavailable');
      writeFileSync(discovery, '{"endpoint":');
      assert.equal((await health()).status, 503);
      writeFileSync(discovery, JSON.stringify(original));
      assert.equal((await health()).status, 200);
      assert.equal(running.child.exitCode, null, 'the gateway never exited');
      assert(!running.stdout.includes('cli-product-token-not-for-output') && !running.stderr.includes('cli-product-token-not-for-output'));
    } finally { running.child.kill('SIGTERM'); await running.exited; }

    // Configuration errors stop the process with exit 1 and a sentence on stderr.
    const broken = join(dirname(discovery), 'broken.json');
    writeFileSync(broken, '{"endpoint":');
    for (const [label, args] of [
      ['missing flag', ['--discovery', discovery, '--origin', HOSTED]],
      ['malformed discovery', ['--discovery', broken, '--token-file', tokenFile, '--origin', HOSTED, '--port', '0']],
      ['no such credential', ['--discovery', discovery, '--token-file', join(dirname(discovery), 'absent.json'), '--origin', HOSTED, '--port', '0']],
      ['port out of range', [...common, '--port', '70000']],
    ] as Array<[string, string[]]>) {
      const result = runGateway(args);
      assert.equal(await result.exited, 1, label);
      assert.notEqual(result.stderr.trim(), '', label);
      assert.equal(result.stdout, '', label);
    }
  });
});

test('the health answer carries the local app address when the launcher gave one, and only then', async () => {
  const runtime = createServer((req, res) => {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(req.url === '/v1/health' ? '{"status":"ok","protocol":"workspace.v1","runtime_instance_id":"i-1"}' : '{"realm_id":"r"}');
  });
  await new Promise<void>(resolve => runtime.listen(0, '127.0.0.1', resolve));
  const endpoint = `http://127.0.0.1:${(runtime.address() as { port: number }).port}`;
  const origin = 'https://hosted.test';
  const servers: Array<ReturnType<typeof createLoopbackGateway>['server']> = [];
  const read = async (appUrl: string | undefined, path: string) => {
    const g = createLoopbackGateway({ endpoint, token: 't', origin, ...(appUrl ? { appUrl } : {}) });
    servers.push(g.server);
    await new Promise<void>(resolve => g.server.listen(0, '127.0.0.1', resolve));
    const port = (g.server.address() as { port: number }).port;
    const response = await fetch(`http://127.0.0.1:${port}/api/runtime${path}`, { headers: { Origin: origin } });
    return { status: response.status, length: response.headers.get('content-length'), text: await response.text() };
  };
  try {
    const withApp = await read('http://127.0.0.1:2222', '/v1/health');
    assert.equal(withApp.status, 200);
    assert.deepEqual(JSON.parse(withApp.text), { status: 'ok', protocol: 'workspace.v1', runtime_instance_id: 'i-1', app_url: 'http://127.0.0.1:2222' });
    assert.equal(withApp.length, String(Buffer.byteLength(withApp.text)), 'the length is the rewritten body');
    const without = await read(undefined, '/v1/health');
    assert.deepEqual(JSON.parse(without.text), { status: 'ok', protocol: 'workspace.v1', runtime_instance_id: 'i-1' });
    // Only the health answer is touched.
    assert.deepEqual(JSON.parse((await read('http://127.0.0.1:2222', '/v1/realm')).text), { realm_id: 'r' });
  } finally {
    for (const server of servers) { server.close(); server.closeAllConnections(); }
    runtime.close();
  }
});
