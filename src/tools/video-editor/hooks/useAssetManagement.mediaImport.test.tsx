// @vitest-environment jsdom

import React from 'react';
import { act, renderHook } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import {
  VideoEditorRuntimeProvider,
  type VideoEditorRuntimeContextValue,
} from '@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx';
import { useAssetManagement, type UseAssetManagementArgs } from './useAssetManagement';
import { RUNTIME_MEDIA_IMPORT_MAX_BYTES } from '@/tools/video-editor/data/AssetResolver.ts';
import type { TimelineData } from '@/tools/video-editor/lib/timeline-data.ts';
import type { TimelineCommands } from '@/tools/video-editor/hooks/useTimelineCommandsService.ts';

const extractVideoMetadataMock = vi.fn();

vi.mock('@/shared/lib/media/videoMetadata.ts', () => ({
  extractVideoMetadata: (...args: unknown[]) => extractVideoMetadataMock(...args),
}));

function buildRuntimeValue(provider: Record<string, unknown>): VideoEditorRuntimeContextValue {
  return {
    provider: provider as VideoEditorRuntimeContextValue['provider'],
    assetResolver: { resolveAssetUrl: vi.fn() },
    auth: {} as VideoEditorRuntimeContextValue['auth'],
    project: {} as VideoEditorRuntimeContextValue['project'],
    shots: {} as VideoEditorRuntimeContextValue['shots'],
    mediaLightbox: {} as VideoEditorRuntimeContextValue['mediaLightbox'],
    agentChat: {} as VideoEditorRuntimeContextValue['agentChat'],
    toast: { error: vi.fn(), success: vi.fn(), warning: vi.fn(), info: vi.fn() },
    telemetry: {} as VideoEditorRuntimeContextValue['telemetry'],
    timelineId: 'timeline-1',
    userId: null,
    extensions: {} as VideoEditorRuntimeContextValue['extensions'],
  };
}

function buildArgs(): UseAssetManagementArgs {
  return {
    dataRef: { current: null as TimelineData | null },
    selectedTrackId: null,
    selectedProjectId: 'runtime-project-id',
    selectClip: vi.fn(),
    setSelectedTrackId: vi.fn(),
    applyEdit: vi.fn(),
    patchRegistry: vi.fn(),
    uploadAsset: vi.fn(),
    invalidateAssetRegistry: vi.fn(),
    resolveAssetUrl: vi.fn(async (file: string) => file),
  };
}

function buildDropData(): TimelineData {
  const tracks = [{ id: 'V1', kind: 'visual' as const }];
  const registry = { assets: {} };
  const config = { output: { width: 1280, height: 720, fps: 30 }, tracks, clips: [], registry };
  return {
    config,
    configVersion: 1,
    registry,
    resolvedConfig: config,
    rows: [{ id: 'V1', actions: [] }],
    meta: {},
    effects: {},
    assetMap: {},
    output: config.output,
    tracks,
    clipOrder: { V1: [] },
    signature: 'sig',
    stableSignature: 'stable',
  } as TimelineData;
}

function renderAssetManagement(provider: Record<string, unknown>, args = buildArgs()) {
  return renderHook(() => useAssetManagement(args), {
    wrapper: ({ children }) => (
      <VideoEditorRuntimeProvider value={buildRuntimeValue(provider)}>
        {children}
      </VideoEditorRuntimeProvider>
    ),
  });
}

