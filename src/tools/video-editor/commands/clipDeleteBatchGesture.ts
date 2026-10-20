import type { EditCommand } from '@/integrations/runtime/timeline-commit-types.ts';
import type { TimelinePatch } from '@/sdk/video/timeline/patch.ts';
import type { TimelineData } from '../lib/timeline-data.ts';
import type { ClipDeleteBatchMember } from './clipDeleteBatchCapture.ts';
import { clipDeletePreview, projectClipDeletePreview } from './clipDeleteGesture.ts';
import { assertFiniteJson, equal, freezeJson } from './clipMovePrimitives.ts';
import type { JsonObject } from './types.ts';

export interface ClipDeleteBatchCapturePort {
  capture(input: { members: readonly ClipDeleteBatchMember[]; current: TimelineData }): JsonObject;
  finish(basis: JsonObject): { commands: EditCommand[]; preview: TimelinePatch };
  submit(input: { commands: EditCommand[]; preview: TimelinePatch }): void;
}

export interface CapturedClipDeleteBatchEdit {
  readonly members: readonly ClipDeleteBatchMember[];
  readonly basis: JsonObject;
  readonly port: ClipDeleteBatchCapturePort;
}

export function captureClipDeleteBatchEdit(
  port: ClipDeleteBatchCapturePort | undefined,
  current: TimelineData,
  members: readonly ClipDeleteBatchMember[],
): CapturedClipDeleteBatchEdit {
  if (!port) throw new Error('clip.delete batch capture is unavailable.');
  assertFiniteJson(members);
  const frozen = freezeJson(structuredClone(members));
  const ids = frozen.map((member) => member.clipId);
  if (!ids.length || new Set(ids).size !== ids.length || frozen.some(({ clipId, ownerRef }) => ownerRef !== 'parent'
    || current.config.clips.filter((clip) => clip.id === clipId).length !== 1
    || current.resolvedConfig.clips.filter((clip) => clip.id === clipId).length !== 1)) {
    throw new Error('Delete batch requires distinct original parent clip identities.');
  }
  const result = port.capture({ members: frozen, current });
  assertFiniteJson(result);
  return Object.freeze({ members: frozen, basis: freezeJson(structuredClone(result)), port });
}

export function submitClipDeleteBatchEdit(captured: CapturedClipDeleteBatchEdit): void {
  const { commands, preview } = captured.port.finish(captured.basis);
  assertFiniteJson(commands);
  const ids = captured.members.map((member) => member.clipId);
  if (commands.length !== ids.length || commands.some((command, index) => command.schema_version !== 1
    || command.op !== 'clip.delete' || command.version !== '1' || command.select !== `parent/clip:${ids[index]}`
    || !equal(command.args, {})) || !equal(preview, clipDeleteBatchPreview(ids))) {
    throw new Error('Unsupported clip.delete batch capture result.');
  }
  captured.port.submit({ commands: freezeJson(structuredClone(commands)), preview: freezeJson(structuredClone(preview)) });
}

export function clipDeleteBatchPreview(clipIds: readonly string[]): TimelinePatch {
  return { version: 1, source: 'parentclip.delete.batch',
    operations: clipIds.flatMap((clipId) => clipDeletePreview(clipId).operations) };
}

/** Compose temporary whole-row removals; the caller installs only the final candidate. */
export function projectClipDeleteBatchPreview(patch: TimelinePatch, current: TimelineData): TimelineData | undefined {
  if (patch.source !== 'parentclip.delete.batch') return undefined;
  assertFiniteJson(patch);
  const ids = patch.operations.map((operation) => operation.target);
  if (!ids.length || ids.some((id) => typeof id !== 'string') || new Set(ids).size !== ids.length
    || !equal(patch, clipDeleteBatchPreview(ids as string[]))) {
    throw new Error('Invalid native parent clip.delete batch preview');
  }
  let next = current;
  for (const id of ids) next = projectClipDeletePreview(clipDeletePreview(id as string), next)!;
  return next;
}
