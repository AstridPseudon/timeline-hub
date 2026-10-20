import { describe, expect, it } from 'vitest';
import type { CommandRecord, EditCommand } from '@/integrations/runtime/timeline-commit-types.ts';
import type { TimelinePatch } from '@/sdk/video/timeline/patch.ts';
import { captureGenericPatch, executeGenericPatch, GenericPatchRefusal, projectGenericPatchPreview } from './genericPatchCapture.ts';
import { AuthoredState, copy, freezeJson, type AuthoredBundle } from './clipMovePrimitives.ts';
import { environment } from './__tests__/commitSessionEnvironment.ts';
import fixture from './fixtures/recipe_m2_generic_patch.json';

const cases = fixture.cases as unknown as Array<{ bundle: AuthoredBundle; patch: TimelinePatch;
  owners: string[]; commands: EditCommand[]; records: CommandRecord[]; after_bundle: AuthoredBundle }>;

describe('bounded native generic patch capture', () => {
  it.each(cases)('matches frozen 027 commands, records and full bundle for $owners', (golden) => {
    const bundle = freezeJson(copy(golden.bundle));
    const patch = copy(golden.patch);
    let index = 0;
    const result = captureGenericPatch(bundle, patch, () => golden.owners[index++]);
    expect(result.commands).toEqual(golden.commands);
    expect(result.records).toEqual(golden.records);
    expect(result.bundle).toEqual(golden.after_bundle);
    expect(executeGenericPatch(bundle, result.commands)).toEqual({ bundle: golden.after_bundle, records: golden.records });
    expect(bundle).toEqual(golden.bundle);
    expect(patch).toEqual(golden.patch);
    expect(Object.isFrozen(result.patch.operations[0].payload)).toBe(true);
    expect(Object.isFrozen(result.commands[0].expect)).toBe(true);
    expect(result.commands[2].expect).toEqual({ [`${golden.owners[0]}::label`]: { state: 'present', value: 'Picture α' } });
    expect(result.commands[3].expect![`${golden.owners[1]}::hold`]).toEqual({ state: 'present', value: 4.123456789 });
    patch.operations[0].payload!.label = 'caller mutation';
    expect(result.patch).toEqual(golden.patch);
    expect(new AuthoredState(result.bundle).entity(golden.owners[0])!.label).toBe('');
  });

  it('uses explicit order first, stable ties and original order for the remainder', () => {
    const golden = cases[0];
    const operations = golden.patch.operations;
    const patch: TimelinePatch = { version: 1, operations: [operations[2], operations[1], operations[0], operations[3]] };
    const result = captureGenericPatch(golden.bundle, patch, (operation) => operation.op === 'track.update'
      ? golden.owners[0] : golden.owners[1]);
    expect(result.commands).toEqual(golden.commands);
    expect(result.preview.operations.map((operation) => operation.payload)).toEqual([
      { label: 'Picture α' }, { hold: 4.123456789 }, { label: '' }, { hold: 3.987654321 },
    ]);
  });

  it.each([
    { op: 'clip.update', target: 'x', payload: { hold: null } },
    { op: 'track.update', target: 'V1', payload: { label: null } },
    { op: 'clip.update', target: 'x', payload: { hold: 2, opacity: 0.5 } },
    { op: 'clip.update', target: 'x', payload: { hold: 2, mode: 'merge' } },
    { op: 'clip.update', target: 'x', payload: { hold: 2 }, clear: ['asset'] },
    { op: 'clip.update', target: 'x', payload: { values: { hold: 2 } } },
    { op: 'track.update', target: 'V1', payload: { label: 'x', mode: 'replace' } },
    { op: 'track.update', target: 'V1', payload: { label: 'x', muted: false } },
    { op: 'project-data.write', target: 'extension', payload: { value: 1 } },
    { op: 'extension.noop', target: 'extension' },
  ])('refuses the complete patch without filtering %j', (operation) => {
    const patch = { version: 1, operations: [cases[0].patch.operations[0], operation] } as TimelinePatch;
    let resolved = false;
    try {
      captureGenericPatch(cases[0].bundle, patch, () => { resolved = true; return ''; });
      expect.fail('unsupported patch accepted');
    } catch (error) {
      expect(error).toBeInstanceOf(GenericPatchRefusal);
      expect((error as GenericPatchRefusal).intentions).toEqual([
        expect.objectContaining({ operationIndex: 0, op: 'track.update', reason: expect.stringContaining('another patch member') }),
        expect.objectContaining({ operationIndex: 1, op: operation.op, target: operation.target }),
      ]);
      expect(resolved).toBe(false);
    }
  });

  it('projects exact empty labels and source seconds once without changing input or unrelated fields', async () => {
    const env = await environment();
    const current = env.current();
    const before = copy(current);
    const patch: TimelinePatch = { version: 1, source: 'timeline.native-label-hold', operations: [
      { op: 'track.update', target: 'V1', payload: { label: '' } },
      { op: 'clip.update', target: 'x', payload: { hold: 1.123456789 } },
    ] };
    const next = projectGenericPatchPreview(patch, current)!;
    expect(next.config.tracks![0].label).toBe('');
    expect(next.resolvedConfig.tracks[0].label).toBe('');
    expect(next.config.clips[0].hold).toBe(1.123456789);
    expect(next.resolvedConfig.clips[0].hold).toBe(1.123456789);
    expect(next.config.clips[0].text).toEqual(before.config.clips[0].text);
    expect(next.config.clips[0].app).toEqual(before.config.clips[0].app);
    expect(next.dataLanes).toBe(current.dataLanes);
    expect(current).toEqual(before);
    expect(() => projectGenericPatchPreview({ ...patch, operations: [...patch.operations,
      { op: 'clip.update', target: 'missing', payload: { hold: 1 } }] }, current)).toThrow('one displayed target');
    expect(current).toEqual(before);
  });
});
