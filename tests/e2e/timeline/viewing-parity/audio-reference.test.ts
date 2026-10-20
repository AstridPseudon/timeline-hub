import assert from 'node:assert/strict';
import { execFile } from 'node:child_process';
import { createHash } from 'node:crypto';
import { mkdtemp, readFile, rm, stat, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { test } from 'node:test';
import { promisify } from 'node:util';
import { AUDIO_PARITY_HANDOFF, AudioReferenceError, decodeExportAudio, probeExportArtifact } from './audio-reference';

const exec = promisify(execFile);

async function ffmpeg(args: readonly string[]) {
  await exec('ffmpeg', ['-v', 'error', '-y', ...args], { maxBuffer: 2 * 1024 * 1024 });
}

async function makeAudioMp4(path: string, codec: 'aac' | 'pcm_s16le' = 'aac', volume?: number) {
  await ffmpeg([
    '-f', 'lavfi', '-i', 'sine=frequency=440:sample_rate=48000:duration=0.4',
    ...(volume ? ['-filter:a', `volume=${volume}`] : []),
    '-ac', '2', '-c:a', codec, ...(codec === 'aac' ? ['-b:a', '128k'] : []),
    '-movflags', '+faststart', path,
  ]);
}

async function makeVideoOnlyMp4(path: string) {
  await ffmpeg([
    '-f', 'lavfi', '-i', 'color=size=16x16:rate=1:duration=0.2', '-an', '-c:v', 'mpeg4', path,
  ]);
}

async function decodeRaw(path: string): Promise<Buffer> {
  const { stdout } = await exec('ffmpeg', [
    '-v', 'error', '-nostdin', '-i', path, '-map', '0:a:0', '-vn', '-f', 's16le', 'pipe:1',
  ], { encoding: 'buffer', maxBuffer: 4 * 1024 * 1024 });
  return stdout;
}

async function withDirectory<T>(callback: (directory: string) => Promise<T>): Promise<T> {
  const directory = await mkdtemp(join(tmpdir(), 'export-audio-reference-'));
  try {
    return await callback(directory);
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
}

function sha256(bytes: Uint8Array) {
  return `sha256:${createHash('sha256').update(bytes).digest('hex')}`;
}

test('decodes the actual AAC stream from one artifact into an attempt-owned WAV', async () => {
  await withDirectory(async directory => {
    const artifactPath = join(directory, 'render-button-download.mp4');
    const outputWavPath = join(directory, 'attempt-001', 'export-audio.wav');
    await makeAudioMp4(artifactPath);
    const sourceBefore = await readFile(artifactPath);

    const reference = await decodeExportAudio({ artifactPath, outputWavPath });
    const outputStat = await stat(outputWavPath);
    const outputPcm = await decodeRaw(outputWavPath);
    const sourceAudio = reference.source.audioStream;
    const outputAudio = reference.output.streams.find(stream => stream.codec_type === 'audio');

    assert.equal(sourceAudio.codec_name, 'aac');
    assert.equal(reference.source.audioStreamIndex, sourceAudio.index);
    assert.ok(reference.source.streams.some(stream => stream.index === sourceAudio.index));
    assert.ok(sourceAudio.time_base);
    assert.ok(sourceAudio.start_time !== undefined || sourceAudio.start_pts !== undefined);
    assert.ok(sourceAudio.duration !== undefined || sourceAudio.duration_ts !== undefined);
    assert.ok(reference.source.packets.length > 0);
    assert.ok(['codec_delay', 'initial_padding', 'seek_preroll', 'trailing_padding']
      .some(field => field in sourceAudio || reference.source.packets.some(packet => field in packet)));
    assert.equal(outputAudio?.codec_name, 'pcm_s16le');
    assert.equal(outputAudio?.channels, sourceAudio.channels);
    assert.equal(outputAudio?.sample_rate, sourceAudio.sample_rate);
    assert.ok(Number(reference.output.format.duration) > 0);
    assert.ok(outputStat.size > 44);
    assert.ok(outputPcm.length > 0);
    assert.equal(outputPcm.length % ((sourceAudio.channels ?? 0) * 2), 0);
    assert.ok(outputPcm.some(value => value !== 0));
    assert.equal(reference.conversion.codec, 'pcm_s16le');
    assert.deepEqual(reference.conversion.filters, []);
    assert.equal(reference.conversion.resampled, false);
    assert.equal(reference.conversion.channelMapping, false);
    assert.deepEqual(reference.conversion.timingEdits, []);
    assert.equal(reference.sourceSha256Before, sha256(sourceBefore));
    assert.equal(reference.sourceSha256After, reference.sourceSha256Before);
    assert.deepEqual(await readFile(artifactPath), sourceBefore);
    console.log('EXPORT_AUDIO_REFERENCE', JSON.stringify({
      source: reference.source.audioStream,
      output: outputAudio,
      hashes: [reference.sourceSha256Before, reference.sourceSha256After],
    }));
  });
});

test('PCM MP4 conversion preserves decoded channel data and gain without a filter', async () => {
  await withDirectory(async directory => {
    const artifactPath = join(directory, 'known-gain.mp4');
    const outputWavPath = join(directory, 'attempt', 'known-gain.wav');
    await makeAudioMp4(artifactPath, 'pcm_s16le', 0.25);

    const reference = await decodeExportAudio({ artifactPath, outputWavPath });
    const expectedPcm = await decodeRaw(artifactPath);
    const actualPcm = await decodeRaw(outputWavPath);

    assert.equal(reference.source.audioStream.codec_name, 'pcm_s16le');
    assert.ok(expectedPcm.length > 0);
    assert.deepEqual(actualPcm, expectedPcm);
    assert.equal(reference.sourceSha256Before, reference.sourceSha256After);
  });
});

test('rejects an MP4 with no audio stream as an invalid artifact', async () => {
  await withDirectory(async directory => {
    const artifactPath = join(directory, 'video-only.mp4');
    await makeVideoOnlyMp4(artifactPath);
    await assert.rejects(
      decodeExportAudio({ artifactPath, outputWavPath: join(directory, 'audio.wav') }),
      (error: unknown) => error instanceof AudioReferenceError
        && error.kind === 'invalid-artifact'
        && /no addressable audio stream/.test(error.message),
    );
  });
});

test('rejects invalid media clearly before attempting a decode', async () => {
  await withDirectory(async directory => {
    const artifactPath = join(directory, 'not-an-export.mp4');
    await writeFile(artifactPath, 'not an MP4');
    await assert.rejects(
      probeExportArtifact({ artifactPath }),
      (error: unknown) => error instanceof AudioReferenceError
        && error.kind === 'invalid-artifact'
        && /invalid export artifact/.test(error.message),
    );
  });
});

test('reports missing ffprobe and ffmpeg tools distinctly', async () => {
  await withDirectory(async directory => {
    const artifactPath = join(directory, 'tool-check.mp4');
    await makeAudioMp4(artifactPath);
    await assert.rejects(
      probeExportArtifact({ artifactPath, ffprobePath: join(directory, 'missing-ffprobe') }),
      (error: unknown) => error instanceof AudioReferenceError
        && error.kind === 'missing-tool'
        && /missing ffprobe tool/.test(error.message),
    );
    await assert.rejects(
      decodeExportAudio({ artifactPath, outputWavPath: join(directory, 'audio.wav'), ffmpegPath: join(directory, 'missing-ffmpeg') }),
      (error: unknown) => error instanceof AudioReferenceError
        && error.kind === 'missing-tool'
        && /missing ffmpeg tool/.test(error.message),
    );
  });
});

test('handoff keeps same-artifact inputs and the existing sample clock explicit', () => {
  assert.match(AUDIO_PARITY_HANDOFF.referenceInput, /exact downloaded App Render-button MP4/);
  assert.equal(AUDIO_PARITY_HANDOFF.playerInput, 'real Player capture WAV');
  assert.match(AUDIO_PARITY_HANDOFF.sampleClock, /48_000 Hz/);
  assert.match(AUDIO_PARITY_HANDOFF.alignment, /none/);
});
