// @vitest-environment jsdom
import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { AIInputModeProvider } from '@/shared/contexts/AIInputModeContext.tsx';
import { captureTrackLabel, finishTrackLabel } from '@/tools/video-editor/commands/trackLabelCapture.ts';
import type { AuthoredBundle } from '@/tools/video-editor/commands/clipMovePrimitives.ts';
import type { TrackLabelCapturePort } from '@/tools/video-editor/commands/trackLabelGesture.ts';
import type { JsonObject } from '@/tools/video-editor/commands/types.ts';
import { useTimelineTrackManagement } from '@/tools/video-editor/hooks/useTimelineTrackManagement.ts';
import { buildTimelineData } from '@/tools/video-editor/lib/timeline-data.ts';
import type { TimelineDeviceClass } from '@/tools/video-editor/lib/mobile-interaction-model.ts';
import { createTimelineEditability, type TimelineEditability } from '@/tools/video-editor/lib/timeline-editability.ts';
import { TrackLabelContent } from './TrackLabel.tsx';

async function setup(deviceClass: TimelineDeviceClass) {
  const config = {
    output: { resolution: '1920x1080', fps: 30, file: 'out.mp4' },
    tracks: [{ id: 'V1', kind: 'visual' as const, label: 'Original' }], clips: [],
  };
  const dataRef = { current: await buildTimelineData(config, { assets: {} }) };
  const bundle: AuthoredBundle = {
    parent: { config: { tracks: [{ ...config.tracks[0], opaque: [null, false] }] } },
    placements: [], shots: {},
    base_parent: { revision_id: 'parent-r1', content_digest: 'sha256:original-parent' },
  };
  const capture = vi.fn<TrackLabelCapturePort['capture']>(() =>
    captureTrackLabel(bundle, 'parent/track:V1') as unknown as JsonObject);
  const finish = vi.fn<TrackLabelCapturePort['finish']>(finishTrackLabel);
  // This is the session handoff, not a Runtime ACK or browser qualification.
  const submit = vi.fn<TrackLabelCapturePort['submit']>();
  const applyEdit = vi.fn();
  const port: TrackLabelCapturePort = { capture, finish, submit };
  function Track({ labelPort = port, editability }: { labelPort?: TrackLabelCapturePort; editability?: TimelineEditability }) {
    const ops = useTimelineTrackManagement({
      dataRef, resolvedConfig: dataRef.current.resolvedConfig, selectedClipId: null,
      setSelectedTrackId: vi.fn(), applyEdit, trackLabelPort: labelPort, editability,
    });
    return <AIInputModeProvider><TrackLabelContent
      track={dataRef.current.resolvedConfig.tracks[0]} deviceClass={deviceClass}
      isSelected={false} hasClips={false} onSelect={vi.fn()} onRemove={vi.fn()}
      onChange={ops.handleTrackPopoverChange} onLabelEditStart={ops.handleTrackLabelEditStart}
    /></AIInputModeProvider>;
  }
  const view = render(<Track />);
  function input() {
    return screen.getByRole('textbox', { name: 'Track name' });
  }
  function remote() {
    (bundle.parent.config as { tracks: { label: string }[] }).tracks[0].label = 'Remote';
    dataRef.current.resolvedConfig.tracks[0] = { ...config.tracks[0], label: 'Remote' };
    view.rerender(<Track />);
  }
  return { ...view, Track, input, remote, bundle, dataRef, capture, finish, submit, applyEdit };
}

