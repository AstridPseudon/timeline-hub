import { describe, expect, it, vi } from 'vitest';
import { environment } from '../commands/__tests__/commitSessionEnvironment.ts';
import type { MediaSelection, VerifiedMedia } from '@/integrations/runtime/timeline-commit-types.ts';
import { createTimelineStore } from './timelineStore.ts';
import { createTimelineCommands } from './useTimelineCommandsService.ts';

describe('prepared video service with the native command session', () => {
  it.each([false, true])('submits at the requested position with an upload placeholder: %s', async (uploading) => {
    const env = await environment();
    const session = await env.mount();
    try {
      const store = createTimelineStore();
      const current = env.current();
      if (uploading) {
        current.rows[0].actions.push({ id: 'uploading-1', start: 20, end: 25, effectId: 'effect-uploading-1' });
        current.meta['uploading-1'] = { track: 'V1', clipType: 'hold', hold: 5, asset: 'uploading:video.webm' };
      }
      const before = structuredClone(current);
      store.getState().syncSlices({
        data: { ...store.getState().data, data: current, dataRef: { current } },
        ops: { ...store.getState().ops, parentClipAddMedia: session.parentClipAddMediaPort },
      });
      store.getState().setMounted(true);
      const media: MediaSelection = {
        asset: 'reserved-media', generation_id: 'generation-media', variant_id: 'variant-media',
        object_id: `sha256:${'2'.repeat(64)}`, catalog_digest: `sha256:${'b'.repeat(64)}`,
      };
      const verified: VerifiedMedia = { selection: media, media_type: 'video/webm', size: 123, duration_seconds: 1 };
      const getProjectVerifiedMedia = vi.fn(async () => verified);
      const commands = createTimelineCommands(store, {
        parentMediaRuntime: { projectId: 'project-commit', getProjectVerifiedMedia },
      });
      const result = await commands.addClip({
        preparedAsset: {
          assetKey: media.asset, mediaType: 'video', durationSeconds: 1, source: 'registered',
          entry: { file: 'https://runtime.test/video.webm', type: 'video/webm', duration: 1 }, mediaSelection: media,
        }, trackId: 'V1', time: 20,
      });
      expect(result).toEqual({ ok: true, data: expect.anything() });
      expect(current).toEqual(before);
      expect(getProjectVerifiedMedia).toHaveBeenCalledWith('project-commit', media);
      await vi.waitFor(() => expect(env.commits()).toHaveLength(1));
      expect(env.commits()[0].body?.commands[0]).toMatchObject({
        op: 'clip.add-media', select: 'parent', args: { media, row: { from: 0, to: 1, hold: 1, at: 20, track: 'V1' } },
      });
    } finally {
      await session.dispose();
    }
  });
});
