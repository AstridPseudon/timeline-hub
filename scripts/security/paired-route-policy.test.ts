import assert from 'node:assert/strict';
import { test } from 'node:test';
import { createServer, request, type IncomingHttpHeaders } from 'node:http';
import { once } from 'node:events';
import { readFileSync, mkdtempSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawn, execFile } from 'node:child_process';
import { createInterface } from 'node:readline';
import { promisify } from 'node:util';
import ts from 'typescript';
import { WebSocket } from 'ws';
import { ACP_ROUTE_ENTRIES } from '../../src/integrations/astrid/acpRouteContract.ts';
import { PAIRED_CONSUMER_ROUTES } from '../../config/vite/pairedConsumerPolicy.generated.ts';
import * as policy from '../../config/vite/pairedRoutePolicy.ts';
import { PAIRED_SESSION_HEADER, validatedPairedSession } from '../../config/vite/pairedSessionContext.ts';
import { PairedRelay } from '../../config/vite/pairedRelay.ts';
import { allowedAcpRoute, allowedRoute, loopbackEndpoint, PRODUCT_SCOPES } from '../reigh-loopback-gateway.ts';

const samples = PAIRED_CONSUMER_ROUTES.map(route => ({ ...route, path: route.path.replace(/:[A-Za-z]+/g, 'disposable') }));
const acpSamples = ACP_ROUTE_ENTRIES.map(route => ({ service: 'acp', method: route.method, path: route.template.replace(/:[A-Za-z]+/g, 'disposable') }));
const publicPath = (route: {service: string; path: string}) => `/api/${route.service === 'runtime' ? 'runtime' : 'astrid'}${route.path}`;

test('every consumer observation passes; every unsupported method and unknown suffix defaults to deny', () => {
  for (const route of [...samples, ...acpSamples]) {
    const path = publicPath(route);
    assert.equal(policy.classifyPairedRoute(path, route.method)?.service, route.service, `${route.method} ${path}`);
    for (const method of ['GET', 'HEAD', 'POST', 'PATCH', 'PUT', 'DELETE', 'OPTIONS', 'TRACE', 'CONNECT']) {
      const expected = [...samples, ...acpSamples].some(other => publicPath(other) === path && other.method === method);
      assert.equal(policy.classifyPairedRoute(path, method) !== null, expected, `${method} ${path}`);
    }
    assert.equal(policy.classifyPairedRoute(`${path}/unknown-operation/unknown-operation/unknown-operation/unknown-operation/unknown-operation/unknown-operation`, route.method), null);
    if (route.service === 'runtime') assert(allowedRoute(route.path, route.method));
    if (route.service === 'acp') assert(allowedAcpRoute(route.path, route.method));
  }
  for (const path of ['/v1/doctor', '/v1/backup', '/v1/restore', '/v1/attempts/a/settle', '/v1/tasks/claim', '/v1/executors', '/v1/projects/p/timelines/t/commit', '/publish-document', '/v1/projects/p/documents/unknown']) {
    assert.equal(policy.classifyPairedRoute(`/api/runtime${path}`, 'POST'), null);
  }
  assert.equal(policy.classifyPairedRoute('/api/astrid/v1/projects/p/anything/nested', 'GET'), null);
  assert.equal(policy.classifyPairedRoute('/api/astrid/v1/handshake', 'POST'), null);
  for (const prefix of ['runtime', 'astrid']) for (const path of ['/v1/tasks/claim', '/v1/projects/selection']) for (const method of ['GET', 'POST', 'PUT']) assert.equal(policy.classifyPairedRoute(`/api/${prefix}${path}`, method), null);
  assert.equal(policy.classifyPairedRoute('/api/runtimeevil/v1/health', 'GET'), null);
  for (const path of ['/api/runtime/v1/objects/a%2Fb', '/api/runtime/v1/objects/a%252Fb', '/api/runtime/v1/objects/../health', '/api/runtime/v1/health#ignored', '/api/runtime//v1/health']) assert(!policy.isSafeForwardPath(path));
});

