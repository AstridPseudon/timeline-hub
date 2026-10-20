import { describe, it, expect, vi, beforeEach } from 'vitest';

import { QueryClient } from '@tanstack/react-query';
import { renderHookWithProviders } from '@/test/test-utils';
import { shotQueryKeys } from '@/shared/lib/queryKeys/shots';

const {
  eqMock,
  fromMock,
  mockUpdate,
  normalizeAndPresentErrorMock,
  updateMock,
} = vi.hoisted(() => ({
  eqMock: vi.fn(),
  fromMock: vi.fn(),
  mockUpdate: vi.fn(),
  normalizeAndPresentErrorMock: vi.fn(),
  updateMock: vi.fn(),
}));
const mockIsDeferredCloudDataAuthority = vi.hoisted(() => vi.fn(() => true));

vi.mock('@/shared/lib/errorHandling/runtimeError', () => ({
  normalizeAndPresentError: normalizeAndPresentErrorMock,
}));

vi.mock('@/integrations/supabase/client', () => ({
  getSupabaseClient: () => ({
    from: fromMock,
  }),
}));

import { useUpdateShotName } from '../useShotUpdates';

function createQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: { retry: false, gcTime: Infinity, staleTime: 0 },
      mutations: { retry: false },
    },
  });
}

describe('useUpdateShotName', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    eqMock.mockImplementation(() => mockUpdate());
    updateMock.mockReturnValue({ eq: eqMock });
    fromMock.mockReturnValue({ update: updateMock });
    mockUpdate.mockResolvedValue({ error: null });
  });

  it('returns mutation object', () => {
    const { result } = renderHookWithProviders(() => useUpdateShotName());
    expect(typeof result.current.mutateAsync).toBe('function');
    expect(result.current.isPending).toBe(false);
  });

  it('rejects in Astrid before Supabase or optimistic cache effects', async () => {
    const queryClient = createQueryClient();
    const key = shotQueryKeys.list('proj-1', 0);
    const previous = [{ id: 'shot-1', name: 'Old Name' }];
    queryClient.setQueryData(key, previous);
    const { result } = renderHookWithProviders(() => useUpdateShotName(), { queryClient });

    await expect(result.current.mutateAsync({
      shotId: 'shot-1',
      name: 'New Name',
      projectId: 'proj-1',
    })).rejects.toMatchObject({ code: 'capability_unavailable' });

    expect(fromMock).not.toHaveBeenCalled();
    expect(queryClient.getQueryData(key)).toEqual(previous);
  });
});
