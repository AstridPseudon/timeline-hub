// Resolve stored visual fields with the INSTALLED composition package, the same calls the renderer makes.
// argv[2]: JSON {fps, rows: [{key, clip}]}; stdout: JSON {key: what the package draws}.
import fs from 'node:fs';
import {DEFAULT_THEME, toRuntimeTheme, prepareCompositionScene, compileCanonicalTransitions} from '@banodoco/timeline-composition';
import {resolveAnimationReferences} from '@banodoco/timeline-composition/theme-api';
import {clipOpacity} from '@banodoco/timeline-composition/evaluation';

const {fps, rows} = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const theme = toRuntimeTheme(DEFAULT_THEME);
const track = {id: 'visual', kind: 'visual', label: 'Visual'};
const phases = (clip) => Object.fromEntries(['entrance', 'exit'].filter((phase) => clip[phase] !== undefined).map((phase) => [
  phase, resolveAnimationReferences(clip[phase], phase).map(({id, durationFrames, easing}) => ({id, durationFrames, easing: easing ?? null})),
]));
const incoming = (clip) => {
  // The transition is declared on the incoming clip B (A -> B), as published.
  const clips = [{id: 'a', track: 'visual', at: 0, hold: 2, clipType: 'text-card'},
    {id: 'b', track: 'visual', at: 2, hold: 2, clipType: 'text-card', transition: clip.transition}];
  const compiled = compileCanonicalTransitions([{track, clips}], fps, theme);
  const plan = prepareCompositionScene([{track, clips}], {assets: {}}, fps, theme, 1920, 1080, undefined,
    {a: 'a', b: 'b'}, {}, 'host', {}, undefined, compiled).tracks[0].prepared.plans[1];
  return {frames: compiled.tracks[0].incomingTransitions[1].T, drawStart: plan.drawStart, ownOffset: plan.ownOffset};
};
const out = {};
for (const {key, clip} of rows) {
  const drawn = phases(clip);
  if (clip.transition !== undefined) drawn.transition = incoming(clip);
  if (clip.effects !== undefined) {
    drawn.opacity = [0, 3, 6, 40, 47].map((frame) => Math.round(clipOpacity({id: 'a', track: 'visual', at: 0, hold: 2, effects: clip.effects}, frame, fps) * 1e4) / 1e4);
  }
  out[key] = drawn;
}
console.log(JSON.stringify(out));
