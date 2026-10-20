import { describe, expect, it, vi } from 'vitest';
import type { JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import { assembleTimelineData } from '../lib/timeline-data.ts';
import { captureParentClipAddEdit, parentClipAddPreview, projectParentClipAddPreview,
  submitParentClipAddEdit, type ParentClipAddCapturePort } from './parentClipAddGesture.ts';

const row: Record<string, JSON> = { id: 'caller-id', track: 'V1', clipType: 'text', at: 0.017, hold: 1.013,
  sourceURL: null, from: null, speed: null, params: { text: 'First', choice: null },
  app: { astrid: { on: null, opaque: [null, false] } }, unknown: { id: 'caller-id', keep: [null, {}, []] } };
function current() {
  const existing = { id: 'existing', track: 'V1', at: 2.017, hold: 3.013, opaque: [null, false], app: { keep: null } };
  const config = { output: { fps: 30, resolution: '1920x1080', file: '' }, tracks: [{ id: 'V1', kind: 'visual' as const }],
    clips: [existing], opaque: { preserve: null } };
  return assembleTimelineData({ config, configVersion: 3, registry: { assets: {} }, assetMap: {}, output: config.output,
    sourceItemsBySchemaRef: {}, resolvedConfig: { ...config, registry: {} } });
}
function setup() {
  const basis = { command: { args: { row: structuredClone(row) } }, localGeneration: 0 };
  const port: ParentClipAddCapturePort = {
    capture: vi.fn(() => basis),
    finish: vi.fn(() => ({ command: { schema_version: 1, op: 'clip.add', version: '1', select: 'parent',
      args: { row: structuredClone(row) } }, preview: parentClipAddPreview(row) })),
    submit: vi.fn(),
  };
  return { basis, port };
}

describe('parent nonmedia add gesture and lossless birth preview', () => {
  it('captures the caller ID once, freezes the original row and submits the exact whole-row preview', () => {
    const { port, basis } = setup();
    const input = structuredClone(row);
    const captured = captureParentClipAddEdit(port, current(), input);
    input.id = 'changed';
    basis.command.args.row.params = { text: 'changed' };
    submitParentClipAddEdit(captured);
    expect(port.capture).toHaveBeenCalledOnce();
    expect(captured.row).toEqual(row);
    expect(captured.basis.command).toEqual({ args: { row } });
    expect(Object.isFrozen(captured.row.app)).toBe(true);
    expect(Object.isFrozen(captured.basis.command)).toBe(true);
    expect(port.finish).toHaveBeenCalledWith(captured.basis);
    expect(port.submit).toHaveBeenCalledWith({ command: { schema_version: 1, op: 'clip.add', version: '1', select: 'parent',
      args: { row } }, preview: parentClipAddPreview(row) });
  });

  it('refuses an unavailable port and non-JSON rows before capture', () => {
    const { port } = setup();
    expect(() => captureParentClipAddEdit(undefined, current(), row)).toThrow('unavailable');
    expect(() => captureParentClipAddEdit(port, current(), { ...row, at: NaN })).toThrow('finite JSON');
    expect(port.capture).not.toHaveBeenCalled();
  });

  it.each(['op', 'select', 'args', 'preview'])(
    'refuses a changed %s result before submission', (field) => {
      const { port } = setup();
      const captured = captureParentClipAddEdit(port, current(), row);
      const finish = port.finish;
      port.finish = (basis) => {
        const result = finish(basis);
        if (field === 'preview') result.preview.operations[0].payload = { id: row.id };
        else Object.assign(result.command, { [field]: field === 'op' ? 'occurrence.add-media'
          : field === 'select' ? 'occurrence:other' : { row: { ...row, id: 'new-id' } } });
        return result;
      };
      expect(() => submitParentClipAddEdit(captured)).toThrow('Unsupported');
      expect(port.submit).not.toHaveBeenCalled();
    });

  it('keeps off-grid seconds, opaque JSON, nulls and absence through the existing data assembly boundary', () => {
    const before = current();
    const original = structuredClone(before.config);
    const next = projectParentClipAddPreview(parentClipAddPreview(row), before)!;
    expect(next.config.clips).toEqual([...original.clips, row]);
    expect(next.resolvedConfig.clips).toEqual([...before.resolvedConfig.clips, row]);
    expect(next.config.clips[1].at).toBe(0.017);
    expect(next.config.clips[1].hold).toBe(1.013);
    expect(next.config.clips[1].from).toBeNull();
    expect(Object.hasOwn(next.config.clips[1], 'to')).toBe(false);
    expect(next.config.clips[1].speed).toBeNull();
    const action = next.rows[0].actions.find((item) => item.id === row.id)!;
    expect(action.start).toBe(0.017);
    expect(action.end).toBeCloseTo(1.03, 12);
    expect(next.registry).toBe(before.registry);
    expect(next.sourceItemsBySchemaRef).toBe(before.sourceItemsBySchemaRef);
    expect(next.config.clips[0]).toBe(before.config.clips[0]);
    expect(before.config).toEqual(original);
  });

  it('handles the first clip without a serializer or registry birth and refuses a second preview of the same ID', () => {
    const before = current();
    before.config.clips = [];
    before.resolvedConfig.clips = [];
    const next = projectParentClipAddPreview(parentClipAddPreview(row), before)!;
    expect(next.config.clips).toEqual([row]);
    expect(next.registry).toEqual({ assets: {} });
    expect(() => projectParentClipAddPreview(parentClipAddPreview(row), next)).toThrow('Invalid');
  });

  it('keeps snapshot metadata and the accepted base while marking a birth as local', () => {
    const before = current();
    before.head = { projectId: 'project', timelineId: 'timeline', headRevisionId: 'r0', headPublicationId: 'p0' };
    before.editProjection = { kind: 'accepted', head: { revisionId: 'r0', publicationId: 'p0' } };
    before.dataLanes = [{ id: 'retained-lane' }] as typeof before.dataLanes;
    before.transcriptReferences = {} as typeof before.transcriptReferences;
    const next = projectParentClipAddPreview(parentClipAddPreview(row), before)!;
    expect(next.head).toBe(before.head);
    expect(next.configVersion).toBe(before.configVersion);
    expect(next.dataLanes).toBe(before.dataLanes);
    expect(next.transcriptReferences).toBe(before.transcriptReferences);
    expect(next.sourceItemsBySchemaRef).toBe(before.sourceItemsBySchemaRef);
    expect(next.registry).toBe(before.registry);
    expect(next.assetMap).toBe(before.assetMap);
    expect(next.editProjection).toEqual({ kind: 'local', base: before.editProjection.head, generation: 0 });
    expect(before.editProjection.kind).toBe('accepted');
    const again = projectParentClipAddPreview(parentClipAddPreview({ ...row, id: 'second' }), next)!;
    expect(again.editProjection).toBe(next.editProjection);
    expect(again.dataLanes).toBe(before.dataLanes);
  });

  it('leaves other sources to the existing compiler and rejects partial, retargeted or multi-row births', () => {
    const data = current();
    expect(projectParentClipAddPreview({ ...parentClipAddPreview(row), source: 'clip.trim' }, data)).toBeUndefined();
    const patch = parentClipAddPreview(row);
    expect(() => projectParentClipAddPreview({ ...patch, operations: [{ ...patch.operations[0], target: 'other' }] }, data)).toThrow('Invalid');
    expect(() => projectParentClipAddPreview({ ...patch, operations: [...patch.operations, ...patch.operations] }, data)).toThrow('Invalid');
    expect(() => projectParentClipAddPreview({ ...patch, operations: [{ op: 'clip.update', target: row.id as string, payload: row }] }, data)).toThrow('Invalid');
    expect(data.config.clips).toHaveLength(1);
  });
});
