import { describe, expect, it } from 'vitest';
import type { EditCommand } from '@/integrations/runtime/generated.ts';
import type { TimelineData } from '../lib/timeline-data.ts';
import { attachGestureCommands, continuousBatchGestureCommands, continuousEffectGestureCommands, gestureCommandsFor, propertyGestureCommands } from './semanticGestures.ts';
import { continuousHistoryInverse, continuousParameterPatch, isContinuousHistoryBatch, isContinuousHistoryInverse } from './continuousHistory.ts';

const effect = { type: 'custom:orbit', intensity: 0.731, params: { amount: 2, nested: { old: true }, opaque: [null, { $absent: true }] }, opaque: { keep: null } };
const state = (value: unknown) => ({ state: 'present' as const, value });
const data = (...values: Array<unknown>) => ({ config: { clips: values.map((value, i) => ({ id: `c${i}`, ...(value === undefined ? {} : { continuous: value }) })) } }) as TimelineData;
const mapped = (d: TimelineData, id: string, value: unknown) => continuousEffectGestureCommands(d, id, { continuous: value } as never).commands!;
const rows = (commands: EditCommand[]) => commands.map(c => ({ id: c.select!, path: 'continuous', before: c.expect!.continuous,
  after: c.args.clear ? { state: 'absent' } : state(c.args.continuous) }));
const receipt = (writes: unknown[]) => ({ status: 'accepted', accepted_publication_id: 'pub-forward', change: { direct_writes: writes } });

