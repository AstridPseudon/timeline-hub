import { describe, expect, it } from 'vitest';
import type { EditCommand } from '@/integrations/runtime/generated.ts';
import { isOverlapTrimBatch, isOverlapTrimInverse, overlapTrimInverse } from './overlapTrimHistory.ts';

const primary = 'parent/clip:primary';
const dependent = 'parent/clip:dependent';
const pair = (): EditCommand[] => [
  { op: 'clip.trim', select: primary, resolved: [primary], args: { in_s: 1, out_s: 6 } },
  { op: 'clip.nudge', select: primary, resolved: [primary], args: { frames: -15,
    relation_choices: [{ target: dependent, edge: 'start', choice: 'detach' }] } },
];
const present = (value: unknown) => ({ state: 'present', value });
const writes = () => [
  { id: primary, path: 'from', before: present(2), after: present(1) },
  { id: primary, path: 'at', before: present(2), after: present(1.5) },
  { id: primary, path: 'hold', before: { state: 'absent' }, after: present(2.5) },
  { id: dependent, path: 'intent.on', before: present(`clip-start "${primary}" -1s`), after: { state: 'absent' } },
  { id: dependent, path: 'intent.fixed_start', before: { state: 'absent' }, after: present(true) },
];
const receipt = (direct_writes = writes()) => ({ status: 'accepted', accepted_publication_id: 'publication', change: { direct_writes } });