test('selected-media consumers use only the exact Runtime GET route', () => {
  const path = '/api/runtime/v1/projects/p/media-selection?association_id=output&object_id=sha256%3Aa&version=2';
  assert.deepEqual(policy.classifyPairedRoute(path, 'GET'), {service: 'runtime', upstreamPath: path.slice('/api/runtime'.length), stream: false});
  for (const method of ['POST', 'PATCH', 'PUT', 'DELETE']) assert.equal(policy.classifyPairedRoute(path, method), null);
  for (const suffix of ['/extra', '-other']) assert.equal(policy.classifyPairedRoute('/api/runtime/v1/projects/p/media-selection'+suffix, 'GET'), null);
  assert.equal(policy.classifyPairedRoute('/api/astrid/v1/projects/p/media-selection', 'GET'), null);
});

test('only consumer and media framing headers are forwarded with canonical names', () => {
  const positive = Object.fromEntries([...policy.PAIRED_FORWARD_HEADERS].map(name => [name.toUpperCase(), 'fixture']));
  assert.equal(policy.hasUnapprovedHeaders(positive), false);
  assert.deepEqual(Object.keys(policy.forwardHeaders(positive)).sort(), [...policy.PAIRED_FORWARD_HEADERS].sort());
  assert.deepEqual(policy.forwardHeaders({ 'X-Astrid-Session': 'disposable-session' }), { 'x-astrid-session': 'disposable-session' });
  for (const name of ['x-hostile-canary', 'x-reigh-paired-session', 'authorization', 'x-output-binding', 'x-astrid-bridge-version', 'x-filename', 'x-expected-version', 'unknown']) {
    assert(policy.hasUnapprovedHeaders({ [name]: 'disposable' }), name);
    assert.deepEqual(policy.forwardHeaders({ [name]: 'disposable' }), {});
  }
  assert.deepEqual(policy.forwardHeaders({ origin: 'https://fake.test', cookie: 'disposable', host: 'fake.test' }), {});
  assert(policy.hasUnapprovedHeaders({ 'x-original-name': ['a', 'b'] }));
  assert(policy.hasUnapprovedHeaders({ 'x-original-name': 'a\r\nb' }));
  assert(policy.hasUnapprovedHeaders({ Accept: 'a', accept: 'b' }));
  assert.equal(policy.classifyPairedRoute('/api/runtime/v1/health', 'GET', { 'Content-Length': '9007199254740992' }), null);
});

function call(port: number, path: string, method: string, headers: Record<string, string> = {}, body = '', chunked = false): Promise<{status: number; headers: IncomingHttpHeaders; body: string}> {
  return new Promise((resolve, reject) => {
    const req = request({ hostname: '127.0.0.1', port, path, method, headers: { ...headers, ...(body && !chunked ? { 'Content-Length': String(Buffer.byteLength(body)) } : {}) } }, res => {
      const chunks: Buffer[] = [];
      res.on('data', chunk => chunks.push(chunk));
      res.on('end', () => resolve({ status: res.statusCode!, headers: res.headers, body: Buffer.concat(chunks).toString() }));
    });
    req.on('error', reject);
    if (body) req.write(body);
    req.end();
  });
}

