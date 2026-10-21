import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import { assertPublicTrimRuntimeLock } from './public-trim-preflight.ts';

const lock = JSON.parse(readFileSync(new URL('../../../../runtime.lock.json', import.meta.url), 'utf8')) as Record<string, unknown>;
const sourceCommit = '95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c';

test('public Trim preflight accepts the full normal Runtime lock', () => {
  assert.doesNotThrow(() => assertPublicTrimRuntimeLock(lock, sourceCommit));
});

test('public Trim preflight rejects a wrong source commit', () => {
  assert.throws(() => assertPublicTrimRuntimeLock({ ...lock, source_commit: '0'.repeat(40) }, sourceCommit));
});

test('public Trim preflight rejects arbitrary lock entries', () => {
  const files = { ...(lock.files as Record<string, unknown>), 'extra/unowned.json': { from: 'extra/unowned.json', sha256: 'sha256:' + '0'.repeat(64) } };
  assert.throws(() => assertPublicTrimRuntimeLock({ ...lock, files }, sourceCommit));
});

