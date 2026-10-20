import { execFile } from 'node:child_process';
import { createHash } from 'node:crypto';
import { lstat, mkdir, readFile, rename, rm, stat } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { promisify } from 'node:util';

const exec = promisify(execFile);
const MAX_PROBE_BYTES = 2 * 1024 * 1024;

export type AudioReferenceErrorKind =
  | 'invalid-artifact'
  | 'missing-tool'
  | 'probe-failed'
  | 'decode-failed'
  | 'output-conflict'
  | 'source-mutated';

export class AudioReferenceError extends Error {
  readonly kind: AudioReferenceErrorKind;

  constructor(kind: AudioReferenceErrorKind, message: string) {
    super(message);
    this.name = 'AudioReferenceError';
    this.kind = kind;
  }
}

export type MediaProbeStream = {
  readonly index?: number;
  readonly codec_type?: string;
  readonly codec_name?: string;
  readonly codec_long_name?: string;
  readonly codec_tag_string?: string;
  readonly sample_fmt?: string;
  readonly sample_rate?: string;
  readonly channels?: number;
  readonly channel_layout?: string;
  readonly time_base?: string;
  readonly start_pts?: number;
  readonly start_time?: string;
  readonly duration_ts?: number;
  readonly duration?: string;
  readonly nb_frames?: string;
  readonly nb_samples?: string;
  readonly initial_padding?: number;
  readonly trailing_padding?: number;
  readonly seek_preroll?: number;
  readonly codec_delay?: number;
  readonly [key: string]: unknown;
};

export type MediaProbePacket = Readonly<Record<string, unknown>>;

export type MediaProbe = {
  readonly streams: readonly MediaProbeStream[];
  readonly format: Readonly<Record<string, unknown>>;
  readonly packets: readonly MediaProbePacket[];
};

export type ExportAudioProbe = MediaProbe & {
  readonly audioStream: MediaProbeStream;
  readonly audioStreamIndex: number;
};

export type ExportAudioDecodeOptions = {
  /** The immutable MP4 downloaded by the normal App Render-button harness. */
  readonly artifactPath: string;
  /** A path owned by the current render attempt; it must not be the artifact. */
  readonly outputWavPath: string;
  readonly ffmpegPath?: string;
  readonly ffprobePath?: string;
  readonly tools?: { readonly ffmpeg?: string; readonly ffprobe?: string };
};

export type ExportAudioReference = {
  readonly artifactPath: string;
  readonly outputWavPath: string;
  readonly sourceSha256Before: string;
  readonly sourceSha256After: string;
  readonly sourceBytes: number;
  readonly source: ExportAudioProbe;
  readonly output: MediaProbe;
  readonly conversion: {
    readonly container: 'wav';
    readonly codec: 'pcm_s16le';
    readonly filters: readonly [];
    readonly resampled: false;
    readonly channelMapping: false;
    readonly timingEdits: readonly [];
  };
};

/**
 * Gate-6 handoff: the later parity case supplies Player capture PCM and this
 * decoded WAV from the same admitted Render-button MP4/authority tuple to the
 * existing player-audio-analyze comparator. Its sample clock remains the
 * analyzer's 48 kHz PCM clock; source PTS, duration and AAC delay fields below
 * are evidence, never alignment inputs. Full native+amplified+video mix,
 * Player volume 0.5/mute, and the planted capture-gain mismatch belong after a
 * stable baseline and must use the same downloaded artifact.
 */
export const AUDIO_PARITY_HANDOFF = {
  referenceInput: 'decoded WAV from the exact downloaded App Render-button MP4',
  playerInput: 'real Player capture WAV',
  sampleClock: 'existing player-audio-analyze 48_000 Hz PCM clock',
  comparator: 'existing player-audio-analyze comparator; no comparator here',
  controls: ['native+amplified+video mix', 'Player volume/mute 0.5', 'planted capture-gain mismatch'],
  alignment: 'none: retain onset, duration, PTS and codec-delay evidence',
} as const;

