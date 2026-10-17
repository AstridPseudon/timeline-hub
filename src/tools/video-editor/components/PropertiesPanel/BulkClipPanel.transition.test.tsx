// @vitest-environment jsdom

import { useEffect, type ReactNode } from 'react';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import type { ComponentProps } from 'react';
import { BulkClipPanelBody } from '@/tools/video-editor/components/PropertiesPanel/BulkClipPanelBody.tsx';
import { useClipEditing } from '@/tools/video-editor/hooks/useClipEditing.ts';
import { configToRows } from '@/tools/video-editor/lib/timeline-data.ts';
import type { ClipMeta, TimelineData } from '@/tools/video-editor/lib/timeline-data.ts';
import { repairConfig } from '@/tools/video-editor/lib/migrate.ts';
import type { TimelineApplyEdit } from '@/tools/video-editor/hooks/timeline-state-types.ts';
import type {
  AstridElementDescriptor,
  AstridElementHost,
} from '@/tools/video-editor/runtime/astrid-element-host.ts';
import type { ResolvedTimelineClip, TimelineClip, TimelineConfig } from '@/tools/video-editor/types/index.ts';
import {
  TransitionRegistryProvider,
  useTransitionRegistryContext,
  type TransitionRegistryRecord,
} from '@/tools/video-editor/transitions/registry/index.ts';

const runtimeContextMock = vi.hoisted(() => ({
  value: null as null | { astridElementHost: unknown },
}));

vi.mock('@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx', async (importOriginal) => ({
  ...await importOriginal<typeof import('@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx')>(),
  useOptionalVideoEditorRuntime: () => runtimeContextMock.value,
}));

vi.mock('@/shared/components/ui/number-input', () => ({
  NumberInput: ({ onChange, value, min, max, step }: {
    onChange: (value: number | null) => void;
    value: number | null;
    min?: number;
    max?: number;
    step?: number;
  }) => (
    <input
      role="spinbutton"
      value={value ?? ''}
      min={min}
      max={max}
      step={step}
      onChange={(event) => onChange(event.currentTarget.value === '' ? null : Number(event.currentTarget.value))}
    />
  ),
}));

vi.mock('@banodoco/timeline-composition/registry.generated', () => ({
  THEME_PACKAGE_REGISTRY: {},
}), { virtual: true });

const transitionId = 'test:bulk-wipe';
const transitionRevision = 'host-transition-r7';

function makeRecord(): TransitionRegistryRecord {
  return {
    transitionId,
    contributionId: 'test-extension:bulk-wipe',
    renderer: (() => ({})) as TransitionRegistryRecord['renderer'],
    schema: [{ name: 'amount', type: 'number', min: 0.25, max: 1 }],
    provenance: 'bundled-extension',
    ownerExtensionId: 'test-extension',
    renderability: {
      defaultRoute: 'preview',
      determinism: 'deterministic',
      capabilities: [{ route: 'preview', status: 'supported', determinism: 'deterministic' }],
    },
    status: 'active',
  } as TransitionRegistryRecord;
}

function InstallRecord({ record, children }: { record: TransitionRegistryRecord; children: ReactNode }) {
  const { registry } = useTransitionRegistryContext();
  useEffect(() => {
    const registration = registry.register(record);
    return () => registration.dispose();
  }, [record, registry]);
  return children;
}

function makeDescriptor(id: string, revision: string): AstridElementDescriptor {
  return {
    id,
    kind: 'transition',
    packId: 'test-pack',
    revision,
    componentPath: 'transitions/bulk-wipe.tsx',
  };
}

function makeElementHost(descriptors: readonly AstridElementDescriptor[]): AstridElementHost {
  const component = () => null;
  return {
    descriptors,
    sequenceRegistry: {},
    resolveComponent: (id, kind, packId) => descriptors.some((descriptor) => descriptor.id === id
      && descriptor.kind === kind && (packId === undefined || descriptor.packId === packId)) ? component : undefined,
    resolveSequenceClipEntry: () => undefined,
    describeClipCapability: () => undefined,
  };
}

