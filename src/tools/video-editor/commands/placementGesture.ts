import type { EditCommand } from '@/integrations/runtime/timeline-commit-types.ts';
import type { TimelinePatch } from '@/sdk/video/timeline/patch.ts';
import type { TimelineData } from '../lib/timeline-data.ts';
import type { PlacementOwnership } from './placementCapture.ts';
import type { JsonObject } from './types.ts';

/** Explicit existing-media re-placement; the session owns capture and submission. */
export interface PlacementCapturePort {
  capture(input: { clipId: string; ownerRef: 'parent' | `occurrence:${string}`;
    ownership: PlacementOwnership; on: number; current: TimelineData }): JsonObject;
  finish(basis: JsonObject, on: number): { command: EditCommand; preview: TimelinePatch };
  submit(input: { command: EditCommand; preview: TimelinePatch }): void;
}
