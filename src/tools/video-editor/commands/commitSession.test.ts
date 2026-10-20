import { describe, expect, it, vi } from 'vitest';
import { captureTrackLabelEdit, submitTrackLabelEdit } from './trackLabelGesture.ts';
import type { TrackLabelArgs } from './trackLabelCapture.ts';
import { fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { acceptedCommit } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { captureClipMove, submitClipMove } from './semanticGestures.ts';
import { environment, scope, document } from './__tests__/commitSessionEnvironment.ts';
import { createTimelineCommandSession } from './commitSession.ts';
import type { OutboxRecord } from './commitOutbox.ts';
import type { EditCommand, MediaSelection } from '@/integrations/runtime/timeline-commit-types.ts';

async function editOwner(env: Awaited<ReturnType<typeof environment>>, change: (record: OutboxRecord) => void) {
  await new Promise<void>((resolve, reject) => {
    const request = env.factory.open('astrid.command-outbox', 1);
    request.addEventListener('error', () => reject(request.error));
    request.addEventListener('success', () => {
      const db = request.result;
      const tx = db.transaction('owners', 'readwrite');
      const store = tx.objectStore('owners');
      const read = store.getAll();
      read.addEventListener('success', () => {
        for (const record of read.result as OutboxRecord[]) {
          change(record);
          store.put(record, JSON.stringify([scope.realmId, scope.actorId, scope.projectId, scope.timelineId, record.ownerId]));
        }
      });
      tx.addEventListener('complete', () => { db.close(); resolve(); });
      tx.addEventListener('abort', () => { db.close(); reject(tx.error); });
    });
  });
}

describe('real clip move session through the Runtime HTTP boundary', () => {
  it('queues one native parent intent and retries its exact request after an unknown ACK', async () => {
    const env = await environment();
    const session = await env.mount();
    const media: MediaSelection = {
      asset: 'reserved-media',
      generation_id: 'generation-media',
      variant_id: 'variant-media',
      object_id: 'sha256:2222222222222222222222222222222222222222222222222222222222222222',
      catalog_digest: 'sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
    };
    const row = { id: 'native-clip', track: 'V1', at: 2, clipType: 'video', asset: 'reserved-media', from: 0, to: 1, hold: 1, speed: 1 };
    const basis = session.parentClipAddMediaPort.capture({ row, media, current: env.current() });
    const captured = session.parentClipAddMediaPort.finish(basis, {
      selection: { ...media }, media_type: 'video/mp4', size: 1, duration_seconds: 1,
    });
    env.setFault('lost');
    session.parentClipAddMediaPort.submit(captured);

    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const first = structuredClone(env.commits()[0]);
    const [stored] = await env.outboxes.list(scope);
    expect(stored.intents).toHaveLength(1);
    expect(stored.intents[0].payload).toMatchObject({ commands: [{ op: 'clip.add-media', args: { row, media } }] });

    await session.retry();
    expect(env.commits()).toHaveLength(2);
    expect(env.commits()[1]).toEqual(first);
    expect(env.current().config.clips).toContainEqual(expect.objectContaining({ id: 'native-clip', asset: 'reserved-media' }));
    await session.dispose();
  });

  it('drains a just-submitted gesture on dispose without flushing or starting a request', async () => {
    const env = await environment();
    const session = await env.mount();
    const owner = session.getState().ownerId!;
    env.move(session, 5);
    await session.dispose();
    expect(env.commits()).toHaveLength(0);
    const [saved] = await env.outboxes.list(scope);
    expect(saved.intents).toHaveLength(1);
    expect(saved.intents[0].payload).toMatchObject({ commands: [{ args: { on: 5 } }] });
    expect(() => env.move(session, 7)).toThrow('unavailable');
    const reopened = await env.mount();
    expect(reopened.getState().recoverableOwners).toEqual([owner]);
    await reopened.recover(owner);
    expect(env.commits()[0].body?.commands[0].expect?.['parent/clip:x::at']).toEqual({ state: 'present', value: 1 });
    expect(env.current().config.clips[0].at).toBe(5);
    await reopened.dispose();
  });
  it('holds the claim until an already-started durable append finishes', async () => {
    const env = await environment();
    let finishAppend!: () => void;
    const gate = new Promise<void>((resolve) => { finishAppend = resolve; });
    const create = env.outboxes.create;
    const appending = vi.fn();
    env.outboxes.create = (scope, work) => create(scope, (box, owner) => work({ ...box, append: async (...args) => {
      appending();
      await gate;
      return box.append(...args);
    } }, owner));
    const session = await env.mount();
    env.move(session, 5);
    await vi.waitFor(() => expect(appending).toHaveBeenCalledOnce());
    const closed = vi.fn();
    const closing = session.dispose().then(closed);
    await Promise.resolve();
    expect(closed).not.toHaveBeenCalled();
    await expect(env.outboxes.recover(scope, session.getState().ownerId!, async () => {})).rejects.toThrow('claimed');
    finishAppend();
    await closing;
    expect((await env.outboxes.list(scope))[0].intents).toHaveLength(1);
    expect(env.commits()).toHaveLength(0);
  });
  it.each(['accepted', 'error'] as const)('releases without A network completion, retains queued B and fences late %s', async (outcome) => {
    const env = await environment();
    const session = await env.mount();
    const network = env.pause();
    env.move(session, 5);
    await vi.waitFor(() => expect(env.commits()).toHaveLength(1));
    const original = structuredClone(env.commits()[0]);
    env.move(session, 7);
    await session.dispose();
    const [saved] = await env.outboxes.list(scope);
    expect(saved.intents).toHaveLength(2);
    expect(saved.pending?.request.key).toBe(original.key);
    expect(JSON.parse(saved.pending!.request.body)).toEqual(original.body);
    expect(saved.intents[1].payload).toMatchObject({ commands: [{ expect: { 'parent/clip:x::at': { state: 'present', value: 5 } } }] });
    const projectCount = env.projected.length;
    const closedState = session.getState();
    if (outcome === 'error') env.setFault('lost');
    const reopened = await env.mount();
    const recovering = reopened.recover(saved.ownerId);
    await vi.waitFor(() => expect(env.commits()).toHaveLength(2));
    network.resolve();
    await recovering;
    expect(env.commits()[1]).toEqual(original);
    expect(env.commits()).toHaveLength(3);
    expect(env.commits()[2].body).toMatchObject({ base_publication_id: 'p1', commands: [{ args: { on: 7 } }] });
    expect(env.commits()[2].key).not.toBe(original.key);
    expect(env.current().config.clips[0].at).toBe(7);
    expect(session.getState()).toEqual(closedState);
    expect(env.projected).toHaveLength(projectCount + 2);
    expect(reopened.getState().status).toBe('saved');
    await reopened.dispose();
  });
  it('reports a durable failure during close and never transmits the ephemeral preview', async () => {
    const env = await environment();
    const session = await env.mount();
    env.factory.open = () => { throw new Error('disk full'); };
    env.move(session, 5);
    await expect(session.dispose()).rejects.toThrow('Unsaved move: disk full');
    expect(session.getState()).toMatchObject({ status: 'error', error: 'Unsaved move: disk full', canUndo: false });
    expect(env.commits()).toHaveLength(0);
  });
  it('never starts a reserved transmission after close and lets a new claimant retry it exactly', async () => {
    const env = await environment();
    let finishReservation!: () => void;
    const gate = new Promise<void>((resolve) => { finishReservation = resolve; });
    const reserved = vi.fn();
    const create = env.outboxes.create;
    env.outboxes.create = (scope, work) => create(scope, (box, owner) => work({ ...box, dispatch: (build, transmit) =>
      box.dispatch(build, async (request) => {
        reserved(request);
        await gate;
        return transmit(request);
      }) }, owner));
    const session = await env.mount();
    env.move(session, 5);
    await vi.waitFor(() => expect(reserved).toHaveBeenCalledOnce());
    const finished = expect(session.flush()).rejects.toThrow('not acknowledged');
    await session.dispose();
    expect(env.commits()).toHaveLength(0);
    const reopened = await env.mount();
    await reopened.recover(session.getState().ownerId!);
    const request = reserved.mock.calls[0][0];
    expect(env.commits()[0]).toMatchObject({ path: request.path, method: request.method,
      body: JSON.parse(request.body), key: request.key });
    finishReservation();
    await finished;
    expect(env.commits()).toHaveLength(1);
    expect(reopened.getState().status).toBe('saved');
    await reopened.dispose();
  });
  it('opens the exact public immutable closure, preserving unknown/null/absent fields and child scope', async () => {
    const raw = acceptedCommit({ revision_id: 'r0', publication_id: 'p0' },
      { revision_id: 'old', publication_id: 'old' }, { children: true }).data.canonical_document;
    const env = await environment(raw);
    expect(env.initial.canonicalDocument).toEqual(raw);
    const projectReads = env.calls.filter((call) => call.path.startsWith('/v1/projects/')).map((call) => call.path);
    expect(projectReads).toEqual([
      '/v1/projects/project-commit/timelines/timeline-commit/commits?limit=50',
      '/v1/projects/project-commit/timelines/timeline-commit/composition-revisions/r0',
      '/v1/projects/project-commit/shots/shot-1/revisions/shot-r1',
      '/v1/projects/project-commit/timelines/child-timeline/revisions/internal-r1',
    ]);
  });
  it('refuses a missing raw manifest without inferring document or child pins', async () => {
    const raw = document();
    delete (raw as Partial<typeof raw>).dependency_manifest;
    await expect(environment(raw)).rejects.toThrow('dependency manifest');
  });
  it('captures dependent A5/B7 before preview, submits B at HA with original guards and a fresh key', async () => {
    const env = await environment();
    const session = await env.mount();
    const gate = env.pause();
    env.move(session, 5);
    env.move(session, 7);
    await vi.waitFor(() => expect(env.commits()).toHaveLength(1));
    expect(env.previews).toHaveBeenCalledTimes(2);
    gate.resolve();
    await session.flush();
    const [a, b] = env.commits();
    expect(a.body?.base_publication_id).toBe('p0');
    expect(b.body?.base_publication_id).toBe('p1');
    expect(b.body?.commands[0].expect?.['parent/clip:x::at']).toEqual({ state: 'present', value: 5 });
    expect(b.key).not.toBe(a.key);
    expect(env.projected.at(-1)?.head.publicationId).toBe('p2');
    expect(env.calls.filter((call) => call.method !== 'GET' && call.path !== '/v1/handshake').map((call) => call.path)).toEqual(env.commits().map((call) => call.path));
    await session.dispose();
  });
  it('keeps a drag capture original when its predecessor is acknowledged before drop', async () => {
    const env = await environment();
    const session = await env.mount();
    env.setFault('lost');
    env.move(session, 5);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const captured = captureClipMove(session.port, env.current(), 'x');
    const original = structuredClone(captured.basis);
    await session.retry();
    submitClipMove(captured, 7);
    await session.flush();
    expect(captured.basis).toEqual(original);
    expect(env.commits()[2].body?.base_publication_id).toBe('p1');
    expect(env.commits()[2].body?.commands[0].expect?.['parent/clip:x::at']).toEqual({ state: 'present', value: 5 });
    await session.dispose();
  });
  it('advances publication identity when a same-value move reuses the content revision', async () => {
    const env = await environment();
    const session = await env.mount();
    env.move(session, 5);
    await session.flush();
    env.move(session, 5);
    await session.flush();
    expect(env.projected.slice(-2).map((basis) => basis.head)).toEqual([
      { revisionId: 'r1', publicationId: 'p1' }, { revisionId: 'r1', publicationId: 'p2' },
    ]);
    await session.undo();
    expect(env.commits()[2].body).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p2',
      commands: [{ op: 'timeline.inverse', args: { publications: ['p2'] } }] });
    await session.dispose();
  });
  it('recovers an explicitly chosen owner and retries the exact pending A before B', async () => {
    const env = await environment();
    const first = await env.mount();
    env.setFault('lost');
    env.move(first, 5);
    env.move(first, 7);
    await vi.waitFor(() => expect(first.getState().status).toBe('retry'));
    const owner = first.getState().ownerId!;
    const original = env.commits()[0];
    await first.dispose();
    const reopened = await env.mount(await env.provider.loadTimelineCommandBasis('timeline-commit'));
    expect(reopened.getState().status).toBe('recovery');
    expect(env.commits()).toHaveLength(1);
    await reopened.recover(owner);
    expect(env.commits()[1]).toEqual(original);
    const b = env.commits()[2];
    expect(b.body?.base_publication_id).toBe('p1');
    expect(b.body?.commands[0].expect?.['parent/clip:x::at']).toEqual({ state: 'present', value: 5 });
    await reopened.dispose();
  });
  it.each(['accepted', 'conflict'] as const)(
    'queues B authored after uncertain A without retransmitting, then recovers exact A: %s', async (outcome) => {
      const env = await environment();
      const first = await env.mount();
      env.setFault('lost');
      env.move(first, 5);
      await vi.waitFor(() => expect(first.getState().status).toBe('retry'));
      const [original] = await env.outboxes.list(scope);
      const requestA = original.pending!.request;
      const wireA = structuredClone(env.commits()[0]);
      expect(wireA).toMatchObject({ method: requestA.method, path: requestA.path,
        bodyText: requestA.body, key: requestA.key });
      // The fake transport has already accepted A, but the session still displays H0 + A.
      const acceptedA = await env.provider.loadTimelineCommandBasis(scope.timelineId);
      expect(acceptedA.head).toEqual({ revisionId: 'r1', publicationId: 'p1' });
      expect(env.current().head?.headPublicationId).toBe('p0');
      expect(env.current().config.clips[0].at).toBe(5);
      expect(env.projected).toHaveLength(0);
      for (const head of [ { ...env.current().head!, headRevisionId: 'other' },
        { ...env.current().head!, headPublicationId: 'other' } ]) {
        expect(() => captureClipMove(first.port, { ...env.current(), head }, 'x')).toThrow('Displayed timeline');
      }
      const captured = captureClipMove(first.port, env.current(), 'x');
      const originalCapture = structuredClone(captured.basis);
      const finish = vi.spyOn(first.port, 'finish');
      submitClipMove(captured, 7);
      const commandB = structuredClone(finish.mock.results[0].value.command) as EditCommand;
      expect(commandB.expect!['parent/clip:x::at']).toEqual({ state: 'present', value: 5 });
      expect(commandB.reads!.length).toBeGreaterThan(0);
      expect(commandB.selections!.length).toBeGreaterThan(0);
      await vi.waitFor(() => expect(first.getState().status).toBe('retry'));
      const [queued] = await env.outboxes.list(scope);
      expect(env.commits()).toEqual([wireA]);
      expect(queued.pending).toEqual(original.pending);
      expect(queued.intents).toHaveLength(2);
      expect(queued.intents[0]).toEqual(original.intents[0]);
      expect(queued.intents[1]).toMatchObject({ basis: { after: original.intents[0].id },
        payload: { commands: [commandB], displayBasis: env.initial } });
      expect(queued.intents[1].readyBase).toBeUndefined();
      expect(captured.basis).toEqual(originalCapture);
      expect(() => submitClipMove(captured, 9)).toThrow('Timeline changed during the move');
      await expect(first.undo()).rejects.toThrow('uncertain');
      await expect(env.outboxes.recover(scope, queued.ownerId, async () => {})).rejects.toThrow('claimed');
      for (const field of ['realmId', 'actorId', 'projectId', 'timelineId']) {
        const other = { ...scope, [field]: 'other' };
        expect(await env.outboxes.list(other)).toEqual([]);
        await expect(env.outboxes.recover(other, queued.ownerId, async () => {})).rejects.toThrow('explicit claim');
      }
      await first.dispose();
      expect((await env.outboxes.list(scope))[0].intents).toEqual(queued.intents);
      const recovered = await env.mount(acceptedA);
      expect(recovered.getState()).toMatchObject({ status: 'recovery', recoverableOwners: [queued.ownerId] });
      expect(env.commits()).toEqual([wireA]);
      if (outcome === 'conflict') env.setFault('conflict');
      await recovered.recover(queued.ownerId);
      expect(env.project.mock.calls[0]).toEqual([env.initial, queued.intents.map((intent) => (intent.payload as { preview: unknown }).preview)]);
      expect(env.commits()[1]).toEqual(wireA);
      expect(finish.mock.results.map((result) => result.type)).toEqual(['return', 'throw']);
      if (outcome === 'accepted') {
        expect(env.commits()).toHaveLength(3);
        const wireB = env.commits()[2];
        expect(wireB.body).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p1', commands: [commandB] });
        expect(wireB.body?.commands).toEqual([commandB]);
        expect(wireB.key).not.toBe(wireA.key);
        expect(wireB.path).toBe(wireA.path);
        expect(recovered.getState()).toMatchObject({ status: 'saved', canUndo: true });
        expect(env.current().config.clips[0].at).toBe(7);
        expect(env.project.mock.calls.at(-1)?.[0].head).toEqual({ revisionId: 'r2', publicationId: 'p2' });
        expect(env.project.mock.calls.at(-1)?.[0].canonicalDocument.parent_revision.payload.clips).toMatchObject([{ id: 'x', at: 7 }]);
        await recovered.undo();
        await recovered.flush();
        expect(env.commits()[3].body).toMatchObject({ base_revision_id: 'r2', base_publication_id: 'p2',
          commands: [{ op: 'timeline.inverse', args: { publications: ['p2'] } }] });
        expect(env.commits()[3].key).not.toBe(wireB.key);
      } else {
        expect(recovered.getState()).toMatchObject({ status: 'conflict', canUndo: false });
        const [retained] = await env.outboxes.list(scope);
        expect(retained.intents.map(({ conflict, ...intent }) => intent)).toEqual(queued.intents);
        expect(retained.intents.every((intent) => intent.conflict !== undefined)).toBe(true);
        expect(retained.pending?.request).toEqual(requestA);
        expect(retained.intents[1].readyBase).toBeUndefined();
        await recovered.retry();
        await expect(recovered.flush()).rejects.toThrow('conflict');
        expect(env.commits()).toHaveLength(2);
      }
      await recovered.dispose();
    });
  it('retains an unsaved B preview after uncertain A without an ephemeral transmission', async () => {
    const env = await environment();
    const session = await env.mount();
    env.setFault('lost');
    env.move(session, 5);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const [original] = await env.outboxes.list(scope);
    const wireA = structuredClone(env.commits()[0]);
    const open = env.factory.open.bind(env.factory);
    env.factory.open = () => { throw new Error('disk full'); };
    env.move(session, 7);
    await vi.waitFor(() => expect(session.getState().status).toBe('error'));
    expect(session.getState()).toMatchObject({ error: 'Unsaved move: disk full', canUndo: false });
    expect(env.current().config.clips[0].at).toBe(7);
    expect(env.commits()).toEqual([wireA]);
    env.factory.open = open;
    const [retained] = await env.outboxes.list(scope);
    expect(retained.intents).toEqual(original.intents);
    expect(retained.pending).toEqual(original.pending);
    await session.retry();
    expect(env.commits()[1]).toEqual(wireA);
    expect(env.commits()[2].body?.commands[0].expect?.['parent/clip:x::at']).toEqual({ state: 'present', value: 5 });
    expect(session.getState().status).toBe('saved');
    await session.dispose();
  });
  it.each([true, false])('recovers legacy work only with a matching original document: %s', async (matching) => {
    const env = await environment();
    const session = await env.mount();
    env.setFault('busy');
    env.move(session, 5);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    await session.dispose();
    await editOwner(env, (record) => {
      delete (record.intents[0].payload as Record<string, unknown>).displayBasis;
      if (!matching && 'head' in record.intents[0].basis) record.intents[0].basis.head.revisionId = 'another-revision';
    });
    const reopened = await env.mount({ ...env.initial, head: { revisionId: 'r0', publicationId: 'new-publication' } });
    const [saved] = await env.outboxes.list(scope);
    if (matching) {
      await reopened.recover(session.getState().ownerId!);
      expect(env.projected.at(-1)).toEqual({ head: env.initial.head, canonicalDocument: env.initial.canonicalDocument });
      expect(reopened.getState().status).toBe('retry');
    } else {
      await expect(reopened.recover(session.getState().ownerId!)).rejects.toThrow('verified original display basis');
      expect(env.projected).toHaveLength(0);
      expect(env.commits()).toHaveLength(1);
      const [retained] = await env.outboxes.list(scope);
      expect(retained.intents).toEqual(saved.intents);
      expect(retained.pending).toEqual(saved.pending);
    }
    await reopened.dispose();
  });
  it.each(['missing dependent display basis', 'missing revision', 'empty revision', 'missing publication',
    'empty publication', 'missing document', 'mismatched revision'] as const)(
    'retains work without projecting or sending when recovery has a %s', async (fault) => {
      const env = await environment();
      const session = await env.mount();
      env.setFault('lost');
      env.move(session, 5);
      env.move(session, 7);
      await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
      // A's cached ACK must arrive before B's retryable refusal.
      const send = env.provider.commitTimeline.bind(env.provider);
      env.setFault(null);
      vi.spyOn(env.provider, 'commitTimeline').mockImplementation(async (...args) => {
        const result = await send(...args);
        env.setFault('busy');
        return result;
      });
      await session.retry();
      await session.dispose();
      await editOwner(env, (record) => {
        const payload = record.intents[0].payload as Record<string, unknown>;
        if (fault === 'missing dependent display basis') delete payload.displayBasis;
        else {
          const basis = payload.displayBasis as { head: { revisionId?: string; publicationId?: string }; canonicalDocument?: unknown };
          if (fault === 'missing publication') delete basis.head.publicationId;
          else if (fault === 'empty publication') basis.head.publicationId = '';
          else if (fault === 'missing revision') delete basis.head.revisionId;
          else if (fault === 'empty revision') basis.head.revisionId = '';
          else if (fault === 'missing document') delete basis.canonicalDocument;
          else basis.head.revisionId = 'another-revision';
        }
      });
      const [saved] = await env.outboxes.list(scope);
      const count = env.commits().length;
      const reopened = await env.mount(await env.provider.loadTimelineCommandBasis(scope.timelineId));
      await expect(reopened.recover(saved.ownerId)).rejects.toThrow('verified original display basis');
      expect(reopened.getState()).toMatchObject({ status: 'error', canUndo: false });
      expect(() => env.move(reopened, 9)).toThrow('verified original display basis');
      await reopened.retry();
      await expect(reopened.flush()).rejects.toThrow('verified original display basis');
      expect(env.projected).toHaveLength(0);
      expect(env.commits()).toHaveLength(count);
      const [retained] = await env.outboxes.list(scope);
      expect(retained.intents).toEqual(saved.intents);
      expect(retained.pending).toEqual(saved.pending);
      expect(retained.accepted).toEqual(saved.accepted);
      await reopened.dispose();
    });
  it('keeps recovery explicit and permits a later claim after the live owner releases its lock', async () => {
    const env = await environment();
    const first = await env.mount();
    env.setFault('lost');
    env.move(first, 5);
    await vi.waitFor(() => expect(first.getState().status).toBe('retry'));
    const owner = first.getState().ownerId!;
    const second = await env.mount();
    await expect(second.recover(owner)).rejects.toThrow('claimed');
    expect(env.commits()).toHaveLength(1);
    await first.dispose();
    await second.recover(owner);
    expect(env.commits()[1]).toEqual(env.commits()[0]);
    await second.dispose();
  });
  it('recovers B on its original display closure after A is acknowledged without changing submission bytes', async () => {
    const env = await environment();
    const first = await env.mount();
    env.setFault('lost');
    env.move(first, 5);
    env.move(first, 7);
    await vi.waitFor(() => expect(first.getState().status).toBe('retry'));
    const [original] = await env.outboxes.list(scope);
    const b = original.intents[1];
    await env.provider.undoTimeline({ projectId: scope.projectId, timelineId: scope.timelineId,
      headRevisionId: 'r1', headPublicationId: 'p1' }, ['p1'], 'independent-c');
    await first.retry();
    expect(env.commits()[2]).toEqual(env.commits()[0]);
    const requestB = structuredClone(env.commits()[3]);
    expect(requestB.body).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p1',
      commands: [{ args: { on: 7 }, expect: { 'parent/clip:x::at': { state: 'present', value: 5 } } }] });
    expect(requestB.key).not.toBe(env.commits()[0].key);
    expect(first.getState()).toMatchObject({ status: 'conflict', error: expect.stringContaining('expect') });
    const [beforeClose] = await env.outboxes.list(scope);
    expect(JSON.parse(beforeClose.pending!.request.body)).toEqual(requestB.body);
    expect(beforeClose.pending!.request.key).toBe(requestB.key);
    expect(beforeClose.intents[0]).toMatchObject({ ...b, readyBase: { revisionId: 'r1', publicationId: 'p1' } });
    expect(beforeClose.accepted?.head).toEqual({ revisionId: 'r1', publicationId: 'p1' });
    await first.dispose();
    const project = vi.fn(async () => {});
    const reopened = await createTimelineCommandSession({
      initial: await env.provider.loadTimelineCommandBasis('timeline-commit'), scope, outboxes: env.outboxes,
      send: (request, key) => env.provider.commitTimeline(request, key),
      preview: env.previews, project, changed: () => {},
    });
    await reopened.recover(original.ownerId);
    expect(project).toHaveBeenCalledExactlyOnceWith(env.initial, [(b.payload as any).preview]);
    expect((b.payload as any).preview.operations).toEqual([{ op: 'clip.move', target: 'x', payload: { at: 7 } }]);
    // B's failed original guard is a durable typed conflict; recovery cannot resend it.
    expect(env.commits()).toHaveLength(4);
    expect(reopened.getState()).toMatchObject({ status: 'conflict', error: first.getState().error, canUndo: false });
    await reopened.retry();
    await expect(reopened.flush()).rejects.toThrow(first.getState().error!);
    expect(env.commits()).toHaveLength(4);
    const [recovered] = await env.outboxes.list(scope);
    expect(recovered.intents).toEqual(beforeClose.intents);
    expect(recovered.pending).toEqual(beforeClose.pending);
    expect(recovered.accepted).toEqual(beforeClose.accepted);
    await reopened.dispose();
  });
  it.each((['conflict', 'refused', 'validation', 'authorization'] as const).flatMap((fault) =>
    [true, false].map((pending) => ({ fault, pending }))))(
    'retains typed $fault on recovery with pending request: $pending', async ({ fault, pending }) => {
      const env = await environment();
      const first = await env.mount();
      env.setFault(fault);
      env.move(first, 5);
      env.move(first, 7);
      const status = fault === 'conflict' ? 'conflict' : 'error';
      await vi.waitFor(() => expect(first.getState().status).toBe(status));
      const original = first.getState();
      await first.dispose();
      if (!pending) {
        // A retained rejection blocks the first intent even without a request reservation.
        await editOwner(env, (record) => { delete record.pending; });
      }
      const [saved] = await env.outboxes.list(scope);
      const reopened = await env.mount();
      await reopened.recover(original.ownerId!);
      expect(reopened.getState()).toMatchObject({ status, error: original.error, canUndo: false });
      await reopened.retry();
      expect(reopened.getState()).toMatchObject({ status, error: original.error, canUndo: false });
      await expect(reopened.flush()).rejects.toThrow(original.error!);
      expect(env.commits()).toHaveLength(1);
      expect((await env.outboxes.list(scope))[0].intents).toHaveLength(2);
      const [retained] = await env.outboxes.list(scope);
      expect(retained.intents).toEqual(saved.intents);
      expect(retained.pending).toEqual(saved.pending);
      await reopened.dispose();
    });
  it('keeps newer observed C when an old A acknowledgement arrives', async () => {
    const env = await environment();
    const session = await env.mount();
    const gate = env.pause();
    env.move(session, 5);
    await vi.waitFor(() => expect(env.commits()).toHaveLength(1));
    session.observe({ head: { revisionId: 'rc', publicationId: 'pc' }, canonicalDocument: document(9, 'rc') });
    gate.resolve();
    await session.flush();
    expect(env.projected.at(-1)?.head.publicationId).toBe('pc');
    await session.dispose();
  });
  it.each(['busy', 'unavailable', 'conflict'] as const)('distinguishes %s from an accepted move and retains its suffix', async (fault) => {
    const env = await environment();
    const session = await env.mount();
    env.setFault(fault);
    env.move(session, 5);
    env.move(session, 7);
    await vi.waitFor(() => expect(session.getState().status).toBe(fault === 'conflict' ? 'conflict' : 'retry'));
    const owners = await env.outboxes.list(scope);
    expect(owners[0].intents).toHaveLength(2);
    await expect(session.undo()).rejects.toThrow();
    if (fault !== 'conflict') {
      const first = env.commits()[0];
      env.setFault(null);
      await session.retry();
      expect(env.commits()[1]).toEqual(first);
      expect(session.getState().status).toBe('saved');
    }
    await session.dispose();
  });
  it('keeps the preview visible and sends nothing when durable append fails', async () => {
    const env = await environment();
    const session = await env.mount();
    const originalOpen = env.factory.open.bind(env.factory);
    env.factory.open = () => { throw new Error('disk full'); };
    env.move(session, 5);
    await vi.waitFor(() => expect(session.getState().status).toBe('error'));
    expect(session.getState().error).toContain('Unsaved move');
    expect(env.previews).toHaveBeenCalledOnce();
    expect(env.commits()).toHaveLength(0);
    await expect(session.flush()).rejects.toThrow();
    env.factory.open = originalOpen;
    await session.retry();
    expect(env.commits()).toHaveLength(1);
    expect(session.getState().status).toBe('saved');
    await session.dispose();
  });
  it('undo sends the explicit accepted publication via the same durable commit path', async () => {
    const env = await environment();
    const session = await env.mount();
    env.move(session, 5);
    await session.flush();
    await session.undo();
    await session.flush();
    expect(env.commits()[1].body?.commands).toEqual([{ schema_version: 1, op: 'timeline.inverse', version: '1', select: null, args: { publications: ['p1'] } }]);
    expect(env.commits()[1].key).not.toBe(env.commits()[0].key);
    await session.dispose();
  });
});

