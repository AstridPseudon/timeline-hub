import assert from 'node:assert/strict';
import { test } from 'node:test';
import { audibleEdges, monitorSamples } from './player-audio-monitor';
import { phaseGainTable, phaseSourcePcm, PHASE_MARKERS } from './player-audio-phase';
import { measureColdPhase, measureFlatCalibration, qualifyPhysicalPhase } from './player-audio-phase-qualification';

const source = phaseSourcePcm();
const onset = 19_373;
function capture(gains: number[], offset = 0) {
  const pcm = new Int16Array(6 * 48_000 * 2);
  for (let sample = 0; sample < source.length / 2; sample++) {
    const gain = gains[Math.max(0, Math.min(89, Math.floor(sample / 1600) + offset))];
    for (let channel = 0; channel < 2; channel++) pcm[(onset + sample) * 2 + channel] = Math.round(source[sample * 2 + channel] * gain);
  }
  return pcm;
}
const measure = (pcm: Int16Array) => measureColdPhase(pcm, source, phaseGainTable('amplified'), audibleEdges(monitorSamples(pcm)).onset);
const flat = (pcm = capture(Array(90).fill(2))) => measureFlatCalibration(pcm, source, audibleEdges(monitorSamples(pcm)).onset);

test('flat calibration checks every marker and channel at absolute x2 with the unchanged plateau bound', () => {
  const calibration = flat();
  assert.equal(calibration.valid, true);
  assert.equal(qualifyPhysicalPhase(measure(capture(phaseGainTable('amplified'))), calibration), 'compatible');
  for (const marker of PHASE_MARKERS) {
    for (const channel of [0, 1]) {
      const pcm = capture(Array(90).fill(2));
      for (let sample = marker.firstSample; sample < marker.lastSample; sample++) pcm[(onset + sample) * 2 + channel] = Math.round(pcm[(onset + sample) * 2 + channel] * 0.9);
      const result = flat(pcm);
      assert.equal(result.valid, false, `${marker.frequency}Hz channel ${channel}`);
      assert.equal(qualifyPhysicalPhase(measure(capture(phaseGainTable('amplified'))), result), 'inconclusive');
    }
  }
});

test('bad plateau, absent calibration, missing or reordered markers cannot attribute phase', () => {
  const cold = measure(capture(phaseGainTable('amplified')));
  assert.equal(qualifyPhysicalPhase(cold), 'inconclusive');
  const gainError = capture(Array(90).fill(1.8));
  assert.equal(flat(gainError).valid, false);
  const missing = capture(Array(90).fill(2));
  missing.fill(0, (onset + PHASE_MARKERS[0].firstSample) * 2, (onset + PHASE_MARKERS[0].lastSample) * 2);
  assert.equal(flat(missing).valid, false);
  const reversed = capture(Array(90).fill(2));
  const original = reversed.slice();
  PHASE_MARKERS.forEach((marker, index) => {
    const other = PHASE_MARKERS[5 - index];
    reversed.set(original.subarray((onset + other.firstSample) * 2, (onset + other.lastSample) * 2), (onset + marker.firstSample) * 2);
  });
  assert.equal(flat(reversed).valid, false);
});

test('qualified flat calibration never divides out or forgives +/-1 and +/-2 frame errors', () => {
  for (const offset of [-2, -1, 1, 2]) assert.equal(qualifyPhysicalPhase(measure(capture(phaseGainTable('amplified'), offset)), flat()), 'phase-mismatch');
});

test('slewed or channel-dependent candidate frames remain inconclusive', () => {
  const cold = measure(capture(phaseGainTable('amplified')));
  const changed = structuredClone(cold);
  const windows = changed.windows.filter(window => window.markerFrame === 3);
  windows[1].channels[0].candidates = [4];
  assert.equal(qualifyPhysicalPhase(changed, flat()), 'inconclusive');
  assert.equal(qualifyPhysicalPhase(measure(capture(phaseGainTable('amplified'), 40)), flat()), 'inconclusive');
});

test('right-channel mixed tones are inconclusive even when marker amplitude is correct', () => {
  for (const faded of [false, true]) {
    const pcm = capture(faded ? phaseGainTable('amplified') : Array(90).fill(2));
    const marker = PHASE_MARKERS[0];
    for (let sample = marker.firstSample; sample < marker.lastSample; sample++) {
      pcm[(onset + sample) * 2 + 1] += Math.round(2000 * Math.sin(2 * Math.PI * PHASE_MARKERS[1].frequency * sample / 48_000));
    }
    if (faded) {
      const result = measure(pcm);
      assert.equal(result.verdict, 'inconclusive');
      assert.equal(qualifyPhysicalPhase(result, flat()), 'inconclusive');
    } else assert.equal(flat(pcm).valid, false);
  }
});
