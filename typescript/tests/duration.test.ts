import assert from 'node:assert/strict';
import {test} from 'node:test';
import {getTimelineDurationInFrames, type TimelineClip} from '../src/index';

const clip: TimelineClip = {id: 'clip', at: 0, hold: 1, track: 'visual'};
const resolvedConfig: {clips: TimelineClip[]; theme?: string; resolvedOnly: true} = {
  clips: [clip], resolvedOnly: true,
};

test('timeline duration accepts clip-only, resolved, and full-config inputs', () => {
  assert.equal(getTimelineDurationInFrames({clips: [clip]}, 30), 30);
  assert.equal(getTimelineDurationInFrames(resolvedConfig, 30), 30);
  assert.equal(getTimelineDurationInFrames({
    theme: 'default', clips: [clip], tracks: [], output: {},
    pinnedShotGroups: undefined, theme_overrides: undefined,
  }, 30), 30);
});
