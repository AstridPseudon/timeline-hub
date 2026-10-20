import { describe, expect, it, vi } from 'vitest';
import { acceptedCommit } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { captureClipMove, submitClipMove } from './semanticGestures.ts';
import { environment, scope, document } from './__tests__/commitSessionEnvironment.ts';
import { createTimelineCommandSession } from './commitSession.ts';
import type { OutboxRecord } from './commitOutbox.ts';
import type { EditCommand } from '@/integrations/runtime/timeline-commit-types.ts';

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
