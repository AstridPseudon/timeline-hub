// @vitest-environment jsdom
import { act, cleanup, renderHook, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { document, environment } from '../commands/__tests__/commitSessionEnvironment.ts';
import { authoringBundleFromDocument } from '../commands/authoringBundle.ts';
import { captureClipMove as captureNativeMove, executeClipMove, finishClipMove } from '../commands/clipMoveCapture.ts';
import { captureClipMove, submitClipMove } from '../commands/semanticGestures.ts';
import type { CommandSessionState } from '../commands/commitSession.ts';
import { buildTimelineData, type TimelineData } from '../lib/timeline-data.ts';
import { serializeForDisk } from '../lib/serialize.ts';
import { createTimelineStore } from './timelineStore.ts';
import { TimelineEventBus } from './useTimelineEventBus.ts';
import { useTimelineCommandSession } from './useTimelineCommandSession.ts';
import { createRecoveryConfig } from './useTimelineSave.draftConfig.ts';
import { useTimelineCommit } from './useTimelineCommit.ts';
import { captureClipParamsEdit, submitClipParamsEdit } from '../commands/clipParamsGesture.ts';
import type { ClipSetParamsArgs } from '@/integrations/runtime/timeline-commit-types.ts';

afterEach(() => { cleanup(); vi.unstubAllGlobals(); vi.restoreAllMocks(); });

async function setup(raw = document(), applyParams?: Parameters<typeof environment>[1]) {
  const env = await environment(raw, applyParams);
  vi.stubGlobal('indexedDB', env.factory);
  const held = new Set<string>();
  vi.stubGlobal('navigator', { locks: { request: async (key: string, _options: unknown, work: (lock: unknown) => Promise<unknown>) => {
    if (held.has(key)) return work(null);
    held.add(key);
    try { return await work({ name: key }); } finally { held.delete(key); }
  } } });
  const mount = (initial = env.current()) => {
    const eventBus = new TimelineEventBus();
    const lastSavedSignatureRef = { current: initial.stableSignature };
    const configVersionRef = { current: initial.configVersion };
    const headRevisionRef = { current: initial.head };
    const snapshotWriteBlockedRef = { current: false };
    const store = createTimelineStore();
    const recoveryConfig = createRecoveryConfig();
    let clean = true;
    const installed: { data: TimelineData; status: CommandSessionState['status'] }[] = [];
    let status: CommandSessionState['status'] = 'loading';
    const hook = renderHook(({ loaded }: { loaded: TimelineData }) => {
      const commit = useTimelineCommit({ eventBus, lastSavedSignatureRef, initialData: initial, snapshotWriteBlockedRef });
      const commands = useTimelineCommandSession({ provider: env.provider, timelineId: 'timeline-commit',
        commit: { ...commit, commitData: (data, options) => {
          commit.commitData(data, options);
          installed.push({ data: commit.dataRef.current!, status });
        } }, legacyClean: () => clean, snapshotWriteBlockedRef,
        resolveAssetUrl: async (file) => file, loaded, configVersionRef, headRevisionRef,
        lastSavedSignatureRef, store, recoveryConfig, shots: { canonicalDraft: null } });
      status = commands.state.status;
      return { commit, commands };
    }, { initialProps: { loaded: initial } });
    const move = (at: number) => submitClipMove(captureClipMove(hook.result.current.commands.port,
      hook.result.current.commit.dataRef.current!, 'x'), at);
    return { hook, move, installed, eventBus, headRevisionRef, configVersionRef, store, recoveryConfig,
      lastSavedSignatureRef, setClean: (value: boolean) => { clean = value; } };
  };
  return { env, mount, held };
}

const originalBase = { revisionId: 'r0', publicationId: 'p0' };
const latestData = async (env: Awaited<ReturnType<typeof environment>>) => {
  const basis = await env.provider.loadTimelineCommandBasis('timeline-commit');
  const parent = basis.canonicalDocument.parent_revision.payload;
  return buildTimelineData({ ...parent.config as object, clips: parent.clips } as never, { assets: {} }, undefined,
    1, undefined, { projectId: 'project-commit', timelineId: 'timeline-commit',
      headRevisionId: basis.head.revisionId, headPublicationId: basis.head.publicationId });
};
const publishC = (env: Awaited<ReturnType<typeof environment>>) => env.provider.undoTimeline({
  projectId: 'project-commit', timelineId: 'timeline-commit', headRevisionId: 'r1', headPublicationId: 'p1',
}, ['p1'], 'independent-c');

const opaqueRoots = () => JSON.parse('{"opaque":{"retained":[null,false,[]]},"nullable":null,"enabled":false,"count":0,"label":"","ordered":[0,false,null,[],{}],"__proto__":{"prototype":null,"__proto__":[]},"constructor":false,"prototype":[]}');
const assertRoots = (data: TimelineData, opaque: Record<string, unknown>) => {
  expect(data.config).toMatchObject({ opaque: { retained: [null, false, []] } });
  for (const config of [data.config, data.resolvedConfig]) {
    expect(Object.fromEntries(Object.keys(opaque).map((key) => [key, (config as unknown as Record<string, unknown>)[key]]))).toStrictEqual(opaque);
    for (const key of Object.keys(opaque)) expect(Object.hasOwn(config, key)).toBe(true);
    expect(Object.getPrototypeOf(config)).toBe(Object.prototype);
    expect(Object.hasOwn(config, 'absent')).toBe(false);
    expect(config).not.toHaveProperty('editProjection');
  }
};

describe('atomic command projection facts', () => {
  it('shows selected PARAM PENDING without changing the accepted display, then atomically projects ACK and keeps an ordinary suffix', async () => {
    const raw = document();
    for (const rows of [raw.parent_revision.payload.clips, raw.parent_revision.payload.config.clips]) {
      Object.assign(rows[0], { clipType: 'text', elementRef: { packId: 'fixture', id: 'text', kind: 'effect', revision: 'v1' },
        params: { seed: 4, opaque: [null, false, {}] } });
    }
    raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
    // Synthetic normal-port acceptance only; native validation has its own provider probe.
    const { env, mount } = await setup(raw, (before, command) => {
      const next = structuredClone(before);
      const row = next.parent_revision.payload.clips[0];
      row.params = { ...row.params, ...(command.args as ClipSetParamsArgs).values };
      next.parent_revision.payload.config.clips = structuredClone(next.parent_revision.payload.clips);
      return next;
    });
    const mounted = mount();
    await waitFor(() => expect(mounted.hook.result.current.commands.clipParamsPort).toBeDefined());
    const snapshotSaves = vi.fn();
    mounted.eventBus.on('scheduleSave', snapshotSaves);
    const save = vi.spyOn(env.provider, 'saveTimeline');
    const saveAtHead = vi.spyOn(env.provider, 'saveTimelineAtHead');
    const pause = env.pause();
    const captured = captureClipParamsEdit(mounted.hook.result.current.commands.clipParamsPort,
      mounted.hook.result.current.commit.data!, 'x');
    act(() => submitClipParamsEdit(captured, { values: { seed: 8 }, clear: [],
      schema_source: { document_id: 'retained-v1', version: 1, content_digest: `sha256:${'1'.repeat(64)}` } }));
    await waitFor(() => expect(mounted.hook.result.current.commands.state.status).toBe('pending'));
    expect(mounted.hook.result.current.commands.state.error).toContain('PENDING');
    expect(mounted.hook.result.current.commands.activeRef.current).toBe(true);
    expect(mounted.hook.result.current.commit.data!.config.clips[0].params.seed).toBe(4);
    expect(mounted.hook.result.current.commit.data!.editProjection).toEqual({ kind: 'accepted', head: originalBase });
    await waitFor(() => expect(env.commits()).toHaveLength(1));
    act(() => mounted.move(5));
    expect(mounted.hook.result.current.commit.data!.config.clips[0]).toMatchObject({ at: 5, params: { seed: 4 } });
    pause.resolve();
    await act(async () => { await mounted.hook.result.current.commands.flush(); });
    const final = mounted.hook.result.current.commit.data!;
    expect(final.config.clips[0]).toMatchObject({ at: 5, params: { seed: 8, opaque: [null, false, {}] } });
    expect(final.editProjection).toEqual({ kind: 'accepted', head: { revisionId: 'r2', publicationId: 'p2' } });
    expect(mounted.installed.some(({ data }) => data.config.clips[0].params.seed === 8
      && data.config.clips[0].at === 5 && data.editProjection?.kind === 'local')).toBe(true);
    expect(env.commits()[1].body).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p1',
      commands: [{ op: 'clip.move', expect: { 'parent/clip:x::at': { state: 'present', value: 1 } } }] });
    expect(snapshotSaves).not.toHaveBeenCalled();
    expect(save).not.toHaveBeenCalled();
    expect(saveAtHead).not.toHaveBeenCalled();
    mounted.hook.unmount();
  });

  it('projects the exact verified initial config, registry and head with no commands or graph', async () => {
    const raw = document();
    const opaque = opaqueRoots();
    raw.parent_revision.payload.config = { ...raw.parent_revision.payload.config as object, ...opaque,
      x_null: null, x_nested: { unknown: [false, 0, []] } };
    raw.parent_revision.payload.clips[0].at = 9;
    raw.parent_revision.payload.registry = { assets: { original: { file: 'original.png', type: 'image/png' } } };
    raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
    const { env, mount } = await setup(raw);
    const basis = { ...env.initial, graph: undefined };
    vi.spyOn(env.provider, 'loadTimelineCommandBasis').mockResolvedValue(basis);
    const resolve = vi.spyOn(env.provider, 'resolveTimelineCommandAsset').mockResolvedValue('/verified/original.png');
    const save = vi.spyOn(env.provider, 'saveTimeline');
    const saveAtHead = vi.spyOn(env.provider, 'saveTimelineAtHead');
    const mounted = mount();
    const snapshots = vi.fn();
    mounted.eventBus.on('scheduleSave', snapshots);
    const before = env.current();
    expect(before.config.clips[0].at).toBe(1); // Old host config disagrees with the canonical clips.
    expect(before.editProjection).toBeUndefined();
    await waitFor(() => expect(mounted.hook.result.current.commands.port).toBeDefined());
    const data = mounted.hook.result.current.commit.data!;
    const expected = await buildTimelineData({ ...raw.parent_revision.payload.config as object,
      clips: raw.parent_revision.payload.clips } as never, raw.parent_revision.payload.registry as never,
      async () => '/verified/original.png', before.configVersion + 1, undefined, before.head);
    expect(data).toEqual({ ...expected, editProjection: { kind: 'accepted', head: originalBase } });
    assertRoots(data, opaque);
    expect(mounted.recoveryConfig.snapshot(data.head, data.config)).toMatchObject(opaque);
    expect(mounted.installed.map(({ data }) => data)).toEqual([data]);
    expect(resolve).toHaveBeenCalledWith('original.png', raw.parent_revision.payload.registry);
    expect(mounted.headRevisionRef.current).toEqual(data.head);
    expect(mounted.configVersionRef.current).toBe(data.configVersion);
    expect(mounted.store.getState().configVersion).toBe(data.configVersion);
    expect(mounted.lastSavedSignatureRef.current).toBe(data.stableSignature);
    expect(mounted.recoveryConfig.snapshot(data.head, data.config)).toMatchObject({
      x_null: null, x_nested: { unknown: [false, 0, []] },
    });
    expect(mounted.recoveryConfig.snapshot(data.head, data.config)).not.toHaveProperty('x_absent');
    expect(data.config).not.toHaveProperty('compiled');
    expect(data.resolvedConfig).not.toHaveProperty('compiled');
    expect(basis.canonicalDocument).toEqual(raw);
    expect(env.commits()).toHaveLength(0);
    expect(snapshots).not.toHaveBeenCalled();
    expect(save).not.toHaveBeenCalled();
    expect(saveAtHead).not.toHaveBeenCalled();
  });

  it.each(['manifest', 'revision', 'publication', 'project', 'timeline', 'bundle'] as const)(
    'refuses an initial basis with a bad %s without changing the displayed object', async (fault) => {
      const { env, mount, held } = await setup();
      const basis = structuredClone(env.initial);
      if (fault === 'manifest') basis.canonicalDocument.dependency_manifest.shots.push({
        shot_id: 'missing', revision_id: 'missing', content_digest: fixtureDigest(null), internal_timeline_revision_id: 'missing',
      });
      if (fault === 'bundle') basis.canonicalDocument.parent_revision.payload.config.bundle = { schema_version: 2 };
      if (fault === 'revision') basis.head.revisionId = 'wrong';
      if (fault === 'publication') basis.head.publicationId = '';
      if (fault === 'project') basis.canonicalDocument.project_id = 'wrong';
      if (fault === 'timeline') basis.canonicalDocument.timeline_id = 'wrong';
      vi.spyOn(env.provider, 'loadTimelineCommandBasis').mockResolvedValue(basis);
      const mounted = mount();
      await waitFor(() => expect(mounted.hook.result.current.commands.state.status).toBe('error'));
      expect(mounted.hook.result.current.commit.data).toBe(env.current());
      expect(mounted.hook.result.current.commit.data?.editProjection).toBeUndefined();
      expect(mounted.installed).toHaveLength(0);
      expect(held.size).toBe(0);
      expect(env.commits()).toHaveLength(0);
    });

  it.each(['local', 'accepted'] as const)('preserves an existing %s projection during initial bootstrap', async (kind) => {
    const { env, mount } = await setup();
    const initial = { ...env.current(), editProjection: kind === 'local'
      ? { kind: 'local' as const, base: originalBase, generation: 3 }
      : { kind: 'accepted' as const, head: originalBase } };
    const mounted = mount(initial);
    await waitFor(() => expect(mounted.hook.result.current.commands.port).toBeDefined());
    expect(mounted.hook.result.current.commit.data).toBe(initial);
    expect(mounted.installed).toHaveLength(0);
    expect(env.commits()).toHaveLength(0);
  });

  it.each(['local', 'recovery', 'recovery pending', 'accepted', 'head', 'unmount'] as const)(
    'a delayed initial asset resolver preserves an intervening %s', async (intervening) => {
      const raw = document();
      raw.parent_revision.payload.registry = { assets: { original: { file: 'original.png', type: 'image/png' } } };
      raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
      const { env, mount, held } = await setup(raw);
      let finish!: (url: string) => void;
      const gate = new Promise<string>((resolve) => { finish = resolve; });
      const resolve = vi.spyOn(env.provider, 'resolveTimelineCommandAsset').mockReturnValue(gate);
      const mounted = mount();
      await waitFor(() => expect(resolve).toHaveBeenCalled());
      let next = env.current();
      if (intervening === 'unmount') mounted.hook.unmount();
      else act(() => {
        if (intervening === 'recovery pending') mounted.setClean(false);
        else if (intervening === 'head') mounted.headRevisionRef.current = { ...next.head!, headRevisionId: 'r-new', headPublicationId: 'p-new' };
        else {
          next = { ...next, config: { ...next.config, clips: next.config.clips.map((clip) => ({ ...clip, at: 7 })) },
            editProjection: intervening === 'accepted' ? { kind: 'accepted', head: { revisionId: 'r-new', publicationId: 'p-new' } }
              : intervening === 'local' ? { kind: 'local', base: originalBase, generation: 1 } : undefined };
          mounted.hook.result.current.commit.commitData(next, { save: false, skipHistory: true });
          if (intervening === 'recovery') mounted.setClean(false);
        }
      });
      const head = mounted.headRevisionRef.current;
      mounted.recoveryConfig.remember(head, { x_intervening: null });
      mounted.configVersionRef.current = 42;
      mounted.store.getState().setConfigVersion(42);
      const signature = mounted.lastSavedSignatureRef.current;
      await act(async () => { finish('/verified/original.png'); await gate; });
      if (intervening === 'unmount') await waitFor(() => expect(held.size).toBe(0));
      else await waitFor(() => expect(mounted.hook.result.current.commands.port).toBeDefined());
      expect(mounted.hook.result.current.commit.dataRef.current).toBe(next);
      expect(mounted.headRevisionRef.current).toBe(head);
      expect(mounted.configVersionRef.current).toBe(42);
      expect(mounted.store.getState().configVersion).toBe(42);
      expect(mounted.lastSavedSignatureRef.current).toBe(signature);
      expect(mounted.recoveryConfig.snapshot(head, next.config)).toEqual({ ...next.config, x_intervening: null });
      expect(mounted.installed).toHaveLength(0);
      expect(env.commits()).toHaveLength(0);
    });

  it('preserves raw opaque roots on load, preview, recovery and accepted projection', async () => {
    const raw = document();
    const opaque = opaqueRoots();
    raw.parent_revision.payload.config = { ...raw.parent_revision.payload.config as object, ...opaque };
    raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
    const original = structuredClone(raw);
    const { env, mount, held } = await setup(raw);
    const first = mount();
    await waitFor(() => expect(first.hook.result.current.commands.port).toBeDefined());
    assertRoots(first.hook.result.current.commit.data!, opaque);
    env.setFault('lost');
    act(() => { first.move(5); first.move(7); });
    await waitFor(() => expect(first.hook.result.current.commands.state.status).toBe('retry'));
    assertRoots(first.hook.result.current.commit.data!, opaque);
    const owner = first.hook.result.current.commands.state.ownerId!;
    first.hook.unmount();
    await waitFor(() => expect(held.size).toBe(0));
    const recovered = mount(await latestData(env));
    await waitFor(() => expect(recovered.hook.result.current.commands.state.status).toBe('recovery'));
    assertRoots(recovered.hook.result.current.commit.data!, opaque);
    env.setFault('busy');
    await act(async () => { await recovered.hook.result.current.commands.recover(owner); });
    expect(recovered.hook.result.current.commit.data?.config.clips[0].at).toBe(7);
    assertRoots(recovered.hook.result.current.commit.data!, opaque);
    env.setFault(null);
    await act(async () => { await recovered.hook.result.current.commands.retry(); });
    expect(recovered.hook.result.current.commands.state.status).toBe('saved');
    expect(recovered.hook.result.current.commit.data?.editProjection).toEqual({ kind: 'accepted', head: { revisionId: 'r2', publicationId: 'p2' } });
    for (const { data } of recovered.installed) assertRoots(data, opaque);
    const accepted = await env.provider.loadTimelineCommandBasis('timeline-commit');
    let expected = await authoringBundleFromDocument(original);
    const requests = new Map(env.commits().map((call) => [call.key, call.body!]));
    expect(requests.size).toBe(2);
    for (const [index, request] of [...requests.values()].entries()) {
      const native = finishClipMove(captureNativeMove(expected, 'parent/clip:x'), [5, 7][index]);
      expect(request.commands).toEqual([native.command]);
      expect(executeClipMove(expected, request.commands[0])).toEqual(native);
      expected = native.bundle;
    }
    expect(accepted.canonicalDocument.parent_revision.payload).toStrictEqual({ ...expected.parent, occurrences: [] });
    expect(env.commits()[2]).toEqual(env.commits()[0]);
    expect(JSON.stringify(env.commits())).not.toContain('editProjection');
    expect(raw).toStrictEqual(original);
  });

  it('installs accepted closure data and its exact fact while the session is still saving', async () => {
    const { env, mount } = await setup();
    const { hook, move, installed } = mount();
    await waitFor(() => expect(hook.result.current.commands.port).toBeDefined());
    const gate = env.pause();
    act(() => { move(5); });
    await waitFor(() => expect(hook.result.current.commands.state.status).toBe('saving'));
    expect(hook.result.current.commit.data?.editProjection).toEqual({ kind: 'local', base: originalBase, generation: 1 });
    await act(async () => { gate.resolve(); await hook.result.current.commands.flush(); });
    const accepted = installed.find(({ data }) => data.editProjection?.kind === 'accepted'
      && data.editProjection.head.publicationId === 'p1')!;
    expect(accepted.status).toBe('saving');
    expect(accepted.data.config.clips[0].at).toBe(5);
    expect(accepted.data.editProjection).toEqual({ kind: 'accepted', head: { revisionId: 'r1', publicationId: 'p1' } });
    expect(hook.result.current.commit.data).toBe(accepted.data);
    expect(hook.result.current.commands.state.status).toBe('saved');
    act(() => { move(5); });
    await act(async () => { await hook.result.current.commands.flush(); });
    expect(hook.result.current.commit.data?.editProjection).toEqual({ kind: 'accepted', head: { revisionId: 'r1', publicationId: 'p2' } });
    for (const { data } of installed) {
      expect(data.config).not.toHaveProperty('editProjection');
      expect(data.resolvedConfig).not.toHaveProperty('editProjection');
      expect(JSON.stringify(serializeForDisk(data.resolvedConfig))).not.toContain('editProjection');
    }
    expect(JSON.stringify(env.commits())).not.toContain('editProjection');
  });

  it('keeps B local at its original base after A ACK when B cannot yet be accepted', async () => {
    const { env, mount } = await setup();
    const { hook, move, installed } = mount();
    await waitFor(() => expect(hook.result.current.commands.port).toBeDefined());
    installed.length = 0;
    env.setFault('lost');
    act(() => { move(5); move(7); });
    await waitFor(() => expect(hook.result.current.commands.state.status).toBe('retry'));
    const b = hook.result.current.commit.data!;
    expect(b.editProjection).toEqual({ kind: 'local', base: originalBase, generation: 2 });
    // C's inverse breaks B's original A5 guard; the HTTP fixture returns a typed conflict.
    await publishC(env);
    await act(async () => { await hook.result.current.commands.retry(); });
    expect(env.commits()[2]).toEqual(env.commits()[0]);
    expect(env.commits()[3].body?.base_publication_id).toBe('p1');
    expect(env.commits()[3].body?.commands[0].expect?.['parent/clip:x::at']).toEqual({ state: 'present', value: 5 });
    expect(hook.result.current.commands.state.status).toBe('conflict');
    await act(async () => { await hook.result.current.commands.retry(); });
    expect(env.commits()).toHaveLength(4);
    expect(hook.result.current.commit.data).toBe(b);
    expect(b.config.clips[0].at).toBe(7);
    expect(b.editProjection).toEqual({ kind: 'local', base: originalBase, generation: 2 });
    expect(installed.every(({ data }) => data.editProjection?.kind === 'local')).toBe(true);
  });

  it('recovers local data using the persisted original display basis rather than the reopened head', async () => {
    const { env, mount, held } = await setup();
    const first = mount();
    await waitFor(() => expect(first.hook.result.current.commands.port).toBeDefined());
    env.setFault('lost');
    act(() => { first.move(5); first.move(7); });
    await waitFor(() => expect(first.hook.result.current.commands.state.status).toBe('retry'));
    const owner = first.hook.result.current.commands.state.ownerId!;
    first.hook.unmount();
    await waitFor(() => expect(held.size).toBe(0));
    const current = await latestData(env);
    expect(current.head?.headPublicationId).toBe('p1');
    const recovered = mount(current);
    await waitFor(() => expect(recovered.hook.result.current.commands.state.status).toBe('recovery'));
    expect(recovered.installed).toHaveLength(0);
    expect(recovered.hook.result.current.commit.data).toBe(current);
    env.setFault('busy');
    await act(async () => { await recovered.hook.result.current.commands.recover(owner); });
    expect(recovered.hook.result.current.commit.data?.config.clips[0].at).toBe(7);
    expect(recovered.hook.result.current.commit.data?.editProjection).toEqual({ kind: 'local', base: originalBase, generation: 1 });
    expect(recovered.hook.result.current.commands.state.status).toBe('retry');
    env.setFault(null);
    await act(async () => { await recovered.hook.result.current.commands.retry(); });
    expect(recovered.hook.result.current.commit.data?.editProjection).toEqual({ kind: 'accepted', head: { revisionId: 'r2', publicationId: 'p2' } });
  });

  it('retains the original local base when recovery follows an acknowledged predecessor', async () => {
    const { env, mount, held } = await setup();
    const first = mount();
    await waitFor(() => expect(first.hook.result.current.commands.port).toBeDefined());
    env.setFault('lost');
    act(() => { first.move(5); first.move(7); });
    await waitFor(() => expect(first.hook.result.current.commands.state.status).toBe('retry'));
    await publishC(env);
    await act(async () => { await first.hook.result.current.commands.retry(); });
    const owner = first.hook.result.current.commands.state.ownerId!;
    first.hook.unmount();
    await waitFor(() => expect(held.size).toBe(0));
    const recovered = mount(await latestData(env));
    await waitFor(() => expect(recovered.hook.result.current.commands.state.status).toBe('recovery'));
    await act(async () => { await recovered.hook.result.current.commands.recover(owner); });
    expect(recovered.hook.result.current.commit.data?.config.clips[0].at).toBe(7);
    expect(recovered.hook.result.current.commit.data?.editProjection).toMatchObject({ kind: 'local', base: originalBase });
    expect(recovered.hook.result.current.commands.state.status).toBe('conflict');
    await act(async () => { await recovered.hook.result.current.commands.retry(); });
    expect(env.commits()).toHaveLength(4);
  });

  it('projects a known newer C at C instead of relabeling it as the late A acceptance', async () => {
    const { env, mount } = await setup();
    const { hook, move, installed } = mount();
    await waitFor(() => expect(hook.result.current.commands.port).toBeDefined());
    env.setFault('lost');
    act(() => { move(5); });
    await waitFor(() => expect(hook.result.current.commands.state.status).toBe('retry'));
    await publishC(env);
    const current = await latestData(env);
    act(() => { hook.rerender({ loaded: current }); });
    await waitFor(() => expect(env.calls.filter((call) => call.path.endsWith('/commits?limit=50')).length).toBeGreaterThanOrEqual(4));
    await act(async () => { await hook.result.current.commands.retry(); });
    expect(hook.result.current.commit.data?.config.clips[0].at).toBe(1);
    expect(hook.result.current.commit.data?.editProjection).toEqual({ kind: 'accepted', head: { revisionId: 'r2', publicationId: 'p2' } });
    expect(installed.some(({ data }) => data.editProjection?.kind === 'accepted' && data.editProjection.head.publicationId === 'p1')).toBe(false);
  });

  it.each(['ordinary', 'legacy spread'] as const)('clears an accepted fact on a later %s local edit', async (edit) => {
    const { mount } = await setup();
    const { hook, move } = mount();
    await waitFor(() => expect(hook.result.current.commands.port).toBeDefined());
    act(() => { move(5); });
    await act(async () => { await hook.result.current.commands.flush(); });
    expect(hook.result.current.commit.data?.editProjection?.kind).toBe('accepted');
    act(() => {
      const current = hook.result.current.commit.data!;
      if (edit === 'ordinary') hook.result.current.commit.applyEdit({ type: 'config',
        resolvedConfig: { ...current.resolvedConfig, clips: current.resolvedConfig.clips.map((clip) => ({ ...clip, label: 'local' })) } });
      else hook.result.current.commit.commitData({ ...current, config: { ...current.config,
        clips: current.config.clips.map((clip) => ({ ...clip, label: 'local' })) } }, { save: false });
    });
    expect(hook.result.current.commit.data?.config.clips[0].label).toBe('local');
    expect(hook.result.current.commit.data?.editProjection).toBeUndefined();
  });

  it('does not invent a local publication pair for displayed data with an incomplete head', async () => {
    const { env, mount } = await setup();
    const initial = env.current();
    const { hook, move } = mount({ ...initial, head: { ...initial.head!, headPublicationId: undefined } });
    await waitFor(() => expect(hook.result.current.commands.port).toBeDefined());
    act(() => { hook.result.current.commit.commitData({ ...initial, head: { ...initial.head!, headPublicationId: undefined } }, { save: false }); });
    const gate = env.pause();
    act(() => { move(5); });
    await waitFor(() => expect(hook.result.current.commands.state.status).toBe('saving'));
    expect(hook.result.current.commit.data?.config.clips[0].at).toBe(5);
    expect(hook.result.current.commit.data?.editProjection).toBeUndefined();
    await act(async () => { gate.resolve(); await hook.result.current.commands.flush(); });
    expect(hook.result.current.commit.data?.editProjection?.kind).toBe('accepted');
  });
});