describe('bounded overlap resize history', () => {
  const multi = () => {
    const commands = pair();
    (commands[1].args.relation_choices as unknown[]).push({ target: 'parent/clip:second', edge: 'start', choice: 'detach' });
    return commands;
  };
  const multiWrites = () => [...writes(),
    { id: 'parent/clip:second', path: 'intent.on', before: present(`clip-start "${primary}" -0.75s +0f`), after: { state: 'absent' } },
    { id: 'parent/clip:second', path: 'intent.fixed_start', before: { state: 'absent' }, after: present(true) },
    { id: 'parent/clip:second', path: 'at', before: present(1.25), after: present(1) },
  ];
  it('owns multiple exact source targets and their real inverse/redo fields', () => {
    expect(isOverlapTrimBatch(multi())).toBe(true);
    const inverse = overlapTrimInverse(multi(), receipt(multiWrites()))!;
    expect(isOverlapTrimInverse(inverse)).toBe(true);
    expect(overlapTrimInverse([inverse], receipt(inverse.args.writes as ReturnType<typeof writes>))?.args.writes).toEqual(multiWrites());
  });
  it.each(['empty', 'duplicate', 'primary', 'foreign owner', 'unscoped', 'end', 'unknown choice'])('refuses multi choice %s', (kind) => {
    const commands = multi(); const choices = commands[1].args.relation_choices as Array<Record<string, unknown>>;
    if (kind === 'empty') choices.length = 0;
    if (kind === 'duplicate') choices[1].target = dependent;
    if (kind === 'primary') choices[1].target = primary;
    if (kind === 'foreign owner') choices[1].target = 'occurrence:other/clip:second';
    if (kind === 'unscoped') choices[1].target = 'second';
    if (kind === 'end') choices[1].edge = 'end';
    if (kind === 'unknown choice') choices[1].choice = 'move';
    expect(isOverlapTrimBatch(commands)).toBe(false);
    expect(overlapTrimInverse(commands, receipt(multiWrites()))).toBeUndefined();
  });
  it.each(['unchosen same owner', 'foreign owner', 'second primary', 'primary relation', 'dependent hold', 'duplicate', 'document', 'consequence'])('rejects multi inverse %s', (kind) => {
    const direct = multiWrites();
    if (kind === 'unchosen same owner') direct[5].id = 'parent/clip:unchosen';
    if (kind === 'foreign owner') direct[5].id = 'occurrence:other/clip:second';
    if (kind === 'second primary') direct[5].path = 'from';
    if (kind === 'primary relation') direct[5].id = primary;
    if (kind === 'dependent hold') direct[5].path = 'hold';
    if (kind === 'duplicate') direct.push(structuredClone(direct[5]));
    if (kind === 'document') direct[5].path = '';
    if (kind === 'consequence') direct[5] = { ...direct[5], cause: 0 } as never;
    expect(overlapTrimInverse(multi(), receipt(direct))).toBeUndefined();
  });
  it('does not let inverse replay acquire a new dependent identity', () => {
    const inverse = overlapTrimInverse(multi(), receipt(multiWrites()))!;
    const direct = structuredClone(inverse.args.writes) as ReturnType<typeof writes>;
    direct[5].id = 'parent/clip:unchosen';
    expect(overlapTrimInverse([inverse], receipt(direct))).toBeUndefined();
  });
  it.each(['promote dependent', 'new dependent field'])('does not let left inverse replay %s', (kind) => {
    const inverse = overlapTrimInverse(multi(), receipt(multiWrites()))!;
    const direct = structuredClone(inverse.args.writes) as ReturnType<typeof writes>;
    if (kind === 'promote dependent') {
      direct.slice(0, 3).forEach((write) => { write.id = dependent; });
      direct.splice(3, 2); // Leave a structurally valid inverse with a different primary.
    } else direct[3].path = 'at';
    expect(isOverlapTrimInverse({ op: 'timeline.inverse', select: null, args: { publication: 'p', writes: direct } })).toBe(true);
    expect(overlapTrimInverse([inverse], receipt(direct))).toBeUndefined();
  });
  it('accepts only the ordered pair and reverses the actual direct writes', () => {
    expect(isOverlapTrimBatch(pair())).toBe(true);
    const inverse = overlapTrimInverse(pair(), receipt())!;
    expect(isOverlapTrimInverse(inverse)).toBe(true);
    expect(inverse.args.writes).toEqual(writes().map((write) => ({ ...write, before: write.after, after: write.before })));
    expect(overlapTrimInverse([inverse], receipt(inverse.args.writes as ReturnType<typeof writes>))?.args.writes).toEqual(writes());
  });
  it.each(['reversed', 'third command', 'seconds', 'foreign primary', 'foreign dependent', 'extra trim argument', 'end choice'])(
    'does not take history ownership for %s', (kind) => {
      const commands = pair();
      if (kind === 'reversed') commands.reverse();
      if (kind === 'third command') commands.push(commands[0]);
      if (kind === 'seconds') commands[1].args = { seconds: -0.5, relation_choices: commands[1].args.relation_choices };
      if (kind === 'foreign primary') commands[1].select = dependent;
      if (kind === 'foreign dependent') (commands[1].args.relation_choices as Array<{ target: string }>)[0].target = 'occurrence:other/clip:dependent';
      if (kind === 'extra trim argument') commands[0].args.speed = 2;
      if (kind === 'end choice') (commands[1].args.relation_choices as Array<{ edge: string }>)[0].edge = 'end';
      expect(isOverlapTrimBatch(commands)).toBe(false);
      expect(overlapTrimInverse(commands, receipt())).toBeUndefined();
    },
  );
  it.each(['foreign id', 'foreign field', 'wrong from owner', 'duplicate', 'malformed state', 'consequence', 'missing from'])(
    'rejects an accepted receipt with %s', (kind) => {
      const direct = writes();
      if (kind === 'foreign id') direct[0].id = 'parent/clip:foreign';
      if (kind === 'foreign field') direct[0].path = 'speed';
      if (kind === 'wrong from owner') direct[0].id = dependent;
      if (kind === 'duplicate') direct.push(direct[0]);
      if (kind === 'malformed state') direct[0].before = { state: 'absent', value: 2 };
      if (kind === 'consequence') direct[0] = { ...direct[0], cause: 0 } as never;
      if (kind === 'missing from') direct.shift();
      expect(overlapTrimInverse(pair(), receipt(direct))).toBeUndefined();
    },
  );
});


