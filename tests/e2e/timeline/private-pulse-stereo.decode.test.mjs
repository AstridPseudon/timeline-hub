import assert from 'node:assert/strict';
import {mkdtemp, rm, writeFile} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {test} from 'node:test';
import {createSyntheticPcmWav} from './tab-audio-capture.analysis.mjs';
import {decodeFloat} from './private-pulse-stereo.decode.mjs';

test('decodes PCM larger than the child-process stdout default without buffering stdout', async () => {
  const directory = await mkdtemp(join(tmpdir(), 'timeline-private-pulse-decode-test-'));
  const input = join(directory, 'input.wav');
  try {
    await writeFile(input, createSyntheticPcmWav({durationSeconds: 3}));
    const samples = await decodeFloat(input, 0);
    assert.equal(samples.length, 3 * 48_000 * 2);
    assert.ok(samples.byteLength > 1024 * 1024);
  } finally {
    await rm(directory, {recursive: true, force: true});
  }
});