function makeClip(id: string, at: number, track: string, transition?: TimelineClip['transition'], elementRef?: TimelineClip['elementRef']): TimelineClip {
  return {
    id,
    at,
    track,
    clipType: 'hold',
    hold: 2,
    ...(transition !== undefined ? { transition } : {}),
    ...(elementRef !== undefined ? { elementRef } : {}),
  } as TimelineClip;
}

function makeTimelineData(clips: TimelineClip[]): TimelineData {
  const config = repairConfig({
    output: { resolution: '1920x1080', fps: 30, file: 'out.mp4' },
    tracks: [
      { id: 'V1', kind: 'visual', label: 'Video 1' },
      { id: 'V2', kind: 'visual', label: 'Video 2' },
    ],
    clips,
  } as TimelineConfig);
  const rowData = configToRows(config);
  const tracks = (config.tracks ?? []).map((track) => ({ ...track }));
  return {
    config,
    configVersion: 1,
    registry: { assets: {} },
    resolvedConfig: {
      output: { ...config.output },
      tracks,
      clips: config.clips.map((clip) => ({ ...clip })) as ResolvedTimelineClip[],
      registry: {},
    } as TimelineData['resolvedConfig'],
    rows: rowData.rows,
    meta: rowData.meta,
    effects: rowData.effects,
    assetMap: {},
    output: { ...config.output },
    tracks,
    clipOrder: rowData.clipOrder,
    signature: 'bulk-transition-signature',
    stableSignature: 'bulk-transition-stable-signature',
  } as TimelineData;
}

function makeAssignmentData(): TimelineData {
  return makeTimelineData([
    makeClip('previous-a', 0, 'V1'),
    makeClip('target-a', 2, 'V1', {
      type: 'legacy:transition-a', duration: 0.75, revision: 'legacy-transition-a-r2',
      params: { amount: 0.9, opaqueParam: 'authored-a' }, opaqueTransition: { owner: 'clip-a' },
    }, {
      id: 'legacy:transition-a', revision: 'legacy-transition-a-r2', kind: 'transition',
      packId: 'legacy-pack', opaqueReference: { owner: 'clip-a' },
    }),
    makeClip('previous-b', 10, 'V2'),
    makeClip('target-b', 12, 'V2', {
      type: 'legacy:transition-b', duration: 0.9, revision: 'legacy-transition-b-r4',
      params: null, opaqueTransition: { owner: 'clip-b' },
    }, {
      id: 'legacy:transition-b', revision: 'legacy-transition-b-r4', kind: 'transition',
      packId: 'legacy-pack', opaqueReference: { owner: 'clip-b' },
    }),
  ]);
}

function makeBoundData(revisionB = 'captured-transition-r2'): TimelineData {
  return makeTimelineData([
    makeClip('previous-a', 0, 'V1'),
    makeClip('target-a', 2, 'V1', {
      type: transitionId, duration: 0.5, revision: 'captured-transition-r1',
      params: null, opaqueTransition: { owner: 'clip-a' },
    }, {
      id: transitionId, revision: 'captured-transition-r1', kind: 'transition',
      packId: 'test-pack', opaqueReference: { owner: 'clip-a' },
    }),
    makeClip('previous-b', 10, 'V2'),
    makeClip('target-b', 12, 'V2', {
      type: transitionId, duration: 0.5, revision: revisionB,
      opaqueTransition: { owner: 'clip-b' },
    }, {
      id: transitionId, revision: revisionB, kind: 'transition',
      packId: 'test-pack', opaqueReference: { owner: 'clip-b' },
    }),
  ]);
}

function makePanelProps(overrides: Partial<ComponentProps<typeof BulkClipPanelBody>> = {}) {
  return {
    clips: [],
    visibleTabs: ['effects'] as const,
    compositionWidth: 1920,
    compositionHeight: 1080,
    sharedEntrance: null,
    sharedExit: null,
    sharedContinuous: null,
    sharedText: null,
    sharedTransition: null,
    sharedEntranceType: null,
    sharedExitType: null,
    sharedContinuousType: null,
    sharedTransitionType: null,
    sharedSpeed: null,
    sharedFrom: null,
    sharedTo: null,
    sharedX: null,
    sharedY: null,
    sharedWidth: null,
    sharedHeight: null,
    sharedOpacity: null,
    sharedVolume: null,
    sharedFontSize: null,
    sharedTextColor: null,
    sharedTransitionDuration: null,
    onChange: vi.fn(),
    onChangeDeep: vi.fn(),
    onResetPosition: vi.fn(),
    onToggleMute: vi.fn(),
    onClose: vi.fn(),
    activeTab: 'effects' as const,
    setActiveTab: vi.fn(),
    effectResources: { effects: [], entrance: [], exit: [], continuous: [] },
    ...overrides,
  } as ComponentProps<typeof BulkClipPanelBody>;
}

