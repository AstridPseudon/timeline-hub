import type { EditCommand } from '@/integrations/runtime/timeline-commit-types.ts';
import { captureClipSplit, finishClipSplit } from './clipSplitCapture.ts';
import { ClipMoveError, assertFiniteJson, copy, freezeJson, object } from './clipMovePrimitives.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';

export type ClipSplitBatchMember = { readonly clipId: string; readonly rightId: string };
export type ClipSplitBatchBasis = { readonly bundle: AuthoredBundle; readonly commands: readonly EditCommand[] };

function validateSequence(commands: readonly EditCommand[]): void {
  if (!commands.length) throw new ClipMoveError('Split batch requires original targets');
  const targets = commands.map((command) => command.select);
  const created = commands.map((command) => command.args?.right_id);
  if (new Set(targets).size !== targets.length || new Set(created).size !== created.length
    || created.some((id) => targets.includes(`parent/clip:${id}`))
    || commands.some((command) => command.args?.on !== commands[0].args?.on)) {
    throw new ClipMoveError('Split batch requires distinct original targets and reserved IDs at one playhead');
  }
}

/** Each native capture observes the preceding split, including its new member and reads. */
export function captureClipSplitBatch(bundle: AuthoredBundle, members: readonly ClipSplitBatchMember[], on: number): ClipSplitBatchBasis {
  assertFiniteJson(members);
  assertFiniteJson(on);
  const snapshot = copy(bundle);
  let next = snapshot;
  const commands = members.map(({ clipId, rightId }) => {
    const result = finishClipSplit(captureClipSplit(next, `parent/clip:${clipId}`, { on, right_id: rightId }));
    next = result.bundle;
    return result.command;
  });
  validateSequence(commands);
  return freezeJson({ bundle: snapshot, commands });
}

/** Replay the complete fixed sequence on isolated bytes; no member refreshes its guards. */
export function executeClipSplitBatch(bundle: AuthoredBundle, commands: readonly EditCommand[]) {
  assertFiniteJson(bundle);
  assertFiniteJson(commands);
  validateSequence(commands);
  let next = copy(bundle);
  const results = commands.map((command, ordinal) => {
    const result = finishClipSplit({ bundle: next, command });
    next = result.bundle;
    // Native batch records attribute derived writes to the owning command ordinal.
    return { ...result, record: { ...result.record, ordinal,
      derived_writes: result.record.derived_writes.map((write) => ({ ...write, cause: ordinal })) } };
  });
  return { bundle: next, commands: results.map((result) => result.command), records: results.map((result) => result.record) };
}

export function finishClipSplitBatch(basis: unknown) {
  assertFiniteJson(basis);
  if (!object(basis) || !object(basis.bundle) || !Array.isArray(basis.commands) || !basis.commands.every(object)) {
    throw new ClipMoveError('incomplete clip split batch basis');
  }
  return executeClipSplitBatch(basis.bundle as AuthoredBundle, basis.commands as EditCommand[]);
}
