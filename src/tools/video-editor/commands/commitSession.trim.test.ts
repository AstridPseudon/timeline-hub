import { describe, expect, it, vi } from 'vitest';
import { environment, trimDocument, scope } from './__tests__/commitSessionEnvironment.ts';
import { captureClipTrimEdit, submitClipTrimEdit } from './clipTrimGesture.ts';
import { authoringBundleFromDocument } from './authoringBundle.ts';
import { executeClipTrim } from './clipTrimCapture.ts';
import { fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';

describe('parent trim in the shared durable command session', () => {
  it('captures before gesture updates and sends one exact native source-seconds command', async () => {
    const raw = trimDocument();
    const env = await environment(raw);
    const session = await env.mount();
    const current = env.current();
    const captured = captureClipTrimEdit(session.clipTrimPort, current, 'x');
    const originalBasis = structuredClone(captured.basis);
    // A pointer preview changes display fields, never the raw begin basis.
    current.resolvedConfig.clips[0].from = 8;
    current.resolvedConfig.clips[0].hold = 100;
    const args = { in_s: 1, out_s: 5 };
    submitClipTrimEdit(captured, args);
    await session.flush();
    const native = executeClipTrim(await authoringBundleFromDocument(raw), {
      schema_version: 1, op: 'clip.trim', version: '1', select: 'parent/clip:x', args, intent: {},
    });
    expect(env.commits()).toHaveLength(1);
    expect(env.commits()[0].body!.commands).toEqual([native.command]);
    expect(captured.basis).toEqual(originalBasis);
    const accepted = env.projected.at(-1)!.canonicalDocument.parent_revision.payload;
    expect(accepted.clips).toEqual(native.bundle.parent.clips);
    expect(accepted.opaque).toEqual({ absent: null });
    expect(accepted.clips[0]).toMatchObject({ from: 1, to: 5, hold: 4, speed: 2,
      unknown: { keep: [null, false, 0] }, app: { astrid: { opaque: [null, false] } } });
    expect(env.previews).toHaveBeenCalledOnce();
    await session.undo();
    await session.flush();
    expect(env.commits()[1].body!.commands[0]).toMatchObject({ op: 'timeline.inverse', args: { publications: ['p1'] } });
    expect(env.projected.at(-1)!.canonicalDocument.parent_revision.payload).toEqual(raw.parent_revision.payload);
    await session.dispose();
  });
  it('queues move → trim with original claims, replays the exact request after reload, and undoes only trim', async () => {
    const env = await environment(trimDocument());
    const first = await env.mount();
    env.setFault('lost');
    env.move(first, 5);
    const captured = captureClipTrimEdit(first.clipTrimPort, env.current(), 'x');
    submitClipTrimEdit(captured, { in_s: 1, out_s: 5 });
    await vi.waitFor(() => expect(first.getState().status).toBe('retry'));
    const original = structuredClone(env.commits()[0]);
    const [stored] = await env.outboxes.list(scope);
    expect(stored.intents).toHaveLength(2);
    expect(stored.intents[1].basis).toEqual({ after: stored.intents[0].id });
    const trimPayload = structuredClone(stored.intents[1].payload);
    expect(trimPayload).toMatchObject({ commands: [{ op: 'clip.trim', args: { in_s: 1, out_s: 5 },
      expect: { 'parent/clip:x::from': { state: 'present', value: 2 } },
      reads: expect.arrayContaining([{ ref: 'parent/clip:x', path: ['at'], state: { state: 'present', value: 5 } }]) }],
    after: { parent: { clips: [{ at: 5, from: 1, to: 5, hold: 4, speed: 2 }, { id: 'other', at: 25 }] } } });
    const pending = structuredClone(stored.pending);
    await first.dispose();
    const reopened = await env.mount(await env.provider.loadTimelineCommandBasis('timeline-commit'));
    expect(reopened.getState().status).toBe('recovery');
    expect(env.commits()).toHaveLength(1);
    await reopened.recover(stored.ownerId);
    expect(env.commits()[1]).toEqual(original);
    expect(pending!.request.key).toBe(original.key);
    expect(JSON.parse(pending!.request.body)).toEqual(original.body);
    expect(env.commits()[2].body).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p1',
      commands: (trimPayload as { commands: unknown }).commands });
    expect(env.commits()[2].key).not.toBe(original.key);
    expect(env.current().config.clips[0]).toMatchObject({ at: 5, from: 1, to: 5, hold: 4, speed: 2 });
    await reopened.undo();
    await reopened.flush();
    expect(env.current().config.clips[0]).toMatchObject({ at: 5, from: 2, to: 6, hold: 17, speed: 2 });
    await reopened.dispose();
  });
  it('retains the original begin guards when a predecessor ACK arrives before finish', async () => {
    const env = await environment(trimDocument());
    const session = await env.mount();
    env.setFault('lost');
    env.move(session, 5);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const captured = captureClipTrimEdit(session.clipTrimPort, env.current(), 'x');
    const original = structuredClone(captured.basis);
    await session.retry();
    submitClipTrimEdit(captured, { out_s: 5 });
    await session.flush();
    expect(captured.basis).toEqual(original);
    expect(env.commits()[2].body).toMatchObject({ base_publication_id: 'p1', commands: [{ op: 'clip.trim',
      args: { in_s: null, out_s: 5 }, expect: { 'parent/clip:x::from': { state: 'present', value: 2 } } }] });
    expect(env.current().config.clips[0]).toMatchObject({ at: 5, from: 2, to: 5, hold: 3, speed: 2 });
    await session.dispose();
  });
  it('preserves disjoint observed data when finishing an older trim capture', async () => {
    const env = await environment(trimDocument());
    const session = await env.mount();
    const captured = captureClipTrimEdit(session.clipTrimPort, env.current(), 'x');
    const remote = await env.external((raw) => {
      raw.parent_revision.payload.opaque = { new: [null, false] };
      for (const clips of [raw.parent_revision.payload.clips,
        (raw.parent_revision.payload.config as { clips: Array<{ id: string; at: number }> }).clips]) {
        (clips as Array<{ id: string; at: number }>).find((clip) => clip.id === 'other')!.at = 29;
      }
    });
    session.observe(remote);
    await vi.waitFor(() => expect(env.current().head?.headRevisionId).toBe(remote.head.revisionId));
    submitClipTrimEdit(captured, { in_s: 1, out_s: 5 });
    await session.flush();
    const accepted = env.projected.at(-1)!.canonicalDocument.parent_revision.payload;
    expect(accepted.opaque).toEqual({ new: [null, false] });
    expect(accepted.clips[1]).toMatchObject({ id: 'other', at: 29 });
    expect(env.commits()[0].body!.commands[0].expect?.['parent/clip:x::from']).toEqual({ state: 'present', value: 2 });
    await session.dispose();
  });
  it('retains source endpoint input on an observed original-guard failure', async () => {
    const env = await environment(trimDocument());
    const session = await env.mount();
    const captured = captureClipTrimEdit(session.clipTrimPort, env.current(), 'x');
    const remote = await env.external((raw) => {
      (raw.parent_revision.payload.clips[0] as { from: number }).from = 3;
      (raw.parent_revision.payload.config as { clips: Array<{ from: number }> }).clips[0].from = 3;
    });
    session.observe(remote);
    await vi.waitFor(() => expect(env.current().head?.headRevisionId).toBe(remote.head.revisionId));
    const args = { in_s: 1, out_s: 5 };
    expect(() => submitClipTrimEdit(captured, args)).toThrow('original capture');
    expect(args).toEqual({ in_s: 1, out_s: 5 });
    expect(captured.basis.command).toMatchObject({ expect: { 'parent/clip:x::from': { state: 'present', value: 2 } } });
    expect(env.previews).not.toHaveBeenCalled();
    expect(env.commits()).toHaveLength(0);
    await session.dispose();
  });
  it('retains an unobserved source conflict durably without recapturing or retrying rejected work', async () => {
    const env = await environment(trimDocument());
    const session = await env.mount();
    const captured = captureClipTrimEdit(session.clipTrimPort, env.current(), 'x');
    await env.external((raw) => {
      (raw.parent_revision.payload.clips[0] as { from: number }).from = 3;
      (raw.parent_revision.payload.config as { clips: Array<{ from: number }> }).clips[0].from = 3;
    });
    submitClipTrimEdit(captured, { in_s: 1, out_s: 5 });
    await expect(session.flush()).rejects.toThrow('original capture');
    expect(session.getState().status).toBe('conflict');
    const [stored] = await env.outboxes.list(scope);
    expect(stored.intents[0].payload).toMatchObject({ commands: [{ op: 'clip.trim', args: { in_s: 1, out_s: 5 },
      expect: { 'parent/clip:x::from': { state: 'present', value: 2 } } }], preview: { source: 'clip.trim' } });
    await session.dispose();
    const recovered = await env.mount(await env.provider.loadTimelineCommandBasis('timeline-commit'));
    await recovered.recover(stored.ownerId);
    await recovered.retry();
    expect(recovered.getState().status).toBe('conflict');
    expect(env.commits()).toHaveLength(1);
    const [retained] = await env.outboxes.list(scope);
    expect(retained.intents).toEqual(stored.intents);
    expect(retained.pending).toEqual(stored.pending);
    await recovered.dispose();
  });
  it('drains a discrete trim into the existing outbox on close', async () => {
    const env = await environment(trimDocument());
    const first = await env.mount();
    submitClipTrimEdit(captureClipTrimEdit(first.clipTrimPort, env.current(), 'x'), { in_s: 1, out_s: 5 });
    await first.dispose();
    expect(env.commits()).toHaveLength(0);
    const [stored] = await env.outboxes.list(scope);
    expect(stored.intents).toHaveLength(1);
    expect(stored.intents[0].payload).toMatchObject({ commands: [{ op: 'clip.trim' }], preview: { source: 'clip.trim' } });
    const reopened = await env.mount();
    await reopened.recover(stored.ownerId);
    expect(env.commits()).toHaveLength(1);
    expect(env.current().config.clips[0]).toMatchObject({ from: 1, to: 5, hold: 4, speed: 2 });
    await reopened.dispose();
  });
  it('retains a local trim preview on IDB failure and retries the same command after storage recovers', async () => {
    const env = await environment(trimDocument());
    const session = await env.mount();
    const captured = captureClipTrimEdit(session.clipTrimPort, env.current(), 'x');
    const prepared = session.clipTrimPort.finish(captured.basis, { in_s: 1, out_s: 5 });
    const open = env.factory.open.bind(env.factory);
    env.factory.open = () => { throw new Error('disk full'); };
    session.clipTrimPort.submit(prepared);
    await vi.waitFor(() => expect(session.getState().status).toBe('error'));
    expect(session.getState()).toMatchObject({ error: expect.stringContaining('disk full'), canUndo: false });
    expect(env.previews).toHaveBeenCalledWith(prepared.preview);
    expect(env.commits()).toHaveLength(0);
    await expect(session.flush()).rejects.toThrow('disk full');
    expect(captured.basis.command).toMatchObject({ expect: { 'parent/clip:x::from': { state: 'present', value: 2 } } });
    env.factory.open = open;
    await session.retry();
    expect(env.commits()).toHaveLength(1);
    expect(env.commits()[0].body!.commands).toEqual([prepared.command]);
    expect(session.getState().status).toBe('saved');
    await session.dispose();
  });
  it.each(['project', 'timeline', 'publication', 'occurrence', 'mapped'] as const)('refuses unsupported %s capture without traffic', async (kind) => {
    const raw = trimDocument();
    if (kind === 'mapped') {
      (raw.parent_revision.payload.clips[0] as Record<string, unknown>).time_map = {};
      (raw.parent_revision.payload.config as { clips: unknown[] }).clips = structuredClone(raw.parent_revision.payload.clips as unknown[]);
      raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
    }
    const env = await environment(raw);
    const session = await env.mount();
    const current = structuredClone(env.current());
    if (kind === 'project') current.head!.projectId = 'other';
    if (kind === 'timeline') current.head!.timelineId = 'other';
    if (kind === 'publication') delete current.head!.headPublicationId;
    if (kind === 'occurrence') current.resolvedConfig.clips[0].app = { canonical: { occurrenceId: 'o', clipRef: 'occurrence:o/clip:x' } };
    expect(() => captureClipTrimEdit(session.clipTrimPort, current, 'x')).toThrow();
    expect(env.previews).not.toHaveBeenCalled();
    expect(env.commits()).toHaveLength(0);
    expect((await env.outboxes.list(scope))[0].intents).toHaveLength(0);
    await session.dispose();
  });
  it('refuses mixed previews without consuming the prepared trim', async () => {
    const env = await environment(trimDocument());
    const session = await env.mount();
    const captured = captureClipTrimEdit(session.clipTrimPort, env.current(), 'x');
    const prepared = session.clipTrimPort.finish(captured.basis, { in_s: 1, out_s: 5 });
    expect(() => session.clipTrimPort.submit({ ...prepared, preview: { ...prepared.preview, operations: [
      ...prepared.preview.operations, { op: 'clip.move', target: 'other', payload: { at: 99 } },
    ] } })).toThrow('native source-window preview');
    expect(env.previews).not.toHaveBeenCalled();
    session.clipTrimPort.submit(prepared);
    await session.flush();
    expect(env.commits()).toHaveLength(1);
    await session.dispose();
  });
});

