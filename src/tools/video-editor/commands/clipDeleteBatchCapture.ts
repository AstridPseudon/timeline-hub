import type { EditCommand } from '@/integrations/runtime/timeline-commit-types.ts';
import { captureClipDelete, finishClipDelete } from './clipDeleteCapture.ts';
import { ClipMoveError, assertFiniteJson, copy, freezeJson, object } from './clipMovePrimitives.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';

export type ClipDeleteBatchMember = { readonly clipId: string; readonly ownerRef: 'parent' };
export type ClipDeleteBatchBasis = { readonly bundle: AuthoredBundle; readonly commands: readonly EditCommand[] };

function validateTargets(targets: readonly unknown[]): void {
  if (!targets.length || new Set(targets).size !== targets.length
    || targets.some((target) => typeof target !== 'string' || !/^parent\/clip:(?!.*::)[^/]+$/.test(target))) {
    throw new ClipMoveError('Delete batch requires distinct original parent clip identities');
  }
}

/** Each single-delete capture sees the preceding removal, including its collection order. */
export function captureClipDeleteBatch(bundle: AuthoredBundle, members: readonly ClipDeleteBatchMember[]): ClipDeleteBatchBasis {
  assertFiniteJson(bundle);
  assertFiniteJson(members);
  if (members.some((member) => !object(member) || member.ownerRef !== 'parent' || typeof member.clipId !== 'string')) {
    throw new ClipMoveError('Delete batch requires explicit parent ownership for every target');
  }
  const targets = members.map(({ clipId }) => `parent/clip:${clipId}`);
  validateTargets(targets);
  const snapshot = copy(bundle);
  let next = snapshot;
  const commands = targets.map((select) => {
    const result = finishClipDelete(captureClipDelete(next, select));
    next = result.bundle;
    return result.command;
  });
  return freezeJson({ bundle: snapshot, commands });
}

/** Replay fixed original claims on isolated bytes; a later refusal cannot publish an earlier removal. */
export function executeClipDeleteBatch(bundle: AuthoredBundle, commands: readonly EditCommand[]) {
  assertFiniteJson(bundle);
  assertFiniteJson(commands);
  validateTargets(commands.map((command) => command.select));
  let next = copy(bundle);
  const results = commands.map((command, ordinal) => {
    const result = finishClipDelete({ bundle: next, command });
    next = result.bundle;
    return { ...result, record: { ...result.record, ordinal,
      derived_writes: result.record.derived_writes.map((write) => ({ ...write, cause: ordinal })) } };
  });
  return { bundle: next, commands: results.map((result) => result.command), records: results.map((result) => result.record) };
}

export function finishClipDeleteBatch(basis: unknown) {
  assertFiniteJson(basis);
  if (!object(basis) || !object(basis.bundle) || !Array.isArray(basis.commands) || !basis.commands.every(object)) {
    throw new ClipMoveError('incomplete clip delete batch basis');
  }
  return executeClipDeleteBatch(basis.bundle as AuthoredBundle, basis.commands as EditCommand[]);
}
