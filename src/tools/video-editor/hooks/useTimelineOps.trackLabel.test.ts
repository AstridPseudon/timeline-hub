// @vitest-environment jsdom
import { renderHook } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import type { TimelinePatch, TimelinePatchOperation } from '@/sdk/video/timeline/patch.ts';
import { TimelineVersionConflictError } from '@/sdk/video/timeline/errors.ts';
import { captureTrackLabel, finishTrackLabel } from '../commands/trackLabelCapture.ts';
import type { TrackLabelCapturePort } from '../commands/trackLabelGesture.ts';
import type { AuthoredBundle } from '../commands/clipMovePrimitives.ts';
import { buildTimelineData } from '../lib/timeline-data.ts';
import { useTimelineOps, type UseTimelineOpsArgs } from './useTimelineOps';

const update = (payload: Record<string, unknown>): TimelinePatchOperation => ({
  op: 'track.update', target: 'V1', payload,
});
const patch = (...operations: TimelinePatchOperation[]): TimelinePatch => ({ version: 1, operations });

async function setup() {
  const data = await buildTimelineData({
    output: { resolution: '1920x1080', fps: 30, file: 'out.mp4' },
    tracks: [{ id: 'V1', kind: 'visual', label: 'Picture' }],
    clips: [],
  }, { assets: {} });
  const bundle: AuthoredBundle = {
    parent: { config: { tracks: [{ id: 'V1', kind: 'visual', label: 'Picture', opaque: [null, false] }] } },
    placements: [], shots: {},
    base_parent: { revision_id: 'parent-r1', content_digest: 'sha256:original-parent' },
  };
  // Native capture/finish; submit is only a local handoff spy, never a transport ACK.
  const capture = vi.fn(({ trackId }: Parameters<TrackLabelCapturePort['capture']>[0]) =>
    captureTrackLabel(bundle, `parent/track:${trackId}`));
  const finish = vi.fn<TrackLabelCapturePort['finish']>(finishTrackLabel);
  const submit = vi.fn<TrackLabelCapturePort['submit']>();
  const trackLabelPort: TrackLabelCapturePort = { capture, finish, submit };
  const args: UseTimelineOpsArgs = {
    dataRef: { current: data }, commitData: vi.fn(), trackLabelPort,
    createManualCheckpoint: vi.fn(), jumpToCheckpoint: vi.fn(), checkpoints: [],
  };
  return { args, bundle, capture, finish, submit };
}

