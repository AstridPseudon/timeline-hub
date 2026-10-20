import type { EditCommand } from '@/integrations/runtime/timeline-commit-types.ts';
import type { TimelinePatch } from '@/sdk/video/timeline/patch.ts';
import { assembleTimelineData, type TimelineData } from '../lib/timeline-data.ts';
import { assertFiniteJson, equal, freezeJson } from './clipMovePrimitives.ts';
import type { JsonObject } from './types.ts';

export interface ClipDeleteCapturePort {
  capture(input: { clipId: string; current: TimelineData; ownerRef: 'parent' }): JsonObject;
  finish(basis: JsonObject): { command: EditCommand };
  submit(input: { command: EditCommand; preview: TimelinePatch }): void;
}

export interface CapturedClipDeleteEdit {
  readonly clipId: string;
  readonly basis: JsonObject;
  readonly port: ClipDeleteCapturePort;
}

export function captureClipDeleteEdit(
  port: ClipDeleteCapturePort | undefined,
  current: TimelineData,
  clipId: string,
  ownerRef: 'parent',
): CapturedClipDeleteEdit {
  if (!port) throw new Error('clip.delete capture is unavailable.');
  if (current.resolvedConfig.clips.filter((clip) => clip.id === clipId).length !== 1) {
    throw new Error('clip.delete requires an unambiguous clip identity.');
  }
  const result = port.capture({ clipId, current, ownerRef });
  assertFiniteJson(result);
  const basis = freezeJson(structuredClone(result));
  return Object.freeze({ clipId, basis, port });
}

export function submitClipDeleteEdit(captured: CapturedClipDeleteEdit): void {
  const { command } = captured.port.finish(captured.basis);
  assertFiniteJson(command);
  if (command.schema_version !== 1 || command.op !== 'clip.delete' || command.version !== '1'
    || command.select !== `parent/clip:${captured.clipId}` || !equal(command.args, {})) {
    throw new Error('Unsupported clip.delete capture result.');
  }
  captured.port.submit({
    command: freezeJson(structuredClone(command)),
    preview: clipDeletePreview(captured.clipId),
  });
}

export function clipDeletePreview(clipId: string): TimelinePatch {
  return { version: 1, source: 'parentclip.delete', operations: [{ op: 'clip.remove', target: clipId }] };
}

/** Remove only the selected row; keep unrelated authored rows and local projection data verbatim. */
export function projectClipDeletePreview(patch: TimelinePatch, current: TimelineData): TimelineData | undefined {
  if (patch.source !== 'parentclip.delete') return undefined;
  assertFiniteJson(patch);
  const target = patch.operations[0]?.target;
  if (typeof target !== 'string' || !equal(patch, clipDeletePreview(target))
    || current.config.clips.filter((clip) => clip.id === target).length !== 1
    || current.resolvedConfig.clips.filter((clip) => clip.id === target).length !== 1) {
    throw new Error('Invalid native parent clip.delete preview');
  }
  const config = { ...current.config, clips: current.config.clips.filter((clip) => clip.id !== target) };
  const assembled = assembleTimelineData({ ...current, config,
    resolvedConfig: { ...current.resolvedConfig, clips: current.resolvedConfig.clips.filter((clip) => clip.id !== target) } });
  const base = current.editProjection?.kind === 'accepted' ? current.editProjection.head
    : current.head?.headRevisionId && current.head.headPublicationId
      ? { revisionId: current.head.headRevisionId, publicationId: current.head.headPublicationId } : undefined;
  return { ...current, ...assembled, dataLanes: current.dataLanes,
    editProjection: current.editProjection?.kind === 'local' ? current.editProjection
      : base ? { kind: 'local', base, generation: 0 } : undefined };
}