test('local-helper CLI canary enforces exact hosted origin, host, identity and loopback binding', { timeout: 30_000 }, async t => {
  // Exercise main(), including discovery/credential validation and its real listen().
  // lsof observes only this test-owned PID; it detects a wildcard listener even if
  // the CLI advertises a loopback URL. No production listen/handler is mocked.
  const scratch = mkdtempSync(join(tmpdir(), 'helper-origin-'));
  const token = 'synthetic-helper-product-credential';
  const actor = 'synthetic-helper-actor';
  const realm = 'synthetic-helper-realm';
  const origin = 'https://hosted.test';
  const tokenFile = join(scratch, 'credential.json');
  const auditFile = join(scratch, 'audit.jsonl');
  writeFileSync(tokenFile, JSON.stringify({ token, actor_id: actor }), { mode: 0o600 });
  const identity = { protocol: 'workspace.v1', actor_id: actor, realm_id: realm, scopes: PRODUCT_SCOPES };
  let handshakeIdentity: Record<string, unknown> = identity;
  let handshakes = 0;
  const forwarded: Array<{ path: string; method: string; authenticated: boolean; loopback: boolean }> = [];
  const backend = createServer(async (req, res) => {
    if (req.url === '/v1/handshake') {
      handshakes += 1;
      const chunks: Buffer[] = [];
      for await (const chunk of req) chunks.push(Buffer.from(chunk));
      assert(req.headers.authorization === `Bearer ${token}`, 'synthetic handshake credential');
      assert.deepEqual(JSON.parse(Buffer.concat(chunks).toString()), {
        protocol: 'workspace.v1', client_name: 'reigh-loopback-gateway', client_version: '1', requested_scopes: PRODUCT_SCOPES,
      });
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify(handshakeIdentity));
      return;
    }
    forwarded.push({ path: req.url!, method: req.method!, authenticated: req.headers.authorization === `Bearer ${token}`, loopback: req.socket.localAddress === '127.0.0.1' && req.socket.remoteAddress === '127.0.0.1' });
    res.writeHead(206, { 'Content-Type': 'application/octet-stream', 'Content-Range': 'bytes 0-2/6', ETag: '"synthetic-local"', 'Set-Cookie': 'synthetic=not-forwarded' });
    res.end('PNG');
  });
  const children: Array<{ child: ReturnType<typeof spawn>; closed: Promise<unknown> }> = [];
  let launchNumber = 0;
  const launch = async (endpoint: string) => {
    const discoveryFile = join(scratch, `discovery-${++launchNumber}.json`);
    writeFileSync(discoveryFile, JSON.stringify({ endpoint, actor_id: actor, realm_id: realm }), { mode: 0o600 });
    // An allowlisted environment prevents ambient Runtime/ACP credentials, Node
    // preload hooks or proxy configuration from entering this synthetic fixture.
    const env = Object.fromEntries(['PATH', 'TMPDIR', 'TMP', 'TEMP', 'SystemRoot'].flatMap(key => process.env[key] ? [[key, process.env[key]!]] : []));
    const child = spawn(process.execPath, ['--import', import.meta.resolve('tsx'), fileURLToPath(new URL('../reigh-loopback-gateway.ts', import.meta.url)), '--discovery', discoveryFile, '--token-file', tokenFile, '--origin', origin, '--port', '0', '--audit-log', auditFile], { env, stdio: ['ignore', 'pipe', 'pipe'] });
    const closed = once(child, 'close');
    children.push({ child, closed });
    let stderr = '';
    child.stderr!.on('data', chunk => { stderr += chunk; });
    const lines = createInterface({ input: child.stdout! });
    const outcome = await new Promise<{ ready?: { base: string; realm_id: string }; code?: number | null; error?: string }>((resolve, reject) => {
      const timer = setTimeout(() => reject(new Error('test-owned helper startup did not settle')), 5000);
      const finish = (result: { ready?: { base: string; realm_id: string }; code?: number | null; error?: string }) => { clearTimeout(timer); resolve(result); };
      lines.once('line', line => {
        try { finish({ ready: JSON.parse(line) }); } catch { clearTimeout(timer); reject(new Error('invalid helper startup record')); }
      });
      child.once('error', () => { clearTimeout(timer); reject(new Error('test-owned helper failed to spawn')); });
      child.once('close', code => finish({ code, error: stderr.trim() }));
    });
    return { child, outcome };
  };
  try {
    await new Promise<void>(resolve => backend.listen(0, '127.0.0.1', resolve));
    const endpoint = `http://127.0.0.1:${(backend.address() as {port: number}).port}`;
    assert.equal(loopbackEndpoint(endpoint).origin, endpoint);
    const endpointNegatives = [
      'http://0.0.0.0:1234', 'http://localhost:1234', 'http://[::1]:1234', 'http://192.0.2.1:1234',
      'https://127.0.0.1:1234', 'http://127.0.0.1', 'http://user:pass@127.0.0.1:1234',
      `${endpoint}/redirect`, `${endpoint}/?target=remote`, `${endpoint}/#fragment`,
    ];
    for (const invalid of endpointNegatives) assert.throws(() => loopbackEndpoint(invalid), /Runtime must be a fixed/);
    const endpointRefused = await launch('http://0.0.0.0:1234');
    assert.equal(endpointRefused.outcome.code, 1);
    assert.equal(endpointRefused.outcome.error, 'Runtime must be a fixed http://127.0.0.1:PORT origin');
    assert.equal(handshakes, 0, 'invalid discovery endpoint never contacted');
    for (const mismatch of [
      { ...identity, protocol: 'wrong.v1' }, { ...identity, actor_id: 'different-actor' },
      { ...identity, realm_id: 'different-realm' }, { ...identity, scopes: ['handshake'] },
    ]) {
      handshakeIdentity = mismatch;
      const refused = await launch(endpoint);
      assert.equal(refused.outcome.code, 1);
      assert.equal(refused.outcome.error, 'Scoped runtime product identity did not match');
      assert.equal(forwarded.length, 0, 'identity refusal never forwards product requests');
    }
    handshakeIdentity = identity;
    const { child, outcome } = await launch(endpoint);
    assert(outcome.ready, 'valid synthetic discovery identity starts helper');
    assert.equal(outcome.ready.realm_id, realm);
    const base = new URL(outcome.ready.base);
    assert.equal(base.hostname, '127.0.0.1');
    const port = Number(base.port);
    const { stdout: listeners } = await promisify(execFile)('lsof', ['-nP', '-a', '-p', String(child.pid), '-iTCP', '-sTCP:LISTEN', '-Fn'], { timeout: 3000 });
    const bound = listeners.split('\n').filter(line => line.startsWith('n')).map(line => line.slice(1));
    assert.deepEqual(bound, [`127.0.0.1:${port}`]);
    const path = `${base.pathname}/v1/objects/synthetic`;
    const refusals: Array<{ case: string; status: number; error: string; upstream_calls: number }> = [];
    const refuse = async (name: string, headers: Record<string, string>, status = 403, error = 'hosted_origin_required', method = 'GET', target = path) => {
      const result = await call(port, target, method, headers);
      assert.equal(result.status, status, name);
      assert.equal(JSON.parse(result.body).error, error, name);
      assert.equal(forwarded.length, 0, name);
      refusals.push({ case: name, status: result.status, error, upstream_calls: forwarded.length });
    };
    for (const hostile of ['https://evil.test', 'https://hosted.test.evil.test', 'http://hosted.test', 'https://hosted.test:444', 'https://hosted.test/', 'null']) {
      await refuse(hostile, { Origin: hostile, Referer: `${origin}/editor` });
    }
    await refuse('missing-origin-and-referer', {});
    await refuse('hostile-preflight', { Origin: 'https://evil.test', 'Access-Control-Request-Method': 'GET' }, 403, 'hosted_origin_required', 'OPTIONS');
    for (const host of [`localhost:${port}`, 'hosted.test', `127.0.0.1:${port + 1}`]) await refuse('invalid-host', { Origin: origin, Host: host }, 403, 'invalid_host');
    await refuse('missing-session', { Origin: origin }, 401, 'session_required', 'GET', '/session/wrong/api/runtime/v1/health');
    await refuse('browser-credential', { Origin: origin, Authorization: 'Bearer synthetic-browser' }, 403, 'browser_credentials_forbidden');
    await refuse('unsupported-route', { Origin: origin }, 404, 'route_not_allowed', 'GET', `${base.pathname}/v1/doctor`);
    const positive = await call(port, path, 'GET', { Origin: origin, Range: 'bytes=0-2' });
    assert.equal(positive.status, 206); assert.equal(positive.body, 'PNG');
    assert.equal(positive.headers['content-range'], 'bytes 0-2/6');
    assert.equal(positive.headers.etag, '"synthetic-local"');
    assert.equal(positive.headers['access-control-allow-origin'], origin);
    assert.equal(positive.headers['set-cookie'], undefined);
    assert.deepEqual(forwarded, [{ path: '/v1/objects/synthetic', method: 'GET', authenticated: true, loopback: true }]);
    const audit = readFileSync(auditFile, 'utf8');
    assert(!audit.includes(token), 'audit redacts product credential');
    assert(!audit.includes(base.pathname.split('/')[2]), 'audit redacts session capability');
    assert(!audit.includes('synthetic-browser'), 'audit redacts browser credential');
    const entries = audit.trim().split('\n').map(line => JSON.parse(line));
    assert(entries.some(entry => entry.status === 403 && entry.origin === 'https://evil.test'));
    assert(entries.some(entry => entry.status === 206 && entry.response_bytes === 3));
    t.diagnostic(JSON.stringify({ helper_pid: child.pid, listener: bound[0], endpoint_negatives: endpointNegatives.length, identity_refusals: 4, handshakes, refusals, positive: { status: positive.status, body: positive.body, upstream_calls: forwarded.length, fixed_loopback: true }, audit_entries: entries.length, audit_credentials_redacted: true, second_machine_LAN: 'not exercised; remains open' }));
  } finally {
    for (const { child } of children) if (child.exitCode === null && child.signalCode === null) child.kill('SIGTERM');
    await Promise.all(children.map(({ closed }) => closed));
    backend.closeAllConnections();
    await new Promise<void>(resolve => backend.close(() => resolve()));
    rmSync(scratch, { recursive: true, force: true });
    t.diagnostic(JSON.stringify({ owned_children: children.map(({ child }) => ({ pid: child.pid, exit_code: child.exitCode, signal: child.signalCode })), fixture_removed: true }));
  }
});

