import { describe, expect, it, vi } from 'vitest';
import { acceptedCommit, fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import type { JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import type { TimelineData } from '../lib/timeline-data.ts';
import { createShotCompositionAdapter } from '../data/shotCompositionAdapter.ts';
import { projectCanonicalComposition } from '../data/shotCompositionProjection.ts';
import { captureClipParamsEdit, submitClipParamsEdit } from './clipParamsGesture.ts';
import { captureClipParams, finishClipParams, type ClipParamsArgs } from './clipParamsCapture.ts';
import { AuthoredState, type AuthoredBundle } from './clipMovePrimitives.ts';
import { environment, scope, document } from './__tests__/commitSessionEnvironment.ts';
import { authoringBundleFromDocument } from './authoringBundle.ts';

function withParams(params?: JSON) {
  const raw = document();
  for (const clips of [raw.parent_revision.payload.clips, raw.parent_revision.payload.config.clips]) {
    if (params !== undefined) (clips as Array<Record<string, unknown>>)[0].params = structuredClone(params);
  }
  raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
  return raw;
}
function rawClip(raw: ReturnType<typeof document>) {
  return (raw.parent_revision.payload.clips as Array<Record<string, JSON>>)[0];
}
function changeClips(raw: ReturnType<typeof document>, change: (clip: Record<string, JSON>) => void) {
  change(rawClip(raw));
  raw.parent_revision.payload.config.clips = structuredClone(raw.parent_revision.payload.clips);
}
function projectedDisplay(env: Awaited<ReturnType<typeof environment>>): TimelineData {
  const composition = createShotCompositionAdapter({ load: async () => env.initial.graph }).prepare(env.initial.graph);
  const { config } = projectCanonicalComposition(composition, { ...env.current().resolvedConfig,
    clips: structuredClone(env.initial.canonicalDocument.parent_revision.payload.clips) as TimelineData['config']['clips'],
  });
  return { ...env.current(), config, resolvedConfig: config };
}
const args: ClipParamsArgs = { values: { x: 2 }, clear: [] };
const clearOnly: ClipParamsArgs = { values: {}, clear: ['missing', 'literal.key', ''] };
const clearContainers = [undefined, null, {}, { opaque: { keep: [null, false, {}, []] }, 'a::b': '' }];

// Offline simulated acceptance exercises App's outbox. Actual Runtime acceptance
// follows the released Agent/Runtime pair and official client pin.
describe('clip params on the existing durable command session', () => {
  it.each([
    ['wrong project', { projectId: 'other-project' }],
    ['wrong parent', { parentDocumentId: 'other-timeline' }],
    ['wrong source shot', { shotId: 'other-shot' }],
    ['stale shot revision', { revisionId: 'old-shot-revision' }],
    ['stale internal revision', { internalTimelineRevisionId: 'old-internal-revision' }],
    ['wrong output identity', { outputIdentity: 'other-output' }],
    ['wrong owner', { ownerRef: 'occurrence:occ-1' }],
    ['wrong occurrence', { occurrenceId: 'occ-1' }],
    ['wrong clipRef', { clipRef: 'occurrence:occ-1/clip:child-title' }],
    ['wrong raw ID', { rawClipId: 'other-clip' }],
    ['missing raw target', { rawClipId: 'missing', clipRef: 'occurrence:occ-0/clip:missing' }],
    ['unaddressable binding', { clipRef: null }],
    ['missing binding', undefined],
    ['clipRef alone', { clipRef: 'occurrence:occ-0/clip:child-title' }],
  ] as const)('refuses projected %s before preview or outbox changes', async (name, forged) => {
    const raw = acceptedCommit({ revision_id: 'r0', publication_id: 'p0' },
      { revision_id: 'old', publication_id: 'old' }, { children: true }).data.canonical_document;
    const env = await environment(raw);
    const session = await env.mount();
    const current = projectedDisplay(env);
    const selected = current.resolvedConfig.clips.find((clip) => clip.id === 'occ-0:child-title')!;
    const canonical = forged === undefined ? undefined : name === 'clipRef alone'
      ? forged : { ...(selected.app!.canonical as object), ...forged };
    selected.app = { ...selected.app, canonical };
    const before = structuredClone(current);
    const outboxes = await env.outboxes.list(scope);
    expect(() => captureClipParamsEdit(session.clipParamsPort, current, selected.id)).toThrow();
    expect(current).toEqual(before);
    expect(await env.outboxes.list(scope)).toEqual(outboxes);
    expect(env.previews).not.toHaveBeenCalled();
    expect(env.commits()).toHaveLength(0);
    await session.dispose();
  });
  it('refuses a complete sibling identity attached to another projector output', async () => {
    const raw = acceptedCommit({ revision_id: 'r0', publication_id: 'p0' },
      { revision_id: 'old', publication_id: 'old' }, { children: true }).data.canonical_document;
    const env = await environment(raw);
    const session = await env.mount();
    const current = projectedDisplay(env);
    const selected = current.resolvedConfig.clips.find((clip) => clip.id === 'occ-0:child-title')!;
    const sibling = current.resolvedConfig.clips.find((clip) => clip.id === 'occ-1:child-title')!;
    selected.app = structuredClone(sibling.app);
    const before = structuredClone(current);
    const outboxes = await env.outboxes.list(scope);
    expect(() => captureClipParamsEdit(session.clipParamsPort, current, selected.id)).toThrow();
    expect(current).toEqual(before);
    expect(await env.outboxes.list(scope)).toEqual(outboxes);
    expect(env.previews).not.toHaveBeenCalled();
    expect(env.commits()).toHaveLength(0);
    await session.dispose();
  });
  it.each([
    [false, { clipRef: 'parent/clip:x' }],
    [false, null],
    [false, 'projected'],
    [true, undefined],
    [true, 'projected'],
  ] as const)('targets the exact raw parent (same child ID: %s, opaque canonical: %j)', async (collision, canonical) => {
    const raw = acceptedCommit({ revision_id: 'r0', publication_id: 'p0' },
      { revision_id: 'old', publication_id: 'old' }, { children: true }).data.canonical_document;
    const seed = await environment(raw);
    const projected = projectedDisplay(seed).resolvedConfig.clips.find((clip) => clip.id === 'occ-0:child-title')!;
    const parent = rawClip(raw);
    if (collision) parent.id = 'child-title';
    parent.params = { x: 1, opaque: [null, false] };
    parent.app = { keep: null, ...(canonical === undefined ? {} : {
      canonical: canonical === 'projected' ? structuredClone(projected.app!.canonical) as JSON : canonical,
    }) };
    raw.parent_revision.payload.config.clips = [structuredClone(parent)];
    raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
    const env = await environment(raw);
    const session = await env.mount();
    const current = projectedDisplay(env);
    const captured = captureClipParamsEdit(session.clipParamsPort, current, parent.id as string);
    const before = captured.basis.bundle as AuthoredBundle;
    const native = finishClipParams(captureClipParams(before, `parent/clip:${parent.id}`, args), args);
    submitClipParamsEdit(captured, args);
    await session.dispose();
    const [stored] = await env.outboxes.list(scope);
    const payload = stored.intents[0].payload as unknown as { commands: JSON[]; after: AuthoredBundle };
    expect(payload.commands).toEqual([native.command]);
    expect(payload.after).toEqual(native.bundle);
    expect(new AuthoredState(payload.after).entity(`parent/clip:${parent.id}`)).toEqual({ ...parent, params: { x: 2, opaque: [null, false] } });
    expect(payload.after.shots).toEqual(before.shots);
    expect(payload.after.placements).toEqual(before.placements);
    expect(env.previews).toHaveBeenCalledExactlyOnceWith({ version: 1, operations: [
      { op: 'clip.update', target: parent.id, payload: { params: { x: 2, opaque: [null, false] } } },
    ] });
    expect(env.commits()).toHaveLength(0);
  });
  it('refuses a parent/projected display collision even with a complete authored canonical identity', async () => {
    const raw = acceptedCommit({ revision_id: 'r0', publication_id: 'p0' },
      { revision_id: 'old', publication_id: 'old' }, { children: true }).data.canonical_document;
    const seed = await environment(raw);
    const projected = projectedDisplay(seed).resolvedConfig.clips.find((clip) => clip.id === 'occ-0:child-title')!;
    const parent = rawClip(raw);
    parent.id = projected.id;
    parent.app = structuredClone(projected.app) as JSON;
    raw.parent_revision.payload.config.clips = [structuredClone(parent)];
    raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
    const env = await environment(raw);
    const session = await env.mount();
    const current = projectedDisplay(env);
    expect(current.resolvedConfig.clips.filter((clip) => clip.id === parent.id)).toHaveLength(2);
    const before = structuredClone(current);
    const outboxes = await env.outboxes.list(scope);
    expect(() => captureClipParamsEdit(session.clipParamsPort, current, parent.id as string)).toThrow('unambiguous');
    expect(current).toEqual(before);
    expect(await env.outboxes.list(scope)).toEqual(outboxes);
    expect(env.previews).not.toHaveBeenCalled();
    expect(env.commits()).toHaveLength(0);
    await session.dispose();
  });
  it('stages exact native occurrence writes without changing the sibling or source', async () => {
    const raw = acceptedCommit({ revision_id: 'r0', publication_id: 'p0' },
      { revision_id: 'old', publication_id: 'old' }, { children: true }).data.canonical_document;
    const internal = raw.internal_timeline_revisions[0];
    (internal.payload.clips as Array<Record<string, JSON>>)[0].params = { x: 1, old: null, opaque: [] };
    internal.content_digest = fixtureDigest(internal.payload);
    raw.dependency_manifest.internal_timelines[0].content_digest = internal.content_digest;
    const env = await environment(raw);
    const session = await env.mount();
    const current = projectedDisplay(env);
    const captured = captureClipParamsEdit(session.clipParamsPort, current, 'occ-0:child-title');
    const edit = { values: { x: null }, clear: ['old'] };
    const before = captured.basis.bundle as AuthoredBundle;
    const native = finishClipParams(captureClipParams(before, 'occurrence:occ-0/clip:child-title', edit), edit);
    submitClipParamsEdit(captured, edit);
    await session.dispose();
    const [stored] = await env.outboxes.list(scope);
    const payload = stored.intents[0].payload as unknown as { commands: JSON[]; after: AuthoredBundle };
    expect(payload.commands).toEqual([native.command]);
    expect(payload.after).toEqual(native.bundle);
    expect(new AuthoredState(payload.after).entity('occurrence:occ-0/clip:child-title')!.params).toEqual({ x: null, opaque: [] });
    expect(new AuthoredState(payload.after).entity('occurrence:occ-1/clip:child-title')).toEqual(
      new AuthoredState(before).entity('occurrence:occ-1/clip:child-title'));
    expect(payload.after.shots['shot-1']).toEqual(before.shots['shot-1']);
    expect(env.previews).toHaveBeenCalledExactlyOnceWith({ version: 1, operations: [
      { op: 'clip.update', target: 'occ-0:child-title', payload: { params: { x: null, opaque: [] } } },
    ] });
    expect(env.commits()).toHaveLength(0);
  });
  it.each(clearContainers)('durably records unchanged clears on %j with no preview or fabricated container', async (params) => {
    const env = await environment(withParams(params));
    const session = await env.mount();
    const captured = captureClipParamsEdit(session.clipParamsPort, env.current(), 'x');
    const original = structuredClone(captured.basis);
    const native = finishClipParams(captureClipParams(captured.basis.bundle as AuthoredBundle, 'parent/clip:x', clearOnly), clearOnly);
    const finished = session.clipParamsPort.finish(captured.basis, clearOnly);
    expect(finished.command).toEqual(native.command);
    expect(finished.previewParams).toBeNull();
    expect(native.record.writes).toHaveLength(clearOnly.clear.length);
    expect(native.record.writes.every((write) => write.before.state === 'absent' && write.after.state === 'absent')).toBe(true);
    const fabricated = { version: 1 as const, operations: [{ op: 'clip.update' as const, target: 'x', payload: { params: {} } }] };
    expect(() => session.clipParamsPort.submit({ command: finished.command, preview: fabricated })).toThrow('params-only preview');
    submitClipParamsEdit(captured, clearOnly);
    await session.dispose();
    const [stored] = await env.outboxes.list(scope);
    const payload = stored.intents[0].payload as unknown as { before: AuthoredBundle; after: AuthoredBundle; commands: JSON[]; preview: JSON };
    expect(payload.commands).toEqual([native.command]);
    expect(payload.before).toEqual(captured.basis.bundle);
    expect(payload.after).toEqual(native.bundle);
    expect(payload.after).toEqual(payload.before);
    expect(payload.preview).toBeNull();
    expect(captured.basis).toEqual(original);
    expect(env.previews).not.toHaveBeenCalled();
    expect(env.commits()).toHaveLength(0);
    const reopened = await env.mount();
    await reopened.recover(stored.ownerId);
    await reopened.flush();
    expect(env.commits()).toHaveLength(1);
    expect(env.commits()[0].body!.commands).toEqual([native.command]);
    expect(rawClip(env.projected.at(-1)!.canonicalDocument)).toEqual(rawClip(env.initial.canonicalDocument));
    const [accepted] = await env.outboxes.list(scope);
    expect(accepted.intents).toHaveLength(0);
    expect(accepted.accepted!.head).toEqual({ revisionId: 'r0', publicationId: 'p1' });
    expect(reopened.getState()).toMatchObject({ status: 'saved', canUndo: true });
    expect(env.calls.filter((call) => call.method !== 'GET' && call.path !== '/v1/handshake')).toEqual(env.commits());
    await reopened.dispose();
  });
  it('clears literal object keys while retaining other params and native source claims', async () => {
    const env = await environment(withParams({ 'literal.key': null, '': [], opaque: { keep: false }, 'a::b': {} }));
    const session = await env.mount();
    const captured = captureClipParamsEdit(session.clipParamsPort, env.current(), 'x');
    const native = finishClipParams(captureClipParams(captured.basis.bundle as AuthoredBundle, 'parent/clip:x', clearOnly), clearOnly);
    submitClipParamsEdit(captured, clearOnly);
    await session.flush();
    expect(env.commits()[0].body!.commands).toEqual([native.command]);
    expect(rawClip(env.projected.at(-1)!.canonicalDocument).params).toEqual({ opaque: { keep: false }, 'a::b': {} });
    expect(env.previews).toHaveBeenCalledExactlyOnceWith({ version: 1, operations: [{ op: 'clip.update', target: 'x',
      payload: { params: { opaque: { keep: false }, 'a::b': {} } } }] });
    await session.dispose();
  });
  it('previews an emptied object distinctly from an unchanged absent/null container', async () => {
    const env = await environment(withParams({ missing: null }));
    const session = await env.mount();
    submitClipParamsEdit(captureClipParamsEdit(session.clipParamsPort, env.current(), 'x'), clearOnly);
    await session.flush();
    expect(rawClip(env.projected.at(-1)!.canonicalDocument).params).toEqual({});
    expect(env.previews).toHaveBeenCalledExactlyOnceWith({ version: 1, operations: [
      { op: 'clip.update', target: 'x', payload: { params: {} } },
    ] });
    await session.dispose();
  });
  it.each([undefined, null, {}])('guards clear-only %j captures against changed leaves, containers and identity', async (params) => {
    // Native reads the whole container only when it is absent/null.
    const changes = ['leaf', 'type', 'asset', 'deleted'];
    if (params === undefined || params === null) changes.push('container');
    for (const change of changes) {
      const env = await environment(withParams(params));
      const session = await env.mount();
      const captured = captureClipParamsEdit(session.clipParamsPort, env.current(), 'x');
      const original = structuredClone(captured.basis);
      const remote = await env.external((raw) => {
        if (change === 'deleted') {
          raw.parent_revision.payload.clips = [];
          raw.parent_revision.payload.config.clips = [];
        } else changeClips(raw, (clip) => {
          if (change === 'leaf') clip.params = { missing: null };
          if (change === 'container') {
            if (params === undefined) clip.params = null;
            else if (params === null) delete clip.params;
          }
          if (change === 'type') clip.clipType = 'audio';
          if (change === 'asset') clip.asset = 'other';
        });
      });
      session.observe(remote);
      await vi.waitFor(() => expect(env.current().head!.headRevisionId).toBe(remote.head.revisionId));
      expect(() => submitClipParamsEdit(captured, clearOnly)).toThrow();
      expect(captured.basis).toEqual(original);
      expect(env.previews).not.toHaveBeenCalled();
      expect(env.commits()).toHaveLength(0);
      expect((await env.outboxes.list(scope))[0].intents).toHaveLength(0);
      await session.dispose();
    }
  });
  it.each([undefined, null, {}])('rebases a clear-only %j capture over disjoint changes using its original claims', async (params) => {
    const env = await environment(withParams(params));
    const session = await env.mount();
    const captured = captureClipParamsEdit(session.clipParamsPort, env.current(), 'x');
    const native = finishClipParams(captureClipParams(captured.basis.bundle as AuthoredBundle, 'parent/clip:x', clearOnly), clearOnly);
    const remote = await env.external((raw) => {
      changeClips(raw, (clip) => {
        clip.at = 8;
        clip.text = { content: 'remote' };
        if (params !== undefined && params !== null) (clip.params as Record<string, JSON>).opaque = [null, false];
      });
      raw.parent_revision.payload.config.x_remote = { keep: false };
      (raw.parent_revision.payload.clips as JSON[]).push({ id: 'other', at: 20, hold: 1, track: 'V1' });
      raw.parent_revision.payload.config.clips = structuredClone(raw.parent_revision.payload.clips);
    });
    session.observe(remote);
    await vi.waitFor(() => expect(env.current().head!.headRevisionId).toBe(remote.head.revisionId));
    submitClipParamsEdit(captured, clearOnly);
    await session.flush();
    expect(env.commits()[0].body).toMatchObject({ base_revision_id: 'r0', base_publication_id: 'p0', commands: [native.command] });
    expect(env.projected.at(-1)!.canonicalDocument.parent_revision.payload).toEqual(remote.canonicalDocument.parent_revision.payload);
    expect(env.previews).not.toHaveBeenCalled();
    await session.dispose();
  });
  it.each([undefined, null, {}])('keeps move → unchanged clear on %j through lost ACK and reload', async (params) => {
    const env = await environment(withParams(params));
    const session = await env.mount();
    env.setFault('lost');
    env.move(session, 5);
    const captured = captureClipParamsEdit(session.clipParamsPort, env.current(), 'x');
    const native = finishClipParams(captureClipParams(captured.basis.bundle as AuthoredBundle, 'parent/clip:x', clearOnly), clearOnly);
    submitClipParamsEdit(captured, clearOnly);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const request = structuredClone(env.commits()[0]);
    await session.dispose();
    const [stored] = await env.outboxes.list(scope);
    expect(stored.intents).toHaveLength(2);
    expect(stored.intents[1].basis).toEqual({ after: stored.intents[0].id });
    expect(stored.intents[1].payload).toMatchObject({ commands: [native.command], preview: null });
    const reopened = await env.mount(await env.provider.loadTimelineCommandBasis(scope.timelineId));
    await reopened.recover(stored.ownerId);
    await reopened.flush();
    expect(env.commits()).toHaveLength(3);
    expect(env.commits()[1]).toEqual(request);
    expect(env.commits()[2].key).not.toBe(request.key);
    expect(env.commits()[2].body).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p1', commands: [native.command] });
    expect(rawClip(env.projected.at(-1)!.canonicalDocument)).toEqual(new AuthoredState(native.bundle).entity('parent/clip:x'));
    expect((await env.outboxes.list(scope))[0].accepted!.head).toEqual({ revisionId: 'r1', publicationId: 'p2' });
    // Only the move needed an immediate local preview.
    expect(env.previews).toHaveBeenCalledOnce();
    await reopened.dispose();
  });
  it.each([undefined, null, {}])('retries the exact unchanged clear on %j before its queued move after reload', async (params) => {
    const env = await environment(withParams(params));
    const session = await env.mount();
    env.setFault('lost');
    submitClipParamsEdit(captureClipParamsEdit(session.clipParamsPort, env.current(), 'x'), clearOnly);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const request = structuredClone(env.commits()[0]);
    expect(env.previews).not.toHaveBeenCalled();
    env.move(session, 5);
    await session.dispose();
    const [stored] = await env.outboxes.list(scope);
    expect(stored.pending!.request.key).toBe(request.key);
    expect(JSON.parse(stored.pending!.request.body)).toEqual(request.body);
    expect(stored.intents[0].payload).toMatchObject({ preview: null });
    const reopened = await env.mount(await env.provider.loadTimelineCommandBasis(scope.timelineId));
    await reopened.recover(stored.ownerId);
    await reopened.flush();
    expect(env.commits()).toHaveLength(3);
    expect(env.commits()[1]).toEqual(request);
    expect(env.commits()[2].body).toMatchObject({ base_revision_id: 'r0', base_publication_id: 'p1', commands: [{ op: 'clip.move' }] });
    const after = (stored.intents[1].payload as unknown as { after: AuthoredBundle }).after;
    expect(rawClip(env.projected.at(-1)!.canonicalDocument)).toEqual(new AuthoredState(after).entity('parent/clip:x'));
    await reopened.dispose();
  });
  it.each([undefined, null, {}])('retains an unchanged clear draft on %j honestly when durable storage fails', async (params) => {
    const env = await environment(withParams(params));
    const session = await env.mount();
    const captured = captureClipParamsEdit(session.clipParamsPort, env.current(), 'x');
    const native = finishClipParams(captureClipParams(captured.basis.bundle as AuthoredBundle, 'parent/clip:x', clearOnly), clearOnly);
    const open = env.factory.open.bind(env.factory);
    env.factory.open = () => { throw new Error('disk full'); };
    submitClipParamsEdit(captured, clearOnly);
    await vi.waitFor(() => expect(session.getState().status).toBe('error'));
    await expect(session.flush()).rejects.toThrow('disk full');
    expect(session.getState().canUndo).toBe(false);
    expect(env.previews).not.toHaveBeenCalled();
    expect(env.commits()).toHaveLength(0);
    env.factory.open = open;
    await session.retry();
    expect(env.commits()).toHaveLength(1);
    expect(env.commits()[0].body!.commands).toEqual([native.command]);
    expect(rawClip(env.projected.at(-1)!.canonicalDocument)).toEqual(rawClip(env.initial.canonicalDocument));
    expect(session.getState().status).toBe('saved');
    await session.dispose();
  });
  it.each([undefined, null, {}])('retains the original clear-only %j draft on an unobserved relevant change', async (params) => {
    const env = await environment(withParams(params));
    const session = await env.mount();
    const captured = captureClipParamsEdit(session.clipParamsPort, env.current(), 'x');
    await env.external((raw) => { changeClips(raw, (clip) => { clip.params = { missing: null }; }); });
    submitClipParamsEdit(captured, clearOnly);
    await expect(session.flush()).rejects.toThrow('original capture');
    expect(session.getState().status).toBe('conflict');
    const [stored] = await env.outboxes.list(scope);
    expect(stored.intents[0].payload).toMatchObject({ commands: [{ args: clearOnly,
      expect: { 'parent/clip:x::params.missing': { state: 'absent' } } }], preview: null });
    expect(stored.pending!.outcome!.kind).toBe('rejected');
    expect(env.previews).not.toHaveBeenCalled();
    await session.dispose();
  });
  it.each([undefined, null, {}])('stages exact native occurrence clears on %j without changing its sibling or source', async (params) => {
    const raw = acceptedCommit({ revision_id: 'r0', publication_id: 'p0' },
      { revision_id: 'old', publication_id: 'old' }, { children: true }).data.canonical_document;
    const internal = raw.internal_timeline_revisions[0];
    if (params !== undefined) (internal.payload.clips as Array<Record<string, JSON>>)[0].params = structuredClone(params);
    internal.content_digest = fixtureDigest(internal.payload);
    raw.dependency_manifest.internal_timelines[0].content_digest = internal.content_digest;
    const env = await environment(raw);
    const session = await env.mount();
    const authored = await authoringBundleFromDocument(raw);
    const occurrence = authored.placements[0].occurrence_id;
    const ownerRef = `occurrence:${occurrence}`;
    const clipId = (new AuthoredState(authored).config(ownerRef).clips as Array<{ id: string }>)[0].id;
    const displayId = `${occurrence}:${clipId}`;
    const select = `${ownerRef}/clip:${clipId}`;
    const current = projectedDisplay(env);
    const captured = captureClipParamsEdit(session.clipParamsPort, current, displayId);
    const native = finishClipParams(captureClipParams(captured.basis.bundle as AuthoredBundle, select, clearOnly), clearOnly);
    submitClipParamsEdit(captured, clearOnly);
    await session.dispose();
    const [stored] = await env.outboxes.list(scope);
    expect(stored.intents[0].payload).toMatchObject({ commands: [native.command], before: authored, after: native.bundle, preview: null });
    expect(native.bundle).toEqual(authored);
    expect(env.previews).not.toHaveBeenCalled();
    expect(env.commits()).toHaveLength(0);
  });
  it.each([undefined, null, {}])('preserves original container presence %j and native claims', async (params) => {
    const env = await environment(withParams(params));
    const session = await env.mount();
    const captured = captureClipParamsEdit(session.clipParamsPort, env.current(), 'x');
    const original = structuredClone(captured.basis);
    const edit = { values: { 'dot.key': null, 'a::b': [], 'x[y]': false, '': {} }, clear: ['old'] };
    const native = finishClipParams(captureClipParams(captured.basis.bundle as AuthoredBundle, 'parent/clip:x', edit), edit);
    submitClipParamsEdit(captured, edit);
    await session.flush();
    expect(env.commits()[0].body!.commands[0]).toEqual(native.command);
    expect(captured.basis).toEqual(original);
    expect(rawClip(env.projected.at(-1)!.canonicalDocument).params).toEqual(edit.values);
    expect(rawClip(env.projected.at(-1)!.canonicalDocument).text).toEqual({ content: 'keep' });
    expect(env.previews).toHaveBeenCalledExactlyOnceWith({ version: 1, operations: [
      { op: 'clip.update', target: 'x', payload: { params: edit.values } },
    ] });
    await session.undo();
    await session.flush();
    const restored = rawClip(env.projected.at(-1)!.canonicalDocument);
    if (params === undefined) expect(restored).not.toHaveProperty('params');
    else expect(restored.params).toEqual(params);
    await session.dispose();
  });
  it('keeps null, absent, clear and opaque keys distinct without sending a whole params map', async () => {
    const env = await environment(withParams({ x: 1, old: null, opaque: { keep: [false, {}, ''] } }));
    const session = await env.mount();
    const captured = captureClipParamsEdit(session.clipParamsPort, env.current(), 'x');
    submitClipParamsEdit(captured, { values: { x: null }, clear: ['old', 'missing'] });
    await session.flush();
    const command = env.commits()[0].body!.commands[0];
    expect(command.args).toEqual({ values: { x: null }, clear: ['old', 'missing'] });
    expect(command.expect).toEqual({ 'parent/clip:x::params.x': { state: 'present', value: 1 },
      'parent/clip:x::params.old': { state: 'present', value: null }, 'parent/clip:x::params.missing': { state: 'absent' } });
    expect(rawClip(env.projected.at(-1)!.canonicalDocument).params).toEqual({ x: null, opaque: { keep: [false, {}, ''] } });
    await session.dispose();
  });
  it.each(['leaf', 'type', 'asset', 'deleted', 'container'])(
    'refuses an observed relevant %s change against the original snapshot, retaining input', async (change) => {
      const env = await environment(withParams({ x: 1, y: 1 }));
      const session = await env.mount();
      const captured = captureClipParamsEdit(session.clipParamsPort, env.current(), 'x');
      const original = structuredClone(captured.basis);
      const remote = await env.external((raw) => {
        if (change === 'deleted') {
          raw.parent_revision.payload.clips = [];
          raw.parent_revision.payload.config.clips = [];
        } else changeClips(raw, (clip) => {
          if (change === 'leaf') (clip.params as Record<string, JSON>).x = 9;
          if (change === 'type') clip.clipType = 'audio';
          if (change === 'asset') clip.asset = 'different-asset';
          if (change === 'container') clip.params = null;
        });
      });
      session.observe(remote);
      await vi.waitFor(() => expect(env.current().head!.headRevisionId).toBe(remote.head.revisionId));
      expect(() => submitClipParamsEdit(captured, args)).toThrow();
      expect(captured.basis).toEqual(original);
      expect(args).toEqual({ values: { x: 2 }, clear: [] });
      expect(env.previews).not.toHaveBeenCalled();
      expect(env.commits()).toHaveLength(0);
      expect((await env.outboxes.list(scope))[0].intents).toHaveLength(0);
      await session.dispose();
    },
  );
  it('stages original writes onto disjoint remote params, rows and metadata without overwriting them', async () => {
    const env = await environment(withParams({ x: 1, y: null, opaque: [] }));
    const session = await env.mount();
    const captured = captureClipParamsEdit(session.clipParamsPort, env.current(), 'x');
    const remote = await env.external((raw) => {
      changeClips(raw, (clip) => { (clip.params as Record<string, JSON>).y = { remote: false }; clip.at = 8; });
      (raw.parent_revision.payload.clips as JSON[]).push({ id: 'other', track: 'V1', at: 20, hold: 1, params: { untouched: null } });
      raw.parent_revision.payload.config.clips = structuredClone(raw.parent_revision.payload.clips);
      raw.parent_revision.payload.config.x_remote = { keep: [null, false] };
    });
    session.observe(remote);
    await vi.waitFor(() => expect(env.current().head!.headRevisionId).toBe(remote.head.revisionId));
    submitClipParamsEdit(captured, args);
    await session.dispose();
    const [stored] = await env.outboxes.list(scope);
    const payload = stored.intents[0].payload as unknown as { before: AuthoredBundle; after: AuthoredBundle; commands: unknown[] };
    expect(payload.commands[0]).toMatchObject({ expect: { 'parent/clip:x::params.x': { state: 'present', value: 1 } } });
    const next = new AuthoredState(payload.after).entity('parent/clip:x')!;
    expect(next.params).toEqual({ x: 2, y: { remote: false }, opaque: [] });
    expect(next.at).toBe(8);
    expect(payload.after.parent.clips).toEqual((payload.after.parent.config as Record<string, JSON>).clips);
    expect((payload.after.parent.clips as JSON[])[1]).toEqual((payload.before.parent.clips as JSON[])[1]);
    expect((payload.after.parent.config as Record<string, JSON>).x_remote).toEqual({ keep: [null, false] });
    expect(env.previews.mock.calls[0][0].operations[0].payload.params).toEqual(next.params);
    expect(env.commits()).toHaveLength(0);
    const reopened = await env.mount(remote);
    await reopened.recover(stored.ownerId);
    expect(rawClip(env.projected.at(-1)!.canonicalDocument).params).toEqual(next.params);
    await reopened.dispose();
  });
  it('keeps queued move → params, original guards and exact retry identity through reload', async () => {
    const env = await environment(withParams({ x: 1, opaque: null }));
    const session = await env.mount();
    env.setFault('lost');
    env.move(session, 5);
    submitClipParamsEdit(captureClipParamsEdit(session.clipParamsPort, env.current(), 'x'), args);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const original = structuredClone(env.commits()[0]);
    await session.dispose();
    const [stored] = await env.outboxes.list(scope);
    expect(stored.intents).toHaveLength(2);
    expect(stored.intents[1].basis).toEqual({ after: stored.intents[0].id });
    expect(stored.intents[1].payload).toMatchObject({ commands: [{ op: 'clip.set-params',
      expect: { 'parent/clip:x::params.x': { state: 'present', value: 1 } } }], after: { parent: { clips: [{ at: 5, params: { x: 2 } }] } } });
    const reopened = await env.mount(await env.provider.loadTimelineCommandBasis(scope.timelineId));
    expect(reopened.getState().status).toBe('recovery');
    await reopened.recover(stored.ownerId);
    expect(env.commits()[1]).toEqual(original);
    expect(env.commits()[2].key).not.toBe(original.key);
    expect(env.commits()[2].body).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p1',
      commands: (stored.intents[1].payload as { commands: JSON }).commands });
    expect(env.current().config.clips[0]).toMatchObject({ at: 5, params: { x: 2, opaque: null } });
    await reopened.undo();
    await reopened.flush();
    expect(env.current().config.clips[0]).toMatchObject({ at: 5, params: { x: 1, opaque: null } });
    await reopened.dispose();
  });
  it('does not recapture after the predecessor ACK advances the raw closure', async () => {
    const env = await environment(withParams({ x: 1 }));
    const session = await env.mount();
    env.setFault('lost');
    env.move(session, 5);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const captured = captureClipParamsEdit(session.clipParamsPort, env.current(), 'x');
    const original = structuredClone(captured.basis);
    await session.retry();
    submitClipParamsEdit(captured, args);
    await session.flush();
    expect(captured.basis).toEqual(original);
    expect(env.commits()[2].body).toMatchObject({ base_publication_id: 'p1', commands: [{ op: 'clip.set-params',
      expect: { 'parent/clip:x::params.x': { state: 'present', value: 1 } } }] });
    expect(env.current().config.clips[0]).toMatchObject({ at: 5, params: { x: 2 } });
    await session.dispose();
  });
  it('retries a pending params request exactly before a newer local move after reload', async () => {
    const env = await environment(withParams({ x: 1 }));
    const session = await env.mount();
    env.setFault('lost');
    submitClipParamsEdit(captureClipParamsEdit(session.clipParamsPort, env.current(), 'x'), args);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const original = structuredClone(env.commits()[0]);
    env.move(session, 5);
    await session.dispose();
    const [stored] = await env.outboxes.list(scope);
    expect(stored.pending!.request.key).toBe(original.key);
    expect(JSON.parse(stored.pending!.request.body)).toEqual(original.body);
    const reopened = await env.mount(await env.provider.loadTimelineCommandBasis(scope.timelineId));
    await reopened.recover(stored.ownerId);
    expect(env.commits()[1]).toEqual(original);
    expect(env.commits()[2].body).toMatchObject({ base_publication_id: 'p1', commands: [{ op: 'clip.move' }] });
    expect(env.current().config.clips[0]).toMatchObject({ at: 5, params: { x: 2 } });
    await reopened.dispose();
  });
  it('keeps an unobserved relevant change as a typed conflict with the original draft retained', async () => {
    const env = await environment(withParams({ x: 1, y: null }));
    const session = await env.mount();
    const captured = captureClipParamsEdit(session.clipParamsPort, env.current(), 'x');
    await env.external((raw) => { changeClips(raw, (clip) => { (clip.params as Record<string, JSON>).x = 9; }); });
    submitClipParamsEdit(captured, args);
    await expect(session.flush()).rejects.toThrow('original capture');
    expect(session.getState().status).toBe('conflict');
    const [stored] = await env.outboxes.list(scope);
    expect(stored.intents[0].payload).toMatchObject({ commands: [{ args, expect: {
      'parent/clip:x::params.x': { state: 'present', value: 1 },
    } }], preview: { operations: [{ payload: { params: { x: 2, y: null } } }] } });
    expect(stored.pending!.outcome!.kind).toBe('rejected');
    await session.dispose();
  });
  it('keeps submitted bytes immutable and drains them without a request on close', async () => {
    const env = await environment(withParams({ x: 1 }));
    const session = await env.mount();
    const captured = captureClipParamsEdit(session.clipParamsPort, env.current(), 'x');
    const { command, previewParams } = session.clipParamsPort.finish(captured.basis, args);
    expect(Object.isFrozen(command.args)).toBe(true);
    const preview = { version: 1 as const, operations: [{ op: 'clip.update' as const, target: 'x', payload: { params: previewParams } }] };
    session.clipParamsPort.submit({ command, preview });
    previewParams!.x = 99;
    preview.operations[0].target = 'other';
    await session.dispose();
    const [stored] = await env.outboxes.list(scope);
    expect(stored.intents[0].payload).toMatchObject({ commands: [{ args }], preview: {
      operations: [{ op: 'clip.update', target: 'x', payload: { params: { x: 2 } } }],
    } });
    expect(env.commits()).toHaveLength(0);
    expect(() => session.clipParamsPort.finish(captured.basis, args)).toThrow('unavailable');
  });
  it('retains the params draft and sends nothing on storage failure, then retries the durable append', async () => {
    const env = await environment(withParams({ x: 1 }));
    const session = await env.mount();
    const open = env.factory.open.bind(env.factory);
    env.factory.open = () => { throw new Error('disk full'); };
    submitClipParamsEdit(captureClipParamsEdit(session.clipParamsPort, env.current(), 'x'), args);
    await vi.waitFor(() => expect(session.getState().status).toBe('error'));
    expect(env.previews).toHaveBeenCalledOnce();
    expect(env.commits()).toHaveLength(0);
    await expect(session.flush()).rejects.toThrow('disk full');
    env.factory.open = open;
    await session.retry();
    expect(env.current().config.clips[0].params).toEqual({ x: 2 });
    await session.dispose();
  });
  it('refuses mixed or forged previews and stale prepared commands without appending', async () => {
    const env = await environment(withParams({ x: 1 }));
    const session = await env.mount();
    const captured = captureClipParamsEdit(session.clipParamsPort, env.current(), 'x');
    const { command, previewParams } = session.clipParamsPort.finish(captured.basis, args);
    expect(() => session.clipParamsPort.submit({ command, preview: null })).toThrow('params-only preview');
    for (const payload of [{ params: previewParams, hold: 100 }, { params: { x: 99 } }]) {
      expect(() => session.clipParamsPort.submit({ command, preview: { version: 1, operations: [
        { op: 'clip.update', target: 'x', payload },
      ] } })).toThrow('params-only preview');
    }
    expect(env.previews).not.toHaveBeenCalled();
    expect((await env.outboxes.list(scope))[0].intents).toHaveLength(0);
    const remote = await env.external((raw) => { changeClips(raw, (clip) => { clip.at = 9; }); });
    session.observe(remote);
    await vi.waitFor(() => expect(env.current().head!.headRevisionId).toBe(remote.head.revisionId));
    expect(() => session.clipParamsPort.submit({ command, preview: { version: 1, operations: [
      { op: 'clip.update', target: 'x', payload: { params: previewParams } },
    ] } })).toThrow('not captured');
    expect(env.commits()).toHaveLength(0);
    await session.dispose();
  });
  it.each(['project', 'timeline', 'revision', 'publication', 'duplicate', 'legacy', 'synthetic', 'canonical'])(
    'refuses invalid %s display ownership before preview', async (fault) => {
      const env = await environment();
      const session = await env.mount();
      const current = structuredClone(env.current());
      let clipId = 'x';
      if (fault === 'project') current.head!.projectId = 'other';
      if (fault === 'timeline') current.head!.timelineId = 'other';
      if (fault === 'revision') current.head!.headRevisionId = 'other';
      if (fault === 'publication') delete current.head!.headPublicationId;
      if (fault === 'duplicate') current.resolvedConfig.clips.push(current.resolvedConfig.clips[0]);
      if (fault === 'legacy') current.config.pinnedShotGroups = [{ clipIds: ['x'] }] as never;
      if (fault === 'synthetic') { clipId = 'display-only'; current.resolvedConfig.clips[0].id = clipId; }
      if (fault === 'canonical') {
        clipId = 'display-only';
        current.resolvedConfig.clips[0].id = clipId;
        current.resolvedConfig.clips[0].app = { canonical: { clipRef: 'parent/clip:x' } };
      }
      expect(() => captureClipParamsEdit(session.clipParamsPort, current, clipId)).toThrow();
      expect(env.previews).not.toHaveBeenCalled();
      expect(env.commits()).toHaveLength(0);
      await session.dispose();
    },
  );
  it('uses an existing validated occurrence clipRef and refuses inferred or forged owners', async () => {
    const raw = acceptedCommit({ revision_id: 'r0', publication_id: 'p0' },
      { revision_id: 'old', publication_id: 'old' }, { children: true }).data.canonical_document;
    const env = await environment(raw);
    const session = await env.mount();
    const authored = await authoringBundleFromDocument(raw);
    const occurrence = authored.placements[0].occurrence_id;
    const ownerRef = `occurrence:${occurrence}`;
    const config = new AuthoredState(authored).config(ownerRef);
    const clipId = (config.clips as Array<{ id: string }>)[0].id;
    const displayId = `${occurrence}:${clipId}`;
    const current = projectedDisplay(env);
    const selected = current.resolvedConfig.clips.find((clip) => clip.id === displayId)!;
    const captured = captureClipParamsEdit(session.clipParamsPort, current, displayId);
    const prepared = session.clipParamsPort.finish(captured.basis, args);
    expect(prepared.command).toMatchObject({ select: `${ownerRef}/clip:${clipId}`, bindings: { 'scalar.owner': ownerRef } });
    expect(prepared.command.reads).toContainEqual({ ref: ownerRef, path: ['occurrence_id'], state: { state: 'present', value: occurrence } });
    for (const canonical of [undefined, { clipRef: null }, { occurrenceId: 'other', rawClipId: clipId, ownerRef, clipRef: `${ownerRef}/clip:${clipId}` }]) {
      selected.app = { canonical } as never;
      expect(() => captureClipParamsEdit(session.clipParamsPort, current, displayId)).toThrow();
    }
    // A raw child ID alone never gives permission to infer its occurrence.
    selected.id = clipId;
    selected.app = {};
    expect(() => captureClipParamsEdit(session.clipParamsPort, current, clipId)).toThrow('explicit occurrence');
    expect(env.commits()).toHaveLength(0);
    await session.dispose();
  });
});
