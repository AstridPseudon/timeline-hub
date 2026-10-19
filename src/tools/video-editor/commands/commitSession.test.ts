import { describe, expect, it, vi } from 'vitest';
import { acceptedCommit } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { captureClipMove, submitClipMove } from './semanticGestures.ts';
import { environment, scope, document } from './__tests__/commitSessionEnvironment.ts';
import type { OutboxRecord } from './commitOutbox.ts';
import { captureClipMove as captureRawMove, finishClipMove } from './clipMoveCapture.ts';
import { authoringBundleFromDocument } from './authoringBundle.ts';

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
    expect(env.projections[0]).toEqual({ basis: env.initial, previews: env.previews.mock.calls.map(([patch]) => patch) });
    expect(env.commits()[1]).toEqual(original);
    const b = env.commits()[2];
    expect(b.body?.base_publication_id).toBe('p1');
    expect(b.body?.commands[0].expect?.['parent/clip:x::at']).toEqual({ state: 'present', value: 5 });
    await reopened.dispose();
  });
  it('recovers retained B at its original display pair after A ACK, keeping its exact guarded request at HA', async () => {
    const env = await environment();
    const session = await env.mount();
    env.setFault('lost');
    env.move(session, 5);
    env.move(session, 7);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const [original] = await env.outboxes.list(scope);
    const b = original.intents[1];
    await env.provider.undoTimeline({ projectId: scope.projectId, timelineId: scope.timelineId,
      headRevisionId: 'r1', headPublicationId: 'p1' }, ['p1'], 'independent-c');
    const c = await env.provider.loadTimelineCommandBasis(scope.timelineId);
    session.observe(c);
    await session.retry();
    expect(env.commits()[2]).toEqual(env.commits()[0]);
    expect(session.getState()).toMatchObject({ status: 'conflict', error: expect.stringContaining('expect') });
    const [rejected] = await env.outboxes.list(scope);
    expect(rejected.intents).toHaveLength(1);
    expect(rejected.intents[0]).toMatchObject({ id: b.id, payload: b.payload, basis: b.basis,
      readyBase: { revisionId: 'r1', publicationId: 'p1' } });
    expect(JSON.parse(rejected.pending!.request.body)).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p1',
      commands: (b.payload as { commands: unknown }).commands });
    expect(rejected.accepted?.head).toEqual({ revisionId: 'r1', publicationId: 'p1' });
    await session.dispose();
    const reopened = await env.mount(c);
    const count = env.commits().length;
    await reopened.recover(original.ownerId);
    expect(env.projections.at(-1)).toEqual({ basis: env.initial, previews: [env.previews.mock.calls[1][0]] });
    expect(reopened.getState()).toMatchObject({ status: 'conflict', error: session.getState().error, canUndo: false });
    await reopened.retry();
    await expect(reopened.flush()).rejects.toThrow(session.getState().error!);
    expect(env.commits()).toHaveLength(count);
    const [recovered] = await env.outboxes.list(scope);
    expect(recovered.intents).toEqual(rejected.intents);
    expect(recovered.pending).toEqual(rejected.pending);
    expect(recovered.accepted).toEqual(rejected.accepted);
    await reopened.dispose();
  });
  it.each(['conflict', 'refused', 'validation', 'authorization'] as const)(
    'preserves typed %s after recovery without resending a rejected head', async (fault) => {
      const env = await environment();
      const session = await env.mount();
      env.setFault(fault);
      env.move(session, 5);
      await vi.waitFor(() => expect(session.getState().status).toBe(fault === 'conflict' ? 'conflict' : 'error'));
      const error = session.getState().error;
      await session.dispose();
      // Retained heads also carry the typed rejection independently of the pending request.
      await editOwner(env, (record) => { delete record.pending; });
      const reopened = await env.mount();
      await reopened.recover(session.getState().ownerId!);
      expect(reopened.getState()).toMatchObject({ status: fault === 'conflict' ? 'conflict' : 'error', error, canUndo: false });
      await reopened.retry();
      expect(env.commits()).toHaveLength(1);
      expect(reopened.getState().error).toBe(error);
      await reopened.dispose();
    });
  it('recovers legacy work only from its stored direct head and matching original document', async () => {
    const env = await environment();
    const session = await env.mount();
    env.setFault('busy');
    env.move(session, 5);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    await session.dispose();
    await editOwner(env, (record) => {
      delete (record.intents[0].payload as Record<string, unknown>).displayBasis;
    });
    const reopened = await env.mount({ ...env.initial, head: { revisionId: 'r0', publicationId: 'new-publication' } });
    await reopened.recover(session.getState().ownerId!);
    expect(env.projections.at(-1)?.basis).toEqual({ head: env.initial.head, canonicalDocument: env.initial.canonicalDocument });
    expect(reopened.getState().status).toBe('retry');
    await reopened.dispose();
  });
  it.each(['missing dependent display basis', 'missing publication', 'mismatched revision'] as const)(
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
          const basis = payload.displayBasis as { head: { revisionId: string; publicationId?: string } };
          if (fault === 'missing publication') delete basis.head.publicationId;
          else basis.head.revisionId = 'another-revision';
        }
      });
      const [saved] = await env.outboxes.list(scope);
      const count = env.commits().length;
      const reopened = await env.mount(await env.provider.loadTimelineCommandBasis(scope.timelineId));
      await expect(reopened.recover(saved.ownerId)).rejects.toThrow('verified original display basis');
      expect(env.projections).toHaveLength(0);
      expect(env.commits()).toHaveLength(count);
      const [retained] = await env.outboxes.list(scope);
      expect(retained.intents).toEqual(saved.intents);
      expect(retained.pending).toEqual(saved.pending);
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
  it('keeps a newer publication C distinct from late A even when both share a content revision', async () => {
    const env = await environment();
    const session = await env.mount();
    env.setFault('lost');
    env.move(session, 5);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const a = await env.provider.loadTimelineCommandBasis(scope.timelineId);
    const { command } = finishClipMove(captureRawMove(await authoringBundleFromDocument(a.canonicalDocument), 'parent/clip:x'), 5);
    const c = await env.provider.commitTimeline({ api_version: 1, project_id: scope.projectId, timeline_id: scope.timelineId,
      base_revision_id: a.head.revisionId, base_publication_id: a.head.publicationId, commands: [command], source: { via: 'app' } }, 'independent-c');
    expect(c.accepted).toEqual({ revisionId: 'r1', publicationId: 'p2' });
    session.observe({ head: c.accepted, canonicalDocument: c.canonicalDocument, graph: c.graph });
    await session.retry();
    expect(env.commits()[2]).toEqual(env.commits()[0]);
    expect(env.projected.map((basis) => basis.head)).toEqual([c.accepted]);
    expect(await session.flush()).toEqual(c.accepted);
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
