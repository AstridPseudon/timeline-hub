// @vitest-environment jsdom

import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { AgentChatProvider } from '@/shared/contexts/AgentChatContext.tsx';
import type { CanonicalDocument } from '@/integrations/runtime/timeline-commit-types.ts';
import { fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { trimDocument, environment, scope } from '@/tools/video-editor/commands/__tests__/commitSessionEnvironment.ts';
import { captureClipParamsEdit, submitClipParamsEdit } from '@/tools/video-editor/commands/clipParamsGesture.ts';
import { VideoEditorProvider } from '@/tools/video-editor/contexts/VideoEditorProvider.tsx';
import { useTimelineEditorData, useTimelineEditorOps } from '@/tools/video-editor/hooks/timelineStore.ts';
import * as commandSession from '@/tools/video-editor/hooks/useTimelineCommandSession.ts';
import { ClipPanelBody } from './ClipPanelBody.tsx';

// External host services and the initial read are fixed; provider/state/save,
// native capture, IndexedDB outbox and the Runtime client remain connected.
// Acceptance is simulated offline; released Agent/Runtime acceptance is separate.
vi.mock('@/tools/video-editor/runtime/installedTimelineHostServiceHooks.ts', async () => {
  const { PUBLIC_TIMELINE_SERVICE_HOOKS } = await import('@/tools/video-editor/runtime/timelineHostServiceHooks.ts');
  return { INSTALLED_TIMELINE_SERVICE_HOOKS: PUBLIC_TIMELINE_SERVICE_HOOKS };
});
vi.mock('@/tools/video-editor/adapters/app/useAstridShotsHost.ts', () => {
  const shots = { shots: [], isLoading: false, error: null, refetchShots: vi.fn(),
    finalVideoMap: new Map(), dismissFinalVideo: vi.fn(), canonicalDraft: null };
  return { useAstridShotsHost: () => shots };
});
vi.mock('@/shared/hooks/settings/useToolSettings', () => ({ useToolSettings: () => ({ settings: {} }) }));
vi.mock('@/tools/video-editor/hooks/useEffects.ts', () => {
  const effects = { data: [] };
  return { useEffects: () => effects };
});
vi.mock('@/tools/video-editor/hooks/useTimelineQueries.ts', () => ({
  useTimelineQueries: (_provider: unknown, _id: string, _resolve: unknown, initial: unknown) => ({
    timelineQuery: { data: initial, isLoading: false, error: null, refetch: vi.fn() },
    assetRegistryQuery: { data: (initial as { registry: unknown }).registry },
  }),
}));

afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks(); });

function rawClips(raw: CanonicalDocument) {
  return [raw.parent_revision.payload.clips as Array<Record<string, unknown>>,
    (raw.parent_revision.payload.config as { clips: Array<Record<string, unknown>> }).clips];
}

