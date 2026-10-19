import { describe, expect, it } from 'vitest';
import type { CommandRecord, EditCommand } from '@/integrations/runtime/timeline-commit-types.ts';
import { captureClipMove, executeClipMove, finishClipMove } from './clipMoveCapture.ts';
import type { AuthoredBundle, ClipMoveBasis } from './clipMoveCapture.ts';
import { AuthoredState } from './clipMovePrimitives.ts';
import fixture from './fixtures/recipe_m1_move.json';

/* Inputs: Agent tests/editing_conformance/fixtures/recipe_m1_{move,occurrence}.json,
 * plus sequential/container/shared-materialization cases using its real authored bundle.
 * Regenerate all expected outputs from the committed inputs, from App's root:
 * PYTHONPATH=/home/user/work/wt/agt-m1-core /home/user/work/venv-agent/bin/python - <<'PY'
 * import json
 * from pathlib import Path
 * from astrid.sdk.timeline.capture import capture_move
 * from astrid.sdk.timeline.commands import execute
 * p = Path('src/tools/video-editor/commands/fixtures/recipe_m1_move.json')
 * data = json.loads(p.read_text())
 * for f in [data, *data['cases']]:
 *     f['command'] = capture_move(f['bundle'], f['select'], f['on'])
 *     plan = execute(f['bundle'], [f['command']])
 *     f['after_bundle'], f['record'] = plan.bundle, plan.records[0]
 * p.write_text(json.dumps(data, separators=(',', ':'), ensure_ascii=False, allow_nan=False) + '\n')
 * PY
 */
type Golden = {
  name: string;
  bundle: AuthoredBundle;
  select: string;
  on: number;
  command: EditCommand;
  after_bundle: AuthoredBundle;
  record: CommandRecord;
};
const goldens = [fixture, ...fixture.cases] as unknown as Golden[];
const named = (name: string) => goldens.find((golden) => golden.name === name)!;
const detached = <T>(value: T): T => structuredClone(value);
const clip = (bundle: AuthoredBundle, ref: string = fixture.select) => new AuthoredState(bundle).entity(ref)!;