// Touch rows select a track for TrackInspector; desktop owns this command-backed editor.
describe.each(['desktop'] as const)('%s production track rename', (deviceClass) => {
  it.each(['音楽 🎬', '', 'Original'])('submits %j with the original native guard after a remote change', async (label) => {
    const env = await setup(deviceClass);
    const input = env.input();
    fireEvent.focus(input);
    expect(env.capture).toHaveBeenCalledTimes(1);
    expect(env.submit).not.toHaveBeenCalled();
    fireEvent.change(input, { target: { value: 'Temporary' } });
    fireEvent.change(input, { target: { value: label } });
    env.remote();
    expect(input).toHaveValue(label);
    fireEvent.keyDown(input, { key: 'Enter' });
    fireEvent.blur(input);
    expect(env.capture).toHaveBeenCalledTimes(1);
    expect(env.submit).toHaveBeenCalledExactlyOnceWith({
      command: expect.objectContaining({
        op: 'track.set', select: 'parent/track:V1', args: { values: { label }, clear: [] },
        expect: { 'parent/track:V1::label': { state: 'present', value: 'Original' } },
      }),
      preview: { version: 1, operations: [{ op: 'track.update', target: 'V1', payload: { label } }] },
    });
    expect(env.applyEdit).not.toHaveBeenCalled();
    expect(env.dataRef.current.resolvedConfig.tracks[0].label).toBe('Remote');
    expect((env.bundle.parent.config as { tracks: { opaque: unknown }[] }).tracks[0].opaque).toEqual([null, false]);
  });

  it('releases a clean focus and captures the next edit from the new raw state', async () => {
    const env = await setup(deviceClass);
    const input = env.input();
    fireEvent.focus(input);
    env.remote();
    fireEvent.blur(input);
    expect(input).toHaveValue('Remote');
    expect(env.submit).not.toHaveBeenCalled();
    fireEvent.focus(input);
    fireEvent.change(input, { target: { value: 'Next' } });
    fireEvent.blur(input);
    expect(env.capture).toHaveBeenCalledTimes(2);
    expect(env.submit.mock.calls[0][0].command.expect).toEqual({
      'parent/track:V1::label': { state: 'present', value: 'Remote' },
    });
  });

  it('retains the draft and original command on submit refusal', async () => {
    const env = await setup(deviceClass);
    env.submit.mockImplementation(() => { throw new Error('Original label guard no longer holds.'); });
    const input = env.input();
    fireEvent.focus(input);
    fireEvent.change(input, { target: { value: 'Keep locally' } });
    env.remote();
    fireEvent.blur(input);
    expect(input).toHaveValue('Keep locally');
    expect(screen.getByRole('alert')).toHaveTextContent('Original label guard no longer holds.');
    fireEvent.focus(input);
    fireEvent.keyDown(input, { key: 'Enter' });
    expect(env.capture).toHaveBeenCalledTimes(1);
    expect(env.submit).toHaveBeenCalledTimes(2);
    expect(env.submit.mock.calls[1][0]).toEqual(env.submit.mock.calls[0][0]);
    expect(env.applyEdit).not.toHaveBeenCalled();
  });

  it('retains typed input after capture refusal without refreshing capture', async () => {
    const env = await setup(deviceClass);
    env.capture.mockImplementation(() => { throw new Error('Ambiguous track identity.'); });
    const input = env.input();
    fireEvent.focus(input);
    fireEvent.change(input, { target: { value: 'Keep locally' } });
    env.remote();
    fireEvent.blur(input);
    fireEvent.focus(input);
    fireEvent.keyDown(input, { key: 'Enter' });
    expect(input).toHaveValue('Keep locally');
    expect(screen.getByRole('alert')).toHaveTextContent('Ambiguous track identity.');
    expect(env.capture).toHaveBeenCalledTimes(1);
    expect(env.finish).not.toHaveBeenCalled();
    expect(env.submit).not.toHaveBeenCalled();
    expect(env.applyEdit).not.toHaveBeenCalled();
  });

  it('finishes a dirty focused input once when the row unmounts without blur', async () => {
    const env = await setup(deviceClass);
    const input = env.input();
    fireEvent.focus(input);
    fireEvent.change(input, { target: { value: 'Before unmount' } });
    env.unmount();
    expect(env.capture).toHaveBeenCalledTimes(1);
    expect(env.submit).toHaveBeenCalledTimes(1);
    expect(env.submit.mock.calls[0][0].command.args).toEqual({ values: { label: 'Before unmount' }, clear: [] });
    expect(env.applyEdit).not.toHaveBeenCalled();
  });
});

// Independent review reproduction: a rejected draft must survive row teardown.
it.each(['desktop'] as const)('retains the refused %s draft when the same row is remounted', async (deviceClass) => {
  const env = await setup(deviceClass);
  env.submit.mockImplementation(() => { throw new Error('Original label guard no longer holds.'); });
  const input = env.input();
  fireEvent.focus(input);
  fireEvent.change(input, { target: { value: 'Keep after refused teardown' } });
  env.unmount();
  expect(env.submit).toHaveBeenCalledTimes(1);
  expect(env.applyEdit).not.toHaveBeenCalled();
  render(<env.Track />);
  const reopened = env.input();
  expect(reopened).toHaveValue('Keep after refused teardown');
  expect(screen.getByRole('alert')).toHaveTextContent('Original label guard no longer holds.');
});

