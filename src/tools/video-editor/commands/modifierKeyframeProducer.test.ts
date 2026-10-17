import {describe, expect, it} from 'vitest';
import {compositeEffectGestureCommands} from './semanticGestures';
import {configToRows, rowsToConfig} from '../lib/timeline-data';
import {sanitizeTimelineClipSnapshot} from '../lib/timeline-domain';
import type {TimelineConfig} from '../types';

const path = 'modifiers["shade"].params.strength';
const keys = {
  [path]: [{time: 0, value: 0, interpolation: 'linear' as const, opaque: {retain: [null, false, 1.125]}},
    {time: 1, value: 1, interpolation: 'linear' as const}],
  'literal.key[0]': [{time: 7.125, value: false, interpolation: 'hold' as const, opaque: {old: true}}],
};
const target = {id: 'target', at: 2, hold: 2, track: 'v', clipType: 'media' as const, keyframeOrigin: .25,
  modifiers: [{id: 'shade', element: 'timeline.component/fresh_vignette_029.vignette', params: {strength: .2}}]};

describe('existing complete-pair modifier keyframe producer and save projection', () => {
  it('sends the stable instance-addressed map through the existing clip.set pair with exact captured expectations', () => {
    const data = {config: {clips: [target]}, tracks: [{id: 'v', kind: 'visual', label: 'Visual'}]} as never;
    const patch = {keyframes: structuredClone(keys), keyframeOrigin: .25};
    const before = structuredClone(target);
    const result = compositeEffectGestureCommands(data, 'target', patch);
    expect(result.commands).toEqual([{op: 'clip.set', select: 'parent/clip:target', resolved: ['parent/clip:target'],
      args: patch, expect: {keyframes: {state: 'absent'}, keyframeOrigin: {state: 'present', value: .25}}}]);
    patch.keyframes[path][0].value = .9;
    expect(result.commands![0].args.keyframes).toEqual(keys);
    expect(target).toEqual(before);
  });

  it('preserves both channels, opaque per-key siblings, static params and origin through rows and fresh JSON readback', () => {
    const config: TimelineConfig = {clips: [{...target, keyframes: structuredClone(keys)}],
      tracks: [{id: 'v', kind: 'visual', label: 'Visual'}], output: {fps: 20, resolution: '200x100', file: 'test.mp4'}};
    const rows = configToRows(config);
    const saved = JSON.parse(JSON.stringify(rows));
    const fresh = rowsToConfig(saved.rows, saved.meta, config.output, saved.clipOrder, saved.tracks);
    const loaded = sanitizeTimelineClipSnapshot(fresh.clips[0]);
    expect(loaded.keyframes).toEqual(keys);
    expect(loaded.keyframeOrigin).toBe(.25);
    expect(loaded.modifiers).toEqual(target.modifiers);
    expect(config.clips[0].modifiers![0].params).toEqual({strength: .2});
  });
});
