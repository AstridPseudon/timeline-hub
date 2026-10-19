import assert from 'node:assert/strict';
import { test } from 'node:test';
import { audibleEdges, monitorSamples, requireAudibleDuration, SAMPLE_RATE } from './player-audio-monitor';

test('known three-second linear and frame-stepped fades pass the live edge-duration comparator', () => {
  for (const frameStepped of [false, true]) {
    const pcm = new Int16Array(6 * SAMPLE_RATE * 2);
    for (let sample = 0; sample < 3 * SAMPLE_RATE; sample++) {
      const time = frameStepped ? Math.floor(sample / SAMPLE_RATE * 30) / 30 : sample / SAMPLE_RATE;
      const gain = Math.min(1, time / 0.6) * Math.min(1, (3 - time) / 0.6);
      const value = 0.25 * gain * Math.sin(2 * Math.PI * 660 * sample / SAMPLE_RATE);
      const index = (sample + Math.round(0.4 * SAMPLE_RATE)) * 2;
      pcm[index] = Math.round(32768 * value);
      pcm[index + 1] = Math.round(32768 * value * 0.75);
    }
    const capture = monitorSamples(pcm);
    const edges = audibleEdges(capture);
    console.log('SYNTHETIC_FADE', JSON.stringify({ frameStepped, onset: edges.onset, offset: edges.offset, duration: edges.offset - edges.onset }));
    requireAudibleDuration(edges.offset - edges.onset);
    assert.throws(() => requireAudibleDuration(2.84), /three-second live media duration/);
    assert.ok(capture.rms(0.46, 0.56) / capture.rms(1.4, 2.4) < 0.6);
    assert.ok(capture.rms(3.2, 3.3) / capture.rms(1.4, 2.4) < 0.6);
  }
});
