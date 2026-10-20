import { describe, expect, it } from 'vitest';
import { planGenerationAssetRegistration } from './timeline-asset-plans.ts';

describe('planGenerationAssetRegistration content type', () => {
  it('reads the MIME type from metadata so a Runtime video is not registered as a still image', () => {
    // Runtime generation rows carry their MIME type (e.g. video/mp4) in metadata.content_type.
    const withType = planGenerationAssetRegistration({
      generationId: 'g',
      variantType: 'image',
      imageUrl: '/api/runtime/v1/objects/sha256%3Aabc',
      metadata: { content_type: 'video/mp4' },
    });
    expect(withType).toMatchObject({ ok: true, assetEntry: { type: 'video/mp4' } });

    const withoutType = planGenerationAssetRegistration({
      generationId: 'g',
      variantType: 'image',
      imageUrl: '/api/runtime/v1/objects/sha256%3Aabc',
    });
    expect(withoutType).toMatchObject({ ok: true, assetEntry: { type: 'image/png' } });
  });
});
