import { describe, expect, it } from 'vitest';
import { buildTimelineCommandData } from './timelineData.ts';
import fixture from './fixtures/recipe_m2_app_track_create.json';
import {
  captureTrackCreateEdit,
  projectTrackCreatePreview,
  submitTrackCreateEdit,
  trackCreatePreview,
  type TrackCreateCapturePort,
} from './trackCreateGesture.ts';
import { captureTrackCreate, finishTrackCreate, type TrackCreateArgs } from './trackCreateCapture.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';

const bundle = fixture.bundle as unknown as AuthoredBundle;
const row = fixture.input.row as TrackCreateArgs['row'];

function current() {
  const parent = bundle.parent;
  return buildTimelineCommandData({ ...(parent.config as never), clips: parent.clips } as never, { assets: {} });
}

describe('parent track.create gesture port', () => {
  it('keeps the reserved full row through capture, submit, and local projection', () => {
    const port: TrackCreateCapturePort = {
      capture: () => captureTrackCreate(bundle, { row }),
      finish: (basis, args) => {
        const result = finishTrackCreate(basis, args);
        return { command: result.command, preview: trackCreatePreview(args.row) };
      },
      submit: ({ command, preview }) => {
        expect(command.op).toBe('track.create');
        expect(preview).toEqual(trackCreatePreview(row));
      },
    };
    const captured = captureTrackCreateEdit(port, current(), row);

    submitTrackCreateEdit(captured);
    const projected = projectTrackCreatePreview(trackCreatePreview(row), current());

    expect(projected?.config.tracks.at(-1)).toEqual(row);
    expect(projected?.resolvedConfig.tracks.at(-1)).toEqual(row);
    expect(captured.row).toEqual(row);
  });

  it('refuses a duplicate displayed identity before local projection', () => {
    const duplicate = { ...row, id: 'picture' };
    expect(() => projectTrackCreatePreview(trackCreatePreview(duplicate), {
      ...current(), config: { ...current().config, tracks: [...current().config.tracks, duplicate as never] },
    })).toThrow('Invalid native track.create preview');
  });
});
