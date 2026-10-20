/**
 * Persisted Runaway source items for browser specs: the 566 typed transitions a reloaded project would
 * carry in its bundle, spread over frames 0..8084 of an 8085-frame 48 fps composition. Seeded through
 * `publishFakeRuntimeComposition`, the same path a saved project takes, so the Runaway fixture
 * extension's lane renders them with no host-side loader involved.
 */
import type { RunawayTransitionPayload } from '../../../src/tools/video-editor/dev/runaway-timeline/runawayTimelineData.ts';
import { publishFakeRuntimeComposition, transcriptBundle, type SeededTranscriptSegment } from './support';

export const RUNAWAY_SCHEMA_REF = 'astrid.runaway_transition/v1';
export const RUNAWAY_TRANSITION_COUNT = 566;
const RUNAWAY_FPS = 48;
const RUNAWAY_FRAME_COUNT = 8_085;

function frameToMs(frame: number): number {
  return Math.round((frame * 1000) / RUNAWAY_FPS);
}

/** The 566 typed transitions spread over frames 0..8084 of an 8085-frame 48 fps composition. */
export function runawaySourceItems() {
  const segmentSize = Math.ceil(RUNAWAY_TRANSITION_COUNT / 10);
  const segmentCounts = Object.fromEntries(Array.from({ length: 10 }, (_, index) => [
    `S${String(index + 1).padStart(2, '0')}`,
    index === 9 ? RUNAWAY_TRANSITION_COUNT - 9 * segmentSize : segmentSize,
  ]));
  const timingSummary = {
    evidenceId: 'runaway-e2e-evidence',
    runId: 'runaway-e2e-run',
    summary: 'Deterministic Runaway browser fixture',
    frameCount: RUNAWAY_FRAME_COUNT,
    transitionCount: RUNAWAY_TRANSITION_COUNT,
    fps: RUNAWAY_FPS,
    segmentCounts,
  };
  return Array.from({ length: RUNAWAY_TRANSITION_COUNT }, (_, index) => {
    const frameAt = (position: number) => Math.round((position * (RUNAWAY_FRAME_COUNT - 1)) / (RUNAWAY_TRANSITION_COUNT - 1));
    const frame = frameAt(index);
    const startMs = frameToMs(frame);
    const nextFrame = index + 1 < RUNAWAY_TRANSITION_COUNT ? frameAt(index + 1) : RUNAWAY_FRAME_COUNT;
    const durationMs = Math.max(1, frameToMs(nextFrame) - startMs);
    const manifestId = `T${String(index + 1).padStart(4, '0')}`;
    const segmentNumber = Math.min(10, Math.floor(index / segmentSize) + 1);
    const isRose = index % 2 === 0;
    const payload = {
      id: `runaway-e2e-row-${manifestId}`,
      manifestId,
      ordinal: index,
      runId: 'runaway-e2e-run',
      taskId: null,
      startMs,
      durationMs,
      prompt: `${isRose ? 'rose' : 'teal'} neon piano chord, deterministic browser fixture`,
      segmentId: `S${String(segmentNumber).padStart(2, '0')}`,
      segmentLabel: `Runaway fixture region ${String(segmentNumber).padStart(2, '0')}`,
      timingMode: index % 5 === 0 ? 'hard_cut' : 'hold',
      colourName: isRose ? 'rose' : 'teal',
      colourHex: isRose ? '#D47795' : '#26A7D0',
      frame,
      fps: RUNAWAY_FPS,
      metadata: {},
      timingSummary,
    } satisfies RunawayTransitionPayload;
    return {
      id: manifestId,
      shape: 'interval',
      domain: 'timeline_seconds',
      extent: { start: startMs / 1000, end: (startMs + durationMs) / 1000 },
      schemaRef: RUNAWAY_SCHEMA_REF,
      payload,
      sourceArtifactRef: { assetId: 'astrid:runaway-timing:runaway-e2e' },
      provenance: { adapterId: 'astrid.runaway.e2e', adapterVersion: '1' },
    };
  });
}

/** One persisted bundle carrying the Runaway items and, optionally, transcript segments for one asset. */
export function composedExtensionBundle(transcript?: { segments: readonly SeededTranscriptSegment[]; assetId: string }) {
  const bundle = transcript
    ? transcriptBundle(transcript.segments, transcript.assetId)
    : { schema_version: 1, itemsBySchemaRef: {} as Record<string, unknown[]> };
  return {
    ...bundle,
    itemsBySchemaRef: { ...bundle.itemsBySchemaRef, [RUNAWAY_SCHEMA_REF]: runawaySourceItems() },
  };
}

/**
 * Publish the composed-extension world the dedicated extension specs measure: `segments` as the transcript
 * of the carrier clip's asset plus the 566 Runaway transitions, as one persisted bundle. Call after the
 * shared reset, before opening the editor.
 */
export function publishComposedExtensions(
  segments: readonly SeededTranscriptSegment[],
  assetId: string = 'demo-clip',
) {
  return publishFakeRuntimeComposition(({ config }) => {
    config.bundle = composedExtensionBundle({ segments, assetId });
  });
}