async function withRelay(run: (venue: {port: number; origin: string; cookie: string; frames: Record<string, any>[]; waitForFrame(type: string): Promise<void>}) => Promise<void>) {
  const config = { origin: '', loopbackTest: true, enabled: true };
  const relay = new PairedRelay(config);
  const server = createServer(relay.handler());
  relay.installUpgrade(server as never);
  await new Promise<void>(resolve => server.listen(0, '127.0.0.1', resolve));
  const port = (server.address() as {port: number}).port;
  config.origin = `http://127.0.0.1:${port}`;
  const socket = new WebSocket(`${config.origin.replace('http:', 'ws:')}/api/pairing/connector`);
  const frames: Record<string, any>[] = [];
  const waitForFrame = async (type: string) => {
    if (frames.some(frame => frame.type === type)) return;
    while (!frames.some(frame => frame.type === type)) await once(socket, 'message');
  };
  try {
    await once(socket, 'open');
    const hello = once(socket, 'message');
    socket.send(JSON.stringify({ type: 'connector_hello', connector_id: 'fixture', connector_secret: 'synthetic-credential', realm_id: 'disposable' }));
    const ack = JSON.parse((await hello)[0].toString());
    socket.on('message', raw => {
      const frame = JSON.parse(raw.toString()); if (frame.type.startsWith('request_')) frames.push(frame);
      if (frame.type === 'request_end') {
        socket.send(JSON.stringify({ type: 'response_start', id: frame.id, status: 200, headers: { 'content-type': 'application/json' } }));
        socket.send(JSON.stringify({ type: 'response_chunk', id: frame.id, data: Buffer.from('{"synthetic":true}').toString('base64') }));
        socket.send(JSON.stringify({ type: 'response_end', id: frame.id }));
      }
    });
    const redeem = await call(port, '/api/pairing/redeem', 'POST', { Origin: config.origin, 'Content-Type': 'application/json' }, JSON.stringify({ invitation: ack.invitation }));
    assert.equal(redeem.status, 200);
    const cookie = String(redeem.headers['set-cookie']).split(';', 1)[0];
    await run({ port, origin: config.origin, cookie, frames, waitForFrame });
  } finally {
    relay.restart(); socket.terminate(); server.closeAllConnections();
    await new Promise<void>(resolve => server.close(() => resolve()));
  }
}

