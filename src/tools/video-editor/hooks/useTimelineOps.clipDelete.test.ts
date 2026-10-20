// @vitest-environment jsdom
import { act, renderHook } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { toast } from '@/shared/components/ui/runtime/sonner.tsx';
import type { TimelinePatch, TimelinePatchOperation } from '@/sdk/video/timeline/patch.ts';
import { TimelineVersionConflictError } from '@/sdk/video/timeline/errors.ts';
import { captureClipDelete, finishClipDelete } from '../commands/clipDeleteCapture.ts';
import type { ClipDeleteCapturePort } from '../commands/clipDeleteGesture.ts';
import type { AuthoredBundle } from '../commands/clipMovePrimitives.ts';
import type { TimelineProvisionedAsset } from '../commands/provisioning.ts';
import { buildTimelineCommandData } from '../commands/timelineData.ts';
import { useClipEditing } from './useClipEditing.ts';
import { createTimelineStore } from './timelineStore.ts';
import { createTimelineCommands } from './useTimelineCommandsService.ts';
import { useTimelineOps, type UseTimelineOpsArgs } from './useTimelineOps.ts';

vi.mock('@/shared/components/ui/runtime/sonner.tsx', () => ({ toast: { error: vi.fn() } }));

const remove: TimelinePatchOperation = { op: 'clip.remove', target: 'c' };
const patch = (...operations: TimelinePatchOperation[]): TimelinePatch => ({ version: 1, operations });

function setup() {
  const config = {
    output: { resolution: '1920x1080', fps: 30, file: 'test.mp4' },
    tracks: [{ id: 'picture', kind: 'visual' as const }],
    clips: [
      { id: 'c', track: 'picture', at: 2, hold: 3, clipType: 'hold' as const },
      { id: 'other', track: 'picture', at: 8, hold: 2, clipType: 'hold' as const },
    ],
  };
  const current = buildTimelineCommandData(config, { assets: {} });
  const bundle: AuthoredBundle = {
    parent: { config: { ...structuredClone(config), clips: [
      { ...config.clips[0], opaque: { keep: [null, false, 0] } }, config.clips[1],
    ] } },
    placements: [], shots: {},
    base_parent: { revision_id: 'parent-r1', content_digest: 'sha256:original-parent' },
  };
  const expected = captureClipDelete(bundle, 'parent/clip:c').command;
  // Real portable capture/finish; submit observes local handoff, never a durable ACK.
  const capture = vi.fn<ClipDeleteCapturePort['capture']>(({ clipId }) =>
    captureClipDelete(bundle, `parent/clip:${clipId}`));
  const finish = vi.fn<ClipDeleteCapturePort['finish']>(finishClipDelete);
  const submit = vi.fn<ClipDeleteCapturePort['submit']>();
  const port: ClipDeleteCapturePort = { capture, finish, submit };
  const args: UseTimelineOpsArgs = {
    dataRef: { current }, commitData: vi.fn(), clipDeletePort: port,
    createManualCheckpoint: vi.fn(), jumpToCheckpoint: vi.fn(), checkpoints: [],
  };
  const selectedClipIds = new Set(['c', 'other']);
  const applyEdit = vi.fn();
  const store = createTimelineStore();
  const initial = store.getState();
  initial.syncSlices({
    data: { ...initial.data, dataRef: args.dataRef, selectedClipIds,
      selectedClipIdsRef: { current: selectedClipIds } },
    ops: { ...initial.ops, applyEdit, clipDelete: port },
  });
  const hookArgs = {
    dataRef: args.dataRef, resolvedConfig: current.resolvedConfig, selectedClipId: 'c',
    selectedTrack: null, currentTime: 0, selectClip: vi.fn(), setSelectedTrackId: vi.fn(),
    applyEdit, clipDeletePort: port,
  };
  return { args, hookArgs, store, applyEdit, selectedClipIds, bundle, expected, capture, finish, submit };
}

function expectNoWrite(env: ReturnType<typeof setup>) {
  expect(env.applyEdit).not.toHaveBeenCalled();
  expect(env.args.commitData).not.toHaveBeenCalled();
  expect(env.selectedClipIds).toEqual(new Set(['c', 'other']));
  expect(env.store.getState().data.selectedClipIds).toBe(env.selectedClipIds);
  expect(env.hookArgs.selectClip).not.toHaveBeenCalled();
  expect(env.hookArgs.setSelectedTrackId).not.toHaveBeenCalled();
}