describe('multiple right overlap trim history', () => {
  const batch = (): EditCommand[] => [{ op: 'clip.trim', select: primary, resolved: [primary], args: { out_s: 3,
    relation_choices: [dependent, 'parent/clip:second', 'parent/clip:third'].map((target) => ({ target, edge: 'start', choice: 'detach' })) } }];
  const direct = () => [
    { id: primary, path: 'to', before: present(2), after: present(3) },
    { id: primary, path: 'hold', before: { state: 'absent' }, after: present(3) },
    ...[dependent, 'parent/clip:second', 'parent/clip:third'].flatMap((id) => [
      { id, path: 'intent.on', before: present(`clip-end "${primary}" +1s`), after: { state: 'absent' } },
      { id, path: 'intent.fixed_start', before: { state: 'absent' }, after: present(true) },
    ]),
  ];
  it('owns one exact trim and its multi-dependent accepted inverse and redo', () => {
    expect(isOverlapTrimBatch(batch())).toBe(true);
    const inverse = overlapTrimInverse(batch(), receipt(direct()))!;
    expect(isOverlapTrimInverse(inverse)).toBe(true);
    expect(inverse.args.writes).toEqual(direct().map((write) => ({ ...write, before: write.after, after: write.before })));
    expect(overlapTrimInverse([inverse], receipt(inverse.args.writes as ReturnType<typeof writes>))?.args.writes).toEqual(direct());
    expect(overlapTrimInverse(batch(), { ...receipt(), status: 'no_change' })).toBeNull();
    expect(overlapTrimInverse(batch(), { ...receipt(), status: 'refused' })).toBeUndefined();
  });
  it.each(['empty', 'duplicate', 'primary', 'foreign', 'unscoped', 'end', 'unknown', 'extra choice', 'missing offset', 'fractional frames', 'missing anchor', 'extra trim', 'nudge', 'unresolved'])(
    'refuses malformed right batch %s', (kind) => {
      const commands = batch(); const choices = commands[0].args.relation_choices as Array<Record<string, unknown>>;
      if (kind === 'empty') choices.length = 0;
      if (kind === 'duplicate') choices[1].target = dependent;
      if (kind === 'primary') choices[1].target = primary;
      if (kind === 'foreign') choices[1].target = 'occurrence:other/clip:second';
      if (kind === 'unscoped') choices[1].target = 'second';
      if (kind === 'end') choices[1].edge = 'end';
      if (kind === 'unknown') choices[1].choice = 'move';
      if (kind === 'extra choice') choices[1].relation_affected = [];
      if (kind === 'missing offset') choices[1].choice = 'adjust-offset';
      if (kind === 'fractional frames') Object.assign(choices[1], { choice: 'adjust-offset', offset_seconds: 0, offset_frames: 0.5 });
      if (kind === 'missing anchor') Object.assign(choices[1], { choice: 're-anchor', offset_seconds: 0, offset_frames: 0 });
      if (kind === 'extra trim') commands[0].args.in_s = 0;
      if (kind === 'nudge') commands.push(pair()[1]);
      if (kind === 'unresolved') commands[0].resolved = [dependent];
      expect(isOverlapTrimBatch(commands)).toBe(false);
      expect(overlapTrimInverse(commands, receipt(direct()))).toBeUndefined();
    });
  it.each(['unchosen', 'foreign', 'dependent to', 'dependent hold', 'primary at', 'duplicate', 'document', 'consequence', 'generic diff', 'malformed state', 'missing to'])(
    'rejects right receipt %s', (kind) => {
      const rows = direct();
      if (kind === 'unchosen') rows[4].id = 'parent/clip:unchosen';
      if (kind === 'foreign') rows[4].id = 'occurrence:other/clip:second';
      if (kind === 'dependent to') rows[4].path = 'to';
      if (kind === 'dependent hold') rows[4].path = 'hold';
      if (kind === 'primary at') rows[1].path = 'at';
      if (kind === 'duplicate') rows.push(structuredClone(rows[4]));
      if (kind === 'document') rows[4].path = '';
      if (kind === 'consequence') rows[4] = { ...rows[4], cause: 0 } as never;
      if (kind === 'generic diff') rows[4].path = 'app.opaque';
      if (kind === 'malformed state') rows[4].before = { state: 'absent', value: 1 };
      if (kind === 'missing to') rows.shift();
      expect(overlapTrimInverse(batch(), receipt(rows))).toBeUndefined();
    });
  it.each(['new id', 'new field', 'promote dependent'])('inverse replay cannot acquire %s', (kind) => {
    const inverse = overlapTrimInverse(batch(), receipt(direct()))!;
    const rows = structuredClone(inverse.args.writes) as ReturnType<typeof writes>;
    if (kind === 'new id') rows[4].id = 'parent/clip:unchosen';
    if (kind === 'new field') rows[4].path = 'at';
    if (kind === 'promote dependent') { rows[0].id = dependent; rows[1].id = dependent; rows.splice(2, 2); }
    expect(overlapTrimInverse([inverse], receipt(rows))).toBeUndefined();
  });
});
