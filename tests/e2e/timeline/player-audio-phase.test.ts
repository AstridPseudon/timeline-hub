import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { test } from 'node:test';
import { audibleEdges, monitorSamples, SAMPLE_RATE } from './player-audio-monitor';
import {
  measurePhysicalPhase, phaseClip, phaseGainTable, phaseSourcePcm, phaseSourceWav,
  PHASE_CLOCK_BOUND_SECONDS, PHASE_FPS, PHASE_GAIN_BOUND_DB, PHASE_MARKERS,
} from './player-audio-phase';

const source = phaseSourcePcm();
const hash = (pcm: Int16Array) => createHash('sha256').update(new Uint8Array(pcm.buffer, pcm.byteOffset, pcm.byteLength)).digest('hex');

// Deliberately independent synthetic oracle, never used by the diagnostic.
const oracleGain = (frame: number, volume: number) => volume
  * Math.min(1, Math.max(0, frame / 18))
  * Math.min(1, Math.max(0, (90 - frame) / 18));

function syntheticCapture(volume: number, gainOffsetFrames = 0, onsetSample = 19_373) {
  const pcm = new Int16Array(6 * SAMPLE_RATE * 2);
  for (let sample = 0; sample < source.length / 2; sample++) {
    const frame = Math.floor(sample / (SAMPLE_RATE / PHASE_FPS));
    const gain = oracleGain(frame + gainOffsetFrames, volume);
    for (let channel = 0; channel < 2; channel++) {
      pcm[(sample + onsetSample) * 2 + channel] = Math.round(source[sample * 2 + channel] * gain);
    }
  }
  return pcm;
}

function measure(pcm: Int16Array, backend: 'native' | 'amplified') {
  return measurePhysicalPhase(pcm, source, phaseGainTable(backend), audibleEdges(monitorSamples(pcm)).onset);
}

test('source is deterministic, unshifted 3s 48k stereo PCM16 with known marker positions', () => {
  assert.deepEqual(phaseSourcePcm(), source);
  const wav = phaseSourceWav(source);
  assert.equal(wav.length, 44 + 3 * 48_000 * 4);
  assert.equal(wav.toString('ascii', 0, 4), 'RIFF');
  assert.equal(wav.readUInt16LE(20), 1);
  assert.equal(wav.readUInt16LE(22), 2);
  assert.equal(wav.readUInt32LE(24), 48_000);
  assert.equal(wav.readUInt16LE(34), 16);
  for (let index = 0; index < source.length; index++) assert.equal(wav.readInt16LE(44 + index * 2), source[index]);
  assert.throws(() => phaseSourceWav(new Int16Array(2)), /three-second/);
  for (const marker of PHASE_MARKERS) {
    const raw = monitorSamples(source);
    const start = (marker.firstSample + 0.5) / SAMPLE_RATE;
    const end = (marker.lastSample + 0.5) / SAMPLE_RATE;
    // PCM16 rounding error is at most half a sample unit; the two-sided
    // spectral amplitude error is therefore bounded by one sample unit.
    assert.ok(Math.abs(raw.spectrum(marker.frequency, start, end).amplitude - 0.125) <= 1 / 32768);
    assert.ok(Math.abs(raw.spectrum(marker.frequency, start, end, 1).amplitude - 0.09375) <= 1 / 32768);
    assert.equal(Math.floor(marker.firstSample / 1600), marker.frame);
    assert.equal(Math.floor((marker.lastSample - 1) / 1600), marker.frame);
  }
});

test('fixture uses the actual supported authored fade and public App volume behavior', () => {
  for (const backend of ['native', 'amplified'] as const) {
    const clip = phaseClip(backend);
    assert.deepEqual(clip.params, { fadeIn: 0.6, fadeOut: 0.6 });
    assert.equal(clip.to, 3);
    assert.equal(clip.from, 0);
    assert.equal(clip.speed, 1);
    const table = phaseGainTable(backend);
    for (let frame = 0; frame < 90; frame++) {
      assert.equal(table[frame], oracleGain(frame, clip.volume));
    }
    // Adjacent candidate ranges under +/-0.5 dB do not overlap here.
    for (let frame = 2; frame <= 8; frame++) {
      assert.ok(20 * Math.log10(table[frame + 1] / table[frame]) > 2 * PHASE_GAIN_BOUND_DB);
    }
  }
  assert.equal(PHASE_GAIN_BOUND_DB, 0.5);
  assert.equal(PHASE_CLOCK_BOUND_SECONDS, 1 / 30);
});

