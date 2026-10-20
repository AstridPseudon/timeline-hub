import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { monitorSamples, SAMPLE_RATE } from '../player-audio-monitor';
import { decodeExportAudio, type ExportAudioDecodeOptions, type ExportAudioReference } from './audio-reference';

const exec = promisify(execFile);

export type ExportAudioMonitor = {
  readonly status: 'supported';
  readonly reference: ExportAudioReference;
  readonly rawPcm: Buffer;
  readonly monitor: ReturnType<typeof monitorSamples>;
} | {
  readonly status: 'unsupported';
  readonly reference: ExportAudioReference;
  readonly reason: string;
};

export async function decodeExportAudioMonitor(options: ExportAudioDecodeOptions): Promise<ExportAudioMonitor> {
  const reference = await decodeExportAudio(options);
  const source = reference.source.audioStream;
  const output = reference.output.streams.find(stream => stream.codec_type === 'audio');
  if (source.sample_rate !== String(SAMPLE_RATE) || source.channels !== 2
    || output?.sample_rate !== String(SAMPLE_RATE) || output.channels !== 2
    || output.codec_name !== 'pcm_s16le' || output.sample_fmt !== 's16') {
    return {
      status: 'unsupported', reference,
      reason: `monitor requires native ${SAMPLE_RATE}Hz stereo and decoded pcm_s16le/s16; `
        + `source ${source.sample_rate}Hz/${source.channels}ch, `
        + `output ${output?.sample_rate}Hz/${output?.channels}ch/${output?.codec_name}/${output?.sample_fmt}`,
    };
  }
  const { stdout: rawPcm } = await exec(options.ffmpegPath ?? options.tools?.ffmpeg ?? 'ffmpeg', [
    '-v', 'error', '-nostdin', '-i', reference.outputWavPath,
    '-map', '0:a:0', '-f', 's16le', 'pipe:1',
  ], { encoding: 'buffer', maxBuffer: 64 * 1024 * 1024 });
  if (rawPcm.length === 0 || rawPcm.length % 4 !== 0) {
    return { status: 'unsupported', reference, reason: 'decoded PCM must contain complete stereo int16 sample frames' };
  }
  const pcm = new Int16Array(rawPcm.buffer, rawPcm.byteOffset, rawPcm.length / 2);
  return { status: 'supported', reference, rawPcm, monitor: monitorSamples(pcm) };
}
