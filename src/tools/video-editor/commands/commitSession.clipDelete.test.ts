import { describe, expect, it, vi } from 'vitest';
import type { CommitRequest } from '@/integrations/runtime/timeline-commit-types.ts';
import type { TimelineCommandBasis, TimelineCommitResult } from '../data/DataProvider.ts';
import { authoringBundleFromDocument } from './authoringBundle.ts';
import { captureClipDeleteEdit, submitClipDeleteEdit } from './clipDeleteGesture.ts';
import { executeClipDelete } from './clipDeleteCapture.ts';
import { executeClipMove } from './clipMoveCapture.ts';
import { buildTimelineData } from '../lib/timeline-data.ts';
import { compileTimelinePatch } from '../lib/timeline-patch.ts';
import { captureTrackLabelEdit, submitTrackLabelEdit } from './trackLabelGesture.ts';
import { finishTrackLabel, type TrackLabelArgs } from './trackLabelCapture.ts';
import { fixtureDigest, acceptedCommit } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { captureClipMove, submitClipMove } from './semanticGestures.ts';
import { environment, scope, document } from './__tests__/commitSessionEnvironment.ts';
import { createTimelineCommandSession } from './commitSession.ts';

// Offline operation/session proof. This is not a real Runtime acceptance test.
async function deleteEnvironment(raw = document()) {
  const parent = raw.parent_revision.payload;
  (parent.clips as unknown[]).push({ id: 'y', track: 'V1', at: 9, hold: 1,
    text: { content: 'unrelated' }, opaque: { literal: 'parent/clip:x', nullable: null } });
  (parent.config as Record<string, unknown>).clips = structuredClone(parent.clips);
  raw.parent_revision.content_digest = fixtureDigest(parent);
  const env = await environment(raw);
  let basis = env.initial;
  let current = env.current();
  let lost: string | undefined;
  const cache = new Map<string, TimelineCommitResult>();
  const beforeByPublication = new Map<string, typeof raw>();
  const calls: { request: CommitRequest; key: string }[] = [];
  const previews = vi.fn((patch) => {
    const compiled = compileTimelinePatch(patch, current);
    if (!compiled.valid || !compiled.nextData) throw new Error('Invalid test preview');
    current = compiled.nextData;
  });
  const mount = () => createTimelineCommandSession({ scope, initial: basis, outboxes: env.outboxes,
    changed: () => {}, preview: previews,
    project: async (next, patches) => {
      current = await buildTimelineData(next.canonicalDocument.parent_revision.payload.config as never,
        { assets: {} }, undefined, 1, undefined, { projectId: scope.projectId, timelineId: scope.timelineId,
          headRevisionId: next.head.revisionId, headPublicationId: next.head.publicationId });
      for (const patch of patches) previews(patch);
    },
    send: async (request, key) => {
      calls.push({ request: structuredClone(request), key });
      let result = cache.get(key);
      if (!result) {
        const command = request.commands[0];
        const original = await authoringBundleFromDocument(basis.canonicalDocument);
        const before = structuredClone(basis.canonicalDocument);
        const after = command.op === 'clip.delete' ? executeClipDelete(original, command).bundle
          : command.op === 'clip.move' ? executeClipMove(original, command).bundle
          : command.op === 'track.set' ? finishTrackLabel({ bundle: original, command }, command.args as TrackLabelArgs).bundle : original;
        const head = { revisionId: `r${cache.size + 1}`, publicationId: `p${cache.size + 1}` };
        const canonicalDocument = command.op === 'timeline.inverse'
          ? structuredClone(beforeByPublication.get((command.args.publications as string[])[0])!)
          : structuredClone(basis.canonicalDocument);
        const payload = command.op === 'timeline.inverse' ? canonicalDocument.parent_revision.payload : { ...after.parent, occurrences: [] };
        canonicalDocument.parent_revision = { revision_id: head.revisionId,
          payload, content_digest: fixtureDigest(payload) };
        const response = acceptedCommit({ revision_id: head.revisionId, publication_id: head.publicationId },
          { revision_id: request.base_revision_id, publication_id: request.base_publication_id }, { commands: request.commands });
        response.data.canonical_document = canonicalDocument;
        response.data.document_digest = fixtureDigest(canonicalDocument);
        response.receipt.idempotency_key = key;
        result = { response, accepted: head, canonicalDocument, graph: {}, receipt: response.receipt };
        cache.set(key, result);
        beforeByPublication.set(head.publicationId, before);
        basis = { head, canonicalDocument };
      }
      if (request.commands[0].op === lost) { lost = undefined; throw new Error('lost acknowledgement'); }
      return result;
    },
  });
  return { ...env, mount, calls, previews, current: () => current, basis: () => basis,
    lose: (op: string) => { lost = op; },
    remove: (session: Awaited<ReturnType<typeof mount>>) =>
      submitClipDeleteEdit(captureClipDeleteEdit(session.clipDeletePort, current, 'x')) };
}

