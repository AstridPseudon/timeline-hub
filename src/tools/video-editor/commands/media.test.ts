import { describe, expect, it } from 'vitest';
import { createDefaultTimelineConfig } from '@/tools/video-editor/lib/defaults.ts';
import { buildSwitchShotGroupToFinalVideoMutation } from '@/tools/video-editor/lib/shot-group-commands.ts';
import { buildTimelineData } from '@/tools/video-editor/lib/timeline-data.ts';
import type { AssetRegistry } from '@/tools/video-editor/types/index.ts';
import { applyPreparedMediaCommand } from './media.ts';

describe('prepared media command', () => {
  it('persists the prepared registry entry and clip replacement in one compound mutation', async () => {
    const config = {
      ...createDefaultTimelineConfig(),
      tracks: [{ id: 'V1', kind: 'visual' as const, label: 'V1' }],
      clips: [{
        id: 'clip-old',
        at: 0,
        track: 'V1',
        clipType: 'hold' as const,
        hold: 2,
        asset: 'asset-old',
      }],
    };
    const registry: AssetRegistry = {
      assets: {
        'asset-old': { file: 'old.png', type: 'image/png' },
      },
    };
    const current = await buildTimelineData(config, registry);
    const preparedEntry = {
      file: 'new.png',
      type: 'image/png',
      generationId: 'generation-new',
    };

    const result = applyPreparedMediaCommand(current, {
      type: 'place-prepared-media',
      payload: {
        asset: {
          assetKey: 'asset-new',
          mediaType: 'image',
          durationSeconds: 2,
          entry: preparedEntry,
          source: 'registered',
        },
        trackId: 'V1',
        at: 0,
        removeClipId: 'clip-old',
      },
    });

    expect(result).not.toBeNull();
    expect(result?.nextData.registry.assets['asset-new']).toEqual(preparedEntry);
    expect(result?.nextData.config.clips).toEqual([
      expect.objectContaining({ asset: 'asset-new', track: 'V1' }),
    ]);
    expect(result?.nextData.config.clips.some((clip) => clip.id === 'clip-old')).toBe(false);
    expect(result?.history).toMatchObject({
      appliedCount: 1,
      commandTypes: ['place-prepared-media'],
      failedCount: 0,
    });
  });

  it('rejects a prepared placement whose deferred target no longer exists', async () => {
    const current = await buildTimelineData(
      {
        ...createDefaultTimelineConfig(),
        tracks: [{ id: 'V1', kind: 'visual' as const, label: 'V1' }],
        clips: [],
      },
      { assets: {} },
    );

    const result = applyPreparedMediaCommand(current, {
      type: 'place-prepared-media',
      payload: {
        asset: {
          assetKey: 'asset-new',
          mediaType: 'image',
          durationSeconds: 1,
          entry: { file: 'new.png', type: 'image/png' },
          source: 'registered',
        },
        trackId: 'V1',
        at: 0,
        removeClipId: 'clip-deleted',
      },
    });

    expect(result).toBeNull();
  });

  it('keeps the prepared replacement clip id aligned with pinned group membership after source removal', async () => {
    const current = await buildTimelineData(
      {
        ...createDefaultTimelineConfig(),
        tracks: [{ id: 'V1', kind: 'visual' as const, label: 'V1' }],
        clips: [
          { id: 'clip-1', at: 0, track: 'V1', clipType: 'hold' as const, hold: 2, asset: 'asset-one' },
          { id: 'clip-2', at: 2, track: 'V1', clipType: 'hold' as const, hold: 2, asset: 'asset-two' },
        ],
        pinnedShotGroups: [{
          shotId: 'shot-1',
          trackId: 'V1',
          clipIds: ['clip-1', 'clip-2'],
          mode: 'images',
        }],
      },
      {
        assets: {
          'asset-one': { file: 'one.png', type: 'image/png' },
          'asset-two': { file: 'two.png', type: 'image/png' },
        },
      },
    );

    const mutation = buildSwitchShotGroupToFinalVideoMutation({
      currentData: current,
      shotId: 'shot-1',
      rowId: 'V1',
      clipIds: ['clip-1', 'clip-2'],
      assetKey: 'asset-final',
      durationSeconds: 4,
    });
    expect(mutation).not.toBeNull();
    const replacementClipId = Object.keys(mutation?.metaUpdates ?? {})[0];
    const replacementAction = mutation?.rows[0]?.actions.find((action) => action.id === replacementClipId);

    const result = applyPreparedMediaCommand(current, {
      type: 'place-prepared-media',
      payload: {
        asset: {
          assetKey: 'asset-final',
          mediaType: 'video',
          durationSeconds: 4,
          entry: { file: 'final.mp4', type: 'video/mp4' },
          source: 'registered',
        },
        trackId: 'V1',
        at: replacementAction?.start ?? 0,
        clipSpanSeconds: replacementAction ? replacementAction.end - replacementAction.start : 4,
        clipId: replacementClipId,
        removeClipIds: mutation?.metaDeletes,
        pinnedShotGroupsOverride: mutation?.pinnedShotGroupsOverride
          ? JSON.parse(JSON.stringify(mutation.pinnedShotGroupsOverride))
          : undefined,
      },
    });

    expect(result?.nextData.config.clips).toEqual([
      expect.objectContaining({ id: replacementClipId, asset: 'asset-final' }),
    ]);
    expect(result?.nextData.config.pinnedShotGroups).toEqual([expect.objectContaining({
      clipIds: [replacementClipId],
    })]);
  });

  it('preserves replacement clip metadata while changing the prepared asset and duration bounds', async () => {
    const current = await buildTimelineData(
      {
        ...createDefaultTimelineConfig(),
        tracks: [{ id: 'V1', kind: 'visual' as const, label: 'V1' }],
        clips: [{
          id: 'clip-3',
          at: 7,
          track: 'V1',
          clipType: 'media' as const,
          asset: 'asset-old',
          from: 1,
          to: 11,
          speed: 2,
          volume: 0.4,
          opacity: 0.6,
          cropTop: 0.1,
          cropBottom: 0.2,
          cropLeft: 0.3,
          cropRight: 0.4,
          effects: { blur: 0.5 },
        }],
        pinnedShotGroups: [{
          shotId: 'shot-1',
          trackId: 'V1',
          clipIds: ['clip-3'],
          mode: 'video',
          videoAssetKey: 'asset-old',
        }],
      },
      {
        assets: {
          'asset-old': { file: 'old.mp4', type: 'video/mp4', generationId: 'old' },
        },
      },
    );

    const result = applyPreparedMediaCommand(current, {
      type: 'place-prepared-media',
      payload: {
        asset: {
          assetKey: 'asset-new',
          mediaType: 'video',
          durationSeconds: 3,
          entry: { file: 'new.mp4', type: 'video/mp4', generationId: 'new' },
          source: 'registered',
        },
        trackId: 'V1',
        at: 7,
        clipSpanSeconds: 3,
        clipId: 'clip-3',
        replaceClipId: 'clip-3',
        pinnedShotGroupsOverride: [{
          shotId: 'shot-1',
          trackId: 'V1',
          clipIds: ['clip-3'],
          mode: 'video',
          videoAssetKey: 'asset-new',
        }],
      },
    });

    expect(result?.nextData.config.clips).toEqual([expect.objectContaining({
      id: 'clip-3',
      asset: 'asset-new',
      at: 7,
      from: 1,
      to: 7,
      speed: 2,
      volume: 0.4,
      opacity: 0.6,
      cropTop: 0.1,
      cropBottom: 0.2,
      cropLeft: 0.3,
      cropRight: 0.4,
      effects: { blur: 0.5 },
    })]);
    expect(result?.nextData.config.clips[0]?.at).toBe(7);
    expect(result?.nextData.rows[0]?.actions).toEqual([
      { id: 'clip-3', start: 7, end: 10, effectId: 'effect-clip-3' },
    ]);
  });

  it('uses normal duplicate ripple and metadata behavior for prepared afterClipId placement', async () => {
    const current = await buildTimelineData(
      {
        ...createDefaultTimelineConfig(),
        tracks: [{ id: 'V1', kind: 'visual' as const, label: 'V1' }],
        clips: [
          {
            id: 'clip-1',
            at: 0,
            track: 'V1',
            clipType: 'hold' as const,
            hold: 2,
            asset: 'asset-old',
            opacity: 0.5,
            effects: { glow: 1 },
          },
          { id: 'clip-2', at: 4, track: 'V1', clipType: 'hold' as const, hold: 2, asset: 'asset-after' },
        ],
      },
      {
        assets: {
          'asset-old': { file: 'old.png', type: 'image/png' },
          'asset-after': { file: 'after.png', type: 'image/png' },
        },
      },
    );

    const result = applyPreparedMediaCommand(current, {
      type: 'place-prepared-media',
      payload: {
        asset: {
          assetKey: 'asset-copy',
          mediaType: 'video',
          durationSeconds: 2,
          entry: { file: 'copy.mp4', type: 'video/mp4' },
          source: 'registered',
        },
        at: 0,
        afterClipId: 'clip-1',
      },
    });

    expect(result?.nextData.rows[0]?.actions).toEqual([
      { id: 'clip-1', start: 0, end: 2, effectId: 'effect-clip-1' },
      { id: 'clip-3', start: 2, end: 4, effectId: 'effect-clip-3' },
      { id: 'clip-2', start: 6, end: 8, effectId: 'effect-clip-2' },
    ]);
    expect(result?.nextData.config.clips).toEqual(expect.arrayContaining([
      expect.objectContaining({
        id: 'clip-3',
        asset: 'asset-copy',
        opacity: 0.5,
        effects: { glow: 1 },
      }),
    ]));
  });

  it('keeps the source-window clone and opaque metadata while rippling only the source track', async () => {
    const config = {
      ...createDefaultTimelineConfig(),
      output: { resolution: '1920x1080', fps: 30, file: 'out.mp4' },
      tracks: [
        { id: 'V1', kind: 'visual' as const, label: 'V1' },
        { id: 'V2', kind: 'visual' as const, label: 'V2' },
      ],
      clips: [
        {
          id: 'clip-1',
          at: 1,
          track: 'V1',
          clipType: 'media' as const,
          asset: 'asset-source',
          from: 2,
          to: 6,
          speed: 2,
          opacity: 0.5,
          effects: { glow: 1 },
          transition: { type: 'crossfade', duration: 0.5, params: { opaque: [null, false] } },
          params: { claims: { reserved: true }, opaque: { ordered: [null, false, 0] } },
          app: { opaque: { keep: null, ordered: [false, 0, ''] } },
          keyframes: { opacity: [{ time: 0, value: 0.5, interpolation: 'linear' as const }] },
        },
        { id: 'clip-2', at: 5, track: 'V1', clipType: 'hold' as const, hold: 1, asset: 'asset-peer' },
        { id: 'clip-4', at: 5, track: 'V2', clipType: 'hold' as const, hold: 1, asset: 'asset-peer' },
      ],
    };
    const registry: AssetRegistry = {
      assets: {
        'asset-source': { file: 'source.mp4', type: 'video/mp4', media_id: 'media-source' },
        'asset-peer': { file: 'peer.png', type: 'image/png' },
      },
    };
    const current = await buildTimelineData(config, registry);
    const before = structuredClone(current);
    const command = {
      type: 'place-prepared-media' as const,
      payload: {
        asset: {
          assetKey: 'asset-copy',
          mediaType: 'video' as const,
          durationSeconds: 2,
          entry: { file: 'copy.mp4', type: 'video/mp4', media_id: 'media-copy' },
          source: 'registered' as const,
        },
        at: 0,
        afterClipId: 'clip-1',
      },
    };

    const result = applyPreparedMediaCommand(current, command);
    expect(result).not.toBeNull();
    expect(result?.nextData.rows.find((row) => row.id === 'V1')?.actions).toEqual([
      { id: 'clip-1', start: 1, end: 3, effectId: 'effect-clip-1' },
      { id: 'clip-5', start: 3, end: 5, effectId: 'effect-clip-5' },
      { id: 'clip-2', start: 7, end: 8, effectId: 'effect-clip-2' },
    ]);
    expect(result?.nextData.rows.find((row) => row.id === 'V2')?.actions).toEqual([
      { id: 'clip-4', start: 5, end: 6, effectId: 'effect-clip-4' },
    ]);
    expect(result?.nextData.config.clips).toEqual(expect.arrayContaining([
      expect.objectContaining({
        id: 'clip-5',
        at: 3,
        track: 'V1',
        asset: 'asset-copy',
        from: 2,
        to: 6,
        speed: 2,
        opacity: 0.5,
        effects: { glow: 1 },
        transition: { type: 'crossfade', duration: 0.5, params: { opaque: [null, false] } },
        params: { claims: { reserved: true }, opaque: { ordered: [null, false, 0] } },
        app: { opaque: { keep: null, ordered: [false, 0, ''] } },
        keyframes: { opacity: [{ time: 0, value: 0.5, interpolation: 'linear' }] },
      }),
      expect.objectContaining({ id: 'clip-2', at: 7 }),
      expect.objectContaining({ id: 'clip-4', at: 5 }),
    ]));
    expect(result?.nextData.registry.assets['asset-copy']).toEqual(command.payload.asset.entry);
    expect(result?.history).toMatchObject({
      appliedCount: 1,
      commandTypes: ['place-prepared-media'],
      failedCount: 0,
    });
    expect(current).toEqual(before);
  });

  it('replays the prepared after-anchor command from JSON without changing its local result', async () => {
    const config = {
      ...createDefaultTimelineConfig(),
      tracks: [{ id: 'V1', kind: 'visual' as const, label: 'V1' }],
      clips: [
        { id: 'clip-1', at: 0, track: 'V1', clipType: 'hold' as const, hold: 1, asset: 'asset-source' },
        { id: 'clip-2', at: 1, track: 'V1', clipType: 'hold' as const, hold: 1, asset: 'asset-peer' },
      ],
    };
    const current = await buildTimelineData(config, {
      assets: {
        'asset-source': { file: 'source.png', type: 'image/png' },
        'asset-peer': { file: 'peer.png', type: 'image/png' },
      },
    });
    const command = {
      type: 'place-prepared-media' as const,
      payload: {
        asset: {
          assetKey: 'asset-copy',
          mediaType: 'image' as const,
          durationSeconds: 1,
          entry: { file: 'copy.png', type: 'image/png' },
          source: 'registered' as const,
        },
        at: 0,
        afterClipId: 'clip-1',
      },
    };
    const first = applyPreparedMediaCommand(current, command);
    const reloaded = JSON.parse(JSON.stringify(command)) as typeof command;
    const replay = applyPreparedMediaCommand(current, reloaded);

    expect(replay).toEqual(first);
    expect(applyPreparedMediaCommand(current, {
      ...command,
      payload: { ...command.payload, afterClipId: 'clip-missing' },
    })).toBeNull();
  });
});