describe('trim captured after an accepted prefix loses its ACK', () => {
  it('keeps B unsent behind exact A, recovers original guards, and targets only B for undo', async () => {
    const env = await environment(trimDocument());
    const first = await env.mount();
    env.setFault('lost');
    env.move(first, 5);
    await vi.waitFor(() => expect(first.getState().status).toBe('retry'));
    const [a] = await env.outboxes.list(scope);
    const wireA = structuredClone(env.commits()[0]);
    const acceptedA = await env.provider.loadTimelineCommandBasis(scope.timelineId);
    expect(acceptedA.head.publicationId).toBe('p1');
    const capture = vi.spyOn(first.clipTrimPort, 'capture');
    const finish = vi.spyOn(first.clipTrimPort, 'finish');
    const captured = captureClipTrimEdit(first.clipTrimPort, env.current(), 'x');
    submitClipTrimEdit(captured, { out_s: 5 });
    await vi.waitFor(async () => expect((await env.outboxes.list(scope))[0].intents).toHaveLength(2));
    const [queued] = await env.outboxes.list(scope);
    expect(env.commits()).toEqual([wireA]);
    expect(queued.pending).toEqual(a.pending);
    expect(queued.intents[1].basis).toEqual({ after: a.intents[0].id });
    expect(queued.intents[1].readyBase).toBeUndefined();
    const commandB = finish.mock.results[0].value.command;
    expect(commandB.reads).toEqual(expect.arrayContaining([
      { ref: 'parent/clip:x', path: ['from'], state: { state: 'present', value: 2 } },
      { ref: 'parent/clip:x', path: ['at'], state: { state: 'present', value: 5 } },
    ]));
    expect(env.current().head!.headPublicationId).toBe('p0');
    expect(env.current().config.clips.find((clip) => clip.id === 'x')!).toMatchObject({ at: 5, from: 2, to: 5, hold: 3, speed: 2 });
    await first.dispose();
    const reopened = await env.mount(acceptedA);
    expect(env.commits()).toEqual([wireA]);
    await reopened.recover(queued.ownerId);
    expect(env.commits()).toHaveLength(3);
    expect(env.commits()[1]).toEqual(wireA);
    expect(env.commits()[1].bodyText).toBe(a.pending!.request.body);
    expect(env.commits()[2].body).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p1', commands: [commandB] });
    expect(env.commits()[2].key).not.toBe(wireA.key);
    expect(capture).toHaveBeenCalledOnce();
    expect(finish).toHaveBeenCalledOnce();
    expect(env.current().config.clips.find((clip) => clip.id === 'x')!).toMatchObject({ at: 5, from: 2, to: 5, hold: 3, speed: 2 });
    await reopened.undo();
    await reopened.flush();
    expect(env.commits()[3].body!.commands[0]).toMatchObject({ op: 'timeline.inverse', args: { publications: ['p2'] } });
    expect(env.current().config.clips.find((clip) => clip.id === 'x')!).toMatchObject({ at: 5, from: 2, to: 6, hold: 17, speed: 2 });
    await reopened.dispose();
  });

  it.each([undefined, null, {}, { astrid: { for: 19 } }])('projects exact native app removal, including %j', async (app) => {
    const raw = trimDocument();
    for (const clips of [raw.parent_revision.payload.clips, (raw.parent_revision.payload.config as { clips: Array<Record<string, unknown>> }).clips]) {
      if (app === undefined) delete (clips[0] as Record<string, unknown>).app;
      else (clips[0] as Record<string, unknown>).app = structuredClone(app);
    }
    raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
    const env = await environment(raw);
    const session = await env.mount();
    submitClipTrimEdit(captureClipTrimEdit(session.clipTrimPort, env.current(), 'x'), { out_s: 5 });
    expect(env.current().config.clips.find((clip) => clip.id === 'x')!).not.toHaveProperty('app');
    expect(env.current().resolvedConfig.clips[0]).not.toHaveProperty('app');
    await session.flush();
    expect(env.current().config.clips.find((clip) => clip.id === 'x')!).not.toHaveProperty('app');
    await session.undo();
    await session.flush();
    if (app === undefined) expect(env.current().config.clips.find((clip) => clip.id === 'x')!).not.toHaveProperty('app');
    else expect(env.current().config.clips.find((clip) => clip.id === 'x')!.app).toEqual(app);
    await session.dispose();
  });
});
