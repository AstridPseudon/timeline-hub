import type { CommandRecord, EditCommand } from '@/integrations/runtime/timeline-commit-types.ts';
import type { TimelinePatch, TimelinePatchOperation } from '@/sdk/video/timeline/patch.ts';
import { assembleTimelineData, type TimelineData } from '../lib/timeline-data.ts';
import { captureClipSet, executeClipSet } from './clipScalarCapture.ts';
import { captureTrackLabel, finishTrackLabel, type TrackLabelArgs } from './trackLabelCapture.ts';
import { assertFiniteJson, copy, equal, freezeJson, object, type AuthoredBundle } from './clipMovePrimitives.ts';

export class GenericPatchRefusal extends Error {
  readonly intentions: Array<{ operationIndex: number; op: string; target: string; reason: string }>;

  constructor(patch: TimelinePatch, failures: Map<number, string>) {
    const intentions = patch.operations.map((operation, operationIndex) => ({
      operationIndex,
      op: operation.op,
      target: operation.target,
      reason: failures.get(operationIndex) ?? 'Not submitted because another patch member was refused',
    }));
    super(`Native patch refused: ${intentions.map((item) =>
      `${item.operationIndex} ${item.op} ${item.target}: ${item.reason}`).join('; ')}`);
    this.intentions = intentions;
  }
}

function supported(operation: TimelinePatchOperation): boolean {
  const payload = operation.payload;
  if (Object.keys(operation).some((key) => !['op', 'target', 'payload', 'order'].includes(key))
    || typeof operation.target !== 'string' || !operation.target
    || (operation.order !== undefined && !Number.isFinite(operation.order)) || !object(payload)) return false;
  if (operation.op === 'track.update') {
    return typeof payload.label === 'string' && Object.keys(payload).every((key) => key === 'label' || key === 'mode')
      && (!('mode' in payload) || payload.mode === 'merge');
  }
  return operation.op === 'clip.update' && equal(Object.keys(payload), ['hold'])
    && typeof payload.hold === 'number' && Number.isFinite(payload.hold) && payload.hold > 0;
}

function commandArgs(command: EditCommand): TrackLabelArgs {
  if (!object(command.args) || !object(command.args.values) || !Array.isArray(command.args.clear)) {
    throw new Error('Unsupported track.set command arguments');
  }
  return command.args as unknown as TrackLabelArgs;
}

function executeTrackSet(bundle: AuthoredBundle, command: EditCommand, ordinal = 0) {
  if (command.op !== 'track.set' || typeof command.select !== 'string') {
    throw new Error('Unsupported native patch member');
  }
  const result = finishTrackLabel(captureTrackLabel(bundle, command.select), commandArgs(command));
  if (!equal(result.command, command)) throw new Error('Submitted track.set does not match its captured claims');
  result.record.ordinal = ordinal;
  result.record.derived_writes.forEach((write) => { write.cause = ordinal; });
  return result;
}

export function executeGenericPatch(bundle: AuthoredBundle, commands: readonly EditCommand[]) {
  let after = copy(bundle);
  const records: CommandRecord[] = [];
  for (const [ordinal, command] of commands.entries()) {
    const result = command.op === 'track.set'
      ? executeTrackSet(after, command, ordinal)
      : command.op === 'clip.set'
        ? executeClipSet(after, command, ordinal)
        : (() => { throw new Error('Unsupported native patch member'); })();
    after = result.bundle;
    records.push(result.record);
  }
  return { bundle: after, records };
}

