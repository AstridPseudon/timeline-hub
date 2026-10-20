// @vitest-environment jsdom

import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { AgentChatProvider } from '@/shared/contexts/AgentChatContext.tsx';
import { fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import type { AgentState } from '@/integrations/runtime/timeline-commit-types.ts';
import { document as commandDocument, environment, scope } from '@/tools/video-editor/commands/__tests__/commitSessionEnvironment.ts';
import { captureClipParamsEdit, submitClipParamsEdit } from '@/tools/video-editor/commands/clipParamsGesture.ts';
import { VideoEditorProvider } from '@/tools/video-editor/contexts/VideoEditorProvider.tsx';
import { useTimelineEditorData, useTimelineEditorOps } from '@/tools/video-editor/hooks/timelineStore.ts';
import * as commandSession from '@/tools/video-editor/hooks/useTimelineCommandSession.ts';
import type { AvailableSequenceMetadata } from '@/tools/video-editor/sequences/registry.ts';
import { SequenceParamEditor } from './SequenceParamEditor.tsx';

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

const metadata: AvailableSequenceMetadata = {
  clipType: 'unregistered-test-sequence', themeId: 'test', label: 'Discrete params',
  description: 'Native params fixture.', whenToUse: 'Test.',
  hold: { defaultSeconds: 1, minSeconds: 1, maxSeconds: 4, stepSeconds: 1 },
  params: [
    { key: 'assets', label: 'Assets', kind: 'asset-list', description: 'Assets.' },
    { key: 'keyframes', label: 'Keyframes', kind: 'json', description: 'Frames.' },
  ],
};
const initialParams = { assets: ['asset-a'], keyframes: [{ at: 0 }], opaque: { keep: [null, false, 0, []] } };

async function mounted(legacyGroup = false, params: AgentState = { state: 'present', value: initialParams }) {
  const raw = commandDocument();
  for (const clips of [raw.parent_revision.payload.clips, raw.parent_revision.payload.config.clips]) {
    const clip = (clips as Array<Record<string, unknown>>)[0];
    if (params.state === 'absent') delete clip.params;
    else clip.params = structuredClone(params.value);
  }
  raw.parent_revision.payload.config.x_opaque = { untouched: [null, false, []] };
  if (legacyGroup) raw.parent_revision.payload.config.pinnedShotGroups = [
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
    return <SequenceParamEditor clipType={metadata.clipType} metadata={metadata}
      params={current.config.clips[0].params} registry={{ 'asset-a': {}, 'asset-b': {} }}
      current={current} clipId="x" clipParamsPort={ops.clipParams} onChange={onChange} />;
  }
  const client = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: false } } });
  const view = render(<QueryClientProvider client={client}><MemoryRouter><AgentChatProvider>
    <VideoEditorProvider dataProvider={env.provider} projectId={scope.projectId}
      timelineId={scope.timelineId} userId={null} initialTimelineData={env.current()}>
      <Inspector />
    </VideoEditorProvider>
  </AgentChatProvider></MemoryRouter></QueryClientProvider>);
  const session = () => hook.mock.results.at(-1)!.value as ReturnType<typeof commandSession.useTimelineCommandSession>;
  await waitFor(() => expect(ops.clipParams).toBeDefined());
  await waitFor(() => expect(screen.getByPlaceholderText('asset-key-a, asset-key-b')).toBeEnabled());
  expect(ops.clipParams).toBe(session().clipParamsPort);
  return { env, original, view, onChange, saveTimeline, saveTimelineAtHead, session,
    current: () => editor.data!, port: () => ops.clipParams! };
}

