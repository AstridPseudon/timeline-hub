import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFileSync} from 'node:fs';
import {applyAudioEnvelope, audioEnvelopeWav, compileAudioEnvelope} from '@banodoco/timeline-composition/evaluation';
import {prepareNormalAudioSources} from './normal-audio-sources.mjs';
import {compiledAudioSourceClock} from './compiled-audio-source-clock.mjs';

const input = JSON.parse(readFileSync(0, 'utf8'));
const {clip, rawChild, path, fps, prepared} = input;
const clock = compiledAudioSourceClock(clip, fps);
const envelope = compileAudioEnvelope(clip, fps);
const reference = source => {
  const channels = [new Float32Array(90000).fill(0.25), new Float32Array(90000).fill(-0.125)];
  const origin = compiledAudioSourceClock(source, fps);
  applyAudioEnvelope(channels, 30000, compileAudioEnvelope(source, fps), origin.source_from, origin.playback_rate);
  return Buffer.from(audioEnvelopeWav(channels, 30000));
};
const bytes = readFileSync(path), expected = reference(clip), rawBytes = reference(rawChild);
assert.deepEqual(bytes, expected);
assert.deepEqual(JSON.parse(prepared.envelope_key), envelope);
assert.equal(prepared.source_from, clock.source_from);
assert.equal(prepared.playback_rate, clock.playback_rate);
assert.notDeepEqual(bytes, rawBytes); // The real projector clipped the occurrence's end.
let maxRawDifference = 0;
for (let p = 44; p < bytes.length; p += 4) {
  maxRawDifference = Math.max(maxRawDifference, Math.abs(bytes.readFloatLE(p) - rawBytes.readFloatLE(p)));
}
const [part, restarted] = prepareNormalAudioSources({fps, attemptDirectory: input.sliceDirectory, clips: [
  {clip: input.sliced, originalClip: clip, source: input.source},
  {clip: input.sliced, source: input.source},
]});
const partBytes = readFileSync(part.path), restartBytes = readFileSync(restarted.path);
let maxSliceDifference = 0, maxRestartDifference = 0;
for (let p = 44; p < bytes.length; p += 4) {
  maxSliceDifference = Math.max(maxSliceDifference, Math.abs(bytes.readFloatLE(p) - partBytes.readFloatLE(p)));
  maxRestartDifference = Math.max(maxRestartDifference, Math.abs(bytes.readFloatLE(p) - restartBytes.readFloatLE(p)));
}
assert.ok(maxSliceDifference <= 1e-7);
assert.ok(maxRestartDifference > 0.1);
const hash = buffer => createHash('sha256').update(buffer).digest('hex');
console.log(JSON.stringify({clock, at: clip.at, to: clip.to, envelope, sliceClock: compiledAudioSourceClock(input.sliced, fps),
  maxSliceDifference, maxRestartDifference,
  wavBytes: bytes.length, wavSha256: hash(bytes), rawWavSha256: hash(rawBytes), maxRawDifference,
  samples: [0, 2002, 5000, 10000, 30000, 50000, 70000].map(sample =>
    [sample, bytes.readFloatLE(44 + sample * 8), bytes.readFloatLE(48 + sample * 8)])}));