async function mounted(options: { group?: boolean; speed?: 'absent' | 'null'; missingPort?: boolean; staleHead?: boolean } = {}) {
  const raw = trimDocument();
  for (const clips of rawClips(raw)) {
    const clip = (clips as Array<Record<string, unknown>>)[0];
    if (options.speed === 'absent') delete clip.speed;
    if (options.speed === 'null') clip.speed = null;
    clip.enabled = null;
  }
  if (options.group) (raw.parent_revision.payload.config as Record<string, unknown>).pinnedShotGroups = [
    { shotId: 'legacy-shot', trackId: 'V1', clipIds: ['x'] },
  ];
  raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
  const original = structuredClone(raw);
  const env = await environment(raw);
  vi.stubGlobal('indexedDB', env.factory);
  const held = new Set<string>();
  vi.stubGlobal('navigator', { locks: { request: async (key: string, _options: unknown, work: (lock: unknown) => Promise<unknown>) => {
    if (held.has(key)) return work(null);
    held.add(key);
    try { return await work({ name: key }); } finally { held.delete(key); }
  } } });
  const hook = vi.spyOn(commandSession, 'useTimelineCommandSession');
  const saveTimeline = vi.spyOn(env.provider, 'saveTimeline');
  const saveTimelineAtHead = vi.spyOn(env.provider, 'saveTimelineAtHead');
  const onChange = vi.fn();
  let editor!: ReturnType<typeof useTimelineEditorData>;
  let ops!: ReturnType<typeof useTimelineEditorOps>;
  function Inspector() {
    editor = useTimelineEditorData();
    ops = useTimelineEditorOps();
    const current = editor.data!;
    const clip = current.resolvedConfig.clips.find((item) => item.id === 'x')!;
    const displayed = options.staleHead
      ? { ...current, head: { ...current.head!, headRevisionId: 'stale-displayed-head' } } : current;
    return <ClipPanelBody clip={clip} track={current.tracks[0]} current={displayed}
      clipTrimPort={options.missingPort ? undefined : ops.clipTrim} onChange={onChange}
      deviceClass="desktop" interactionMode="move" precisionEnabled={false} hasPredecessor={false}
      onResetPosition={vi.fn()} onClose={vi.fn()} onToggleMute={vi.fn()} onSplitAtPlayhead={vi.fn()}
      onMoveTrackUp={vi.fn()} onMoveTrackDown={vi.fn()} onSetInteractionMode={vi.fn()} onSetPrecisionEnabled={vi.fn()}
      compositionWidth={1920} compositionHeight={1080} registry={current.resolvedConfig.registry}
      activeTab="timing" setActiveTab={vi.fn()}
      effectResources={{ canCreateEffect: false, canUpdateEffect: false, effects: [] }} />;
  }
  const client = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: false } } });
  const view = render(<QueryClientProvider client={client}><MemoryRouter><AgentChatProvider>
    <VideoEditorProvider dataProvider={env.provider} projectId={scope.projectId}
      timelineId={scope.timelineId} userId={null} initialTimelineData={env.current()}>
      <Inspector />
    </VideoEditorProvider>
  </AgentChatProvider></MemoryRouter></QueryClientProvider>);
  const session = () => hook.mock.results.at(-1)!.value as ReturnType<typeof commandSession.useTimelineCommandSession>;
  await waitFor(() => expect(ops.clipTrim).toBeDefined());
  expect(ops.clipTrim).toBe(session().clipTrimPort);
  return { env, original, view, onChange, saveTimeline, saveTimelineAtHead, session,
    current: () => editor.data!, port: () => ops.clipTrim!, paramsPort: () => ops.clipParams! };
}

function sourceInput(label: 'Source In' | 'Source Out') {
  return screen.getByLabelText(label).querySelector('input')!;
}

function noSnapshots(editor: Awaited<ReturnType<typeof mounted>>) {
  expect(editor.onChange).not.toHaveBeenCalled();
  expect(editor.saveTimeline).not.toHaveBeenCalled();
  expect(editor.saveTimelineAtHead).not.toHaveBeenCalled();
  expect(editor.env.calls.filter((call) => call.method !== 'GET').map((call) => call.path))
    .toEqual(['/v1/handshake', ...editor.env.commits().map(() => expect.stringMatching(/\/commit$/))]);
}

