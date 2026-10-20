// @vitest-environment jsdom
import { act, cleanup, renderHook, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { document, environment } from '../commands/__tests__/commitSessionEnvironment.ts';
import { fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { authoringBundleFromDocument } from '../commands/authoringBundle.ts';
import { executeClipMove } from '../commands/clipMoveCapture.ts';
import { captureClipMove, submitClipMove } from '../commands/semanticGestures.ts';
import type { CommandSessionState } from '../commands/commitSession.ts';
import { buildTimelineData, type TimelineData } from '../lib/timeline-data.ts';
import { serializeForDisk } from '../lib/serialize.ts';
import { createTimelineStore } from './timelineStore.ts';
import { TimelineEventBus } from './useTimelineEventBus.ts';
import { useTimelineCommandSession } from './useTimelineCommandSession.ts';
import { useTimelineCommit } from './useTimelineCommit.ts';

afterEach(() => { cleanup(); vi.unstubAllGlobals(); });

async function setup(initialDocument = document()) {
  const env = await environment(initialDocument);
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
    const installed: { data: TimelineData; status: CommandSessionState['status'] }[] = [];
    let status: CommandSessionState['status'] = 'loading';
    const hook = renderHook(({ loaded }: { loaded: TimelineData }) => {
      const commit = useTimelineCommit({ eventBus, lastSavedSignatureRef, initialData: initial, snapshotWriteBlockedRef });
      const commands = useTimelineCommandSession({ provider: env.provider, timelineId: 'timeline-commit',
        commit: { ...commit, commitData: (data, options) => {
          commit.commitData(data, options);
          installed.push({ data: commit.dataRef.current!, status });
        } }, legacyClean: () => true, snapshotWriteBlockedRef,
        resolveAssetUrl: async (file) => file, loaded, configVersionRef, headRevisionRef,
        lastSavedSignatureRef, store, shots: { canonicalDraft: null } });
      status = commands.state.status;
      return { commit, commands };
    }, { initialProps: { loaded: initial } });
    const move = (at: number) => submitClipMove(captureClipMove(hook.result.current.commands.port,
      hook.result.current.commit.dataRef.current!, 'x'), at);
    return { hook, move, installed };
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

describe('atomic command projection facts', () => {
  it('preserves raw opaque roots on load, preview, recovery and accepted projection', async () => {
    const raw = document();
    const opaque = JSON.parse('{"opaque":{"retained":[null,false,[]]},"nullable":null,"ordered":[0,false,null,[],{}],"__proto__":{"prototype":null},"constructor":false,"prototype":[]}');
    raw.parent_revision.payload.config = { ...raw.parent_revision.payload.config as object, ...opaque };
    raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
    const original = structuredClone(raw);
    const { env, mount, held } = await setup(raw);
    const assertRoots = (data: TimelineData) => {
      expect(data.config).toMatchObject({ opaque: { retained: [null, false, []] } });
      for (const config of [data.config, data.resolvedConfig]) {
        expect(Object.fromEntries(Object.keys(opaque).map((key) => [key, (config as unknown as Record<string, unknown>)[key]]))).toStrictEqual(opaque);
        for (const key of Object.keys(opaque)) expect(Object.hasOwn(config, key)).toBe(true);
        expect(Object.getPrototypeOf(config)).toBe(Object.prototype);
        expect(config).not.toHaveProperty('editProjection');
      }
    };
    const first = mount();
    await waitFor(() => expect(first.hook.result.current.commands.port).toBeDefined());
    assertRoots(first.hook.result.current.commit.data!);
    env.setFault('lost');
    act(() => { first.move(5); first.move(7); });
    await waitFor(() => expect(first.hook.result.current.commands.state.status).toBe('retry'));
    assertRoots(first.hook.result.current.commit.data!);
    const owner = first.hook.result.current.commands.state.ownerId!;
    first.hook.unmount();
    await waitFor(() => expect(held.size).toBe(0));
    const recovered = mount(await latestData(env));
    await waitFor(() => expect(recovered.hook.result.current.commands.state.status).toBe('recovery'));
    assertRoots(recovered.hook.result.current.commit.data!);
    env.setFault('busy');
    await act(async () => { await recovered.hook.result.current.commands.recover(owner); });
    expect(recovered.hook.result.current.commit.data?.config.clips[0].at).toBe(7);
    assertRoots(recovered.hook.result.current.commit.data!);
    env.setFault(null);
    await act(async () => { await recovered.hook.result.current.commands.retry(); });
    expect(recovered.hook.result.current.commands.state.status).toBe('saved');
    expect(recovered.hook.result.current.commit.data?.editProjection?.kind).toBe('accepted');
    for (const { data } of recovered.installed) assertRoots(data);
    const accepted = await env.provider.loadTimelineCommandBasis('timeline-commit');
    let expected = await authoringBundleFromDocument(original);
    const requests = new Map(env.commits().map((call) => [call.key, call.body!]));
    for (const request of requests.values()) expected = executeClipMove(expected, request.commands[0]).bundle;
    expect(accepted.canonicalDocument.parent_revision.payload).toEqual({ ...expected.parent, occurrences: [] });
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
    const accepted = installed.find(({ data }) => data.editProjection?.kind === 'accepted')!;
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
    const gate = env.pause();
    act(() => { move(5); });
    await waitFor(() => expect(hook.result.current.commands.state.status).toBe('saving'));
    expect(hook.result.current.commit.data?.config.clips[0].at).toBe(5);
    expect(hook.result.current.commit.data?.editProjection).toBeUndefined();
    await act(async () => { gate.resolve(); await hook.result.current.commands.flush(); });
    expect(hook.result.current.commit.data?.editProjection?.kind).toBe('accepted');
  });
});
