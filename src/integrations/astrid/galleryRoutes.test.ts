import { describe, expect, it, vi } from 'vitest';

vi.mock('./runtimeReadModels.ts', () => ({
  runtimeGenerationToSummary: (generation: { generation_id: string }) => ({ id: generation.generation_id }),
  runtimeGenerationToDetail: vi.fn(),
}));

import { AstridLocalGalleryRoutes, GALLERY_VARIANT_CONCURRENCY } from './galleryRoutes.ts';

describe('gallery list variant loading', () => {
  it('loads one variants page per generation with bounded concurrency', async () => {
    const GENERATIONS = 60;
    let inFlight = 0;
    let peak = 0;
    const variantCalls: string[] = [];
    const transport = {
      requestJson: vi.fn(async (path: string) => {
        if (path.includes('/variants')) {
          variantCalls.push(path);
          inFlight++; peak = Math.max(peak, inFlight);
          await Promise.resolve(); await Promise.resolve();
          inFlight--;
          return { items: [], next_cursor: null };
        }
        return {
          items: Array.from({ length: GENERATIONS }, (_, i) => ({ generation_id: `g${i}` })),
          next_cursor: null,
        };
      }),
    };
    const routes = new AstridLocalGalleryRoutes(transport as never, { projectSlug: 'p' });
    const page = await routes.list({ limit: 200 });
    expect(page.generations).toHaveLength(GENERATIONS);
    expect(variantCalls).toHaveLength(GENERATIONS);
    // Before the fix all 60 were issued at once.
    expect(peak).toBeLessThanOrEqual(GALLERY_VARIANT_CONCURRENCY);
  });
});
