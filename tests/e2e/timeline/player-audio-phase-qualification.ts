import { monitorSamples, SAMPLE_RATE } from './player-audio-monitor';
import { measurePhysicalPhase, PHASE_GAIN_BOUND_DB } from './player-audio-phase';

type Measurement = ReturnType<typeof measurePhysicalPhase>;

// Reuse the analyzer's amplitudes and the same monitor RMS. Identification on
// one channel alone must not hide a mixed/ambiguous marker on the other.
function channelPurity(pcm: Int16Array, measurement: Measurement) {
  const capture = monitorSamples(pcm);
  return measurement.windows.filter(window => window.markerFrame !== null).map(window => ({
    firstSample: window.firstSample,
    channels: window.channels.map((channel, index) => {
      const rms = capture.rms((window.firstSample + 0.5) / SAMPLE_RATE,
        (window.firstSample + 200 + 0.5) / SAMPLE_RATE, index);
      return rms > 0 ? channel.amplitude ** 2 / (2 * rms ** 2) : 0;
    }),
  }));
}

export function measureColdPhase(...args: Parameters<typeof measurePhysicalPhase>) {
  const measurement = measurePhysicalPhase(...args);
  const purity = channelPurity(args[0], measurement);
  const pure = purity.every(window => window.channels.every(value => value > 0.99));
  return { ...measurement, channelPurity: purity, verdict: pure ? measurement.verdict : 'inconclusive' as const };
}

// Reuse the marker analyzer's raw windows. Flat calibration has no gain-frame
// inference: all six frequencies must meet their fixed absolute source level.
export function measureFlatCalibration(pcm: Int16Array, source: Int16Array, onset: number) {
  const measurement = measurePhysicalPhase(pcm, source, Array(90).fill(2), onset);
  const complete = measurement.markers.every((marker, index, markers) =>
    marker.windows >= 2 && marker.windows <= 4 && marker.consecutive
    && (index === 0 || marker.firstCaptureSample! > markers[index - 1].lastCaptureSample!));
  const purity = channelPurity(pcm, measurement);
  const levels = measurement.windows.filter(window => window.markerFrame !== null);
  const valid = complete && purity.every(window => window.channels.every(value => value > 0.99)) && measurement.plateauDifferenceDb.every(db => Number.isFinite(db) && Math.abs(db) <= PHASE_GAIN_BOUND_DB)
    && levels.every(window => window.channels.every(channel =>
      Number.isFinite(channel.differenceDb) && Math.abs(channel.differenceDb) <= PHASE_GAIN_BOUND_DB));
  return { valid, measurement, channelPurity: purity };
}

export function qualifyPhysicalPhase(cold: Measurement, calibration?: ReturnType<typeof measureFlatCalibration>) {
  // A changing or channel-dependent inferred frame is a slewed/ambiguous marker,
  // even when each individual window happens to have one candidate.
  const stable = cold.markers.every(marker => {
    const candidates = cold.windows.filter(window => window.markerFrame === marker.frame)
      .flatMap(window => window.channels.map(channel => channel.candidates));
    return candidates.length > 0 && candidates.every(frames => frames.length === 1 && frames[0] === candidates[0][0]);
  });
  return !calibration?.valid || !stable ? 'inconclusive' : cold.verdict;
}
