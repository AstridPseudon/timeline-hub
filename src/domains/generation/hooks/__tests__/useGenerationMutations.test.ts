import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import React from 'react';
import { queryKeys } from '@/shared/lib/queryKeys';

// Mock supabase
const mockIsDeferredCloudDataAuthority = vi.hoisted(() => vi.fn(() => true));
const mockFrom = vi.fn();
const mockRpc = vi.fn();
const mockResolveGenerationProjectScope = vi.fn();
const mockResolveVariantProjectScope = vi.fn();
vi.mock('@/integrations/supabase/client', () => ({
  getSupabaseClient: () => ({
    from: (...args: unknown[]) => mockFrom(...args),
    rpc: (...args: unknown[]) => mockRpc(...args),
  }),
}));

vi.mock('@/shared/lib/tasks/generationTaskRepository', () => ({
  resolveGenerationProjectScope: (...args: unknown[]) => mockResolveGenerationProjectScope(...args),
  resolveVariantProjectScope: (...args: unknown[]) => mockResolveVariantProjectScope(...args),
}));

vi.mock('@/shared/lib/errorHandling/runtimeError', () => ({
  normalizeAndPresentError: vi.fn(),
  normalizeAndPresentAndRethrow: (error: unknown) => {
    if (error instanceof Error) {
      throw error;
    }
    const message = (
      error
      && typeof error === 'object'
      && 'message' in error
      && typeof (error as { message?: unknown }).message === 'string'
    )
      ? (error as { message: string }).message
      : String(error);
    throw new Error(message);
  },
}));

import { useDeleteGeneration, useDeleteVariant, useToggleGenerationStar } from '@/domains/generation/hooks/useGenerationMutations';

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

describe('useDeleteGeneration', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockResolveGenerationProjectScope.mockResolvedValue({
      generationId: 'gen-123',
      projectId: 'project-1',
      status: 'ok',
    });
  });

  it('rejects in Astrid authority before repository or client calls', async () => {

    const { wrapper } = createWrapper();
    const { result } = renderHook(() => useDeleteGeneration(), { wrapper });

    await expect(result.current.mutateAsync({ id: 'gen-123', projectId: 'project-1' }))
      .rejects.toMatchObject({ code: 'capability_unavailable' });

    expect(mockResolveGenerationProjectScope).not.toHaveBeenCalled();
    expect(mockFrom).not.toHaveBeenCalled();
  });
});

describe('useDeleteVariant', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockResolveVariantProjectScope.mockResolvedValue({
      variantId: 'variant-123',
      generationId: 'gen-123',
      projectId: 'project-1',
      status: 'ok',
    });
  });

  it('rejects in Astrid authority before repository or client calls', async () => {

    const { wrapper } = createWrapper();
    const { result } = renderHook(() => useDeleteVariant(), { wrapper });

    await expect(result.current.mutateAsync({ id: 'variant-123', projectId: 'project-1' }))
      .rejects.toMatchObject({ code: 'capability_unavailable' });

    expect(mockResolveVariantProjectScope).not.toHaveBeenCalled();
    expect(mockFrom).not.toHaveBeenCalled();
  });
});

describe('useToggleGenerationStar', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockResolveGenerationProjectScope.mockResolvedValue({
      generationId: 'gen-123',
      projectId: 'project-1',
      status: 'ok',
    });
  });

  it('rejects in Astrid authority without optimistic cache drift or repository calls', async () => {
    const { wrapper, queryClient } = createWrapper();
    const key = queryKeys.unified.byProject('project-1', 1, 50, null, false);
    const previous = {
      items: [{ id: 'gen-123', starred: false }],
    };
    queryClient.setQueryData(key, previous);

    const { result } = renderHook(() => useToggleGenerationStar(), { wrapper });

    await expect(result.current.mutateAsync({
      id: 'gen-123',
      starred: true,
      projectId: 'project-1',
    })).rejects.toMatchObject({ code: 'capability_unavailable' });

    expect(queryClient.getQueryData(key)).toEqual(previous);
    expect(mockResolveGenerationProjectScope).not.toHaveBeenCalled();
    expect(mockFrom).not.toHaveBeenCalled();
  });
});
