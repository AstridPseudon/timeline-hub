import type { DocumentPin, EditCommand, VerifiedDocument, VerifiedDocumentObject } from '@/integrations/runtime/timeline-commit-types.ts';
import type { SubmittedClipParamsInput } from '@/sdk/video/timeline/timelineOps.ts';
import type { TimelinePatch } from '@/sdk/video/timeline/patch.ts';
import type { TimelineData } from '../lib/timeline-data.ts';
import { assertFiniteJson, equal, freezeJson } from './clipMovePrimitives.ts';
import type { ClipParamsArgs } from './clipParamsCapture.ts';
import type { JsonObject } from './types.ts';

export interface ClipParamsCapturePort {
  submittedInput?(input: { clipId: string; current: TimelineData }): SubmittedClipParamsInput | undefined;
  capture(input: { clipId: string; current: TimelineData }): JsonObject;
  prefetch(basis: JsonObject, pin: DocumentPin): Promise<{
    basis: JsonObject;
    schema_source: DocumentPin;
    schema_inputs: [VerifiedDocument, Record<string, VerifiedDocumentObject>][];
    realm_id: string;
  }>;
  invalidatePrefetch(): void;
  finish(basis: JsonObject, args: ClipParamsArgs): { command: EditCommand; previewParams: null };
  submit(input: { command: EditCommand; preview: TimelinePatch | null }): void;
}

export function captureClipParamsEdit(port: ClipParamsCapturePort | undefined, current: TimelineData, clipId: string) {
  if (!port) throw new Error('clip.set-params capture is unavailable');
  const basis = port.capture({ clipId, current });
  assertFiniteJson(basis);
  return Object.freeze({ clipId, basis: freezeJson(structuredClone(basis)), port });
}

export function submitClipParamsEdit(captured: ReturnType<typeof captureClipParamsEdit>, args: ClipParamsArgs): void {
  const { command, previewParams } = captured.port.finish(captured.basis, args);
  assertFiniteJson(command);
  if (command.schema_version !== 1 || command.op !== 'clip.set-params' || command.version !== '1'
    || command.select !== captured.basis.select || !equal(command.args, args) || previewParams !== null) {
    throw new Error('Unsupported server-authoritative clip.set-params result');
  }
  captured.port.submit({ command: freezeJson(structuredClone(command)), preview: null });
}
