import type { DocumentPin, EditCommand, VerifiedDocument, VerifiedDocumentObject, JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import type { TimelinePatch } from '@/sdk/video/timeline/patch.ts';
import type { TimelineData } from '../lib/timeline-data.ts';
import { assertFiniteJson, equal, freezeJson } from './clipMovePrimitives.ts';
import type { ClipParamsArgs } from './clipParamsCapture.ts';
import type { JsonObject } from './types.ts';

export interface ClipParamsCapturePort {
  resolveAuthority?(input: { select: string; rawClip: Record<string, unknown> | null | undefined }): DocumentPin;
  capture(input: { clipId: string; current: TimelineData }): JsonObject;
  prefetch?(basis: JsonObject, pin: DocumentPin): Promise<{
    basis: JsonObject;
    schema_source: DocumentPin;
    schema_inputs: [VerifiedDocument, Record<string, VerifiedDocumentObject>][];
    realm_id: string;
  }>;
  invalidatePrefetch?(): void;
  finish(basis: JsonObject, args: ClipParamsArgs): { command: EditCommand; previewParams: Record<string, JSON> | null };
  submit(input: { command: EditCommand; preview: TimelinePatch | null }): void;
}

export function captureClipParamsEdit(port: ClipParamsCapturePort | undefined, current: TimelineData, clipId: string) {
  if (!port) throw new Error('clip.set-params capture is unavailable; draft preserved');
  if (current.resolvedConfig.clips.filter((clip) => clip.id === clipId).length !== 1) {
    throw new Error('clip.set-params requires an unambiguous clip identity');
  }
  const basis = port.capture({ clipId, current });
  assertFiniteJson(basis);
  return Object.freeze({ clipId, basis: freezeJson(structuredClone(basis)), port });
}

export function submitClipParamsEdit(captured: ReturnType<typeof captureClipParamsEdit>, args: ClipParamsArgs): void {
  assertFiniteJson(args);
  const { command, previewParams } = captured.port.finish(captured.basis, args);
  assertFiniteJson(command);
  if (command.schema_version !== 1 || command.op !== 'clip.set-params' || command.version !== '1'
    || command.select !== captured.basis.select || !equal(command.args, args) || previewParams !== null) {
    throw new Error('Unsupported native selected clip parameter capture result');
  }
  captured.port.submit({ command: freezeJson(structuredClone(command)), preview: null });
}
