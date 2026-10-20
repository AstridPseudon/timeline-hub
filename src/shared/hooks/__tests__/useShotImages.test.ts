import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import React from 'react';

// Mock supabase
vi.mock('@/integrations/supabase/client', () => {
  const createSupabaseMockChain = () => {
    const chain: Record<string, ReturnType<typeof vi.fn>> = {};
    chain.select = vi.fn().mockReturnValue(chain);
    chain.eq = vi.fn().mockReturnValue(chain);
    chain.order = vi.fn().mockReturnValue(chain);
    chain.abortSignal = vi.fn().mockResolvedValue({ data: [], error: null });
    return chain;
  };

  return {
    getSupabaseClient: () => ({
      from: vi.fn(() => createSupabaseMockChain()),
    }),
  };
});

vi.mock('@/shared/lib/query/queryDefaults', () => ({
  QUERY_PRESETS: {
    realtimeBacked: { staleTime: 0 },
  },
  STANDARD_RETRY: 3,
  STANDARD_RETRY_DELAY: vi.fn(() => 1000),
}));

vi.mock('@/shared/lib/queryKeys', () => ({
  queryKeys: {
    generations: {
      byShot: (shotId: string) => ['generations', 'shot', shotId],
    },
    shots: {
      list: (projectId: string, limit: number) => ['shots', projectId, limit],
    },
  },
}));

vi.mock('@/shared/hooks/shots', () => ({
  mapShotGenerationToRow: vi.fn((sg: Record<string, unknown>) => ({
    id: sg.id,
    generation_id: sg.generation_id,
    timeline_frame: sg.timeline_frame,
  })),
}));

import { useShotImages, useTimelineImages, useUnpositionedImages, useVideoOutputs } from '@/shared/hooks/shots/useShotImages';

function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false, gcTime: 0 } },
  });
  return ({ children }: { children: React.ReactNode }) =>
    React.createElement(QueryClientProvider, { client: queryClient }, children);
}

describe('useShotImages', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('is disabled when shotId is null', () => {
    const { result } = renderHook(() => useShotImages(null), {
      wrapper: createWrapper(),
    });

    expect(result.current.data).toBeUndefined();
    expect(result.current.isFetching).toBe(false);
  });

  it('does not fetch relational shot images in Astrid authority', () => {
    const { result } = renderHook(() => useShotImages('shot-1'), {
      wrapper: createWrapper(),
    });

    expect(result.current.isFetching).toBe(false);
    expect(result.current.error).toBeNull();
  });

});

describe('useTimelineImages', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('is disabled when shotId is null', () => {
    const { result } = renderHook(() => useTimelineImages(null), {
      wrapper: createWrapper(),
    });

    expect(result.current.data).toBeUndefined();
  });
});

describe('useUnpositionedImages', () => {
  it('is disabled when shotId is null', () => {
    const { result } = renderHook(() => useUnpositionedImages(null), {
      wrapper: createWrapper(),
    });

    expect(result.current.data).toBeUndefined();
  });
});

describe('useVideoOutputs', () => {
  it('is disabled when shotId is null', () => {
    const { result } = renderHook(() => useVideoOutputs(null), {
      wrapper: createWrapper(),
    });

    expect(result.current.data).toBeUndefined();
  });
});
