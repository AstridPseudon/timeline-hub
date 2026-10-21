import type { EditCommand } from '@/integrations/runtime/timeline-commit-types.ts';
import type { TimelinePatch } from '@/sdk/video/timeline/patch.ts';
import { assembleTimelineData, type TimelineData } from '../lib/timeline-data.ts';
import { createSplitClipId } from '../lib/editor-utils.ts';
import { equal, freezeJson, object } from './clipMovePrimitives.ts';
import type { JsonObject } from './types.ts';

export interface ClipSplitCapturePort {
  /** Routing only: known raw parent binding and supported shape, before capture. */
  supports?(input: { clipId: string; current: TimelineData }): boolean;
  capture(input: { clipId: string; on: number; rightId: string; current: TimelineData }): JsonObject;
  finish(basis: JsonObject): { command: EditCommand; preview: TimelinePatch };
  submit(input: { command: EditCommand; preview: TimelinePatch }): void;
}

/** Conservative ingress cohort; unsupported shapes retain their established writer. */
export function supportsParentClipSplit(rows: readonly JsonObject[], registry: JsonObject, clipId: string): boolean {
  const matches = rows.filter((row) => row.id === clipId);
  if (matches.length !== 1 || clipId.includes('/') || clipId.includes('::')) return false;
  const row = matches[0];
  const assets = registry.assets;
  const source = object(assets) && typeof row.asset === 'string' ? assets[row.asset] : undefined;
  if (row.clipType !== 'media' || !object(source) || typeof source.type !== 'string'
    || !['image', 'video', 'audio'].includes(source.type.trim().toLowerCase().split(';', 1)[0].split('/', 1)[0].split('-', 1)[0])) return false;
  if (['clip_type', 'asset_id', 'media_id', 'object_id', 'at_ms', 'from_ms', 'to_ms',
    'duration', 'duration_ms', 'time_map', 'timeMap', 'clips', 'children', 'transition', 'effects',
    'animation', 'animations', 'keyframes', 'enter', 'exit', 'continuous'].some((key) => row[key] != null)) return false;
  const params = row.params;
  if (object(params) && ['keyframes', 'animation', 'animations', 'effects', 'fade_in', 'fade_out',
    'volume_curve', 'fadeIn', 'fadeOut', 'fadeInCurve', 'fadeOutCurve'].some((key) => params[key] != null)) return false;
  const relations = ['on', 'until', 'until_film_end', 'cut', 'sequence', 'sequence_index', 'sequence_fit',
    'orphan', 'formulas', 'anchor', 'standin', 'standin_intent', 'words', 'beats'];
  const speed = row.speed ?? 1;
  const window = row.from != null || row.to != null;
  if (typeof row.at !== 'number' || row.at < 0 || typeof speed !== 'number' || speed <= 0
    || (window && (typeof row.from !== 'number' || typeof row.to !== 'number' || row.from < 0 || row.to <= row.from))
    || (!window && (source.type !== 'image' || typeof row.hold !== 'number' || row.hold <= 0))) return false;
  const duration = (typeof row.hold === 'number' ? row.hold : (row.to as number) - (row.from as number)) / speed;
  if (window && row.hold != null && Math.abs((row.hold as number) - ((row.to as number) - (row.from as number))) > 1e-9) return false;
  for (const container of [row, row.app, object(row.app) ? row.app.astrid : undefined]) {
    if (container == null) continue;
    if (!object(container) || relations.some((key) => container[key] != null)
      || (container.fixed_start != null && container.fixed_start !== true)
      || (container.for != null && (typeof container.for !== 'number' || Math.abs(container.for - duration) > 1e-9))) return false;
  }
  return rows.every((other) => other.id === clipId || other.transition == null);
}

/** Reserve once at the existing ID seam; the session persists this exact ID for retries. */
export function splitParentClip(port: ClipSplitCapturePort, current: TimelineData, clipId: string, on: number): string {
  const rightId = createSplitClipId([...current.config.clips, ...current.resolvedConfig.clips].map((clip) => clip.id), clipId);
  submitClipSplitEdit(captureClipSplitEdit(port, current, clipId, on, rightId));
  return rightId;
}

