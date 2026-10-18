/**
 * Deterministic Runaway rows for browser gates, ported verbatim from the retired timeline bridge stub
 * (only types and exports added). The real Runtime's typed lane contract is paginated even when this
 * fixture fits in one page; keeping that envelope catches protocol and header regressions instead of
 * letting a browser gate silently fall back to an empty lane.
 *
 * Not a Runtime-recorded route: no recording exists for `runaway-transitions`, so this is held only by
 * the App's own client (`runawayTimelineData.ts`) and `server.contract.test.mjs`.
 */

const RUNAWAY_TOTAL_COUNT = 566;
const RUNAWAY_SCALE_COUNTS = new Map<string, number>([
  ['runaway-scale-5000', 5_000],
  ['runaway-scale-50000', 50_000],
]);
const RUNAWAY_PAGE_LIMIT = 1_000;
const RUNAWAY_FPS = 48;
const RUNAWAY_FRAME_COUNT = 8_085;
const RUNAWAY_SNAPSHOT = 'runaway-v1:deterministic-browser-stub';

function frameToMs(frame: number): number {
  return Math.round((frame * 1000) / RUNAWAY_FPS);
}

const runawayTransitionCache = new Map<number, Array<Record<string, unknown>>>();

function runawayTransitionsForCount(totalCount: number): Array<Record<string, unknown>> {
  const cached = runawayTransitionCache.get(totalCount);
  if (cached) return cached;
  const manifestWidth = totalCount >= 10_000 ? 5 : 4;
  const segmentSize = Math.ceil(totalCount / 10);
  const transitions = Array.from({ length: totalCount }, (_, index) => {
    const ordinal = index;
    // Spread the typed rows across the complete composition envelope. Keeping
    // the endpoints explicit matters: the final row is the final visible frame
    // (8084), while the composition itself contains 8085 frames (0..8084).
    const frame = Math.round(
      (index * (RUNAWAY_FRAME_COUNT - 1)) / (totalCount - 1),
    );
    const startMs = frameToMs(frame);
    const nextFrame = index + 1 < totalCount
      ? Math.round(
        ((index + 1) * (RUNAWAY_FRAME_COUNT - 1)) / (totalCount - 1),
      )
      : RUNAWAY_FRAME_COUNT;
    // Derive each duration from the same rounded frame-time endpoints as the
    // start. This keeps every duration positive and makes the sum exactly span
    // the declared composition envelope instead of accumulating per-row drift.
    const durationMs = Math.max(1, frameToMs(nextFrame) - startMs);
    const segmentNumber = Math.min(10, Math.floor(index / segmentSize) + 1);
    const isRose = index % 2 === 0;
    return {
      id: `runaway-stub-row-${String(index + 1).padStart(manifestWidth, '0')}`,
      run_id: 'runaway-stub-run-v1',
      task_id: null,
      ordinal,
      start_ms: startMs,
      duration_ms: durationMs,
      prompt: `${isRose ? 'rose' : 'teal'} neon piano chord, deterministic browser fixture`,
      metadata: {
        manifest_id: `T${String(index + 1).padStart(manifestWidth, '0')}`,
        segment_id: `S${String(segmentNumber).padStart(2, '0')}`,
        segment_label: `Runaway fixture region ${String(segmentNumber).padStart(2, '0')}`,
        timing_mode: index % 5 === 0 ? 'hard_cut' : 'hold',
        colour_name: isRose ? 'rose' : 'teal',
        colour_hex: isRose ? '#D47795' : '#26A7D0',
        frame,
        fps: RUNAWAY_FPS,
      },
      created_at: '2026-08-24T00:00:00Z',
    };
  });
  runawayTransitionCache.set(totalCount, transitions);
  return transitions;
}

export function runawayPage(url: URL): Record<string, unknown> {
  const project = url.pathname.split('/')[3] ?? 'runaway-browser-stub';
  const totalCount = RUNAWAY_SCALE_COUNTS.get(project) ?? RUNAWAY_TOTAL_COUNT;
  const runawayTransitions = runawayTransitionsForCount(totalCount);
  const requestedLimit = Number(url.searchParams.get('limit') || RUNAWAY_PAGE_LIMIT);
  const limit = Number.isSafeInteger(requestedLimit) && requestedLimit > 0
    ? Math.min(requestedLimit, RUNAWAY_PAGE_LIMIT)
    : RUNAWAY_PAGE_LIMIT;
  const requestedCursor = url.searchParams.get('cursor');
  const start = requestedCursor === null ? 0 : Number(requestedCursor);
  const offset = Number.isSafeInteger(start) && start >= 0 && start <= totalCount
    ? start
    : 0;
  const transitions = runawayTransitions.slice(offset, offset + limit);
  const nextOffset = offset + transitions.length;
  return {
    api_version: 'v1',
    project,
    count: transitions.length,
    total_count: totalCount,
    snapshot: RUNAWAY_SNAPSHOT,
    page: {
      // The client contract fixes the bridge page limit at 1000.  A smaller
      // request is only a useful harness convenience; it must not change the
      // declared wire contract.
      limit: RUNAWAY_PAGE_LIMIT,
      next_cursor: nextOffset < totalCount ? String(nextOffset) : null,
    },
    timing_summary: {
      evidence_id: 'runaway-stub-evidence-v1',
      run_id: 'runaway-stub-run-v1',
      summary: 'Deterministic Runaway browser fixture',
      created_at: '2026-08-24T00:00:00Z',
      data: {
        frame_count: RUNAWAY_FRAME_COUNT,
        transition_count: totalCount,
        fps: RUNAWAY_FPS,
        segment_counts: Object.fromEntries(
          Array.from({ length: 10 }, (_, index) => [
            `S${String(index + 1).padStart(2, '0')}`,
            index === 9 ? totalCount - 9 * Math.ceil(totalCount / 10) : Math.ceil(totalCount / 10),
          ]),
        ),
      },
    },
    transitions,
  };
}
