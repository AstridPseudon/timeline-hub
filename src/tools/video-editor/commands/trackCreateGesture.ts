import type { EditCommand } from '@/integrations/runtime/timeline-commit-types.ts';
import type { TimelinePatch } from '@/sdk/video/timeline/patch.ts';
import { assembleTimelineData, type TimelineData } from '../lib/timeline-data.ts';
import type { TrackDefinition } from '../types/index.ts';
import { assertFiniteJson, equal, freezeJson, object } from './clipMovePrimitives.ts';
import type { TrackCreateArgs } from './trackCreateCapture.ts';
import type { JsonObject } from './types.ts';

export interface TrackCreateCapturePort {
  capture(input: { row: TrackCreateArgs['row']; current: TimelineData }): JsonObject;
  finish(basis: JsonObject, args: TrackCreateArgs): { command: EditCommand; preview: TimelinePatch };
  submit(input: { command: EditCommand; preview: TimelinePatch }): void;
}

export interface CapturedTrackCreate {
  readonly row: TrackCreateArgs['row'];
  readonly basis: JsonObject;
  readonly port: TrackCreateCapturePort;
}

/** The caller allocates row.id once; retries reuse the complete authored row. */
export function captureTrackCreateEdit(
  port: TrackCreateCapturePort | undefined,
  current: TimelineData,
  row: TrackCreateArgs['row'],
): CapturedTrackCreate {
  if (!port) throw new Error('track.create capture is unavailable.');
  assertFiniteJson(row);
  const original = freezeJson(structuredClone(row));
  const basis = freezeJson(structuredClone(port.capture({ row: original, current })));
  return Object.freeze({ row: original, basis, port });
}

export function trackCreatePreview(row: TrackCreateArgs['row']): TimelinePatch {
  return { version: 1, source: 'track.create', operations: [{ op: 'track.add', target: row.id,
    payload: structuredClone(row) as Record<string, unknown> }] };
}

export function submitTrackCreateEdit(captured: CapturedTrackCreate): void {
  const { command, preview } = captured.port.finish(captured.basis, { row: captured.row });
  assertFiniteJson(command);
  assertFiniteJson(preview);
  if (command.schema_version !== 1 || command.op !== 'track.create' || command.version !== '1'
    || command.select !== 'parent' || !equal(command.args, { row: captured.row })
    || !equal(preview, trackCreatePreview(captured.row))) {
    throw new Error('Unsupported track.create capture result.');
  }
  captured.port.submit({ command: freezeJson(structuredClone(command)), preview: freezeJson(structuredClone(preview)) });
}

/** Keep the complete authored track row in the local display projection. */
export function projectTrackCreatePreview(patch: TimelinePatch, current: TimelineData): TimelineData | undefined {
  if (patch.source !== 'track.create') return undefined;
  assertFiniteJson(patch);
  const [operation] = patch.operations;
  const row = operation?.payload;
  if (patch.version !== 1 || patch.operations.length !== 1 || operation.op !== 'track.add'
    || !object(row) || row.id !== operation.target || !equal(patch, trackCreatePreview(row as TrackCreateArgs['row']))
    || current.config.tracks?.some((track) => track.id === row.id)
    || current.resolvedConfig.tracks.some((track) => track.id === row.id)) {
    throw new Error('Invalid native track.create preview');
  }
  const config = { ...current.config, tracks: [...(current.config.tracks ?? []),
    structuredClone(row) as unknown as TrackDefinition] };
  const resolvedConfig = { ...current.resolvedConfig,
    tracks: [...current.resolvedConfig.tracks, structuredClone(row) as unknown as TrackDefinition] };
  return assembleTimelineData({ ...current, config, resolvedConfig, output: current.output,
    registry: current.registry, assetMap: current.assetMap });
}
