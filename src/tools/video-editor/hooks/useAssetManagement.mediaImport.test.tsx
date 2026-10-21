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

function addUploadPlaceholder(data: TimelineData, clipId = 'uploading-1'): TimelineData {
  return {
    ...data,
    rows: [{
      ...data.rows[0]!,
      actions: [{ id: clipId, start: 3, end: 8, effectId: `effect-${clipId}` }],
    }],
    meta: {
      ...data.meta,
      [clipId]: { asset: 'uploading:clip.mp4', track: 'V1', clipType: 'hold', hold: 5 },
    },
  };
}

function renderAssetManagement(provider: Record<string, unknown>, args = buildArgs()) {
  const toastError = vi.fn();
  const runtime = buildRuntimeValue(provider);
  runtime.toast.error = toastError;
  const hook = renderHook(() => useAssetManagement(args), {
    wrapper: ({ children }) => (
      <VideoEditorRuntimeProvider value={runtime}>
        {children}
      </VideoEditorRuntimeProvider>
    ),
  });
  return { ...hook, toastError };
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
    expect(addClip).toHaveBeenCalledWith({
      preparedAsset: prepared,
      trackId: 'V1',
      time: 3,
      forceNewTrack: false,
      insertAtTop: false,
    });
    expect(addClip.mock.calls[0]?.[0].preparedAsset.mediaSelection).toBe(mediaSelection);
    expect(args.applyEdit).not.toHaveBeenCalled();
  });

  it('hands a local upload placeholder to native ADD without claiming an accepted replacement', async () => {
    const addClip = vi.fn().mockResolvedValue({ ok: true, data: { clipId: 'clip-1', trackId: 'V1' } });
    const args = buildArgs();
    args.commands = { addClip: addClip as unknown as TimelineCommands['addClip'] };
    args.dataRef.current = addUploadPlaceholder(buildDropData());
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

    await act(async () => {
      await result.current.handleAssetDrop('sha256:asset', 'V1', 3, false, false, prepared ?? undefined, 'uploading-1');
    });

    expect(addClip).toHaveBeenCalledWith({
      preparedAsset: prepared,
      trackId: 'V1',
      time: 3,
      forceNewTrack: false,
      insertAtTop: false,
    });
  });

  it('keeps an accepted-row replacement refusal visible and preserves the authored row', async () => {
    const addClip = vi.fn().mockResolvedValue({
      ok: false,
      error: { code: 'invalid_argument', message: 'Native prepared parent media only supports a new manual clip.' },
    });
    const args = buildArgs();
    args.commands = { addClip: addClip as unknown as TimelineCommands['addClip'] };
    const data = buildDropData();
    data.rows[0]!.actions = [{ id: 'clip-authored', start: 3, end: 8, effectId: 'effect-clip-authored' }];
    data.meta['clip-authored'] = { asset: 'asset-authored', track: 'V1', clipType: 'media', from: 0, to: 5 };
    args.dataRef.current = data;
    const { result, toastError } = renderAssetManagement({
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
      placed = await result.current.handleAssetDrop('sha256:asset', 'V1', 3, false, false, prepared ?? undefined, 'clip-authored');
    });

    expect(placed).toBe(false);
    expect(addClip).toHaveBeenCalledWith(expect.objectContaining({ removeClipId: 'clip-authored' }));
    expect(args.dataRef.current?.rows[0]?.actions[0]?.id).toBe('clip-authored');
    expect(args.applyEdit).not.toHaveBeenCalled();
    expect(toastError).toHaveBeenCalledWith('Failed to save asset', {
      description: 'Native prepared parent media only supports a new manual clip.',
    });
  });

  it('refuses a prepared video without its original selection before local editing', async () => {
    const args = buildArgs();
    args.dataRef.current = buildDropData();
    const before = args.dataRef.current;
    const { result, toastError } = renderAssetManagement({
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
      },
    });

    let placed = true;
    await act(async () => {
      placed = await result.current.handleAssetDrop('sha256:asset', 'V1', 3, false, false, prepared ?? undefined);
    });

    expect(placed).toBe(false);
    expect(args.applyEdit).not.toHaveBeenCalled();
    expect(args.dataRef.current).toBe(before);
    expect(toastError).toHaveBeenCalledWith('Failed to save asset', {
      description: 'Runtime prepared video is missing its original media selection.',
    });
  });

  it('refuses a selected prepared video when the native consumer is unavailable', async () => {
    const args = buildArgs();
    args.dataRef.current = buildDropData();
    const { result, toastError } = renderAssetManagement({
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
    expect(toastError).toHaveBeenCalledWith('Failed to save asset', {
      description: 'Runtime prepared video placement is unavailable.',
    });
  });

  it('preserves the native refusal without falling back to a local snapshot edit', async () => {
    const refusalMessage = `verified media refused ${'x'.repeat(300)}`;
    const addClip = vi.fn().mockResolvedValue({
      ok: false,
      error: { code: 'mutation_failed', message: refusalMessage },
    });
    const args = buildArgs();
    args.commands = { addClip: addClip as unknown as TimelineCommands['addClip'] };
    args.dataRef.current = buildDropData();
    const { result, toastError } = renderAssetManagement({
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
    const toastDescription = toastError.mock.calls[0]?.[1]?.description;
    expect(toastDescription).toBe(refusalMessage.slice(0, 240));
    expect(toastDescription).toHaveLength(240);
  });

  it('forwards native placement and removal intent without falling back on refusal', async () => {
    const addClip = vi.fn().mockResolvedValue({
      ok: false,
      error: { code: 'invalid_argument', message: 'Native prepared parent media only supports a new manual clip.' },
    });
    const args = buildArgs();
    args.commands = { addClip: addClip as unknown as TimelineCommands['addClip'] };
    args.dataRef.current = buildDropData();
    const { result, toastError } = renderAssetManagement({
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
      placed = await result.current.handleAssetDrop('sha256:asset', 'V1', 3, true, true, prepared ?? undefined, 'uploading-1');
    });

    expect(placed).toBe(false);
    expect(addClip).toHaveBeenCalledWith({
      preparedAsset: prepared,
      trackId: 'V1',
      time: 3,
      forceNewTrack: true,
      insertAtTop: true,
      removeClipId: 'uploading-1',
    });
    expect(args.applyEdit).not.toHaveBeenCalled();
    expect(toastError).toHaveBeenCalledWith('Failed to save asset', {
      description: 'Native prepared parent media only supports a new manual clip.',
    });
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
