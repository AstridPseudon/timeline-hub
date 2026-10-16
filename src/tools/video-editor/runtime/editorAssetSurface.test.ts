import { describe, expect, it, vi } from 'vitest';
import { createEditorAssetSurface } from './editorAssetSurface.ts';
import type { TimelineData } from '@/tools/video-editor/lib/timeline-data.ts';

function timelineData(assets: Record<string, Record<string, unknown>>): TimelineData {
  return { registry: { assets } } as unknown as TimelineData;
}

describe('editor asset surface', () => {
  it('reads current registry identity and delegates legacy profile reads', async () => {
    let data: TimelineData | null = timelineData({
      asset_a: {
        file: 'Interview.mov', type: 'video', media_id: 'media_a',
        content_sha256: 'sha256:abc', metadata: { category: 'source' },
      },
    });
    const loadProfile = vi.fn().mockResolvedValue({ transcript: { segments: [] } });
    const assets = createEditorAssetSurface(() => data, loadProfile);

    expect(assets.keys()).toEqual(['asset_a']);
    expect(assets.get('asset_a')).toMatchObject({
      file: 'Interview.mov', kind: 'video', media_id: 'media_a',
      content_sha256: 'sha256:abc', category: 'source',
    });
    expect(assets.search('category', 'source')).toEqual(['asset_a']);
    expect(assets.has('asset_a')).toBe(true);
    expect(await assets.loadProfile('asset_a')).toEqual({ transcript: { segments: [] } });
    expect(loadProfile).toHaveBeenCalledWith('asset_a');

    data = timelineData({ asset_b: { file: 'new.wav', type: 'audio' } });
    expect(assets.keys()).toEqual(['asset_b']);
    expect(assets.get('asset_a')).toBeUndefined();
  });
});