/** Only merge-mode label SET and positive hold SET; ownership comes from the host resolver. */
export function captureGenericPatch(
  bundle: AuthoredBundle,
  patch: TimelinePatch,
  resolve: (operation: TimelinePatchOperation) => string,
) {
  assertFiniteJson(patch);
  const original = freezeJson(copy(patch));
  const failures = new Map<number, string>();
  original.operations.forEach((operation, index) => {
    if (!supported(operation)) failures.set(index,
      'Requires a parent label-only merge or exact positive hold SET');
  });
  if (!original.operations.length || !Number.isSafeInteger(original.version) || original.version < 0) {
    throw new Error('Native patch requires operations and a non-negative integer version');
  }
  if (failures.size) throw new GenericPatchRefusal(original, failures);
  const owners = original.operations.map((operation, index) => {
    try { return resolve(operation); }
    catch (error) {
      failures.set(index, error instanceof Error ? error.message : String(error));
      return '';
    }
  });
  if (failures.size) throw new GenericPatchRefusal(original, failures);

  const ordered = original.operations.map((operation, index) => ({ operation, index })).sort((a, b) => {
    if (a.operation.order === undefined) return b.operation.order === undefined ? a.index - b.index : 1;
    if (b.operation.order === undefined) return -1;
    return a.operation.order - b.operation.order || a.index - b.index;
  });
  let after = copy(bundle);
  const commands: EditCommand[] = [];
  const records: CommandRecord[] = [];
  for (const { operation, index } of ordered) {
    try {
      const result = operation.op === 'track.update'
        ? finishTrackLabel(captureTrackLabel(after, owners[index]), {
          values: { label: operation.payload!.label as string }, clear: [],
        })
        : executeClipSet(after, captureClipSet(after, owners[index], {
          values: { hold: operation.payload!.hold as number },
        }), commands.length);
      result.record.ordinal = commands.length;
      result.record.derived_writes.forEach((write) => { write.cause = commands.length; });
      after = result.bundle;
      commands.push(result.command);
      records.push(result.record);
    } catch (error) {
      failures.set(index, error instanceof Error ? error.message : String(error));
    }
  }
  if (failures.size) throw new GenericPatchRefusal(original, failures);
  const preview: TimelinePatch = {
    version: 1,
    source: 'timeline.native-label-hold',
    operations: ordered.map(({ operation }) => ({
      op: operation.op,
      target: operation.target,
      payload: operation.op === 'track.update'
        ? { label: operation.payload!.label }
        : { hold: operation.payload!.hold },
    })),
  };
  return freezeJson({ patch: original, owners, commands, records, bundle: after, preview });
}

export type GenericPatchBasis = {
  readonly current: TimelineData;
  readonly capture: ReturnType<typeof captureGenericPatch>;
  readonly localGeneration: number;
  readonly localBasis: import('./commitOutbox.ts').OutboxBasis;
};

export interface GenericPatchCapturePort {
  capture(input: { patch: TimelinePatch; current: TimelineData }): GenericPatchBasis;
  finish(basis: GenericPatchBasis): { commands: EditCommand[]; preview: TimelinePatch };
  submit(input: { commands: EditCommand[]; preview: TimelinePatch }): void;
}

/** One local projection, preserving exact authored values and unrelated display state. */
export function projectGenericPatchPreview(patch: TimelinePatch, current: TimelineData): TimelineData | undefined {
  if (patch.source !== 'timeline.native-label-hold') return undefined;
  assertFiniteJson(patch);
  if (patch.version !== 1 || !patch.operations.length || patch.operations.some((operation) => !supported(operation))) {
    throw new Error('Invalid native patch preview');
  }
  const config = copy(current.config);
  const resolvedConfig = copy(current.resolvedConfig);
  for (const operation of patch.operations) {
    for (const target of [config, resolvedConfig]) {
      const rows = operation.op === 'track.update' ? target.tracks ?? [] : target.clips;
      const matches = rows.filter((row) => row.id === operation.target);
      if (matches.length !== 1) throw new Error('Native patch preview requires one displayed target');
      Object.assign(matches[0], copy(operation.payload));
    }
  }
  return { ...current, ...assembleTimelineData({ ...current, config, resolvedConfig }), dataLanes: current.dataLanes };
}
