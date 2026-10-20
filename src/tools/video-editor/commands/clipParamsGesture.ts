import type { DocumentPin, EditCommand, JSON, VerifiedDocument, VerifiedDocumentObject } from '@/integrations/runtime/timeline-commit-types.ts';
import type { TimelinePatch } from '@/sdk/video/timeline/patch.ts';
import type { TimelineData } from '../lib/timeline-data.ts';
import { assertFiniteJson, equal, freezeJson, object } from './clipMovePrimitives.ts';
import type { ClipParamsArgs } from './clipParamsCapture.ts';
import type { JsonObject } from './types.ts';

export interface ClipParamsCapturePort {
  capture(input: { clipId: string; current: TimelineData }): JsonObject;
  // Detached native capture inputs only; prefetch never submits or refreshes a basis.
  prefetch?(basis: JsonObject, pin: DocumentPin): Promise<{
    basis: JsonObject;
    schema_source: DocumentPin;
    schema_inputs: [VerifiedDocument, Record<string, VerifiedDocumentObject>][];
    realm_id: string;
  }>;
  invalidatePrefetch?(): void;
  // A null previewParams means no local preview, never a params container value.
  finish(basis: JsonObject, args: ClipParamsArgs): { command: EditCommand; previewParams: Record<string, JSON> | null };
  submit(input: { command: EditCommand; preview: TimelinePatch | null }): void;
}

export interface CapturedClipParamsEdit {
  readonly clipId: string;
  readonly basis: JsonObject;
  readonly port: ClipParamsCapturePort;
}

/** Capture once before a discrete edit; the session resolves the raw semantic owner. */
export function captureClipParamsEdit(
  port: ClipParamsCapturePort | undefined,
  current: TimelineData,
  clipId: string,
): CapturedClipParamsEdit {
  if (!port) throw new Error('clip.set-params capture is unavailable.');
  if (current.resolvedConfig.clips.filter((clip) => clip.id === clipId).length !== 1) {
    throw new Error('clip.set-params requires an unambiguous clip identity.');
  }
  const basis = port.capture({ clipId, current });
  assertFiniteJson(basis);
  return Object.freeze({ clipId, basis: freezeJson(structuredClone(basis)), port });
}

export function submitClipParamsEdit(captured: CapturedClipParamsEdit, args: ClipParamsArgs): void {
  assertFiniteJson(args);
  const { command, previewParams } = captured.port.finish(captured.basis, args);
  assertFiniteJson(command);
  assertFiniteJson(previewParams);
  if (command.schema_version !== 1 || command.op !== 'clip.set-params' || command.version !== '1'
    || command.select !== captured.basis.select || !equal(command.args, args)
    || (previewParams !== null && !object(previewParams))) {
    throw new Error('Unsupported clip.set-params capture result.');
  }
  captured.port.submit({
    command: freezeJson(structuredClone(command)),
    preview: previewParams === null ? null : { version: 1, operations: [{ op: 'clip.update', target: captured.clipId,
      payload: { params: freezeJson(structuredClone(previewParams)) } }] },
  });
}
