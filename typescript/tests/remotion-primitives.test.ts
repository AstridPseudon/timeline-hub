import assert from 'node:assert/strict';
import {test} from 'node:test';
import {Easing, interpolate as canonicalInterpolate, spring as canonicalSpring} from 'remotion';
import {interpolate, spring} from '../src/lib/remotion-primitives.generated.js';
import {builtinClipLookStyle} from '../src/lib/clip-look';

test('compiled primitives equal the installed canonical spring and interpolation on bounded vectors', () => {
  for (const fps of [24, 30, 24000 / 1001]) {
    for (const durationInFrames of [1, 12, 18, 31]) {
      for (const frame of [-1, 0, .5, 1, 6, 12, 18, 31, 60]) {
        for (const config of [{}, {damping: 14, stiffness: 110},
          {damping: 20, stiffness: 120, mass: .75, overshootClamping: true}]) {
          const input = {fps, durationInFrames, frame, config, from: -.2, to: 1.3};
          assert.equal(spring(input), canonicalSpring(input));
        }
        const progress = canonicalSpring({fps, durationInFrames, frame, config: {damping: 14, stiffness: 110}});
        for (const id of ['fade-up', 'scale-in'] as const) {
          const style = builtinClipLookStyle(id, frame, durationInFrames, fps);
          assert.equal(style.opacity, progress);
          assert.equal(id === 'fade-up' ? style.translateY : style.scale,
            canonicalInterpolate(progress, [0, 1], id === 'fade-up' ? [40, 0] : [.85, 1]));
        }
      }
    }
  }
  for (const input of [-1, 0, .125, .5, 1, 2]) {
    for (const easing of [Easing.linear, Easing.inOut(Easing.quad), Easing.bezier(.25, .1, .25, 1)]) {
      for (const extrapolate of ['extend', 'clamp', 'identity', 'wrap'] as const) {
        const options = {easing, extrapolateLeft: extrapolate, extrapolateRight: extrapolate};
        assert.equal(interpolate(input, [0, .5, 1], [40, 10, 0], options),
          canonicalInterpolate(input, [0, .5, 1], [40, 10, 0], options));
      }
    }
  }
});
