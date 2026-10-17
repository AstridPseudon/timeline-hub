import { describe, expect, it } from 'vitest';
import type { EditCommand } from '@/integrations/runtime/generated.ts';
import { clipParamsHistoryInverse, isClipParamsHistoryBatch, isClipParamsHistoryInverse } from './clipParamsHistory.ts';
const command = (path = 'data', value: unknown = { opaque: [null, { $absent: true }] }, before: NonNullable<EditCommand['expect']>[string] = { state: 'present', value: null }): EditCommand => ({
  op: 'clip.set-param', select: 'parent/clip:c1', resolved: ['parent/clip:c1'], args: { path, value }, expect: { [`params.${path}`]: before },
});
const write = (path = 'data', value: unknown = { opaque: [null, { $absent: true }] }, before: unknown = { state: 'present', value: null }) => ({
  id: 'parent/clip:c1', path: `params.${path}`, before, after: { state: 'present', value },
});
const receipt = (writes: unknown[] = [write()]) => ({ status: 'accepted', accepted_publication_id: 'accepted-publication', change: { direct_writes: writes } });
describe('W64 params receipt boundary', () => {
  it('binds a complete changed-key inventory while leaving unchanged keys out of the inverse', () => {
    const commands = [command(), command('added', null, { state: 'absent' }), command('retained', ['same'], { state: 'present', value: ['same'] })];
    const inverse = clipParamsHistoryInverse(commands, receipt([write('added', null, { state: 'absent' }), write()]))!;
    expect(isClipParamsHistoryInverse(inverse)).toBe(true);
    expect(inverse.args.publication).toBe('accepted-publication');
    expect(inverse.args.writes).toEqual([write('added', null, { state: 'absent' }), write()].map(row => ({ ...row, before: row.after, after: row.before })));
    expect(clipParamsHistoryInverse([inverse], receipt(inverse.args.writes as unknown[]))?.args.writes).toEqual([write('added', null, { state: 'absent' }), write()]);
  });
  it.each(['missing', 'unexpected', 'duplicate', 'bad before', 'bad after', 'missing state', 'absent value', 'missing value', 'top-level', 'nested', 'wrong target', 'extra metadata', 'no publication'])(
    'refuses %s direct receipt ownership', kind => {
      const row: Record<string, unknown> = write();
      if (kind === 'bad before') row.before = { state: 'absent' };
      if (kind === 'bad after') row.after = { state: 'present', value: 'wrong' };
      if (kind === 'missing state') row.before = {};
      if (kind === 'absent value') row.before = { state: 'absent', value: null };
      if (kind === 'missing value') row.after = { state: 'present' };
      if (kind === 'top-level') row.path = 'opacity';
      if (kind === 'nested') row.path = 'params.data.child';
      if (kind === 'wrong target') row.id = 'parent/clip:other';
      if (kind === 'extra metadata') row.consequence = true;
      const result = receipt(kind === 'missing' ? [] : kind === 'unexpected' ? [row, write('extra')] : kind === 'duplicate' ? [row, row] : [row]);
      if (kind === 'no publication') result.accepted_publication_id = '';
      expect(clipParamsHistoryInverse([command()], result)).toBeUndefined();
    });
  it('requires every changed key, including when duplicate rows match the expected count', () => {
    expect(clipParamsHistoryInverse([command(), command('second')], receipt([write(), write()]))).toBeUndefined();
  });
  it.each(['conflict', 'refused', 'error', 'preview'])('%s cannot arm history', status => {
    expect(clipParamsHistoryInverse([command()], { ...receipt(), status })).toBeUndefined();
  });
  it('recognizes no-change only with an empty actual write inventory', () => {
    const unchanged = command('data', null);
    expect(clipParamsHistoryInverse([unchanged], { ...receipt([]), status: 'no_change' })).toBeNull();
    expect(clipParamsHistoryInverse([command()], { ...receipt([]), status: 'no_change' })).toBeUndefined();
    expect(clipParamsHistoryInverse([unchanged], { ...receipt(), status: 'no_change' })).toBeUndefined();
  });
  it.each(['clip.clear', 'clip.set-look', 'duplicate key', 'mixed clip', 'occurrence', 'nested key', 'missing expect'])(
    'does not widen this family to %s', kind => {
      const commands = [command()];
      if (kind === 'clip.clear' || kind === 'clip.set-look') commands[0].op = kind;
      if (kind === 'duplicate key') commands.push(command());
      if (kind === 'mixed clip') commands.push({ ...command('other'), select: 'parent/clip:c2', resolved: ['parent/clip:c2'] });
      if (kind === 'occurrence') { commands[0].select = 'occurrence:o/clip:c1'; commands[0].resolved = [commands[0].select]; }
      if (kind === 'nested key') commands[0].args.path = 'data.child';
      if (kind === 'missing expect') delete commands[0].expect;
      expect(isClipParamsHistoryBatch(commands)).toBe(false);
      expect(clipParamsHistoryInverse(commands, receipt())).toBeUndefined();
    });
});