// Remount is presentation recovery, never a new capture or a submission trigger.
describe.each(['desktop'] as const)('%s refused teardown retry', (deviceClass) => {
  it.each(['finish', 'submit'] as const)('retains the original capture after %s refusal and remote change', async (phase) => {
    const env = await setup(deviceClass);
    env[phase].mockImplementation(() => { throw new Error('Original label guard no longer holds.'); });
    const input = env.input();
    fireEvent.focus(input);
    fireEvent.change(input, { target: { value: 'Keep my original intent' } });
    env.remote();
    env.unmount();
    expect(env.finish).toHaveBeenCalledTimes(1);
    expect(env.submit).toHaveBeenCalledTimes(phase === 'submit' ? 1 : 0);
    const originalBasis = env.finish.mock.calls[0][0];
    const reopenedView = render(<env.Track />);
    const reopened = env.input();
    expect(reopened).toHaveValue('Keep my original intent');
    expect(screen.getByRole('alert')).toHaveTextContent('Original label guard no longer holds.');
    expect(env.capture).toHaveBeenCalledTimes(1);
    expect(env.finish).toHaveBeenCalledTimes(1);
    expect(env.submit).toHaveBeenCalledTimes(phase === 'submit' ? 1 : 0);
    fireEvent.focus(reopened);
    fireEvent.blur(reopened);
    expect(env.finish.mock.calls[1][0]).toBe(originalBasis);
    expect(env.finish.mock.calls[1][1]).toEqual({ values: { label: 'Keep my original intent' }, clear: [] });
    if (phase === 'submit') {
      expect(env.submit).toHaveBeenCalledTimes(2);
      expect(env.submit.mock.calls[1][0]).toEqual(env.submit.mock.calls[0][0]);
      expect(env.submit.mock.calls[1][0].command.expect).toEqual({
        'parent/track:V1::label': { state: 'present', value: 'Original' },
      });
    } else {
      expect(env.submit).not.toHaveBeenCalled();
    }
    expect(env.capture).toHaveBeenCalledTimes(1);
    reopenedView.unmount();
    expect(env.finish).toHaveBeenCalledTimes(2);
    expect(env.applyEdit).not.toHaveBeenCalled();
  });
});

it.each(['desktop'] as const)('retains %s capture refusal and typed input through row teardown', async (deviceClass) => {
  const env = await setup(deviceClass);
  env.capture.mockImplementation(() => { throw new Error('Ambiguous track identity.'); });
  const input = env.input();
  fireEvent.focus(input);
  fireEvent.change(input, { target: { value: 'Keep without capture' } });
  env.unmount();
  render(<env.Track />);
  const reopened = env.input();
  expect(reopened).toHaveValue('Keep without capture');
  expect(screen.getByRole('alert')).toHaveTextContent('Ambiguous track identity.');
  fireEvent.focus(reopened);
  fireEvent.keyDown(reopened, { key: 'Enter' });
  expect(env.capture).toHaveBeenCalledTimes(1);
  expect(env.finish).not.toHaveBeenCalled();
  expect(env.submit).not.toHaveBeenCalled();
  expect(env.applyEdit).not.toHaveBeenCalled();
});

it('keeps a refused draft with its command owner when the same row shows another session', async () => {
  const env = await setup('desktop');
  env.submit.mockImplementation(() => { throw new Error('Original owner refuses.'); });
  const input = env.input();
  fireEvent.focus(input);
  fireEvent.change(input, { target: { value: 'Original owner draft' } });
  fireEvent.blur(input);
  const otherPort = { capture: vi.fn(env.capture), finish: vi.fn(finishTrackLabel), submit: vi.fn() };
  env.rerender(<env.Track labelPort={otherPort} />);
  expect(env.input()).toHaveValue('Original');
  expect(screen.queryByRole('alert')).not.toBeInTheDocument();
  fireEvent.focus(env.input());
  fireEvent.change(env.input(), { target: { value: 'Other owner draft' } });
  fireEvent.blur(env.input());
  expect(otherPort.submit).toHaveBeenCalledTimes(1);
  expect(otherPort.submit.mock.calls[0][0].command.args).toEqual({ values: { label: 'Other owner draft' }, clear: [] });
  expect(env.submit).toHaveBeenCalledTimes(1);
  env.rerender(<env.Track />);
  expect(env.input()).toHaveValue('Original owner draft');
  expect(screen.getByRole('alert')).toHaveTextContent('Original owner refuses.');
  fireEvent.focus(env.input());
  fireEvent.keyDown(env.input(), { key: 'Enter' });
  expect(env.submit).toHaveBeenCalledTimes(2);
  expect(otherPort.submit).toHaveBeenCalledTimes(1);
  expect(env.applyEdit).not.toHaveBeenCalled();
});

