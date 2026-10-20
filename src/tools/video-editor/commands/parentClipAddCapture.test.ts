import { describe, expect, it } from 'vitest';
import type { CommandRecord, EditCommand, JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import { captureParentClipAdd, executeParentClipAdd, finishParentClipAdd } from './parentClipAddCapture.ts';
import { AuthoredState, ClipMoveError, copy } from './clipMovePrimitives.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';
import fixture from './fixtures/recipe_m2_parent_clip_add.json';

// Native fixtures generated at Agent 0ace5c0bd; executed against frozen Agent 027bd16d
// by fixtures/parent_clip_add_parity.py (full commands, records and after-bundles).
// The first case matches its unchanged recipe_m2_clip_add.json command/record (standalone ordinal/cause 0).
type Golden = {
  name: string; bundle: AuthoredBundle; select: string; row: Record<string, JSON>;
  command: EditCommand; record: CommandRecord; after_bundle: AuthoredBundle;
};
const cases = fixture.cases as unknown as Golden[];
const named = (name: string) => cases.find((item) => item.name === name)!;
const first = named('native_first_clip');
const existing = named('ordered_append_shared_closure');
const roundtrip = <T>(value: T): T => JSON.parse(JSON.stringify(value));
const tracks = (bundle: AuthoredBundle) => (bundle.parent.config as Record<string, JSON>).tracks as Record<string, JSON>[];
const clips = (bundle: AuthoredBundle) => bundle.parent.clips as Record<string, JSON>[];

describe('native parent-only literal clip.add capture', () => {
  for (const golden of cases) {
    it(`matches exact command, record and authored after-bundle: ${golden.name}`, () => {
      const bundle = copy(golden.bundle), row = copy(golden.row);
      const basis = captureParentClipAdd(bundle, golden.select, row);
      const result = finishParentClipAdd(basis);
      expect(result).toEqual({ command: golden.command, record: golden.record, bundle: golden.after_bundle });
      expect(executeParentClipAdd(bundle, golden.command)).toEqual(result);
      expect(finishParentClipAdd(roundtrip(basis))).toEqual(result);
      expect(Object.isFrozen(basis)).toBe(true);
      expect(Object.isFrozen(basis.command.reads)).toBe(true);
      expect(Object.isFrozen(basis.bundle.parent)).toBe(true);
      expect(bundle).toEqual(golden.bundle);
      expect(row).toEqual(golden.row);
    });
  }

  for (const refusal of fixture.refusals) {
    it(`refuses atomically with the native kind: ${refusal.name}`, () => {
      const withBundle = refusal as typeof refusal & { bundle?: AuthoredBundle };
      const bundle = copy(withBundle.bundle ?? named(refusal.case).bundle);
      const before = copy(bundle);
      const command = copy(refusal.command) as EditCommand;
      expect(() => executeParentClipAdd(bundle, command)).toThrowError(ClipMoveError);
      try {
        executeParentClipAdd(bundle, command);
      } catch (error) {
        expect((error as ClipMoveError).kind).toBe(refusal.kind);
      }
      expect(bundle).toEqual(before);
      expect(command).toEqual(refusal.command);
    });
  }

  it('retains original capture, head and source closure after caller mutation and JSON reload', () => {
    const bundle = copy(existing.bundle), row = copy(existing.row);
    const basis = captureParentClipAdd(bundle, 'parent', row);
    const persisted = roundtrip(basis);
    bundle.base_parent = { revision_id: 'new-head', content_digest: 'sha256:new' };
    tracks(bundle)[0].kind = 'other';
    clips(bundle).reverse();
    bundle.source_mapping = {};
    row.id = 'fresh-retry-id';
    row.params = { text: 'changed' };
    expect(finishParentClipAdd(persisted)).toEqual(finishParentClipAdd(basis));
    expect(finishParentClipAdd(persisted).command).toEqual(existing.command);
    expect(persisted.bundle.base_parent).toEqual(existing.bundle.base_parent);
    expect(persisted.bundle.source_mapping).toEqual(existing.bundle.source_mapping);
    expect(finishParentClipAdd(persisted).command.created).toEqual(['parent/clip:first-clip']);
  });

  it('preserves literal seconds, opaque JSON, absent fields and the ordered prefix', () => {
    const result = finishParentClipAdd(captureParentClipAdd(existing.bundle, 'parent', existing.row));
    expect(clips(result.bundle)).toEqual([...clips(existing.bundle), existing.row]);
    const added = new AuthoredState(result.bundle).entity('parent/clip:first-clip')!;
    expect(added.at).toBe(0.017);
    expect(added.hold).toBe(1.013);
    expect(added.from).toBeNull();
    expect(Object.hasOwn(added, 'to')).toBe(false);
    expect(added.opaque).toEqual({ id: 'first-clip', ordered: [null, false, 0, {}, []] });
    expect(result.command.reads!.some((read) => read.path.includes('fps'))).toBe(false);
    expect(result.command.reads!.some((read) => read.ref === 'parent/clip:clip-a')).toBe(false);
    expect(result.bundle.shots).toEqual(existing.bundle.shots);
    expect(result.bundle.placements).toEqual(existing.bundle.placements);
    expect(result.bundle.source_mapping).toEqual(existing.bundle.source_mapping);
    expect(result.bundle.parent.registry).toEqual(existing.bundle.parent.registry);
  });

  it('synchronizes both empty and nonempty equal mirrors with a derived write', () => {
    for (const golden of [first, existing]) {
      const result = executeParentClipAdd(golden.bundle, golden.command);
      expect((result.bundle.parent.config as Record<string, JSON>).clips).toEqual(result.bundle.parent.clips);
      expect(result.record.derived_writes).toEqual([{ ref: 'parent', path: ['config', 'clips'],
        before: { state: 'present', value: clips(golden.bundle) },
        after: { state: 'present', value: clips(result.bundle) }, cause: 0 }]);
    }
  });

  it('does not materialize absent or null secondary clip codecs', () => {
    for (const name of ['absent_payload', 'null_payload', 'absent_mirror', 'null_mirror']) {
      const golden = named(name), result = executeParentClipAdd(golden.bundle, golden.command);
      expect(result.record.derived_writes).toEqual([]);
      const parent = result.bundle.parent, config = parent.config as Record<string, JSON>;
      const target = name.endsWith('payload') ? parent : config;
      expect(Object.hasOwn(target, 'clips')).toBe(!name.startsWith('absent'));
      if (name.startsWith('null')) expect(target.clips).toBeNull();
    }
  });

  it('retains source and transcript dependency pins exactly without claiming media authority', () => {
    for (const name of ['retained_media.transcript', 'retained_config']) {
      const golden = named(name), result = executeParentClipAdd(golden.bundle, golden.command);
      expect(result.record.dependencies).toEqual(golden.record.dependencies);
      expect(result.record.dependencies).toHaveLength(1);
      expect(result.record.dependencies[0].key).toMatch(/^compile.document:sha256:/);
      expect(result.bundle.source_mapping).toEqual(golden.bundle.source_mapping);
    }
  });

  it('uses the same created identity on exact retries and records only the next explicit creation', () => {
    const basis = captureParentClipAdd(first.bundle, 'parent', first.row);
    const a = finishParentClipAdd(basis);
    expect(finishParentClipAdd(roundtrip(basis))).toEqual(a);
    expect(() => executeParentClipAdd(a.bundle, a.command)).toThrow('occupied');
    const b = finishParentClipAdd(captureParentClipAdd(a.bundle, 'parent', { ...first.row, id: 'second-clip' }));
    expect(b.command.created).toEqual(['parent/clip:second-clip']);
    expect(b.command.expect).toEqual({ 'parent/clip:second-clip::': { state: 'absent' } });
    expect(b.command.selections![0].order).toEqual(['parent/clip:first-clip']);
    expect(clips(b.bundle).map((row) => row.id)).toEqual(['first-clip', 'second-clip']);
    expect(a.command).toEqual(first.command);
  });

  it('allows unrelated row-value and revision-image changes while keeping the original claims', () => {
    const head = copy(existing.bundle);
    clips(head)[0].opaque_disjoint = [null, false];
    ((head.parent.config as Record<string, JSON>).clips as Record<string, JSON>[])[0].opaque_disjoint = [null, false];
    head.base_parent = { revision_id: 'new', content_digest: 'sha256:new' };
    const result = executeParentClipAdd(head, existing.command);
    expect(result.command).toEqual(existing.command);
    expect(clips(result.bundle)[0].opaque_disjoint).toEqual([null, false]);
    expect(clips(result.bundle).at(-1)).toEqual(existing.row);
  });

  it.each(['membership', 'order', 'shape', 'track-kind', 'track-absence', 'null-vs-absence', 'duplicate', 'reserved-member', 'mirrors'])(
    'refuses changed original %s guards without refreshing capture', (change) => {
    const head = copy(existing.bundle);
    const config = head.parent.config as Record<string, JSON>;
    if (change === 'membership') clips(head).push({ ...copy(existing.row), id: 'other' });
    if (change === 'order') clips(head).reverse();
    if (change === 'shape') delete config.clips;
    if (change === 'track-kind') tracks(head)[0].kind = 'audio';
    if (change === 'track-absence') config.tracks = [];
    if (change === 'null-vs-absence') tracks(head)[0].enabled = null;
    if (change === 'duplicate') clips(head).push(copy(clips(head)[0]));
    if (change === 'reserved-member') clips(head)[0].id = 'bad::id';
    if (change !== 'shape' && change !== 'mirrors') config.clips = copy(head.parent.clips);
    if (change === 'mirrors') (config.clips as Record<string, JSON>[])[0].at = 100;
    const before = copy(head);
    expect(() => executeParentClipAdd(head, existing.command)).toThrow();
    expect(head).toEqual(before);
    expect(finishParentClipAdd(captureParentClipAdd(existing.bundle, 'parent', existing.row)).command).toEqual(existing.command);
  });

  it.each(['resolved', 'expect', 'authorship', 'reads', 'selections', 'bindings', 'created'] as const)(
    'refuses incomplete or forged %s claims after JSON roundtrip', (key) => {
    const basis = roundtrip(captureParentClipAdd(existing.bundle, 'parent', existing.row));
    delete basis.command[key];
    expect(() => finishParentClipAdd(basis)).toThrow('incomplete');
    const command = copy(existing.command);
    Object.assign(command, { [key]: key === 'resolved' ? ['parent'] : ['expect', 'authorship', 'bindings'].includes(key) ? {} : [] });
    expect(() => executeParentClipAdd(existing.bundle, command)).toThrow('original capture');
  });

  it.each([
    ['undefined', undefined], ['NaN', NaN], ['infinity', Infinity], ['negative infinity', -Infinity],
    ['bigint', 1n], ['date', new Date(0)], ['map', new Map()], ['undefined element', [undefined]], ['sparse array', Array(1)],
  ])('refuses non-JSON values before capture or finish: %s', (_name, value) => {
    const row = { ...copy(first.row), opaque: value } as Record<string, JSON>;
    expect(() => captureParentClipAdd(first.bundle, 'parent', row)).toThrow('finite JSON');
    const basis = roundtrip(captureParentClipAdd(first.bundle, 'parent', first.row));
    Object.assign(basis.bundle.parent, { opaque: value });
    expect(() => finishParentClipAdd(basis)).toThrow('finite JSON');
  });
});