describe('Agent built-in clip.move capture parity', () => {
  for (const golden of goldens) {
    it(`matches exact command, authored bundle and recorder: ${golden.name}`, () => {
      const input = detached(golden.bundle);
      const basis = captureClipMove(input, golden.select);
      const result = finishClipMove(basis, golden.on);
      expect(result.command).toEqual(golden.command);
      expect(result.bundle).toEqual(golden.after_bundle);
      expect(result.record).toEqual(golden.record);
      expect(input).toEqual(golden.bundle);
      expect(executeClipMove(input, golden.command)).toEqual(result);
    });
  }

  it('captures before preview and keeps the original basis across repeated finish and input mutation', () => {
    const input = detached(fixture.bundle) as AuthoredBundle;
    const basis = captureClipMove(input, fixture.select);
    const preview = finishClipMove(basis, 5);
    clip(input).at = 999;
    clip(preview.bundle).at = 999;
    preview.command.reads!.length = 0;
    const drop = finishClipMove(basis, fixture.on);
    expect(drop.command).toEqual(fixture.command);
    expect(drop.bundle).toEqual(fixture.after_bundle);
    expect(() => finishClipMove({} as ClipMoveBasis, 4)).toThrow('unknown clip move basis');
  });

  it('captures unacknowledged B7 from the authored A5 result, with A5 guards intact', () => {
    const aGolden = named('sequential_A5');
    const a = finishClipMove(captureClipMove(aGolden.bundle, aGolden.select), 5);
    const b = finishClipMove(captureClipMove(a.bundle, aGolden.select), 7);
    expect(b.command).toEqual(named('sequential_B7').command);
    expect(b.bundle).toEqual(named('sequential_B7').after_bundle);
    expect(b.command.expect![`${aGolden.select}::at`]).toEqual({ state: 'present', value: 5 });
    expect(b.command.expect![`${aGolden.select}::app.astrid.on`]).toEqual({ state: 'absent' });
    expect(clip(b.bundle, aGolden.select).at).toBe(7);
    expect(() => executeClipMove(aGolden.bundle, b.command)).toThrow('original capture');
  });

  it('keeps unchanged writes and absent clears while preserving opaque app fields', () => {
    const golden = named('same_value');
    const result = finishClipMove(captureClipMove(golden.bundle, golden.select), golden.on);
    expect(result.bundle).toEqual(golden.bundle);
    expect(result.record.writes).toContainEqual({ ref: golden.select, path: ['at'],
      before: { state: 'present', value: 5 }, after: { state: 'present', value: 5 } });
    expect(result.record.writes).toContainEqual({ ref: golden.select, path: ['app', 'on'],
      before: { state: 'absent' }, after: { state: 'absent' } });
    expect(clip(result.bundle).app).toMatchObject({ opaque: { keep: true }, astrid: { fixed_start: true, for: 2 } });
  });

  it('isolates repeated shared children and retains semantic guards across first materialization', () => {
    const aGolden = named('repeated_shared_A');
    const a = finishClipMove(captureClipMove(aGolden.bundle, aGolden.select), aGolden.on);
    const sibling = 'occurrence:o2/clip:c';
    expect(clip(a.bundle, sibling)).toEqual(clip(aGolden.bundle, sibling));
    const b = finishClipMove(captureClipMove(a.bundle, aGolden.select), 14);
    const materialized = named('disjoint_same_child_first_materialization_B');
    expect(b.command).toEqual(materialized.command);
    const applied = executeClipMove(materialized.bundle, b.command);
    expect(applied.bundle).toEqual(materialized.after_bundle);
    expect(clip(applied.bundle, aGolden.select).opaque_disjoint).toEqual({ keep: true });
    expect(applied.record.dependencies.find((dependency) => dependency.key === 'move.images'))
      .not.toEqual(b.record.dependencies.find((dependency) => dependency.key === 'move.images'));
    expect(b.command.reads!.some((read) => read.path.some((key) => key.includes('revision') || key.includes('digest')))).toBe(false);
  });

  it('distinguishes absent/null and boolean/number guards', () => {
    const golden = named('sequential_B7');
    const changed = detached(golden.bundle);
    (clip(changed).app as Record<string, unknown>).on = null;
    expect(() => executeClipMove(changed, golden.command)).toThrow('original capture');
    const forged = detached(golden.command);
    forged.expect![`${golden.select}::app.astrid.fixed_start`] = { state: 'present', value: 1 };
    expect(() => executeClipMove(golden.bundle, forged)).toThrow('original capture');
  });

  it.each([
    ['negative', -1], ['nan', NaN], ['infinite', Infinity], ['boolean', true],
  ])('refuses invalid target %s', (_label, on) => {
    expect(() => finishClipMove(captureClipMove(fixture.bundle as AuthoredBundle, fixture.select), on as number)).toThrow();
  });

  it.each([
    ['speed', 0], ['speed', -1], ['speed', { numerator: 1, denominator: 1 }],
    ['time_map', {}], ['timeMap', {}], ['children', []], ['clips', []],
    ['from_ms', 0], ['to_ms', 1000], ['duration', 99], ['at_ms', 99999],
  ])('refuses unsupported clip timing %s=%j', (key, value) => {
    const input = detached(fixture.bundle) as AuthoredBundle;
    clip(input)[key] = value;
    expect(() => captureClipMove(input, fixture.select)).toThrow();
  });

  it.each(['sequence', 'sequence_index', 'sequence_fit', 'formulas'])('refuses %s timing', (key) => {
    const input = detached(fixture.bundle) as AuthoredBundle;
    (clip(input).app as Record<string, unknown>)[key] = 'unsupported';
    expect(() => captureClipMove(input, fixture.select)).toThrow();
  });

  it.each([
    ['source_offset', 1], ['source_offset', { start: 0 }], ['speed', true],
    ['speed', 2], ['speed', { numerator: 1, denominator: 1 }], ['time_map', {}],
  ])('refuses unsupported occurrence mapping %s=%j', (key, value) => {
    const golden = named('repeated_shared_A');
    const input = detached(golden.bundle);
    input.placements[0][key] = value;
    expect(() => captureClipMove(input, golden.select)).toThrow('translation-only');
  });

  it('refuses intervals before the occurrence or crossing its next blocker, with a half-open end', () => {
    const golden = named('repeated_shared_A');
    const input = detached(golden.bundle);
    input.parent.config = { ...(input.parent.config as Record<string, never>), output: { fps: 30 } };
    const basis = captureClipMove(input, golden.select);
    expect(() => finishClipMove(basis, 9)).toThrow('precedes');
    expect(() => finishClipMove(basis, 18.1)).toThrow('crosses');
    expect(() => finishClipMove(basis, 20)).toThrow('crosses');
    expect(finishClipMove(basis, 18).previewAt).toBe(18);
  });

  it('refuses missing/ambiguous stable identities and never interprets projected IDs', () => {
    for (const ref of ['parent/clip:missing', 'o:c', 'shot:s/clip:c']) {
      expect(() => captureClipMove(fixture.bundle as AuthoredBundle, ref)).toThrow();
    }
    const input = detached(fixture.bundle) as AuthoredBundle;
    (input.parent.clips as unknown[]).push(detached(clip(input)));
    expect(() => captureClipMove(input, fixture.select)).toThrow('ambiguous');
  });

  it('rejects changed source/rate/owner/selection and forged incomplete claims', () => {
    const golden = named('repeated_shared_A');
    const command = golden.command;
    for (const change of ['rate', 'owner', 'blocker', 'order', 'source']) {
      const input = detached(golden.bundle);
      if (change === 'rate') (input.parent.config as Record<string, unknown>).output = { fps: 25 };
      if (change === 'owner') input.placements[0].shot_id = input.placements[1].shot_id;
      if (change === 'blocker') input.placements.push({ ...detached(input.placements[1]), occurrence_id: 'new' });
      if (change === 'order') input.placements.reverse();
      if (change === 'source') clip(input, golden.select).asset = 'other-source';
      expect(() => executeClipMove(input, command), change).toThrow();
    }
    expect(() => executeClipMove(golden.bundle, { ...command, reads: [] })).toThrow('original capture');
  });

  it('guards consumed media identity while retaining revision-image pins only as provenance', () => {
    const golden = named('registry_source');
    const changed = detached(golden.bundle);
    const registry = changed.parent.registry as { assets: { source: { media_id: string } } };
    registry.assets.source.media_id = 'sha256:other';
    expect(() => executeClipMove(changed, golden.command)).toThrow('original capture');
    const disjoint = detached(golden.bundle);
    disjoint.base_parent = { revision_id: 'new-parent', content_digest: 'sha256:new-image' };
    expect(executeClipMove(disjoint, golden.command).command).toEqual(golden.command);
  });

  it('preserves a legacy config clip collection when parent clips are authoritative', () => {
    const input = detached(fixture.bundle) as AuthoredBundle;
    (input.parent.config as Record<string, unknown>).clips = [{ id: 'legacy', at: 88 }];
    const result = finishClipMove(captureClipMove(input, fixture.select), 4);
    expect((result.bundle.parent.config as Record<string, unknown>).clips).toEqual([{ id: 'legacy', at: 88 }]);
  });

  it('fails closed on clipped negative starts, contradictory occurrence codecs and unequal child fps', () => {
    const golden = named('repeated_shared_A');
    const input = detached(golden.bundle);
    clip(input, golden.select).at = -0.001;
    expect(() => captureClipMove(input, golden.select)).toThrow();
    const codecs = detached(golden.bundle);
    codecs.placements[0].at_ms = 10001;
    expect(() => captureClipMove(codecs, golden.select)).toThrow('contradictory occurrence');
    const rate = detached(golden.bundle);
    new AuthoredState(rate).config('occurrence:o').output = { fps: 25 };
    expect(() => captureClipMove(rate, golden.select)).toThrow('parent and child fps differ');
  });
});