for (const backend of ['native', 'amplified'] as const) {
  test(`${backend}: known-good physical PCM passes without source/capture changes or onset fitting`, () => {
    const sourceBefore = hash(source);
    for (const onset of [19_200, 19_373]) {
      const pcm = syntheticCapture(phaseClip(backend).volume, 0, onset);
      const before = hash(pcm);
      const result = measure(pcm, backend);
      assert.equal(result.verdict, 'compatible');
      for (const marker of result.markers) {
        assert.ok(marker.firstCaptureSample! >= onset + marker.firstSample);
        assert.ok(marker.lastCaptureSample! + 200 <= onset + marker.lastSample);
      }
      for (const window of result.windows.filter(item => item.markerFrame !== null)) {
        for (const channel of window.channels) {
          assert.deepEqual(channel.candidates, [window.markerFrame]);
          assert.equal(channel.phaseSeconds, 0);
          assert.ok(Math.abs(channel.differenceDb) < 0.01);
        }
      }
      assert.equal(hash(pcm), before);
    }
    assert.equal(hash(source), sourceBefore);
  });

  for (const offset of [-2, -1, 1, 2]) {
    test(`${backend}: unshifted source with deliberate ${offset}-frame gain error is rejected`, () => {
      const pcm = syntheticCapture(phaseClip(backend).volume, offset);
      const before = hash(pcm);
      const result = measure(pcm, backend);
      assert.equal(result.verdict, 'phase-mismatch');
      for (const window of result.windows.filter(item => item.markerFrame !== null)) {
        for (const channel of window.channels) {
          assert.deepEqual(channel.candidates, [window.markerFrame! + offset]);
          assert.equal(channel.phaseSeconds, offset / 30);
          assert.ok(Math.abs(channel.differenceDb) > 0.5);
          assert.ok(Math.abs(channel.phaseSeconds!) >= PHASE_CLOCK_BOUND_SECONDS);
        }
      }
      assert.equal(hash(pcm), before);
    });
  }
}

test('device gain error, missing marker, silence and wrong marker order cannot pass', () => {
  const good = syntheticCapture(2);
  const halfVolume = good.map(value => Math.round(value / 2));
  assert.equal(measure(halfVolume, 'amplified').verdict, 'inconclusive');
  const missing = good.slice();
  const first = PHASE_MARKERS[0];
  missing.fill(0, (19_373 + first.firstSample) * 2, (19_373 + first.lastSample) * 2);
  assert.equal(measure(missing, 'amplified').verdict, 'inconclusive');
  assert.equal(measurePhysicalPhase(new Int16Array(good.length), source, phaseGainTable('amplified'), 0).verdict, 'inconclusive');
  const reversed = good.slice();
  for (const marker of PHASE_MARKERS) {
    const opposite = PHASE_MARKERS[PHASE_MARKERS.length - 1 - (marker.frame - 3)];
    reversed.set(good.subarray((19_373 + opposite.firstSample) * 2, (19_373 + opposite.lastSample) * 2),
      (19_373 + marker.firstSample) * 2);
  }
  assert.equal(measure(reversed, 'amplified').verdict, 'inconclusive');
});

test('sub-frame mixed gains remain unresolved rather than rounded to a compatible frame', () => {
  const pcm = syntheticCapture(2);
  const marker = PHASE_MARKERS.at(-1)!;
  for (let sample = marker.firstSample; sample < marker.lastSample; sample++) {
    for (let channel = 0; channel < 2; channel++) {
      pcm[(19_373 + sample) * 2 + channel] = Math.round(source[sample * 2 + channel] * oracleGain(Math.sqrt(8 * 9), 2));
    }
  }
  assert.equal(measure(pcm, 'amplified').verdict, 'inconclusive');
});

test('malformed raw PCM and non-finite inputs refuse measurement', () => {
  const good = syntheticCapture(2);
  for (const onset of [NaN, Infinity, -1, 3]) {
    assert.throws(() => measurePhysicalPhase(good, source, phaseGainTable('amplified'), onset), /Expected raw/);
  }
  assert.throws(() => measurePhysicalPhase(good.subarray(2), source, phaseGainTable('amplified'), 0.4), /Expected raw/);
  assert.throws(() => measurePhysicalPhase(good, source.subarray(2), phaseGainTable('amplified'), 0.4), /Expected raw/);
  assert.throws(() => measurePhysicalPhase(good, source, [], 0.4), /Expected raw/);
  assert.throws(() => measurePhysicalPhase(good, source, Array(90).fill(NaN), 0.4), /Expected raw/);
});