test('live relay refuses hostile headers and unsupported paths/methods before the connector', {timeout: 10000}, async () => {
  await withRelay(async ({port, origin, cookie, frames}) => {
    const headers = { Origin: origin, Cookie: cookie };
    for (const name of ['X-Hostile-Canary', 'X-Reigh-Paired-Session', 'Authorization', 'X-Output-Binding']) {
      const result = await call(port, '/api/runtime/v1/health', 'GET', { ...headers, [name]: 'disposable' });
      assert.equal(result.status, 403); assert.equal(JSON.parse(result.body).error, 'paired_header_not_allowed');
    }
    assert.equal((await call(port, '/api/runtime/v1/health', 'DELETE', headers)).status, 404);
    assert.equal((await call(port, '/api/runtime/v1/unlisted', 'GET', headers)).status, 404);
    assert.equal(frames.length, 0);
    for (const path of ['/api/runtime/v1/projects/p/timelines/t/composition-revisions', '/api/astrid/acp/projects/p/chat/main']) {
      assert.equal((await call(port, path, path.endsWith('/main') ? 'PATCH' : 'GET', headers)).status, 200);
    }
  });
});

test('relay chunks bounded synthetic JSON above 128KiB, refusing declared and observed overflow independently', {timeout: 10000}, async () => {
  await withRelay(async ({port, origin, cookie, frames, waitForFrame}) => {
    const path = '/api/runtime/v1/projects/p/timelines/t/composition-revisions';
    const headers = { Origin: origin, Cookie: cookie, 'Content-Type': 'application/json', 'Idempotency-Key': 'disposable' };
    const body = JSON.stringify({ synthetic: 'x'.repeat(policy.PAIRED_MAX_JSON_BYTES - 16) });
    assert.equal(Buffer.byteLength(body), policy.PAIRED_MAX_JSON_BYTES);
    for (const chunked of [false, true]) {
      frames.length = 0;
      assert.equal((await call(port, path, 'POST', headers, body, chunked)).status, 200);
      const chunks = frames.filter(f => f.type === 'request_chunk');
      assert(chunks.length > 3);
      assert(chunks.every(f => Buffer.from(f.data, 'base64').length <= 40 * 1024));
      assert.equal(Buffer.concat(chunks.map(f => Buffer.from(f.data, 'base64'))).toString(), body);
      assert(frames.some(f => f.type === 'request_end'));
    }
    frames.length = 0;
    assert.equal((await call(port, path, 'POST', headers, body + ' ')).status, 413);
    assert.equal(frames.length, 0);
    assert.equal((await call(port, path, 'POST', headers, body + ' ', true)).status, 413);
    await waitForFrame('request_cancel');
    assert(frames.some(f => f.type === 'request_cancel'));
    assert(!frames.some(f => f.type === 'request_end'));
    frames.length = 0;
    assert.equal((await call(port, '/api/runtime/v1/projects/p/objects', 'POST', { Origin: origin, Cookie: cookie }, 'x', true)).status, 411);
    assert.equal((await call(port, '/api/astrid/acp/projects/p/chat/draft', 'PATCH', headers, 'x'.repeat(policy.PAIRED_MAX_CONTROL_JSON_BYTES + 1))).status, 413);
    assert.equal((await call(port, '/api/astrid/generation/compose', 'POST', headers, 'x'.repeat(policy.PAIRED_MAX_COMPOSE_JSON_BYTES + 1))).status, 413);
  });
});

