import { describe, expect, it } from 'vitest';
import { queryDrawFrame, querySceneFrame, queryTrackFrame } from '@banodoco/timeline-composition/evaluation';
import { playerEvaluationClip, preparePlayerClipOpacity, preparePlayerTrack } from './playerEvaluation.ts';
import type { ResolvedTimelineClip, TrackDefinition } from '../types/index.ts';

const track: TrackDefinition = { id: 'V1', kind: 'visual', label: 'Picture' };
const image = (id: string, at: number, overrides: Partial<ResolvedTimelineClip> = {}): ResolvedTimelineClip => ({
  id, at, track: track.id, clipType: 'hold', hold: 1, asset: id,
  assetEntry: { type: 'image/png', src: `https://example.test/${id}.png` }, ...overrides,
});
const prepare = (clips: ResolvedTimelineClip[]) => preparePlayerTrack(track, clips, 30, 1920, 1080);

describe('Player planning with the built Composition evaluator', () => {
  it('evaluates authored opacity and object/array fades on the native content clock', () => {
    for (const fps of [24, 30, 24000 / 1001]) {
      for (const effects of [{ fade_in: 12 / fps, fade_out: 12 / fps },
        [{ fade_in: 12 / fps }, { fade_out: 12 / fps }]]) {
        const clip = image('fading', 30 / fps, { clipType: 'media', from: 90 / fps, to: 330 / fps,
          hold: 60 / fps, speed: 2, opacity: 0.4, effects });
        const original = structuredClone(clip);
        const opacityAt = preparePlayerClipOpacity(clip, fps);
        for (const [frame, multiplier] of [[-1, 0], [0, 0], [6, 0.5], [12, 1], [24, 0.5], [29, 1 / 12], [30, 0], [42, 0]]) {
          expect(opacityAt(frame)).toBeCloseTo(0.4 * multiplier, 12);
        }
        // A native transition can extend the content clock past the own span.
        expect(preparePlayerClipOpacity({ ...clip, effects: { fade_in: 12 / fps } }, fps)(42)).toBe(0.4);
        expect(preparePlayerClipOpacity({ ...clip, effects: { fade_in: 60 / fps, fade_out: 60 / fps } }, fps)(15))
          .toBeCloseTo(0.4 / 16, 12);
        expect(preparePlayerClipOpacity({ ...clip, effects: { fade_in: -1, fade_out: NaN } }, fps)(6)).toBe(0.4);
        expect(preparePlayerClipOpacity({ ...clip, opacity: 0 }, fps)(12)).toBe(0);
        expect(clip).toEqual(original);
      }
    }
  });

  it('keeps cuts and excluded ends half-open without an extra overlap frame', () => {
    const { scene, plans, clips } = prepare([image('b', 1), image('a', 0)]);
    expect(clips.map(clip => clip.id)).toEqual(['a', 'b']);
    expect(plans.get('a')).toMatchObject({ drawStart: 0, drawDuration: 30 });
    expect(queryTrackFrame(scene.tracks[0].prepared, 29).layers.map(layer => layer.clipIndex)).toEqual([0]);
    expect(queryTrackFrame(scene.tracks[0].prepared, 30).layers.map(layer => layer.clipIndex)).toEqual([1]);
    expect(queryTrackFrame(scene.tracks[0].prepared, 60).layers).toEqual([]);
  });

  it('keeps gaps empty and ordinary authored overlaps present', () => {
    const gap = prepare([image('a', 0), image('b', 2)]).scene;
    expect(querySceneFrame(gap, 45).layers).toEqual([]);
    const overlap = prepare([image('a', 0, { hold: 2 }), image('b', 1)]).scene;
    expect(querySceneFrame(overlap, 45).layers.map(layer => layer.clipId)).toEqual(['a', 'b']);
  });

  it('adapts valid trim and sanitized speed without rewriting source identity', () => {
    const clip = image('video', 2, { clipType: 'media', hold: undefined, from: 3, to: 7, speed: 2,
      assetEntry: { type: 'video/mp4', src: 'https://example.test/video.mp4' } });
    expect(prepare([clip]).plans.get(clip.id)).toMatchObject({ drawStart: 60, ownDuration: 60 });
    expect(playerEvaluationClip(clip)).toMatchObject({ from: 3, to: 7, hold: 4, speed: 2 });
    expect(clip.hold).toBeUndefined();
    for (const speed of [0, -1, NaN, Infinity]) {
      expect(prepare([{ ...clip, speed }]).plans.get(clip.id)?.ownDuration).toBe(120);
    }
    expect(prepare([image('invalid-trim', 0, { clipType: 'media', hold: undefined, from: 7, to: 3 })])
      .plans.get('invalid-trim')?.ownDuration).toBe(1);
  });

  it.each(['crossfade', 'cross-fade'])('uses shared %s windows and clamps own-frame before a nonzero boundary', type => {
    const { scene, plans } = prepare([image('a', 2), image('b', 3, { transition: { type, duration: 0.4 } })]);
    const incoming = plans.get('b')!;
    expect(incoming).toMatchObject({ drawStart: 78, drawDuration: 42, ownOffset: 12, ownDuration: 30 });
    expect(queryDrawFrame(incoming, 9)).toMatchObject({ ownFrame: 0, opacity: 0.75 });
    expect(queryDrawFrame(incoming, 17).ownFrame).toBe(5);
    const middle = querySceneFrame(scene, 84);
    expect(middle.layers.map(layer => layer.clipId)).toEqual(['a', 'b']);
    expect(middle.layers.map(layer => layer.transitionOpacity)).toEqual([1, 0.5]);
    expect(querySceneFrame(scene, 120).layers).toEqual([]);
  });

  it.each([
    { at: 2, duration: 0.5 }, // gap
    { at: 0.5, duration: 0.5 }, // overlap
    { at: 1, duration: 2 }, // too long
  ])('retains host timing for unsupported shared boundary %j', ({ at, duration }) => {
    const { plans } = prepare([image('a', 0), image('b', at, { transition: { type: 'crossfade', duration } })]);
    expect(plans.size).toBe(0);
  });

  it.each(['wipe', 'slide-push', 'zoom-through', 'custom:iris', 'missing'])('preserves %s without substituting a shared fade', type => {
    const { plans, scene } = prepare([image('a', 0), image('b', 1, { transition: { type, duration: 0.5 } })]);
    expect(plans.size).toBe(0);
    expect(scene.tracks[0].prepared.plans.every(plan => !plan.fadeIn && !plan.fadeOut)).toBe(true);
  });

  it('does not partly share a transition chain touching video or an injected effect', () => {
    for (const last of [image('c', 2, { assetEntry: { type: 'video/mp4', src: 'video.mp4' } }),
      image('c', 2, { continuous: { type: 'custom:audible', params: {} } })]) {
      const { plans } = prepare([image('a', 0), image('b', 1, { transition: { type: 'crossfade', duration: 0.3 } }),
        { ...last, transition: { type: 'crossfade', duration: 0.3 } }, image('unrelated', 5)]);
      expect([...plans.keys()]).toEqual(['unrelated']);
    }
  });

  it('keeps both sides of a shared image transition chain on the host clock when it touches fade', () => {
    const { plans, scene } = prepare([image('a', 0),
      image('b', 1, { transition: { type: 'crossfade', duration: 0.3 } }),
      image('c', 2, { transition: { type: 'fade', duration: 0.3 } }),
      image('d', 3, { transition: { type: 'cross-fade', duration: 0.3 } }), image('unrelated', 5)]);
    expect([...plans.keys()]).toEqual(['unrelated']);
    expect(scene.tracks[0].prepared.plans.every(plan => !plan.fadeIn && !plan.fadeOut)).toBe(true);
  });

  it('keeps undeclared custom and typed component internals unknown and present', () => {
    for (const clip of [image('custom', 0, { clipType: 'custom:unknown' }),
      image('typed', 0, { elementRef: { id: 'unknown', kind: 'effect', revision: 'r1' } })]) {
      const { scene, plans } = prepare([clip]);
      expect(plans.size).toBe(0);
      const layer = querySceneFrame(scene, 15).layers[0];
      expect(layer).toMatchObject({ clipId: clip.id, visible: 'unknown' });
      expect(layer.findings.some(finding => finding.code === 'unknown-component-internals')).toBe(true);
    }
  });

  it.each(['fade', 'crossfade', 'cross-fade'])('respects %s host dispatch when a native clip name is served by a custom component', type => {
    const { plans, scene } = preparePlayerTrack(track,
      [image('a', 0), image('b', 1, { transition: { type, duration: 0.5 } })],
      30, 1920, 1080, clip => clip.id !== 'a');
    expect(plans.size).toBe(0);
    expect(querySceneFrame(scene, 15).layers[0].visible).toBe('unknown');
  });
});
