import { getAudioFade, getAudioVolumeProp } from '../../../src/tools/video-editor/lib/audioFade';
import { monitorSamples, SAMPLE_RATE } from './player-audio-monitor';

export const PHASE_FPS = 30;
export const PHASE_GAIN_BOUND_DB = 0.5;
export const PHASE_CLOCK_BOUND_SECONDS = 1 / PHASE_FPS;
const FRAME_SAMPLES = SAMPLE_RATE / PHASE_FPS;
const WINDOW_SAMPLES = 200;
const SOURCE_PEAK = 4096;
// monitorSamples floors seconds to samples. The interior of that sample's time
// interval avoids a floating-point round trip selecting its preceding sample.
const sampleTime = (sample: number) => (sample + 0.5) / SAMPLE_RATE;

// These tones identify source positions, independently of DOM currentTime.
// Each marker occupies the middle half of one existing authored fade frame.
export const PHASE_MARKERS = Array.from({ length: 6 }, (_, index) => ({
  frame: index + 3,
  frequency: 1200 + index * 240,
  firstSample: (index + 3) * FRAME_SAMPLES + FRAME_SAMPLES / 4,
  lastSample: (index + 3) * FRAME_SAMPLES + 3 * FRAME_SAMPLES / 4,
}));

export function phaseClip(backend: 'native' | 'amplified') {
  return {
    id: backend, clipType: 'media' as const, track: backend, asset: backend,
    at: 0, from: 0, to: 3, speed: 1,
    volume: backend === 'amplified' ? 2 : 1,
    params: { fadeIn: 0.6, fadeOut: 0.6 },
  };
}

// Read the App's public implementation; the diagnostic owns no fade evaluator.
export function phaseGainTable(backend: 'native' | 'amplified') {
  const clip = phaseClip(backend);
  const volume = getAudioVolumeProp(clip.volume, getAudioFade(clip, PHASE_FPS));
  if (typeof volume !== 'function') throw new Error('Expected authored fade');
  return Array.from({ length: 90 }, (_, frame) => volume(frame));
}

export function phaseSourcePcm() {
  const pcm = new Int16Array(3 * SAMPLE_RATE * 2);
  for (let sample = 0; sample < pcm.length / 2; sample++) {
    const marker = PHASE_MARKERS.find(item => sample >= item.firstSample && sample < item.lastSample);
    const value = SOURCE_PEAK * Math.sin(2 * Math.PI * (marker?.frequency ?? 660) * sample / SAMPLE_RATE);
    pcm[sample * 2] = Math.round(value);
    pcm[sample * 2 + 1] = Math.round(value * 0.75);
  }
  return pcm;
}

export function phaseSourceWav(pcm = phaseSourcePcm()) {
  if (pcm.length !== 3 * SAMPLE_RATE * 2) throw new Error('Expected three-second stereo source');
  const wav = Buffer.alloc(44 + pcm.byteLength);
  wav.write('RIFF', 0);
  wav.writeUInt32LE(wav.length - 8, 4);
  wav.write('WAVEfmt ', 8);
  wav.writeUInt32LE(16, 16);
  wav.writeUInt16LE(1, 20);
  wav.writeUInt16LE(2, 22);
  wav.writeUInt32LE(SAMPLE_RATE, 24);
  wav.writeUInt32LE(SAMPLE_RATE * 4, 28);
  wav.writeUInt16LE(4, 32);
  wav.writeUInt16LE(16, 34);
  wav.write('data', 36);
  wav.writeUInt32LE(pcm.byteLength, 40);
  for (let index = 0; index < pcm.length; index++) wav.writeInt16LE(pcm[index], 44 + index * 2);
  return wav;
}

const differenceDb = (actual: number, reference: number) => 20 * Math.log10(actual / reference);

type PhaseChannel = {
  amplitude: number;
  sourceAmplitude: number;
  appliedGain: number;
  expectedGain: number;
  differenceDb: number;
  candidates: number[];
  phaseSeconds: number | null;
};

