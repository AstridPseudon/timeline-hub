// Review controls only: apply the proposal in memory; never import the e2e runner.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';
import test from 'node:test';
import ts from 'typescript';
import { classifyGate5FaultOrder, sameGate5CommitIdentity } from './tests/e2e/local/support/gate5-fault-order.ts';

const root = path.dirname(fileURLToPath(import.meta.url));
const filename = path.join(root, 'tests/e2e/local/three-products.spec.ts');
const before = readFileSync(filename, 'utf8');
const patch = readFileSync(path.join(root, 'proposed-v3.patch'), 'utf8');
function applyInMemory(source, diff) {
  const lines = source.split(/(?<=\n)/);
  const result = [];
  let cursor = 0;
  for (const hunk of diff.split(/^@@ /m).slice(1)) {
    const [header, ...body] = hunk.split('\n');
    const start = Number(header.match(/^-(\d+)/)[1]) - 1;
    result.push(...lines.slice(cursor, start));
    cursor = start;
    for (const line of body.slice(0, -1)) {
      if (line.startsWith('+')) result.push(`${line.slice(1)}\n`);
      else if (line.startsWith('-')) assert.equal(lines[cursor++], `${line.slice(1)}\n`);
      else {
        const context = line.startsWith(' ') ? line.slice(1) : line;
        assert.equal(lines[cursor], `${context}\n`);
        result.push(lines[cursor++]);
      }
    }
  }
  return result.join('') + lines.slice(cursor).join('');
}
const after = applyInMemory(before, patch);
const between = (source, start, end) => source.slice(source.indexOf(start), source.indexOf(end, source.indexOf(start)));
const helper = (source) => between(source, 'async function faultFirstCommit(', '\nfunction accepted(');
const restart = (source) => between(source, '  const originalARequest =', "  const b = accepted(wire.posts[2]);");
const p3 = (source) => between(source, "test('M2 real gate 5 (M1 real mounted path):", "test('M2 ordinary extension batch:");
const reset = (source) => p3(source).slice(0, p3(source).indexOf('  const { wire, before, a, owner }'));
const downstream = (source) => p3(source).slice(p3(source).indexOf('  const b = accepted(wire.posts[2]);'));
const sha = (value) => createHash('sha256').update(value).digest('hex');

