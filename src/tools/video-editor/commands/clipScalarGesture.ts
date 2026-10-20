import type { EditCommand, JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import type { TimelinePatch } from '@/sdk/video/timeline/patch.ts';
import type { TimelineData } from '../lib/timeline-data.ts';
import { equal, freezeJson } from './clipMovePrimitives.ts';
import type { JsonObject } from './types.ts';

export type ClipScalarOwner = 'parent' | `occurrence:${string}`;
export type ClipScalarArgs = { values: Record<string, JSON>; clear: Array<'hold' | 'asset' | 'transition'> };
export interface ClipScalarCapturePort {
  /** An omitted owner is resolved and validated by the same session that captures the edit. */
  capture(input: { clipId: string; ownerRef?: ClipScalarOwner; current: TimelineData }): JsonObject;
  finish(basis: JsonObject, args: ClipScalarArgs): { command: EditCommand };
  submit(input: { command: EditCommand; preview: TimelinePatch }): void;
}
export interface CapturedClipScalarEdit {
  readonly clipId: string;
  readonly basis: JsonObject;
  readonly port: ClipScalarCapturePort;
}

export function clipScalarPreview(clipId: string, args: ClipScalarArgs): TimelinePatch {
  return { version: 1, operations: [{ op: 'clip.update', target: clipId, payload: structuredClone(args.values), clear: [...args.clear] }] };
}

/** The session validates explicit ownership or resolves it from its raw authoring basis. */
export function captureClipScalarEdit(
  port: ClipScalarCapturePort | undefined, current: TimelineData, clipId: string, ownerRef?: ClipScalarOwner,
): CapturedClipScalarEdit {
  if (!port) throw new Error('clip.set capture is unavailable.');
  if (current.resolvedConfig.clips.filter((clip) => clip.id === clipId).length !== 1) {
    throw new Error('clip.set requires an unambiguous clip identity.');
  }
  const basis = freezeJson(structuredClone(port.capture({ clipId, ownerRef, current })));
  return Object.freeze({ clipId, basis, port });
}

export function submitClipScalarEdit(captured: CapturedClipScalarEdit, args: ClipScalarArgs): void {
  const { command } = captured.port.finish(captured.basis, args);
  if (command.schema_version !== 1 || command.op !== 'clip.set' || command.version !== '1'
    || command.select !== captured.basis.select || !equal(command.args, args)) {
    throw new Error('Unsupported clip.set capture result.');
  }
  captured.port.submit({ command: freezeJson(structuredClone(command)), preview: clipScalarPreview(captured.clipId, args) });
}
