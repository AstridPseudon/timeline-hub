// @vitest-environment node
import { writeFileSync } from 'node:fs';
import { afterAll, describe, expect, it } from 'vitest';
import type { AgentRead, AgentSelection, AgentState, CommandRecord, EditCommand, JSON, MediaSelection, VerifiedMedia } from '@/integrations/runtime/timeline-commit-types.ts';
import {
  captureParentClipAddMediaAfterAnchor,
  finishParentClipAddMediaAfterAnchor,
  executeParentClipAddMediaAfterAnchor,
} from './parentAfterAnchorCapture.ts';
import { ClipMoveError, copy } from './clipMovePrimitives.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';

const media: MediaSelection = {
  asset: 'reserved-new',
  generation_id: 'generation-new',
  variant_id: 'variant-new',
  object_id: 'sha256:2222222222222222222222222222222222222222222222222222222222222222',
  catalog_digest: 'sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
};
const verified: VerifiedMedia = { selection: media, media_type: 'video/fixture', size: 123, duration_seconds: 10 };

function bundle(): AuthoredBundle {
  const clips: Record<string, JSON>[] = [
    { id: 'before', clipType: 'video', asset: 'picture', track: 'overlay', at: 0, hold: 1 },
    { id: 'anchor', clipType: 'video', asset: 'picture', track: 'overlay', at: 1.003, hold: 4,
      from: 2, to: 6, speed: 2, effectId: 'effect-anchor', opaque: { keep: [null, false, {}] } },
    { id: 'later', clipType: 'video', asset: 'picture', track: 'overlay', at: 6, hold: 1, at_ms: 6000 },
    { id: 'other', clipType: 'video', asset: 'picture', track: 'other', at: 2, hold: 1 },
  ];
  const config = {
    output: { fps: { numerator: 24, denominator: 1 } },
    tracks: [
      { id: 'overlay', kind: 'visual', role: 'output' },
      { id: 'other', kind: 'visual', role: 'output' },
    ],
    clips: copy(clips),
    registry: { assets: {
      picture: { media_id: 'sha256:1111111111111111111111111111111111111111111111111111111111111111', type: 'video' },
    } },
  } as Record<string, JSON>;
  return {
    schema_version: 1,
    project_id: 'project-1',
    timeline_id: 'film',
    base_parent: { revision_id: 'parent-r1' },
    parent: { config, clips, registry: copy(config.registry) },
    placements: [{ occurrence_id: 'occ-a', shot_id: 'shot-other', track: 'other', placement: { track: 'other' } }],
    shots: {},
  } as AuthoredBundle;
}

const parity: unknown[] = [];
afterAll(() => {
  if (process.env.PARENT_AFTER_PARITY_OUTPUT) writeFileSync(process.env.PARENT_AFTER_PARITY_OUTPUT, JSON.stringify(parity));
});

