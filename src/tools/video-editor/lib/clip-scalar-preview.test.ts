import { describe, expect, it } from 'vitest';
import type { TimelinePatch, TimelinePatchOperation } from '@/sdk/video/timeline/patch.ts';
import type { TimelineConfig } from '../types/index.ts';
import { assembleTimelineData } from './timeline-data.ts';
import { compileTimelinePatch, validateTimelinePatch } from './timeline-patch.ts';

function current() {
  const config = { output: { fps: 30, resolution: '1920x1080' }, tracks: [{ id: 'V1', kind: 'visual' }],
    opaque: { keep: [null, { nested: true }] }, clips: [
      { id: 'z', track: 'V1', at: 7.01234567, hold: 4, speed: 2, asset: 'a', transition: null,
        from: 1, to: 5, opaque: { keep: true }, app: { opaque: [null, 9] } },
      { id: 'a', track: 'V1', at: 1, hold: 3, opaque: 'preserve order' },
    ] } as unknown as TimelineConfig;
  return assembleTimelineData({ config, configVersion: 1, resolvedConfig: { ...config, tracks: config.tracks!, registry: {} },
    registry: { assets: {} }, assetMap: {}, output: config.output });
}
const patch = (op: Partial<TimelinePatchOperation>): TimelinePatch => ({ version: 1, operations: [{ op: 'clip.update', target: 'z', payload: {}, ...op }] });

describe('local clip.update scalar leaf preview', () => {
  it.each(['hold', 'asset', 'transition'] as const)('removes %s exactly without normalizing other authored leaves or clip order', (key) => {
    const data = current();
    const before = structuredClone(data.config);
    const preview = JSON.parse(JSON.stringify(patch({ clear: [key] })));
    const compiled = compileTimelinePatch(preview, data);
    expect(compiled.valid).toBe(true);
    const expected = structuredClone(before);
    delete expected.clips[0][key];
    expect(compiled.nextData!.config).toEqual(expected);
    expect(compiled.nextData!.config.clips[0]).not.toHaveProperty(key);
    expect(compiled.nextData!.resolvedConfig.clips[0]).not.toHaveProperty(key);
    expect(compiled.nextData!.clipOrder).toEqual(data.clipOrder);
    expect(data.config).toEqual(before);
    expect(compiled.mutation).toBeNull();
    expect(compiled.nextData!.config.clips[0]).not.toHaveProperty('clear');
  });
  it('keeps exact source hold seconds, speed and the source window', () => {
    const data = current();
    const result = compileTimelinePatch(patch({ payload: { hold: 4.123456789 }, clear: [] }), data);
    expect(result.nextData!.config.clips).toEqual([{ ...data.config.clips[0], hold: 4.123456789 }, data.config.clips[1]]);
    expect(result.nextData!.rows[0].actions.find((action) => action.id === 'z')).toMatchObject({ start: 7.01234567,
      end: 7.01234567 + 4.123456789 / 2 });
  });
  it.each([
    { clear: ['asset', 'asset'] }, { clear: ['unknown'] }, { clear: null }, { clear: 'asset' },
    { clear: ['hold'], payload: { hold: 4 } }, { clear: [], payload: { asset: null } },
    { clear: [], payload: { mode: 'replace' } }, { clear: ['asset'], op: 'asset.update' },
  ])('rejects malformed/removal-as-value metadata: %j', (op) => {
    expect(validateTimelinePatch(patch(op as never)).valid).toBe(false);
  });
  it.each([null, '', 0, -1, Infinity, NaN])('rejects invalid hold values %j', (hold) => {
    expect(compileTimelinePatch(patch({ payload: { hold }, clear: [] }), current()).valid).toBe(false);
  });
  it('fails atomically for a missing/ambiguous target or mixed mutation batch', () => {
    const data = current();
    expect(compileTimelinePatch(patch({ target: 'missing', clear: ['asset'] }), data).valid).toBe(false);
    data.config.clips.push(data.config.clips[0]);
    expect(compileTimelinePatch(patch({ clear: ['asset'] }), data).valid).toBe(false);
    const mixed = patch({ clear: ['asset'] });
    expect(compileTimelinePatch({ ...mixed, operations: [...mixed.operations, { op: 'track.remove', target: 'V1' }] }, current()).valid).toBe(false);
  });
});
