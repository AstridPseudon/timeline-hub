import Ajv from 'ajv';
import { createTimelineCommandRunner, type TimelineCommand, type TimelineCommandContext, type TimelineCommandDescriptor } from '../commands';
import { describe, expect, it } from 'vitest';
import {
  validateAudioEnvelope,
  compileAudioEnvelope,
  audioEnvelopeAt,
  type AudioEnvelope,
} from '@banodoco/timeline-composition/evaluation';
import schema from '../../../../vendor/timeline-schema/typescript/dist/timeline.schema.json';
import { AUDIO_GAIN_CURVES } from '../../../../vendor/timeline-composition/typescript/src/lib/audio-curves.generated';
import { buildTimelineData, rowsToConfig, type TimelineData } from './timeline-data';
import { buildDataFromCurrentRegistry } from './timeline-save-utils';
import { serializeForDisk } from './serialize';
import { sanitizeTimelineClipSnapshot, serializeTimelineConfigSnapshot } from './timeline-domain';
import type { AssetRegistry, TimelineClip, TimelineConfig } from '../types';

const envelope: AudioEnvelope = {
  keyframes: Object.keys(AUDIO_GAIN_CURVES).map((curve, index) => ({
    at: index / 10,
    value: index / 5,
    curve: curve as keyof typeof AUDIO_GAIN_CURVES,
  })),
  multiply: [{ keyframes: [{ at: 0, value: 0.8 }] }],
  minimum: [{ keyframes: [{ at: 0, value: 0.5 }] }],
  duck: true,
};
const registry: AssetRegistry = {
  assets: { tone: { file: 'synthetic-tone.wav', type: 'audio/wav' } },
};
const makeConfig = (audio?: TimelineClip['audio']): TimelineConfig => ({
  theme: '2rp',
  output: { resolution: '1920x1080', fps: 30, file: 'out.mp4' },
  tracks: [{ id: 'A1', kind: 'audio', label: 'Audio', volume: 0.5 }],
  app: { vendor: { opaque: ['keep', null, { nested: true }] } },
  clips: [{
    id: 'tone', at: 0, track: 'A1', asset: 'tone', clipType: 'media',
    from: 0.25, to: 1.25, speed: 1, volume: 0.4,
    params: { fadeIn: 0.73, fadeOut: 0.83, fadeInCurve: 's-curve', opaque: [1, null, { keep: true }] },
    app: { vendor: { opaque: 'preserve { bytes }', nested: [false, 1.23456789] } },
    ...(audio !== undefined ? { audio } : {}),
  }],
});
const toConfig = (data: TimelineData): TimelineConfig => rowsToConfig(
  data.rows, data.meta, data.output, data.clipOrder, data.tracks,
  data.config.pinnedShotGroups, data.config,
);
const save = (data: TimelineData): TimelineConfig => {
  const rebuilt = buildDataFromCurrentRegistry(toConfig(data), data);
  return JSON.parse(JSON.stringify(serializeForDisk(rebuilt.resolvedConfig)));
};
// Compile the assigned vendored schema itself, not the permissive test shim or
// the LOCK083 dependency's copy. Both schema entry points are public contracts.
const ajv = new Ajv({ allErrors: true, strictKeywords: true });
const validateConfig = ajv.compile(schema);
const validateClip = ajv.compile({ ...schema, $ref: '#/definitions/TimelineClip' });
const expectSchemaValid = (config: TimelineConfig): void => {
  expect(validateConfig(config), JSON.stringify(validateConfig.errors)).toBe(true);
  expect(validateClip(config.clips[0]), JSON.stringify(validateClip.errors)).toBe(true);
};
const expectOpaqueAndLegacy = (actual: TimelineConfig, original: TimelineConfig): void => {
  expect(JSON.stringify(actual.app)).toBe(JSON.stringify(original.app));
  expect(JSON.stringify(actual.clips[0].app)).toBe(JSON.stringify(original.clips[0].app));
  expect(JSON.stringify(actual.clips[0].params)).toBe(JSON.stringify(original.clips[0].params));
};

