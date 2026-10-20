import { describe, expect, it } from 'vitest';
import type { EditCommand, JSON, MediaSelection, VerifiedMedia } from '@/integrations/runtime/timeline-commit-types.ts';
import {
  executeParentClipSwapMedia,
  parentClipMediaSelection,
} from './parentClipAddCapture.ts';
import {
  captureParentClipSwapMedia,
  finishParentClipSwapMedia,
} from './parentClipSwapCapture.ts';
import { ClipMoveError, copy } from './clipMovePrimitives.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';

const oldMedia: MediaSelection = {
  asset: 'reserved-old',
  generation_id: 'generation-old',
  variant_id: 'variant-old',
  object_id: 'sha256:1111111111111111111111111111111111111111111111111111111111111111',
  catalog_digest: 'sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
};
const newMedia: MediaSelection = {
  asset: 'reserved-new',
  generation_id: 'generation-new',
  variant_id: 'variant-new',
  object_id: 'sha256:2222222222222222222222222222222222222222222222222222222222222222',
  catalog_digest: 'sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
};
const verified: VerifiedMedia = { selection: newMedia, media_type: 'video/fixture', size: 123, duration_seconds: 8 };

function binding(media: MediaSelection) {
  return {
    media_id: media.object_id,
    type: 'video',
    generationId: media.generation_id,
    variantId: media.variant_id,
    catalog_digest: media.catalog_digest,
  } as Record<string, JSON>;
}

function bundle(): AuthoredBundle {
  const clips: JSON[] = [{
    id: 'clip-a', track: 'overlay', at: 3.003, hold: 4, from: 2, to: 6, speed: 2,
    clipType: 'video', asset: oldMedia.asset, opaque: { keep: [null, false, 0] },
  }];
  const registry = { assets: { [oldMedia.asset]: binding(oldMedia) } } as Record<string, JSON>;
  const config = {
    output: { fps: 30 },
    tracks: [{ id: 'overlay', kind: 'visual', role: 'output', opaque: { lane: true } }],
    clips: copy(clips),
    registry: copy(registry),
  } as Record<string, JSON>;
  return {
    schema_version: 1,
    project_id: 'project-1',
    timeline_id: 'film',
    parent: { config, clips, registry: copy(registry) },
    placements: [],
    shots: {},
  } as AuthoredBundle;
}

describe('native parent clip.swap-media capture', () => {
  it('changes only the raw asset while preserving the complete clip carrier', () => {
    const input = bundle(), before = copy(input);
    const basis = captureParentClipSwapMedia(input, 'clip-a', newMedia);
    const result = finishParentClipSwapMedia(basis, verified);
    const clip = result.bundle.parent.clips[0] as Record<string, JSON>;
    const newBinding = binding(newMedia);
    delete newBinding.catalog_digest;

    expect(result.command).toMatchObject({
      schema_version: 1, op: 'clip.swap-media', version: '1', select: 'parent/clip:clip-a',
      args: { old_media: oldMedia, media: newMedia }, intent: { ownership: 'parent' }, resolved: [],
      bindings: { 'media.target': 'parent/clip:clip-a' },
    });
    expect(result.record.bindings).toContainEqual({ key: 'media.owner', ref: 'parent', policy: 'fixed', dependencies: [] });
    expect(clip).toEqual({ ...before.parent.clips[0] as Record<string, JSON>, asset: newMedia.asset });
    expect((result.bundle.parent.config as Record<string, JSON>).clips).toEqual(result.bundle.parent.clips);
    expect((result.bundle.parent.registry as Record<string, JSON>).assets).toEqual({
      [oldMedia.asset]: binding(oldMedia), [newMedia.asset]: newBinding,
    });
    expect((result.bundle.parent.config as Record<string, JSON>).registry).toEqual(result.bundle.parent.registry);
    expect(result.record.dependencies).toEqual([
      { key: 'media.old', kind: 'media', pin: oldMedia, policy: 'exact' },
      { key: 'media.new', kind: 'media', pin: newMedia, policy: 'exact' },
    ]);
    expect(input).toEqual(before);
    expect(executeParentClipSwapMedia(input, result.command, [verified])).toEqual(result);
  });

  it('retains the exact captured target and new selection across JSON retry', () => {
    const basis = captureParentClipSwapMedia(bundle(), 'clip-a', copy(newMedia));
    const first = finishParentClipSwapMedia(JSON.parse(JSON.stringify(basis)), copy(verified));
    const changed = copy(newMedia);
    changed.catalog_digest = 'sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc';
    expect(first.command.args.media).toEqual(newMedia);
    expect(basis.command.args.old_media).toEqual(oldMedia);
    expect(() => finishParentClipSwapMedia(basis, { ...verified, selection: changed })).toThrow(ClipMoveError);
  });

  it('keeps an untrimmed raw video clip untrimmed during replacement', () => {
    const input = bundle();
    const clip = input.parent.clips[0] as Record<string, JSON>;
    const mirror = ((input.parent.config as Record<string, JSON>).clips as JSON[])[0] as Record<string, JSON>;
    delete clip.from;
    delete clip.to;
    delete mirror.from;
    delete mirror.to;
    const result = finishParentClipSwapMedia(captureParentClipSwapMedia(input, 'clip-a', newMedia), verified);
    const replaced = result.bundle.parent.clips[0] as Record<string, JSON>;
    expect(replaced).not.toHaveProperty('from');
    expect(replaced).not.toHaveProperty('to');
    expect(replaced).toMatchObject({ hold: 4, speed: 2, asset: newMedia.asset });
  });

  it('refuses a changed old carrier without mutating it', () => {
    const original = bundle();
    const basis = captureParentClipSwapMedia(original, 'clip-a', newMedia);
    const changed = copy(original);
    const changedAssets = (changed.parent.registry as Record<string, JSON>).assets as Record<string, JSON>;
    const changedBinding = changedAssets[oldMedia.asset] as Record<string, JSON>;
    changedBinding.media_id = 'sha256:3333333333333333333333333333333333333333333333333333333333333333';
    const before = copy(changed);
    const command = basis.command as EditCommand;
    expect(() => executeParentClipSwapMedia(changed, command, [verified])).toThrowError(ClipMoveError);
    expect(changed).toEqual(before);
    expect(parentClipMediaSelection(original, 'clip-a')).toEqual(oldMedia);
  });
});