function TestBulkPanel({
  dataRef,
  applyEdit,
  selectedClipIds,
  sharedTransitionType,
  sharedTransitionDuration,
}: {
  dataRef: { current: TimelineData | null };
  applyEdit: TimelineApplyEdit;
  selectedClipIds: string[];
  sharedTransitionType: string | null;
  sharedTransitionDuration: number | null;
}) {
  const editing = useClipEditing({
    dataRef,
    resolvedConfig: dataRef.current?.resolvedConfig ?? null,
    selectedClipId: null,
    selectedTrack: null,
    currentTime: 0,
    selectClip: vi.fn(),
    setSelectedTrackId: vi.fn(),
    applyEdit,
  });
  const data = dataRef.current!;
  const selected = selectedClipIds.map((id) => data.config.clips.find((clip) => clip.id === id)!) as unknown as ResolvedTimelineClip[];
  const firstTransition = data.meta[selectedClipIds[0]!]?.transition ?? null;
  return (
    <BulkClipPanelBody
      {...makePanelProps({
        clips: selected,
        sharedTransition: firstTransition,
        sharedTransitionType,
        sharedTransitionDuration,
        onChangeDeep: (patchFn) => editing.handleUpdateClipsDeep(selectedClipIds, patchFn),
      })}
    />
  );
}

function renderPanel(args: {
  data: TimelineData;
  host?: AstridElementHost;
  selectedTransitionType?: string | null;
  selectedTransitionDuration?: number | null;
}) {
  runtimeContextMock.value = args.host ? { astridElementHost: args.host } : null;
  const applyEdit = vi.fn<TimelineApplyEdit>();
  const dataRef = { current: args.data };
  const selectedClipIds = ['target-b', 'target-a'];
  const rendered = render(
    <TransitionRegistryProvider>
      <InstallRecord record={makeRecord()}>
        <TestBulkPanel
          dataRef={dataRef}
          applyEdit={applyEdit}
          selectedClipIds={selectedClipIds}
          sharedTransitionType={args.selectedTransitionType ?? null}
          sharedTransitionDuration={args.selectedTransitionDuration ?? null}
        />
      </InstallRecord>
    </TransitionRegistryProvider>,
  );
  return { ...rendered, applyEdit };
}

function transitionSelectTrigger(): HTMLElement {
  return screen.getAllByRole('combobox')[3] as HTMLElement;
}

beforeEach(() => {
  runtimeContextMock.value = null;
});