// Compile the actual connector function without importing its executable entry
// point, which would read discovery/credentials and contact a Runtime.
test('connector rechecks service, normalizes and preserves media headers, and uses the same JSON cap', async () => {
  const source = ts.createSourceFile('connector.ts', readFileSync(new URL('../reigh-local-connector.ts', import.meta.url), 'utf8'), ts.ScriptTarget.Latest, true);
  const functions = ['routePath', 'beginRequest'].map(name => {
    const declaration = source.statements.find(node => ts.isFunctionDeclaration(node) && node.name?.text === name);
    assert(declaration, name); return declaration.getText(source);
  });
  const messages: Record<string, unknown>[] = [];
  const requests = new Map();
  const outgoing: Record<string, string>[] = [];
  const redirects: string[] = [];
  const context = { pair_id: 'p', connector_id: 'c', realm_id: 'r', generation: 1, expires_at: Date.now() + 60_000 };
  const dependencies = { ...policy, PAIRED_SESSION_HEADER, validatedPairedSession, state: { connectorId: 'c' }, realm: { realm_id: 'r' }, generation: 1, pairs: new Map([['p', context.expires_at]]), send: (message: Record<string, unknown>) => messages.push(message), requests, endpoint: new URL('http://127.0.0.1:1'), token: 'synthetic-product', acpBridgeToken: 'synthetic-acp', process: {env: {}}, ASTRID_BRIDGE_PROTOCOL_HEADER: 'X-Astrid-Bridge-Version', ASTRID_BRIDGE_PROTOCOL_VERSION: 'v1', pausedResponses: new Map(), fetch: async (_url: URL, options: {headers: Record<string, string>; redirect: string}) => { outgoing.push(options.headers); redirects.push(options.redirect); return { status: 200, headers: new Headers(), body: null }; } };
  const compiled = ts.transpileModule(functions.join('\n'), {compilerOptions: {target: ts.ScriptTarget.ES2022}}).outputText;
  const begin = new Function(...Object.keys(dependencies), `${compiled}; return beginRequest;`)(...Object.values(dependencies));
  await begin('a', 'runtime', '/v1/projects/p/media-imports', 'POST', { 'Content-Length': '1', 'X-Expected-Digest': 'sha256:disposable', 'X-Media-Width': '2', 'X-Media-Height': '3', 'X-Media-Duration-Seconds': '1' }, context);
  assert.equal(outgoing.length, 1);
  assert.equal(outgoing[0]['x-media-width'], '2'); assert.equal(outgoing[0]['x-expected-digest'], 'sha256:disposable');
  assert.equal(outgoing[0].Authorization, 'Bearer synthetic-product');
  assert.equal(redirects[0], 'error');
  assert.deepEqual(JSON.parse(outgoing[0][PAIRED_SESSION_HEADER]), context);
  for (const [service, path, method, headers] of [
    ['runtime', '/v1/health', 'GET', {'x-hostile-canary': 'disposable'}],
    ['astrid', '/acp/connect', 'POST', {}],
    ['runtime', '/v1/projects/p/media-imports', 'POST', {}],
    ['runtime', '/v1/projects/p/timelines/t/composition-revisions', 'POST', {'content-length': String(policy.PAIRED_MAX_JSON_BYTES + 1)}],
  ] as const) await begin('reject', service, path, method, headers, context);
  assert.equal(outgoing.length, 1); assert.equal(messages.filter(m => m.type === 'response_error').length, 4);
  let redirectedHits = 0;
  const redirected = createServer((_req, res) => { redirectedHits += 1; res.end('should never be fetched'); });
  await new Promise<void>(resolve => redirected.listen(0, '127.0.0.1', resolve));
  const redirectPort = (redirected.address() as {port: number}).port;
  const local = createServer((_req, res) => { res.writeHead(307, { Location: `http://127.0.0.1:${redirectPort}/unapproved` }); res.end(); });
  await new Promise<void>(resolve => local.listen(0, '127.0.0.1', resolve));
  try {
    const fixed = { ...dependencies, endpoint: new URL(`http://127.0.0.1:${(local.address() as {port: number}).port}`), fetch: globalThis.fetch };
    const beginLocal = new Function(...Object.keys(fixed), `${compiled}; return beginRequest;`)(...Object.values(fixed));
    await beginLocal('redirect', 'runtime', '/v1/objects/disposable', 'GET', {}, context);
    assert.equal(redirectedHits, 0);
    assert(messages.some(message => message.id === 'redirect' && message.type === 'response_error'));
  } finally {
    for (const server of [local, redirected]) server.closeAllConnections();
    await Promise.all([local, redirected].map(server => new Promise<void>(resolve => server.close(() => resolve()))));
  }
});