describe('mounted single-parent source controls through the native provider outbox (offline transport)', () => {
  it.each([
    { label: 'Source In', value: 0, args: { in_s: 0, out_s: null }, from: 0, to: 6 },
    { label: 'Source Out', value: 10, args: { in_s: null, out_s: 10 }, from: 2, to: 10 },
    { label: 'Source Out', value: 9.8999, args: { in_s: null, out_s: 9.8999 }, from: 2, to: 9.8999 },
  ] as const)('commits $label=$value once in source seconds with speed=2', async ({ label, value, args, from, to }) => {
    const editor = await mounted();
    const { env, original, current, port, session, view } = editor;
    const before = current();
    const capture = vi.spyOn(port(), 'capture');
    const finish = vi.spyOn(port(), 'finish');
    const submit = vi.spyOn(port(), 'submit');
    const gate = env.pause();
    const input = sourceInput(label);
    act(() => input.focus());
    fireEvent.change(input, { target: { value: '4' } });
    fireEvent.change(input, { target: { value: String(value) } });
    expect(current()).toBe(before);
    expect(env.commits()).toHaveLength(0);
    expect(submit).not.toHaveBeenCalled();
    expect((await env.outboxes.list(scope))[0].intents).toEqual([]);
    fireEvent.blur(input);
    await waitFor(() => expect(env.commits()).toHaveLength(1));
    expect(capture).toHaveBeenCalledExactlyOnceWith({ clipId: 'x', current: before });
    expect(finish).toHaveBeenCalledOnce();
    expect(submit).toHaveBeenCalledOnce();
    const command = env.commits()[0].body!.commands[0];
    expect(command).toMatchObject({ op: 'clip.trim', select: 'parent/clip:x', args,
      expect: { 'parent/clip:x::from': { state: 'present', value: 2 },
        'parent/clip:x::to': { state: 'present', value: 6 } } });
    expect(env.commits()[0].body!.commands).toHaveLength(1);
    const stored = (await env.outboxes.list(scope))[0];
    expect(stored.intents).toHaveLength(1);
    expect(stored.intents[0].payload).toMatchObject({ commands: [command], preview: { source: 'clip.trim' } });
    expect(JSON.parse(stored.pending!.request.body)).toEqual(env.commits()[0].body);
    expect(stored.pending!.request.key).toBe(env.commits()[0].key);
    const expectedTiming = { at: 1, track: 'V1', speed: 2, from, to, hold: Number((to - from).toFixed(6)) };
    expect(current().config.clips[0]).toMatchObject(expectedTiming);
    expect(current().resolvedConfig.clips[0]).toMatchObject(expectedTiming);
    expect(sourceInput('Source In')).toHaveValue(String(from));
    expect(sourceInput('Source Out')).toHaveValue(String(to));
    await act(async () => { gate.resolve(); await session().flush(); });
    expect(session().state.status).toBe('saved');
    expect(current().resolvedConfig.clips[0]).toMatchObject(expectedTiming);
    const accepted = await env.provider.loadTimelineCommandBasis(scope.timelineId);
    const expected = structuredClone(original);
    for (const clips of rawClips(expected)) {
      Object.assign(clips[0], { from, to, hold: expectedTiming.hold });
      const astrid = (clips[0].app as { astrid: Record<string, unknown> }).astrid;
      delete astrid.for;
      delete astrid.until;
    }
    expect(accepted.canonicalDocument.parent_revision.payload).toEqual(expected.parent_revision.payload);
    fireEvent.blur(input);
    expect(submit).toHaveBeenCalledOnce();
    noSnapshots(editor);
    view.unmount();
  });

  it.each(['absent', 'null'] as const)('retains raw %s speed and opaque/null fields through a trim', async (speed) => {
    const editor = await mounted({ speed });
    const { env, original, current, port, session, view } = editor;
    const finish = vi.spyOn(port(), 'finish');
    const input = sourceInput('Source In');
    act(() => input.focus());
    fireEvent.change(input, { target: { value: '0' } });
    fireEvent.blur(input);
    await act(async () => { await session().flush(); });
    expect(session().state.status).toBe('saved');
    expect(env.commits()).toHaveLength(1);
    expect(finish.mock.results[0].value.command.reads).toContainEqual({ ref: 'parent/clip:x', path: ['speed'],
      state: speed === 'absent' ? { state: 'absent' } : { state: 'present', value: null } });
    const accepted = await env.provider.loadTimelineCommandBasis(scope.timelineId);
    const clip = rawClips(accepted.canonicalDocument)[0][0];
    if (speed === 'absent') expect(clip).not.toHaveProperty('speed');
    else expect(clip.speed).toBeNull();
    expect(clip.unknown).toEqual(rawClips(original)[0][0].unknown);
    expect(clip.enabled).toBeNull();
    expect(current().resolvedConfig.clips[0]).toMatchObject({ from: 0, to: 6, hold: 6 });
    noSnapshots(editor);
    view.unmount();
  });

  it.each(['capture', 'finish', 'submit'] as const)('retains the typed endpoint after a %s failure without recapture on blur', async (stage) => {
    const editor = await mounted();
    const { env, current, port, view } = editor;
    const before = current();
    const capture = vi.spyOn(port(), 'capture');
    const failed = stage === 'capture' ? capture : vi.spyOn(port(), stage);
    failed.mockImplementation(() => { throw new Error(`Native ${stage} unavailable`); });
    const input = sourceInput('Source Out');
    act(() => input.focus());
    fireEvent.change(input, { target: { value: '8.5' } });
    fireEvent.blur(input);
    expect(screen.getByRole('alert')).toHaveTextContent(`Native ${stage} unavailable`);
    expect(sourceInput('Source Out')).toHaveValue('8.5');
    expect(capture).toHaveBeenCalledOnce();
    expect(current()).toBe(before);
    expect((await env.outboxes.list(scope))[0].intents).toEqual([]);
    expect(env.commits()).toHaveLength(0);
    noSnapshots(editor);
    view.unmount();
  });

  it.each<Parameters<typeof mounted>[0]>([{ group: true }, { missingPort: true }, { staleHead: true }])('refuses unsupported ownership or a missing native port and retains the draft: %j', async (options = {}) => {
    const editor = await mounted(options);
    const before = editor.current();
    const input = sourceInput('Source In');
    act(() => input.focus());
    fireEvent.change(input, { target: { value: '1.25' } });
    fireEvent.blur(input);
    expect(screen.getByRole('alert')).toHaveTextContent(options.group ? /ungrouped parent/i : options.staleHead ? /raw authoring basis/i : /unavailable/i);
    expect(sourceInput('Source In')).toHaveValue('1.25');
    expect(editor.current()).toBe(before);
    expect((await editor.env.outboxes.list(scope))[0].intents).toEqual([]);
    expect(editor.env.commits()).toHaveLength(0);
    noSnapshots(editor);
    editor.view.unmount();
  });

  it('retains an out-of-bounds source value and reports the native range refusal', async () => {
    const editor = await mounted();
    const input = sourceInput('Source Out');
    act(() => input.focus());
    fireEvent.change(input, { target: { value: '11' } });
    fireEvent.blur(input);
    expect(screen.getByRole('alert')).toHaveTextContent('source range must fit inside the file');
    expect(sourceInput('Source Out')).toHaveValue('11');
    expect(editor.current().config.clips[0]).toMatchObject({ from: 2, to: 6, hold: 17 });
    expect(editor.env.commits()).toHaveLength(0);
    noSnapshots(editor);
    editor.view.unmount();
  });

  it('captures a fresh begin after an unchanged focus visit without submitting a trim', async () => {
    const editor = await mounted();
    const capture = vi.spyOn(editor.port(), 'capture');
    const input = sourceInput('Source In');
    act(() => input.focus());
    fireEvent.blur(input);
    fireEvent.focus(input);
    expect(capture).toHaveBeenCalledTimes(2);
    fireEvent.blur(input);
    expect(editor.env.commits()).toHaveLength(0);
    expect((await editor.env.outboxes.list(scope))[0].intents).toEqual([]);
    noSnapshots(editor);
    editor.view.unmount();
  });

  it('submits a keyboard step once and does not submit again on blur', async () => {
    const editor = await mounted();
    const capture = vi.spyOn(editor.port(), 'capture');
    const submit = vi.spyOn(editor.port(), 'submit');
    const input = sourceInput('Source In');
    act(() => input.focus());
    fireEvent.keyDown(input, { key: 'ArrowUp' });
    await act(async () => { await editor.session().flush(); });
    fireEvent.blur(input);
    expect(capture).toHaveBeenCalledOnce();
    expect(submit).toHaveBeenCalledOnce();
    expect(editor.env.commits()).toHaveLength(1);
    expect(editor.env.commits()[0].body!.commands[0].args).toEqual({ in_s: 2.1, out_s: null });
    noSnapshots(editor);
    editor.view.unmount();
  });

  it('retains the local source preview when outbox storage fails and retries without a new capture', async () => {
    const editor = await mounted();
    const { env, current, port, session, view } = editor;
    const capture = vi.spyOn(port(), 'capture');
    const open = env.factory.open.bind(env.factory);
    env.factory.open = () => { throw new Error('disk full'); };
    const input = sourceInput('Source In');
    act(() => input.focus());
    fireEvent.change(input, { target: { value: '1.25' } });
    fireEvent.blur(input);
    await waitFor(() => expect(session().state.status).toBe('error'));
    expect(session().state.error).toContain('disk full');
    expect(sourceInput('Source In')).toHaveValue('1.25');
    expect(current().config.clips[0]).toMatchObject({ from: 1.25, to: 6, hold: 4.75, speed: 2 });
    expect(env.commits()).toHaveLength(0);
    env.factory.open = open;
    await act(async () => { await session().retry(); });
    expect(session().state.status).toBe('saved');
    expect(env.commits()).toHaveLength(1);
    expect(capture).toHaveBeenCalledOnce();
    noSnapshots(editor);
    view.unmount();
  });

  it('keeps the original focus capture when another local command changes the generation', async () => {
    const editor = await mounted();
    const { env, current, port, paramsPort, session, view } = editor;
    const capture = vi.spyOn(port(), 'capture');
    const finish = vi.spyOn(port(), 'finish');
    const input = sourceInput('Source In');
    act(() => input.focus());
    fireEvent.change(input, { target: { value: '1.25' } });
    act(() => submitClipParamsEdit(captureClipParamsEdit(paramsPort(), current(), 'x'), { values: { note: 'local' }, clear: [] }));
    await act(async () => { await session().flush(); });
    fireEvent.blur(input);
    expect(screen.getByRole('alert')).toHaveTextContent('Timeline changed during the trim');
    expect(sourceInput('Source In')).toHaveValue('1.25');
    expect(capture).toHaveBeenCalledOnce();
    expect(finish.mock.calls[0][0]).toEqual(capture.mock.results[0].value);
    expect(env.commits()).toHaveLength(1);
    expect(env.commits()[0].body!.commands[0].op).toBe('clip.set-params');
    expect(current().config.clips[0]).toMatchObject({ from: 2, to: 6, params: { note: 'local' } });
    noSnapshots(editor);
    view.unmount();
  });

  it('retains a rejected stale-head trim in the durable outbox with its original guards', async () => {
    const editor = await mounted();
    const { env, current, port, session, view } = editor;
    const capture = vi.spyOn(port(), 'capture');
    const input = sourceInput('Source In');
    act(() => input.focus());
    fireEvent.change(input, { target: { value: '1.25' } });
    await env.external((raw) => {
      for (const clips of rawClips(raw)) clips[0].from = 3;
    });
    fireEvent.blur(input);
    await waitFor(() => expect(session().state.status).toBe('conflict'));
    expect(session().state.error).toContain('original capture');
    expect(sourceInput('Source In')).toHaveValue('1.25');
    expect(current().config.clips[0]).toMatchObject({ from: 1.25, to: 6, hold: 4.75 });
    expect(capture).toHaveBeenCalledOnce();
    expect(env.commits()).toHaveLength(1);
    const stored = (await env.outboxes.list(scope))[0];
    expect(stored.intents).toHaveLength(1);
    expect(stored.intents[0].payload).toMatchObject({ commands: [{ op: 'clip.trim', args: { in_s: 1.25, out_s: null },
      expect: { 'parent/clip:x::from': { state: 'present', value: 2 } } }] });
    noSnapshots(editor);
    view.unmount();
  });
});