type ToolName = 'ffmpeg' | 'ffprobe';

function toolPath(options: Pick<ExportAudioDecodeOptions, 'ffmpegPath' | 'ffprobePath' | 'tools'>, tool: ToolName) {
  return tool === 'ffmpeg'
    ? options.ffmpegPath ?? options.tools?.ffmpeg ?? 'ffmpeg'
    : options.ffprobePath ?? options.tools?.ffprobe ?? 'ffprobe';
}

function errorMessage(error: unknown): string {
  return error instanceof Error ? error.message : String(error);
}

async function runTool(tool: ToolName, command: string, args: readonly string[], kind: 'probe' | 'decode') {
  try {
    const result = await exec(command, [...args], { encoding: 'utf8', maxBuffer: MAX_PROBE_BYTES });
    return result.stdout;
  } catch (error) {
    const code = (error as NodeJS.ErrnoException).code;
    if (code === 'ENOENT') {
      throw new AudioReferenceError('missing-tool', `missing ${tool} tool: ${command}`);
    }
    const detail = errorMessage(error).replace(/\s+/g, ' ').trim();
    throw new AudioReferenceError(kind === 'probe' ? 'probe-failed' : 'decode-failed',
      `${tool} ${kind} failed: ${detail}`);
  }
}

async function hashFile(path: string): Promise<string> {
  const bytes = await readFile(path);
  return `sha256:${createHash('sha256').update(bytes).digest('hex')}`;
}

async function readProbe(path: string, ffprobePath: string): Promise<MediaProbe> {
  const stdout = await runTool('ffprobe', ffprobePath, [
    '-v', 'error', '-show_streams', '-show_format', '-show_packets',
    '-read_intervals', '%+#1', '-of', 'json', path,
  ], 'probe');
  try {
    const parsed = JSON.parse(stdout) as {
      streams?: MediaProbeStream[];
      format?: Record<string, unknown>;
      packets?: MediaProbePacket[];
    };
    if (!Array.isArray(parsed.streams) || !parsed.format || typeof parsed.format !== 'object') {
      throw new Error('probe JSON has no streams/format');
    }
    return { streams: parsed.streams, format: parsed.format, packets: parsed.packets ?? [] };
  } catch (error) {
    throw new AudioReferenceError('probe-failed', `ffprobe returned invalid JSON for ${path}: ${errorMessage(error)}`);
  }
}

function audioProbe(path: string, probe: MediaProbe): ExportAudioProbe {
  const audioStream = probe.streams.find(stream => stream.codec_type === 'audio'
    && typeof stream.index === 'number');
  const audioStreamIndex = audioStream?.index;
  if (!audioStream || typeof audioStreamIndex !== 'number') {
    throw new AudioReferenceError('invalid-artifact', `artifact has no addressable audio stream: ${path}`);
  }
  return { ...probe, audioStream, audioStreamIndex };
}

async function assertRegularFile(path: string, label: string): Promise<number> {
  try {
    const entry = await lstat(path);
    if (!entry.isFile() || entry.isSymbolicLink()) throw new Error('not a regular file');
    return entry.size;
  } catch (error) {
    throw new AudioReferenceError('invalid-artifact', `${label} is unavailable: ${path} (${errorMessage(error)})`);
  }
}

export async function probeExportArtifact(options: {
  readonly artifactPath: string;
  readonly ffprobePath?: string;
  readonly tools?: { readonly ffprobe?: string };
}): Promise<ExportAudioProbe> {
  const artifactPath = resolve(options.artifactPath);
  await assertRegularFile(artifactPath, 'export artifact');
  const ffprobePath = options.ffprobePath ?? options.tools?.ffprobe ?? 'ffprobe';
  let probe: MediaProbe;
  try {
    probe = await readProbe(artifactPath, ffprobePath);
  } catch (error) {
    if (error instanceof AudioReferenceError && error.kind === 'probe-failed') {
      throw new AudioReferenceError('invalid-artifact', `invalid export artifact: ${artifactPath} (${error.message})`);
    }
    throw error;
  }
  return audioProbe(artifactPath, probe);
}

