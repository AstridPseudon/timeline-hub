import assert from 'node:assert/strict';
import { test } from 'node:test';
import { assertNativePts, recordTabStream, TAB_AUDIO_MIME } from './tab-audio';

class MockRecorder {
  state = 'inactive';
  private listeners = new Map<string, (event?: any) => void>();

  constructor(private readonly stream: { getTracks: () => Array<{ kind: string; readyState: string }> }, private readonly options: { mimeType: string }) {
    assert.equal(options.mimeType, TAB_AUDIO_MIME);
    assert.equal(stream.getTracks().length, 2);
  }

  addEventListener(name: string, listener: (event?: any) => void): void {
    this.listeners.set(name, listener);
  }

  start(): void {
    this.state = 'recording';
    queueMicrotask(() => this.listeners.get('dataavailable')?.({ data: { arrayBuffer: async () => Uint8Array.from([0x1a, 0x45, 0xdf, 0xa3]) } }));
  }

  stop(): void {
    this.state = 'inactive';
    queueMicrotask(() => this.listeners.get('stop')?.());
  }
}

function mockBackend(overrides: Partial<Record<'warm' | 'ready' | 'play' | 'wait' | 'stopPlayer', () => Promise<void>>> = {}) {
  const tracks = [
    { kind: 'video', readyState: 'live', stopped: false, stop: () => undefined },
    { kind: 'audio', readyState: 'live', stopped: false, stop: () => undefined },
  ];
  const events: string[] = [];
  const stream = {
    getTracks: () => tracks,
  };
  return {
    backend: {
      getDisplayMedia: async () => { events.push('getDisplayMedia'); return stream; },
      MediaRecorder: MockRecorder,
      warm: overrides.warm ?? (async () => { events.push('warm'); }),
      ready: overrides.ready ?? (async () => { events.push('ready'); }),
      play: overrides.play ?? (async () => { events.push('play'); }),
      wait: overrides.wait ?? (async () => { events.push('wait'); }),
      stopPlayer: overrides.stopPlayer ?? (async () => { events.push('stopPlayer'); }),
    },
    events,
    tracks,
  } as const;
}

test('stream mocks start the recorder before warm/readiness/play and retain mux bytes', async () => {
  const mock = mockBackend();
  const result = await recordTabStream({ durationMs: 1 }, mock.backend);
  assert.deepEqual(result.events, ['before-warm', 'stream:ready', 'recorder:start', 'warm', 'readiness', 'play', 'recorder:stop', 'tracks:stop', 'cleanup']);
  assert.deepEqual(mock.events, ['getDisplayMedia', 'warm', 'ready', 'play', 'wait', 'stopPlayer']);
  assert.deepEqual(result.chunks, ['GkXfow==']);
  assert.deepEqual(result.tracks, [{ kind: 'video', readyState: 'live' }, { kind: 'audio', readyState: 'live' }]);
  assert.equal(result.events.indexOf('recorder:start') < result.events.indexOf('warm'), true);
  assert.equal(result.events.indexOf('warm') < result.events.indexOf('readiness'), true);
  assert.equal(result.events.indexOf('readiness') < result.events.indexOf('play'), true);
});

test('stream failure still stops the recorder tracks without asserting physical audio mix', async () => {
  const mock = mockBackend({ warm: async () => { throw new Error('warm failed'); } });
  let stopped = 0;
  for (const track of mock.tracks) track.stop = () => { stopped++; };
  await assert.rejects(recordTabStream({}, mock.backend), /warm failed/);
  assert.equal(stopped, 2);
});

test('native packet timestamps are required for one video and one audio stream', () => {
  assertNativePts({
    streams: [{ codec_type: 'video' }, { codec_type: 'audio' }],
    packets: [
      { codec_type: 'audio', pts: '0' }, { codec_type: 'video', pts: '42' },
      { codec_type: 'audio', pts: '960' }, { codec_type: 'video', pts: '83' },
    ],
    format: {},
  });
  assert.throws(() => assertNativePts({
    streams: [{ codec_type: 'video' }, { codec_type: 'audio' }],
    packets: [{ codec_type: 'video', pts: '42' }, { codec_type: 'video', pts: '41' }],
    format: {},
  }), /video packet pts are not monotonic/);
});
