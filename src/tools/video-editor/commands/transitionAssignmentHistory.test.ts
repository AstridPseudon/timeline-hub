import { describe, expect, it } from 'vitest';
import type { EditCommand } from '@/integrations/runtime/generated.ts';
import { isTransitionAssignmentBatch, isTransitionAssignmentInverse, transitionAssignmentInverse } from './transitionAssignmentHistory.ts';

const absent = { state: 'absent' as const };
const present = (value: unknown) => ({ state: 'present' as const, value });
const reference = { id: 'fade', revision: 'sha256:pinned', kind: 'transition', packId: 'rendering', opaque: { keep: null } };
const transition = { type: 'fade', revision: reference.revision, duration: 0.731, params: null, opaque: { retained: true } };
const assignment = (id = 'after'): EditCommand => structuredClone({
  op: 'clip.set-transition', select: `parent/clip:${id}`, resolved: [`parent/clip:${id}`],
  args: { transition, elementRef: reference, from_clip: 'parent/clip:before' },
  expect: { transition: absent, elementRef: absent },
});
const writes = (call = assignment()) => ['elementRef', 'transition'].filter(path => JSON.stringify(call.expect![path]) !== JSON.stringify(present(call.args[path])))
  .map(path => ({ id: call.select!, path, before: structuredClone(call.expect![path]), after: present(structuredClone(call.args[path])) }));
const receipt = (direct = writes()) => ({ status: 'accepted', accepted_publication_id: 'accepted-pub', change: { direct_writes: direct } });