beforeEach(() => vi.clearAllMocks());

describe('ordinary single clip delete ingresses', () => {
  it.each(['ops', 'service', 'hook'] as const)('hands off the exact native command through %s without a rows/snapshot write', (ingress) => {
    const env = setup();
    const before = structuredClone(env.args.dataRef.current);
    if (ingress === 'ops') {
      const { result } = renderHook(() => useTimelineOps(env.args));
      const diff = result.current.apply(patch(remove));
      expect(diff.entries).toEqual([expect.objectContaining({ op: 'clip.remove', target: 'c' })]);
    } else if (ingress === 'service') {
      expect(createTimelineCommands(env.store).deleteClip({ clipId: 'c' })).toEqual({ ok: true, data: { clipId: 'c' } });
    } else {
      const { result } = renderHook(() => useClipEditing(env.hookArgs));
      act(() => result.current.handleDeleteClip('c'));
    }
    expect(env.capture).toHaveBeenCalledExactlyOnceWith({ clipId: 'c', current: env.args.dataRef.current });
    expect(env.finish).toHaveBeenCalledExactlyOnceWith(env.capture.mock.results[0].value);
    expect(env.submit).toHaveBeenCalledExactlyOnceWith({ command: env.expected, preview: patch(remove) });
    expect(env.args.dataRef.current).toEqual(before);
    expectNoWrite(env);
  });

  it('retains the original whole-row guard when authored state changes after capture', () => {
    const env = setup();
    env.capture.mockImplementation(({ clipId }) => {
      const basis = captureClipDelete(env.bundle, `parent/clip:${clipId}`);
      (env.bundle.parent.config.clips as Array<Record<string, unknown>>)[0].hold = 99;
      return basis;
    });
    const { result } = renderHook(() => useTimelineOps(env.args));
    result.current.apply(patch(remove));
    expect(env.submit.mock.calls[0][0].command).toEqual(env.expected);
    expect(env.submit.mock.calls[0][0].command.expect).toEqual({
      'parent/clip:c::': { state: 'present', value: expect.objectContaining({ hold: 3, opaque: { keep: [null, false, 0] } }) },
    });
    expectNoWrite(env);
  });

  it.each(['capture', 'finish', 'submit'] as const)('keeps data and selection on %s refusal in every ingress', (phase) => {
    for (const ingress of ['ops', 'service', 'hook']) {
      const env = setup();
      const before = structuredClone(env.args.dataRef.current);
      const refusal = new Error(`${phase} refused`);
      env[phase].mockImplementation(() => { throw refusal; });
      if (ingress === 'ops') {
        const { result } = renderHook(() => useTimelineOps(env.args));
        expect(() => result.current.apply(patch(remove))).toThrow(refusal);
      } else if (ingress === 'service') {
        expect(createTimelineCommands(env.store).deleteClip({ clipId: 'c' })).toMatchObject({
          ok: false, error: { code: 'mutation_failed', message: refusal.message },
        });
      } else {
        const { result } = renderHook(() => useClipEditing(env.hookArgs));
        act(() => result.current.handleDeleteClip('c'));
        expect(toast.error).toHaveBeenCalledWith(refusal.message);
      }
      expect(env.args.dataRef.current).toEqual(before);
      if (phase !== 'submit') expect(env.submit).not.toHaveBeenCalled();
      expectNoWrite(env);
    }
  });

  it('refuses read-only edits before capture through all three ingresses', () => {
    const env = setup();
    const denied = () => ({ allowed: false, reason: 'timeline_read_only' as const });
    const editability = { check: denied, checkTimeline: denied };
    const { result: ops } = renderHook(() => useTimelineOps({ ...env.args, editability }));
    expect(() => ops.current.apply(patch(remove))).toThrow('timeline_read_only');
    expect(createTimelineCommands(env.store, { timelineEditability: editability }).deleteClip({ clipId: 'c' }))
      .toMatchObject({ ok: false, error: { code: 'timeline_read_only' } });
    const { result: hook } = renderHook(() => useClipEditing({ ...env.hookArgs, editability }));
    act(() => hook.current.handleDeleteClip('c'));
    expect(toast.error).toHaveBeenCalledWith(expect.stringContaining('timeline_read_only'));
    expect(env.capture).not.toHaveBeenCalled();
    expectNoWrite(env);
  });

  it('preserves the service managed-object guard before capture', () => {
    const env = setup();
    const managedObjectGuard = {
      checkClipManaged: vi.fn(() => ({ objectId: 'c', kind: 'clip' as const, managedBy: 'test.extension' })),
      checkTrackManaged: vi.fn(() => null),
    };
    expect(createTimelineCommands(env.store, { managedObjectGuard }).deleteClip({ clipId: 'c' }))
      .toMatchObject({ ok: false, error: { code: 'managed_object_blocked' } });
    expect(env.capture).not.toHaveBeenCalled();
    expectNoWrite(env);
  });

  it.each(['ops', 'service', 'hook'] as const)('retains the existing writer without a qualified native port through %s', (ingress) => {
    const env = setup();
    if (ingress === 'ops') {
      const { result } = renderHook(() => useTimelineOps({ ...env.args, clipDeletePort: undefined }));
      result.current.apply(patch(remove));
      expect(env.args.commitData).toHaveBeenCalledOnce();
    } else if (ingress === 'service') {
      env.store.getState().syncSlices({ ops: { ...env.store.getState().ops, clipDelete: undefined } });
      expect(createTimelineCommands(env.store).deleteClip({ clipId: 'c' }).ok).toBe(true);
      expect(env.applyEdit).toHaveBeenCalledOnce();
    } else {
      const { result } = renderHook(() => useClipEditing({ ...env.hookArgs, clipDeletePort: undefined }));
      act(() => result.current.handleDeleteClip('c'));
      expect(env.applyEdit).toHaveBeenCalledOnce();
    }
    expect(env.capture).not.toHaveBeenCalled();
    expect(env.submit).not.toHaveBeenCalled();
    expect(toast.error).not.toHaveBeenCalled();
  });

  it('retains the existing multi-delete UI writer when the native port is available', () => {
    const env = setup();
    const { result } = renderHook(() => useClipEditing(env.hookArgs));
    act(() => result.current.handleDeleteClips(['c', 'other']));
    expect(env.applyEdit).toHaveBeenCalledWith({ type: 'rows', rows: [{ id: 'picture', actions: [] }],
      metaDeletes: ['c', 'other'] }, { semantic: true });
    expect(env.capture).not.toHaveBeenCalled();
  });

  it('retains the shot-menu group writer with a native port present', () => {
    const env = setup();
    env.args.dataRef.current!.config.pinnedShotGroups = [{ shotId: 'shot', trackId: 'picture', clipIds: ['c', 'other'] }];
    const { result } = renderHook(() => useClipEditing(env.hookArgs));
    act(() => result.current.handleDeleteClips(['c', 'other'], { allowPinnedGroupDelete: true }));
    expect(env.applyEdit).toHaveBeenCalledWith({ type: 'rows', rows: [{ id: 'picture', actions: [] }],
      metaDeletes: ['c', 'other'] }, { semantic: true });
    expect(env.capture).not.toHaveBeenCalled();
    expect(toast.error).not.toHaveBeenCalled();
    env.applyEdit.mockClear();
    expect(createTimelineCommands(env.store).deleteClip({ clipId: 'c', allowPinnedGroupDelete: true }).ok).toBe(true);
    expect(env.applyEdit).toHaveBeenCalledOnce();
    expect(env.capture).not.toHaveBeenCalled();
  });

  it('retains prepared-media removeIds as a separate unconverted writer', () => {
    const env = setup();
    const asset: TimelineProvisionedAsset = {
      assetKey: 'replacement', mediaType: 'image', durationSeconds: 5,
      entry: { file: 'replacement.png', type: 'image/png' }, source: 'registered',
    };
    const result = createTimelineCommands(env.store).addClip({
      preparedAsset: asset, time: 0, trackId: 'picture', removeClipIds: ['c', 'other'],
    });
    expect(result.ok).toBe(true);
    expect(env.applyEdit).toHaveBeenCalledExactlyOnceWith({
      type: 'prepared-media', command: { type: 'place-prepared-media', payload: expect.objectContaining({
        asset, removeClipIds: ['c', 'other'],
      }) },
    }, expect.objectContaining({ semantic: true }));
    expect(env.capture).not.toHaveBeenCalled();
    expect(env.submit).not.toHaveBeenCalled();
    expect(toast.error).not.toHaveBeenCalled();
  });

  it('surfaces native semantic dependency refusal and keeps the work', () => {
    const env = setup();
    (env.bundle.parent.config.clips as Array<Record<string, unknown>>)[1].transition = { id: 'crossfade' };
    const { result } = renderHook(() => useClipEditing(env.hookArgs));
    const before = structuredClone(env.args.dataRef.current);
    act(() => result.current.handleDeleteClip('c'));
    expect(toast.error).toHaveBeenCalledWith(expect.stringContaining('dependencies'));
    expect(env.submit).not.toHaveBeenCalled();
    expect(env.args.dataRef.current).toEqual(before);
    expectNoWrite(env);
  });
});

