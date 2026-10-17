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
