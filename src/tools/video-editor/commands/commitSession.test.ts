import { describe, expect, it, vi } from 'vitest';
import { acceptedCommit } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { captureClipMove, submitClipMove } from './semanticGestures.ts';
import { environment, scope, document } from './__tests__/commitSessionEnvironment.ts';

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
