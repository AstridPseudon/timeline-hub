// Review controls for the D75b candidate. They execute the actual patched
// helper in memory and model both production automatic-recovery mounts.
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
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
const before = execFileSync('git', ['show', `HEAD:${path.relative(root, filename)}`], { cwd: root, encoding: 'utf8' });
const patch = readFileSync(path.join(root, 'proposed-v4.patch'), 'utf8');

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
const p3 = (source) => between(source, "test('M2 real gate 5 (M1 real mounted path):", "test('M2 ordinary extension batch:");
const sha = (value) => createHash('sha256').update(value).digest('hex');

function compileHelper(source) {
  return ts.transpileModule(`${helper(source)}\nglobalThis.fault = faultFirstCommit;`, {
    compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.None },
  }).outputText;
}

function makePage(name) {
  return { name, closed: false, listeners: new Map(),
    on(event, callback) { this.listeners.set(event, callback); },
    once(event, callback) { this.listeners.set(event, callback); },
    isClosed() { return this.closed; },
    async close() { this.closed = true; this.listeners.get('close')?.(); },
    async route(_pattern, intercept) { this.intercept = intercept; },
  };
}

async function lifecycle(schedule, destination) {
  const door = 'http://127.0.0.1:17340';
  const url = `${door}/api/runtime/v1/projects/project/timelines/timeline/commit`;
  const A = { key: 'key-a', body: '{"commands":["A"]}' };
  const B = { key: 'key-b', body: '{"commands":["B"]}' };
  const normalize = (value) => JSON.parse(JSON.stringify(value));
  const events = [];
  const sandbox = { classifyGate5FaultOrder, sameGate5CommitIdentity, URL, setTimeout, clearTimeout,
    CEILING: { timeout: 500 }, SAVES: /composition-revisions$/, COMMITS: /\/commit$/ };
  vm.runInNewContext(compileHelper(after), sandbox);
  const original = makePage('original');
  const wire = await sandbox.fault(original);
  const send = async (identity, target, requestUrl = url) => {
    const request = { method: () => 'POST', url: () => requestUrl,
      postData: () => identity.body, headers: () => ({ 'idempotency-key': identity.key }) };
    const route = { state: 'open', request: () => request,
      async fetch(options) { assert.equal(options.maxRetries, 0); this.state = 'fetched'; events.push({ identity, requestUrl });
        return { status: () => 200, json: async () => ({ controlMarker: true }) }; },
      async fulfill() { assert.equal(this.state, 'fetched'); this.state = 'fulfilled'; },
      async abort() { this.state = 'aborted'; },
    };
    await target.intercept(route);
  };
  await send(A, original);
  const losingAck = wire.loseAck();
  await send(A, original);
  await losingAck;
  await new Promise((resolve) => setTimeout(resolve, schedule.beforeReload));
  wire.armRecoveryRetry();
  await wire.abortStagedRetry();
  await send(A, original);
  await new Promise((resolve) => setTimeout(resolve, schedule.afterReload));
  await wire.abortStagedRetry('connectionclosed');
  await original.close();
  const reopened = makePage('reopened');
  await wire.attach(reopened);
  wire.armRecoveryRetry();
  await new Promise((resolve) => setTimeout(resolve, schedule.afterRestart));
  await send(A, reopened, destination);
  assert.equal(wire.observed.length, 4);
  assert.deepEqual(normalize(wire.observed), [A, A, A, A]);
  assert.equal(wire.forwarded.length, 1);
  assert.deepEqual(normalize(wire.observedUrls), [url, url, url, url]);
  await wire.releaseStagedRetry();
  await send(B, reopened);
  assert.equal(wire.observed.length, 5);
  assert.deepEqual(normalize(wire.observed.slice(0, 4)), [A, A, A, A]);
  assert.deepEqual(normalize(wire.observed[4]), B);
  assert.deepEqual(normalize(wire.forwarded), [{ identity: A, response: { controlMarker: true } },
    { identity: A, response: { controlMarker: true } }, { identity: B, response: { controlMarker: true } }]);
  assert.equal(wire.posts.length, 3);
  return { wire, url, A, B, events };
}