it.each(['desktop'] as const)('releases a clean %s capture on row teardown before the next edit', async (deviceClass) => {
  const env = await setup(deviceClass);
  fireEvent.focus(env.input());
  env.remote();
  env.unmount();
  expect(env.submit).not.toHaveBeenCalled();
  render(<env.Track />);
  const reopened = env.input();
  expect(reopened).toHaveValue('Remote');
  fireEvent.focus(reopened);
  fireEvent.change(reopened, { target: { value: 'Next intent' } });
  fireEvent.blur(reopened);
  expect(env.capture).toHaveBeenCalledTimes(2);
  expect(env.submit).toHaveBeenCalledTimes(1);
  expect(env.submit.mock.calls[0][0].command.expect).toEqual({
    'parent/track:V1::label': { state: 'present', value: 'Remote' },
  });
  expect(env.applyEdit).not.toHaveBeenCalled();
});

// A retained authored capture uses the remounted owner's current local policy.
describe.each(['desktop'] as const)('%s live-policy retry', (deviceClass) => {
  it('uses the unlocked remount policy after the original hook refused a new lock', async () => {
    const env = await setup(deviceClass);
    const input = env.input();
    fireEvent.focus(input);
    fireEvent.change(input, { target: { value: 'Keep until unlocked' } });
    env.rerender(<env.Track editability={createTimelineEditability({ lockedTrackIds: ['V1'] })} />);
    fireEvent.blur(input);
    expect(screen.getByRole('alert')).toHaveTextContent('track_locked');
    env.unmount();
    expect(env.finish).not.toHaveBeenCalled();
    const remounted = render(<env.Track />);
    const reopened = env.input();
    expect(reopened).toHaveValue('Keep until unlocked');
    fireEvent.focus(reopened);
    fireEvent.blur(reopened);
    expect(env.capture).toHaveBeenCalledTimes(1);
    expect(env.submit).toHaveBeenCalledTimes(1);
    expect(env.submit.mock.calls[0][0].command.expect).toEqual({
      'parent/track:V1::label': { state: 'present', value: 'Original' },
    });
    expect(env.applyEdit).not.toHaveBeenCalled();
    remounted.unmount();
  });

  it.each(['track_locked', 'timeline_read_only', 'canonical_shot_draft_active'] as const)(
    'retains the original draft through %s refusal and retries after unlock', async (reason) => {
      const env = await setup(deviceClass);
      env.submit.mockImplementation(() => { throw new Error('Temporary synchronous refusal'); });
      const input = env.input();
      fireEvent.focus(input);
      fireEvent.change(input, { target: { value: 'Keep guarded intent' } });
      env.remote();
      env.unmount();
      expect(env.submit).toHaveBeenCalledTimes(1);
      const basis = env.finish.mock.calls[0][0];
      const original = env.submit.mock.calls[0][0];
      const editability = reason === 'canonical_shot_draft_active'
        ? { ...createTimelineEditability(), checkTimeline: () => ({ allowed: false, reason }) }
        : createTimelineEditability({ lockedTrackIds: reason === 'track_locked' ? ['V1'] : [],
          readOnly: reason === 'timeline_read_only' });
      env.submit.mockImplementation(() => {});
      const remounted = render(<env.Track editability={editability} />);
      const reopened = env.input();
      expect(reopened).toHaveValue('Keep guarded intent');
      expect(screen.getByRole('alert')).toHaveTextContent('Temporary synchronous refusal');
      expect(env.finish).toHaveBeenCalledTimes(1);
      expect(env.submit).toHaveBeenCalledTimes(1);
      fireEvent.focus(reopened);
      fireEvent.blur(reopened);
      expect(screen.getByRole('alert')).toHaveTextContent(reason);
      expect(reopened).toHaveValue('Keep guarded intent');
      expect(env.finish).toHaveBeenCalledTimes(1);
      expect(env.submit).toHaveBeenCalledTimes(1);
      remounted.unmount();
      const unlocked = render(<env.Track />);
      const retry = env.input();
      expect(retry).toHaveValue('Keep guarded intent');
      expect(screen.getByRole('alert')).toHaveTextContent(reason);
      fireEvent.focus(retry);
      fireEvent.keyDown(retry, { key: 'Enter' });
      fireEvent.blur(retry);
      unlocked.unmount();
      expect(env.capture).toHaveBeenCalledTimes(1);
      expect(env.finish).toHaveBeenCalledTimes(2);
      expect(env.finish.mock.calls[1][0]).toBe(basis);
      expect(env.submit).toHaveBeenCalledTimes(2);
      expect(env.submit.mock.calls[1][0]).toEqual(original);
      expect(original.command.expect).toEqual({
        'parent/track:V1::label': { state: 'present', value: 'Original' },
      });
      expect(env.applyEdit).not.toHaveBeenCalled();
    },
  );
});
