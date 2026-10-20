import { describe, expect, it, vi } from 'vitest';
import type { CommitRequest } from '@/integrations/runtime/generated.ts';
import type { TimelineCommitResult } from '../data/DataProvider.ts';
import { environment, scope } from './__tests__/commitSessionEnvironment.ts';

// Unit transport only: provider/compiler versions are result metadata here.
// TimelineCommandBasis has no engine/schema fields; requests retain the real
// command schema_version/version. A paired Runtime upgrade needs live coverage.
async function persistedSuffix(fault: 'lost' | 'unavailable' = 'lost') {
  const env = await environment();
  const first = await env.mount();
  env.setFault(fault);
  env.move(first, 5);
  env.move(first, 7);
  await vi.waitFor(() => expect(first.getState().status).toBe('retry'));
  await first.dispose();
  const [saved] = await env.reopenOutboxes().list(scope);
  expect(saved.intents).toHaveLength(2);
  expect(saved.intents[1].basis).toEqual({ after: saved.intents[0].id });
  expect(saved.pending?.request).toEqual(env.requests[0]);
  return { env, saved };
}

describe('persisted command recovery across provider metadata changes (unit transport)', () => {
  it('replays accepted A exactly, retains guarded B at HA, and preserves disjoint observed C', async () => {
    const { env, saved } = await persistedSuffix();
    const originalA = saved.pending!.request;
    const originalB = saved.intents[1];
    const oldAcceptance = env.acceptances()[0];
    expect(oldAcceptance.data).toMatchObject({ provider_version: 'provider-1', compiler_version: 'compiler-1' });
    expect(JSON.parse(originalA.body)).toMatchObject({ base_revision_id: 'r0', base_publication_id: 'p0',
      commands: [{ schema_version: 1, version: '1', args: { on: 5 } }] });

    env.setVersions('provider-2', 'compiler-2');
    // This fake policy refuses unaccepted old commands, but already accepted
    // identities still replay. It is not Runtime compatibility validation.
    env.setIncompatible(true);
    const c = await env.external((document) => {
      document.parent_revision.payload.opaque = { collaborator: ['C', null] };
    });
    const client = env.reopenProvider();
    const basis = await client.loadTimelineCommandBasis(scope.timelineId);
    expect(basis.head).toEqual(c.head);
    const results: TimelineCommitResult[] = [];
    const send = client.commitTimeline.bind(client);
    vi.spyOn(client, 'commitTimeline').mockImplementation(async (...args) => {
      const result = await send(...args);
      results.push(result);
      if (results.length === 1) {
        env.setIncompatible(false);
        env.setFault('busy');
      }
      return result;
    });
    const outboxes = env.reopenOutboxes();
    const reopened = await env.mount(basis, client, outboxes);
    try {
      expect(reopened.getState()).toMatchObject({ status: 'recovery', recoverableOwners: [saved.ownerId] });
      expect(env.requests).toHaveLength(1);
      await reopened.recover(saved.ownerId);
      expect(env.requests[1]).toEqual(originalA);
      expect(results[0].response).toEqual(oldAcceptance);
      expect(results[0].receipt).toEqual(oldAcceptance.receipt);
      expect(results[0].accepted).toEqual({ revisionId: 'r1', publicationId: 'p1' });
      expect(env.acceptances()).toEqual([oldAcceptance]);

      const [retained] = await outboxes.list(scope);
      expect(retained.accepted).toMatchObject({ intentId: saved.intents[0].id,
        head: { revisionId: 'r1', publicationId: 'p1' }, value: { response: oldAcceptance } });
      expect(retained.intents).toEqual([{ ...originalB, readyBase: { revisionId: 'r1', publicationId: 'p1' } }]);
      const requestB = env.requests[2];
      const bodyB = JSON.parse(requestB.body) as CommitRequest;
      expect(requestB.key).not.toBe(originalA.key);
      expect(requestB.path).toBe(originalA.path);
      expect(bodyB).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p1' });
      expect(bodyB.commands).toEqual((originalB.payload as { commands: unknown }).commands);
      expect(bodyB.commands[0].expect?.['parent/clip:x::at']).toEqual({ state: 'present', value: 5 });
      expect(bodyB.commands[0].bindings).toBeDefined();
      expect(bodyB.commands[0].reads?.length).toBeGreaterThan(0);
      expect(bodyB.commands[0].selections?.length).toBeGreaterThan(0);
      // Recovery paints the original displayed closure and B preview, not C
      // relabelled as B's authoring basis or A's stale acknowledged graph.
      expect(env.projected.at(-1)).toEqual(env.initial);
      expect(env.previews).toHaveBeenCalledTimes(2);
      expect(reopened.getState().status).toBe('retry');

      env.setFault(null);
      await reopened.retry();
      expect(env.requests).toHaveLength(4);
      expect(env.requests[3]).toEqual(requestB);
      expect(results[1].response.data).toMatchObject({ provider_version: 'provider-2', compiler_version: 'compiler-2',
        base_revision_id: 'r1', base_publication_id: 'p1', previous_revision_id: c.head.revisionId,
        previous_publication_id: c.head.publicationId });
      expect(env.current().config.clips[0].at).toBe(7);
      expect(env.projected.at(-1)?.canonicalDocument.parent_revision.payload.opaque).toEqual({ collaborator: ['C', null] });
      expect(reopened.getState().status).toBe('saved');
      expect((await outboxes.list(scope))[0].intents).toEqual([]);
      expect(env.acceptances()).toHaveLength(2);
      expect(env.acceptances()[0]).toEqual(oldAcceptance);
    } finally { await reopened.dispose(); }
  });

  it('surfaces a changed B guard after replaying accepted A without refreshing or dropping B', async () => {
    const { env, saved } = await persistedSuffix();
    const originalB = saved.intents[1];
    const c = await env.external((document) => {
      const clips = document.parent_revision.payload.clips as { at: number }[];
      clips[0].at = 9;
    });
    env.setVersions('provider-2', 'compiler-2');
    const client = env.reopenProvider();
    const outboxes = env.reopenOutboxes();
    const reopened = await env.mount(await client.loadTimelineCommandBasis(scope.timelineId), client, outboxes);
    try {
      await reopened.recover(saved.ownerId);
      expect(env.requests[1]).toEqual(saved.pending!.request);
      expect(JSON.parse(env.requests[2].body)).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p1',
        commands: (originalB.payload as { commands: unknown }).commands });
      expect(reopened.getState()).toMatchObject({ status: 'conflict', canUndo: false, error: expect.stringContaining('expect') });
      const [refused] = await outboxes.list(scope);
      expect(refused.intents[0]).toMatchObject({ ...originalB, readyBase: { revisionId: 'r1', publicationId: 'p1' } });
      expect(refused.intents[0].conflict).toMatchObject({ kind: 'conflict' });
      expect(refused.accepted?.head).toEqual({ revisionId: 'r1', publicationId: 'p1' });
      await reopened.retry();
      await expect(reopened.flush()).rejects.toThrow('expect');
      expect(env.requests).toHaveLength(3);
      expect((await outboxes.list(scope))[0].intents).toEqual(refused.intents);
      expect((await client.loadTimelineCommandBasis(scope.timelineId)).head).toEqual(c.head);
      expect(env.acceptances()).toHaveLength(1);
    } finally { await reopened.dispose(); }
  });

  it('keeps an unaccepted incompatible A visibly refused with its dependent suffix across another reopen', async () => {
    const { env, saved } = await persistedSuffix('unavailable');
    const error = 'incompatible_command: Old command version is incompatible';
    expect(env.acceptances()).toEqual([]);
    env.setFault(null);
    env.setVersions('provider-2', 'compiler-2');
    env.setIncompatible(true);
    await env.external((document) => { document.parent_revision.payload.opaque = { collaborator: 'C' }; });
    const client = env.reopenProvider();
    const outboxes = env.reopenOutboxes();
    const reopened = await env.mount(await client.loadTimelineCommandBasis(scope.timelineId), client, outboxes);
    await reopened.recover(saved.ownerId);
    expect(env.requests).toHaveLength(2);
    expect(env.requests[1]).toEqual(saved.pending!.request);
    expect(reopened.getState()).toMatchObject({ status: 'error', canUndo: false, error });
    const [refused] = await outboxes.list(scope);
    expect(refused.pending?.outcome).toMatchObject({ kind: 'rejected', error: { kind: 'refused' } });
    expect(refused.intents).toEqual(saved.intents.map((intent) => ({ ...intent,
      conflict: { kind: 'refused', message: error } })));
    expect(refused.accepted).toBeUndefined();
    expect(refused.intents[1].readyBase).toBeUndefined();
    await reopened.dispose();

    env.setIncompatible(false);
    const nextClient = env.reopenProvider();
    const nextOutboxes = env.reopenOutboxes();
    const next = await env.mount(await nextClient.loadTimelineCommandBasis(scope.timelineId), nextClient, nextOutboxes);
    try {
      await next.recover(saved.ownerId);
      await next.retry();
      await expect(next.flush()).rejects.toThrow('Old command version is incompatible');
      expect(() => env.move(next, 11)).toThrow('Old command version is incompatible');
      expect(next.getState()).toMatchObject({ status: 'error', canUndo: false });
      expect(env.requests).toHaveLength(2);
      const [retained] = await nextOutboxes.list(scope);
      expect(retained.pending).toEqual(refused.pending);
      expect(retained.intents).toEqual(refused.intents);
      expect(env.acceptances()).toEqual([]);
    } finally { await next.dispose(); }
  });

  it.each(['realmId', 'actorId', 'projectId', 'timelineId'] as const)(
    'cannot discover or recover the persisted owner under a changed %s', async (field) => {
      const { env, saved } = await persistedSuffix();
      env.setVersions('provider-2', 'compiler-2');
      const outboxes = env.reopenOutboxes();
      const otherScope = { ...scope, [field]: 'other' };
      expect(await outboxes.list(otherScope)).toEqual([]);
      const work = vi.fn(async () => {});
      await expect(outboxes.recover(otherScope, saved.ownerId, work)).rejects.toThrow('explicit claim');
      expect(work).not.toHaveBeenCalled();
      expect(await outboxes.list(scope)).toEqual([saved]);
      expect(env.requests).toHaveLength(1);
    },
  );

  it('retains persisted bytes when a new Runtime schema digest fails the normal handshake', async () => {
    const { env, saved } = await persistedSuffix();
    env.setSchemaDigest(`sha256:${'f'.repeat(64)}`);
    const client = env.reopenProvider();
    await expect(client.loadTimelineCommandBasis(scope.timelineId)).rejects.toThrow('schema digest mismatch');
    await expect(client.commitTimeline(JSON.parse(saved.pending!.request.body) as CommitRequest,
      saved.pending!.request.key)).rejects.toThrow('schema digest mismatch');
    expect(await env.reopenOutboxes().list(scope)).toEqual([saved]);
    expect(env.requests).toHaveLength(1);
    expect(env.acceptances()).toHaveLength(1);
  });

  it('drains a queued B append on close before a new provider claims the persisted A identity', async () => {
    const env = await environment();
    const first = await env.mount();
    env.setFault('lost');
    env.move(first, 5);
    await vi.waitFor(() => expect(first.getState().status).toBe('retry'));
    const [before] = await env.outboxes.list(scope);
    env.move(first, 7);
    await first.dispose();
    const outboxes = env.reopenOutboxes();
    const [saved] = await outboxes.list(scope);
    expect(saved.intents).toHaveLength(2);
    expect(saved.pending?.request).toEqual(before.pending!.request);
    expect(saved.intents[1]).toMatchObject({ basis: { after: saved.intents[0].id },
      payload: { commands: [{ args: { on: 7 }, expect: { 'parent/clip:x::at': { state: 'present', value: 5 } } }] } });
    env.setVersions('provider-2', 'compiler-2');
    const client = env.reopenProvider();
    const reopened = await env.mount(await client.loadTimelineCommandBasis(scope.timelineId), client, outboxes);
    try {
      expect(env.requests).toHaveLength(1);
      await reopened.recover(saved.ownerId);
      expect(env.requests[1]).toEqual(saved.pending!.request);
      expect(env.requests).toHaveLength(3);
      expect(env.current().config.clips[0].at).toBe(7);
      expect(reopened.getState().status).toBe('saved');
    } finally { await reopened.dispose(); }
  });
});
