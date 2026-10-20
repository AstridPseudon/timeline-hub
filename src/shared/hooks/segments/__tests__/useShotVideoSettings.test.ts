import { describe, it, expect, vi, beforeEach } from 'vitest';

import { renderHookWithProviders } from '@/test/test-utils';

const mockSingle = vi.fn();
const mockIsDeferredCloudDataAuthority = vi.hoisted(() => vi.fn(() => true));
vi.mock('@/integrations/supabase/client', () => ({
  getSupabaseClient: () => ({
    from: vi.fn(() => ({
      select: vi.fn(() => ({
        eq: vi.fn(() => ({
          single: () => mockSingle(),
        })),
      })),
    })),
  }),
}));

vi.mock('@/shared/lib/settingsMigration', () => ({
  readShotSettings: vi.fn((raw: unknown) => raw),
}));

vi.mock('@/shared/lib/errorHandling/runtimeError', () => ({
  normalizeAndPresentError: vi.fn(),
}));

vi.mock('@/shared/lib/tooling/toolIds', () => ({
  TOOL_IDS: { TRAVEL_BETWEEN_IMAGES: 'travel-between-images' },
}));

import { useShotVideoSettings } from '../useShotVideoSettings';
import { normalizeAndPresentError } from '@/shared/lib/errorHandling/runtimeError';

describe('useShotVideoSettings', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('returns null data when shotId is null', () => {
    const { result } = renderHookWithProviders(() => useShotVideoSettings(null));
    expect(result.current.data).toBeUndefined();
    expect(result.current.isLoading).toBe(false);
  });

  it('does not start a Supabase read in Astrid authority', () => {
    const { result } = renderHookWithProviders(() => useShotVideoSettings('shot-1'));
    expect(result.current.isLoading).toBe(false);
    expect(mockSingle).not.toHaveBeenCalled();
  });

  it('provides refetch function', () => {
    const { result } = renderHookWithProviders(() => useShotVideoSettings('shot-1'));
    expect(typeof result.current.refetch).toBe('function');
  });
});