describe('dormant parent after-anchor media capture', () => {
  it('matches Agent raw clone, rate-aware ripple, opaque data, and complete claims', () => {
    const input = bundle();
    const basis = captureParentClipAddMediaAfterAnchor(input, 'parent/clip:anchor', { id: 'born' }, media, [verified]);
    const result = finishParentClipAddMediaAfterAnchor(
      basis,
    );
    parity.push({ original: input, requested: { id: 'born' }, ...result });
    const rows = result.bundle.parent.clips as Record<string, JSON>[];

    // Complete record from exact Agent 3b3208c43, including ordered observations
    // and both real mirror compilations (before birth and at command finish).
    const present = (value: JSON): AgentState => ({ state: 'present', value: copy(value) });
    const absent: AgentState = { state: 'absent' };
    const read = (ref: string, path: string[], state: AgentState): AgentRead => ({ ref, path, state });
    const select = (key: string, members: string[], order = members, boundaries = members): AgentSelection =>
      ({ key, query_version: 1, owner: 'parent', members, order, boundaries, policy: 'guard-membership' });
    const original = input.parent.clips as Record<string, JSON>[];
    const config = input.parent.config as Record<string, JSON>;
    const born = { ...original[1], id: 'born', asset: media.asset, at: 3.003, effectId: 'effect-born' };
    const shifted = original.map((row) => row.id === 'later' ? { ...row, at: 8, at_ms: 8000 } : row);
    const after = [shifted[0], shifted[1], born, ...shifted.slice(2)];
    const reads = [
      read('parent', ['config', 'output', 'fps'], present({ numerator: 24, denominator: 1 })),
      read('parent/source', ['source_window'], absent),
      read('parent/collection:track', [], present({ members: present([]), config: present({}) })),
      read('parent/track:overlay', [], present((config.tracks as JSON[])[0])),
      read('parent/collection:occurrence', [], present({ container: 'array' })),
      read('occurrence:occ-a', ['placement', 'track'], present('other')),
      read('occurrence:occ-a', ['track'], present('other')),
      read('parent/collection:asset', [], present({
        '0': { registry: present({}), assets: present({}) },
        '1': { registry: present({}), assets: present({}) },
      })),
      read('parent/asset:reserved-new', [], absent),
      read('parent/collection:clip', [], present({ members: present([]), config: present({}), payload_members: present([]) })),
      read('parent/clip:anchor', [], present(original[1])),
      read('parent/asset:picture', [], present(((config.registry as Record<string, JSON>).assets as Record<string, JSON>).picture)),
      read('parent/clip:later', ['track'], present('overlay')),
      read('parent/clip:later', [], present(original[2])),
      read('parent/clip:other', ['track'], present('other')),
      read('parent/clip:born', [], absent),
    ];
    const selections = [
      select('collection.tracks', ['parent/track:overlay', 'parent/track:other']),
      select('collection.occurrences', ['occurrence:occ-a']),
      select('collection.clips.after', ['parent/clip:anchor'],
        original.map((row) => `parent/clip:${row.id}`), ['parent/clip:anchor', 'parent/clip:later']),
    ];
    const bindings = { 'media.track': 'parent/track:overlay', 'parent.after-clip': 'parent/clip:anchor',
      'parent.after-track': 'parent/track:overlay' };
    const command: EditCommand = {
      schema_version: 1, op: 'clip.add-media', version: '1', select: 'parent/clip:anchor',
      args: { row: born, media }, intent: {}, resolved: [], reads, selections, bindings,
      created: ['parent/asset:reserved-new', 'parent/clip:born'],
      expect: { 'parent/asset:reserved-new::': absent, 'parent/clip:later::at': present(6),
        'parent/clip:later::at_ms': present(6000), 'parent/clip:born::': absent },
      authorship: { 'parent/asset:reserved-new::': 'direct', 'parent/clip:later::at': 'direct',
        'parent/clip:later::at_ms': 'direct', 'parent/clip:born::': 'direct' },
    };
    const record: CommandRecord = { ordinal: 0, command, reads, selections,
      writes: [
        { ref: 'parent/asset:reserved-new', path: [], before: absent, after: present({
          media_id: media.object_id, type: 'video', generationId: media.generation_id, variantId: media.variant_id,
        }) },
        { ref: 'parent/clip:later', path: ['at'], before: present(6), after: present(8) },
        { ref: 'parent/clip:later', path: ['at_ms'], before: present(6000), after: present(8000) },
        { ref: 'parent/clip:born', path: [], before: absent, after: present(born) },
      ],
      bindings: [{ key: 'media.owner', ref: 'parent', policy: 'fixed', dependencies: [] },
        ...Object.entries(bindings).map(([key, ref]) => ({ key, ref, policy: 'fixed' as const, dependencies: [] }))],
      created: [{ ref: 'parent/asset:reserved-new', kind: 'asset', owner: 'parent' },
        { ref: 'parent/clip:born', kind: 'clip', owner: 'parent' }],
      dependencies: [{ key: 'media.new', kind: 'media', pin: media, policy: 'exact' }],
      derived_writes: [
        { ref: 'parent', path: ['config', 'clips'], before: present(original), after: present(shifted), cause: 0 },
        { ref: 'parent', path: ['config', 'clips'], before: present(shifted), after: present(after), cause: 0 },
      ],
    };
    expect(result.command).toEqual(command);
    expect(result.record).toEqual(record);
    expect(executeParentClipAddMediaAfterAnchor(input, command, [verified])).toEqual(result);

    expect(result.command).toMatchObject({
      schema_version: 1, op: 'clip.add-media', version: '1', select: 'parent/clip:anchor',
      args: { media, row: { id: 'born', asset: media.asset, track: 'overlay', at: 3.003,
        from: 2, to: 6, speed: 2, effectId: 'effect-born', opaque: { keep: [null, false, {}] } } },
    });
    expect(result.command.args).not.toHaveProperty('afterClipId');
    expect(rows.map((row) => row.id)).toEqual(['before', 'anchor', 'born', 'later', 'other']);
    expect(rows.find((row) => row.id === 'later')).toMatchObject({ at: 8, at_ms: 8000 });
    expect(rows.find((row) => row.id === 'other')).toMatchObject({ at: 2 });
    expect(result.record.selections.find((item) => item.key === 'collection.clips.after')).toEqual({
      key: 'collection.clips.after', query_version: 1, owner: 'parent', members: ['parent/clip:anchor'],
      order: ['parent/clip:before', 'parent/clip:anchor', 'parent/clip:later', 'parent/clip:other'],
      boundaries: ['parent/clip:anchor', 'parent/clip:later'],
      policy: 'guard-membership',
    });
    expect(result.record.reads).toEqual(expect.arrayContaining([
      expect.objectContaining({ ref: 'parent/clip:anchor', path: [] }),
      expect.objectContaining({ ref: 'parent/asset:picture', path: [] }),
      expect.objectContaining({ ref: 'parent', path: ['config', 'output', 'fps'] }),
      expect.objectContaining({ ref: 'parent/clip:later', path: ['track'] }),
      expect.objectContaining({ ref: 'parent/clip:later', path: [] }),
      expect.objectContaining({ ref: 'parent/clip:other', path: ['track'] }),
    ]));
    expect(result.record.writes).toEqual(expect.arrayContaining([
      expect.objectContaining({ ref: 'parent/clip:later', path: ['at'] }),
      expect.objectContaining({ ref: 'parent/clip:later', path: ['at_ms'] }),
    ]));
    expect(result.record.bindings).toEqual(expect.arrayContaining([
      expect.objectContaining({ key: 'parent.after-clip', ref: 'parent/clip:anchor' }),
      expect.objectContaining({ key: 'parent.after-track', ref: 'parent/track:overlay' }),
    ]));
    expect(result.record.created.map((item) => item.ref)).toEqual(['parent/asset:reserved-new', 'parent/clip:born']);
    expect(input.parent.clips).toEqual(bundle().parent.clips);
  });

  it('keeps the selected tuple and reserved IDs across JSON reload, and rejects wrong ownership or identity', () => {
    const input = bundle();
    const basis = captureParentClipAddMediaAfterAnchor(input, 'parent/clip:anchor', { id: 'born' }, media, [verified]);
    expect(finishParentClipAddMediaAfterAnchor(JSON.parse(JSON.stringify(basis)))).toEqual(
      finishParentClipAddMediaAfterAnchor(basis),
    );
    expect(() => captureParentClipAddMediaAfterAnchor(input, 'occurrence:occ-a', { id: 'born' }, media, [verified]))
      .toThrowError(ClipMoveError);
    expect(() => captureParentClipAddMediaAfterAnchor(input, 'parent/clip:missing', { id: 'born' }, media, [verified]))
      .toThrowError(ClipMoveError);
    const ambiguous = bundle();
    const duplicate = copy((ambiguous.parent.clips as Record<string, JSON>[])[1]);
    (ambiguous.parent.clips as Record<string, JSON>[]).push(duplicate);
    ((ambiguous.parent.config as Record<string, JSON>).clips as Record<string, JSON>[]).push(copy(duplicate));
    expect(() => captureParentClipAddMediaAfterAnchor(ambiguous, 'parent/clip:anchor', { id: 'born' }, media, [verified]))
      .toThrowError(ClipMoveError);
    const changed = copy(basis.command);
    (changed.args.media as Record<string, JSON>).catalog_digest =
      'sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc';
    expect(() => finishParentClipAddMediaAfterAnchor({ ...basis, command: changed })).toThrowError(ClipMoveError);
  });
  it('preserves an incoming source transition through capture and replay', () => {
    const input = bundle();
    const source = (input.parent.clips as Record<string, JSON>[])[1];
    source.transition = { type: 'crossfade', duration: .5, opaque: [false, null] };
    (input.parent.config as Record<string, JSON>).clips = copy(input.parent.clips);
    const basis = captureParentClipAddMediaAfterAnchor(input, 'parent/clip:anchor', { id: 'born' }, media, [verified]);
    const result = finishParentClipAddMediaAfterAnchor(basis);
    expect(result.command.args.row).toEqual({ ...source, id: 'born', asset: media.asset, at: 3.003, effectId: 'effect-born' });
    expect(finishParentClipAddMediaAfterAnchor(JSON.parse(JSON.stringify(basis)))).toEqual(result);
    parity.push({ original: input, requested: { id: 'born' }, ...result });
  });

  // Exact Agent 3b3208c43 requires a positive numeric hold before raw-window
  // validation; keep the Main-compatible missing/null-hold requirement open.
  it.each(['missing', 'null'])('refuses a %s video hold atomically and accepts the equivalent positive window', (hold) => {
    const input = bundle();
    const source = (input.parent.clips as Record<string, JSON>[])[1];
    if (hold === 'missing') delete source.hold;
    else source.hold = null;
    source.transition = { type: 'crossfade', duration: .5, opaque: [false, null] };
    (input.parent.config as Record<string, JSON>).clips = copy(input.parent.clips);
    const before = copy(input);
    expect(() => captureParentClipAddMediaAfterAnchor(
      input, 'parent/clip:anchor', { id: 'born' }, media, [verified],
    )).toThrow('clip.hold must be a finite positive number');
    expect(input).toEqual(before);
    parity.push({ original: input, requested: { id: 'born' }, refused: true });

    const validInput = bundle();
    const validSource = (validInput.parent.clips as Record<string, JSON>[])[1];
    validSource.transition = copy(source.transition);
    (validInput.parent.config as Record<string, JSON>).clips = copy(validInput.parent.clips);
    const result = finishParentClipAddMediaAfterAnchor(
      captureParentClipAddMediaAfterAnchor(validInput, 'parent/clip:anchor', { id: 'born' }, media, [verified]));
    expect(result.command.args.row).toEqual({
      ...validSource, id: 'born', asset: media.asset, at: 3.003, effectId: 'effect-born',
    });
    expect(result.command.args.row).toMatchObject({ hold: 4, from: 2, to: 6, transition: source.transition });
  });

  it('preserves explicit null effects but refuses explicit null track/asset overrides', () => {
    const input = bundle();
    const requested = { id: 'born', effectId: null, effect_id: null };
    const result = finishParentClipAddMediaAfterAnchor(
      captureParentClipAddMediaAfterAnchor(input, 'parent/clip:anchor', requested, media, [verified]));
    expect(result.command.args.row).toMatchObject({ effectId: null, effect_id: null });
    parity.push({ original: input, requested, ...result });
    for (const key of ['track', 'asset']) {
      const requested = { id: 'born', [key]: null };
      expect(() => captureParentClipAddMediaAfterAnchor(input, 'parent/clip:anchor', requested, media, [verified]))
        .toThrow(ClipMoveError);
      parity.push({ original: input, requested, refused: true });
    }
  });

  it('floors a positive sub-0.05 duration and refuses a cloned zero hold at media validation', () => {
    for (const hold of [.01, 0]) {
      const input = bundle();
      const source = (input.parent.clips as Record<string, JSON>[])[1];
      source.hold = hold;
      delete source.from;
      delete source.to;
      (input.parent.config as Record<string, JSON>).clips = copy(input.parent.clips);
      const capture = () => captureParentClipAddMediaAfterAnchor(input, 'parent/clip:anchor', { id: 'born' }, media, [verified]);
      if (hold === 0) {
        expect(capture).toThrow('clip.hold must be a finite positive number');
        parity.push({ original: input, requested: { id: 'born' }, refused: true, zeroHold: true });
      } else {
        const result = finishParentClipAddMediaAfterAnchor(capture());
        expect((result.command.args.row as Record<string, JSON>).at).toBe(1.053);
        expect((result.bundle.parent.clips as Record<string, JSON>[]).find((row) => row.id === 'later')!.at).toBe(6.05);
        parity.push({ original: input, requested: { id: 'born' }, ...result });
      }
    }
  });

  it('refuses source at_ms instead of stripping it before raw-window validation', () => {
    const input = bundle();
    (input.parent.clips as Record<string, JSON>[])[1].at_ms = 1003;
    (input.parent.config as Record<string, JSON>).clips = copy(input.parent.clips);
    const before = copy(input);
    expect(() => captureParentClipAddMediaAfterAnchor(input, 'parent/clip:anchor', { id: 'born' }, media, [verified]))
      .toThrow('media edit does not support at_ms');
    expect(input).toEqual(before);
    parity.push({ original: input, requested: { id: 'born' }, refused: true });
  });

});