function rawTrack(raw: ReturnType<typeof document>) {
  return (raw.parent_revision.payload.config as { tracks: Array<{ id: string; label?: string }> }).tracks[0];
}

function rename(session: Awaited<ReturnType<typeof createTimelineCommandSession>>, current: ReturnType<Awaited<ReturnType<typeof environment>>['current']>, label: string) {
  submitTrackLabelEdit(captureTrackLabelEdit(session.trackLabelPort, current, 'V1'), { values: { label }, clear: [] });
}

describe('track labels in the existing durable command session', () => {
  it.each([undefined, 'Original', ''])('keeps original presence %j for value, empty and clear edits', async (original) => {
    for (const args of [
      { values: { label: 'Renamed' }, clear: [] },
      { values: { label: '' }, clear: [] },
      { values: {}, clear: ['label'] },
    ] as TrackLabelArgs[]) {
      const raw = document();
      if (original !== undefined) rawTrack(raw).label = original;
      raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
      const env = await environment(raw);
      const session = await env.mount();
      const captured = captureTrackLabelEdit(session.trackLabelPort, env.current(), 'V1');
      submitTrackLabelEdit(captured, args);
      await session.flush();
      const command = env.commits()[0].body!.commands[0];
      expect(command).toMatchObject({ op: 'track.set', version: '1', select: 'parent/track:V1', args,
        expect: { 'parent/track:V1::label': original === undefined ? { state: 'absent' } : { state: 'present', value: original } },
        bindings: { 'scalar.target': 'parent/track:V1' } });
      expect(Object.keys(command.expect!)).toEqual(['parent/track:V1::label']);
      expect(command.reads).toEqual([{ ref: 'parent/track:V1', path: ['id'], state: { state: 'present', value: 'V1' } }]);
      const accepted = env.projected.at(-1)!.canonicalDocument;
      if ('label' in args.values) expect(rawTrack(accepted).label).toBe(args.values.label);
      else expect(rawTrack(accepted)).not.toHaveProperty('label');
      expect(accepted.parent_revision.payload.opaque).toEqual({ absent: null });
      expect(accepted.parent_revision.payload.clips).toEqual(raw.parent_revision.payload.clips);
      expect(env.previews.mock.calls[0][0]).toEqual({ version: 1, operations: [{ op: 'track.update', target: 'V1',
        payload: { label: 'label' in args.values ? args.values.label : 'V1' } }] });
      await session.undo();
      await session.flush();
      expect(env.commits()[1].body!.commands[0]).toMatchObject({ op: 'timeline.inverse', args: { publications: ['p1'] } });
      const restored = rawTrack(env.projected.at(-1)!.canonicalDocument);
      if (original === undefined) expect(restored).not.toHaveProperty('label');
      else expect(restored.label).toBe(original);
      await session.dispose();
    }
  });
  it('keeps queued move → label guards and the exact native pending identity through reload', async () => {
    const env = await environment();
    const session = await env.mount();
    env.setFault('lost');
    env.move(session, 5);
    rename(session, env.current(), 'Queued label');
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const original = structuredClone(env.commits()[0]);
    const [stored] = await env.outboxes.list(scope);
    expect(stored.intents).toHaveLength(2);
    expect(stored.intents[1].basis).toEqual({ after: stored.intents[0].id });
    const labelPayload = structuredClone(stored.intents[1].payload);
    expect(labelPayload).toMatchObject({ commands: [{ op: 'track.set', args: { values: { label: 'Queued label' }, clear: [] },
      expect: { 'parent/track:V1::label': { state: 'absent' } } }],
    after: { parent: { clips: [{ at: 5 }], config: { tracks: [{ label: 'Queued label' }] } } } });
    expect(stored.pending?.request.key).toBe(original.key);
    expect(JSON.parse(stored.pending!.request.body)).toEqual(original.body);
    await session.dispose();
    const reopened = await env.mount(await env.provider.loadTimelineCommandBasis('timeline-commit'));
    expect(reopened.getState().status).toBe('recovery');
    expect(env.commits()).toHaveLength(1);
    await reopened.recover(stored.ownerId);
    expect(env.commits()[1]).toEqual(original);
    expect(env.commits()[2].body).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p1',
      commands: (labelPayload as { commands: unknown }).commands });
    expect(env.commits()[2].key).not.toBe(original.key);
    expect(env.current().config.clips[0].at).toBe(5);
    expect(rawTrack(env.projected.at(-1)!.canonicalDocument).label).toBe('Queued label');
    await reopened.undo();
    await reopened.flush();
    expect(rawTrack(env.projected.at(-1)!.canonicalDocument)).not.toHaveProperty('label');
    expect(env.current().config.clips[0].at).toBe(5);
    await reopened.dispose();
  });
  it('keeps typing capture original when A is acknowledged before label completion', async () => {
    const env = await environment();
    const session = await env.mount();
    env.setFault('lost');
    env.move(session, 5);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const captured = captureTrackLabelEdit(session.trackLabelPort, env.current(), 'V1');
    const basis = structuredClone(captured.basis);
    await session.retry();
    submitTrackLabelEdit(captured, { values: { label: 'Typed over A' }, clear: [] });
    await session.flush();
    expect(captured.basis).toEqual(basis);
    expect(env.commits()[2].body).toMatchObject({ base_publication_id: 'p1', commands: [{ op: 'track.set',
      expect: { 'parent/track:V1::label': { state: 'absent' } } }] });
    expect(env.current().config.clips[0].at).toBe(5);
    await session.dispose();
  });
  it('refuses an observed external label mutation during typing without replacing the input', async () => {
    const env = await environment();
    const session = await env.mount();
    const captured = captureTrackLabelEdit(session.trackLabelPort, env.current(), 'V1');
    session.observe(await env.external((raw) => { rawTrack(raw).label = 'Someone else'; }));
    await vi.waitFor(() => expect(env.current().config.tracks[0].label).toBe('Someone else'));
    const args: TrackLabelArgs = { values: { label: 'My typing' }, clear: [] };
    expect(() => submitTrackLabelEdit(captured, args)).toThrow('Track label changed');
    expect(args.values.label).toBe('My typing');
    expect(captured.basis.command).toMatchObject({ expect: { 'parent/track:V1::label': { state: 'absent' } } });
    expect(env.commits()).toHaveLength(0);
    expect((await env.outboxes.list(scope))[0].intents).toHaveLength(0);
    await session.dispose();
  });
  it('surfaces an unobserved external label change as a real guarded conflict', async () => {
    const env = await environment();
    const session = await env.mount();
    const captured = captureTrackLabelEdit(session.trackLabelPort, env.current(), 'V1');
    await env.external((raw) => { rawTrack(raw).label = 'Someone else'; });
    submitTrackLabelEdit(captured, { values: { label: 'My typing' }, clear: [] });
    await expect(session.flush()).rejects.toThrow('original capture');
    expect(session.getState().status).toBe('conflict');
    const [stored] = await env.outboxes.list(scope);
    expect(stored.intents[0].payload).toMatchObject({ commands: [{ args: { values: { label: 'My typing' } } }],
      preview: { operations: [{ payload: { label: 'My typing' } }] } });
    await session.dispose();
  });
  it.each(['move', 'label'] as const)('allows disjoint remote editing while %s guards stay original', async (operation) => {
    const env = await environment();
    const session = await env.mount();
    const capturedMove = captureClipMove(session.port, env.current(), 'x');
    const capturedLabel = captureTrackLabelEdit(session.trackLabelPort, env.current(), 'V1');
    const remote = await env.external((raw) => {
      if (operation === 'move') rawTrack(raw).label = 'Remote label';
      else {
        (raw.parent_revision.payload.clips as Array<{ at: number }>)[0].at = 8;
        (raw.parent_revision.payload.config as { clips: Array<{ at: number }> }).clips[0].at = 8;
      }
    });
    session.observe(remote);
    await vi.waitFor(() => expect(env.current().head?.headRevisionId).toBe(remote.head.revisionId));
    if (operation === 'move') submitClipMove(capturedMove, 5);
    else submitTrackLabelEdit(capturedLabel, { values: { label: 'Local label' }, clear: [] });
    await session.flush();
    const accepted = env.projected.at(-1)!.canonicalDocument;
    expect(env.current().config.clips[0].at).toBe(operation === 'move' ? 5 : 8);
    expect(rawTrack(accepted).label).toBe(operation === 'move' ? 'Remote label' : 'Local label');
    const command = env.commits()[0].body!.commands[0];
    expect(command.expect?.[operation === 'move' ? 'parent/clip:x::at' : 'parent/track:V1::label'])
      .toEqual(operation === 'move' ? { state: 'present', value: 1 } : { state: 'absent' });
    if (operation === 'move') expect(command.reads?.some((read) => read.path.includes('label'))).toBe(false);
    else expect(command.reads?.some((read) => read.ref.includes('/clip:'))).toBe(false);
    await session.dispose();
  });
  it('drains a label-only edit on close into the same outbox without starting a request', async () => {
    const env = await environment();
    const session = await env.mount();
    rename(session, env.current(), 'Closed draft');
    await session.dispose();
    expect(env.commits()).toHaveLength(0);
    const [stored] = await env.outboxes.list(scope);
    expect(stored.intents).toHaveLength(1);
    expect(stored.intents[0].payload).toMatchObject({ commands: [{ op: 'track.set' }] });
    const recovered = await env.mount();
    await recovered.recover(stored.ownerId);
    expect(rawTrack(env.projected.at(-1)!.canonicalDocument).label).toBe('Closed draft');
    await recovered.dispose();
  });
  it('keeps a pending label request unchanged when a newer move is authored', async () => {
    const env = await environment();
    const session = await env.mount();
    env.setFault('lost');
    rename(session, env.current(), 'First label');
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const original = structuredClone(env.commits()[0]);
    env.move(session, 5);
    await session.dispose();
    const [stored] = await env.outboxes.list(scope);
    expect(stored.pending?.request.key).toBe(original.key);
    expect(JSON.parse(stored.pending!.request.body)).toEqual(original.body);
    const recovered = await env.mount(await env.provider.loadTimelineCommandBasis('timeline-commit'));
    await recovered.recover(stored.ownerId);
    expect(env.commits()[1]).toEqual(original);
    expect(env.commits()[2].body).toMatchObject({ base_publication_id: 'p1', commands: [{ op: 'clip.move',
      expect: { 'parent/clip:x::at': { state: 'present', value: 1 } } }] });
    expect(env.commits()[2].key).not.toBe(original.key);
    expect(env.current().config.clips[0].at).toBe(5);
    expect(rawTrack(env.projected.at(-1)!.canonicalDocument).label).toBe('First label');
    await recovered.dispose();
  });
  it('refuses synthetic or ambiguous track ownership and unprepared commands atomically', async () => {
    const raw = acceptedCommit({ revision_id: 'r0', publication_id: 'p0' },
      { revision_id: 'old', publication_id: 'old' }, { children: true }).data.canonical_document;
    const env = await environment(raw);
    const session = await env.mount();
    expect(() => captureTrackLabelEdit(session.trackLabelPort, env.current(), env.current().config.tracks[0].id)).toThrow();
    expect(() => session.trackLabelPort.submit({ command: { schema_version: 1, op: 'track.set', version: '1',
      select: 'parent/track:V1', args: { values: { label: 'Uncaptured' }, clear: [] } },
    preview: { version: 1, operations: [] } })).toThrow('not captured');
    expect(env.previews).not.toHaveBeenCalled();
    expect(env.commits()).toHaveLength(0);
    await session.dispose();
  });
  it.each(['project', 'timeline', 'publication', 'synthetic'] as const)('refuses a mismatched %s display basis', async (mismatch) => {
    const env = await environment();
    const session = await env.mount();
    const current = structuredClone(env.current());
    if (mismatch === 'project') current.head!.projectId = 'other-project';
    if (mismatch === 'timeline') current.head!.timelineId = 'other-timeline';
    if (mismatch === 'publication') delete current.head!.headPublicationId;
    if (mismatch === 'synthetic') {
      current.resolvedConfig.tracks[0].id = 'display-only';
      current.config.tracks[0].id = 'display-only';
    }
    expect(() => captureTrackLabelEdit(session.trackLabelPort, current, mismatch === 'synthetic' ? 'display-only' : 'V1')).toThrow();
    expect(env.previews).not.toHaveBeenCalled();
    expect(env.commits()).toHaveLength(0);
    await session.dispose();
  });
  it('refuses mixed previews atomically and keeps the original capture available', async () => {
    const env = await environment();
    const session = await env.mount();
    const captured = captureTrackLabelEdit(session.trackLabelPort, env.current(), 'V1');
    const args: TrackLabelArgs = { values: { label: 'Only label' }, clear: [] };
    const { command } = session.trackLabelPort.finish(captured.basis, args);
    expect(() => session.trackLabelPort.submit({ command, preview: { version: 1, operations: [
      { op: 'track.update', target: 'V1', payload: { label: 'Only label', muted: true } },
    ] } })).toThrow('label-only preview');
    expect(env.previews).not.toHaveBeenCalled();
    expect((await env.outboxes.list(scope))[0].intents).toHaveLength(0);
    submitTrackLabelEdit(captured, args);
    await session.flush();
    expect(env.commits()).toHaveLength(1);
    expect(env.commits()[0].body!.commands[0]).toEqual(command);
    await session.dispose();
  });
  it('refuses a typing capture invalidated by a newer local move without changing the pending request', async () => {
    const env = await environment();
    const session = await env.mount();
    const captured = captureTrackLabelEdit(session.trackLabelPort, env.current(), 'V1');
    env.setFault('lost');
    env.move(session, 5);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const original = structuredClone(env.commits()[0]);
    expect(() => submitTrackLabelEdit(captured, { values: { label: 'Kept input' }, clear: [] })).toThrow('Timeline changed');
    const [stored] = await env.outboxes.list(scope);
    expect(stored.intents).toHaveLength(1);
    expect(JSON.parse(stored.pending!.request.body)).toEqual(original.body);
    expect(stored.pending!.request.key).toBe(original.key);
    await session.retry();
    expect(env.commits()[1]).toEqual(original);
    await session.dispose();
  });
});

