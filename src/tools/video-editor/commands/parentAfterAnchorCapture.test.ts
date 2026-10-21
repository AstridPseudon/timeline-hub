import { describe, expect, it } from 'vitest';
import type { JSON, MediaSelection, VerifiedMedia } from '@/integrations/runtime/timeline-commit-types.ts';
import {
  captureParentClipAddMediaAfterAnchor,
  finishParentClipAddMediaAfterAnchor,
} from './parentAfterAnchorCapture.ts';
import { ClipMoveError, copy } from './clipMovePrimitives.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';

const media: MediaSelection = {
  asset: 'reserved-new',
  generation_id: 'generation-new',
  variant_id: 'variant-new',
  object_id: 'sha256:2222222222222222222222222222222222222222222222222222222222222222',
  catalog_digest: 'sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
};
const verified: VerifiedMedia = { selection: media, media_type: 'video/fixture', size: 123, duration_seconds: 10 };

function bundle(): AuthoredBundle {
  const clips: Record<string, JSON>[] = [
    { id: 'before', clipType: 'video', asset: 'picture', track: 'overlay', at: 0, hold: 1 },
    { id: 'anchor', clipType: 'video', asset: 'picture', track: 'overlay', at: 1.003, hold: 4,
      from: 2, to: 6, speed: 2, at_ms: 1003, effectId: 'effect-anchor', opaque: { keep: [null, false, {}] } },
    { id: 'later', clipType: 'video', asset: 'picture', track: 'overlay', at: 6, hold: 1, at_ms: 6000 },
    { id: 'other', clipType: 'video', asset: 'picture', track: 'other', at: 2, hold: 1 },
  ];
  const config = {
    output: { fps: { numerator: 24, denominator: 1 } },
    tracks: [
      { id: 'overlay', kind: 'visual', role: 'output' },
      { id: 'other', kind: 'visual', role: 'output' },
    ],
    clips: copy(clips),
    registry: { assets: {
      picture: { media_id: 'sha256:1111111111111111111111111111111111111111111111111111111111111111', type: 'video' },
    } },
  } as Record<string, JSON>;
  return {
    schema_version: 1,
    project_id: 'project-1',
    timeline_id: 'film',
    parent: { config, clips, registry: copy(config.registry) },
    placements: [{ occurrence_id: 'occ-a', track: 'other', placement: { track: 'other' } }],
    shots: {},
  } as AuthoredBundle;
}

describe('dormant parent after-anchor media capture', () => {
  it('matches Agent raw clone, rate-aware ripple, opaque data, and complete claims', () => {
    const input = bundle();
    const basis = captureParentClipAddMediaAfterAnchor(input, 'parent/clip:anchor', { id: 'born' }, media, [verified]);
    const result = finishParentClipAddMediaAfterAnchor(
      basis,
    );
    const rows = result.bundle.parent.clips as Record<string, JSON>[];

    expect(result.command).toMatchObject({
      schema_version: 1, op: 'clip.add-media', version: '1', select: 'parent/clip:anchor',
      args: { media, row: { id: 'born', asset: media.asset, track: 'overlay', at: 3.003, at_ms: 3003,
        from: 2, to: 6, speed: 2, effectId: 'effect-born', opaque: { keep: [null, false, {}] } } },
    });
    expect(result.command.args).not.toHaveProperty('afterClipId');
    expect(rows.map((row) => row.id)).toEqual(['before', 'anchor', 'born', 'later', 'other']);
    expect(rows.find((row) => row.id === 'later')).toMatchObject({ at: 8, at_ms: 8000 });
    expect(rows.find((row) => row.id === 'other')).toMatchObject({ at: 2 });
    expect(result.record.selections.find((item) => item.key === 'collection.clips.after')).toEqual({
      key: 'collection.clips.after', query_version: 1, owner: 'parent', members: ['parent/clip:anchor'],
      order: ['parent/clip:before', 'parent/clip:anchor', 'parent/clip:later', 'parent/clip:other'],
      boundaries: ['parent/clip:anchor', 'parent/clip:later'],
      policy: 'guard-membership',
    });
    expect(result.record.reads).toEqual(expect.arrayContaining([
      expect.objectContaining({ ref: 'parent/clip:anchor', path: [] }),
      expect.objectContaining({ ref: 'parent/asset:picture', path: [] }),
      expect.objectContaining({ ref: 'parent', path: ['config', 'output', 'fps'] }),
      expect.objectContaining({ ref: 'parent/clip:later', path: ['track'] }),
      expect.objectContaining({ ref: 'parent/clip:later', path: [] }),
      expect.objectContaining({ ref: 'parent/clip:other', path: ['track'] }),
    ]));
    expect(result.record.writes).toEqual(expect.arrayContaining([
      expect.objectContaining({ ref: 'parent/clip:later', path: ['at'] }),
      expect.objectContaining({ ref: 'parent/clip:later', path: ['at_ms'] }),
    ]));
    expect(result.record.bindings).toEqual(expect.arrayContaining([
      expect.objectContaining({ key: 'parent.after-clip', ref: 'parent/clip:anchor' }),
      expect.objectContaining({ key: 'parent.after-track', ref: 'parent/track:overlay' }),
    ]));
    expect(result.record.created.map((item) => item.ref)).toEqual(['parent/asset:reserved-new', 'parent/clip:born']);
    expect(input.parent.clips).toEqual(bundle().parent.clips);
  });

  it('keeps the selected tuple and reserved IDs across JSON reload, and rejects wrong ownership or identity', () => {
    const input = bundle();
    const basis = captureParentClipAddMediaAfterAnchor(input, 'parent/clip:anchor', { id: 'born' }, media, [verified]);
    expect(finishParentClipAddMediaAfterAnchor(JSON.parse(JSON.stringify(basis)))).toEqual(
      finishParentClipAddMediaAfterAnchor(basis),
    );
    expect(() => captureParentClipAddMediaAfterAnchor(input, 'occurrence:occ-a', { id: 'born' }, media, [verified]))
      .toThrowError(ClipMoveError);
    expect(() => captureParentClipAddMediaAfterAnchor(input, 'parent/clip:missing', { id: 'born' }, media, [verified]))
      .toThrowError(ClipMoveError);
    const ambiguous = bundle();
    const duplicate = copy((ambiguous.parent.clips as Record<string, JSON>[])[1]);
    (ambiguous.parent.clips as Record<string, JSON>[]).push(duplicate);
    ((ambiguous.parent.config as Record<string, JSON>).clips as Record<string, JSON>[]).push(copy(duplicate));
    expect(() => captureParentClipAddMediaAfterAnchor(ambiguous, 'parent/clip:anchor', { id: 'born' }, media, [verified]))
      .toThrowError(ClipMoveError);
    const changed = copy(basis.command);
    (changed.args.media as Record<string, JSON>).catalog_digest =
      'sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc';
    expect(() => finishParentClipAddMediaAfterAnchor({ ...basis, command: changed })).toThrowError(ClipMoveError);
  });
});
