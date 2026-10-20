// @vitest-environment jsdom
import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { captureTrackLabel, finishTrackLabel } from '@/tools/video-editor/commands/trackLabelCapture.ts';
import type { AuthoredBundle } from '@/tools/video-editor/commands/clipMovePrimitives.ts';
import type { TrackLabelCapturePort } from '@/tools/video-editor/commands/trackLabelGesture.ts';
import type { JsonObject } from '@/tools/video-editor/commands/types.ts';
import { TrackInspector } from '@/tools/video-editor/components/PropertiesPanel/TrackInspector.tsx';
import { useTimelineTrackManagement } from '@/tools/video-editor/hooks/useTimelineTrackManagement.ts';
import { buildTimelineData } from '@/tools/video-editor/lib/timeline-data.ts';

async function setup() {
  const config = {
    output: { resolution: '1920x1080', fps: 30, file: 'out.mp4' },
    tracks: [{ id: 'V1', kind: 'visual' as const, label: 'Original' }],
    clips: [],
  };
  const dataRef = { current: await buildTimelineData(config, { assets: {} }) };
  const bundle: AuthoredBundle = {
    parent: { config: { tracks: [{ ...config.tracks[0], opaque: [null, false] }] } },
    placements: [],
    shots: {},
    base_parent: { revision_id: 'parent-r1', content_digest: 'sha256:original-parent' },
  };
  const capture = vi.fn<TrackLabelCapturePort['capture']>(() =>
    captureTrackLabel(bundle, 'parent/track:V1') as unknown as JsonObject);
  const finish = vi.fn<TrackLabelCapturePort['finish']>(finishTrackLabel);
  // This is the Inspector/session handoff, not a Runtime ACK or browser qualification.
  const submit = vi.fn<TrackLabelCapturePort['submit']>();
  const applyEdit = vi.fn();
  const onChange = vi.fn();
  const port: TrackLabelCapturePort = { capture, finish, submit };

  function Inspector({ visible = true, labelPort = port }: {
    visible?: boolean;
    labelPort?: TrackLabelCapturePort;
  }) {
    const ops = useTimelineTrackManagement({
      dataRef,
      resolvedConfig: dataRef.current.resolvedConfig,
      selectedClipId: null,
      setSelectedTrackId: vi.fn(),
      applyEdit,
      trackLabelPort: labelPort,
    });
    return visible ? <TrackInspector
      track={dataRef.current.resolvedConfig.tracks[0]}
      hasClips={false}
      onChange={onChange}
      onLabelEditStart={ops.handleTrackLabelEditStart}
      onAddTrack={vi.fn()}
      onRemove={vi.fn()}
    /> : null;
  }

  const view = render(<Inspector />);
  function remote() {
    (bundle.parent.config as { tracks: { label: string }[] }).tracks[0].label = 'Remote';
    dataRef.current.resolvedConfig.tracks[0] = { ...config.tracks[0], label: 'Remote' };
    view.rerender(<Inspector />);
  }
  return { ...view, Inspector, remote, bundle, dataRef, capture, finish, submit, applyEdit, onChange };
}

describe('touch TrackInspector command path', () => {
  it.each(['音楽 🎬', '', 'Original'])('submits %j with the original capture after a remote change', async (label) => {
    const env = await setup();
    const input = screen.getByRole('textbox', { name: 'Track name' });
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
        op: 'track.set',
        select: 'parent/track:V1',
        args: { values: { label }, clear: [] },
        expect: { 'parent/track:V1::label': { state: 'present', value: 'Original' } },
      }),
      preview: { version: 1, operations: [{ op: 'track.update', target: 'V1', payload: { label } }] },
    });
    expect(env.onChange).not.toHaveBeenCalled();
    expect(env.applyEdit).not.toHaveBeenCalled();
    expect(env.dataRef.current.resolvedConfig.tracks[0].label).toBe('Remote');
    expect((env.bundle.parent.config as { tracks: { opaque: unknown }[] }).tracks[0].opaque).toEqual([null, false]);
  });

  it('retains a dirty draft and its original capture when Inspector close refuses the save', async () => {
    const env = await setup();
    env.submit.mockImplementation(() => { throw new Error('Original label guard no longer holds.'); });
    const input = screen.getByRole('textbox', { name: 'Track name' });
    fireEvent.focus(input);
    fireEvent.change(input, { target: { value: 'Keep after close' } });

    // Closing/switching away unmounts the visible Inspector body; returning remounts it.
    env.rerender(<env.Inspector visible={false} />);
    expect(env.submit).toHaveBeenCalledTimes(1);
    expect(env.applyEdit).not.toHaveBeenCalled();
    env.rerender(<env.Inspector />);
    const reopened = screen.getByRole('textbox', { name: 'Track name' });
    expect(reopened).toHaveValue('Keep after close');
    expect(screen.getByRole('alert')).toHaveTextContent('Original label guard no longer holds.');

    env.remote();
    expect(reopened).toHaveValue('Keep after close');
    fireEvent.focus(reopened);
    fireEvent.keyDown(reopened, { key: 'Enter' });
    expect(env.submit).toHaveBeenCalledTimes(2);
    expect(env.submit.mock.calls[1][0]).toEqual(env.submit.mock.calls[0][0]);
    expect(env.capture).toHaveBeenCalledTimes(1);
    expect(env.onChange).not.toHaveBeenCalled();
  });

  it('retains typed input after capture refusal without entering a legacy edit path', async () => {
    const env = await setup();
    env.capture.mockImplementation(() => { throw new Error('Ambiguous track identity.'); });
    const input = screen.getByRole('textbox', { name: 'Track name' });
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
    expect(env.onChange).not.toHaveBeenCalled();
    expect(env.applyEdit).not.toHaveBeenCalled();
  });

  it('releases a clean close before a remote update and captures the next Inspector edit', async () => {
    const env = await setup();
    const input = screen.getByRole('textbox', { name: 'Track name' });
    fireEvent.focus(input);
    env.rerender(<env.Inspector visible={false} />);
    expect(env.submit).not.toHaveBeenCalled();
    env.remote();
    const reopened = screen.getByRole('textbox', { name: 'Track name' });
    expect(reopened).toHaveValue('Remote');
    fireEvent.focus(reopened);
    fireEvent.change(reopened, { target: { value: 'After close' } });
    fireEvent.blur(reopened);
    expect(env.capture).toHaveBeenCalledTimes(2);
    expect(env.submit).toHaveBeenCalledTimes(1);
    expect(env.submit.mock.calls[0][0].command.expect).toEqual({
      'parent/track:V1::label': { state: 'present', value: 'Remote' },
    });
    expect(env.onChange).not.toHaveBeenCalled();
    expect(env.applyEdit).not.toHaveBeenCalled();
  });
});
