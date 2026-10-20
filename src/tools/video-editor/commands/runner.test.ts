import { describe, expect, it } from 'vitest';
import { buildTimelineData } from '@/tools/video-editor/lib/timeline-data.ts';
import { TIMELINE_POSTPROCESS_SHADER_APP_KEY } from '@/tools/video-editor/lib/timeline-domain.ts';
import { validateSerializedConfig } from '@/tools/video-editor/lib/serialize.ts';
import type { TimelineConfig } from '@/tools/video-editor/types/index.ts';
import { createTimelineCommandRunner } from './runner.ts';
import type { TimelineCommandEffect } from './types.ts';

const makeCurrent = () => buildTimelineData({
  output: { width: 1280, height: 720, fps: 30 },
  tracks: [{ id: 'V1', kind: 'visual' }],
  clips: [{ id: 'clip-1', track: 'V1', at: 0, clipType: 'hold', hold: 2 }],
}, { assets: {} });

const runnerFor = (effect: TimelineCommandEffect) => createTimelineCommandRunner([{
  type: 'test-effect',
  validate: () => [],
  apply: () => effect,
  dryRun: () => effect,
  invert: () => null,
}]);

describe.each(['data', 'config'] as const)('%s effect internal validation', (type) => {
  it.each([
    ['clip field', (config: TimelineConfig) => Object.assign(config.clips[0], { unexpected: true })],
    ['track field', (config: TimelineConfig) => Object.assign(config.tracks![0], { unexpected: true })],
    ['track role', (config: TimelineConfig) => Object.assign(config.tracks![0], { role: 'invalid' })],
    ['live binding', (config: TimelineConfig) => { config.clips[0].params = { liveBindings: [{ bindingId: 'binding-1' }] }; }],
    ['clip shader stack', (config: TimelineConfig) => {
      config.clips[0].app = { shader: [
        { scope: 'clip', extensionId: 'test', contributionId: 'first', shaderId: 'first' },
        { scope: 'clip', extensionId: 'test', contributionId: 'second', shaderId: 'second' },
      ] } as never;
    }],
    ['postprocess shader stack', (config: TimelineConfig) => {
      config.app = { [TIMELINE_POSTPROCESS_SHADER_APP_KEY]: [
        { scope: 'postprocess', extensionId: 'test', contributionId: 'first', shaderId: 'first' },
        { scope: 'postprocess', extensionId: 'test', contributionId: 'second', shaderId: 'second' },
      ] } as never;
    }],
  ])('rejects malformed %s before normalization even alongside opaque roots', async (_name, mutate) => {
    const current = await makeCurrent();
    const before = JSON.stringify(current);
    const config = structuredClone(current.config);
    mutate(config);
    // Public validation proves the existing non-root guard also rejects it.
    expect(() => validateSerializedConfig(config)).toThrow();
    const opaqueConfig = { ...config, ...JSON.parse('{"opaque":[null,false,0],"__proto__":{"literal":true}}') };
    const effect: TimelineCommandEffect = { mutation: type === 'data'
      ? { type, data: { ...current, config: opaqueConfig } }
      : { type, config: opaqueConfig } };
    const runner = runnerFor(effect);
    for (const result of [runner.apply(current, { type: 'test-effect', payload: {} }), runner.dryRun(current, { type: 'test-effect', payload: {} })]) {
      expect(result.status).toBe('rejected');
      expect(result.nextData).toBe(current);
      expect(result.errors[0].message).not.toContain('unexpected top-level key');
    }
    expect(JSON.stringify(current)).toBe(before);
  });
});

describe('command envelope guards with opaque roots', () => {
  it.each([NaN, Infinity, -Infinity])('rejects a non-finite payload value %s before applying its effect', async (at) => {
    const current = await makeCurrent();
    Object.assign(current.config, { opaque: null });
    const runner = runnerFor({ mutation: { type: 'data', data: current } });
    const result = runner.apply(current, { type: 'test-effect', payload: { at } });
    expect(result.status).toBe('rejected');
    expect(result.errors[0].code).toBe('invalid_command');
    expect(result.nextData).toBe(current);
  });
});
