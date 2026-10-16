import Ajv from 'ajv';
import { describe, expect, it } from 'vitest';
import {
  validateAudioEnvelope,
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

describe('authored audio envelope persistence', () => {
  it('survives JSON load, default-row metadata, a row edit, shared save and reload with every registered curve', async () => {
    const original = makeConfig({ envelope });
    validateAudioEnvelope(envelope);
    expect(schema.definitions.AudioEnvelope.properties.keyframes.items.properties.curve.enum)
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
  ])('leaves %s uncoerced by the field sanitizer and rejects it at both schema entry points', (_name, audio) => {
    const config = makeConfig();
    Object.assign(config.clips[0], { audio });
    const sanitized = sanitizeTimelineClipSnapshot(config.clips[0]);
    expect(sanitized.audio).toEqual(audio);
    expect(validateClip(sanitized)).toBe(false);
    expect(validateConfig({ ...config, clips: [sanitized] })).toBe(false);
  });
});
