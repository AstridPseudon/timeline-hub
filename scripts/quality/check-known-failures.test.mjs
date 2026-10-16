#!/usr/bin/env node

import { after, describe, it } from 'node:test';
import { strict as assert } from 'node:assert';
import { spawnSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { checkKnownFailures, FILE_BUDGETS, MAX_SRC_ENTRIES } from './check-known-failures.mjs';

const moduleDir = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(moduleDir, '..', '..');
const gateScript = resolve(moduleDir, 'check-known-failures.mjs');
const JOURNEY = 'tests/e2e/local/direct-journey.spec.ts';
const TODAY = '2026-10-16';

const tempRoots = [];
after(() => {
  for (const root of tempRoots) rmSync(root, { recursive: true, force: true });
});

function makeRepo(files) {
  const root = mkdtempSync(join(os.tmpdir(), 'known-failures-'));
  tempRoots.push(root);
  for (const [rel, content] of Object.entries(files)) {
    const abs = join(root, rel);
    mkdirSync(dirname(abs), { recursive: true });
    writeFileSync(abs, content, 'utf8');
  }
  return root;
}

const comment = (expires = '2026-10-30', reason = 'fixture') =>
  `// known-failure: reigh-app | ${expires} | ${reason}`;

const specWith = (markers, { expires, reason } = {}) => {
  const body = Array.from({ length: markers }, (_, i) =>
    `${comment(expires, reason)}\ntest.fail('case ${i}', async () => {});`,
  );
  return ['import { test } from "@playwright/test";', ...body, ''].join('\n');
};

const run = (root, budgets, extra = {}) =>
  checkKnownFailures({ repoRoot: root, today: TODAY, fileBudgets: budgets, ...extra });

describe('known-failure gate: spec files', () => {
  it('counts a test.fail( marker in a .spec.ts file against its budget', () => {
    const root = makeRepo({ 'tests/e2e/a.spec.ts': specWith(1) });
    const result = run(root, { 'tests/e2e/a.spec.ts': 1 });
    assert.deepEqual(result.problems, []);
    assert.equal(result.entries.length, 1);
    assert.equal(result.entries[0].where, 'tests/e2e/a.spec.ts:3');
    assert.deepEqual(result.specReport, [{ rel: 'tests/e2e/a.spec.ts', count: 1, budget: 1 }]);
  });

  it('fails a spec marker that has no budget entry (budget 0)', () => {
    const root = makeRepo({ 'tests/e2e/a.spec.ts': specWith(1) });
    const result = run(root, {});
    assert.equal(result.problems.length, 1);
    assert.match(result.problems[0], /tests\/e2e\/a\.spec\.ts: 1 known-failure markers, budget is 0/);
  });

  it('fails a spec with more markers than its budget', () => {
    const root = makeRepo({ 'tests/e2e/a.spec.ts': specWith(2) });
    const result = run(root, { 'tests/e2e/a.spec.ts': 1 });
    assert.match(result.problems.join('\n'), /tests\/e2e\/a\.spec\.ts: 2 known-failure markers, budget is 1/);
  });

  it('fails a spec with fewer markers than its budget', () => {
    const root = makeRepo({ 'tests/e2e/a.spec.ts': specWith(1) });
    const result = run(root, { 'tests/e2e/a.spec.ts': 2 });
    assert.match(result.problems.join('\n'), /tests\/e2e\/a\.spec\.ts: 1 known-failure markers, budget is 2/);
  });

  it('fails a budget entry whose spec file is gone (0 markers against a budget)', () => {
    const root = makeRepo({});
    const result = run(root, { [JOURNEY]: 13 });
    assert.match(result.problems.join('\n'), /direct-journey\.spec\.ts: 0 known-failure markers, budget is 13/);
  });

  it('does not count a test.fail( mentioned only in a comment', () => {
    const root = makeRepo({
      'tests/e2e/a.spec.ts': ' * Expected failures are test.fail(), each with a comment.\n// test.fail(\nlet x = 1;\n',
    });
    const result = run(root, {});
    assert.deepEqual(result.problems, []);
    assert.equal(result.entries.length, 0);
  });
});

describe('known-failure gate: expiry and format', () => {
  it('fails an expired entry in a spec file', () => {
    const root = makeRepo({ 'tests/e2e/a.spec.ts': specWith(1, { expires: '2026-10-15' }) });
    const result = run(root, { 'tests/e2e/a.spec.ts': 1 });
    assert.equal(result.entries[0].status, 'EXPIRED');
    assert.match(result.problems.join('\n'), /expired on 2026-10-15/);
  });

  it('fails an entry whose date does not exist', () => {
    const root = makeRepo({ 'tests/e2e/a.spec.ts': specWith(1, { expires: '2026-02-30' }) });
    const result = run(root, { 'tests/e2e/a.spec.ts': 1 });
    assert.equal(result.entries[0].status, 'MALFORMED');
    assert.match(result.problems.join('\n'), /invalid date 2026-02-30/);
  });

  it('fails a marker with no known-failure comment directly above it', () => {
    const root = makeRepo({
      'tests/e2e/a.spec.ts': 'test.fail(\'bare\', async () => {});\n',
    });
    const result = run(root, { 'tests/e2e/a.spec.ts': 1 });
    assert.equal(result.entries[0].status, 'MALFORMED');
    assert.match(result.problems.join('\n'), /missing or malformed known-failure comment/);
  });
});

describe('known-failure gate: src cap', () => {
  const srcFiles = (count) => Object.fromEntries(
    Array.from({ length: count }, (_, i) => [
      `src/feature/f${i}.test.ts`,
      `${comment()}\nit.fails('case ${i}', () => {});\n`,
    ]),
  );

  it('keeps the src cap at 10 and counts it.fails and the ternary form', () => {
    assert.equal(MAX_SRC_ENTRIES, 10);
    const root = makeRepo({
      ...srcFiles(MAX_SRC_ENTRIES - 1),
      'src/feature/ternary.test.ts': `${comment()}\n(flag ? it.fails : it)('case', () => {});\n`,
    });
    const result = run(root, {});
    assert.equal(result.srcCount, MAX_SRC_ENTRIES);
    assert.deepEqual(result.problems, []);
  });

  it('fails when src has more than 10 entries', () => {
    const root = makeRepo(srcFiles(MAX_SRC_ENTRIES + 1));
    const result = run(root, {});
    assert.match(result.problems.join('\n'), /11 src entries exceed the limit of 10/);
  });

  it('does not let spec markers count against the src cap', () => {
    const root = makeRepo({
      ...srcFiles(MAX_SRC_ENTRIES),
      'tests/e2e/a.spec.ts': specWith(3),
    });
    const result = run(root, { 'tests/e2e/a.spec.ts': 3 });
    assert.equal(result.srcCount, MAX_SRC_ENTRIES);
    assert.deepEqual(result.problems, []);
  });
});

describe('known-failure gate: this repository', () => {
  it('carries no budget entry for the journey spec (M = 0)', () => {
    assert.equal(FILE_BUDGETS[JOURNEY], undefined);
  });

  it('passes with the journey file matching its budget', () => {
    const result = checkKnownFailures({ repoRoot });
    const journey = result.specReport.find((spec) => spec.rel === JOURNEY);
    assert.ok(journey, 'journey spec is scanned');
    assert.equal(journey.count, 0, 'the journey spec has no known-failure marker');
    assert.equal(journey.budget, 0);
    assert.deepEqual(result.problems, []);
  });

  it('exits 0 from the npm script entry point', () => {
    const proc = spawnSync(process.execPath, [gateScript], { cwd: repoRoot, encoding: 'utf8' });
    assert.equal(proc.status, 0, proc.stderr);
    assert.doesNotMatch(proc.stdout, /direct-journey/, 'no marker and no budget: the journey is not listed');
  });
});
