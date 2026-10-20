import {createWriteStream} from 'node:fs';
import {mkdtemp, readFile, rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {pipeline} from 'node:stream/promises';
import {spawn} from 'node:child_process';

const STDERR_LIMIT = 64 * 1024;

export async function decodeFloat(path, streamIndex) {
  if (!Number.isInteger(streamIndex) || streamIndex < 0) throw new Error('Audio stream index is invalid');

  const directory = await mkdtemp(join(tmpdir(), 'timeline-private-pulse-decode-'));
  const decodedPath = join(directory, 'audio.f32le');
  const decoder = spawn('ffmpeg', [
    '-v', 'error', '-i', path, '-map', `0:${streamIndex}`, '-f', 'f32le', 'pipe:1',
  ], {stdio: ['ignore', 'pipe', 'pipe']});
  let stderr = '';
  decoder.stderr.setEncoding('utf8');
  decoder.stderr.on('data', (chunk) => {
    if (stderr.length < STDERR_LIMIT) stderr += chunk.slice(0, STDERR_LIMIT - stderr.length);
  });
  const exited = new Promise((resolve, reject) => {
    decoder.once('error', reject);
    decoder.once('close', (code, signal) => {
      if (code === 0) resolve();
      else reject(new Error(`ffmpeg ${code ?? signal}: ${stderr}`));
    });
  });
  const written = pipeline(decoder.stdout, createWriteStream(decodedPath, {flags: 'wx'}));

  try {
    await Promise.all([exited, written]);
    const bytes = await readFile(decodedPath);
    if (bytes.length % Float32Array.BYTES_PER_ELEMENT) throw new Error('PCM output is not float32-aligned');
    return new Float32Array(bytes.buffer, bytes.byteOffset, bytes.length / Float32Array.BYTES_PER_ELEMENT);
  } finally {
    if (decoder.exitCode === null && decoder.signalCode === null) decoder.kill('SIGKILL');
    await Promise.allSettled([exited, written]);
    await rm(directory, {recursive: true, force: true});
  }
}
