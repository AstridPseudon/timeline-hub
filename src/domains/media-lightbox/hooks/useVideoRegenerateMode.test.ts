// @vitest-environment jsdom

import { renderHook } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { useVideoRegenerateMode } from './useVideoRegenerateMode';

type Params = Parameters<typeof useVideoRegenerateMode>[0];

function buildParams(overrides: Partial<Params> = {}): Params {
  return {
    isVideo: true,
    media: {
      id: 'child-video',
      parent_generation_id: 'parent-video',
      params: { segment_index: 1 },
      metadata: {},
    } as never,
    shotId: 'shot-1',
    selectedProjectId: 'project-1',
    actualGenerationId: 'child-video',
    adjustedTaskDetailsData: undefined,
    primaryVariant: null,
    variantParamsToLoad: null,
    setVariantParamsToLoad: () => {},
    ...overrides,
  };
}

describe('useVideoRegenerateMode', () => {
  it('cannot regenerate a root parent video or a non-video', () => {
    const rootParent = renderHook(() => useVideoRegenerateMode(buildParams({
      media: { id: 'parent-video', params: { segment_index: 0 }, metadata: {} } as never,
    })));
    expect(rootParent.result.current.canRegenerate).toBe(false);
    expect(rootParent.result.current.regenerateFormProps).toBeNull();

    const image = renderHook(() => useVideoRegenerateMode(buildParams({ isVideo: false })));
    expect(image.result.current.canRegenerate).toBe(false);
    expect(image.result.current.regenerateFormProps).toBeNull();
  });

  it('cannot regenerate join-clips outputs', () => {
    const { result } = renderHook(() => useVideoRegenerateMode(buildParams({
      media: {
        id: 'joined',
        parent_generation_id: 'parent-video',
        params: { tool_type: 'join-clips' },
        metadata: {},
      } as never,
    })));

    expect(result.current.canRegenerate).toBe(false);
  });

  it('builds the form props from the media params and falls back to the default structure type outside slot mode', () => {
    const { result } = renderHook(() => useVideoRegenerateMode(buildParams({
      currentSegmentImages: {
        startUrl: 'https://cdn.example.com/start.png',
        endUrl: 'https://cdn.example.com/end.png',
        startGenerationId: 'gen-start',
        endGenerationId: 'gen-end',
        startShotGenerationId: 'shot-gen-start',
      },
      currentFrameCount: 33,
    })));

    const props = result.current.regenerateFormProps;
    expect(result.current.canRegenerate).toBe(true);
    expect(props?.task).toMatchObject({
      projectId: 'project-1',
      generationId: 'parent-video',
      shotId: 'shot-1',
      segmentIndex: 1,
    });
    expect(props?.images).toMatchObject({
      startImageUrl: 'https://cdn.example.com/start.png',
      endImageUrl: 'https://cdn.example.com/end.png',
      startImageGenerationId: 'gen-start',
      endImageGenerationId: 'gen-end',
      pairShotGenerationId: 'shot-gen-start',
    });
    expect(props?.frame?.currentFrameCount).toBe(33);
    expect(props?.structure?.structureVideoType).toBe('flow');
    expect(props?.structure?.structureVideoDefaults).toBeUndefined();
    expect(props?.structure?.structureVideoUrl).toBeUndefined();
  });

  it('lets timeline slot mode own the structure video data and the segment images', () => {
    const { result } = renderHook(() => useVideoRegenerateMode(buildParams({
      segmentSlotMode: {
        pairData: {
          frames: 49,
          startImage: { id: 'slot-start', url: 'https://cdn.example.com/slot-start.png', generationId: 'slot-gen-start' },
          endImage: { id: 'slot-end', url: 'https://cdn.example.com/slot-end.png', generationId: 'slot-gen-end' },
        },
        structureVideoType: null,
        structureVideoUrl: 'https://cdn.example.com/guide.mp4',
        maxFrameLimit: 81,
      } as never,
    })));

    const props = result.current.regenerateFormProps;
    expect(props?.structure?.structureVideoType).toBeNull();
    expect(props?.structure?.structureVideoUrl).toBe('https://cdn.example.com/guide.mp4');
    expect(props?.images).toMatchObject({
      startImageUrl: 'https://cdn.example.com/slot-start.png',
      endImageGenerationId: 'slot-gen-end',
      pairShotGenerationId: 'slot-start',
    });
    expect(props?.frame).toMatchObject({ currentFrameCount: 49, maxFrames: 81 });
  });
});