/** Fixed raw capture windows: no lag search, fitting, resampling or PCM edits. */
export function measurePhysicalPhase(
  pcm: Int16Array,
  sourcePcm: Int16Array,
  gains: readonly number[],
  globalOnsetSeconds: number,
) {
  if (pcm.length !== 6 * SAMPLE_RATE * 2 || sourcePcm.length !== 3 * SAMPLE_RATE * 2
    || gains.length !== 90 || gains.some(gain => !Number.isFinite(gain) || gain < 0)
    || !Number.isFinite(globalOnsetSeconds) || globalOnsetSeconds < 0 || globalOnsetSeconds > 2) {
    throw new Error('Expected raw 6s capture, 3s source, 90 frame gains and one global onset');
  }
  const capture = monitorSamples(pcm);
  const source = monitorSamples(sourcePcm);
  const windows: Array<{
    firstSample: number;
    purity: number;
    markerFrame: number | null;
    channels: PhaseChannel[];
  }> = [];
  for (let first = 0; first + WINDOW_SAMPLES <= pcm.length / 2; first += WINDOW_SAMPLES) {
    const start = sampleTime(first);
    const end = sampleTime(first + WINDOW_SAMPLES);
    const rms = capture.rms(start, end);
    const bands = PHASE_MARKERS.map(marker => ({ marker, ...capture.spectrum(marker.frequency, start, end) }));
    const strongest = bands.reduce((best, band) => band.amplitude > best.amplitude ? band : best);
    const purity = rms > 0 ? strongest.amplitude ** 2 / (2 * rms ** 2) : 0;
    // Boundary windows are retained, but only near-pure marker windows infer a
    // frame. A real slew/mixed frame can be inconclusive, never rounded to pass.
    const marker = purity > 0.99 && strongest.amplitude > 0.004 ? strongest.marker : null;
    const channels = marker ? [0, 1].map(channel => {
      const amplitude = capture.spectrum(marker.frequency, start, end, channel).amplitude;
      const sourceAmplitude = source.spectrum(marker.frequency,
        sampleTime(marker.firstSample), sampleTime(marker.lastSample), channel).amplitude;
      const candidates = gains.slice(0, 19).flatMap((gain, frame) => (
        gain > 0 && Math.abs(differenceDb(amplitude, sourceAmplitude * gain)) <= PHASE_GAIN_BOUND_DB ? [frame] : []
      ));
      return {
        amplitude, sourceAmplitude, appliedGain: amplitude / sourceAmplitude,
        expectedGain: gains[marker.frame],
        differenceDb: differenceDb(amplitude, sourceAmplitude * gains[marker.frame]),
        candidates,
        phaseSeconds: candidates.length === 1 ? (candidates[0] - marker.frame) / PHASE_FPS : null,
      };
    }) : [];
    windows.push({ firstSample: first, purity, markerFrame: marker?.frame ?? null, channels });
  }
  const markers = PHASE_MARKERS.map(marker => {
    const found = windows.filter(window => window.markerFrame === marker.frame);
    const consecutive = found.every((window, index) => index === 0
      || window.firstSample === found[index - 1].firstSample + WINDOW_SAMPLES);
    return {
      ...marker, windows: found.length, consecutive,
      firstCaptureSample: found[0]?.firstSample ?? null,
      lastCaptureSample: found.at(-1)?.firstSample ?? null,
    };
  });
  // Absolute plateau calibration is checked, never divided out of the markers.
  const plateau = [0, 1].map(channel => differenceDb(
    capture.spectrum(660, globalOnsetSeconds + 1, globalOnsetSeconds + 2, channel).amplitude,
    source.spectrum(660, 1, 2, channel).amplitude * gains[30],
  ));
  const qualified = plateau.every(db => Number.isFinite(db) && Math.abs(db) <= PHASE_GAIN_BOUND_DB)
    && markers.every((marker, index) => marker.windows >= 2 && marker.windows <= 4 && marker.consecutive
      && (index === 0 || marker.firstCaptureSample! > markers[index - 1].lastCaptureSample!))
    && windows.filter(window => window.markerFrame !== null)
      .every(window => window.channels.every(channel => channel.candidates.length === 1));
  const compatible = qualified && windows.filter(window => window.markerFrame !== null)
    .every(window => window.channels.every(channel => Math.abs(channel.differenceDb) <= PHASE_GAIN_BOUND_DB
      && channel.phaseSeconds !== null && Math.abs(channel.phaseSeconds) < PHASE_CLOCK_BOUND_SECONDS));
  return {
    verdict: !qualified ? 'inconclusive' : compatible ? 'compatible' : 'phase-mismatch',
    globalOnsetSeconds, plateauDifferenceDb: plateau, markers, windows,
  };
}