export interface CapturedClipSplitEdit {
  readonly clipId: string;
  readonly on: number;
  readonly rightId: string;
  readonly basis: JsonObject;
  readonly port: ClipSplitCapturePort;
}

/** The caller reserves the new identity once; native replay never allocates another one. */
export function captureClipSplitEdit(
  port: ClipSplitCapturePort | undefined,
  current: TimelineData,
  clipId: string,
  on: number,
  rightId: string,
): CapturedClipSplitEdit {
  if (!port) throw new Error('clip.split capture is unavailable.');
  if (current.resolvedConfig.clips.filter((clip) => clip.id === clipId).length !== 1) {
    throw new Error('clip.split requires an unambiguous clip identity.');
  }
  const basis = freezeJson(structuredClone(port.capture({ clipId, on, rightId, current })));
  return Object.freeze({ clipId, on, rightId, basis, port });
}

export function clipSplitPreview(clipId: string, left: JsonObject, right: JsonObject): TimelinePatch {
  return { version: 1, source: 'clip.split', operations: [{ op: 'clip.split', target: clipId,
    payload: { left: structuredClone(left), right: structuredClone(right) } }] };
}

export function submitClipSplitEdit(captured: CapturedClipSplitEdit): void {
  const { command, preview } = captured.port.finish(captured.basis);
  if (command.schema_version !== 1 || command.op !== 'clip.split' || command.version !== '1'
    || command.select !== `parent/clip:${captured.clipId}`
    || !equal(command.args, { on: captured.on, right_id: captured.rightId })) {
    throw new Error('Unsupported clip.split capture result.');
  }
  captured.port.submit({ command: freezeJson(structuredClone(command)), preview: freezeJson(structuredClone(preview)) });
}

/** Apply the complete native rows locally; the Runtime remains authoritative for acceptance. */
export function projectClipSplitPreview(patch: TimelinePatch, current: TimelineData): TimelineData | undefined {
  if (patch.source !== 'clip.split') return undefined;
  const [operation] = patch.operations;
  const payload = operation?.payload;
  const left = payload?.left;
  const right = payload?.right;
  if (patch.version !== 1 || patch.operations.length !== 1 || operation.op !== 'clip.split'
    || !object(payload) || !object(left) || !object(right)
    || !equal(Object.keys(payload).sort(), ['left', 'right'])
    || left.id !== operation.target || typeof left.id !== 'string' || typeof right.id !== 'string'
    || left.id === right.id || current.config.clips.filter((clip) => clip.id === operation.target).length !== 1
    || current.config.clips.some((clip) => clip.id === right.id)
    || current.resolvedConfig.clips.some((clip) => clip.id === right.id)) {
    throw new Error('Invalid native clip.split preview');
  }

  const existing = current.resolvedConfig.clips.find((clip) => clip.id === operation.target);
  const resolvedRow = (row: JsonObject) => (existing?.assetEntry === undefined
    ? structuredClone(row) : { ...structuredClone(row), assetEntry: existing.assetEntry }) as unknown as TimelineData['resolvedConfig']['clips'][number];
  const clips = current.config.clips.flatMap((clip) => clip.id === operation.target
    ? [structuredClone(left), structuredClone(right)] as unknown as TimelineData['config']['clips'] : [clip]);
  const resolvedClips = current.resolvedConfig.clips.flatMap((clip) => clip.id === operation.target
    ? [resolvedRow(left), resolvedRow(right)] : [clip]);
  const config = { ...current.config, clips };
  const resolvedConfig = { ...current.resolvedConfig, clips: resolvedClips };
  const assembled = assembleTimelineData({
    config, configVersion: current.configVersion, head: current.head, registry: current.registry,
    resolvedConfig, output: current.output, assetMap: current.assetMap,
    sourceItemsBySchemaRef: current.sourceItemsBySchemaRef, transcriptReferences: current.transcriptReferences,
  });
  const base = current.editProjection?.kind === 'accepted' ? current.editProjection.head
    : current.head?.headRevisionId && current.head.headPublicationId
      ? { revisionId: current.head.headRevisionId, publicationId: current.head.headPublicationId } : undefined;
  return { ...current, ...assembled, dataLanes: current.dataLanes,
    editProjection: current.editProjection?.kind === 'local' ? current.editProjection
      : base ? { kind: 'local', base, generation: 0 } : undefined };
}

