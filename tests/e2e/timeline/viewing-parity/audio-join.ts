import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { requireUnchangedGain } from '../player-audio-comparator';

const exec = promisify(execFile);
export const AUDIO_SAMPLE_RATE = 48_000;
const AUDIO_BLOCK_SECONDS = 0.02;
const AUDIO_ACTIVITY_RMS = 0.004;
const AUDIO_COMPARE_SECONDS = 0.1;

export type NativeAudioProbe = {
  streams: Array<Record<string, unknown>>;
  packets: Array<Record<string, unknown>>;
  format: Record<string, unknown>;
};

export type DecodedNativeAudio = {
  path: string;
  probe: NativeAudioProbe;
  pcm: Int16Array;
  sampleCount: number;
};

async function decodePcm(path: string, streamIndex: number): Promise<Buffer> {
  const { stdout } = await exec('ffmpeg', [
    '-v', 'error', '-nostdin', '-i', path, '-map', `0:${streamIndex}`,
    '-f', 's16le', 'pipe:1',
  ], { encoding: 'buffer', maxBuffer: 64 * 1024 * 1024 });
  return stdout;
}

export async function decodeNativeAudio(path: string, label: string): Promise<DecodedNativeAudio> {
  const { stdout } = await exec('ffprobe', [
    '-v', 'error', '-show_streams', '-show_packets', '-show_format', '-of', 'json', path,
  ], { maxBuffer: 8 * 1024 * 1024 });
  const probe = JSON.parse(stdout) as NativeAudioProbe;
  const audio = probe.streams.filter(stream => stream.codec_type === 'audio');
  if (audio.length !== 1) throw new Error(`${label} must contain exactly one audio stream`);
  const stream = audio[0];
  if (stream.sample_rate !== String(AUDIO_SAMPLE_RATE) || stream.channels !== 2) {
    throw new Error(`${label} must be native ${AUDIO_SAMPLE_RATE}Hz stereo; got ${stream.sample_rate}Hz/${stream.channels}ch`);
  }
  if (typeof stream.index !== 'number') throw new Error(`${label} audio stream has no index`);
  const raw = await decodePcm(path, stream.index);
  if (raw.length === 0 || raw.length % 4 !== 0) {
    throw new Error(`${label} decoded PCM must contain complete stereo int16 sample frames`);
  }
  const pcm = new Int16Array(raw.buffer, raw.byteOffset, raw.length / 2);
  return { path, probe, pcm, sampleCount: raw.length / 4 };
}

function rms(pcm: Int16Array, start: number, end: number, channel: number): number {
  const first = Math.max(0, Math.floor(start * AUDIO_SAMPLE_RATE));
  const last = Math.min(pcm.length / 2, Math.floor(end * AUDIO_SAMPLE_RATE));
  if (last <= first) throw new Error(`audio comparison window is outside decoded PCM: ${start}-${end}s`);
  let sum = 0;
  for (let sample = first; sample < last; sample++) sum += (pcm[sample * 2 + channel] / 32768) ** 2;
  return Math.sqrt(sum / (last - first));
}

function audibleOnset(pcm: Int16Array): number {
  const blocks = Math.floor((pcm.length / 2) / (AUDIO_SAMPLE_RATE * AUDIO_BLOCK_SECONDS));
  for (let block = 0; block < blocks; block++) {
    const start = block * AUDIO_BLOCK_SECONDS;
    if (rms(pcm, start, start + AUDIO_BLOCK_SECONDS, 0) > AUDIO_ACTIVITY_RMS) return start;
  }
  throw new Error('audio comparison input is silent');
}

export type AudioJoinResult = {
  sharedOffsetSeconds: number;
  captureWindow: { start: number; end: number };
  exportWindow: { start: number; end: number };
  channels: Array<{ captureRms: number; exportRms: number; gainDifferenceDb: number }>;
};

/**
 * Compare the same mixed Player output against the same normal MP4 export.
 * Onset is used once to establish one stream-wide capture offset; no clip or
 * channel is independently shifted, resampled, padded, or filtered.
 */
export function compareNativeAudio(capture: Pick<DecodedNativeAudio, 'pcm'>,
  exported: Pick<DecodedNativeAudio, 'pcm'>): AudioJoinResult {
  const captureOnset = audibleOnset(capture.pcm);
  const exportOnset = audibleOnset(exported.pcm);
  const sharedOffsetSeconds = captureOnset - exportOnset;
  const captureWindow = { start: captureOnset + 0.2, end: captureOnset + 0.2 + AUDIO_COMPARE_SECONDS };
  const exportWindow = {
    start: captureWindow.start - sharedOffsetSeconds,
    end: captureWindow.end - sharedOffsetSeconds,
  };
  const channels = [0, 1].map(channel => {
    const captureRms = rms(capture.pcm, captureWindow.start, captureWindow.end, channel);
    const exportRms = rms(exported.pcm, exportWindow.start, exportWindow.end, channel);
    if (captureRms <= AUDIO_ACTIVITY_RMS || exportRms <= AUDIO_ACTIVITY_RMS) {
      throw new Error(`audio comparison window is below ${AUDIO_ACTIVITY_RMS} RMS on channel ${channel}`);
    }
    requireUnchangedGain(captureRms, exportRms);
    return { captureRms, exportRms, gainDifferenceDb: 20 * Math.log10(captureRms / exportRms) };
  });
  return { sharedOffsetSeconds, captureWindow, exportWindow, channels };
}
