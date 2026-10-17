import { describe, expect, it } from 'vitest';
import type { EditCommand } from '@/integrations/runtime/generated.ts';
import { fadeHistoryInverse, isFadeHistoryBatch, isFadeHistoryInverse } from './fadeHistory.ts';

const absent = { state: 'absent' } as const;
const present = (value: unknown) => ({ state: 'present' as const, value });
const call = (effects: unknown = absent): EditCommand => ({ op: 'clip.set-fade', select: 'parent/clip:c', resolved: ['parent/clip:c'],
  args: { fade_in: null }, expect: { effects, entrance: absent, exit: present(null) } } as EditCommand);
const writes = [ { id: 'parent/clip:c', path: 'effects', before: absent, after: present({ fade_in: null, opaque: [null, {}] }) },
  { id: 'parent/clip:c', path: 'entrance', before: absent, after: present(null) } ];
const receipt = (direct_writes: unknown[] = writes) => ({ status: 'accepted', accepted_publication_id: 'pub-real', change: { direct_writes } });

describe('fade receipt history boundary', () => {
  it('uses only the publication and exact swapped tagged direct writes', () => {
    const inverse = fadeHistoryInverse([call()], receipt())!;
    expect(inverse).toEqual({ op: 'timeline.inverse', select: null, args: { publication: 'pub-real', writes: writes.map(w => ({ ...w, before: w.after, after: w.before })) } });
    expect(isFadeHistoryInverse(inverse)).toBe(true);
    expect(fadeHistoryInverse([inverse], receipt(writes.map(w => ({ ...w, before: w.after, after: w.before }))))).toEqual({ ...inverse, args: { publication: 'pub-real', writes } });
    (inverse.args.writes as typeof writes)[0].after = present('mutated') as never;
    expect(writes[0].before).toEqual(absent);
  });
  it.each([absent, present(null), present({ fade_out: 0.2, opaque: { x: null } })])('admits the actual effects-container state %j', effects => {
    const path = effects.state === 'present' && effects.value !== null ? 'effects.fade_in' : 'effects';
    expect(fadeHistoryInverse([call(effects)], receipt([{ ...writes[0], path }]))).toBeDefined();
    expect(fadeHistoryInverse([call(effects)], receipt([{ ...writes[0], path: path === 'effects' ? 'effects.fade_in' : 'effects' }]))).toBeUndefined();
  });
  it.each(['wrong clip', 'wrong scope', 'extra path', 'opposite side', 'duplicate', 'extra key', 'malformed tag', 'empty', 'missing publication'] as const)('rejects %s receipts', kind => {
    const result = receipt(structuredClone(writes));
    const row = result.change.direct_writes[0] as Record<string, unknown>;
    if (kind === 'wrong clip') row.id = 'parent/clip:other';
    if (kind === 'wrong scope') row.id = 'occurrence:other/clip:c';
    if (kind === 'extra path') row.path = 'params';
    if (kind === 'opposite side') result.change.direct_writes.push({ ...writes[1], path: 'exit' });
    if (kind === 'duplicate') result.change.direct_writes.push(structuredClone(writes[0]));
    if (kind === 'extra key') row.owner = 'forged';
    if (kind === 'malformed tag') row.before = { state: 'absent', value: null };
    if (kind === 'empty') result.change.direct_writes = [];
    if (kind === 'missing publication') result.accepted_publication_id = '';
    expect(fadeHistoryInverse([call()], result)).toBeUndefined();
  });
  it('does not acquire new inverse paths or clips on Redo', () => {
    const inverse = fadeHistoryInverse([call()], receipt([writes[1]]))!;
    expect(fadeHistoryInverse([inverse], receipt(writes))).toBeUndefined();
    const complete = fadeHistoryInverse([call()], receipt(writes))!;
    expect(fadeHistoryInverse([complete], receipt([writes[0]]))).toBeUndefined();
    expect(fadeHistoryInverse([inverse], receipt([{ ...writes[1], id: 'parent/clip:other' }]))).toBeUndefined();
  });
  it.each(['refused', 'conflict', 'preview', 'error'])('creates no inverse for %s', status => {
    expect(fadeHistoryInverse([call()], { ...receipt(), status })).toBeUndefined();
  });
  it('acknowledges no-change without inventing a publication', () => {
    expect(fadeHistoryInverse([call()], { ...receipt(), status: 'no_change', accepted_publication_id: null, change: { direct_writes: [] } })).toBeNull();
  });
  it.each(['legacy array', 'bad clear', 'negative', 'unknown arg', 'unresolved', 'multiple clips', 'missing tag'] as const)('rejects %s commands', kind => {
    const command = call();
    if (kind === 'legacy array') command.expect!.effects = present([]);
    if (kind === 'bad clear') command.args.clear = ['fade_in'];
    if (kind === 'negative') command.args.fade_in = -1;
    if (kind === 'unknown arg') command.args.param = 3;
    if (kind === 'unresolved') delete command.resolved;
    if (kind === 'missing tag') delete command.expect!.exit;
    const batch = kind === 'multiple clips' ? [command, call()] : [command];
    expect(isFadeHistoryBatch(batch)).toBe(false);
    expect(fadeHistoryInverse(batch, receipt())).toBeUndefined();
  });
});
