import assert from 'node:assert/strict';
import { test } from 'node:test';
import { createServer, request } from 'node:http';
import { existsSync, mkdtempSync, mkdirSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { createServer as createViteServer } from 'vite';
import { OPERATION_PREFIX as O, createRuntimeProxyServer } from './runtime-discovery-proxy.mjs';
import {
  createRuntimeOperationAdmissionPlugin, createRuntimeOperationProxyOptions,
  createWorkspaceRuntimeProxyOptions,
} from '../config/vite/runtimeProxy.ts';

// Central service only: real HTTP/Vite/proxy, synthetic upstream responses, NOT Runtime acceptance.
// Node fetch does not implement Chrome's Origin/Fetch Metadata policy; the adapter supplies it.
const H = 'X-Astrid-Operation-Handle';
const launch = { actorId: 'astrid-app', realmId: 'realm', runtimeInstanceId: 'instance' };
const scope = { actorId: launch.actorId, realmId: launch.realmId, projectId: 'project-commit', timelineId: 'timeline-commit' };
const saved = { method: 'POST', path: '/v1/projects/project-commit/timelines/timeline-commit/commit', key: 'key-p2',
  body: '{ "project_id":"project-commit", "timeline_id":"timeline-commit", "note":"café 🎞" }\n' };
const deferred = () => {
  let resolveValue;
  const promise = new Promise(resolve => { resolveValue = resolve; });
  return { promise, resolve: resolveValue };
};
const listen = (server, port = 0) => new Promise((resolveListen, reject) => {
  server.once('error', reject);
  server.listen(port, '127.0.0.1', () => resolveListen(server.address().port));
});
const close = server => new Promise(resolveClose => { server.close(resolveClose); server.closeAllConnections(); });
async function freePort() {
  const reservation = createServer();
  const port = await listen(reservation);
  await close(reservation);
  return port;
}
function raw(port, path, { method = 'GET', headers = {}, body } = {}) {
  return new Promise((resolveReply, reject) => {
    const req = request({ hostname: '127.0.0.1', port, path, method, headers }, res => {
      const chunks = [];
      res.on('data', chunk => chunks.push(chunk));
      res.once('error', reject);
      res.once('end', () => resolveReply({ status: res.statusCode, headers: res.headers, body: Buffer.concat(chunks) }));
    });
    req.once('error', reject);
    req.end(body);
  });
}
async function fixture(t) {
  const directory = mkdtempSync(join(tmpdir(), 'operation-host-coupled-'));
  const originalFetch = globalThis.fetch;
  const originalWindow = Object.getOwnPropertyDescriptor(globalThis, 'window');
  const hosts = [];
  const upstreams = [];
  let vite;
  let proxy;
  t.after(async () => {
    hosts.forEach(host => host.dispose());
    globalThis.fetch = originalFetch;
    if (originalWindow) Object.defineProperty(globalThis, 'window', originalWindow);
    else delete globalThis.window;
    await vite?.close();
    if (proxy?.listening) await close(proxy);
    for (const server of upstreams) await close(server);
    rmSync(directory, { recursive: true, force: true });
  });
  const records = [];
  let intercept;
  let accepted;
  let metadata;
  const upstream = async label => {
    const server = createServer(async (req, res) => {
      const chunks = [];
      for await (const chunk of req) chunks.push(chunk);
      const record = { label, method: req.method, path: req.url, headers: req.headers, body: Buffer.concat(chunks) };
      records.push(record);
      if (await intercept?.(req, res, record)) return;
      res.setHeader('Content-Type', 'application/json');
      if (req.url === '/v1/health') res.end(JSON.stringify(metadata.health));
      else if (req.url === '/v1/handshake') res.end(JSON.stringify(metadata.handshake));
      else if (req.url === '/v1/realm') res.end(JSON.stringify({ realm_id: launch.realmId }));
      else if (req.url.endsWith('/commit')) res.end(JSON.stringify(accepted));
      else if (req.url === '/v1/tasks' && req.method === 'POST') res.end(JSON.stringify({ data: { task_id: 'task' }, receipt: {} }));
      else if (req.url === '/v1/tasks/task') res.end(JSON.stringify({ task_id: 'task' }));
      else if (req.url.startsWith('/v1/tasks/task/managed-outputs?')) res.end(JSON.stringify({ items: [{ association_id: 'output' }], next_cursor: null }));
      else if (req.url === '/v1/managed-outputs/output') res.end(JSON.stringify({ association_id: 'output' }));
      else if (req.url.startsWith('/v1/projects/project-commit/media-selection?')) res.end(JSON.stringify({ media_id: 'media' }));
      else if (req.url === '/v1/objects/object') {
        res.writeHead(206, { 'Content-Type': 'application/octet-stream', 'Content-Range': 'bytes 1-3/5', ETag: '"object"', 'Set-Cookie': 'hidden=1' });
        res.end(req.method === 'HEAD' ? undefined : Buffer.from([1, 2, 3]));
      } else { res.statusCode = 404; res.end('{}'); }
    });
    upstreams.push(server);
    return `http://127.0.0.1:${await listen(server)}`;
  };
  const endpoint = await upstream('first');
  const discoveryPath = join(directory, 'discovery.json');
  const credential = join(directory, 'credential.json');
  const realm = join(directory, 'realm');
  mkdirSync(realm);
  writeFileSync(join(directory, 'catalog.json'), JSON.stringify({ selected_realm_id: launch.realmId,
    realms: [{ realm_id: launch.realmId, source_profile: 'astrid', data_root: realm }] }));
  const rotate = (target, token) => {
    writeFileSync(credential, JSON.stringify({ version: 1, scope: 'astrid', actor_id: launch.actorId, token }));
    writeFileSync(discoveryPath, JSON.stringify({ endpoint: target, credential_file: credential,
      active_realm: launch.realmId, runtime_instance_id: launch.runtimeInstanceId, realm_root: realm }));
  };
  rotate(endpoint, 'first-token');
  const appPort = await freePort();
  const origin = `http://127.0.0.1:${appPort}`;
  const proxyPort = await freePort();
  proxy = createRuntimeProxyServer({ discoveryPath, allowedOrigin: origin, expectedHost: `127.0.0.1:${proxyPort}` });
  await listen(proxy, proxyPort);
  const target = `http://127.0.0.1:${proxyPort}`;
  vite = await createViteServer({ configFile: false, envDir: directory, root: process.cwd(), cacheDir: join(directory, '.vite'),
    logLevel: 'silent', appType: 'custom', optimizeDeps: { noDiscovery: true, include: [] },
    resolve: { alias: {
      '@': resolve('src'), '@astrid/editor-sdk': resolve('src/sdk/index.ts'),
      '@banodoco/timeline-schema': existsSync(resolve('vendor/timeline-schema/typescript/dist/src/index.js'))
        ? resolve('vendor/timeline-schema/typescript/dist/src/index.js') : resolve('src/tools/video-editor/lib/timeline-schema.fallback.ts'),
      '@workspace-effects': resolve('vendor/banodoco-effects'),
      '@workspace-animations': resolve('vendor/banodoco-animations'),
      '@workspace-transitions': resolve('vendor/banodoco-transitions'),
    } },
    plugins: [createRuntimeOperationAdmissionPlugin(origin)],
    server: { host: '127.0.0.1', port: appPort, strictPort: true, watch: null, hmr: false, proxy: {
      [O]: createRuntimeOperationProxyOptions(target),
      '/api/runtime': createWorkspaceRuntimeProxyOptions(target, 'startup-token-must-not-reach-bound-route'),
      '/runtime-config/v1/workspace.json': { target, changeOrigin: true },
    } } });
  await vite.listen();
  const { RuntimeOperationHost } = await vite.ssrLoadModule('/src/integrations/runtime/operationHost.ts');
  const client = await vite.ssrLoadModule('/src/integrations/runtime/client.ts');
  const contract = await vite.ssrLoadModule('/src/integrations/runtime/contract-metadata.ts');
  const { acceptedCommit } = await vite.ssrLoadModule('/src/integrations/runtime/__tests__/timelineCommitFixture.ts');
  accepted = acceptedCommit({ revision_id: 'r2', publication_id: 'p2' }, { revision_id: 'r1', publication_id: 'p1' }, { children: true });
  metadata = {
    health: { status: 'ok', protocol: 'workspace.v1', schema_digest: contract.RUNTIME_SCHEMA_DIGEST, runtime_instance_id: launch.runtimeInstanceId },
    handshake: { protocol: 'workspace.v1', schema_digest: contract.RUNTIME_SCHEMA_DIGEST, actor_id: launch.actorId,
      realm_id: launch.realmId, scopes: [...client.RUNTIME_CLIENT_SCOPES], capabilities: [contract.RUNTIME_TARGETED_EXECUTION_CAPABILITY] },
  };
  const calls = [];
  const fetchImpl = (input, init = {}) => {
    const url = new URL(String(input), origin);
    assert.equal(url.origin, origin);
    const headers = new Headers(init.headers);
    headers.set('Origin', origin);
    headers.set('Sec-Fetch-Site', 'same-origin');
    calls.push({ path: url.pathname, init, headers });
    return originalFetch(url, { ...init, headers }); // Immediate native dispatch; no delayed forwarding.
  };
  Object.defineProperty(globalThis, 'window', { configurable: true, value: { location: { origin } } });
  globalThis.fetch = fetchImpl; // Exercise the existing workspace.json launch-policy loader, without mocking it.
  const host = () => { const owner = new RuntimeOperationHost(fetchImpl); hosts.push(owner); return owner; };
  const handle = () => calls.findLast(call => call.path.startsWith(`${O}/runtime/`)).headers.get(H);
  const send = (path, options = {}) => raw(appPort, path, { ...options, headers: { Origin: origin, ...options.headers } });
  return { host, calls, handle, records, rotate, upstream, metadata, proxy, origin, send, accepted,
    intercept(fn) { intercept = fn; } };
}
const socketTest = (name, run) => test(name, { timeout: 20_000 }, run);

socketTest('coupled: production owner negotiates, reads and decodes exact UTF8 bytes through a pinned Vite/proxy binding', async t => {
  const f = await fixture(t);
  const host = f.host();
  const op = await host.bind();
  assert.equal(op.isCurrentIdentity(scope), true);
  assert.deepEqual(await op.getRecoverableIdentity(), { actorId: launch.actorId, realmId: launch.realmId });
  assert(Object.isFrozen(op));
  assert.deepEqual(Object.keys(op).sort(), ['retire', 'isCurrentIdentity', 'getRecoverableIdentity', 'admitTask', 'getTask',
    'listManagedOutputs', 'getManagedOutput', 'getProjectMediaSelection', 'getObject', 'headObject', 'transmit'].sort());
  const firstHandle = f.handle();
  const secondEndpoint = await f.upstream('second');
  f.rotate(secondEndpoint, 'second-token');
  assert.equal((await op.admitTask({ capability_id: 'cap', capability_digest: 'digest', input_object_ids: [] }, 'admission-key')).task_id, 'task');
  assert.equal((await op.getTask('task')).task_id, 'task');
  assert.equal((await op.listManagedOutputs('task', 'a/b')).items[0].association_id, 'output');
  assert.equal((await op.getManagedOutput('output')).association_id, 'output');
  assert.equal((await op.getProjectMediaSelection(scope.projectId, { generation_id: 'g/a' })).media_id, 'media');
  const object = await op.getObject('object', [1, 3]);
  assert.deepEqual([...object.data], [1, 2, 3]);
  assert.equal(object.content_range, 'bytes 1-3/5');
  assert.equal(object.etag, '"object"');
  assert.equal(object.headers['set-cookie'], undefined);
  assert.equal(object.headers['cache-control'], 'no-store');
  assert.equal((await op.headObject('object', [1, 3])).data.length, 0);
  const result = await op.transmit(scope, saved);
  assert.deepEqual(result.response, f.accepted);
  assert.equal(result.receipt, result.response.receipt);
  assert.equal(result.receipt.idempotency_key, saved.key);
  assert.deepEqual(result.accepted, { revisionId: 'r2', publicationId: 'p2' });
  assert.deepEqual(result.canonicalDocument, f.accepted.data.canonical_document);
  assert.equal(result.graph.occurrences.length, 2);
  assert(f.records.every(record => record.label === 'first' && record.headers.authorization === 'Bearer first-token'));
  for (const record of f.records) assert.equal(record.headers[H.toLowerCase()], undefined);
  const commit = f.records.find(record => record.path === saved.path);
  assert.deepEqual(commit.body, Buffer.from(saved.body));
  assert.equal(commit.headers['idempotency-key'], saved.key);
  assert.equal(f.calls.filter(call => call.path.endsWith('/workspace.json')).length, 1);
  assert(f.calls.filter(call => call.path.startsWith(`${O}/runtime/`)).every(call => call.headers.get(H) === firstHandle));
  for (const { init } of f.calls.filter(call => call.path.startsWith(O))) {
    assert.equal(init.mode, 'same-origin'); assert.equal(init.credentials, 'omit');
    assert.equal(init.cache, 'no-store'); assert.equal(init.redirect, 'error'); assert(init.signal);
  }
  const next = await host.reconnect();
  assert.notEqual(f.handle(), firstHandle);
  assert.equal(op.isCurrentIdentity(scope), false);
  assert.equal(next.isCurrentIdentity(scope), true);
  await next.transmit(scope, saved);
  const commits = f.records.filter(record => record.path === saved.path);
  assert.equal(commits[1].label, 'second');
  assert.equal(commits[1].headers.authorization, 'Bearer second-token');
  assert.deepEqual(commits[1].body, commits[0].body);
  assert.equal(commits[1].headers['idempotency-key'], commits[0].headers['idempotency-key']);
});

socketTest('coupled: browser retirement ignores a late fixture ACK and a new equal-identity binding sends the original request', async t => {
  const f = await fixture(t);
  const owner = f.host();
  const old = await owner.bind();
  const oldHandle = f.handle();
  const entered = deferred();
  const release = deferred();
  let first = true;
  f.intercept(async (_req, res, record) => {
    if (record.path !== saved.path || !first) return false;
    first = false; entered.resolve(); await release.promise;
    res.end(JSON.stringify(f.accepted)); return true;
  });
  t.after(() => release.resolve());
  const pending = old.transmit(scope, saved);
  const refused = assert.rejects(pending);
  await entered.promise;
  const replacement = owner.reconnect();
  assert.equal(old.isCurrentIdentity(scope), false);
  const current = await replacement;
  release.resolve();
  await refused;
  await assert.rejects(old.getTask('task'));
  assert.equal((await current.transmit(scope, saved)).receipt.receipt_id, 'p2');
  const commits = f.records.filter(record => record.path === saved.path);
  assert.equal(commits.length, 2);
  assert.deepEqual(commits[0].body, commits[1].body);
  assert.equal(commits[0].headers['idempotency-key'], commits[1].headers['idempotency-key']);
  assert.notEqual(f.handle(), oldHandle);
  assert.equal((await f.send(`${O}/runtime/v1/tasks/task`, { headers: { [H]: oldHandle } })).status, 410);
});

for (const path of ['/v1/health', '/v1/handshake', '/v1/realm', '/v1/tasks/task', '/v1/objects/object']) {
  socketTest(`coupled: dispose rejects a stale socket await at ${path}`, async t => {
    const f = await fixture(t);
    const owner = f.host();
    const negotiating = ['/v1/health', '/v1/handshake', '/v1/realm'].includes(path);
    const op = negotiating ? undefined : await owner.bind();
    const entered = deferred();
    const release = deferred();
    f.intercept(async (_req, res, record) => {
      if (record.path !== path) return false;
      entered.resolve(); await release.promise; res.end('{}'); return true;
    });
    t.after(() => release.resolve());
    const pending = negotiating ? owner.bind() : path.includes('/objects/') ? op.getObject('object') : op.getTask('task');
    const refused = assert.rejects(pending);
    await entered.promise;
    owner.dispose();
    if (op) assert.equal(op.isCurrentIdentity(scope), false);
    release.resolve();
    await refused;
    const count = f.calls.length;
    await assert.rejects(owner.bind());
    if (op) await assert.rejects(op.getTask('task'));
    assert.equal(f.calls.length, count);
  });
}

socketTest('coupled: remote retirement is observed on the next response and server disposal rejects pending work', async t => {
  const f = await fixture(t);
  const owner = f.host();
  const op = await owner.bind();
  const handle = f.handle();
  assert.equal((await f.send(O, { method: 'DELETE', headers: { [H]: handle } })).status, 204);
  assert.equal(op.isCurrentIdentity(scope), true); // Local boolean cannot observe remote retirement synchronously.
  await assert.rejects(op.getTask('task'));
  assert.equal(op.isCurrentIdentity(scope), false);
  const current = await owner.bind();
  const entered = deferred();
  const release = deferred();
  f.intercept(async (_req, res, record) => {
    if (record.path !== saved.path) return false;
    entered.resolve(); await release.promise; res.end(JSON.stringify(f.accepted)); return true;
  });
  t.after(() => release.resolve());
  const refused = assert.rejects(current.transmit(scope, saved));
  await entered.promise;
  await close(f.proxy);
  release.resolve();
  await refused;
  assert.equal(current.isCurrentIdentity(scope), false);
  assert(f.calls.every(call => !call.path.startsWith('/api/runtime')));
});

socketTest('coupled: wrong realm refuses real negotiation and malformed fixture receipts never trigger fallback reads', async t => {
  const f = await fixture(t);
  f.metadata.handshake.realm_id = 'wrong-realm';
  const owner = f.host();
  await assert.rejects(owner.bind(), /authority/);
  assert.equal(f.records.filter(record => record.path === saved.path).length, 0);
  f.metadata.handshake.realm_id = launch.realmId;
  const op = await owner.bind();
  f.accepted.receipt.project_id = 'wrong-project';
  await assert.rejects(op.transmit(scope, saved), /invalid/);
  assert.equal(op.isCurrentIdentity(scope), false);
  assert(f.records.every(record => !record.path.includes('/inspect') && !record.path.includes('/composition-revisions/')));
});

socketTest('coupled: forbidden origin, duplicate Connection nominations and alternative proxy paths fail closed', async t => {
  const f = await fixture(t);
  const op = await f.host().bind();
  const handle = f.handle();
  let count = f.records.length;
  for (const [path, headers, status] of [
    [`${O}/runtime/v1/tasks/task`, { [H]: handle, Origin: 'http://evil.invalid' }, 403],
    ['/api/runtime/v1/tasks/task', { [H]: handle }, 400],
    [`${O}/extra`, { [H]: handle }, 400],
    [`${O}/runtime/v1/%2e%2e/tasks`, { [H]: handle }, 400],
    [`${O}/runtime/v1/tasks/task`, { [H]: handle, Connection: ['X-First', `x-SeCoNd, ${H}`], 'X-First': 'secret', 'X-Second': 'secret' }, 400],
  ]) {
    assert.equal((await f.send(path, { headers })).status, status, path);
    assert.equal(f.records.length, count);
  }
  const response = await f.send(`${O}/runtime/v1/tasks/task`, { headers: { [H]: handle,
    Connection: ['X-First, Authorization', 'x-SeCoNd, Cookie'], 'X-First': 'secret', 'X-Second': 'secret',
    Authorization: 'Bearer browser-secret', Cookie: 'secret=1' } });
  assert.equal(response.status, 200);
  const last = f.records.at(-1);
  assert.equal(last.headers.authorization, 'Bearer first-token');
  for (const key of ['x-first', 'x-second', 'cookie', H.toLowerCase()]) assert.equal(last.headers[key], undefined);
  assert.equal(op.isCurrentIdentity(scope), true);
  count = f.calls.length;
  op.retire();
  assert.equal(op.isCurrentIdentity(scope), false);
  await assert.rejects(op.transmit({ ...scope, realmId: 'wrong' }, saved));
  assert.equal(f.calls.length, count + 1); // Best-effort DELETE only.
});