describe('BulkClipPanelBody transition consumer', () => {
  it('pins assignment to the unique host descriptor through handleUpdateClipsDeep and preserves per-clip siblings', async () => {
    const hostDescriptor = makeDescriptor(transitionId, transitionRevision);
    const user = userEvent.setup();
    const { applyEdit } = renderPanel({
      data: makeAssignmentData(),
      host: makeElementHost([hostDescriptor]),
    });

    await user.click(transitionSelectTrigger());
    const option = await screen.findByRole('option', { name: new RegExp(transitionId.replace(':', '\\:')) });
    expect(option).not.toHaveAttribute('data-disabled');
    await user.click(option);

    await waitFor(() => expect(applyEdit).toHaveBeenCalledTimes(1));
    const [mutation, options] = applyEdit.mock.calls[0]!;
    expect(mutation.type).toBe('rows');
    const updates = mutation.metaUpdates as Record<string, Partial<ClipMeta>>;
    expect(updates['target-a']?.transition).toEqual({
      type: transitionId,
      duration: 0.75,
      revision: transitionRevision,
      params: { amount: 0.25, opaqueParam: 'authored-a' },
      opaqueTransition: { owner: 'clip-a' },
    });
    expect(updates['target-b']?.transition).toEqual({
      type: transitionId,
      duration: 0.9,
      revision: transitionRevision,
      params: { amount: 0.25 },
      opaqueTransition: { owner: 'clip-b' },
    });
    expect(updates['target-a']?.elementRef).toEqual({
      id: transitionId,
      revision: transitionRevision,
      kind: 'transition',
      packId: 'test-pack',
      opaqueReference: { owner: 'clip-a' },
    });
    expect(updates['target-b']?.elementRef).toEqual({
      id: transitionId,
      revision: transitionRevision,
      kind: 'transition',
      packId: 'test-pack',
      opaqueReference: { owner: 'clip-b' },
    });
    const commands = options?.editCommands ?? [];
    expect(commands.map((command) => command.select)).toEqual([
      'parent/clip:target-b',
      'parent/clip:target-a',
    ]);
    expect(commands).toHaveLength(2);
    expect(commands.map((command) => command.op)).toEqual(['clip.set-transition', 'clip.set-transition']);
    expect(commands[0]?.args).toEqual(expect.objectContaining({
      transition: updates['target-b']?.transition,
      elementRef: updates['target-b']?.elementRef,
    }));
  });

  it('changes duration while retaining each captured revision, reference, params and opaque siblings', async () => {
    const revA = 'captured-transition-r1';
    const revB = 'captured-transition-r2';
    const { applyEdit } = renderPanel({
      data: makeBoundData(revB),
      host: makeElementHost([makeDescriptor(transitionId, revA), makeDescriptor(transitionId, revB)]),
      selectedTransitionType: transitionId,
      selectedTransitionDuration: 0.5,
    });

    fireEvent.change(screen.getByRole('spinbutton'), { target: { value: '1.25' } });
    await waitFor(() => expect(applyEdit).toHaveBeenCalledTimes(1));
    const [mutation, options] = applyEdit.mock.calls[0]!;
    const updates = mutation.metaUpdates as Record<string, Partial<ClipMeta>>;
    expect(updates['target-a']?.transition).toEqual({
      type: transitionId, duration: 1.25, revision: revA, params: null,
      opaqueTransition: { owner: 'clip-a' },
    });
    expect(updates['target-b']?.transition).toEqual({
      type: transitionId, duration: 1.25, revision: revB,
      opaqueTransition: { owner: 'clip-b' },
    });
    expect(updates['target-b']?.transition).not.toHaveProperty('params');
    expect(updates['target-a']?.elementRef).toEqual({
      id: transitionId, revision: revA, kind: 'transition', packId: 'test-pack',
      opaqueReference: { owner: 'clip-a' },
    });
    expect(updates['target-b']?.elementRef).toEqual({
      id: transitionId, revision: revB, kind: 'transition', packId: 'test-pack',
      opaqueReference: { owner: 'clip-b' },
    });
    expect(options?.editCommands).toHaveLength(2);
    expect(options?.editCommands?.map((command) => command.op)).toEqual([
      'clip.set-transition', 'clip.set-transition',
    ]);
  });

  it('resets only declared params and keeps the captured binding and opaque transition/reference siblings', async () => {
    const revA = 'captured-transition-r1';
    const revB = 'captured-transition-r2';
    const data = makeBoundData(revB);
    data.config.clips.find((clip) => clip.id === 'target-a')!.transition = {
      ...data.config.clips.find((clip) => clip.id === 'target-a')!.transition!,
      params: { amount: 0.9, opaqueParam: 'keep-a' },
    };
    data.meta['target-a']!.transition = data.config.clips.find((clip) => clip.id === 'target-a')!.transition;
    data.config.clips.find((clip) => clip.id === 'target-b')!.transition = {
      ...data.config.clips.find((clip) => clip.id === 'target-b')!.transition!,
      params: { amount: 0.8, opaqueParam: 'authored-b' },
    };
    data.meta['target-b']!.transition = data.config.clips.find((clip) => clip.id === 'target-b')!.transition;
    const { applyEdit } = renderPanel({
      data,
      host: makeElementHost([makeDescriptor(transitionId, revA), makeDescriptor(transitionId, revB)]),
      selectedTransitionType: transitionId,
      selectedTransitionDuration: 0.5,
    });

    fireEvent.click(screen.getByText('Reset defaults'));
    await waitFor(() => expect(applyEdit).toHaveBeenCalledTimes(1));
    const [mutation, options] = applyEdit.mock.calls[0]!;
    const updates = mutation.metaUpdates as Record<string, Partial<ClipMeta>>;
    expect(updates['target-a']?.transition).toEqual({
      type: transitionId, duration: 0.5, revision: revA,
      params: { amount: 0.25, opaqueParam: 'keep-a' }, opaqueTransition: { owner: 'clip-a' },
    });
    expect(updates['target-b']?.transition).toEqual({
      type: transitionId, duration: 0.5, revision: revB,
      params: { amount: 0.25, opaqueParam: 'authored-b' }, opaqueTransition: { owner: 'clip-b' },
    });
    expect(updates['target-a']?.elementRef).toEqual(expect.objectContaining({ revision: revA, opaqueReference: { owner: 'clip-a' } }));
    expect(updates['target-b']?.elementRef).toEqual(expect.objectContaining({ revision: revB, opaqueReference: { owner: 'clip-b' } }));
    expect(options?.editCommands).toHaveLength(2);
    expect(options?.editCommands?.map((command) => command.op)).toEqual([
      'clip.set-transition', 'clip.set-transition',
    ]);
  });

  it.each([
    ['missing host descriptor', []],
    ['ambiguous host descriptors', [makeDescriptor(transitionId, transitionRevision), makeDescriptor(transitionId, 'host-transition-r8')]],
  ])('disables assignment when the descriptor is %s', async (_label, descriptors) => {
    const user = userEvent.setup();
    const host = makeElementHost(descriptors as AstridElementDescriptor[]);
    const { applyEdit } = renderPanel({ data: makeAssignmentData(), host });

    await user.click(transitionSelectTrigger());
    const option = await screen.findByRole('option', { name: new RegExp(transitionId.replace(':', '\\:')) });
    expect(option).toHaveAttribute('data-disabled');
    await user.click(option);
    expect(applyEdit).not.toHaveBeenCalled();
  });

  it('keeps the existing all-members atomic refusal when one captured binding is unavailable', async () => {
    const { applyEdit } = renderPanel({
      data: makeBoundData('captured-transition-not-installed'),
      host: makeElementHost([makeDescriptor(transitionId, 'captured-transition-r1')]),
      selectedTransitionType: transitionId,
      selectedTransitionDuration: 0.5,
    });

    fireEvent.change(screen.getByRole('spinbutton'), { target: { value: '1.25' } });
    await waitFor(() => expect(applyEdit).toHaveBeenCalledTimes(1));
    const [, options] = applyEdit.mock.calls[0]!;
    const commands = options?.editCommands ?? [];
    expect(commands).toHaveLength(0);
    expect(commands.some((command) => command.op === 'clip.set-transition')).toBe(false);
  });

  it('leaves Remove outside the typed bulk assignment/update slice', async () => {
    const { applyEdit } = renderPanel({
      data: makeBoundData('captured-transition-r2'),
      host: makeElementHost([
        makeDescriptor(transitionId, 'captured-transition-r1'),
        makeDescriptor(transitionId, 'captured-transition-r2'),
      ]),
      selectedTransitionType: transitionId,
      selectedTransitionDuration: 0.5,
    });

    fireEvent.click(screen.getByText('Remove'));
    await waitFor(() => expect(applyEdit).toHaveBeenCalledTimes(1));
    const [mutation, options] = applyEdit.mock.calls[0]!;
    expect(mutation.metaUpdates).toEqual({
      'target-b': { transition: undefined },
      'target-a': { transition: undefined },
    });
    expect(options?.editCommands).toHaveLength(2);
    expect(options?.editCommands?.map((command) => command.op)).toEqual(['clip.clear', 'clip.clear']);
    expect(options?.editCommands?.some((command) => command.op === 'clip.set-transition')).toBe(false);
  });
});