// HTTP and acceptance are fabricated by the unit fixture; browser/Runtime proof is a separate lane.
describe('explicit resolution in the same command session', () => {
  it('keeps the unknown-ACK barrier and offers only exact retry', async () => {
    const env = await environment();
    const session = await env.mount();
    env.setFault('lost');
    rename(session, env.current(), 'Mine');
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const original = structuredClone((await env.outboxes.list(scope))[0]);
    expect(session.getState()).toMatchObject({ canDiscardRejected: false, canReapplyLabel: false });
    await expect(session.useLatest()).rejects.toThrow('definitively rejected');
    await expect(session.keepLabelChanges()).rejects.toThrow('definitively rejected');
    expect((await env.outboxes.list(scope))[0]).toEqual(original);
    expect(env.commits()).toHaveLength(1);
    await session.retry();
    expect(env.commits()[1]).toEqual(env.commits()[0]);
    await session.dispose();
  });

  it.each<TrackLabelArgs>([
    { values: { label: 'Mine' }, clear: [] },
    { values: { label: '' }, clear: [] },
    { values: {}, clear: ['label'] },
  ])('authors a new explicit label intent %j, then reloads and retries it exactly', async (args) => {
    const env = await environment();
    const session = await env.mount();
    const captured = captureTrackLabelEdit(session.trackLabelPort, env.current(), 'V1');
    const remote = await env.external((raw) => { rawTrack(raw).label = 'Someone else'; });
    submitTrackLabelEdit(captured, args);
    await expect(session.flush()).rejects.toThrow('original capture');
    const [rejected] = await env.outboxes.list(scope);
    const original = structuredClone(env.commits()[0]);
    expect(session.getState()).toMatchObject({ canDiscardRejected: true, canReapplyLabel: true });
    session.observe(remote);
    await session.retry();
    expect(env.commits()).toEqual([original]);
    expect((await env.outboxes.list(scope))[0]).toEqual(rejected);
    expect(env.projected).toHaveLength(0);

    // A further external write must be guarded only by the explicit NEW intent.
    const fresh = await env.external((raw) => { rawTrack(raw).label = 'Latest label'; });
    env.setFault('lost');
    await session.keepLabelChanges();
    expect(session.getState().status).toBe('retry');
    const [kept] = await env.outboxes.list(scope);
    expect(kept.ownerId).toBe(rejected.ownerId);
    expect(kept.intents).toHaveLength(1);
    expect(kept.intents[0].id).not.toBe(rejected.intents[0].id);
    const replacement = structuredClone(env.commits()[1]);
    expect(replacement.key).not.toBe(original.key);
    expect(replacement.body).toMatchObject({ base_revision_id: fresh.head.revisionId,
      base_publication_id: fresh.head.publicationId, commands: [{ op: 'track.set', select: 'parent/track:V1', args,
        expect: { 'parent/track:V1::label': { state: 'present', value: 'Latest label' } } }] });
    expect(replacement.body!.commands[0].bindings).toEqual(original.body!.commands[0].bindings);
    expect(kept.intents[0].payload).toMatchObject({ before: { base_parent: { revision_id: fresh.head.revisionId } } });
    expect(env.commits()[0]).toEqual(original);
    expect(JSON.parse(rejected.pending!.request.body)).toEqual(original.body);
    expect(rejected.intents[0].payload).toMatchObject({ commands: [original.body!.commands[0]] });
    await session.dispose();

    const reopened = await env.mount(await env.provider.loadTimelineCommandBasis(scope.timelineId));
    await reopened.recover(kept.ownerId);
    expect(env.commits()[2]).toEqual(replacement);
    expect(reopened.getState().status).toBe('saved');
    const accepted = env.projected.at(-1)!.canonicalDocument;
    if ('label' in args.values) expect(rawTrack(accepted).label).toBe(args.values.label);
    else expect(rawTrack(accepted)).not.toHaveProperty('label');
    await reopened.undo();
    await reopened.flush();
    expect(rawTrack(env.projected.at(-1)!.canonicalDocument).label).toBe('Latest label');
    await reopened.dispose();
  });

  it('retains dependent B and unsupported operations until Use latest explicitly discards all displayed work', async () => {
    const env = await environment();
    const session = await env.mount();
    env.setFault('conflict');
    env.move(session, 5);
    rename(session, env.current(), 'Dependent B');
    await expect(session.flush()).rejects.toThrow('conflict');
    const [original] = await env.outboxes.list(scope);
    expect(original.intents).toHaveLength(2);
    expect(session.getState()).toMatchObject({ canDiscardRejected: true, canReapplyLabel: false });
    await expect(session.keepLabelChanges()).rejects.toThrow('no retained suffix');
    await session.retry();
    expect((await env.outboxes.list(scope))[0]).toEqual(original);
    expect(env.commits()).toHaveLength(1);
    env.setFault(null);
    const fresh = await env.external((raw) => { rawTrack(raw).label = 'Remote'; });
    await session.useLatest();
    expect(session.getState()).toMatchObject({ status: 'saved', canDiscardRejected: false, canReapplyLabel: false });
    const [cleared] = await env.outboxes.list(scope);
    expect(cleared.ownerId).toBe(original.ownerId);
    expect(cleared.intents).toEqual([]);
    expect(cleared.pending).toBeUndefined();
    expect(env.current().config.clips[0].at).toBe(1);
    expect(env.current().config.tracks[0].label).toBe('Remote');
    expect(env.current().head?.headPublicationId).toBe(fresh.head.publicationId);
    expect(env.commits()).toHaveLength(1);
    const next = captureTrackLabelEdit(session.trackLabelPort, env.current(), 'V1');
    submitTrackLabelEdit(next, { values: { label: 'Next' }, clear: [] });
    await session.flush();
    expect(env.commits()[1].body).toMatchObject({ base_revision_id: fresh.head.revisionId,
      base_publication_id: fresh.head.publicationId });
    await session.dispose();
    const reopened = await env.mount(await env.provider.loadTimelineCommandBasis(scope.timelineId));
    expect(reopened.getState().status).toBe('saved');
    expect(reopened.getState().recoverableOwners).toEqual([]);
    await reopened.dispose();
  });

  it('disables Keep for a rejected parent-label prefix with an original dependent suffix', async () => {
    const env = await environment();
    const session = await env.mount();
    env.setFault('conflict');
    rename(session, env.current(), 'A');
    env.move(session, 7);
    await expect(session.flush()).rejects.toThrow('conflict');
    const [original] = await env.outboxes.list(scope);
    expect(original.intents[1]).toMatchObject({ basis: { after: original.intents[0].id },
      payload: { commands: [{ op: 'clip.move', expect: { 'parent/clip:x::at': { state: 'present', value: 1 } } }] } });
    expect(session.getState()).toMatchObject({ canDiscardRejected: true, canReapplyLabel: false });
    await expect(session.keepLabelChanges()).rejects.toThrow('no retained suffix');
    expect((await env.outboxes.list(scope))[0]).toEqual(original);
    expect(env.commits()).toHaveLength(1);
    await session.dispose();
  });

  it.each(['deleted target', 'ambiguous owner', 'wrong scope', 'wrong revision', 'read failure', 'storage failure'] as const)(
    'preserves the original rejected request on %s', async (failure) => {
      const env = await environment();
      const session = await env.mount();
      env.setFault('conflict');
      rename(session, env.current(), 'Retain me');
      await expect(session.flush()).rejects.toThrow('conflict');
      const [original] = await env.outboxes.list(scope);
      const fresh = await env.external((raw) => {
        if (failure === 'deleted target') (raw.parent_revision.payload.config as { tracks: unknown[] }).tracks = [];
        if (failure === 'ambiguous owner') {
          const children = acceptedCommit({ revision_id: 'child-parent', publication_id: 'child-p' },
            { revision_id: 'old', publication_id: 'old' }, { children: true }).data.canonical_document;
          raw.parent_revision.payload.occurrences = children.parent_revision.payload.occurrences;
          raw.shot_revisions = children.shot_revisions;
          raw.internal_timeline_revisions = children.internal_timeline_revisions;
          raw.dependency_manifest = children.dependency_manifest;
        }
      });
      const load = vi.spyOn(env.provider, 'loadTimelineCommandBasis');
      if (failure === 'wrong scope') load.mockResolvedValueOnce({ ...fresh,
        canonicalDocument: { ...fresh.canonicalDocument, project_id: 'other-project' } });
      if (failure === 'wrong revision') load.mockResolvedValueOnce({ ...fresh, head: { ...fresh.head, revisionId: 'other' } });
      if (failure === 'read failure') load.mockRejectedValueOnce(new Error('cannot fetch closure'));
      const open = env.factory.open;
      if (failure === 'storage failure') env.factory.open = () => { throw new Error('disk full'); };
      await expect(session.keepLabelChanges()).rejects.toThrow();
      env.factory.open = open;
      load.mockRestore();
      expect((await env.outboxes.list(scope))[0]).toEqual(original);
      expect(env.commits()).toHaveLength(1);
      expect(env.projected).toHaveLength(0);
      expect(session.getState().canDiscardRejected).toBe(true);
      await session.dispose();
      const reopened = await env.mount();
      await reopened.recover(original.ownerId);
      expect((await env.outboxes.list(scope))[0].pending).toEqual(original.pending);
      await reopened.dispose();
    },
  );

  it.each(['keep', 'latest'] as const)('fences %s when dispose races the fresh read', async (action) => {
    const env = await environment();
    const session = await env.mount();
    env.setFault('conflict');
    rename(session, env.current(), 'Retain me');
    await expect(session.flush()).rejects.toThrow('conflict');
    const [original] = await env.outboxes.list(scope);
    let finish!: (basis: typeof env.initial) => void;
    const load = vi.spyOn(env.provider, 'loadTimelineCommandBasis').mockImplementationOnce(() =>
      new Promise((resolve) => { finish = resolve; }));
    const resolving = action === 'keep' ? session.keepLabelChanges() : session.useLatest();
    const refused = expect(resolving).rejects.toThrow(/closed|Stale/);
    await vi.waitFor(() => expect(load).toHaveBeenCalledOnce());
    await session.dispose();
    finish(env.initial);
    await refused;
    expect((await env.outboxes.list(scope))[0]).toEqual(original);
    expect(env.projected).toHaveLength(0);
    load.mockRestore();
  });
});
