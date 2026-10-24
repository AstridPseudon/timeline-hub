import assert from 'node:assert/strict';
import test from 'node:test';
import { createFakeIndexedDB } from 'fake-indexeddb';
import { createCommitOutbox } from '../../../../src/tools/video-editor/commands/commitOutbox.ts';
import { classifyGate5FaultOrder, sameGate5CommitIdentity } from './gate5-fault-order.ts';

const A = { key: 'key-a', body: '{"commands":["A"]}' };
const B = { key: 'key-b', body: '{"commands":["B"]}' };

test('fast and slow automatic retries stage only the first exact A replay', () => {
  for (const schedule of ['fast', 'slow']) {
    assert.equal(classifyGate5FaultOrder({ initial: undefined, candidate: A, automaticRetryStaged: false, recoveryForwarded: false }), 'initial');
    assert.equal(classifyGate5FaultOrder({ initial: A, candidate: A, automaticRetryStaged: false, recoveryForwarded: false }), 'stage-automatic-retry', schedule);
    assert.equal(classifyGate5FaultOrder({ initial: A, candidate: A, automaticRetryStaged: true, recoveryForwarded: false }), 'forward-dependent-or-recovery', schedule);
    assert.equal(classifyGate5FaultOrder({ initial: A, candidate: A, automaticRetryStaged: true, recoveryForwarded: true }), 'reject-unexpected-duplicate', schedule);
  }
});

test('different body/key traffic remains visible instead of being staged as A', () => {
  assert.equal(classifyGate5FaultOrder({ initial: A, candidate: B, automaticRetryStaged: false, recoveryForwarded: false }), 'forward-dependent-or-recovery');
  assert.equal(classifyGate5FaultOrder({ initial: A, candidate: { key: A.key, body: B.body }, automaticRetryStaged: false, recoveryForwarded: false }), 'forward-dependent-or-recovery');
  assert.equal(classifyGate5FaultOrder({ initial: A, candidate: { key: B.key, body: A.body }, automaticRetryStaged: false, recoveryForwarded: false }), 'forward-dependent-or-recovery');
  assert.equal(sameGate5CommitIdentity(A, { ...A }), true);
  assert.equal(sameGate5CommitIdentity(A, B), false);
});

test('a real outbox retry reuses A identity and settles one accepted owner result', async () => {
  const outboxes = createCommitOutbox({ indexedDB: createFakeIndexedDB(), exclusiveLock: async (_name, work) => work() });
  const scope = { realmId: 'realm', actorId: 'actor', projectId: 'project', timelineId: 'timeline' };
  const sent = [];
  let acknowledgements = 0;
  await outboxes.create(scope, async (owner) => {
    await owner.append({ commands: [{ op: 'doc.patch', args: { changes: [] } }] }, {
      head: { revisionId: 'revision-before', publicationId: 'publication-before' },
    });
    const build = () => ({ method: 'POST', path: '/v1/projects/project/timelines/timeline/commit',
      body: { commands: [{ op: 'doc.patch', args: { changes: [] } }] } });
    const transmit = (request) => {
      sent.push({ body: JSON.stringify(request.body), key: request.key });
      if (sent.length === 1) return { kind: 'retry', error: { code: 'offline-control' } };
      acknowledgements++;
      return { kind: 'accepted', head: { revisionId: 'revision-after', publicationId: 'publication-after' },
        value: { response: { data: { status: 'accepted' }, receipt: { receipt_id: 'publication-after' } } } };
    };
    await owner.dispatch(build, transmit);
    await owner.dispatch(() => { throw new Error('An exact pending retry must reuse its request'); }, transmit);
    const settled = await owner.read();
    assert.equal(settled.intents.length, 0);
    assert.equal(settled.pending, undefined);
    assert.equal(settled.accepted.head.revisionId, 'revision-after');
    assert.equal(settled.accepted.value.response.data.status, 'accepted');
    assert.equal(acknowledgements, 1);
    assert.equal(sent.length, 2);
    assert.equal(sent[0].key, sent[1].key);
    assert.equal(sent[0].body, sent[1].body);
  });
});
