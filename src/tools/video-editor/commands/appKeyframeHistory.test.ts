import { describe, expect, it } from 'vitest';
import type { EditCommand } from '@/integrations/runtime/generated.ts';
import { appKeyframeHistoryInverse, isAppKeyframeHistoryBatch } from './appKeyframeHistory.ts';
const call = (): EditCommand => ({ op: 'clip.set', select: 'parent/clip:c', resolved: ['parent/clip:c'],
  args: { keyframes: { 'literal.key[0]': [{ time: 7.125, value: false, interpolation: 'hold', opaque: [null, { a: 1.125 }] }] }, keyframeOrigin: -2.375 },
  expect: { keyframes: { state: 'present', value: null }, keyframeOrigin: { state: 'present', value: -2.375 } },
});
function receipt() { const c = call(); return { status: 'accepted', accepted_publication_id: 'publication-real', change: { direct_writes:
  ['keyframes', 'keyframeOrigin'].map(path => ({ id: c.select!, path, before: c.expect![path], after: { state: 'present', value: c.args[path] } })),
} }; }
describe('W26 receipt qualification', () => {
  it('retains paired equal-origin forward writes and builds only changed inverse replay writes', () => {
    const inverse = appKeyframeHistoryInverse([call()], receipt())!;
    expect(inverse.args.writes).toHaveLength(2);
    const writes = receipt().change.direct_writes.slice(0, 1).map(write => ({ ...write, before: write.after, after: write.before }));
    const redo = appKeyframeHistoryInverse([inverse], { ...receipt(), accepted_publication_id: 'undo-real', change: { direct_writes: writes } })!;
    expect(redo.args).toEqual({ publication: 'undo-real', writes: receipt().change.direct_writes.slice(0, 1) });
  });
  it.each(['missing', 'extra', 'duplicate', 'foreign', 'malformed', 'wrong-before', 'wrong-after', 'no-publication'])(
    '%s cannot authorize history', kind => {
      const result = receipt();
      if (kind === 'missing') result.change.direct_writes.pop();
      if (kind === 'extra') result.change.direct_writes.push({ ...result.change.direct_writes[0], path: 'params.keyframes' });
      if (kind === 'duplicate') result.change.direct_writes[1] = result.change.direct_writes[0];
      if (kind === 'foreign') result.change.direct_writes[0].id = 'occurrence:other/clip:c';
      if (kind === 'malformed') result.change.direct_writes[0].before = { state: 'absent', value: null } as never;
      if (kind === 'wrong-before') result.change.direct_writes[0].before = { state: 'absent' };
      if (kind === 'wrong-after') result.change.direct_writes[0].after.value = {};
      if (kind === 'no-publication') result.accepted_publication_id = '';
      expect(appKeyframeHistoryInverse([call()], result)).toBeUndefined();
    });
  it('acknowledges only the complete equal paired no-change receipt without an inverse', () => {
    const c = call(); c.expect = Object.fromEntries(Object.entries(c.args).map(([path, value]) => [path, { state: 'present', value }]));
    const result = receipt(); result.status = 'no_change'; result.accepted_publication_id = null as never;
    result.change.direct_writes = result.change.direct_writes.map(write => ({ ...write, before: write.after }));
    expect(appKeyframeHistoryInverse([c], result)).toBeNull();
    expect(appKeyframeHistoryInverse([c], { ...result, change: { direct_writes: [] } })).toBeUndefined();
  });
  it('rejects no-change for an actual changed pair', () => expect(appKeyframeHistoryInverse([call()], {
    status: 'no_change', accepted_publication_id: null, change: { direct_writes: [] },
  })).toBeUndefined());
  it.each(['missing-pair', 'extra-field', 'batch', 'wrong-scope'])(
    'does not register unsupported %s shapes', kind => {
      const c = call(); const calls = [c];
      if (kind === 'missing-pair') delete c.args.keyframeOrigin;
      if (kind === 'extra-field') c.args.speed = 2;
      if (kind === 'batch') calls.push({ ...call(), select: 'parent/clip:other' });
      if (kind === 'wrong-scope') c.select = 'clip:c';
      expect(isAppKeyframeHistoryBatch(calls)).toBe(false);
    });
});
