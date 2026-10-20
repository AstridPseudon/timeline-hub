import assert from 'node:assert/strict';
import {test} from 'node:test';
import type {CSSProperties, ReactElement} from 'react';
import {clipOpacity, prepareScene, querySceneFrame, VIDEO_INTERPRETATION} from '../src/evaluation';
import {clipOpacity as internalClipOpacity} from '../src/lib/clip-look';
import {composeClipLook} from '../src/ClipLook';
import {DEFAULT_THEME, toRuntimeTheme} from '../src/ThemeContext';
import type {TimelineClip, TrackDefinition} from '../src/types';

const theme = toRuntimeTheme(DEFAULT_THEME);
const track: TrackDefinition = {id: 'v', kind: 'visual', label: 'Picture'};
const hash = 'a'.repeat(64);
const assets = {assets: {video: {file: 'video.mp4', type: 'video/mp4',
  resolution: '1920x1080', content_sha256: hash}}};
const capabilities = {media: {video: {version: 1 as const, objectId: `sha256:${hash}`,
  contentSha256: hash, file: 'video.mp4', interpretation: VIDEO_INTERPRETATION,
  stream: {index: 0, codec: 'h264' as const, pixelFormat: 'yuv420p', profile: 'Main', level: '40',
    sampleAspectRatio: '1:1' as const, width: 1920, height: 1080}}}};
const clip = (fps: number, overrides: Partial<TimelineClip> = {}): TimelineClip => ({
  id: 'clip', track: 'v', at: 60 / fps, hold: 30 / fps, asset: 'video', opacity: .4, ...overrides,
});
const normalOpacity = (clip: TimelineClip, frame: number, fps: number): number => {
  const tree = composeClipLook({clip, fps, kind: 'element', children: 'content'}, frame, theme) as ReactElement<{style: CSSProperties}>;
  const opacity = tree.props.style.opacity ?? 1;
  assert.ok(typeof opacity === 'number');
  return opacity;
};
const close = (actual: number, expected: number) => assert.ok(Math.abs(actual - expected) < 1e-12,
  `Expected ${expected}, got ${actual}`);

test('public clip opacity is the existing function and matches normal look and real scene clocks', () => {
  assert.strictEqual(clipOpacity, internalClipOpacity);
  for (const fps of [24, 30, 24000 / 1001]) {
    for (const speed of [.5, 1, 2]) {
      for (const source of [
        {hold: 30 * speed / fps, from: 90 / fps, to: 330 / fps},
        {hold: undefined, from: 90 / fps, to: (90 + 30 * speed) / fps},
      ]) {
        for (const effects of [{fade_in: 12 / fps, fade_out: 12 / fps},
          [{fade_in: 12 / fps}, {fade_out: 12 / fps}]]) {
          const target = clip(fps, {...source, speed, effects});
          const before = structuredClone(target);
          const scene = prepareScene([{track, clips: [target], transitions: []}], assets,
            fps, 1920, 1080, {capabilities});
          assert.equal(scene.tracks[0].prepared.plans[0].ownDuration, 30);
          for (const [frame, multiplier] of [[-1, 0], [0, 0], [6, .5], [12, 1],
            [18, 1], [24, .5], [29, 1 / 12], [30, 0], [42, 0]]) {
            const expected = .4 * multiplier;
            close(clipOpacity(target, frame, fps), expected);
            close(normalOpacity(target, frame, fps), expected);
            const answer = querySceneFrame(scene, 60 + frame);
            if (frame >= 0 && frame < 30) {
              assert.equal(answer.layers[0].contentFrame, frame);
              close(answer.layers[0].opacity!, expected);
            } else assert.deepEqual(answer.layers, []);
          }
          assert.deepEqual(target, before);
        }
      }
    }
  }
});

test('overlapping fades multiply, zero alpha survives, and invalid or subframe fades are ignored', () => {
  for (const fps of [24, 30, 24000 / 1001]) {
    for (const [effects, multiplier] of [
      [{fade_in: 60 / fps, fade_out: 60 / fps}, 1 / 16],
      [[{fade_in: 60 / fps}, {fade_out: 60 / fps}], 1 / 16],
      [{fade_in: -1, fade_out: NaN}, 1],
      [[{fade_in: Infinity}, {fade_out: -Infinity}], 1],
      [{fade_in: .1 / fps, fade_out: 0}, 1],
      [undefined, 1],
    ] as const) {
      for (const opacity of [undefined, 0, .4, 2, -1]) {
        const target = clip(fps, {opacity, effects: effects as TimelineClip['effects']});
        const expected = Math.min(1, Math.max(0, (opacity ?? 1) * multiplier));
        const scene = prepareScene([{track, clips: [target], transitions: []}], assets,
          fps, 1920, 1080, {capabilities});
        close(clipOpacity(target, 15, fps), expected);
        close(normalOpacity(target, 15, fps), expected);
        close(querySceneFrame(scene, 75).layers[0].opacity!, expected);
      }
    }
  }
});

test('fade-out follows rounded native duration with a one-frame minimum', () => {
  for (const fps of [24, 30, 24000 / 1001]) {
    for (const [duration, frames, sample, multiplier] of [
      [30.49, 30, 24, .5], [30.51, 31, 24, 7 / 12], [0, 1, 0, 1 / 12],
    ]) {
      const target = clip(fps, {hold: duration * 2 / fps, speed: 2,
        effects: {fade_out: 12 / fps}});
      const scene = prepareScene([{track, clips: [target], transitions: []}], assets,
        fps, 1920, 1080, {capabilities});
      assert.equal(scene.tracks[0].prepared.plans[0].ownDuration, frames);
      close(clipOpacity(target, sample, fps), .4 * multiplier);
      close(normalOpacity(target, sample, fps), .4 * multiplier);
      close(querySceneFrame(scene, 60 + sample).layers[0].opacity!, .4 * multiplier);
      assert.deepEqual(querySceneFrame(scene, 60 + frames).layers, []);
      assert.equal(clipOpacity(target, frames, fps), 0);
    }
  }
});

test('transition handles use content frames and compose track and transition alpha once', () => {
  for (const fps of [24, 30, 24000 / 1001]) {
    const previous = clip(fps, {id: 'previous'});
    const target = clip(fps, {at: 90 / fps, speed: 2, hold: 60 / fps,
      effects: {fade_in: 12 / fps}});
    const scene = prepareScene([{track: {...track, opacity: .5}, clips: [previous, target],
      transitions: [{T: 12, kind: 'dissolve', align: 'end', incomingPolicy: 'preroll-crossfade'}]}],
    assets, fps, 1920, 1080, {capabilities});
    const before = structuredClone(scene);
    for (const [frame, contentFrame, transitionOpacity, appearance] of [
      [78, 0, 0, 0], [84, 6, .5, .2], [90, 12, 1, .4], [119, 41, 1, .4],
    ]) {
      const layer = querySceneFrame(scene, frame).layers.find(layer => layer.clipId === target.id)!;
      assert.equal(layer.contentFrame, contentFrame);
      assert.equal(layer.transitionOpacity, transitionOpacity);
      close(clipOpacity(target, contentFrame, fps), appearance);
      close(normalOpacity(target, contentFrame, fps), appearance);
      close(layer.opacity!, .5 * transitionOpacity * appearance);
    }
    assert.deepEqual(querySceneFrame(scene, 120).layers, []);
    // Standalone appearance remains defined beyond the real half-open draw end.
    assert.equal(clipOpacity(target, 42, fps), .4);
    assert.deepEqual(scene, before);
  }
});