type Move = TimelineCommand<'move-clip', {clipId: string; at: number}>;
const moveEffect = ({currentData, command}: TimelineCommandContext<Move>) => ({
  mutation: {type: 'rows' as const, rows: currentData.rows.map(row => ({...row,
    actions: row.actions.map(action => action.id === command.payload!.clipId
      ? {...action, start: command.payload!.at, end: command.payload!.at + action.end - action.start} : action),
  }))}, summary: 'move authored audio',
});
const move: TimelineCommandDescriptor<Move> = {
  type: 'move-clip', validate: () => [], apply: moveEffect, dryRun: moveEffect,
  invert: ({currentData, command}) => ({type: 'move-clip', payload: {
    clipId: command.payload!.clipId,
    at: currentData.rows.flatMap(row => row.actions).find(action => action.id === command.payload!.clipId)!.start,
  }}),
};

describe('authored audio envelope persistence', () => {
  it('preserves authored gain and opaque values through command, projection, inverse and reload', async () => {
    const original = makeConfig({ envelope });
    const data = await buildTimelineData(original, registry);
    const runner = createTimelineCommandRunner([move]);
    const applied = runner.apply(data, { transactionId: 'audio-roundtrip', commands: [
      { type: 'move-clip', payload: { clipId: 'tone', at: 2 } },
    ] });
    expect(applied.status).toBe('ok');
    expect(save(applied.nextData).clips[0].audio).toEqual({ envelope });
    expectOpaqueAndLegacy(save(applied.nextData), original);
    expect(applied.history.inverseTransaction).toBeTruthy();
    const undone = runner.apply(applied.nextData, applied.history.inverseTransaction!);
    expect(undone.status).toBe('ok');
    const reloaded = await buildTimelineData(save(undone.nextData), registry);
    expect(save(reloaded).clips[0].audio).toEqual({ envelope });
    expect(save(reloaded).clips[0].at).toBe(0);
    expectOpaqueAndLegacy(save(reloaded), original);
  });

  it('uses above-unity gain and overlapping factors once, ahead of legacy fades', () => {
    const gain = { keyframes: [{ at: 0, value: 2 }],
      multiply: [{ keyframes: [{ at: 0, value: 0.8 }] }],
      minimum: [{ keyframes: [{ at: 0, value: 0.5 }] }, { keyframes: [{ at: 0, value: 0.25 }] }] };
    const clip = makeConfig({ envelope: gain }).clips[0];
    const compiled = compileAudioEnvelope({id: clip.id, at: clip.at, track: clip.track, from: clip.from, to: clip.to, speed: clip.speed, params: clip.params, audio: clip.audio}, 30)!;
    expect(compiled).toBe(gain);
    expect(audioEnvelopeAt(compiled, 0)).toBeCloseTo(2 * 0.8 * 0.25);
  });

  it.each([
    { keyframes: [{ at: 0, value: 1 }], duck: 1 },
    { keyframes: [{ at: 0, value: 1 }], duck: null },
    { keyframes: [{ at: 0, value: true }] },
    { keyframes: [{ at: NaN, value: 1 }] },
    { keyframes: [{ at: 0, value: Infinity }] },
    { keyframes: [{ at: 0, value: NaN }] },
    { keyframes: [{ at: 0, value: 1, curve: null }] },
    { keyframes: [{ at: 1, value: 1 }, { at: 0, value: 1 }] },
    { keyframes: [{ at: 0, value: 1 }, { at: 0, value: 2 }] },
  ])('reuses semantic validation at storage before JSON can hide malformed values: %j', malformed => {
    const clip = makeConfig({ envelope }).clips[0];
    Object.assign(clip, { audio: { envelope: malformed } });
    expect(() => sanitizeTimelineClipSnapshot(clip)).toThrow();
    expect(() => validateAudioEnvelope(malformed as AudioEnvelope)).toThrow();
  });

  it('survives JSON load, default-row metadata, a row edit, shared save and reload with every registered curve', async () => {
    const original = makeConfig({ envelope });
    validateAudioEnvelope(envelope);
    expect(schema.definitions.AudioEnvelopeKeyframe.properties.curve.enum)
      .toEqual(Object.keys(AUDIO_GAIN_CURVES));
    const data = await buildTimelineData(JSON.parse(JSON.stringify(original)), registry);
    expect(data.meta.tone.audio).toEqual({ envelope });
    data.rows[0].actions[0].start += 1 / 30;
    data.rows[0].actions[0].end += 1 / 30;
    const rowsConfig = toConfig(data);
    expect(rowsConfig.clips[0].audio).toEqual({ envelope });
    const saved = save(data);
    expect(saved.clips[0].audio).toEqual({ envelope });
    expect(saved.clips[0].at).toBeCloseTo(1 / 30, 4);
    expect(saved.clips[0].from).toBe(0.25);
    expect(saved.clips[0].to).toBe(1.25);
    expectOpaqueAndLegacy(saved, original);
    expectSchemaValid(saved);
    const reloaded = await buildTimelineData(saved, registry);
    expect(reloaded.config.clips[0].audio).toEqual({ envelope });
    expect(reloaded.meta.tone.audio).toEqual({ envelope });
    expect(save(reloaded)).toEqual(saved);
  });

  it('retains audio through strict snapshot serialization while stripping resolved-only clip fields', async () => {
    const original = makeConfig({ envelope });
    expect(serializeTimelineConfigSnapshot(original).config.clips[0].audio).toEqual({ envelope });
    const data = await buildTimelineData(original, registry);
    const saved = serializeForDisk(data.resolvedConfig);
    expect(saved.clips[0].audio).toEqual({ envelope });
    expect(saved.clips[0]).not.toHaveProperty('assetEntry');
    expect(saved.clips[0]).not.toHaveProperty('src');
    expectOpaqueAndLegacy(saved, original);
    expectSchemaValid(saved);
  });

  it('keeps legacy audio absence absent through metadata, save and reload without materializing fades', async () => {
    const original = makeConfig();
    const data = await buildTimelineData(original, registry);
    expect(data.meta.tone).not.toHaveProperty('audio');
    const saved = save(data);
    expect(saved.clips[0]).not.toHaveProperty('audio');
    expectOpaqueAndLegacy(saved, original);
    expectSchemaValid(saved);
    const reloaded = await buildTimelineData(saved, registry);
    expect(reloaded.meta.tone).not.toHaveProperty('audio');
    expect(save(reloaded)).toEqual(saved);
  });

  it.each(['undefined', 'delete'] as const)('keeps an authored audio clear by %s omitted after save and reload', async (clear) => {
    const original = makeConfig({ envelope });
    const data = await buildTimelineData(original, registry);
    expect(data.meta.tone.audio).toEqual({ envelope });
    // Existing optional-field clear representation: undefined is omitted on
    // serialization; deletion is already absent. No null sentinel is added.
    if (clear === 'delete') delete data.meta.tone.audio;
    else data.meta.tone.audio = undefined;
    const saved = save(data);
    expect(saved.clips[0]).not.toHaveProperty('audio');
    expectOpaqueAndLegacy(saved, original);
    expectSchemaValid(saved);
    const reloaded = await buildTimelineData(saved, registry);
    expect(reloaded.meta.tone).not.toHaveProperty('audio');
    expect(save(reloaded)).toEqual(saved);
  });

  it.each([
    ['null audio', null],
    ['missing envelope', {}],
    ['null envelope', { envelope: null }],
    ['empty keyframes', { envelope: { keyframes: [] } }],
    ['negative gain', { envelope: { keyframes: [{ at: 0, value: -1 }] } }],
    ['unknown curve', { envelope: { keyframes: [{ at: 0, value: 1, curve: 'unknown' }] } }],
    ['extra keyframe field', { envelope: { keyframes: [{ at: 0, value: 1, extra: true }] } }],
    ['unsupported envelope field', { envelope: { keyframes: [{ at: 0, value: 1 }], extra: true } }],
    ['invalid nested envelope', { envelope: { keyframes: [{ at: 0, value: 1 }], minimum: [{}] } }],
    ['invalid duck flag', { envelope: { keyframes: [{ at: 0, value: 1 }], duck: 'yes' } }],
    ['derived render source', { envelope, render_source: { url: 'blob:derived' } }],
  ])('rejects %s at storage and both schema entry points', (_name, audio) => {
    const config = makeConfig();
    Object.assign(config.clips[0], { audio });
    expect(() => sanitizeTimelineClipSnapshot(config.clips[0])).toThrow();
    expect(validateClip(config.clips[0])).toBe(false);
    expect(validateConfig(config)).toBe(false);
  });
});
