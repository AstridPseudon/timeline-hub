import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import React from 'react';

// Mock supabase
const mockFrom = vi.fn();
const mockRpc = vi.fn();
const mockIsDeferredCloudDataAuthority = vi.hoisted(() => vi.fn(() => true));
vi.mock('@/integrations/supabase/client', () => ({
  getSupabaseClient: () => ({
    from: (...args: unknown[]) => mockFrom(...args),
    rpc: (...args: unknown[]) => mockRpc(...args),
  }),
}));

vi.mock('@/shared/hooks/invalidation/useGenerationInvalidation', () => ({
  enqueueGenerationsInvalidation: vi.fn(),
}));

vi.mock('@/shared/constants/supabaseErrors', () => ({
  isNotFoundError: (err: { code?: string }) => err?.code === 'PGRST116',
}));

import { useDeleteShot } from '../useShotsCrud';

function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false, gcTime: 0 } },
  });
  return {
    queryClient,
    wrapper: ({ children }: { children: React.ReactNode }) =>
      React.createElement(QueryClientProvider, { client: queryClient }, children),
  };
}

describe('useDeleteShot', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('rejects in Astrid before Supabase or optimistic cache effects', async () => {
    const { wrapper, queryClient } = createWrapper();
    const key = ['shots', 'project-1'];
    const previous = [{ id: 'shot-1', name: 'Shot 1' }];
    queryClient.setQueryData(key, previous);
    const { result } = renderHook(() => useDeleteShot(), { wrapper });

    await expect(result.current.mutateAsync({ shotId: 'shot-1', projectId: 'project-1' }))
      .rejects.toMatchObject({ code: 'capability_unavailable' });

    expect(mockFrom).not.toHaveBeenCalled();
    expect(queryClient.getQueryData(key)).toEqual(previous);
  });
});