export async function decodeExportAudio(options: ExportAudioDecodeOptions): Promise<ExportAudioReference> {
  const artifactPath = resolve(options.artifactPath);
  const outputWavPath = resolve(options.outputWavPath);
  if (artifactPath === outputWavPath) {
    throw new AudioReferenceError('output-conflict', 'decoded WAV path must differ from the source artifact');
  }
  const sourceBytes = await assertRegularFile(artifactPath, 'export artifact');
  try {
    if ((await lstat(outputWavPath)).isSymbolicLink()) {
      throw new AudioReferenceError('output-conflict', `decoded WAV path is a symbolic link: ${outputWavPath}`);
    }
    throw new AudioReferenceError('output-conflict', `decoded WAV path already exists: ${outputWavPath}`);
  } catch (error) {
    if (error instanceof AudioReferenceError) throw error;
    if ((error as NodeJS.ErrnoException).code !== 'ENOENT') {
      throw new AudioReferenceError('output-conflict', `cannot inspect decoded WAV path: ${outputWavPath}`);
    }
  }

  const ffprobePath = toolPath(options, 'ffprobe');
  const ffmpegPath = toolPath(options, 'ffmpeg');
  const sourceSha256Before = await hashFile(artifactPath);
  let sourceProbe: MediaProbe;
  try {
    sourceProbe = await readProbe(artifactPath, ffprobePath);
  } catch (error) {
    if (error instanceof AudioReferenceError && error.kind === 'probe-failed') {
      throw new AudioReferenceError('invalid-artifact', `invalid export artifact: ${artifactPath} (${error.message})`);
    }
    throw error;
  }
  const source = audioProbe(artifactPath, sourceProbe);
  await mkdir(dirname(outputWavPath), { recursive: true });
  const temporaryWavPath = `${outputWavPath}.part-${process.pid}-${Date.now()}`;
  try {
    await runTool('ffmpeg', ffmpegPath, [
      '-hide_banner', '-v', 'error', '-nostdin', '-y',
      '-i', artifactPath,
      '-map', `0:${source.audioStreamIndex}`, '-vn',
      '-c:a', 'pcm_s16le', '-f', 'wav', temporaryWavPath,
    ], 'decode');
    await stat(temporaryWavPath);
    await rename(temporaryWavPath, outputWavPath);
  } catch (error) {
    await rm(temporaryWavPath, { force: true });
    throw error;
  }

  const sourceSha256After = await hashFile(artifactPath);
  if (sourceSha256After !== sourceSha256Before) {
    await rm(outputWavPath, { force: true });
    throw new AudioReferenceError('source-mutated', `export artifact changed while decoding: ${artifactPath}`);
  }
  const output = await readProbe(outputWavPath, ffprobePath);
  const outputAudio = output.streams.find(stream => stream.codec_type === 'audio');
  if (!outputAudio || outputAudio.codec_name !== 'pcm_s16le') {
    throw new AudioReferenceError('decode-failed', `decoded output is not pcm_s16le WAV: ${outputWavPath}`);
  }
  if (outputAudio.channels !== source.audioStream.channels
    || outputAudio.sample_rate !== source.audioStream.sample_rate) {
    throw new AudioReferenceError('decode-failed',
      `decoded output changed channel/sample-rate shape: source ${source.audioStream.channels}ch/${source.audioStream.sample_rate}Hz, `
      + `output ${outputAudio.channels}ch/${outputAudio.sample_rate}Hz`);
  }
  return {
    artifactPath, outputWavPath, sourceSha256Before, sourceSha256After, sourceBytes, source, output,
    conversion: {
      container: 'wav', codec: 'pcm_s16le', filters: [], resampled: false, channelMapping: false, timingEdits: [],
    },
  };
}
