import type { EditCommand } from '@/integrations/runtime/timeline-commit-types.ts';
import type { TimelinePatch } from '@/sdk/video/timeline/patch.ts';
import type { TimelineData } from '../lib/timeline-data.ts';
import { canSplitClipAtTime, createSplitClipId } from '../lib/editor-utils.ts';
import { equal, freezeJson, object } from './clipMovePrimitives.ts';
import { clipSplitPreview, projectClipSplitPreview } from './clipSplitGesture.ts';
import type { ClipSplitBatchMember } from './clipSplitBatchCapture.ts';
import type { JsonObject } from './types.ts';

export interface ClipSplitBatchCapturePort {
  capture(input: { clipIds: readonly string[]; members: readonly ClipSplitBatchMember[]; on: number; current: TimelineData }): JsonObject;
  finish(basis: JsonObject): { commands: EditCommand[]; preview: TimelinePatch };
  submit(input: { commands: EditCommand[]; preview: TimelinePatch }): void;
}

export interface CapturedClipSplitBatchEdit {
  readonly clipIds: readonly string[];
  readonly members: readonly ClipSplitBatchMember[];
  readonly on: number;
  readonly basis: JsonObject;
  readonly port: ClipSplitBatchCapturePort;
}

/** Preserve original input order and strict-interior/no-op behavior before allocating identities. */
export function captureClipSplitBatchEdit(
  port: ClipSplitBatchCapturePort | undefined,
  current: TimelineData,
  clipIds: readonly string[],
  on: number,
  reserveRightId = (used: string[], clipId: string) => createSplitClipId(used, clipId),
): CapturedClipSplitBatchEdit | undefined {
  if (!Number.isFinite(on)) throw new Error('Split batch requires a finite playhead');
  const valid = Object.freeze([...new Set(clipIds.filter((id) => !id.startsWith('uploading-') && current.meta[id]))]);
  if (current.config.pinnedShotGroups?.some((group) => group.clipIds.some((id) => valid.includes(id)))) {
    throw new Error('Split batch cannot edit pinned group members');
  }
  const intersecting = new Set(current.rows.flatMap((row) => row.actions)
    .filter((action) => action.start <= on && on < action.end).map((action) => action.id));
  const eligible = valid.filter((id) => intersecting.has(id)
    && current.resolvedConfig.clips.some((clip) => clip.id === id && canSplitClipAtTime(clip, on)));
  if (!eligible.length) return undefined;
  if (!port) throw new Error('clip.split batch capture is unavailable.');
  const used = [...new Set([...current.config.clips, ...current.resolvedConfig.clips].map((clip) => clip.id))];
  const members = freezeJson(eligible.map((clipId) => {
    const rightId = reserveRightId([...used], clipId);
    used.push(rightId);
    return { clipId, rightId };
  }));
  const basis = freezeJson(structuredClone(port.capture({ clipIds: valid, members, on, current })));
  return Object.freeze({ clipIds: valid, members, on, basis, port });
}

export function submitClipSplitBatchEdit(captured: CapturedClipSplitBatchEdit): void {
  const { commands, preview } = captured.port.finish(captured.basis);
  if (commands.length !== captured.members.length || commands.some((command, index) =>
    command.schema_version !== 1 || command.op !== 'clip.split' || command.version !== '1'
    || command.select !== `parent/clip:${captured.members[index].clipId}`
    || !equal(command.args, { on: captured.on, right_id: captured.members[index].rightId }))) {
    throw new Error('Unsupported clip.split batch capture result.');
  }
  captured.port.submit({ commands: freezeJson(structuredClone(commands)), preview: freezeJson(structuredClone(preview)) });
}

export function clipSplitBatchPreview(splits: Array<{ clipId: string; left: JsonObject; right: JsonObject }>): TimelinePatch {
  return { version: 1, source: 'clip.split.batch', operations: splits.flatMap(({ clipId, left, right }) =>
    clipSplitPreview(clipId, left, right).operations) };
}

/** Build a temporary final candidate. The hook installs it only after all operations validate. */
export function projectClipSplitBatchPreview(patch: TimelinePatch, current: TimelineData): TimelineData | undefined {
  if (patch.source !== 'clip.split.batch') return undefined;
  const targets = patch.operations.map((operation) => operation.target);
  const created = patch.operations.map((operation) => object(operation.payload?.right) ? operation.payload.right.id : undefined);
  if (patch.version !== 1 || !patch.operations.length || new Set(targets).size !== targets.length
    || new Set(created).size !== created.length || created.some((id) => targets.includes(id as string))) {
    throw new Error('Invalid native clip.split batch preview');
  }
  let next = current;
  for (const operation of patch.operations) {
    next = projectClipSplitPreview({ version: 1, source: 'clip.split', operations: [operation] }, next)!;
  }
  return next;
}