describe('TimelineOps single clip.remove adapter', () => {
  it.each([
    [remove, { op: 'clip.remove', target: 'other' }],
    [remove, { op: 'track.update', target: 'picture', payload: { muted: true } }],
    [{ op: 'track.update', target: 'picture', payload: { label: 'Rename' } }, remove],
    [remove, { op: 'clip.move', target: 'other', payload: { at: 12 } }],
  ] satisfies TimelinePatchOperation[][])('refuses mixed/batched operations atomically: %j', (...operations) => {
    const env = setup();
    const before = structuredClone(env.args.dataRef.current);
    const { result } = renderHook(() => useTimelineOps(env.args));
    expect(() => result.current.apply(patch(...operations))).toThrow('only a single');
    expect(env.capture).not.toHaveBeenCalled();
    expect(env.submit).not.toHaveBeenCalled();
    expect(env.args.dataRef.current).toEqual(before);
    expectNoWrite(env);
  });

  it('validates the full request and checks the live version before capture', () => {
    const env = setup();
    const { result } = renderHook(() => useTimelineOps(env.args));
    expect(() => result.current.apply(patch(remove, { op: 'track.add', target: 'invalid', payload: {} })))
      .toThrow('patch validation failed');
    const { result: stale } = renderHook(() => useTimelineOps({ ...env.args, getConfigVersion: () => 2 }));
    expect(() => stale.current.apply(patch(remove))).toThrow(TimelineVersionConflictError);
    expect(env.capture).not.toHaveBeenCalled();
    expectNoWrite(env);
  });

  it('keeps preview read-only and refuses missing or ambiguous display identities', () => {
    const env = setup();
    const { result } = renderHook(() => useTimelineOps(env.args));
    expect(result.current.preview(patch(remove)).fullyPreviewable).toBe(true);
    expect(() => result.current.apply(patch({ ...remove, target: 'missing' }))).toThrow('unambiguous');
    env.args.dataRef.current!.resolvedConfig.clips.push({ ...env.args.dataRef.current!.resolvedConfig.clips[0] });
    expect(() => result.current.apply(patch(remove))).toThrow('unambiguous');
    expect(env.capture).not.toHaveBeenCalled();
    expectNoWrite(env);
  });

  it('continues to use the acknowledgement barrier after synchronous delete acceptance', async () => {
    const env = setup();
    let refuse!: (error: Error) => void;
    const pending = new Promise<number>((_resolve, reject) => { refuse = reject; });
    const flushPendingSave = vi.fn(() => pending);
    const { result } = renderHook(() => useTimelineOps({ ...env.args, flushPendingSave }));
    result.current.apply(patch(remove));
    const settled = vi.fn();
    const flushed = result.current.flush();
    void flushed.then(settled, settled);
    await Promise.resolve();
    expect(flushPendingSave).toHaveBeenCalledTimes(1);
    expect(settled).not.toHaveBeenCalled();
    const failure = new Error('commit acknowledgement unavailable');
    refuse(failure);
    await expect(flushed).rejects.toBe(failure);
    expectNoWrite(env);
  });
});
