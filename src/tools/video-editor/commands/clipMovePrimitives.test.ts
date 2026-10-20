import { describe, expect, it } from 'vitest';
import type { CommandRecord, EditCommand, JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import { captureClipMove, finishClipMove } from './clipMoveCapture.ts';
import { MoveRecording, copy } from './clipMovePrimitives.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';
import fixture from './fixtures/recipe_m2_recorder_primitives.json';

type Golden = {
  bundle: AuthoredBundle; request: EditCommand; command: EditCommand;
  record: CommandRecord; after_bundle: AuthoredBundle;
};
const moves = fixture.moves as unknown as (Golden & { name: string })[];
const label = fixture.label as unknown as Golden;
const command: EditCommand = { schema_version: 1, op: 'clip.move', version: '1',
  select: 'parent/clip:c', args: { on: 4 } };

// Native _recording / _scalar_commands at e8f7c2c89; no client record is acceptance authority.
describe('shared native recording primitives', () => {
  for (const golden of fixture.selections) {
    it(`retains the native query key and membership: ${golden.key} ${golden.members}`, () => {
      const ctx = new MoveRecording(fixture.selection_bundle as AuthoredBundle, command);
      const members = copy(golden.members);
      const key = golden.key as Parameters<MoveRecording['select']>[0];
      expect(ctx.select(key, golden.owner, members)).toEqual(golden.selection.members);
      members.length = 0;
      expect(ctx.command.selections).toEqual([golden.selection]);
      expect(ctx.record.selections).toEqual([golden.selection]);
      expect(ctx.command.selections![0].key).toBe(golden.key);
    });
  }

  it.each(['media.targets', 'media.target.extra', 'move.unknown', 'collection.unknown', ''])('refuses unknown query %s', (key) => {
    const ctx = new MoveRecording(fixture.selection_bundle as AuthoredBundle, command);
    expect(() => ctx.select(key as Parameters<MoveRecording['select']>[0], 'parent', ['parent/clip:c']))
      .toThrow('unsupported recorded query');
    expect(ctx.command.selections).toEqual([]);
  });

  for (const golden of moves) {
    it(`matches native move command, record and bundle for ${golden.name} mirrors`, () => {
      const input = copy(golden.bundle);
      const result = finishClipMove(captureClipMove(input, golden.command.select!), 4);
      expect(result.command).toEqual(golden.command);
      expect(result.record).toEqual(golden.record);
      expect(result.bundle).toEqual(golden.after_bundle);
      expect(input).toEqual(golden.bundle);
      expect(result.record.derived_writes).toHaveLength(golden.name === 'equal' ? 1 : 0);
    });
  }

  it('keeps the original mirror decision when divergent arrays become equal before compile', () => {
    const golden = moves.find((item) => item.name === 'divergent')!;
    const ctx = new MoveRecording(golden.bundle, command);
    ctx.state.bundle.parent.config.clips = copy(ctx.state.bundle.parent.clips);
    ctx.write('parent/clip:c', ['at'], 4);
    const before = copy(ctx.state.bundle.parent.config.clips);
    ctx.compile();
    expect(ctx.state.bundle.parent.config.clips).toEqual(before);
    expect(ctx.record.derived_writes).toEqual([]);
  });

  it('synchronizes equal mirrors once and omits unchanged derived writes on repeated compile', () => {
    const golden = moves.find((item) => item.name === 'equal')!;
    const ctx = new MoveRecording(golden.bundle, command);
    ctx.compile();
    expect(ctx.record.derived_writes).toEqual([]);
    for (const write of golden.record.writes) ctx.assign(write.ref, write.path, write.after);
    ctx.compile();
    ctx.compile();
    expect(ctx.record.derived_writes).toEqual(golden.record.derived_writes);
    expect(ctx.state.bundle.parent.config.clips).toEqual(ctx.state.bundle.parent.clips);
  });

  it('retains the exact native track label capture command, record and bundle', () => {
    const ctx = new MoveRecording(label.bundle, { ...label.request, intent: {} });
    const ref = label.request.select!;
    ctx.read(ref, ['id']);
    ctx.dependency('scalar.images', 'entity', { parent: label.bundle.base_parent });
    ctx.bind('scalar.target', ref, ['scalar.images']);
    const values = label.request.args.values as Record<string, JSON>;
    for (const key of Object.keys(values).sort()) ctx.write(ref, [key], values[key]);
    for (const key of label.request.args.clear as string[]) ctx.clear(ref, [key]);
    ctx.compile();
    expect(ctx.command).toEqual(label.command);
    expect(ctx.record).toEqual(label.record);
    expect(ctx.state.bundle).toEqual(label.after_bundle);
  });
});
