import assert from 'node:assert/strict';
import test from 'node:test';
import type { Suite, TestCase, TestResult } from '@playwright/test/reporter';
import PlaywrightSkipGuard from '../../../../config/testing/playwrightSkipGuard.ts';

function fakeTest(id = 'test-id', annotations: TestCase['annotations'] = []): TestCase {
  return {
    id,
    expectedStatus: 'passed',
    annotations,
    titlePath: () => ['suite', 'test'],
  } as unknown as TestCase;
}

function suiteWith(...tests: TestCase[]): Suite {
  return { allTests: () => tests } as unknown as Suite;
}

test('list discovery does not classify unexecuted tests as NOT RUN', async () => {
  const guard = new PlaywrightSkipGuard({ _mode: 'list' });
  guard.onBegin({} as never, suiteWith(fakeTest()));

  assert.equal(await guard.onEnd(), undefined);
});

test('real execution still rejects an unexecuted test', async () => {
  const guard = new PlaywrightSkipGuard({ _mode: 'test' });
  guard.onBegin({} as never, suiteWith(fakeTest()));

  assert.deepEqual(await guard.onEnd(), { status: 'failed' });
});

test('real execution remains green when a test actually passes', async () => {
  const guard = new PlaywrightSkipGuard();
  const testCase = fakeTest();
  guard.onBegin({} as never, suiteWith(testCase));
  guard.onTestEnd(testCase, { status: 'passed' } as TestResult);

  assert.equal(await guard.onEnd(), undefined);
});

test('real execution still rejects an undeclared skip', async () => {
  const guard = new PlaywrightSkipGuard();
  const testCase = fakeTest('skip-id', [{ type: 'skip', description: 'unexpected environment' }]);
  guard.onBegin({} as never, suiteWith(testCase));
  guard.onTestEnd(testCase, { status: 'skipped' } as TestResult);

  assert.deepEqual(await guard.onEnd(), { status: 'failed' });
});

test('real execution still rejects a run with zero passed tests', async () => {
  const guard = new PlaywrightSkipGuard();
  const testCase = fakeTest('failed-id');
  guard.onBegin({} as never, suiteWith(testCase));
  guard.onTestEnd(testCase, { status: 'failed' } as TestResult);

  assert.deepEqual(await guard.onEnd(), { status: 'failed' });
});
