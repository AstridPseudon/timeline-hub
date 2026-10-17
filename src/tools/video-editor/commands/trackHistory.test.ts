import { describe, expect, it } from 'vitest';
import type { EditCommand } from '@/integrations/runtime/generated.ts';
import { isTrackHistoryBatch, isTrackHistoryInverse, trackHistoryInverse } from './trackHistory.ts';
import { act, renderHook } from '@testing-library/react';
import { vi } from 'vitest';
import { buildTimelineData } from '../lib/timeline-data.ts';
import { useTimelineTrackManagement } from '../hooks/useTimelineTrackManagement.ts';
const patch = (id = 'parent/track:A1'): EditCommand => ({ op: 'timeline.set', select: id, args: { values: { muted: true }, clear: [] }, expect: { [`${id}::muted`]: { state: 'absent' } } });
const write = (id = 'parent/track:A1', path = 'muted') => ({ id, path, before: { state: 'absent' }, after: { state: 'present', value: true } });
const receipt = (writes: unknown[] = [write()]) => ({ status: 'accepted', accepted_publication_id: 'actual', change: { direct_writes: writes } });
describe('bounded track publication inverse', () => {
  it('admits the actual W48 moveTrack captured whole-order command and D156 direct receipt', async () => {
    const data = await buildTimelineData({ output: { resolution: '1280x720', fps: 30, file: 'out.mp4' },
      tracks: [{ id: 'V1', kind: 'visual' }, { id: 'A1', kind: 'audio' }, { id: 'V2', kind: 'visual' }], clips: [] }, { assets: {} });
    const applyEdit = vi.fn();
    const hook = renderHook(() => useTimelineTrackManagement({ dataRef: { current: data }, resolvedConfig: data.resolvedConfig,
      selectedClipId: null, setSelectedTrackId: vi.fn(), applyEdit }));
    act(() => hook.result.current.handleMoveTrack('V1', 'V2'));
    const commands = applyEdit.mock.calls[0][1].editCommands as EditCommand[];
    expect(commands[0].args).toEqual({ expected_order: oldOrder, order: newOrder });
    expect(isTrackHistoryBatch(commands)).toBe(true);
    const inverse = trackHistoryInverse(commands, receipt([orderWrite()]))!;
    expect(isTrackHistoryInverse(inverse)).toBe(true);
    expect(inverse.args).toEqual({ publication: 'actual', writes: [{ ...orderWrite(), before: orderWrite().after, after: orderWrite().before }] });
    hook.unmount();
  });
  it('accepts exact multi-track patches and keeps tagged states', () => {
    const inverse = trackHistoryInverse([patch(), patch('parent/track:A4')], receipt([write(), write('parent/track:A4')]))!;
    expect(isTrackHistoryInverse(inverse)).toBe(true);
    expect(inverse.args.writes[0]).toEqual({ ...write(), before: write().after, after: write().before });
  });
  it.each(['foreign field', 'foreign target', 'duplicate', 'aggregate container'])('rejects %s in actual receipt', kind => {
    const writes = kind === 'foreign field' ? [write(undefined, 'app.secret')]
      : kind === 'foreign target' ? [write('parent/track:other')]
      : kind === 'duplicate' ? [write(), write()] : [write('parent', 'config.tracks')];
    expect(trackHistoryInverse([patch()], receipt(writes))).toBeUndefined();
  });
  it('does not adopt track reorder from missing receipt data or a consequence array', () => {
    expect(isTrackHistoryBatch([{ op: 'timeline.reorder', select: 'parent/track:A1', args: { order: [], expected_order: [] } }])).toBe(false);
    expect(trackHistoryInverse([patch()], receipt([]))).toBeUndefined();
    expect(isTrackHistoryInverse({ op: 'timeline.inverse', select: null, args: { publication: 'actual', writes: [write(undefined, 'track_order')] } })).toBe(false);
  });
  it('an inverse cannot obtain additional authored paths on Redo', () => {
    const inverse = trackHistoryInverse([patch()], receipt())!;
    expect(trackHistoryInverse([inverse], receipt([write(undefined, 'volume')]))).toBeUndefined();
  });
  it.each(['refused', 'conflict', 'error'])('%s supplies no ownership', status => {
    expect(trackHistoryInverse([patch()], { ...receipt(), status })).toBeUndefined();
  });
  it('preserves no_change as explicit null', () => {
    expect(trackHistoryInverse([patch()], { ...receipt(), status: 'no_change' })).toBeNull();
  });
});

const oldOrder = ['parent/track:V1', 'parent/track:A1', 'parent/track:V2'];
const newOrder = ['parent/track:A1', 'parent/track:V2', 'parent/track:V1'];
const reorder = (): EditCommand => ({ op: 'timeline.reorder', select: oldOrder[0], args: { expected_order: [...oldOrder], order: [...newOrder] },
  expect: { [`${oldOrder[0]}::track_order`]: { state: 'present', value: [...oldOrder] } } });
