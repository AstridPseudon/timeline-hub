import { describe, expect, it } from 'vitest';
import { getLegacyAutoPlacementPresentation } from './legacyAutoPlacementPresentation';

const retiredCompletionResultData = {
  completion_follow_up: {
    status: 'degraded',
    recorded_at: '2026-10-20T00:00:00.000Z',
    issues: [{
      step: 'timeline_placement',
      code: 'automatic_timeline_placement_retired',
      message: 'Task output was saved; automatic timeline placement is no longer supported.',
    }],
  },
};

describe('getLegacyAutoPlacementPresentation', () => {
  it('shows the retired completion marker while retaining the task asset', () => {
    expect(getLegacyAutoPlacementPresentation({
      id: 'task-marker',
      status: 'Complete',
      params: {},
      resultData: retiredCompletionResultData,
      hasAsset: true,
    })).toEqual({
      taskId: 'task-marker',
      label: 'Not placed: place manually',
      assetRetained: true,
      action: 'place-manually',
    });
  });

  it('does not infer a placement outcome from a reachable old request', () => {
    expect(getLegacyAutoPlacementPresentation({
      id: 'task-intent',
      status: 'Complete',
      params: { placement_intent: { timeline_id: 'old-timeline', anchor_clip_id: 'old-clip' } },
      hasAsset: true,
    })).toBeNull();
  });

  it('keeps the presentation scoped to the task and output item', () => {
    const first = getLegacyAutoPlacementPresentation({
      id: 'task-a',
      status: 'Complete',
      params: { timeline_placement: { target_track: 'old-track' } },
      hasAsset: true,
    });
    const second = getLegacyAutoPlacementPresentation({
      id: 'task-b',
      status: 'Complete',
      params: {},
      resultData: retiredCompletionResultData,
      hasAsset: true,
    });

    expect(first).toBeNull();
    expect(second?.taskId).toBe('task-b');
    expect(first).not.toBe(second);
  });

  it('does not label modern pending or succeeded tasks without the old marker', () => {
    expect(getLegacyAutoPlacementPresentation({
      id: 'task-modern-pending',
      status: 'In Progress',
      params: { generation_intent: { output_selection: { variant_key: 'v1' } } },
      hasAsset: false,
    })).toBeNull();
    expect(getLegacyAutoPlacementPresentation({
      id: 'task-modern-succeeded',
      status: 'Complete',
      params: { generation_intent: { output_selection: { variant_key: 'v1' } } },
      hasAsset: true,
    })).toBeNull();
  });

  it('does not paint a failed placement or a failed task as success', () => {
    expect(getLegacyAutoPlacementPresentation({
      id: 'task-failed',
      status: 'Failed',
      params: { placement_intent: { timeline_id: 'old-timeline' } },
      resultData: retiredCompletionResultData,
      hasAsset: true,
    })).toBeNull();
    expect(getLegacyAutoPlacementPresentation({
      id: 'task-no-asset',
      status: 'Complete',
      params: { placement_intent: { timeline_id: 'old-timeline' } },
      hasAsset: false,
    })).toBeNull();
  });

  // Original successful completion fixtures from origin/main's handler.test.ts:
  // both save a clip and leave params intact without persisting follow-up issues.
  it.each([
    { timeline_placement: {
      timeline_id: 'timeline-1', source_clip_id: 'clip-source-1', target_track: 'V1',
      insertion_time: 12.5, intent: 'after_source',
    } },
    { placement_intent: {
      timeline_id: 'timeline-1', anchor_clip_id: 'clip-source-1',
      anchor_generation_id: 'gen-source-1', anchor_variant_id: 'variant-source-1',
      relation: 'after', preferred_track_id: 'V1', fallback_at: 22.25, fallback_track_id: 'V1',
    } },
  ])('does not call successfully placed history unplaced for %j', (params) => {
    expect(getLegacyAutoPlacementPresentation({
      id: 'task-1', status: 'Complete', params, resultData: {}, hasAsset: true,
    })).toBeNull();
  });

  it('does not classify a request by retained generation parameters', () => {
    expect(getLegacyAutoPlacementPresentation({
      id: 'task-bound', status: 'Complete', hasAsset: true,
      params: {
        placement_intent: { timeline_id: 'old-timeline', anchor_clip_id: 'old-clip' },
        generation_intent: { output_selection: { variant_key: 'v1' } },
      },
    })).toBeNull();
  });
});