async function opaqueCanonicalDeleteEnvironment() {
  const raw = document();
  const parent = raw.parent_revision.payload;
  (parent.clips as Record<string, unknown>[])[0]!.app = {
    canonical: { ownerRef: 'opaque-owner', clipRef: 'literal', rawClipId: 'literal' },
  };
  (parent.config as Record<string, unknown>).clips = structuredClone(parent.clips);
  raw.parent_revision.content_digest = fixtureDigest(parent);
  return deleteEnvironment(raw);
}

describe('native parent clip delete in the shared durable command session', () => {
  it('accepts an authored parent row with opaque app.canonical metadata', async () => {
    const env = await opaqueCanonicalDeleteEnvironment();
    const session = await env.mount();
    env.remove(session);
    await session.flush();
    expect(env.calls[0].request.commands[0]).toMatchObject({
      op: 'clip.delete', select: 'parent/clip:x', args: {},
      expect: { 'parent/clip:x::': { state: 'present', value: {
        app: { canonical: { ownerRef: 'opaque-owner', clipRef: 'literal', rawClipId: 'literal' } },
      } } },
    });
    expect(env.current().config.clips.map((clip) => clip.id)).toEqual(['y']);
    await session.dispose();
  });

  it('recovers move → label → delete in one queue without replacing either port or refreshing guards', async () => {
    const env = await deleteEnvironment();
    const first = await env.mount();
    env.lose('clip.move');
    submitClipMove(captureClipMove(first.port, env.current(), 'x'), 5);
    submitTrackLabelEdit(captureTrackLabelEdit(first.trackLabelPort, env.current(), 'V1'),
      { values: { label: '保留 label' }, clear: [] });
    env.remove(first);
    expect(env.current().config.clips.map((clip) => clip.id)).toEqual(['y']);
    expect(env.current().config.tracks[0].label).toBe('保留 label');
    await vi.waitFor(() => expect(first.getState().status).toBe('retry'));
    const originalRequest = structuredClone(env.calls[0]);
    const [saved] = await env.outboxes.list(scope);
    const originalCommands = saved.intents.flatMap((intent) =>
      (intent.payload as { commands: unknown[] }).commands);
    expect(originalCommands).toMatchObject([{ op: 'clip.move' }, { op: 'track.set' },
      { op: 'clip.delete', expect: { 'parent/clip:x::': { state: 'present', value: { at: 5 } } } }]);
    await first.dispose();
    const reopened = await env.mount();
    await reopened.recover(first.getState().ownerId!);
    await reopened.flush();
    expect(env.calls[1]).toEqual(originalRequest);
    expect(env.calls.slice(1).flatMap((call) => call.request.commands)).toEqual(originalCommands);
    expect(env.calls.map((call) => call.request.base_publication_id)).toEqual(['p0', 'p0', 'p1', 'p2']);
    expect(new Set(env.calls.map((call) => call.key)).size).toBe(3);
    expect(env.current().config.tracks[0].label).toBe('保留 label');
    expect(env.current().config.clips.map((clip) => clip.id)).toEqual(['y']);
    expect(env.basis().canonicalDocument.parent_revision.payload.opaque).toEqual({ absent: null });
    expect((await env.outboxes.list(scope))[0].intents).toEqual([]);
    await reopened.dispose();
  });

  it('queues move then delete with original whole-row guards at the accepted predecessor base', async () => {
    const env = await deleteEnvironment();
    const session = await env.mount();
    submitClipMove(captureClipMove(session.port, env.current(), 'x'), 5);
    const captured = captureClipDeleteEdit(session.clipDeletePort, env.current(), 'x');
    const original = structuredClone(captured.basis);
    submitClipDeleteEdit(captured);
    await session.flush();
    const [move, remove] = env.calls;
    expect(move.request.commands[0].op).toBe('clip.move');
    expect(remove.request).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p1',
      commands: [{ op: 'clip.delete', select: 'parent/clip:x', args: {},
        expect: { 'parent/clip:x::': { state: 'present', value: { id: 'x', at: 5, app: { opaque: null } } } } }] });
    expect(remove.key).not.toBe(move.key);
    expect(captured.basis).toEqual(original);
    const surviving = env.basis().canonicalDocument.parent_revision.payload;
    expect(surviving.clips).toEqual([env.initial.canonicalDocument.parent_revision.payload.clips[1]]);
    expect(surviving.config.clips).toEqual(surviving.clips);
    expect(surviving.opaque).toEqual({ absent: null });
    expect(surviving.registry).toEqual(env.initial.canonicalDocument.parent_revision.payload.registry);
    expect(env.current().config.clips.map((clip) => clip.id)).toEqual(['y']);
    const beforeUndo = structuredClone(env.current().config);
    await session.undo();
    expect(env.current().config.clips.map((clip) => clip.id)).toEqual(['x', 'y']);
    expect(env.current().config.clips[0]).toMatchObject({ id: 'x', at: 5, app: { opaque: null } });
    expect(env.current().config.tracks).toEqual(beforeUndo.tracks);
    expect(env.calls[2].request.commands).toEqual([{ schema_version: 1, op: 'timeline.inverse', version: '1',
      select: null, args: { publications: ['p2'] } }]);
    await session.dispose();
  });
  it.each([false, true])('recovers delete B authored after unknown A with original guards and a label suffix: %s', async (labelSuffix) => {
    const env = await deleteEnvironment();
    const first = await env.mount();
    env.lose('clip.move');
    submitClipMove(captureClipMove(first.port, env.current(), 'x'), 5);
    await vi.waitFor(() => expect(first.getState().status).toBe('retry'));
    const [original] = await env.outboxes.list(scope);
    const wireA = structuredClone(env.calls[0]);
    const captured = captureClipDeleteEdit(first.clipDeletePort, env.current(), 'x');
    const originalCapture = structuredClone(captured.basis);
    const finish = vi.spyOn(first.clipDeletePort, 'finish');
    submitClipDeleteEdit(captured);
    const commandB = structuredClone(finish.mock.results[0].value.command);
    if (labelSuffix) submitTrackLabelEdit(captureTrackLabelEdit(first.trackLabelPort, env.current(), 'V1'),
      { values: { label: 'ordinary label suffix' }, clear: [] });
    await vi.waitFor(async () => expect((await env.outboxes.list(scope))[0].intents).toHaveLength(labelSuffix ? 3 : 2));
    const [queued] = await env.outboxes.list(scope);
    const commands = queued.intents.flatMap((intent) => (intent.payload as { commands: unknown[] }).commands);
    expect(env.calls).toEqual([wireA]);
    expect(queued.pending).toEqual(original.pending);
    expect(queued.intents[1]).toMatchObject({ basis: { after: queued.intents[0].id },
      payload: { commands: [commandB], displayBasis: env.initial } });
    expect(queued.intents[1].readyBase).toBeUndefined();
    expect(commandB.expect!['parent/clip:x::']).toMatchObject({ state: 'present',
      value: { id: 'x', at: 5, app: { opaque: null } } });
    const changed = structuredClone((queued.intents[1].payload as { before: Parameters<typeof executeClipDelete>[0] }).before);
    (changed.parent.clips as Record<string, unknown>[])[0].app = { opaque: false };
    expect(() => executeClipDelete(changed, commandB)).toThrow();
    await expect(first.undo()).rejects.toThrow('uncertain');
    await first.dispose();
    const recovered = await env.mount();
    expect(env.calls).toEqual([wireA]);
    await recovered.recover(queued.ownerId);
    await recovered.flush();
    expect(env.calls[1]).toEqual(wireA);
    expect(JSON.stringify(env.calls[1].request)).toBe(original.pending!.request.body);
    expect(env.calls[1].key).toBe(original.pending!.request.key);
    expect(env.calls.slice(1).flatMap((call) => call.request.commands)).toEqual(commands);
    expect(env.calls[2].request).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p1', commands: [commandB] });
    expect(new Set(env.calls.map((call) => call.key)).size).toBe(labelSuffix ? 3 : 2);
    expect(captured.basis).toEqual(originalCapture);
    expect(finish).toHaveBeenCalledOnce();
    expect(env.current().config.clips.map((clip) => clip.id)).toEqual(['y']);
    if (labelSuffix) expect(env.current().config.tracks[0].label).toBe('ordinary label suffix');
    expect((await env.outboxes.list(scope))[0].intents).toEqual([]);
    await recovered.dispose();
  });
  it.each(['clip.move', 'clip.delete'])('reopens a lost %s ACK and retries identical bytes/key without refreshing the delete', async (lost) => {
    const env = await deleteEnvironment();
    const first = await env.mount();
    env.lose(lost);
    submitClipMove(captureClipMove(first.port, env.current(), 'x'), 5);
    env.remove(first);
    await vi.waitFor(() => expect(first.getState().status).toBe('retry'));
    const before = structuredClone(env.calls);
    const [persisted] = await env.outboxes.list(scope);
    const deleteIntent = persisted.intents.find((intent) =>
      (intent.payload as { commands: { op: string }[] }).commands[0].op === 'clip.delete')!;
    const original = structuredClone(deleteIntent.payload);
    await first.dispose();
    const reopened = await env.mount();
    expect(reopened.getState().recoverableOwners).toEqual([first.getState().ownerId]);
    expect(env.calls).toEqual(before);
    await reopened.recover(first.getState().ownerId!);
    await reopened.flush();
    expect(env.calls[before.length]).toEqual(before[before.length - 1]);
    expect(JSON.stringify(env.calls[before.length].request)).toBe(persisted.pending!.request.body);
    expect(env.calls[before.length].key).toBe(persisted.pending!.request.key);
    const deletion = env.calls.find((call) => call.request.commands[0].op === 'clip.delete')!;
    expect(deletion.request.commands).toEqual((original as { commands: unknown }).commands);
    expect(deletion.request.commands[0].expect?.['parent/clip:x::']).toMatchObject({ state: 'present', value: { at: 5 } });
    expect(new Set(env.calls.map((call) => call.key)).size).toBe(2);
    expect(env.current().config.clips.map((clip) => clip.id)).toEqual(['y']);
    await reopened.dispose();
  });
  it('drains same-turn deletion before closing without sending or losing the original basis', async () => {
    const env = await deleteEnvironment();
    const session = await env.mount();
    env.remove(session);
    await session.dispose();
    expect(env.calls).toHaveLength(0);
    const [saved] = await env.outboxes.list(scope);
    expect(saved.intents).toHaveLength(1);
    expect(saved.intents[0].payload).toMatchObject({ commands: [{ op: 'clip.delete',
      expect: { 'parent/clip:x::': { state: 'present', value: { at: 1 } } } }] });
    expect(saved.intents[0].basis).toEqual({ head: env.initial.head });
  });
  it('keeps a delete captured over an unacknowledged move original across its ACK', async () => {
    const env = await deleteEnvironment();
    const session = await env.mount();
    env.lose('clip.move');
    submitClipMove(captureClipMove(session.port, env.current(), 'x'), 5);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const captured = captureClipDeleteEdit(session.clipDeletePort, env.current(), 'x');
    const original = structuredClone(captured.basis);
    await session.retry();
    submitClipDeleteEdit(captured);
    await session.flush();
    expect(captured.basis).toEqual(original);
    expect(env.calls[2].request).toMatchObject({ base_publication_id: 'p1', commands: [original.command] });
    await session.dispose();
  });
  it('refuses arbitrary previews, uncaptured commands, and stale local generations without enqueuing', async () => {
    const env = await deleteEnvironment();
    const session = await env.mount();
    const captured = captureClipDeleteEdit(session.clipDeletePort, env.current(), 'x');
    const { command } = session.clipDeletePort.finish(captured.basis);
    for (const operations of [[{ op: 'clip.remove', target: 'y' }],
      [{ op: 'clip.remove', target: 'x' }, { op: 'clip.remove', target: 'y' }],
      [{ op: 'clip.remove', target: 'x', payload: { config: {} } }]]) {
      expect(() => session.clipDeletePort.submit({ command,
        preview: { version: 1, operations } as never })).toThrow('same clip');
    }
    expect(() => session.clipDeletePort.submit({ command: { ...command, select: 'parent/clip:y' },
      preview: { version: 1, operations: [{ op: 'clip.remove', target: 'y' }] } })).toThrow('not captured');
    expect(env.previews).not.toHaveBeenCalled();
    submitClipMove(captureClipMove(session.port, env.current(), 'x'), 5);
    expect(() => submitClipDeleteEdit(captured)).toThrow('changed');
    await session.flush();
    expect(env.calls).toHaveLength(1);
    expect(env.calls[0].request.commands[0].op).toBe('clip.move');
    await session.dispose();
  });
  it.each(['projectId', 'timelineId', 'headRevisionId', 'headPublicationId', 'ambiguous', 'occurrence', 'unaddressable'])(
    'refuses a mismatched display %s before any preview or durable append', async (fault) => {
      const env = await deleteEnvironment();
      const session = await env.mount();
      const current = structuredClone(env.current());
      if (fault === 'ambiguous') current.resolvedConfig.clips.push(current.resolvedConfig.clips[0]);
      else if (fault === 'occurrence' || fault === 'unaddressable') current.resolvedConfig.clips[0].id =
        fault === 'occurrence' ? 'occurrence:o/clip:x' : 'x::unaddressable';
      else current.head![fault] = 'other';
      expect(() => captureClipDeleteEdit(session.clipDeletePort, current, 'x')).toThrow();
      expect(env.calls).toHaveLength(0);
      expect(env.previews).not.toHaveBeenCalled();
      expect((await env.outboxes.list(scope))[0].intents).toHaveLength(0);
      await session.dispose();
    });
  it.each(['unrelated', 'target opaque', 'target source', 'membership', 'order', 'dependency'])(
    'verifies the original capture against a newer closure: %s', async (fault) => {
      const env = await deleteEnvironment();
      const session = await env.mount();
      const captured = captureClipDeleteEdit(session.clipDeletePort, env.current(), 'x');
      const original = structuredClone(captured.basis);
      const remote: TimelineCommandBasis = structuredClone(env.basis());
      const parent = remote.canonicalDocument.parent_revision.payload;
      const clips = parent.clips as Record<string, unknown>[];
      if (fault === 'unrelated') clips[1].opaque = { preserved: [null, false, 0] };
      if (fault === 'target opaque') clips[0].opaque = { changed: true };
      if (fault === 'target source') clips[0].asset = 'different';
      if (fault === 'membership') clips.push({ id: 'z', track: 'V1', at: 20, hold: 1 });
      if (fault === 'order') clips.reverse();
      if (fault === 'dependency') clips[1].transition = { id: 'fade' };
      parent.config.clips = structuredClone(clips);
      remote.head = { revisionId: 'remote-r', publicationId: 'remote-p' };
      remote.canonicalDocument.parent_revision.revision_id = 'remote-r';
      remote.canonicalDocument.parent_revision.content_digest = fixtureDigest(parent);
      session.observe(remote);
      await vi.waitFor(() => expect(env.current().head?.headRevisionId).toBe('remote-r'));
      if (fault === 'unrelated') {
        submitClipDeleteEdit(captured);
        await session.dispose();
        const [saved] = await env.outboxes.list(scope);
        expect(saved.intents[0].payload).toMatchObject({ commands: [original.command],
          after: { parent: { clips: [clips[1]], opaque: { absent: null } } } });
      } else {
        expect(() => submitClipDeleteEdit(captured)).toThrow();
        expect((await env.outboxes.list(scope))[0].intents).toHaveLength(0);
        await session.dispose();
      }
      expect(captured.basis).toEqual(original);
      expect(env.calls).toHaveLength(0);
    });
  it('keeps a visibly refused deletion in the same outbox with its original guards', async () => {
    const env = await environment();
    env.setFault('conflict');
    const session = await env.mount();
    submitClipDeleteEdit(captureClipDeleteEdit(session.clipDeletePort, env.current(), 'x'));
    await vi.waitFor(() => expect(session.getState().status).toBe('conflict'));
    const [saved] = await env.outboxes.list(scope);
    expect(saved.intents[0].payload).toMatchObject({ commands: [{ op: 'clip.delete',
      expect: { 'parent/clip:x::': { state: 'present', value: { id: 'x', at: 1 } } } }] });
    expect(session.getState().error).toBe('conflict: conflict');
    await session.dispose();
  });
});