describe('useAssetManagement Runtime media imports', () => {
  it('uses one Runtime import identity for image and video drops', async () => {
    extractVideoMetadataMock.mockResolvedValue({ duration_seconds: 2.5 });
    const prepareMediaImport = vi.fn()
      .mockResolvedValueOnce({
        provider: 'runtime',
        project: 'runtime-project-id',
        importOperationId: 'operation-image',
        generationId: 'generation-image',
        variantId: 'variant-image',
        assetId: 'sha256:image',
        entry: { file: 'https://runtime.test/image', type: 'image/png' },
      })
      .mockResolvedValueOnce({
        provider: 'runtime',
        project: 'runtime-project-id',
        importOperationId: 'operation-video',
        generationId: 'generation-video',
        variantId: 'variant-video',
        assetId: 'sha256:video',
        entry: { file: 'https://runtime.test/video', type: 'video/mp4', duration: 2.5 },
      });
    const { result } = renderAssetManagement({
      supportsDirectAssetUpload: true,
      prepareMediaImport,
      resolveAssetUrl: vi.fn(),
    });

    const image = new File(['image'], 'frame.png', { type: 'image/png' });
    const video = new File(['video'], 'clip.mp4', { type: 'video/mp4' });
    await act(async () => {
      await result.current.uploadImageGeneration(image);
      await result.current.uploadVideoGeneration(video);
    });

    expect(prepareMediaImport).toHaveBeenNthCalledWith(1, image, {
      filename: 'frame.png',
      mediaType: 'image/png',
    });
    expect(prepareMediaImport).toHaveBeenNthCalledWith(2, video, {
      filename: 'clip.mp4',
      mediaType: 'video/mp4',
      durationSeconds: 2.5,
    });
  });

  it('rejects an oversized Runtime import before invoking the provider', async () => {
    const prepareMediaImport = vi.fn();
    const { result } = renderAssetManagement({
      supportsDirectAssetUpload: true,
      prepareMediaImport,
      resolveAssetUrl: vi.fn(),
    });
    const oversizedImage = new File(['image'], 'huge.png', { type: 'image/png' });
    Object.defineProperty(oversizedImage, 'size', { value: RUNTIME_MEDIA_IMPORT_MAX_BYTES + 1 });

    await expect(result.current.uploadImageGeneration(oversizedImage)).rejects.toThrow(
      'huge.png exceeds the Workspace Runtime media limit of 5 GiB',
    );
    expect(prepareMediaImport).not.toHaveBeenCalled();
  });

  it('carries a prepared Runtime selection outside the registry entry', () => {
    const { result } = renderAssetManagement({
      supportsDirectAssetUpload: true,
      resolveAssetUrl: vi.fn(),
    });
    const mediaSelection = {
      asset: 'sha256:asset',
      generation_id: 'generation-1',
      variant_id: 'variant-1',
      object_id: 'sha256:object',
      catalog_digest: 'sha256:catalog',
    };

    const prepared = result.current.prepareGenerationAsset({
      generationId: 'generation-1',
      variantId: 'variant-1',
      variantType: 'video',
      mediaId: 'sha256:object',
      imageUrl: 'https://runtime.test/object.mp4',
      metadata: {
        content_type: 'video/mp4',
        original_filename: 'object.mp4',
      },
      mediaImport: {
        provider: 'runtime',
        project: 'runtime-project-id',
        importOperationId: 'operation-1',
        generationId: 'generation-1',
        variantId: 'variant-1',
        assetId: 'sha256:asset',
        entry: { file: 'https://runtime.test/object.mp4', type: 'video/mp4' },
        mediaSelection,
      },
    });

    expect(prepared?.mediaSelection).toBe(mediaSelection);
    expect(prepared?.entry).toEqual({
      file: 'https://runtime.test/object.mp4',
      type: 'video/mp4',
      generationId: 'generation-1',
      variantId: 'variant-1',
    });
    expect(JSON.stringify(prepared?.entry)).not.toContain('catalog_digest');
  });

  it('routes a selected prepared video to the native addClip consumer', async () => {
    const addClip = vi.fn().mockResolvedValue({ ok: true, data: { clipId: 'clip-1', trackId: 'V1' } });
    const args = buildArgs();
    args.commands = { addClip: addClip as unknown as TimelineCommands['addClip'] };
    args.dataRef.current = buildDropData();
    const { result } = renderAssetManagement({
      supportsDirectAssetUpload: true,
      resolveAssetUrl: vi.fn(),
    }, args);
    const mediaSelection = Object.freeze({
      asset: 'sha256:asset',
      generation_id: 'generation-1',
      variant_id: 'variant-1',
      object_id: 'sha256:object',
      catalog_digest: 'sha256:catalog',
    });
    const prepared = result.current.prepareGenerationAsset({
      generationId: 'generation-1',
      variantId: 'variant-1',
      variantType: 'video',
      mediaId: 'sha256:object',
      imageUrl: 'https://runtime.test/object.mp4',
      metadata: { content_type: 'video/mp4', original_filename: 'object.mp4' },
      mediaImport: {
        provider: 'runtime',
        project: 'runtime-project-id',
        importOperationId: 'operation-1',
        generationId: 'generation-1',
        variantId: 'variant-1',
        assetId: 'sha256:asset',
        entry: { file: 'https://runtime.test/object.mp4', type: 'video/mp4' },
        mediaSelection,
      },
    });

    let placed = false;
    await act(async () => {
      placed = await result.current.handleAssetDrop('sha256:asset', 'V1', 3, false, false, prepared ?? undefined);
    });

    expect(placed).toBe(true);
    expect(addClip).toHaveBeenCalledWith({ preparedAsset: prepared, trackId: 'V1', time: 3 });
    expect(addClip.mock.calls[0]?.[0].preparedAsset.mediaSelection).toBe(mediaSelection);
    expect(args.applyEdit).not.toHaveBeenCalled();
  });

  it('refuses a selected prepared video when the native consumer is unavailable', async () => {
    const args = buildArgs();
    args.dataRef.current = buildDropData();
    const { result } = renderAssetManagement({
      supportsDirectAssetUpload: true,
      resolveAssetUrl: vi.fn(),
    }, args);
    const prepared = result.current.prepareGenerationAsset({
      generationId: 'generation-1',
      variantId: 'variant-1',
      variantType: 'video',
      mediaId: 'sha256:object',
      imageUrl: 'https://runtime.test/object.mp4',
      metadata: { content_type: 'video/mp4', original_filename: 'object.mp4' },
      mediaImport: {
        provider: 'runtime',
        project: 'runtime-project-id',
        importOperationId: 'operation-1',
        generationId: 'generation-1',
        variantId: 'variant-1',
        assetId: 'sha256:asset',
        entry: { file: 'https://runtime.test/object.mp4', type: 'video/mp4' },
        mediaSelection: {
          asset: 'sha256:asset',
          generation_id: 'generation-1',
          variant_id: 'variant-1',
          object_id: 'sha256:object',
          catalog_digest: 'sha256:catalog',
        },
      },
    });

    let placed = true;
    await act(async () => {
      placed = await result.current.handleAssetDrop('sha256:asset', 'V1', 3, false, false, prepared ?? undefined);
    });

    expect(placed).toBe(false);
    expect(args.applyEdit).not.toHaveBeenCalled();
  });

  it('preserves the native refusal without falling back to a local snapshot edit', async () => {
    const addClip = vi.fn().mockResolvedValue({
      ok: false,
      error: { code: 'mutation_failed', message: 'verified media refused' },
    });
    const args = buildArgs();
    args.commands = { addClip: addClip as unknown as TimelineCommands['addClip'] };
    args.dataRef.current = buildDropData();
    const { result } = renderAssetManagement({
      supportsDirectAssetUpload: true,
      resolveAssetUrl: vi.fn(),
    }, args);
    const prepared = result.current.prepareGenerationAsset({
      generationId: 'generation-1',
      variantId: 'variant-1',
      variantType: 'video',
      mediaId: 'sha256:object',
      imageUrl: 'https://runtime.test/object.mp4',
      metadata: { content_type: 'video/mp4', original_filename: 'object.mp4' },
      mediaImport: {
        provider: 'runtime',
        project: 'runtime-project-id',
        importOperationId: 'operation-1',
        generationId: 'generation-1',
        variantId: 'variant-1',
        assetId: 'sha256:asset',
        entry: { file: 'https://runtime.test/object.mp4', type: 'video/mp4' },
        mediaSelection: {
          asset: 'sha256:asset',
          generation_id: 'generation-1',
          variant_id: 'variant-1',
          object_id: 'sha256:object',
          catalog_digest: 'sha256:catalog',
        },
      },
    });

    let placed = true;
    await act(async () => {
      placed = await result.current.handleAssetDrop('sha256:asset', 'V1', 3, false, false, prepared ?? undefined);
    });

    expect(placed).toBe(false);
    expect(args.applyEdit).not.toHaveBeenCalled();
  });

  it('fails closed for a direct Bridge provider instead of using the legacy generation writer', async () => {
    const { result } = renderAssetManagement({
      supportsDirectAssetUpload: true,
      resolveAssetUrl: vi.fn(),
    });
    const image = new File(['image'], 'frame.png', { type: 'image/png' });

    await expect(result.current.uploadImageGeneration(image)).rejects.toThrow(
      'This editor backend does not support Runtime image/video imports',
    );
  });
});