describe('mounted sequence params through the provider and native command outbox', () => {
  it.each<AgentState>([{ state: 'absent' }, { state: 'present', value: null }, { state: 'present', value: {} }])(
    'submits a mounted port clear from $state/$value without a local patch or snapshot save', async (params) => {
      const { env, original, session, current, port, view, onChange, saveTimeline, saveTimelineAtHead } = await mounted(false, params);
      const before = current();
      const finish = vi.spyOn(port(), 'finish');
      const submit = vi.spyOn(port(), 'submit');
      const gate = env.pause();
      // The inspector hides Clear for absent leaves; exercise its same mounted port directly.
      act(() => submitClipParamsEdit(captureClipParamsEdit(port(), before, 'x'), { values: {}, clear: ['keyframes'] }));
      await waitFor(() => expect(env.commits()).toHaveLength(1));
      expect(finish).toHaveBeenCalledOnce();
      expect(finish.mock.results[0].value.previewParams).toBeNull();
      expect(submit).toHaveBeenCalledExactlyOnceWith({ command: env.commits()[0].body!.commands[0], preview: null });
      expect(env.commits()[0].body!.commands[0]).toMatchObject({ op: 'clip.set-params', args: { values: {}, clear: ['keyframes'] },
        expect: { 'parent/clip:x::params.keyframes': { state: 'absent' } },
        authorship: { 'parent/clip:x::params.keyframes': 'direct' } });
      expect(current()).toBe(before);
      expect((await env.outboxes.list(scope))[0].intents[0].payload).toMatchObject({ preview: null });
      await act(async () => { gate.resolve(); await session().flush(); });
      expect(session().state.status).toBe('saved');
      expect(current().editProjection).toMatchObject({ kind: 'accepted', head: { revisionId: 'r0', publicationId: 'p1' } });
      const accepted = await env.provider.loadTimelineCommandBasis(scope.timelineId);
      expect(accepted.canonicalDocument.parent_revision.payload).toEqual(original.parent_revision.payload);
      expect(env.commits()).toHaveLength(1);
      expect(onChange).not.toHaveBeenCalled();
      expect(saveTimeline).not.toHaveBeenCalled();
      expect(saveTimelineAtHead).not.toHaveBeenCalled();
      expect(env.calls.filter((call) => call.method !== 'GET').map((call) => call.path))
        .toEqual(['/v1/handshake', expect.stringMatching(/\/commit$/)]);
      view.unmount();
    },
  );
  it.each(['assets', 'clear'] as const)('captures the original snapshot for %s and sends no snapshot traffic', async (gesture) => {
    const mountedEditor = await mounted();
    const { env, original, session, current, port, view, onChange, saveTimeline, saveTimelineAtHead } = mountedEditor;
    const before = current();
    const capture = vi.spyOn(port(), 'capture');
    const finish = vi.spyOn(port(), 'finish');
    const submit = vi.spyOn(port(), 'submit');
    const gate = env.pause();
    if (gesture === 'assets') {
      fireEvent.change(screen.getByPlaceholderText('asset-key-a, asset-key-b'), { target: { value: 'asset-b, asset-a, asset-b' } });
    } else fireEvent.click(screen.getByRole('button', { name: 'Clear' }));
    await waitFor(() => expect(env.commits()).toHaveLength(1));
    expect(capture).toHaveBeenCalledExactlyOnceWith({ clipId: 'x', current: before });
    expect(finish).toHaveBeenCalledOnce();
    expect(submit).toHaveBeenCalledOnce();
    const args = gesture === 'assets' ? { values: { assets: ['asset-b', 'asset-a', 'asset-b'] }, clear: [] }
      : { values: {}, clear: ['keyframes'] };
    const command = env.commits()[0].body!.commands[0];
    expect(command).toMatchObject({ op: 'clip.set-params', version: '1', select: 'parent/clip:x', args });
    expect(command.expect).toMatchObject(gesture === 'assets'
      ? { 'parent/clip:x::params.assets': { state: 'present', value: initialParams.assets } }
      : { 'parent/clip:x::params.keyframes': { state: 'present', value: initialParams.keyframes } });
    expect(env.commits()[0].body).toMatchObject({ base_revision_id: 'r0', base_publication_id: 'p0' });
    const outbox = (await env.outboxes.list(scope))[0];
    expect(JSON.parse(outbox.pending!.request.body)).toEqual(env.commits()[0].body);
    expect(outbox.pending!.request.key).toBe(env.commits()[0].key);
    const expectedParams = gesture === 'assets' ? { ...initialParams, assets: args.values.assets }
      : { assets: initialParams.assets, opaque: initialParams.opaque };
    expect(current().config.clips[0].params).toEqual(expectedParams);
    expect(current().editProjection).toMatchObject({ kind: 'local' });
    await act(async () => { gate.resolve(); await session().flush(); });
    expect(current().config.clips[0].params).toEqual(expectedParams);
    expect(current().editProjection).toMatchObject({ kind: 'accepted', head: { publicationId: 'p1' } });
    const accepted = await env.provider.loadTimelineCommandBasis(scope.timelineId);
    const expected = structuredClone(original);
    for (const clips of [expected.parent_revision.payload.clips, expected.parent_revision.payload.config.clips]) {
      (clips as Array<Record<string, unknown>>)[0].params = expectedParams;
    }
    expect(accepted.canonicalDocument.parent_revision.payload).toEqual(expected.parent_revision.payload);
    expect(before.config.clips[0].params).toEqual(initialParams);
    // Display normalization infers "text"; native reads still use the absent raw field.
    expect(before.config.clips[0].clipType).toBe('text');
    expect(command.reads).toContainEqual({ ref: 'parent/clip:x', path: ['clipType'], state: { state: 'absent' } });
    expect(onChange).not.toHaveBeenCalled();
    expect(saveTimeline).not.toHaveBeenCalled();
    expect(saveTimelineAtHead).not.toHaveBeenCalled();
    expect(env.calls.filter((call) => call.method !== 'GET').map((call) => call.path))
      .toEqual(['/v1/handshake', expect.stringMatching(/\/commit$/)]);
    view.unmount();
  });

  it('keeps values visible when the native session cannot address a legacy group owner', async () => {
    const { env, current, view, onChange, saveTimeline, saveTimelineAtHead } = await mounted(true);
    const before = current();
    fireEvent.change(screen.getByPlaceholderText('asset-key-a, asset-key-b'), { target: { value: 'asset-b' } });
    expect(screen.getByRole('alert')).toHaveTextContent('Clip parameters require one unambiguous raw clip identity');
    expect(screen.getByPlaceholderText('asset-key-a, asset-key-b')).toHaveValue('asset-a');
    fireEvent.click(screen.getByRole('button', { name: 'Clear' }));
    expect(screen.getByRole('alert')).toHaveTextContent('Clip parameters require one unambiguous raw clip identity');
    expect(screen.getByRole('textbox', { name: 'Keyframes' })).toHaveValue(JSON.stringify(initialParams.keyframes, null, 2));
    expect(current()).toBe(before);
    expect((await env.outboxes.list(scope))[0].intents).toEqual([]);
    expect(env.commits()).toHaveLength(0);
    expect(onChange).not.toHaveBeenCalled();
    expect(saveTimeline).not.toHaveBeenCalled();
    expect(saveTimelineAtHead).not.toHaveBeenCalled();
    view.unmount();
  });

  it.each(['capture', 'finish', 'submit'] as const)('keeps both displayed values when the native %s port throws', async (stage) => {
    const { env, current, port, view, onChange, saveTimeline, saveTimelineAtHead } = await mounted();
    const before = current();
    vi.spyOn(port(), stage).mockImplementation(() => { throw new Error(`Native ${stage} unavailable`); });
    fireEvent.change(screen.getByPlaceholderText('asset-key-a, asset-key-b'), { target: { value: 'asset-b' } });
    expect(screen.getByRole('alert')).toHaveTextContent(`Native ${stage} unavailable`);
    expect(screen.getByPlaceholderText('asset-key-a, asset-key-b')).toHaveValue('asset-a');
    fireEvent.click(screen.getByRole('button', { name: 'Clear' }));
    expect(screen.getByRole('alert')).toHaveTextContent(`Native ${stage} unavailable`);
    expect(screen.getByRole('textbox', { name: 'Keyframes' })).toHaveValue(JSON.stringify(initialParams.keyframes, null, 2));
    expect(current()).toBe(before);
    expect((await env.outboxes.list(scope))[0].intents).toEqual([]);
    expect((await env.outboxes.list(scope))[0].pending).toBeUndefined();
    expect(env.commits()).toHaveLength(0);
    expect(onChange).not.toHaveBeenCalled();
    expect(saveTimeline).not.toHaveBeenCalled();
    expect(saveTimelineAtHead).not.toHaveBeenCalled();
    view.unmount();
  });
});