describe('W29 transition assignment receipt adapter', () => {
  it('rejects malformed command objects without throwing', () => {
    for (const call of [null, {}, { op: 'clip.set-transition' }]) {
      expect(isTransitionAssignmentBatch([call as EditCommand])).toBe(false);
      expect(transitionAssignmentInverse([call as EditCommand], receipt())).toBeUndefined();
    }
  });
  it('copies only accepted tagged values and the accepted publication without mutating input', () => {
    const call = assignment(); const result = receipt(); const original = structuredClone(result);
    const inverse = transitionAssignmentInverse([call], result)!;
    expect(isTransitionAssignmentBatch([call])).toBe(true);
    expect(isTransitionAssignmentInverse(inverse)).toBe(true);
    expect(inverse).toEqual({ op: 'timeline.inverse', select: null, args: { publication: 'accepted-pub',
      writes: result.change.direct_writes.map(row => ({ ...row, before: row.after, after: row.before })) } });
    (inverse.args.writes as typeof result.change.direct_writes)[0].before = absent;
    expect(result).toEqual(original);
  });
  it.each([undefined, null, {}])('retains params %j and opaque siblings on a captured update', params => {
    const call = assignment(); delete call.args.from_clip;
    const prior = { ...transition, duration: 0.5, ...(params === undefined ? {} : { params }) };
    if (params === undefined) delete (prior as Partial<typeof transition>).params;
    call.args.transition = { ...prior, duration: 0.731 };
    call.expect = { transition: present(prior), elementRef: present(structuredClone(reference)) };
    const result = receipt(writes(call));
    expect(result.change.direct_writes.map(row => row.path)).toEqual(['transition']);
    expect(isTransitionAssignmentBatch([call])).toBe(true);
    expect(transitionAssignmentInverse([call], result)?.args.writes).toEqual([{ id: call.select, path: 'transition',
      before: present(call.args.transition), after: present(prior) }]);
  });
  it('retains present-null separately from absence in a two-clip transaction', () => {
    const calls = [assignment('second'), assignment('first')];
    calls[0].expect = { transition: present(null), elementRef: present(null) };
    const result = receipt(calls.flatMap(call => writes(call)));
    const inverse = transitionAssignmentInverse(calls, result)!;
    expect((inverse.args.writes as { id: string }[]).map(row => row.id)).toEqual([
      'parent/clip:second', 'parent/clip:second', 'parent/clip:first', 'parent/clip:first',
    ]);
    expect(transitionAssignmentInverse([inverse], { ...receipt(), accepted_publication_id: 'undo-pub',
      change: { direct_writes: structuredClone(inverse.args.writes) as never } })?.args.writes).toEqual(result.change.direct_writes);
  });
  it.each(['missing', 'extra', 'wrong-id', 'wrong-path', 'duplicate', 'wrong-before', 'wrong-after', 'bad-tag', 'extra-tag', 'extra-write-key'])(
    'rejects %s direct receipt closure', kind => {
      const direct: Array<Record<string, unknown>> = structuredClone(writes());
      if (kind === 'missing') direct.pop();
      if (kind === 'extra') direct.push({ ...direct[0], id: 'parent/clip:foreign' });
      if (kind === 'wrong-id') direct[0].id = 'parent/clip:foreign';
      if (kind === 'wrong-path') direct[0].path = 'params';
      if (kind === 'duplicate') direct.push(direct[0]);
      if (kind === 'wrong-before') direct[0].before = present(null);
      if (kind === 'wrong-after') direct[0].after = present({ ...reference, revision: 'wrong' });
      if (kind === 'bad-tag') direct[0].before = { state: 'missing' };
      if (kind === 'extra-tag') direct[0].before = { state: 'absent', value: null };
      if (kind === 'extra-write-key') direct[0].cause = 'invented';
      expect(transitionAssignmentInverse([assignment()], receipt(direct as never))).toBeUndefined();
    });
  it('rejects a partial bulk receipt atomically and refuses duplicate targets', () => {
    const calls = [assignment('second'), assignment('first')];
    expect(transitionAssignmentInverse(calls, receipt(writes(calls[0])))).toBeUndefined();
    expect(isTransitionAssignmentBatch([calls[0], calls[0]])).toBe(false);
  });
  it.each(['clear', 'null', 'occurrence', 'unresolved', 'extra-arg', 'wrong-binding', 'unbound-update', 'bad-expect'])(
    'keeps %s outside this adapter', kind => {
      const call = assignment();
      if (kind === 'clear') call.args = { clear: true };
      if (kind === 'null') call.args = { transition: null };
      if (kind === 'occurrence') call.select = call.resolved![0] = 'occurrence:a/clip:after';
      if (kind === 'unresolved') call.resolved = [];
      if (kind === 'extra-arg') call.args.duration_frames = 10;
      if (kind === 'wrong-binding') call.args.elementRef = { ...reference, revision: 'stale' };
      if (kind === 'unbound-update') delete call.args.from_clip;
      if (kind === 'bad-expect') delete call.expect!.elementRef;
      expect(isTransitionAssignmentBatch([call])).toBe(false);
      expect(transitionAssignmentInverse([call], receipt())).toBeUndefined();
    });
  it('closes every absent after-state for a captured clear and restores exact null/absent siblings', () => {
    const calls = [assignment('second'), assignment('first')];
    for (const [index, call] of calls.entries()) {
      const prior = { ...transition } as Record<string, unknown>;
      if (index) delete prior.params;
      call.args = { clear: true };
      call.expect = { transition: present(prior), elementRef: present(structuredClone(reference)) };
    }
    const direct = calls.flatMap(call => ['transition', 'elementRef'].map(path => ({
      id: call.select!, path, before: structuredClone(call.expect![path]), after: absent,
    })));
    expect(isTransitionAssignmentBatch(calls)).toBe(true);
    const inverse = transitionAssignmentInverse(calls, receipt(direct))!;
    expect(isTransitionAssignmentInverse(inverse)).toBe(true);
    expect(inverse.args.writes).toEqual(direct.map(row => ({ ...row, before: absent, after: row.before })));
    expect(transitionAssignmentInverse([inverse], { ...receipt(), accepted_publication_id: 'undo-pub',
      change: { direct_writes: structuredClone(inverse.args.writes) as never } })?.args.writes).toEqual(direct);
    expect(transitionAssignmentInverse(calls, receipt(direct.slice(0, 3)))).toBeUndefined();
    expect(transitionAssignmentInverse(calls, receipt(direct.map(row => ({ ...row, after: present(null) }))))).toBeUndefined();
    const mixed = [calls[0], assignment('other')];
    expect(isTransitionAssignmentBatch(mixed)).toBe(false);
    calls[1].expect!.elementRef = present({ ...reference, revision: 'stale' });
    expect(isTransitionAssignmentBatch(calls)).toBe(false);
  });
  it.each(['refused', 'conflict', 'error', 'preview'])('does not create an inverse for %s', status => {
    expect(transitionAssignmentInverse([assignment()], { ...receipt(), status })).toBeUndefined();
  });
  it('no-change and missing publication produce no usable inverse', () => {
    expect(transitionAssignmentInverse([assignment()], { ...receipt(), status: 'no_change' })).toBeNull();
    expect(transitionAssignmentInverse([assignment()], { ...receipt(), accepted_publication_id: null })).toBeUndefined();
    expect(transitionAssignmentInverse([assignment()], receipt([]))).toBeUndefined();
  });
  it('inverse acknowledgements require exact source writes and a new publication', () => {
    const inverse = transitionAssignmentInverse([assignment()], receipt())!;
    const direct = inverse.args.writes as ReturnType<typeof writes>;
    expect(transitionAssignmentInverse([inverse], { ...receipt(direct), accepted_publication_id: 'accepted-pub' })).toBeUndefined();
    expect(transitionAssignmentInverse([inverse], { ...receipt(direct.slice(0, 1)), accepted_publication_id: 'new-pub' })).toBeUndefined();
    expect(transitionAssignmentInverse([inverse], { ...receipt(direct.map(row => ({ ...row, after: present(null) }))), accepted_publication_id: 'new-pub' })).toBeUndefined();
  });
});
