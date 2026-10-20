import { fireEvent, render, renderHook, screen, within } from '@testing-library/react';
import { Children, isValidElement, type ComponentProps, type ReactNode } from 'react';
import { describe, expect, it, vi } from 'vitest';
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
  const first = selected[0];
  render(<>{bulk ? <BulkClipPanelBody
    clips={selected} visibleTabs={['effects']} activeTab="effects" setActiveTab={vi.fn()}
    compositionWidth={1920} compositionHeight={1080} effectResources={createVideoEditorEffectCatalog()}
    sharedEntrance={null} sharedExit={null} sharedContinuous={null} sharedText={null}
    sharedEntranceType={null} sharedExitType={null} sharedContinuousType={null}
    sharedTransition={first.transition!} sharedTransitionType="crossfade"
    sharedTransitionDuration={clips.every((clip) => clip.transition?.duration === first.transition?.duration) ? first.transition!.duration : null}
    sharedSpeed={null} sharedFrom={null} sharedTo={null} sharedX={null} sharedY={null}
    sharedWidth={null} sharedHeight={null} sharedOpacity={null} sharedVolume={null}
    sharedFontSize={null} sharedTextColor={null}
    onChange={vi.fn()} onChangeDeep={onChangeDeep} onResetPosition={vi.fn()} onToggleMute={vi.fn()} onClose={vi.fn()}
  /> : <ClipTransitionSection clip={first} onChange={onChange} />}</>);

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
  return { clips, patches, assertAuthored, assertPublished };
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

  it.each([false, true])('None (bulk=%s) explicitly clears only the transition', async (bulk) => {
    const { clips, patches, assertAuthored } = await editor(bulk);
    fireEvent.change(within(transitionSection()).getAllByRole('combobox')[0], { target: { value: '__none__' } });
    expect(patches.every((patch) => Object.hasOwn(patch as object, 'transition'))).toBe(true);
    assertAuthored(clips.map((clip, index) => {
      if (!bulk && index) return clip;
      const { transition: _transition, ...rest } = clip;
      return rest;
    }));
  });

  // Requirement: rowsToConfig must retain the explicit undefined transition
  // until RuntimeDataProvider can remove it from the immutable raw basis.
  it.fails.each([false, true])('None publication (bulk=%s) removes the raw transition', async (bulk) => {
    const { clips, assertPublished } = await editor(bulk);
    fireEvent.change(within(transitionSection()).getAllByRole('combobox')[0], { target: { value: '__none__' } });
    await assertPublished(clips.map((clip, index) => {
      if (!bulk && index) return clip;
      const { transition: _transition, ...rest } = clip;
      return rest;
    }));
  });

  it.each([false, true])('type change (bulk=%s) starts a new transition without carrying old binding', async (bulk) => {
    const { clips, assertPublished } = await editor(bulk);
    fireEvent.change(within(transitionSection()).getAllByRole('combobox')[0], { target: { value: 'wipe' } });
    await assertPublished(clips.map((clip, index) => !bulk && index ? clip : {
      ...clip, transition: { type: 'wipe', duration: 0.5, params: undefined },
    }));
  });
});
