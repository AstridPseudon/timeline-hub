import {execFileSync} from 'node:child_process';
import {mkdtempSync, rmSync, statSync, writeFileSync} from 'node:fs';
import path from 'node:path';
import {
  applyAudioEnvelope, audioEnvelopeWav, compileAudioEnvelope,
} from '@banodoco/timeline-composition/evaluation';

// Inactive preparation kernel. The caller supplies the compiled clip's public
// source clock, using compiledAudioSourceClock from package 11's trim/rate helpers.
// Never pass a previously prepared source or persist these results as authored data.
export const prepareAttemptEnvelopePcm = ({
  clip, fps, source, attemptDirectory, sourceClock,
  maxDecodedBytes = 64 * 1024 * 1024,
}) => {
  const envelope = compileAudioEnvelope(clip, fps);
  if (!envelope) return undefined;
  if (clip.audio?.render_source !== undefined) throw new Error('source already prepared');
  if (!sourceClock || !Number.isFinite(sourceClock.source_from)
    || sourceClock.source_from < 0 || !Number.isFinite(sourceClock.playback_rate)
    || sourceClock.playback_rate <= 0) throw new Error('public source clock required');
  if (!Number.isSafeInteger(maxDecodedBytes) || maxDecodedBytes <= 0
    || maxDecodedBytes > 0xffffffff - 44) throw new Error('invalid PCM byte limit');
  if (!path.isAbsolute(source) || !statSync(source).isFile()
    || !path.isAbsolute(attemptDirectory) || !statSync(attemptDirectory).isDirectory()) {
    throw new Error('local source and attempt directory required');
  }
  const run = (program, args, maxBuffer) => execFileSync(program, args, {
    maxBuffer, timeout: 30000, stdio: ['ignore', 'pipe', 'pipe'],
  });
  const probe = JSON.parse(run('ffprobe', [
    '-v', 'error', '-protocol_whitelist', 'file,pipe', '-select_streams', 'a:0',
    '-show_entries', 'stream=sample_rate,channels,start_time', '-of', 'json', source,
  ], 64 * 1024).toString());
  const stream = probe.streams?.[0];
  const sampleRate = Number(stream?.sample_rate), count = stream?.channels;
  if (!Number.isSafeInteger(sampleRate) || sampleRate <= 0
    || !Number.isSafeInteger(count) || count <= 0
    || (stream.start_time !== undefined && Number(stream.start_time) !== 0)) {
    throw new Error('source PCM clock cannot be retained');
  }
  // Full first audio stream, at its original rate/channel count. No filters,
  // trimming, tempo, normalization, scalar gain, padding or timestamp adjustment.
  const pcm = run('ffmpeg', [
    '-v', 'error', '-nostdin', '-protocol_whitelist', 'file,pipe', '-i', source,
    '-map', '0:a:0', '-threads', '1', '-c:a', 'pcm_f32le', '-f', 'f32le', 'pipe:1',
  ], maxDecodedBytes);
  if (!pcm.length || pcm.length % (count * 4) !== 0) throw new Error('invalid decoded PCM');
  const samples = pcm.length / (count * 4);
  const channels = Array.from({length: count}, () => new Float32Array(samples));
  for (let sample = 0; sample < samples; sample++) for (let channel = 0; channel < count; channel++) {
    const value = pcm.readFloatLE((sample * count + channel) * 4);
    if (!Number.isFinite(value)) throw new Error('non-finite source PCM');
    channels[channel][sample] = value;
  }
  applyAudioEnvelope(channels, sampleRate, envelope,
    sourceClock.source_from, sourceClock.playback_rate);
  const wav = Buffer.from(audioEnvelopeWav(channels, sampleRate));
  const directory = mkdtempSync(path.join(attemptDirectory, 'envelope-'));
  try {
    const output = path.join(directory, 'source.wav');
    writeFileSync(output, wav, {flag: 'wx'});
    // The existing consumer parses JSON before comparing its canonical key.
    // Only the later asset-stage owner can attach the attempt's HTTP file URL.
    return {path: output, envelope_key: JSON.stringify(envelope),
      source_from: sourceClock.source_from, playback_rate: sourceClock.playback_rate};
  } catch (error) {
    rmSync(directory, {recursive: true, force: true});
    throw error;
  }
};
