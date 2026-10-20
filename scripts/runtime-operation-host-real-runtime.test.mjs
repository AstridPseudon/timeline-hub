import assert from 'node:assert/strict';
import { test } from 'node:test';
import { createServer } from 'node:http';
import { existsSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { isAbsolute, join, resolve } from 'node:path';
import { createServer as createViteServer } from 'vite';
import { createFakeIndexedDB } from '../vendor/fake-indexeddb/index.js';
import { OPERATION_PREFIX as O, createRuntimeProxyServer } from './runtime-discovery-proxy.mjs';
import { createRuntimeOperationAdmissionPlugin, createRuntimeOperationProxyOptions } from '../config/vite/runtimeProxy.ts';
import { assertProofSources, parseProofInputs } from './runtime-operation-proof-inputs.mjs';

const H = 'X-Astrid-Operation-Handle';
const json = file => JSON.parse(readFileSync(file, 'utf8'));
const listen = (server, port = 0) => new Promise((done, reject) => {
  server.once('error', reject);
  server.listen(port, '127.0.0.1', () => done(server.address().port));
});
const close = server => new Promise(done => { server.close(done); server.closeAllConnections(); });
async function freePort() { const server = createServer(); const port = await listen(server); await close(server); return port; }

// Central service only. Real SQLite Runtime acceptance/restart; Node fetch supplies browser metadata.
// The vendored fake IndexedDB and in-process locks prove session recovery, NOT browser disk durability.
test('real Runtime: same-origin operation retains an exact outbox request across lost ACK and relaunch', { timeout: 300_000 }, async t => {
  assert.equal(process.env.TIMELINE_PROXY_REAL_RUNTIME_RUN, '1', 'central service must explicitly authorize this socket lane');
  assert(isAbsolute(process.env.TIMELINE_PROXY_PROOF_INPUTS ?? ''), 'service must name its proof input JSON by absolute path');
  const inputs = parseProofInputs(json(process.env.TIMELINE_PROXY_PROOF_INPUTS));
  assertProofSources(inputs, process.cwd()); // Fail before any process, socket or Vite launch.
  Object.assign(process.env, {
    ASTRID_CHECKOUT: inputs.agentCheckout, ASTRID_PYTHON: inputs.agentPython,
    ASTRID_RUNTIME_CHECKOUT: inputs.runtimeCheckout, ASTRID_RUNTIME_PYTHON: inputs.runtimePython,
    PYTHONDONTWRITEBYTECODE: '1',
    VITE_RUNTIME_ORIGIN: '', VITE_WORKSPACE_RUNTIME_EXPECTED_ACTOR_ID: '',
    VITE_WORKSPACE_RUNTIME_EXPECTED_REALM_ID: '', VITE_WORKSPACE_RUNTIME_EXPECTED_INSTANCE_ID: '',
  });
  const { DirectHarness, PRODUCT_ACTOR, rawRequest } = await import('../tests/e2e/local/support/harness.ts');
  const { AstridCli, revisionSet } = await import('../tests/e2e/local/support/astrid.ts');
  const harness = new DirectHarness();
  const directory = mkdtempSync(join(inputs.cacheRoot, 'proxy-real-runtime-'));
  const nativeFetch = globalThis.fetch;
  const originalWindow = Object.getOwnPropertyDescriptor(globalThis, 'window');
  const hosts = [], sessions = [], handles = [], browser = [], upstream = [];
  let vite, proxy;
  t.after(async () => {
    for (const session of sessions) await session.dispose();
    hosts.forEach(host => host.dispose());
    globalThis.fetch = nativeFetch;
    if (originalWindow) Object.defineProperty(globalThis, 'window', originalWindow); else delete globalThis.window;
    await vite?.close();
    if (proxy?.listening) await close(proxy);
    await harness.stop();
    rmSync(directory, { recursive: true, force: true });
  });
  await harness.start(); // Existing normal realm/project/media seed; no build or browser requested.
  const seed = await harness.seedThreeProducts();
  await harness.enableTimelineAuthoring(inputs.agentPython);
  const astrid = await AstridCli.create(harness);
  const identity = await astrid.preflight();
  const sources = revisionSet(identity);
  assert.equal(sources.astridHead, inputs.agentHead);
  assert.equal(sources.runtimeHead, inputs.runtimeHead);
  const base = `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}`;
  const history = async () => {
    const response = await harness.runtimeJson('GET', `${base}/commits?limit=50`);
    assert.equal(response.status, 200);
    return response.body;
  };
  const move = await astrid.commitCaptured(harness.seed.projectId, seed.timelineId, (await history()).head,
    { kind: 'move', clipId: seed.appClipId, on: 5 }, 'proxy-proof-native-capture');
  const scope = { actorId: PRODUCT_ACTOR, realmId: harness.realmId, projectId: harness.seed.projectId, timelineId: seed.timelineId };
  const discoveryPath = join(directory, 'discovery.json');
  const credential = join(directory, 'product.json');
  writeFileSync(credential, JSON.stringify({ version: 1, scope: 'astrid', actor_id: PRODUCT_ACTOR, token: harness.productToken }), { mode: 0o600 });
  writeFileSync(join(directory, 'catalog.json'), JSON.stringify({ selected_realm_id: harness.realmId,
    realms: [{ realm_id: harness.realmId, source_profile: 'astrid', data_root: harness.realmDir }] }));
  const selectRuntime = () => writeFileSync(discoveryPath, JSON.stringify({ endpoint: harness.runtimeUrl, credential_file: credential,
    active_realm: harness.realmId, runtime_instance_id: harness.runtimeInstanceId, realm_root: harness.realmDir }));
  selectRuntime();
  const appPort = await freePort();
  let proxyPort = await freePort();
  while (proxyPort === appPort) proxyPort = await freePort();
  const origin = `http://127.0.0.1:${appPort}`;
  proxy = createRuntimeProxyServer({ discoveryPath, allowedOrigin: origin, expectedHost: `127.0.0.1:${proxyPort}` });
  // Observe bytes at the real proxy ingress; do not replace its pinned dispatch or the Runtime.
  proxy.prependListener('request', req => {
    if (req.url !== `${O}/runtime${base}/commit`) return;
    const chunks = [];
    req.on('data', chunk => chunks.push(chunk));
    req.on('end', () => upstream.push({ body: Buffer.concat(chunks), key: req.headers['idempotency-key'], headers: { ...req.headers } }));
  });
  await listen(proxy, proxyPort);
  let loseNextCommit = true;
  const pageFetch = (input, init = {}) => {
    const url = new URL(String(input), origin);
    assert.equal(url.origin, origin);
    if (url.pathname.startsWith(O)) {
      assert.equal(init.cache, 'no-store'); assert.equal(init.credentials, 'omit');
      assert.equal(init.mode, 'same-origin'); assert.equal(init.redirect, 'error'); assert(init.signal);
    }
    const headers = new Headers(init.headers);
    assert.equal(headers.has('Authorization'), false);
    assert.equal(headers.has('Cookie'), false);
    headers.set('Origin', origin); headers.set('Sec-Fetch-Site', 'same-origin');
    const call = { path: url.pathname, headers: Object.fromEntries(headers), body: init.body ? Buffer.from(init.body).toString('utf8') : '' };
    browser.push(call);
    // Dispatch immediately. Fault injection affects only the answer AFTER real durable acceptance.
    return nativeFetch(url, { ...init, headers }).then(async response => {
      call.status = response.status;
      call.responseHeaders = Object.fromEntries(response.headers);
      call.response = await response.clone().text();
      if (url.pathname === O && init.method === 'POST' && response.status === 201) handles.push(JSON.parse(call.response).handle);
      if (url.pathname === `${O}/runtime${base}/commit` && loseNextCommit) {
        loseNextCommit = false;
        assert.equal(response.status, 200);
        assert.equal((await history()).head.publication_id, JSON.parse(call.response).receipt.receipt_id);
        throw new Error('Injected lost ACK after durable Runtime acceptance');
      }
      return response;
    });
  };
  // Only relative page requests use this adapter. Node harness/Agent control traffic stays server-side.
  globalThis.fetch = (input, init) => String(input).startsWith('/') ? pageFetch(input, init) : nativeFetch(input, init);
  Object.defineProperty(globalThis, 'window', { configurable: true, value: { location: { origin } } });
  const loadPage = async () => {
    vite = await createViteServer({ configFile: false, envDir: directory, root: process.cwd(),
      cacheDir: mkdtempSync(join(directory, 'vite-')), logLevel: 'silent', appType: 'custom',
      optimizeDeps: { noDiscovery: true, include: [] },
      resolve: { alias: { '@': resolve('src'), '@astrid/editor-sdk': resolve('src/sdk/index.ts'),
        '@banodoco/timeline-schema': existsSync(resolve('vendor/timeline-schema/typescript/dist/src/index.js'))
          ? resolve('vendor/timeline-schema/typescript/dist/src/index.js') : resolve('src/tools/video-editor/lib/timeline-schema.fallback.ts') } },
      plugins: [createRuntimeOperationAdmissionPlugin(origin)],
      server: { host: '127.0.0.1', port: appPort, strictPort: true, watch: null, hmr: false, proxy: {
        [O]: createRuntimeOperationProxyOptions(`http://127.0.0.1:${proxyPort}`),
        '/runtime-config/v1/workspace.json': { target: `http://127.0.0.1:${proxyPort}`, changeOrigin: true },
      } },
    });
    await vite.listen();
    const modules = {};
    for (const file of ['integrations/runtime/operationHost', 'integrations/runtime/dataProvider',
      'tools/video-editor/commands/commitOutbox', 'tools/video-editor/commands/commitSession',
      'tools/video-editor/commands/trackLabelGesture', 'tools/video-editor/lib/timeline-data']) {
      Object.assign(modules, await vite.ssrLoadModule(`/src/${file}.ts`));
    }
    return modules;
  };
  let page = await loadPage();
  let host = new page.RuntimeOperationHost(pageFetch); hosts.push(host);
  const operation = await host.bind();
  assert.deepEqual(await operation.getRecoverableIdentity(), { actorId: scope.actorId, realmId: scope.realmId });
  const decoded = page.decodeAcceptedTimelineCommit(move, scope.projectId, scope.timelineId);
  const initial = { head: decoded.accepted, canonicalDocument: decoded.canonicalDocument, graph: decoded.graph };
  const factory = createFakeIndexedDB(), held = new Set();
  const outboxes = page.createCommitOutbox({ indexedDB: factory, exclusiveLock: async (key, work) => {
    assert(!held.has(key), 'outbox is already claimed'); held.add(key);
    try { return await work(); } finally { held.delete(key); }
  } });
  const mount = async op => {
    const session = await page.createTimelineCommandSession({ scope, initial, outboxes,
      // Test adapter for the existing parsed sender: retrieve the ORIGINAL durable reservation, never reserialize it.
      send: async (request, key) => {
        const pending = (await outboxes.list(scope)).map(box => box.pending).find(item => item?.request.key === key);
        assert(pending); assert.deepEqual(JSON.parse(pending.request.body), request);
        return op.transmit(scope, pending.request);
      }, preview() {}, project: async () => {}, changed() {},
    });
    sessions.push(session); return session;
  };
  const session = await mount(operation);
  const before = await history();
  // A changed discovery endpoint/credential/identity cannot retarget this already-negotiated operation.
  const replacementCredential = join(directory, 'replacement.json');
  writeFileSync(replacementCredential, JSON.stringify({ version: 1, scope: 'astrid', actor_id: 'other-product', token: 'not-the-original-token' }));
  writeFileSync(discoveryPath, JSON.stringify({ endpoint: 'http://127.0.0.1:1', credential_file: replacementCredential,
    active_realm: harness.realmId, runtime_instance_id: 'other-instance', realm_root: harness.realmDir }));
  const payload = initial.canonicalDocument.parent_revision.payload;
  const current = await page.buildTimelineData({ ...payload.config, clips: payload.clips }, payload.registry, undefined, 1, undefined,
    { projectId: scope.projectId, timelineId: scope.timelineId, headRevisionId: initial.head.revisionId, headPublicationId: initial.head.publicationId });
  page.submitTrackLabelEdit(page.captureTrackLabelEdit(session.trackLabelPort, current, 'V1'), { values: { label: 'Proxy café 🎞' }, clear: [] });
  await assert.rejects(session.flush(), /lost ACK|not acknowledged/);
  assert.equal(session.getState().status, 'retry');
  const [saved] = await outboxes.list(scope);
  assert(saved.pending); assert.equal(saved.intents.length, 1);
  const accepted = JSON.parse(browser.find(call => call.path === `${O}/runtime${base}/commit`).response);
  assert.equal(accepted.data.publisher, scope.actorId);
  assert.equal(accepted.receipt.idempotency_key, saved.pending.request.key);
  const canonical = accepted.data.canonical_document;
  assert.equal(canonical.parent_revision.payload.config.tracks.find(track => track.id === 'V1').label, 'Proxy café 🎞');
  assert.equal(canonical.parent_revision.payload.clips.find(clip => clip.id === seed.appClipId).at, 5);
  assert.deepEqual(canonical.parent_revision.payload.config.x_f2_opaque, seed.opaque.config);
  assert.deepEqual(canonical.shot_revisions, initial.canonicalDocument.shot_revisions);
  assert.deepEqual(canonical.internal_timeline_revisions, initial.canonicalDocument.internal_timeline_revisions);
  assert.equal((await history()).items.length, before.items.length + 1);
  assert.equal(operation.isCurrentIdentity(scope), false); // Lost answer retires the local owner.
  const count = browser.length;
  await assert.rejects(operation.transmit(scope, saved.pending.request));
  assert.equal(browser.length, count);
  await session.dispose();
  selectRuntime();
  // App scope/retirement fences refuse before dispatch; storage lookup is scoped independently.
  for (const field of ['actorId', 'realmId', 'projectId', 'timelineId']) {
    const wrong = { ...scope, [field]: 'wrong' };
    assert.deepEqual(await outboxes.list(wrong), []);
    const op = await host.reconnect(), sent = browser.length;
    await assert.rejects(op.transmit(wrong, saved.pending.request));
    assert.equal(browser.slice(sent).filter(call => call.path !== O).length, 0);
  }
  const stale = await host.reconnect();
  const staleHandle = handles.at(-1);
  const oldInstance = harness.runtimeInstanceId;
  await harness.restartRuntime();
  assert.notEqual(harness.runtimeInstanceId, oldInstance);
  selectRuntime();
  await assert.rejects(stale.transmit(scope, saved.pending.request));
  await assert.rejects(host.reconnect()); // Old page launch identity cannot silently follow the restart.
  host.dispose();
  const retired = await rawRequest({ port: appPort, path: `${O}/runtime/v1/health`, headers: { Origin: origin, [H]: staleHandle } });
  assert.equal(retired.status, 410);
  assert.deepEqual((await outboxes.list(scope))[0].pending.request, saved.pending.request);
  await vite.close(); vite = undefined;
  const relaunchAt = browser.length;
  page = await loadPage(); // Fresh module lifetime models page relaunch; fake IDB remains in this Node process.
  host = new page.RuntimeOperationHost(pageFetch); hosts.push(host);
  const recoveredOperation = await host.bind();
  assert.deepEqual(await recoveredOperation.getRecoverableIdentity(), { actorId: scope.actorId, realmId: scope.realmId });
  const negotiation = browser.slice(relaunchAt);
  assert(negotiation.some(call => call.path === `${O}/runtime/v1/health`
    && JSON.parse(call.response).runtime_instance_id === harness.runtimeInstanceId));
  assert(negotiation.some(call => call.path === `${O}/runtime/v1/handshake`
    && JSON.parse(call.response).actor_id === scope.actorId && JSON.parse(call.response).realm_id === scope.realmId));
  assert(negotiation.some(call => call.path === `${O}/runtime/v1/realm`
    && JSON.parse(call.response).realm_id === scope.realmId));
  const reopened = await mount(recoveredOperation);
  assert.deepEqual(reopened.getState().recoverableOwners, [saved.ownerId]);
  assert.equal(upstream.length, 1, 'no implicit retry during reconnect/relaunch');
  await reopened.recover(saved.ownerId);
  assert.equal(reopened.getState().status, 'saved');
  const [drained] = await outboxes.list(scope);
  assert.equal(drained.pending, undefined); assert.equal(drained.intents.length, 0);
  assert.deepEqual(drained.accepted.value.response, accepted);
  assert.equal(upstream.length, 2);
  for (const post of upstream) {
    assert.deepEqual(post.body, Buffer.from(saved.pending.request.body, 'utf8'));
    assert.equal(post.key, saved.pending.request.key);
    for (const key of ['authorization', 'cookie', 'proxy-authorization', 'x-first', 'x-second']) assert.equal(post.headers[key], undefined);
  }
  assert.deepEqual((await history()).head, { revision_id: accepted.data.accepted_revision_id, publication_id: accepted.receipt.receipt_id });
  assert.equal((await history()).items.length, before.items.length + 1, 'exact replay creates no second publication');
  const commits = browser.filter(call => call.path === `${O}/runtime${base}/commit`);
  assert.deepEqual(commits.map(call => JSON.parse(call.response)), [accepted, accepted]);
  const tokenFromFile = file => {
    const text = readFileSync(file, 'utf8').trim();
    try { const value = JSON.parse(text); return typeof value.token === 'string' ? value.token : text; } catch { return text; }
  };
  const secrets = [harness.productToken, astrid.secret,
    tokenFromFile(join(harness.supportDir, 'credentials/owner.token')),
    tokenFromFile(harness.discovery().worker_credential_file)];
  for (const call of browser) {
    for (const secret of secrets) assert(!JSON.stringify(call).includes(secret), 'server credential leaked into page traffic');
    if (call.responseHeaders) for (const key of ['authorization', 'proxy-authorization', 'cookie', 'set-cookie', H.toLowerCase()]) assert.equal(call.responseHeaders[key], undefined);
    for (const handle of handles) assert(!call.path.includes(handle) && !call.body.includes(handle), 'handle leaked into URL/body');
    if (call.headers[H.toLowerCase()]) assert(call.path === O || call.path.startsWith(`${O}/runtime/`));
  }
  for (const secret of [...secrets, ...handles]) assert(!JSON.stringify([saved, drained]).includes(secret), 'private value persisted in outbox');
  assert(browser.every(call => !call.path.startsWith('/api/runtime')), 'no legacy/fallback dispatch');
  assert.deepEqual(revisionSet(identity), sources);
  assertProofSources(inputs, process.cwd());
});