if (process.argv.includes('--hashes')) {
  for (const [name, pick] of [['full', (s) => s], ['faultFirstCommit', helper], ['restart', restart], ['P3-full', p3],
    ['reset', reset], ['downstream', downstream], ['mounted-D53-helper', (s) => between(s,
      'async function prepareAfterAckLossMountedDocuments(', '\nasync function expectAgentRevision(')],
    ['canonical-history-undo-tail', (s) => p3(s).slice(p3(s).indexOf('  expect(b.data.canonical_document.parent_revision.payload.config)'))]]) {
    console.log(`${name} before=${sha(pick(before))} virtual-after=${sha(pick(after))}`);
  }
  console.log(`patch=${sha(patch)} bytes=${Buffer.byteLength(patch)} source-delta=${Buffer.byteLength(after) - Buffer.byteLength(before)}`);
} else if (process.argv.includes('--lint')) {
  const { ESLint } = await import('eslint');
  const results = await new ESLint({ cwd: root, cache: false }).lintText(after, { filePath: filename });
  const diagnostics = results.flatMap((r) => r.messages);
  console.log(JSON.stringify(diagnostics, null, 2));
  assert.equal(diagnostics.length, 0);
} else if (process.argv.includes('--types')) {
  const configPath = ts.findConfigFile(root, ts.sys.fileExists, 'tsconfig.json');
  const config = ts.readConfigFile(configPath, ts.sys.readFile);
  const parsed = ts.parseJsonConfigFileContent(config.config, ts.sys, root);
  let current = before;
  let version = 0;
  const host = {
    ...ts.sys, getCompilationSettings: () => parsed.options, getScriptFileNames: () => [...new Set([...parsed.fileNames, filename])],
    getScriptVersion: (name) => name === filename ? String(version) : '0',
    getScriptSnapshot: (name) => {
      const text = name === filename ? current : ts.sys.readFile(name);
      return text === undefined ? undefined : ts.ScriptSnapshot.fromString(text);
    },
    getCurrentDirectory: () => root, getDefaultLibFileName: ts.getDefaultLibFilePath,
    useCaseSensitiveFileNames: () => ts.sys.useCaseSensitiveFileNames,
  };
  const service = ts.createLanguageService(host);
  const diagnostics = () => [...service.getSyntacticDiagnostics(filename), ...service.getSemanticDiagnostics(filename)]
    .map((d) => `${d.code}:${ts.flattenDiagnosticMessageText(d.messageText, '\n')}`);
  const baseline = diagnostics();
  current = after;
  version++;
  const virtual = diagnostics();
  const remaining = [...baseline];
  const added = virtual.filter((message) => {
    const index = remaining.indexOf(message);
    if (index < 0) return true;
    remaining.splice(index, 1);
    return false;
  });
  console.log(JSON.stringify({ baseline: baseline.length, virtual: virtual.length, added }, null, 2));
  assert.deepEqual(added, []);
  service.dispose();
} else {
  // Execute the proposed helper itself. Route doubles model callback ordering only;
  // their opaque marker is never a Runtime accepted/merged reply or gate evidence.
  const compile = ts.transpileModule(`${helper(after)}\nglobalThis.fault = faultFirstCommit;`, {
    compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.None },
  }).outputText;
  const door = 'http://127.0.0.1:17340';
  const url = `${door}/api/runtime/v1/projects/project/timelines/timeline/commit`;
  const A = { key: 'key-a', body: '{"commands":["A"]}' };
  const B = { key: 'key-b', body: '{"commands":["B"]}' };
  const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
  async function environment() {
    const events = [];
    let instance = 'old';
    const sandbox = { classifyGate5FaultOrder, sameGate5CommitIdentity, URL, setTimeout, clearTimeout,
      CEILING: { timeout: 500 }, SAVES: /composition-revisions$/, COMMITS: /\/commit$/ };
    vm.runInNewContext(compile, sandbox);
    const page = (name) => ({
      name, closed: false, listeners: new Map(),
      on(event, callback) { this.listeners.set(event, callback); },
      once(event, callback) { this.on(event, callback); },
      async route(_pattern, intercept) { this.intercept = intercept; },
      isClosed() { return this.closed; },
      async close() { this.closed = true; this.listeners.get('close')?.(); await delay(0); },
    });
    const original = page('original');
    const wire = await sandbox.fault(original);
    const send = async (identity, target, destination = url) => {
      const request = { method: () => 'POST', url: () => destination,
        postData: () => identity.body, headers: () => ({ 'idempotency-key': identity.key }) };
      const route = { state: 'open', request: () => request,
        async fetch(options) {
          assert.equal(this.state, 'open');
          assert.deepEqual(Object.keys(options), ['maxRetries']);
          assert.equal(options.maxRetries, 0);
          this.state = 'fetched';
          events.push({ key: identity.key, instance, destination });
          return { status: () => 200, json: async () => ({ controlMarker: true }) };
        },
        async fulfill() { assert.equal(this.state, 'fetched'); this.state = 'fulfilled'; },
        async abort() { this.state = 'aborted'; },
      };
      await target.intercept(route);
      return route;
    };
    await send(A, original);
    const losing = wire.loseAck();
    await send(A, original);
    await losing;
    assert.equal(wire.observed.length, 2);
    assert.equal(wire.forwarded.length, 1);
    return { wire, page, original, send, events, restart() { instance = 'new'; } };
  }
  const beforeRelease = (wire) => {
    assert.equal(wire.observed.length, 3);
    assert.ok(wire.observed.every((identity) => sameGate5CommitIdentity(identity, A)));
    assert.equal(wire.forwarded.length, 1);
    assert.equal(wire.observedUrls[2], wire.observedUrls[0]);
    assert.equal(new URL(wire.observedUrls[2]).origin, door);
  };
  async function reopen(env) {
    await env.original.close();
    env.restart();
    const reopened = env.page('reopened');
    await env.wire.attach(reopened);
    env.wire.armRecoveryRetry();
    return reopened;
  }
  // Run the virtual journey's entire restart block as well as its helper. These
  // controls expose assumptions about callback order; no live gate is run here.
  async function journeySchedule({ reloadRetry = false, mismatch = {}, callbackDelay = 0, doorInstance = 'new' } = {}) {
    const env = await environment();
    const owner = { ownerId: 'owner', pending: { request: A }, intents: ['A', 'B'] };
    const realmBefore = { realmId: 'realm', runtimeInstanceId: 'old', schemaDigest: 'schema', astridFile: 'discovery' };
    const harness = { runtimePort: 49500, runtimeUrl: 'http://127.0.0.1:49500', runtimeInstanceId: 'old', realmId: 'realm',
      doorBase: `${door}/api/runtime`, origin: 'https://app.example',
      async restartRuntime() {
        env.restart();
        this.runtimePort = 49501;
        this.runtimeUrl = 'http://127.0.0.1:49501';
        this.runtimeInstanceId = 'new';
        return { oldPort: 49500, oldInstanceId: 'old' };
      },
      discovery() { return { endpoint: this.runtimeUrl, runtime_instance_id: this.runtimeInstanceId,
        active_realm: this.realmId, door_endpoint: door, door_origin: this.origin, ...mismatch }; },
    };
    const normalize = (value) => JSON.parse(JSON.stringify(value));
    const expectation = (value) => ({
      toBe: (expected) => assert.equal(value, expected),
      toEqual: (expected) => assert.deepEqual(normalize(value), normalize(expected)),
      toHaveLength: (expected) => assert.equal(value.length, expected),
      toMatchObject: (expected) => {
        for (const key of Object.keys(expected)) assert.deepEqual(normalize(value[key]), normalize(expected[key]));
      },
      not: { toBe: (expected) => assert.notEqual(value, expected) },
    });
    expectation.poll = (callback) => ({ toBe: async (expected) => expectation(await callback()).toBe(expected) });
    env.original.reload = async () => {
      await env.wire.abortStagedRetry();
      if (reloadRetry) await env.send(A, env.original);
    };
    const execution = { URL, sameGate5CommitIdentity, expect: expectation, page: env.original, wire: env.wire, harness, realmBefore, owner,
      seed3: { timelineId: 'timeline' }, astrid: {}, sniff: { attach() {} }, recordedA: 'history-A',
      context: { newPage: async () => env.page('reopened') }, CEILING: { timeout: 500 },
      commandOutboxes: async () => [owner], expectConnected: async () => {}, openSeededTimeline: async () => {},
      async openApp(reopened) { await delay(callbackDelay); await env.send(A, reopened); },
      expectSameRealm: async () => ({ ...realmBefore, runtimeInstanceId: doorInstance }),
      expectV2History: async () => 'history-A',
    };
    // B starts only after the release settles the route; retain the actual helper.
    const release = env.wire.releaseStagedRetry;
    env.wire.releaseStagedRetry = async () => { await release(); await env.send(B, execution.reopened); };
    const createPage = execution.context.newPage;
    execution.context.newPage = async () => { execution.reopened = await createPage(); return execution.reopened; };
    const code = ts.transpileModule(`async function run() { ${restart(after)} }\nrun();`, {
      compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.None },
    }).outputText;
    await vm.runInNewContext(code, execution);
    return env;
  }
  for (const [name, callbackDelay] of [['fast', 0], ['slow', 7]]) {
    test(`${name}: stable door request held after restart, then A and B`, async () => {
      const env = await environment();
      const reopened = await reopen(env);
      await delay(callbackDelay);
      await env.send(A, reopened);
      beforeRelease(env.wire);
      await env.wire.releaseStagedRetry();
      await env.send(B, reopened);
      assert.equal(env.wire.observed.length, 4);
      assert.equal(env.wire.forwarded.length, 3);
      assert.deepEqual(env.events.map((event) => event.instance), ['old', 'new', 'new']);
      assert.ok(env.events.every((event) => event.destination === url));
    });
  }
  for (const [name, identity] of [['wrong body', { ...A, body: B.body }], ['wrong key', { ...A, key: B.key }], ['B before A', B]]) {
    test(`${name}: remains observed and is refused`, async () => {
      const env = await environment();
      const reopened = await reopen(env);
      await assert.rejects(env.send(identity, reopened), /early dependent or mismatching/);
      assert.equal(env.wire.observed.length, 3);
      assert.equal(env.wire.forwarded.length, 1);
    });
  }
  test('duplicate while held and duplicate after release are refused', async () => {
    const env = await environment();
    const reopened = await reopen(env);
    await env.send(A, reopened);
    await assert.rejects(env.send(A, reopened), /already has a staged automatic retry/);
    assert.equal(env.wire.forwarded.length, 1);
    await env.wire.releaseStagedRetry();
    await assert.rejects(env.send(A, reopened), /unexpected duplicate exact/);
    assert.equal(env.wire.forwarded.length, 2);
  });
  test('dynamic daemon origin cannot replace the stable browser door', async () => {
    const env = await environment();
    const reopened = await reopen(env);
    await env.send(A, reopened, url.replace(door, 'http://127.0.0.1:49501'));
    assert.throws(() => beforeRelease(env.wire), assert.AssertionError);
    assert.equal(env.wire.forwarded.length, 1);
  });
  for (const [name, callbackDelay] of [['fast', 0], ['slow', 7]]) {
    test(`${name}: actual virtual restart block passes only when intermediate recovery has not sent`, async () => {
      const env = await journeySchedule({ callbackDelay });
      assert.deepEqual(env.events.map((event) => event.instance), ['old', 'new', 'new']);
      assert.equal(env.wire.observed.length, 4);
    });
  }
  for (const [name, mismatch] of [['stale endpoint', { endpoint: 'http://127.0.0.1:49500' }],
    ['stale instance', { runtime_instance_id: 'old' }], ['wrong realm', { active_realm: 'other' }],
    ['wrong door', { door_endpoint: 'http://127.0.0.1:17341' }]]) {
    test(`${name}: actual virtual discovery assertion refuses misrouting`, async () => {
      await assert.rejects(journeySchedule({ mismatch }), assert.AssertionError);
    });
  }
  test('door health on the old instance fails even with the new discovery endpoint', async () => {
    await assert.rejects(journeySchedule({ doorInstance: 'old' }), assert.AssertionError);
  });
  test('FAST RELOAD COUNTEREXAMPLE: actual virtual restart block fails when the intermediate mount sends A', async () => {
    await assert.rejects(journeySchedule({ reloadRetry: true }), assert.AssertionError);
  });
  test('arming the intermediate reload instead still adds an attempt and breaks strict D75 counts', async () => {
    const env = await environment();
    await env.wire.abortStagedRetry();
    env.wire.armRecoveryRetry();
    await env.send(A, env.original);
    assert.equal(env.wire.observed.length, 3);
    const reopened = await reopen(env);
    await env.send(A, reopened);
    assert.equal(env.wire.observed.length, 4);
    assert.equal(env.wire.forwarded.length, 1);
    assert.throws(() => beforeRelease(env.wire), assert.AssertionError);
  });
  test('retains all original waits except the explicitly replaced fixture recovery click', () => {
    const removed = patch.split('\n').filter((line) => line.startsWith('-') && !line.startsWith('---')).join('\n');
    assert.equal(removed, '-  await reopened.getByRole(\'button\', { name: /^Recover saved edits/ })\n-    .and(reopened.locator(`[data-owner-id="${owner.ownerId}"]`)).click();');
    assert.ok(after.includes('await page.reload();\n  await expectConnected(page);'));
    assert.ok(after.includes('const restarted = await harness.restartRuntime();'));
  });
}