describe('W27 continuous pure mapping and receipt boundary', () => {
  it.each([undefined, null, effect])('captures full tagged prior %j before mutation', before => {
    const d = data(before), value = structuredClone(effect), commands = mapped(d, 'c0', value);
    expect(commands).toEqual([{ op: 'clip.set-continuous', select: 'parent/clip:c0', resolved: ['parent/clip:c0'],
      args: { continuous: effect }, expect: { continuous: before === undefined ? { state: 'absent' } : state(before) } }]);
    value.params.amount = 99;
    expect(commands[0].args.continuous).toEqual(effect);
    expect(isContinuousHistoryBatch(commands)).toBe(true);
  });
  it('clears only undefined; null and malformed values retain whole-operation fallback', () => {
    expect(mapped(data(null), 'c0', undefined)[0].args).toEqual({ clear: true });
    for (const value of [null, [], { type: '' }, { type: 'orbit', params: null }, { type: 'orbit', intensity: Infinity }, { ...effect, opaque: undefined }]) {
      expect(continuousEffectGestureCommands(data(effect), 'c0', { continuous: value } as never)).toEqual({ handled: true });
    }
    expect(continuousEffectGestureCommands(data(effect), 'c0', { continuous: effect, opacity: 0.5 })).toEqual({ handled: true });
    expect(propertyGestureCommands(data(effect), 'c0', { continuous: effect })).toBeUndefined();
  });
  it('preserves explicitly authored params intent and shallow whole-value replacement', () => {
    const d = data(structuredClone(effect));
    const patch = continuousParameterPatch(structuredClone(effect), { nested: { replacement: null } });
    const commands = continuousEffectGestureCommands(d, 'c0', patch).commands!;
    expect(commands[0].args).toEqual({ params: { nested: { replacement: null } } });
    const after = { ...effect, params: { ...effect.params, nested: { replacement: null } } };
    const inverse = continuousHistoryInverse(commands, receipt([{ id: 'parent/clip:c0', path: 'continuous', before: state(effect), after: state(after) }]))!;
    expect(isContinuousHistoryInverse(inverse)).toBe(true);
    expect((inverse.args.writes as Array<{ before: unknown }>)[0].before).toEqual(state(after));
    const changedDefaults = continuousParameterPatch({ ...effect, intensity: 0.5 }, { amount: 3 });
    expect(continuousEffectGestureCommands(d, 'c0', changedDefaults).commands![0].args).toHaveProperty('continuous');
  });
  it('retains selection order, different priors, no-op omission and complete inverse coverage', () => {
    const d = data(effect, null, undefined);
    const commands = [...mapped(d, 'c2', effect), ...mapped(d, 'c0', effect), ...mapped(d, 'c1', effect)];
    const writes = rows(commands).filter(w => w.id !== 'parent/clip:c0');
    const inverse = continuousHistoryInverse(commands, receipt(writes))!;
    expect((inverse.args.writes as Array<{id: string}>).map(w => w.id)).toEqual(['parent/clip:c2', 'parent/clip:c1']);
    const undoRows = (inverse.args.writes as unknown[]);
    expect(continuousHistoryInverse([inverse], { ...receipt(undoRows), accepted_publication_id: 'pub-undo' })?.args.writes).toEqual(writes);
    expect(continuousHistoryInverse(commands, receipt([writes[0], writes[0]]))).toBeUndefined();
    expect(continuousHistoryInverse([inverse], receipt(undoRows.slice(0, 1)))).toBeUndefined();
    expect(continuousHistoryInverse([inverse], receipt(undoRows))).toBeUndefined(); // reused forward publication
  });
  it.each(['missing', 'extra', 'duplicate', 'foreign', 'before', 'after', 'malformed', 'nested path', 'metadata', 'no publication', 'refused', 'no_change', 'preview'])('rejects %s receipt', kind => {
    const commands = [...mapped(data(null, undefined), 'c0', effect), ...mapped(data(null, undefined), 'c1', effect)];
    const writes = rows(commands) as Array<Record<string, unknown>>;
    if (kind === 'missing') writes.pop();
    if (kind === 'extra') writes.push({ ...writes[0], id: 'parent/clip:c3' });
    if (kind === 'duplicate') writes[1] = writes[0];
    if (kind === 'foreign') writes[1].id = 'occurrence:other/clip:c1';
    if (kind === 'before') writes[1].before = state({ lost: true });
    if (kind === 'after') writes[1].after = state(null);
    if (kind === 'malformed') writes[1].after = { state: 'present' };
    if (kind === 'nested path') writes[1].path = 'continuous.params.amount';
    if (kind === 'metadata') writes[1].extra = true;
    const result = receipt(writes);
    if (kind === 'no publication') result.accepted_publication_id = '';
    if (['refused', 'no_change', 'preview'].includes(kind)) result.status = kind;
    expect(continuousHistoryInverse(commands, result)).toBeUndefined();
  });
  it('acknowledges no-change only for an unchanged batch with no writes or publication', () => {
    const commands = mapped(data(effect), 'c0', effect);
    expect(continuousHistoryInverse(commands, { ...receipt([]), status: 'no_change', accepted_publication_id: null })).toBeNull();
    expect(continuousHistoryInverse(commands, receipt([]))).toBeUndefined();
  });
  it('keeps occurrence source identity and source before-value rather than display metadata', () => {
    const d = data(null);
    d.head = { projectId: 'p', timelineId: 't', headRevisionId: 'h' };
    d.config.clips[0].app = { canonical: { projectId: 'p', parentDocumentId: 't', headRevisionId: 'h',
      occurrenceId: 'occ-A', shotId: 'A', revisionId: 'shot-r1', internalTimelineRevisionId: 'internal-r1',
      sourceClipId: 'source', outputIdentity: 'out', sourceClip: { id: 'source', continuous: effect } } } as never;
    const commands = mapped(d, 'c0', undefined);
    expect(commands[0]).toMatchObject({ select: 'occurrence:occ-A/clip:source', expect: { continuous: state(effect) } });
    attachGestureCommands(d, commands);
    expect(gestureCommandsFor(d)).toEqual(commands);
  });
  it('keeps a mixed-context bulk operation on whole-operation fallback', () => {
    const d = data(effect, null);
    const commands = [...mapped(d, 'c0', undefined), ...mapped(d, 'c1', effect)];
    commands[1].select = 'occurrence:foreign/clip:source'; commands[1].resolved = [commands[1].select];
    expect(continuousBatchGestureCommands(d, commands.map(c => [c]))).toBeUndefined();
  });
  it('rejects duplicate selectors and wrong resolved identities', () => {
    const commands = mapped(data(effect), 'c0', undefined);
    expect(isContinuousHistoryBatch([...commands, ...commands])).toBe(false);
    commands[0].resolved = ['parent/clip:other'];
    expect(isContinuousHistoryBatch(commands)).toBe(false);
  });
});