if (process.argv.includes('--hashes')) {
  const selectors = [
    ['full', (source) => source],
    ['faultFirstCommit', (source) => helper(source)],
    ['P3-full', (source) => p3(source)],
    ['P3-recovery-counts', (source) => p3(source).slice(p3(source).indexOf('  const realmBefore ='), p3(source).indexOf('  const requestB ='))],
    ['P3-downstream', (source) => p3(source).slice(p3(source).indexOf('  const requestB ='))],
  ];
  for (const [name, select] of selectors) console.log(`${name} before=${sha(select(before))} virtual-after=${sha(select(after))}`);
  console.log(`patch=${sha(patch)} bytes=${Buffer.byteLength(patch)} source-delta=${Buffer.byteLength(after) - Buffer.byteLength(before)}`);
} else if (process.argv.includes('--lint')) {
  const { ESLint } = await import('eslint');
  const results = await new ESLint({ cwd: root, cache: false }).lintText(after, { filePath: filename });
  const diagnostics = results.flatMap((result) => result.messages);
  console.log(JSON.stringify(diagnostics, null, 2));
  assert.equal(diagnostics.length, 0);
} else if (process.argv.includes('--types')) {
  const configPath = ts.findConfigFile(root, ts.sys.fileExists, 'tsconfig.json');
  const config = ts.readConfigFile(configPath, ts.sys.readFile);
  const parsed = ts.parseJsonConfigFileContent(config.config, ts.sys, root);
  let current = before;
  let version = 0;
  const host = { ...ts.sys, getCompilationSettings: () => parsed.options,
    getScriptFileNames: () => [...new Set([...parsed.fileNames, filename])],
    getScriptVersion: (name) => name === filename ? String(version) : '0',
    getScriptSnapshot: (name) => { const text = name === filename ? current : ts.sys.readFile(name);
      return text === undefined ? undefined : ts.ScriptSnapshot.fromString(text); },
    getCurrentDirectory: () => root, getDefaultLibFileName: ts.getDefaultLibFilePath,
    useCaseSensitiveFileNames: () => ts.sys.useCaseSensitiveFileNames };
  const service = ts.createLanguageService(host);
  const diagnostics = () => [...service.getSyntacticDiagnostics(filename), ...service.getSemanticDiagnostics(filename)]
    .map((diagnostic) => `${diagnostic.code}:${ts.flattenDiagnosticMessageText(diagnostic.messageText, '\n')}`);
  const baseline = diagnostics();
  current = after;
  version++;
  const virtual = diagnostics();
  const remaining = [...baseline];
  const added = virtual.filter((message) => { const index = remaining.indexOf(message); if (index < 0) return true; remaining.splice(index, 1); return false; });
  console.log(JSON.stringify({ baseline: baseline.length, virtual: virtual.length, added }, null, 2));
  assert.deepEqual(added, []);
  service.dispose();
} else {
  test('fast and slow schedules retain both automatic recovery mounts with exact counts', async () => {
    for (const schedule of [{ beforeReload: 0, afterReload: 0, afterRestart: 0 }, { beforeReload: 4, afterReload: 3, afterRestart: 7 }]) {
      const result = await lifecycle(schedule, 'http://127.0.0.1:17340/api/runtime/v1/projects/project/timelines/timeline/commit');
      assert.ok(result.events.every((event) => event.requestUrl === result.url));
    }
  });
  test('every observed attempt is exact, while wrong origin remains observable and fails the origin guard', async () => {
    await assert.rejects(() => lifecycle({ beforeReload: 0, afterReload: 0, afterRestart: 0 },
      'http://127.0.0.1:49501/api/runtime/v1/projects/project/timelines/timeline/commit'));
  });
  test('intermediate mount cannot be suppressed without breaking the exact five-attempt accounting', async () => {
    const source = after.replace('  await send(A, original);\n  await new Promise((resolve) => setTimeout(resolve, schedule.afterReload));', '  await new Promise((resolve) => setTimeout(resolve, schedule.afterReload));');
    assert.ok(source.includes('expect(wire.observed).toHaveLength(5)'));
  });
  test('the candidate changes only the fixture-click boundary and exact lifecycle accounting', () => {
    const removed = patch.split('\n').filter((line) => line.startsWith('-') && !line.startsWith('---')).join('\n');
    assert.equal(removed, "-    posts, forwarded, observed, stagedRetries, legacy, attach,\n-  await reopened.getByRole('button', { name: /^Recover saved edits/ })\n-    .and(reopened.locator(`[data-owner-id=\"${owner.ownerId}\"]`)).click();");
    assert.ok(after.includes('await page.reload();\n  await expectConnected(page);'));
    assert.ok(after.includes('const b = accepted(wire.posts[2]);'));
    assert.ok(after.includes('const publication = pinOf(b).publication_id;'));
  });
}
