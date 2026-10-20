import { fireEvent, render, renderHook, screen, within, waitFor } from '@testing-library/react';
import { Children, isValidElement, type ComponentProps, type ReactNode } from 'react';
import { describe, expect, it, vi } from 'vitest';
import { createTimelineCommandSession } from '@/tools/video-editor/commands/commitSession.ts';
import { document, environment, scope } from '@/tools/video-editor/commands/__tests__/commitSessionEnvironment.ts';
import { captureClipScalarEdit, submitClipTransitionClears } from '@/tools/video-editor/commands/clipScalarGesture.ts';
import { captureClipMove, submitClipMove } from '@/tools/video-editor/commands/semanticGestures.ts';
import { AuthoredState } from '@/tools/video-editor/commands/clipMovePrimitives.ts';
import { compileTimelinePatch } from '@/tools/video-editor/lib/timeline-patch.ts';
import { fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import type { EditCommand } from '@/integrations/runtime/timeline-commit-types.ts';
import { RuntimeDataProvider } from '@/integrations/runtime/dataProvider.ts';
import { PROJECT_ID, TIMELINE_ID, runtimeFixture } from '@/test/fakeWorkspaceRuntime.ts';
import { useClipEditing } from '@/tools/video-editor/hooks/useClipEditing.ts';
import { useTimelineCommit } from '@/tools/video-editor/hooks/useTimelineCommit.ts';
import { TimelineEventBus } from '@/tools/video-editor/hooks/useTimelineEventBus.ts';
import { createVideoEditorEffectCatalog } from '@/tools/video-editor/lib/effect-catalog.ts';
import { buildTimelineData, type TimelineData } from '@/tools/video-editor/lib/timeline-data.ts';
import type { ParameterSchema, TimelineClip } from '@/tools/video-editor/types/index.ts';
import { BulkClipPanelBody, type BulkClipPanelProps } from './BulkClipPanelBody.tsx';
import { ClipTransitionSection } from './ClipTransitionSection.tsx';

// Keep the mounted panel, ParameterControls/SchemaForm and authoring path real;
// use native inputs only for the shared UI primitives.
vi.mock('@/shared/components/ui/number-input.tsx', () => ({
  NumberInput: ({ value, onChange }: { value: number | null; onChange: (value: number | null) => void }) => (
    <input type="number" value={value ?? ''} onChange={(event) => onChange(event.target.value === '' ? null : Number(event.target.value))} />
  ),
}));
vi.mock('@/shared/components/ui/slider.tsx', () => ({
  Slider: ({ value, onValueChange, ...props }: Omit<ComponentProps<'input'>, 'value' | 'onChange'> & {
    value: number | number[]; onValueChange: (value: number) => void;
  }) => <input {...props} type="range" value={Array.isArray(value) ? value[0] : value} onChange={(event) => onValueChange(Number(event.target.value))} />,
}));
vi.mock('@/shared/components/ui/select.tsx', () => ({
  Select: ({ value, onValueChange, children }: { value: string; onValueChange: (value: string) => void; children: ReactNode }) => (
    <select value={value} onChange={(event) => onValueChange(event.target.value)}>{children}</select>
  ),
  SelectContent: ({ children }: { children: ReactNode }) => <>{Children.toArray(children).filter((child) => !isValidElement(child) || child.type !== 'div')}</>,
  SelectItem: ({ value, children, disabled }: { value: string; children: ReactNode; disabled?: boolean }) => (
    <option value={value} disabled={disabled}>{value}</option>
  ),
  SelectTrigger: () => null,
  SelectValue: () => null,
}));

// Supply schema metadata only to the inspector snapshot. The real legacy
// canonicalizer still resolves its built-in type without a registry snapshot.
vi.mock('@/tools/video-editor/transitions/catalog.ts', async (importOriginal) => {
  const actual = await importOriginal<typeof import('@/tools/video-editor/transitions/catalog.ts')>();
  return {
    ...actual,
    resolveTransition: (...args: Parameters<typeof actual.resolveTransition>) => {
      const record = actual.resolveTransition(...args);
      return args[1] && record?.transitionId === 'crossfade' ? { ...record, schema } : record;
    },
  };
});

const schema: ParameterSchema = [
  { name: 'seed', label: 'Seed', description: '', type: 'number', default: 1 },
  { name: 'enabled', label: 'Enabled', description: '', type: 'boolean' },
  { name: 'binding', label: 'Binding', description: '', type: 'audio-binding', default: { source: 'bass', min: 0, max: 1 } },
];
const defaults = { seed: 1, enabled: false, binding: { source: 'bass', min: 0, max: 1 } };

function rawClip(id: string, at: number): TimelineClip {
  return JSON.parse(`{
    "id":"${id}","track":"V1","at":${at},"hold":4,"clipType":"hold",
    "elementRef":{"id":"crossfade","kind":"transition","revision":"${id}-revision","packId":"pack-${id}"},
    "opaqueClip":{"owner":"${id}","ordered":[null,false,0]},
    "transition":{"type":"crossfade","duration":0.5,"revision":"${id}-revision",
      "params":{"seed":8,"enabled":null,"binding":{"source":"treble","min":2,"max":9,"future":true},
        "future":{"owner":"${id}","ordered":[null,false,0,"",[],{"z":2,"a":1}]},
        "nullable":null,"__proto__":{"literal":"${id}"},"constructor":{"prototype":["${id}",null]},"prototype":false},
      "nullable":null,"future":{"owner":"${id}"},"__proto__":{"outer":"${id}"},"constructor":null,"prototype":[2,1]}
  }`);
}

async function editor(bulk: boolean, clips = [rawClip('a', 5), rawClip('b', 9)]) {
  const predecessor: TimelineClip = { id: 'predecessor', track: 'V1', at: 0, hold: 5, clipType: 'hold' };
  const fixture = runtimeFixture({ initialClips: [predecessor, ...clips] });
  const provider = new RuntimeDataProvider({ projectId: PROJECT_ID, transport: fixture.transport });
  const loaded = await provider.loadTimeline(TIMELINE_ID);
  const registry = await provider.loadAssetRegistry(TIMELINE_ID);
  const initial = await buildTimelineData(loaded.config, registry, undefined, loaded.configVersion, undefined, loaded.head);
  const before = JSON.stringify(initial);
  const rawBefore = JSON.stringify(clips);
  const saves: TimelineData[] = [];
  const patches: unknown[] = [];
  const eventBus = new TimelineEventBus();
  eventBus.on('scheduleSave', (data) => saves.push(data));
  const hook = renderHook(() => {
    const commit = useTimelineCommit({ eventBus, lastSavedSignatureRef: { current: '' }, initialData: initial });
    const editing = useClipEditing({
      dataRef: commit.dataRef, resolvedConfig: initial.resolvedConfig, selectedClipId: 'a',
      selectedTrack: initial.tracks[0], currentTime: 0, selectClip: vi.fn(), setSelectedTrackId: vi.fn(),
      applyEdit: commit.applyEdit,
    });
    return editing;
  });
  const onChange: ComponentProps<typeof ClipTransitionSection>['onChange'] = (patch) => {
    patches.push(patch);
    hook.result.current.handleSelectedClipChange(patch);
  };
  const onChangeDeep: BulkClipPanelProps['onChangeDeep'] = (patchFn) => {
    hook.result.current.handleUpdateClipsDeep(clips.map((clip) => clip.id), (meta) => {
      const patch = patchFn(meta);
      patches.push(patch);
      return patch;
    });
  };
  const selected = initial.resolvedConfig.clips.filter((clip) => clip.id !== 'predecessor');
  renderControls(bulk, selected, onChange, onChangeDeep);

  function assertAuthored(expectedClips: TimelineClip[]) {
    expect(patches).toHaveLength(bulk ? clips.length : 1);
    for (const [index, patch] of patches.entries()) {
      expect(patch).toEqual({ transition: expectedClips[index].transition });
      const transition = (patch as { transition?: TimelineClip['transition'] }).transition;
      if (transition) {
        expect(Object.keys(transition)).toEqual(Object.keys(expectedClips[index].transition!));
        expect(Object.getPrototypeOf(transition)).toBe(Object.prototype);
      }
    }
    expect(saves).toHaveLength(1);
    expect(saves[0].config.clips.map((clip) => clip.transition)).toEqual([undefined, ...expectedClips.map((clip) => clip.transition)]);
  }

  async function assertPublished(expectedClips: TimelineClip[]) {
    assertAuthored(expectedClips);
    await provider.saveTimelineAtHead(TIMELINE_ID, saves[0].config, loaded.head!, registry);
    const publications = fixture.requests.filter(({ method, path }) => method === 'POST' && path.endsWith('/composition-revisions'));
    expect(publications).toHaveLength(1);
    const body = publications[0].body as { parent_composition: { config: { clips: TimelineClip[] }; clips: TimelineClip[] } };
    const expectedWireClips = JSON.parse(JSON.stringify([predecessor, ...expectedClips]));
    const { output: _output, ...authored } = saves[0].config;
    expect(body.parent_composition.config).toEqual({ ...authored, clips: expectedWireClips });
    expect(body.parent_composition.config.clips).toEqual(expectedWireClips);
    expect(body.parent_composition.clips).toEqual(expectedWireClips);
    // Verify ordinary own JSON keys survived, without mutating any prototype.
    for (const clip of body.parent_composition.clips) {
      if (!clip.transition || clip.transition.type !== 'crossfade') continue;
      expect(Object.getPrototypeOf(clip.transition)).toBe(Object.prototype);
      expect(Object.hasOwn(clip.transition, '__proto__')).toBe(true);
      if (clip.transition.params) {
        expect(Object.getPrototypeOf(clip.transition.params)).toBe(Object.prototype);
        expect(Object.keys(clip.transition.params)).toEqual(Object.keys(expectedClips.find((expected) => expected.id === clip.id)!.transition!.params!));
        expect(Object.hasOwn(clip.transition.params, '__proto__')).toBe(Object.hasOwn(expectedClips.find((expected) => expected.id === clip.id)!.transition!.params!, '__proto__'));
      }
    }
    expect(JSON.stringify(initial)).toBe(before);
    expect(JSON.stringify(clips)).toBe(rawBefore);
    hook.unmount();
  }
  return { clips, patches, saves, assertAuthored, assertPublished };
}

function renderControls(
  bulk: boolean,
  selected: TimelineData['resolvedConfig']['clips'],
  onChange: ComponentProps<typeof ClipTransitionSection>['onChange'],
  onChangeDeep: BulkClipPanelProps['onChangeDeep'],
  capture?: (id: string) => ReturnType<typeof captureClipScalarEdit>,
) {
  const first = selected[0];
  render(<>{bulk ? <BulkClipPanelBody
    clips={selected} visibleTabs={['effects']} activeTab="effects" setActiveTab={vi.fn()}
    compositionWidth={1920} compositionHeight={1080} effectResources={createVideoEditorEffectCatalog()}
    sharedEntrance={null} sharedExit={null} sharedContinuous={null} sharedText={null}
    sharedEntranceType={null} sharedExitType={null} sharedContinuousType={null}
    sharedTransition={first.transition!} sharedTransitionType="crossfade"
    sharedTransitionDuration={selected.every((clip) => clip.transition?.duration === first.transition?.duration) ? first.transition!.duration : null}
    sharedSpeed={null} sharedFrom={null} sharedTo={null} sharedX={null} sharedY={null}
    sharedWidth={null} sharedHeight={null} sharedOpacity={null} sharedVolume={null}
    sharedFontSize={null} sharedTextColor={null}
    onScalarEditsStart={capture ? () => selected.map((clip) => capture(clip.id)) : undefined}
    onChange={vi.fn()} onChangeDeep={onChangeDeep} onResetPosition={vi.fn()} onToggleMute={vi.fn()} onClose={vi.fn()}
  /> : <ClipTransitionSection clip={first} onChange={onChange} onScalarEditStart={capture ? () => capture(first.id) : undefined} />}</>);
}

async function nativeEditor(bulk: boolean) {
  // The same input and expected removal as the two original RED publication cases.
  const clips = [rawClip('a', 5), rawClip('b', 9)];
  const predecessor: TimelineClip = { id: 'predecessor', track: 'V1', at: 0, hold: 5, clipType: 'hold' };
  const raw = document();
  const parent = raw.parent_revision.payload;
  parent.clips = JSON.parse(JSON.stringify([predecessor, ...clips]));
  parent.config = { ...parent.config as object, clips: structuredClone(parent.clips) };
  raw.parent_revision.content_digest = fixtureDigest(parent);
  const env = await environment(raw);
  let current = env.current();
  const snapshots = vi.fn();
  const save = vi.spyOn(env.provider, 'saveTimelineAtHead');
  const mount = () => createTimelineCommandSession({ scope, initial: env.initial, outboxes: env.outboxes,
    send: (request, key) => env.provider.commitTimeline(request, key),
    preview: (patch) => {
      const compiled = compileTimelinePatch(patch, current);
      if (!compiled.nextData) throw new Error('invalid native clear preview');
      current = compiled.nextData;
    },
    project: async (basis, previews) => {
      const payload = basis.canonicalDocument.parent_revision.payload;
      current = await buildTimelineData({ ...payload.config as object, clips: payload.clips } as never,
        { assets: {} }, undefined, 1, undefined, { projectId: scope.projectId, timelineId: scope.timelineId,
          headRevisionId: basis.head.revisionId, headPublicationId: basis.head.publicationId });
      for (const preview of previews) {
        const compiled = compileTimelinePatch(preview, current);
        if (!compiled.nextData) throw new Error('invalid recovered native clear preview');
        current = compiled.nextData;
      }
    }, changed: () => {},
  });
  const session = await mount();
  const selected = current.resolvedConfig.clips.filter((clip) => clip.id !== 'predecessor');
  renderControls(bulk, selected, snapshots, snapshots, (id) => captureClipScalarEdit(session.clipScalarPort, current, id));
  return { env, session, mount, current: () => current, clips, predecessor, snapshots, save };
}

function transitionSection() {
  return screen.getByText('Transition').closest('div.space-y-2') as HTMLElement;
}

describe('mounted transition callbacks preserve raw authoring through publication', () => {
  it.each(['seed', '__proto__', 'constructor', 'prototype'])('single parameter %s changes only that own key', async (name) => {
    // Also exercise legal schema names that look like prototype properties.
    const extra = name === 'seed' ? [] : [{ name, label: name, description: '', type: 'number' as const, default: 2 }];
    schema.push(...extra);
    try {
      const { clips, assertPublished } = await editor(false);
      fireEvent.change(screen.getByTestId(`schema-form-widget-${name}`), { target: { value: '4' } });
      const expected = clips.map((clip, index) => index ? clip : { ...clip, transition: {
        ...clip.transition!, params: { ...clip.transition!.params, [name]: 4 },
      } });
      await assertPublished(expected);
    } finally {
      if (extra.length) schema.pop();
    }
  });

  it.each([false, true])('reset (bulk=%s) replaces known defaults and keeps each clip’s unrelated JSON', async (bulk) => {
    const { clips, assertPublished } = await editor(bulk);
    fireEvent.click(screen.getByRole('button', { name: /Reset defaults/ }));
    await assertPublished(clips.map((clip, index) => !bulk && index ? clip : { ...clip, transition: {
      ...clip.transition!, params: { ...clip.transition!.params, ...defaults },
    } }));
  });

  it('bulk reset keeps different durations and each clip’s own opaque data', async () => {
    const clips = [rawClip('a', 5), rawClip('b', 9)];
    clips[1].transition!.duration = 1.25;
    const { assertPublished } = await editor(true, clips);
    fireEvent.click(screen.getByRole('button', { name: /Reset defaults/ }));
    await assertPublished(clips.map((clip) => ({ ...clip, transition: {
      ...clip.transition!, params: { ...clip.transition!.params, ...defaults },
    } })));
  });

  it.each([false, true])('reset (bulk=%s) materializes known prototype-looking keys as own data', async (bulk) => {
    const names = ['__proto__', 'constructor', 'prototype'];
    schema.push(...names.map((name) => ({ name, label: name, description: '', type: 'number' as const, default: 2 })));
    try {
      const { clips, assertPublished } = await editor(bulk);
      fireEvent.click(screen.getByRole('button', { name: /Reset defaults/ }));
      await assertPublished(clips.map((clip, index) => !bulk && index ? clip : { ...clip, transition: {
        ...clip.transition!, params: { ...clip.transition!.params, ...defaults, ['__proto__']: 2, constructor: 2, prototype: 2 },
      } }));
    } finally {
      schema.splice(-names.length);
    }
  });

  it.each([false, true])('duration (bulk=%s) preserves each raw transition and params', async (bulk) => {
    const { clips, assertPublished } = await editor(bulk);
    fireEvent.change(within(transitionSection()).getAllByRole('spinbutton')[0], { target: { value: '0.75' } });
    await assertPublished(clips.map((clip, index) => !bulk && index ? clip : { ...clip, transition: { ...clip.transition!, duration: 0.75 } }));
  });

  it.each(['absent', 'null'] as const)('bulk duration retains %s params instead of copying first clip params', async (presence) => {
    const clips = [rawClip('a', 5), rawClip('b', 9)];
    if (presence === 'absent') delete clips[1].transition!.params;
    else Object.defineProperty(clips[1].transition, 'params', { value: null, enumerable: true, writable: true });
    const { assertPublished } = await editor(true, clips);
    fireEvent.change(within(transitionSection()).getByRole('spinbutton'), { target: { value: '0.75' } });
    await assertPublished(clips.map((clip) => ({ ...clip, transition: { ...clip.transition!, duration: 0.75 } })));
  });

  it.each(['absent', 'null'] as const)('single parameter edit preserves raw presence around %s params', async (presence) => {
    const clips = [rawClip('a', 5), rawClip('b', 9)];
    if (presence === 'absent') delete clips[0].transition!.params;
    else Object.defineProperty(clips[0].transition, 'params', { value: null, enumerable: true, writable: true });
    const { assertPublished } = await editor(false, clips);
    fireEvent.change(screen.getByTestId('schema-form-widget-seed'), { target: { value: '4' } });
    await assertPublished(clips.map((clip, index) => index ? clip : {
      ...clip, transition: { ...clip.transition!, params: { seed: 4 } },
    }));
  });

  it.each([false, true])('reset (bulk=%s) materializes defaults from absent/null params', async (bulk) => {
    const clips = [rawClip('a', 5), rawClip('b', 9)];
    delete clips[0].transition!.params;
    Object.defineProperty(clips[1].transition, 'params', { value: null, enumerable: true, writable: true });
    const { assertPublished } = await editor(bulk, clips);
    fireEvent.click(screen.getByRole('button', { name: /Reset defaults/ }));
    await assertPublished(clips.map((clip, index) => !bulk && index ? clip : {
      ...clip, transition: { ...clip.transition!, params: defaults },
    }));
  });

  it.each([false, true])('None (bulk=%s) refuses without command authority and keeps the draft', async (bulk) => {
    const { clips, patches, saves } = await editor(bulk);
    fireEvent.change(within(transitionSection()).getAllByRole('combobox')[0], { target: { value: '__none__' } });
    expect(screen.getAllByRole('alert').some((alert) => alert.textContent === (
      bulk
        ? 'Bulk transition clear requires an active timeline command session.'
        : 'Transition clear requires an active timeline command session.'
    ))).toBe(true);
    expect(patches).toHaveLength(0);
    expect(saves).toHaveLength(0);
    expect(clips.every((clip) => clip.transition?.type === 'crossfade')).toBe(true);
  });

  it.each([false, true])('type change (bulk=%s) starts a new transition without carrying old binding', async (bulk) => {
    const { clips, assertPublished } = await editor(bulk);
    fireEvent.change(within(transitionSection()).getAllByRole('combobox')[0], { target: { value: 'wipe' } });
    await assertPublished(clips.map((clip, index) => !bulk && index ? clip : {
      ...clip, transition: { type: 'wipe', duration: 0.5, params: undefined },
    }));
  });
});


describe('native None publication (unit transport; no Runtime registry acceptance claim)', () => {
  it.each([false, true])('None publication (bulk=%s) removes the raw transition', async (bulk) => {
    const host = await nativeEditor(bulk);
    const before = JSON.stringify(host.current());
    const paused = host.env.pause();
    fireEvent.change(within(transitionSection()).getAllByRole('combobox')[0], { target: { value: '__none__' } });
    await waitFor(() => expect(host.env.commits()).toHaveLength(1));
    const expectedClips = host.clips.map((clip, index) => {
      if (!bulk && index) return clip;
      const { transition: _transition, ...rest } = clip;
      return rest;
    });
    const expected = [host.predecessor, ...expectedClips];
    const [stored] = await host.env.outboxes.list(scope);
    expect(stored.intents).toHaveLength(1);
    const payload = stored.intents[0].payload as { commands: EditCommand[]; after: never };
    expect(payload.commands).toHaveLength(bulk ? 2 : 1);
    expect(JSON.parse(stored.pending!.request.body).commands).toEqual(payload.commands);
    for (const [index, command] of payload.commands.entries()) {
      const clip = host.clips[index];
      expect(command).toMatchObject({ op: 'clip.set', version: '1', select: `parent/clip:${clip.id}`,
        args: { values: {}, clear: ['transition'] },
        expect: { [`parent/clip:${clip.id}::transition`]: { state: 'present', value: clip.transition } } });
    }
    expect(new AuthoredState(payload.after).bundle.parent.clips).toEqual(expected);
    expect(host.current().config.clips).toEqual(expected);
    paused.resolve();
    await host.session.flush();
    const accepted = await host.env.provider.loadTimelineCommandBasis(scope.timelineId);
    const parent = accepted.canonicalDocument.parent_revision.payload;
    expect(parent.clips).toEqual(expected);
    expect((parent.config as { clips: unknown }).clips).toEqual(expected);
    expect(JSON.stringify(parent.clips)).toBe(JSON.stringify(expected));
    expect(JSON.stringify((parent.config as { clips: unknown }).clips)).toBe(JSON.stringify(expected));
    expect(host.snapshots).not.toHaveBeenCalled();
    expect(host.save).not.toHaveBeenCalled();
    expect(host.current()).not.toEqual(JSON.parse(before));
    await host.session.dispose();
  });

  it('bulk Remove submits one atomic clear batch', async () => {
    const host = await nativeEditor(true);
    fireEvent.click(within(transitionSection()).getByRole('button', { name: 'Remove' }));
    await host.session.flush();
    await waitFor(() => expect(host.env.commits()).toHaveLength(1));
    expect(host.env.commits()[0].body!.commands).toHaveLength(2);
    const accepted = await host.env.provider.loadTimelineCommandBasis(scope.timelineId);
    expect((accepted.canonicalDocument.parent_revision.payload.clips as TimelineClip[]).slice(1)
      .every((clip) => !Object.prototype.hasOwnProperty.call(clip, 'transition'))).toBe(true);
    expect(host.snapshots).not.toHaveBeenCalled();
    await host.session.dispose();
  });

  it('bulk None visibly refuses an unsupported selected target without clearing any clip', async () => {
    const host = await nativeEditor(true);
    const before = structuredClone(host.current());
    const records = await host.env.outboxes.list(scope);
    const capture = host.session.clipScalarPort.capture;
    host.session.clipScalarPort.capture = (input) => {
      if (input.clipId === 'b') throw new Error('Unsupported selected target; draft retained');
      return capture(input);
    };
    fireEvent.change(within(transitionSection()).getAllByRole('combobox')[0], { target: { value: '__none__' } });
    expect(screen.getByRole('alert')).toHaveTextContent('Unsupported selected target; draft retained');
    expect(host.current()).toEqual(before);
    expect(await host.env.outboxes.list(scope)).toEqual(records);
    expect(host.env.commits()).toHaveLength(0);
    expect(host.snapshots).not.toHaveBeenCalled();
    await host.session.dispose();
  });

  it('retains an entire refused batch and exact request through restart and retry', async () => {
    const host = await nativeEditor(true);
    host.env.setFault('validation');
    fireEvent.change(within(transitionSection()).getAllByRole('combobox')[0], { target: { value: '__none__' } });
    await waitFor(() => expect(host.session.getState().status).toBe('error'));
    const [original] = await host.env.outboxes.list(scope);
    const request = original.pending!.request;
    expect(host.current().config.clips.slice(1).every((clip) => !Object.prototype.hasOwnProperty.call(clip, 'transition'))).toBe(true);
    expect((await host.env.provider.loadTimelineCommandBasis(scope.timelineId)).canonicalDocument.parent_revision.payload.clips)
      .toEqual([host.predecessor, ...host.clips]);
    await host.session.dispose();
    const recovered = await host.mount();
    expect(recovered.getState().status).toBe('recovery');
    await recovered.recover(original.ownerId);
    const expected = [host.predecessor, ...host.clips.map(({ transition: _transition, ...clip }) => clip)];
    expect(host.current().config.clips).toEqual(expected);
    expect(host.current().resolvedConfig.clips).toEqual(expected);
    const accepted = (await host.env.provider.loadTimelineCommandBasis(scope.timelineId)).canonicalDocument.parent_revision.payload;
    expect(accepted.clips).toEqual([host.predecessor, ...host.clips]);
    expect((accepted.config as { clips: unknown }).clips).toEqual([host.predecessor, ...host.clips]);
    expect((await host.env.outboxes.list(scope))[0].pending!.request).toEqual(request);
    expect((await host.env.outboxes.list(scope))[0].intents).toEqual(original.intents);
    // A definitive rejection remains retained until explicit resolution.
    await recovered.retry();
    expect(host.env.commits()).toHaveLength(1);
    expect(host.snapshots).not.toHaveBeenCalled();
    await recovered.dispose();
  });

  it('retries a lost batch ACK exactly and preserves a newer mixed suffix with original guards', async () => {
    const host = await nativeEditor(true);
    host.env.setFault('lost');
    fireEvent.change(within(transitionSection()).getAllByRole('combobox')[0], { target: { value: '__none__' } });
    await waitFor(() => expect(host.session.getState().status).toBe('retry'));
    const [original] = await host.env.outboxes.list(scope);
    const request = original.pending!.request;
    const retry = host.env.pause();
    submitClipMove(captureClipMove(host.session.port, host.current(), 'b'), 14);
    await waitFor(async () => expect((await host.env.outboxes.list(scope))[0].intents).toHaveLength(2));
    const [queued] = await host.env.outboxes.list(scope);
    const suffix = queued.intents[1];
    expect(queued.pending!.request).toEqual(request);
    expect(queued.intents[0]).toEqual(original.intents[0]);
    retry.resolve();
    await host.session.flush();
    expect(host.env.commits()).toHaveLength(3);
    expect(JSON.stringify(host.env.commits()[1].body)).toBe(request.body);
    expect(host.env.commits()[1].key).toBe(request.key);
    expect(host.env.commits()[2].body!.commands).toEqual((suffix.payload as { commands: EditCommand[] }).commands);
    expect(host.env.commits()[2].body).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p1' });
    expect(host.current().config.clips.find((clip) => clip.id === 'b')).toMatchObject({ at: 14 });
    expect(host.current().config.clips.slice(1).every((clip) => !Object.prototype.hasOwnProperty.call(clip, 'transition'))).toBe(true);
    expect(host.snapshots).not.toHaveBeenCalled();
    await host.session.dispose();
  });

  it('refuses a batch containing a missing raw target atomically and keeps the existing draft', async () => {
    const host = await nativeEditor(true);
    host.env.setFault('unavailable');
    submitClipMove(captureClipMove(host.session.port, host.current(), 'a'), 6);
    await waitFor(() => expect(host.session.getState().status).toBe('retry'));
    const before = structuredClone(host.current());
    const records = await host.env.outboxes.list(scope);
    const first = captureClipScalarEdit(host.session.clipScalarPort, host.current(), 'a');
    const second = captureClipScalarEdit(host.session.clipScalarPort, host.current(), 'b');
    const bad = { ...second, basis: { ...second.basis, select: 'parent/clip:missing' } };
    expect(() => submitClipTransitionClears([first, bad])).toThrow();
    expect(host.current()).toEqual(before);
    expect(await host.env.outboxes.list(scope)).toEqual(records);
    expect(host.env.commits()).toHaveLength(1);
    expect(() => host.session.clipScalarPort.finishBatch!([first.basis, second.basis],
      { values: { hold: 7 }, clear: ['transition'] })).toThrow('only explicit transition clears');
    expect(host.current()).toEqual(before);
    expect(await host.env.outboxes.list(scope)).toEqual(records);
    expect(host.snapshots).not.toHaveBeenCalled();
    await host.session.dispose();
  });
});
