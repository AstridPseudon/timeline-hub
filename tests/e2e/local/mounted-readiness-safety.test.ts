import assert from 'node:assert/strict';
import { test } from 'node:test';
import { clearMountedBootstrapFailure, hasFreshSettledOwner, isFreshlyConnected, MountedBootstrapError, readExistingReadonly, readMountedBootstrapFailure, recordMountedBootstrapFailure } from './mounted-readiness-safety.ts';

test('missing database is unavailable, not a verified empty baseline', async () => {
  let reads = 0;
  const result = await readExistingReadonly(async () => false, async () => {
    reads += 1;
    return [];
  });
  assert.deepEqual(result, { status: 'unknown', reason: 'unavailable' });
  assert.equal(reads, 0);
});

test('database read rejection remains unknown', async () => {
  const result = await readExistingReadonly(async () => true, async () => { throw new Error('read rejected'); });
  assert.deepEqual(result, { status: 'unknown', reason: 'read-rejected' });
});

test('an available empty database is a verified empty baseline', async () => {
  const result = await readExistingReadonly(async () => true, async () => []);
  assert.deepEqual(result, { status: 'verified', value: [] });
});

test('only a new settled owner qualifies after the verified baseline', () => {
  const previous = new Set(['old-owner']);
  assert.equal(hasFreshSettledOwner([{ ownerId: 'old-owner', intents: [] }], previous), false);
  assert.equal(hasFreshSettledOwner([{ ownerId: 'new-owner', pending: { state: 'pending' }, intents: [] }], previous), false);
  assert.equal(hasFreshSettledOwner([{ ownerId: 'new-owner', intents: ['gesture'] }], previous), false);
  assert.equal(hasFreshSettledOwner([{ ownerId: 'new-owner', intents: [] }], previous), true);
});

test('a closed page read cannot become a verified baseline', async () => {
  const result = await readExistingReadonly(async () => { throw new Error('page closed'); }, async () => []);
  assert.deepEqual(result, { status: 'unknown', reason: 'unavailable' });
});

test('a disconnected selection read cannot retain the initial connected claim', () => {
  assert.equal(isFreshlyConnected({ attached: true, state: 'connected' }), true);
  assert.equal(isFreshlyConnected({ attached: true, state: 'disconnected' }), false);
  assert.equal(isFreshlyConnected({ attached: 'UNKNOWN', state: 'connected' }), false);
});

test('mounted bootstrap failures expose only a finite safe projection', () => {
  clearMountedBootstrapFailure();
  const cause = new Error('private cause remains on the error');
  recordMountedBootstrapFailure(new MountedBootstrapError({ stage: 'selection', code: 'mounted-bootstrap', class: 'mounted-bootstrap' }, cause));
  assert.deepEqual(readMountedBootstrapFailure(), { stage: 'selection', code: 'mounted-bootstrap', class: 'mounted-bootstrap' });
  clearMountedBootstrapFailure();
  assert.equal(readMountedBootstrapFailure(), undefined);
});
