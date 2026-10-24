// Review-only lifecycle control; this does not run a browser or a Runtime.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import ts from 'typescript';

const source = readFileSync(new URL('./tests/e2e/local/three-products.spec.ts', import.meta.url), 'utf8');
const patch = readFileSync(new URL('./A2-P3-recovery-review.patch', import.meta.url), 'utf8');
const anchor = "  expect(wire.posts, 'reload does not send queued B or retry A').toHaveLength(1);\n";
const barrier = '  await expect.poll(() => wire.observed.length, CEILING).toBe(3);\n';
const proposed = source.replace(anchor, anchor + barrier);
const sha = (value) => createHash('sha256').update(value).digest('hex');

function intermediateBlock(text) {
  const gate = text.indexOf("test('M2 real gate 5 (M1 real mounted path):");
  const from = text.indexOf('  await page.reload();', gate);
  const to = text.indexOf('  await page.close();', from) + '  await page.close();'.length;
  assert.ok(gate >= 0 && from > gate && to > from);
  return text.slice(from, to);
}

// Execute the actual protected intermediate block, with only the browser and
// assertion ports substituted. Retained 26908 has connection/outbox-read/close
// at 124359.152/126596.881/126884.134 ms, no intermediate POST, and the reopened
// POST at 146344.511 ms. Connection and persisted bytes do not prove a mount.
async function runIntermediate(text, retryAvailable) {
  const a = { body: '{"commands":["A"]}', key: 'local-control-a' };
  const owner = { ownerId: 'owner', pending: { request: a }, intents: [{ id: 'A' }, { id: 'B', basis: { after: 'A' } }] };
  const wire = { posts: [a], observed: [a, a], async abortStagedRetry() {} };
  let closed = false;
  let polls = 0;
  let ceiling;
  const expect = (actual) => ({
    toEqual: (expected) => assert.deepEqual(actual, expected),
    toHaveLength: (length) => assert.equal(actual.length, length),
  });
  expect.poll = (read, options) => ({ async toBe(expected) {
    ceiling = options;
    polls++;
    if (retryAvailable) {
      // Admission can follow the shell's connection and IndexedDB read.
      await Promise.resolve();
      if (!closed) wire.observed.push(a);
    }
    assert.equal(read(), expected, 'intermediate retry must be observed before close');
  } });
  const CEILING = { timeout: 90_000 };
  const block = ts.transpileModule(intermediateBlock(text), {
    compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.ESNext },
  }).outputText;
  const execute = new (Object.getPrototypeOf(async function () {}).constructor)(
    'page', 'expectConnected', 'commandOutboxes', 'seed3', 'owner', 'wire', 'expect', 'CEILING', block);
  let error;
  try {
    await execute({ async reload() {}, async close() { closed = true; } }, async () => {},
      async () => [structuredClone(owner)], { timelineId: 'timeline' }, owner, wire, expect, CEILING);
  } catch (caught) { error = caught; }
  return { closed, polls, ceiling, CEILING, wire, a, error };
}

test('review patch adds only the intermediate observation barrier to the exact protected source', () => {
  assert.equal(sha(source), '8661fc919714d292c567844dc4f423855923077ca6a679a1398ec2a46154315b');
  assert.equal(sha(proposed), '736fd38108283b9c8b5faac47adff4a9c1abd087cb326184a6bfec480e491e05');
  assert.equal(patch, '--- a/tests/e2e/local/three-products.spec.ts\n+++ b/tests/e2e/local/three-products.spec.ts\n@@ -1749,0 +1750 @@\n+' + barrier);
  assert.equal(proposed.replace(anchor + barrier, anchor), source);
});

test('retained missing-intermediate schedule: old block closes; proposal refuses to advance', async () => {
  const old = await runIntermediate(source, false);
  assert.equal(old.error, undefined);
  assert.equal(old.closed, true);
  assert.equal(old.wire.observed.length, 2);
  const candidate = await runIntermediate(proposed, false);
  assert.match(candidate.error.message, /intermediate retry must be observed before close/);
  assert.equal(candidate.closed, false);
  assert.equal(candidate.polls, 1);
  assert.equal(candidate.ceiling, candidate.CEILING);
  assert.equal(candidate.ceiling.timeout, 90_000);
});

test('delayed mount schedule: proposal observes exact third A before closing without forwarding it', async () => {
  const old = await runIntermediate(source, true);
  assert.equal(old.closed, true);
  assert.equal(old.wire.observed.length, 2);
  const candidate = await runIntermediate(proposed, true);
  assert.equal(candidate.error, undefined);
  assert.equal(candidate.closed, true);
  assert.deepEqual(candidate.wire.observed, [candidate.a, candidate.a, candidate.a]);
  assert.deepEqual(candidate.wire.posts, [candidate.a]);
});

test('selected intermediate block cannot close without observing its recovery request', async () => {
  const selected = process.env.A2_P3_REVIEW_SOURCE ?? 'proposed';
  assert.ok(['original', 'proposed'].includes(selected));
  const result = await runIntermediate(selected === 'original' ? source : proposed, false);
  assert.equal(result.closed, false, 'a connected shell and durable bytes cannot authorize closing the recovery mount');
  assert.equal(result.polls, 1);
});
