import { describe, expect, it } from 'vitest';
import type { EditCommand } from '@/integrations/runtime/generated.ts';
import { clipLookStyleInverse, isClipLookStyleBatch, isClipLookStyleInverse } from './clipLookStyleHistory.ts';
const set = (name = 'opacity', path = 'opacity', before: unknown = { state: 'present', value: 0.9 }): EditCommand => ({
  op: 'clip.set-look', select: 'parent/clip:a', resolved: ['parent/clip:a'], args: { [name]: 0 }, expect: { [path]: before },
});
const write = (path = 'opacity', before: unknown = { state: 'present', value: 0.9 }) => ({ id: 'parent/clip:a', path, before, after: { state: 'present', value: 0 } });
const receipt = (writes: unknown[] = [write()]) => ({ status: 'accepted', accepted_publication_id: 'publication-exact', change: { direct_writes: writes } });
describe('clip look style receipt adapter', () => {
  it('preserves tags and codec-normalized crop paths with zero and publication identity', () => {
    const writes = [write(), write('cropTop', { state: 'absent' })];
    const inverse = clipLookStyleInverse([set(), set('crop_top', 'cropTop', { state: 'absent' })], receipt(writes))!;
    expect(inverse).toEqual({ op: 'timeline.inverse', select: null, args: { publication: 'publication-exact',
      writes: writes.map(row => ({ ...row, before: row.after, after: row.before })) } });
    expect(isClipLookStyleInverse(inverse)).toBe(true);
    const redoWrites = writes.map(row => ({ ...row, before: row.after, after: row.before }));
    expect(clipLookStyleInverse([inverse], receipt(redoWrites))!.args.writes).toEqual(writes);
    expect(writes[1].before).toEqual({ state: 'absent' });
  });
  it('allows an unchanged requested sibling only when changed fields have exact receipt coverage', () => {
    const commands = [set(), { ...set('volume', 'volume', { state: 'present', value: 0 }), args: { volume: 0 } }];
    expect(clipLookStyleInverse(commands, receipt())).toBeDefined();
    expect(clipLookStyleInverse(commands, receipt([]))).toBeUndefined();
  });
  it.each(['missing', 'extra', 'duplicate', 'before', 'after', 'tag', 'path', 'id', 'unchanged', 'extra key'])(
    'rejects %s receipt', kind => {
      const base = write();
      const rows = kind === 'missing' ? [] : kind === 'extra' ? [base, write('volume')] : kind === 'duplicate' ? [base, base]
        : kind === 'before' ? [{ ...base, before: { state: 'absent' } }] : kind === 'after' ? [{ ...base, after: { state: 'present', value: 0.5 } }]
        : kind === 'tag' ? [{ ...base, after: { state: 'absent', value: 0 } }] : kind === 'path' ? [write('crop_top')]
        : kind === 'id' ? [{ ...base, id: 'parent/clip:other' }] : kind === 'unchanged' ? [{ ...base, after: base.before }]
        : [{ ...base, authority: 'invented' }];
      expect(clipLookStyleInverse([set()], receipt(rows))).toBeUndefined();
    });
  it.each(['preview', 'conflict', 'error', 'refused'])('%s creates no inverse', status => {
    expect(clipLookStyleInverse([set()], { ...receipt(), status })).toBeUndefined();
  });
  it('requires accepted publication and returns null only for an admitted no-change owner', () => {
    expect(clipLookStyleInverse([set()], { ...receipt(), accepted_publication_id: null })).toBeUndefined();
    expect(clipLookStyleInverse([set()], { ...receipt(), status: 'no_change' })).toBeNull();
    expect(clipLookStyleInverse([], { ...receipt(), status: 'no_change' })).toBeUndefined();
  });
  it.each(['speed', 'entrance', 'exit', 'transition', 'fade_in', 'params', 'cropTop'])(
    '%s remains outside this family', name => expect(isClipLookStyleBatch([set(name)])).toBe(false));
  it('excludes mixed move, hold, clear and duplicate-field commands', () => {
    for (const op of ['clip.nudge', 'clip.set-duration', 'clip.clear']) expect(isClipLookStyleBatch([set(), { ...set(), op }])).toBe(false);
    expect(isClipLookStyleBatch([set(), set()])).toBe(false);
    expect(isClipLookStyleBatch([{ ...set(), expect: {} }])).toBe(false);
    expect(isClipLookStyleBatch([{ ...set(), resolved: [] }])).toBe(false);
    expect(isClipLookStyleBatch([{ ...set(), args: { opacity: Number.NaN } }])).toBe(false);
  });
  it('rejects inverse receipts escaping the exact owned fields or states', () => {
    const inverse = clipLookStyleInverse([set()], receipt())!;
    expect(clipLookStyleInverse([inverse], receipt([write('volume')]))).toBeUndefined();
    expect(clipLookStyleInverse([inverse], receipt())).toBeUndefined();
  });
});
