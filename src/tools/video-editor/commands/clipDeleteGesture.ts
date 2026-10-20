import type { EditCommand } from '@/integrations/runtime/timeline-commit-types.ts';
import type { TimelinePatch } from '@/sdk/video/timeline/patch.ts';
import type { TimelineData } from '../lib/timeline-data.ts';
import { equal, freezeJson } from './clipMovePrimitives.ts';
import type { JsonObject } from './types.ts';

export interface ClipDeleteCapturePort {
  capture(input: { clipId: string; current: TimelineData }): JsonObject;
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
): CapturedClipDeleteEdit {
  if (!port) throw new Error('clip.delete capture is unavailable.');
  if (current.resolvedConfig.clips.filter((clip) => clip.id === clipId).length !== 1) {
    throw new Error('clip.delete requires an unambiguous clip identity.');
  }
  const basis = freezeJson(structuredClone(port.capture({ clipId, current })));
  return Object.freeze({ clipId, basis, port });
}

export function submitClipDeleteEdit(captured: CapturedClipDeleteEdit): void {
  const { command } = captured.port.finish(captured.basis);
  if (command.schema_version !== 1 || command.op !== 'clip.delete' || command.version !== '1'
    || command.select !== `parent/clip:${captured.clipId}` || !equal(command.args, {})) {
    throw new Error('Unsupported clip.delete capture result.');
  }
  captured.port.submit({
    command: freezeJson(structuredClone(command)),
    preview: { version: 1, operations: [{ op: 'clip.remove', target: captured.clipId }] },
  });
}
