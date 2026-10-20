import { readFileSync } from 'node:fs';
import { captureClipMove, finishClipMove } from './src/tools/video-editor/commands/clipMoveCapture.ts';
import { captureGenericPatch } from './src/tools/video-editor/commands/genericPatchCapture.ts';
import type { AuthoredBundle } from './src/tools/video-editor/commands/clipMovePrimitives.ts';
import { computeMediaTrim } from '@banodoco/timeline-composition/evaluation';

const fixture = (name: string): any => JSON.parse(readFileSync(new URL(
  `./src/tools/video-editor/commands/fixtures/${name}`,
  import.meta.url,
), 'utf8'));

const label = fixture('recipe_m2_app_track_label.json');
const move = fixture('recipe_m1_move.json');
const bundle = label.bundle as AuthoredBundle;
const patch = {
  version: 1,
  operations: [
    { op: 'clip.update', target: 'parent-clip', payload: { hold: 1.23456789 }, order: 1 },
    { op: 'track.update', target: 'picture', payload: { label: 'ordinary-🎬', mode: 'merge' }, order: 2 },
  ],
};
const holdLabel = captureGenericPatch(bundle, patch, (operation) =>
  operation.op === 'clip.update' ? 'parent/clip:parent-clip' : 'parent/track:picture');
const moved = finishClipMove(captureClipMove(move.bundle, move.select), move.on);
const trim = computeMediaTrim({ from: 0.5, to: 1.5 }, 30);

if (typeof computeMediaTrim !== 'function') throw new Error('public13 computeMediaTrim export is unavailable');
if (trim.trimBefore !== 15 || trim.trimAfter !== 45) throw new Error(`unexpected trim: ${JSON.stringify(trim)}`);
if (holdLabel.commands.map((command) => command.op).join(',') !== 'clip.set,track.set') {
  throw new Error('ordinary hold/label command sequence was not produced');
}
if (holdLabel.commands[0]?.args.values.hold !== 1.23456789 || holdLabel.commands[1]?.args.values.label !== 'ordinary-🎬') {
  throw new Error('ordinary hold/label values were not preserved');
}
if (moved.command.op !== 'clip.move' || moved.command.args.on !== move.on) {
  throw new Error('ordinary move command was not produced');
}

console.log(JSON.stringify({
  composition: { computeMediaTrim: typeof computeMediaTrim, trim },
  ordinary: {
    operations: holdLabel.commands.map((command) => command.op),
    hold: holdLabel.commands[0]?.args.values.hold,
    label: holdLabel.commands[1]?.args.values.label,
    move: { op: moved.command.op, on: moved.command.args.on },
  },
}));