const orderWrite = () => ({ id: oldOrder[0], path: 'track_order', before: { state: 'present', value: [...oldOrder] }, after: { state: 'present', value: [...newOrder] } });

describe('W48 exact reorder receipt boundary', () => {
  it('uses the accepted publication and accepts the exact Undo receipt at a newer publication', () => {
    const undo = trackHistoryInverse([reorder()], receipt([orderWrite()]))!;
    const undoWrite = undo.args.writes[0];
    const redo = trackHistoryInverse([undo], { ...receipt([undoWrite]), accepted_publication_id: 'undo-publication' })!;
    expect(redo.args).toEqual({ publication: 'undo-publication', writes: [orderWrite()] });
  });
  it('keeps accepted no-change without an undo entry and rejects an accepted unchanged write', () => {
    const command = reorder(); command.args.order = [...oldOrder];
    expect(trackHistoryInverse([command], { ...receipt([]), status: 'no_change' })).toBeNull();
    expect(trackHistoryInverse([command], receipt([{ ...orderWrite(), after: orderWrite().before }]))).toBeUndefined();
  });
  it.each(['missing', 'extra', 'duplicate', 'foreign id', 'foreign path', 'consequence', 'before order', 'after order',
    'identity change', 'duplicate identity', 'occurrence identity', 'absent', 'extra tag', 'extra key', 'unrelated publication'])('rejects %s receipt', kind => {
    const row = orderWrite(); let writes: unknown[] = [row];
    if (kind === 'missing') writes = [];
    if (kind === 'extra') writes.push(write());
    if (kind === 'duplicate') writes.push(orderWrite());
    if (kind === 'foreign id') row.id = oldOrder[1];
    if (kind === 'foreign path') row.path = 'order';
    if (kind === 'consequence') { row.id = 'parent'; row.path = 'config.tracks'; }
    if (kind === 'before order') row.before.value.reverse();
    if (kind === 'after order') row.after.value.reverse();
    if (kind === 'identity change') row.after.value[0] = 'parent/track:OTHER';
    if (kind === 'duplicate identity') row.after.value[0] = row.after.value[1];
    if (kind === 'occurrence identity') row.after.value[0] = 'occurrence:A/track:A1';
    if (kind === 'absent') writes = [{ ...row, before: { state: 'absent' } }];
    if (kind === 'extra tag') writes = [{ ...row, before: { ...row.before, extra: true } }];
    if (kind === 'extra key') writes = [{ ...row, extra: true }];
    const result = { ...receipt(writes), ...(kind === 'unrelated publication' ? { accepted_publication_id: '' } : {}) };
    expect(trackHistoryInverse([reorder()], result)).toBeUndefined();
  });
  it.each(['missing guard', 'stale guard', 'partial expected', 'partial target', 'duplicate', 'foreign', 'unselected', 'extra args', 'mixed batch'])('rejects %s command', kind => {
    const command = reorder(); const commands = [command];
    if (kind === 'missing guard') delete command.expect;
    if (kind === 'stale guard') command.expect![`${command.select}::track_order`] = { state: 'present', value: [...oldOrder].reverse() };
    if (kind === 'partial expected') command.args.expected_order = oldOrder.slice(1);
    if (kind === 'partial target') command.args.order = newOrder.slice(1);
    if (kind === 'duplicate') command.args.order = [oldOrder[0], oldOrder[0], oldOrder[1]];
    if (kind === 'foreign') command.args.order = ['occurrence:A/track:V1', ...newOrder.slice(1)];
    if (kind === 'unselected') command.select = 'parent/track:OTHER';
    if (kind === 'extra args') command.args.values = {};
    if (kind === 'mixed batch') commands.push(patch());
    expect(isTrackHistoryBatch(commands)).toBe(false);
    expect(trackHistoryInverse(commands, receipt([orderWrite()]))).toBeUndefined();
  });
  it('preserves track creation history and rejects malformed or mixed order inverses', () => {
    const id = 'parent/track:new'; const track = { id: 'new', kind: 'audio' };
    const command: EditCommand = { op: 'timeline.add', select: id, args: { track }, created: [id], expect: { [`${id}::`]: { state: 'absent' } } };
    expect(isTrackHistoryInverse(trackHistoryInverse([command], receipt([{ id, path: '', before: { state: 'absent' }, after: { state: 'present', value: track } }]))!)).toBe(true);
    const inverse = trackHistoryInverse([reorder()], receipt([orderWrite()]))!;
    expect(trackHistoryInverse([inverse], receipt([orderWrite()]))).toBeUndefined();
    for (const writes of [[...inverse.args.writes, write()], [{ ...orderWrite(), after: { state: 'present', value: ['parent/track:OTHER'] } }]]) {
      expect(isTrackHistoryInverse({ ...inverse, args: { ...inverse.args, writes } })).toBe(false);
    }
  });
});
