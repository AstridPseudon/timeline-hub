import { beforeEach, describe, expect, it, vi } from 'vitest';

const mockMaybeSingle = vi.fn();
const queryBuilder = {
  eq: vi.fn(() => queryBuilder),
  maybeSingle: (...args: unknown[]) => mockMaybeSingle(...args),
};
const mockSelect = vi.fn(() => queryBuilder);
const mockFrom = vi.fn(() => ({ select: mockSelect }));

vi.mock('@/integrations/supabase/client', () => ({
  getSupabaseClient: () => ({
    from: (...args: unknown[]) => mockFrom(...args),
  }),
}));

import { fetchPresetResourceById } from './presetResourcesRepository';
import { RepositoryError } from '@/integrations/astrid/repositories/repositoryErrors';

describe('preset resource repository contracts', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockSelect.mockReturnValue(queryBuilder);
    mockFrom.mockReturnValue({ select: mockSelect });
    queryBuilder.eq.mockImplementation(() => queryBuilder);
    mockMaybeSingle.mockResolvedValue({ data: null, error: null });
  });

  it('returns null for missing preset resources', async () => {
    await expect(fetchPresetResourceById('preset-1')).resolves.toBeNull();
  });

  it('throws RepositoryError for preset query failures', async () => {
    mockMaybeSingle.mockResolvedValue({
      data: null,
      error: { code: 'XX000', message: 'preset query failed' },
    });

    await expect(fetchPresetResourceById('preset-1')).rejects.toMatchObject<Partial<RepositoryError>>({
      name: 'RepositoryError',
      code: 'query_failed',
    });
  });

  it('throws RepositoryError for invalid preset rows', async () => {
    mockMaybeSingle.mockResolvedValue({
      data: { metadata: { name: 'broken' } },
      error: null,
    });

    await expect(fetchPresetResourceById('preset-1')).rejects.toMatchObject<Partial<RepositoryError>>({
      name: 'RepositoryError',
      code: 'invalid_row_shape',
    });
  });
});