/*
Export with PARENT_AFTER_PARITY_OUTPUT=<samples.json> in the focused Vitest run.
Run this checker with exact Agent 3b3208c43903b770010de0649691cfa566447822
on PYTHONPATH (read-only git archive plus pyproject.toml), using dependencies
from the shared Python environment. No Runtime, provider, HTTP or renderer.

PYTHON_AFTER_PARITY
import copy
import json
import sys
from pathlib import Path
from astrid.sdk.timeline._command_state import CommandError
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.native_parent_media_commands import capture_clip_add_media, _after_capture_row
from astrid.sdk.timeline.rebase import replay

samples = json.loads(Path(sys.argv[1]).read_text())
assert len(samples) == 10
media = samples[0]['command']['args']['media']
verified = [dict(selection=media, media_type='video/fixture', size=123, duration_seconds=10)]
accepted = refused = 0
for sample in samples:
    original, requested = sample['original'], sample['requested']
    before = copy.deepcopy(original)
    if sample.get('zeroHold'):
        # The duration helper floors zero, but _clip still rejects cloned hold=0.
        row = _after_capture_row(original, 'parent/clip:anchor', requested, media)
        assert row['at'] == 1.053 and row['hold'] == 0
    try:
        command = capture_clip_add_media(original, requested, media, verified_media=verified,
                                         after='parent/clip:anchor')
    except CommandError as exc:
        assert sample.get('refused'), (requested, str(exc))
        refused += 1
    else:
        assert not sample.get('refused'), requested
        plan = execute(original, [command], verified_media=verified)
        assert command == sample['command'], 'capture differs'
        assert plan.records == [sample['record']], 'COMPLETE record differs'
        assert plan.bundle == sample['bundle'], 'authored bundle differs'
        assert replay(plan, original, verified_media=verified).records == plan.records
        accepted += 1
    assert original == before, 'input mutated'
assert (accepted, refused) == (4, 6)
print('Exact Agent 3b3208c43: 4 complete commands/records/bundles and replay; 6 refusals; zero duration floor matched')
PYTHON_AFTER_PARITY
*/
