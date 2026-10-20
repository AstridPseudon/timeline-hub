import type { EditCommand, JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import type { TimelinePatch } from '@/sdk/video/timeline/patch.ts';
import { assembleTimelineData, type TimelineData } from '../lib/timeline-data.ts';
import type { TimelineClip } from '../types/index.ts';
import { assertFiniteJson, equal, freezeJson, object } from './clipMovePrimitives.ts';
import type { JsonObject } from './types.ts';

export interface ParentClipAddCapturePort {
  capture(input: { row: Record<string, JSON>; current: TimelineData }): JsonObject;
  finish(basis: JsonObject): { command: EditCommand; preview: TimelinePatch };
  submit(input: { command: EditCommand; preview: TimelinePatch }): void;
}

export interface CapturedParentClipAdd {
  readonly row: Record<string, JSON>;
  readonly basis: JsonObject;
  readonly port: ParentClipAddCapturePort;
}

/** The caller allocates row.id before capture; retries never allocate another ID. */
export function captureParentClipAddEdit(
  port: ParentClipAddCapturePort | undefined, current: TimelineData, row: Record<string, JSON>,
): CapturedParentClipAdd {
  if (!port) throw new Error('Parent clip.add capture is unavailable.');
  assertFiniteJson(row);
  const original = freezeJson(structuredClone(row));
  const basis = port.capture({ row: original, current });
  assertFiniteJson(basis);
  return Object.freeze({ row: original, basis: freezeJson(structuredClone(basis)), port });
}

export function parentClipAddPreview(row: Record<string, JSON>): TimelinePatch {
  return { version: 1, source: 'parentclip.add', operations: [{ op: 'clip.add', target: row.id as string,
    payload: structuredClone(row) }] };
}

export function submitParentClipAddEdit(captured: CapturedParentClipAdd): void {
  const { command, preview } = captured.port.finish(captured.basis);
  assertFiniteJson(command);
  assertFiniteJson(preview);
  if (command.schema_version !== 1 || command.op !== 'clip.add' || command.version !== '1'
    || command.select !== 'parent' || !equal(command.args, { row: captured.row })
    || !equal(preview, parentClipAddPreview(captured.row))) {
    throw new Error('Unsupported parent clip.add capture result.');
  }
  captured.port.submit({ command: freezeJson(structuredClone(command)), preview: freezeJson(structuredClone(preview)) });
}

/** Keep the whole authored birth row; row serialization drops opaque fields and nulls. */
export function projectParentClipAddPreview(patch: TimelinePatch, current: TimelineData): TimelineData | undefined {
  if (patch.source !== 'parentclip.add') return undefined;
  assertFiniteJson(patch);
  const [operation] = patch.operations;
  const row = operation?.payload;
  if (patch.version !== 1 || patch.operations.length !== 1 || operation.op !== 'clip.add'
    || !object(row) || typeof row.id !== 'string' || row.id !== operation.target
    || !equal(patch, parentClipAddPreview(row))
    || current.config.clips.some((clip) => clip.id === row.id)
    || current.resolvedConfig.clips.some((clip) => clip.id === row.id)) {
    throw new Error('Invalid native parent clip.add preview');
  }
  const clip = structuredClone(row) as unknown as TimelineClip;
  const config = { ...current.config, clips: [...current.config.clips, clip] };
  return assembleTimelineData({ ...current, config,
    resolvedConfig: { ...current.resolvedConfig, clips: [...current.resolvedConfig.clips, clip] } });
}