describe('TimelineOps track label command ingress', () => {
  it.each([
    { label: 'Picture é 🎬', mode: undefined },
    { label: '', mode: 'merge' },
    { label: 'Picture', mode: 'merge' },
  ])('submits original guarded intent for $label with mode $mode without saving a snapshot', async ({ label, mode }) => {
    const env = await setup();
    const before = structuredClone(env.args.dataRef.current);
    const { result } = renderHook(() => useTimelineOps(env.args));
    const diff = result.current.apply(patch(update({ label, ...(mode ? { mode } : {}) })));

    expect(diff).not.toBeInstanceOf(Promise);
    expect(diff.entries).toEqual([expect.objectContaining({ target: 'V1', after: expect.objectContaining({ label }) })]);
    expect(env.capture).toHaveBeenCalledExactlyOnceWith({ trackId: 'V1', current: env.args.dataRef.current });
    expect(env.finish).toHaveBeenCalledExactlyOnceWith(env.capture.mock.results[0].value, { values: { label }, clear: [] });
    expect(env.submit).toHaveBeenCalledExactlyOnceWith({
      command: expect.objectContaining({
        op: 'track.set', select: 'parent/track:V1', args: { values: { label }, clear: [] },
        expect: { 'parent/track:V1::label': { state: 'present', value: 'Picture' } },
      }),
      preview: { version: 1, operations: [update({ label })] },
    });
    expect(env.args.commitData).not.toHaveBeenCalled();
    expect(env.args.dataRef.current).toEqual(before);
  });

  it('preserves an absent raw label rather than the compiled display fallback', async () => {
    const env = await setup();
    delete (env.bundle.parent.config as { tracks: Array<Record<string, unknown>> }).tracks[0].label;
    const { result } = renderHook(() => useTimelineOps(env.args));
    result.current.apply(patch(update({ label: '' })));
    expect(env.submit.mock.calls[0][0].command.expect).toEqual({ 'parent/track:V1::label': { state: 'absent' } });
    expect(env.submit.mock.calls[0][0].command.args).toEqual({ values: { label: '' }, clear: [] });
    expect(env.args.commitData).not.toHaveBeenCalled();
  });

  it('finishes with the original guards if raw input changes after capture', async () => {
    const env = await setup();
    env.capture.mockImplementation(({ trackId }) => {
      const basis = captureTrackLabel(env.bundle, `parent/track:${trackId}`);
      (env.bundle.parent.config as { tracks: Array<Record<string, unknown>> }).tracks[0].label = 'External edit';
      return basis;
    });
    const { result } = renderHook(() => useTimelineOps(env.args));
    result.current.apply(patch(update({ label: 'My edit' })));
    expect(env.capture).toHaveBeenCalledTimes(1);
    expect(env.submit.mock.calls[0][0].command.expect).toEqual({ 'parent/track:V1::label': { state: 'present', value: 'Picture' } });
    expect(env.args.commitData).not.toHaveBeenCalled();
  });

  it.each([
    [update({ label: 'Rename', muted: true })],
    [update({ label: 'Rename', app: { opaque: true } })],
    [update({ label: 'Rename', mode: 'replace' })],
    [update({ label: 'Rename' }), update({ label: 'Another' })],
    [update({ muted: true }), update({ label: 'Rename' })],
    [update({ label: 'Rename' }), { op: 'clip.add', target: 'new', payload: { track: 'V1', at: 0, clipType: 'hold', hold: 2 } }],
  ] satisfies TimelinePatchOperation[][])('refuses an unsupported label batch atomically: %j', async (...operations) => {
    const env = await setup();
    const before = structuredClone(env.args.dataRef.current);
    const { result } = renderHook(() => useTimelineOps(env.args));
    expect(() => result.current.apply(patch(...operations))).toThrow('single merge-mode label-only track.update');
    expect(env.capture).not.toHaveBeenCalled();
    expect(env.finish).not.toHaveBeenCalled();
    expect(env.submit).not.toHaveBeenCalled();
    expect(env.args.commitData).not.toHaveBeenCalled();
    expect(env.args.dataRef.current).toEqual(before);
  });

  it.each([null, undefined, 7])('does not invent clear semantics for label %j', async (label) => {
    const env = await setup();
    const { result } = renderHook(() => useTimelineOps(env.args));
    expect(() => result.current.apply(patch(update({ label })))).toThrow();
    expect(env.capture).not.toHaveBeenCalled();
    expect(env.submit).not.toHaveBeenCalled();
    expect(env.args.commitData).not.toHaveBeenCalled();
  });

  it('validates the entire batch before capture or submit', async () => {
    const env = await setup();
    const { result } = renderHook(() => useTimelineOps(env.args));
    expect(() => result.current.apply(patch(update({ label: 'Rename' }), { op: 'track.add', target: 'invalid', payload: {} })))
      .toThrow('patch validation failed');
    expect(env.capture).not.toHaveBeenCalled();
    expect(env.submit).not.toHaveBeenCalled();
    expect(env.args.commitData).not.toHaveBeenCalled();
  });

  it('rejects a stale live version before capturing original state', async () => {
    const env = await setup();
    const { result } = renderHook(() => useTimelineOps({ ...env.args, getConfigVersion: () => 2 }));
    expect(() => result.current.apply(patch(update({ label: 'Rename' })))).toThrow(TimelineVersionConflictError);
    expect(env.capture).not.toHaveBeenCalled();
    expect(env.submit).not.toHaveBeenCalled();
    expect(env.args.commitData).not.toHaveBeenCalled();
  });

  it('rejects read-only editing before capture', async () => {
    const env = await setup();
    const denied = () => ({ allowed: false as const, reason: 'timeline_read_only' as const });
    const { result } = renderHook(() => useTimelineOps({ ...env.args, editability: { check: denied, checkTimeline: denied } }));
    expect(() => result.current.apply(patch(update({ label: 'Rename' })))).toThrow('timeline_read_only');
    expect(env.capture).not.toHaveBeenCalled();
    expect(env.submit).not.toHaveBeenCalled();
    expect(env.args.commitData).not.toHaveBeenCalled();
  });

  it('refuses missing capture support without snapshot fallback', async () => {
    const env = await setup();
    const { result } = renderHook(() => useTimelineOps({ ...env.args, trackLabelPort: undefined }));
    expect(() => result.current.apply(patch(update({ label: 'Rename' })))).toThrow('capture is unavailable');
    expect(env.args.commitData).not.toHaveBeenCalled();
  });

  it.each(['capture', 'finish', 'submit'] as const)('propagates %s refusal without snapshot fallback', async (phase) => {
    const env = await setup();
    const failure = new Error(`${phase} unavailable`);
    env[phase].mockImplementation(() => { throw failure; });
    const { result } = renderHook(() => useTimelineOps(env.args));
    expect(() => result.current.apply(patch(update({ label: 'Rename' })))).toThrow(failure);
    expect(env.args.commitData).not.toHaveBeenCalled();
    if (phase !== 'submit') expect(env.submit).not.toHaveBeenCalled();
  });

  it('refuses a missing or ambiguous display target before command capture', async () => {
    const env = await setup();
    const { result } = renderHook(() => useTimelineOps(env.args));
    expect(() => result.current.apply(patch({ ...update({ label: 'Rename' }), target: 'missing' }))).toThrow('unambiguous');
    env.args.dataRef.current!.resolvedConfig.tracks.push({ ...env.args.dataRef.current!.resolvedConfig.tracks[0] });
    expect(() => result.current.apply(patch(update({ label: 'Rename' })))).toThrow('unambiguous');
    expect(env.capture).not.toHaveBeenCalled();
    expect(env.submit).not.toHaveBeenCalled();
    expect(env.args.commitData).not.toHaveBeenCalled();
  });

  it('keeps preview local and preserves unrelated nonlabel behavior', async () => {
    const env = await setup();
    const { result } = renderHook(() => useTimelineOps(env.args));
    expect(result.current.preview(patch(update({ label: 'Preview', mode: 'replace' }))).fullyPreviewable).toBe(true);
    expect(env.capture).not.toHaveBeenCalled();
    expect(env.submit).not.toHaveBeenCalled();
    expect(env.args.commitData).not.toHaveBeenCalled();
    result.current.apply(patch(update({ muted: true })));
    expect(env.args.commitData).toHaveBeenCalledExactlyOnceWith(expect.anything(), { save: true, semantic: true });
    expect(env.capture).not.toHaveBeenCalled();
    expect(env.submit).not.toHaveBeenCalled();
  });

  it('does not treat local command submission as a durable flush acknowledgement', async () => {
    const env = await setup();
    let refuse!: (reason: Error) => void;
    const pending = new Promise<number>((_resolve, reject) => { refuse = reject; });
    const barrier = vi.fn(() => pending);
    const { result } = renderHook(() => useTimelineOps({ ...env.args, flushPendingSave: barrier }));
    result.current.apply(patch(update({ label: 'Rename' })));
    const settled = vi.fn();
    const flushed = result.current.flush();
    void flushed.then(settled, settled);
    await Promise.resolve();
    expect(env.submit).toHaveBeenCalledTimes(1);
    expect(barrier).toHaveBeenCalledTimes(1);
    expect(settled).not.toHaveBeenCalled();
    const failure = new Error('command acknowledgement unavailable');
    refuse(failure);
    await expect(flushed).rejects.toBe(failure);
    expect(env.args.commitData).not.toHaveBeenCalled();
  });
});
