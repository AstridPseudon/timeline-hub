import assert from 'node:assert/strict';
import { execFile } from 'node:child_process';
import { createHash } from 'node:crypto';
import { mkdtemp, readFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { test } from 'node:test';
import { promisify } from 'node:util';
import { gainDifferenceDb, requireUnchangedGain } from '../player-audio-comparator';
import { monitorSamples, SAMPLE_RATE } from '../player-audio-monitor';
import { decodeExportAudioMonitor } from './export-audio-monitor';

const exec = promisify(execFile);

async function withFixture(sampleRate: number, channels: number, check: (artifactPath: string, outputWavPath: string) => Promise<void>) {
  const directory = await mkdtemp(join(tmpdir(), 'export-audio-monitor-'));
  try {
    const artifactPath = join(directory, 'same-download.mp4');
    await exec('ffmpeg', [
      '-v', 'error', '-nostdin', '-y', '-f', 'lavfi',
      '-i', `sine=frequency=660:sample_rate=${sampleRate}:duration=3`,
      '-ac', String(channels), '-c:a', 'aac', '-b:a', '128k', artifactPath,
    ]);
    await check(artifactPath, join(directory, 'decoded.wav'));
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
}

test('shared probe gain comparator retains its 0.5 dB threshold', () => {
  assert.equal(gainDifferenceDb(1, 1), 0);
  assert.ok(Math.abs(gainDifferenceDb(0.5, 1) + 6.0206) < 0.0001);
  for (const db of [-0.49, 0.49]) requireUnchangedGain(10 ** (db / 20), 1);
  for (const db of [-0.51, 0.51]) {
    assert.throws(() => requireUnchangedGain(10 ** (db / 20), 1), /captured output gain mismatch/);
  }
});

test('same-download AAC uses unchanged PCM in the existing monitor and shared gain comparator', async () => {
  await withFixture(SAMPLE_RATE, 2, async (artifactPath, outputWavPath) => {
    const sourceBefore = await readFile(artifactPath);
    const decoded = await decodeExportAudioMonitor({ artifactPath, outputWavPath });
    assert.equal(decoded.status, 'supported');
    const { reference, rawPcm, monitor } = decoded;
    const { stdout: sourcePcm } = await exec('ffmpeg', [
      '-v', 'error', '-nostdin', '-i', artifactPath, '-map', `0:${reference.source.audioStreamIndex}`,
      '-f', 's16le', 'pipe:1',
    ], { encoding: 'buffer', maxBuffer: 4 * 1024 * 1024 });

    assert.equal(reference.artifactPath, artifactPath);
    assert.equal(reference.outputWavPath, outputWavPath);
    assert.equal(reference.sourceSha256Before, `sha256:${createHash('sha256').update(sourceBefore).digest('hex')}`);
    assert.equal(reference.sourceSha256After, reference.sourceSha256Before);
    assert.deepEqual(await readFile(artifactPath), sourceBefore);
    assert.deepEqual(rawPcm, sourcePcm);
    assert.deepEqual(Buffer.from(monitor.pcm.buffer, monitor.pcm.byteOffset, monitor.pcm.byteLength), rawPcm);
    assert.equal(monitor.sampleCount, rawPcm.length / 4);
    assert.ok(monitor.sampleCount >= 3 * SAMPLE_RATE);
    assert.ok(monitor.sampleCount < 3.1 * SAMPLE_RATE);
    assert.deepEqual(reference.conversion.filters, []);
    assert.deepEqual(reference.conversion.timingEdits, []);
    assert.equal(reference.conversion.resampled, false);
    assert.equal(reference.conversion.channelMapping, false);
    assert.ok(reference.source.packets.length > 0);

    // Helper controls only: these are not actual Player captures or gate-6 evidence.
    const half = monitorSamples(monitor.pcm.map(value => Math.round(value * 0.5)));
    const muted = monitorSamples(new Int16Array(monitor.pcm.length));
    for (const start of [0.5, 1.5, 2.5]) {
      for (const channel of [0, 1]) {
        const level = monitor.rms(start, start + 0.1, channel);
        assert.ok(Number.isFinite(level) && level > 0.01);
        requireUnchangedGain(level, level);
        requireUnchangedGain(half.rms(start, start + 0.1, channel), level * 0.5);
        assert.throws(() => requireUnchangedGain(half.rms(start, start + 0.1, channel), level),
          /captured output gain mismatch: -6\./);
        assert.throws(() => requireUnchangedGain(muted.rms(start, start + 0.1, channel), level),
          /captured output gain mismatch: -Infinity dB/);
      }
    }
    console.log('SAME_EXPORT_AUDIO_MONITOR', JSON.stringify({
      artifactPath, outputWavPath, hashes: [reference.sourceSha256Before, reference.sourceSha256After],
      source: reference.source.audioStream, packets: reference.source.packets,
      output: reference.output, sampleCount: monitor.sampleCount,
    }));
  });
});

for (const [sampleRate, channels] of [[44_100, 2], [48_000, 1]]) {
  test(`native ${sampleRate}Hz/${channels}ch is unsupported without conversion or lost metadata`, async () => {
    await withFixture(sampleRate, channels, async (artifactPath, outputWavPath) => {
      const decoded = await decodeExportAudioMonitor({ artifactPath, outputWavPath });
      assert.equal(decoded.status, 'unsupported');
      assert.match(decoded.reason, /requires native 48000Hz stereo/);
      assert.equal(decoded.reference.source.audioStream.sample_rate, String(sampleRate));
      assert.equal(decoded.reference.source.audioStream.channels, channels);
      assert.equal(decoded.reference.sourceSha256Before, decoded.reference.sourceSha256After);
      assert.equal(decoded.reference.conversion.resampled, false);
      assert.equal(decoded.reference.conversion.channelMapping, false);
      assert.ok(decoded.reference.source.packets.length > 0);
    });
  });
}
