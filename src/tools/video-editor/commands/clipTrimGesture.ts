import type { EditCommand } from '@/integrations/runtime/timeline-commit-types.ts';
import type { TimelinePatch } from '@/sdk/video/timeline/patch.ts';
import type { TimelineData } from '../lib/timeline-data.ts';
import { equal, freezeJson } from './clipMovePrimitives.ts';
import type { ClipTrimArgs } from './clipTrimCapture.ts';
import type { JsonObject } from './types.ts';

export interface ClipTrimCapturePort {
  capture(input: { clipId: string; current: TimelineData }): JsonObject;
  finish(basis: JsonObject, args: ClipTrimArgs): { command: EditCommand; preview: TimelinePatch };
  submit(input: { command: EditCommand; preview: TimelinePatch }): void;
}

export interface CapturedClipTrim {
  readonly clipId: string;
  readonly basis: JsonObject;
  readonly port: ClipTrimCapturePort;
}

/** Capture at gesture begin, or immediately before a discrete source-window edit. */
export function captureClipTrimEdit(port: ClipTrimCapturePort | undefined, current: TimelineData, clipId: string): CapturedClipTrim {
  if (!port) throw new Error('clip.trim capture is unavailable.');
  if (current.resolvedConfig.clips.filter((clip) => clip.id === clipId).length !== 1) {
    throw new Error('clip.trim requires an unambiguous clip identity.');
  }
  const basis = freezeJson(structuredClone(port.capture({ clipId, current })));
  return Object.freeze({ clipId, basis, port });
}

/** Endpoints are source seconds; the native operation owns precision and hold. */
export function submitClipTrimEdit(captured: CapturedClipTrim, args: ClipTrimArgs): void {
  const { command, preview } = captured.port.finish(captured.basis, args);
  if (command.schema_version !== 1 || command.op !== 'clip.trim' || command.version !== '1'
    || command.select !== `parent/clip:${captured.clipId}`
    || !equal(command.args, { in_s: args.in_s ?? null, out_s: args.out_s ?? null })) {
    throw new Error('Unsupported clip.trim capture result.');
  }
  captured.port.submit({ command: freezeJson(structuredClone(command)), preview: freezeJson(structuredClone(preview)) });
}

