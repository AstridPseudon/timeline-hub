import { describe, expect, it } from 'vitest';
import type { EditCommand } from '@/integrations/runtime/generated.ts';
import { isPositionResetBatch, isPositionResetInverse, positionResetFields, positionResetInverse } from './positionReset.ts';
const paths = Object.values(positionResetFields);
const command = (id = 'parent/clip:a'): EditCommand => ({ op: 'clip.clear', select: id, resolved: [id], args: { keys: Object.keys(positionResetFields) },
  expect: Object.fromEntries(paths.map((path, index) => [path, index % 3 === 0 ? { state: 'absent' } : { state: 'present', value: index % 3 === 1 ? null : index }])) });
const writes = (commands = [command()]) => commands.flatMap(call => paths.map(path => ({ id: call.select!, path, before: call.expect![path], after: { state: 'absent' } })));
const receipt = (direct_writes: unknown[] = writes()) => ({ status: 'accepted', accepted_publication_id: 'accepted-publication', change: { direct_writes } });
describe('W32 position reset receipt custody', () => {
  it('keeps all eight tagged guards and constructs Redo solely from the Undo receipt', () => {
    const calls = [command('parent/clip:b'), command()];
    const direct = writes(calls); const undo = positionResetInverse(calls, receipt(direct))!;
    expect(isPositionResetBatch(calls)).toBe(true); expect(isPositionResetInverse(undo)).toBe(true);
    expect(undo.args.writes).toEqual(direct.map(row => ({ ...row, before: row.after, after: row.before })));
    expect(positionResetInverse([undo], receipt(undo.args.writes as unknown[]))!.args.writes).toEqual(direct);
  });
  it.each(['missing', 'extra', 'duplicate', 'wrong-before', 'wrong-last-path', 'wrong-member', 'non-finite'])('%s receipt refuses usable history', mode => {
    const rows = structuredClone(writes()) as Array<Record<string, unknown>>;
    if (mode === 'missing') rows.pop();
    if (mode === 'extra') rows.push(rows[0]);
    if (mode === 'duplicate') rows[7] = rows[0];
    if (mode === 'wrong-before') rows[7].before = { state: 'present', value: 93 };
    if (mode === 'wrong-last-path') rows[7].path = 'params.height';
    if (mode === 'wrong-member') rows[7].id = 'parent/clip:b';
    if (mode === 'non-finite') rows[7].after = { state: 'present', value: Infinity };
    expect(positionResetInverse([command()], receipt(rows))).toBeUndefined();
  });
  it('accepts only complete guarded no-change and never manufactures publication identity', () => {
    const call = command(); call.expect = Object.fromEntries(paths.map(path => [path, { state: 'absent' }]));
    const result = { ...receipt(writes([call])), status: 'no_change', accepted_publication_id: null };
    expect(positionResetInverse([call], result)).toBeNull();
    expect(positionResetInverse([command()], result)).toBeUndefined();
    expect(positionResetInverse([call], { ...result, change: { direct_writes: [] } })).toBeUndefined();
  });
  it('does not admit partial crop clears, null numeric setters, mixed owners or bad final guards', () => {
    expect(isPositionResetBatch([{ ...command(), args: { keys: ['crop_top'] } }])).toBe(false);
    expect(isPositionResetBatch([{ ...command(), op: 'clip.set-look', args: { position_x: null } }])).toBe(false);
    expect(isPositionResetBatch([command(), command('occurrence:a/clip:b')])).toBe(false);
    const call = command(); delete call.expect!.cropRight; expect(isPositionResetBatch([call])).toBe(false);
    expect(positionResetInverse([command()], { ...receipt(), accepted_publication_id: null })).toBeUndefined();
  });
});
