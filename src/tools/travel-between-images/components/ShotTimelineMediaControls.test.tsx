// @vitest-environment jsdom
import React from 'react';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { buildTimelineData } from '@/tools/video-editor/lib/timeline-data.ts';
import { applyPreparedMediaCommand } from '@/tools/video-editor/commands/media.ts';
import { createDefaultTimelineConfig } from '@/tools/video-editor/lib/defaults.ts';
import type { AssetRegistry, TimelineConfig } from '@/tools/video-editor/types/index.ts';
import { ShotTimelineMediaControls } from './ShotTimelineMediaControls.tsx';

const state = vi.hoisted(() => ({
  data: { current: {} as object | null },
  editor: {
    resolvedConfig: {
      tracks: [{ id: 'V1', kind: 'visual' }],
      clips: [],
    },
    selectedClipIds: new Set<string>(),
    selectedTrackId: 'V1',
  },
  chrome: { saveStatus: 'saved' as const },
  playback: { currentTime: 1.25 },
  runtime: {
    provider: { prepareMediaImport: vi.fn() },
    assetResolver: { resolveAssetUrl: vi.fn(async (file: string) => file) },
    project: { projectId: 'project-1' },
    timelineId: 'document-1:shot:occ-1',
    timelineEditability: { checkTimeline: () => ({ allowed: true }) },
  },
  assets: {
    uploadImageGeneration: vi.fn(),
    uploadVideoGeneration: vi.fn(),
    prepareGenerationAsset: vi.fn(),
  },
  commands: { addClip: vi.fn() },
}));

vi.mock('@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx', () => ({
  useVideoEditorRuntime: () => state.runtime,
}));

vi.mock('@/tools/video-editor/hooks/timelineStore.ts', () => ({
  useTimelineChromeContext: () => state.chrome,
  useTimelineEditorData: () => ({ ...state.editor, dataRef: state.data }),
  useTimelineEditorOps: () => ({
    selectClip: vi.fn(),
    setSelectedTrackId: vi.fn(),
    applyEdit: vi.fn(),
    patchRegistry: vi.fn(),
  }),
  useTimelinePlaybackContext: () => state.playback,
}));

vi.mock('@/tools/video-editor/hooks/useAssetManagement.ts', () => ({
  useAssetManagement: () => state.assets,
}));

vi.mock('@/tools/video-editor/hooks/useTimelineCommandsService.ts', () => ({
  useTimelineCommandsService: () => state.commands,
}));

describe('ShotTimelineMediaControls', () => {
  beforeEach(() => {
    state.data.current = {};
    state.editor.resolvedConfig = {
      tracks: [{ id: 'V1', kind: 'visual' }],
      clips: [],
    };
    state.editor.selectedClipIds = new Set();
    state.editor.selectedTrackId = 'V1';
    state.playback.currentTime = 1.25;
    state.runtime.project.projectId = 'project-1';
    state.runtime.provider.prepareMediaImport = vi.fn();
    state.assets.uploadImageGeneration.mockReset();
    state.assets.uploadVideoGeneration.mockReset();
    state.assets.prepareGenerationAsset.mockReset();
    state.commands.addClip.mockReset().mockReturnValue({ ok: true, data: { clipId: 'clip-new', trackId: 'V1' } });
  });

  it('imports selected media and sends an add command through the mounted editor', async () => {
    const uploaded = { generationId: 'generation-new', variantId: 'variant-new' };
    const preparedAsset = {
      assetKey: 'asset-new',
      mediaType: 'image',
      entry: { file: 'asset-new' },
      mediaSelection: {
        asset: 'asset-new',
        generation_id: 'generation-new',
        variant_id: 'variant-new',
        object_id: 'sha256:object',
        catalog_digest: 'sha256:catalog',
      },
    };
    state.assets.uploadImageGeneration.mockResolvedValue(uploaded);
    state.assets.prepareGenerationAsset.mockReturnValue(preparedAsset);

    render(<ShotTimelineMediaControls occurrenceId="occ-1" parentDocumentId="document-1" />);
    fireEvent.click(screen.getByRole('button', { name: 'Add media' }));
    const file = new File(['image'], 'new.png', { type: 'image/png' });
    fireEvent.change(screen.getByLabelText('Choose media for shot timeline'), { target: { files: [file] } });

    await waitFor(() => expect(state.commands.addClip).toHaveBeenCalledWith({
      preparedAsset,
      trackId: 'V1',
      time: 1.25,
    }));
    expect(state.commands.addClip.mock.calls[0]?.[0].preparedAsset.mediaSelection).toEqual(
      preparedAsset.mediaSelection,
    );
    expect(state.assets.uploadImageGeneration).toHaveBeenCalledWith(file);
    expect(state.assets.prepareGenerationAsset).toHaveBeenCalledWith(uploaded);
  });

  it('refuses an import when the captured popup data is stale', async () => {
    let resolveUpload!: (value: unknown) => void;
    state.assets.uploadImageGeneration.mockReturnValue(new Promise(resolve => { resolveUpload = resolve; }));
    state.assets.prepareGenerationAsset.mockReturnValue({ assetKey: 'asset-new', mediaType: 'image', entry: { file: 'asset-new' } });

    render(<ShotTimelineMediaControls occurrenceId="occ-1" parentDocumentId="document-1" />);
    fireEvent.click(screen.getByRole('button', { name: 'Add media' }));
    fireEvent.change(screen.getByLabelText('Choose media for shot timeline'), {
      target: { files: [new File(['image'], 'new.png', { type: 'image/png' })] },
    });
    state.data.current = {};
    resolveUpload({ generationId: 'generation-new', variantId: 'variant-new' });

    await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent('shot changed'));
    expect(state.commands.addClip).not.toHaveBeenCalled();
  });

  it('uses replaceClipId for a selected media clip', async () => {
    state.editor.resolvedConfig = {
      tracks: [{ id: 'V1', kind: 'visual' }],
      clips: [{ id: 'clip-old', track: 'V1', at: 0.75, asset: 'asset-old', clipType: 'media' }],
    };
    state.editor.selectedClipIds = new Set(['clip-old']);
    const uploaded = { generationId: 'generation-new', variantId: 'variant-new' };
    const preparedAsset = { assetKey: 'asset-new', mediaType: 'image', entry: { file: 'asset-new' } };
    state.assets.uploadImageGeneration.mockResolvedValue(uploaded);
    state.assets.prepareGenerationAsset.mockReturnValue(preparedAsset);

    render(<ShotTimelineMediaControls occurrenceId="occ-1" parentDocumentId="document-1" />);
    fireEvent.click(screen.getByRole('button', { name: 'Swap selected clip' }));
    fireEvent.change(screen.getByLabelText('Choose media for shot timeline'), {
      target: { files: [new File(['image'], 'replacement.png', { type: 'image/png' })] },
    });

    await waitFor(() => expect(state.commands.addClip).toHaveBeenCalledWith({
      preparedAsset,
      trackId: 'V1',
      time: 0.75,
      replaceClipId: 'clip-old',
    }));
  });

  it('refuses a changed selected clip, owner, or media before writing', async () => {
    let resolveUpload!: (value: unknown) => void;
    state.editor.resolvedConfig = {
      tracks: [{ id: 'V1', kind: 'visual' }],
      clips: [{
        id: 'clip-old', track: 'V1', at: 0.75, asset: 'asset-old', clipType: 'media',
        app: { canonical: { ownerRef: 'occurrence:occ-1', clipRef: 'occurrence:occ-1/clip:clip-old' } },
      }],
    };
    state.editor.selectedClipIds = new Set(['clip-old']);
    state.assets.uploadImageGeneration.mockReturnValue(new Promise(resolve => { resolveUpload = resolve; }));

    const rendered = render(<ShotTimelineMediaControls occurrenceId="occ-1" parentDocumentId="document-1" />);
    fireEvent.click(screen.getByRole('button', { name: 'Swap selected clip' }));
    fireEvent.change(screen.getByLabelText('Choose media for shot timeline'), {
      target: { files: [new File(['image'], 'replacement.png', { type: 'image/png' })] },
    });
    state.editor.resolvedConfig = {
      tracks: [{ id: 'V1', kind: 'visual' }],
      clips: [{
        id: 'clip-new', track: 'V1', at: 0.75, asset: 'asset-new', clipType: 'media',
        app: { canonical: { ownerRef: 'occurrence:other', clipRef: 'occurrence:other/clip:clip-new' } },
      }],
    };
    state.editor.selectedClipIds = new Set(['clip-new']);
    rendered.rerender(<ShotTimelineMediaControls occurrenceId="occ-1" parentDocumentId="document-1" />);
    resolveUpload({ generationId: 'generation-new', variantId: 'variant-new' });

    await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent('shot changed'));
    expect(state.commands.addClip).not.toHaveBeenCalled();
    expect(state.assets.prepareGenerationAsset).not.toHaveBeenCalled();
  });

  it('refuses when the current project scope changes before writing', async () => {
    let resolveUpload!: (value: unknown) => void;
    state.assets.uploadImageGeneration.mockReturnValue(new Promise(resolve => { resolveUpload = resolve; }));

    render(<ShotTimelineMediaControls occurrenceId="occ-1" parentDocumentId="document-1" />);
    fireEvent.click(screen.getByRole('button', { name: 'Add media' }));
    fireEvent.change(screen.getByLabelText('Choose media for shot timeline'), {
      target: { files: [new File(['image'], 'new.png', { type: 'image/png' })] },
    });
    state.runtime.project.projectId = 'project-other';
    resolveUpload({ generationId: 'generation-new', variantId: 'variant-new' });

    await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent('shot changed'));
    expect(state.commands.addClip).not.toHaveBeenCalled();
  });

  it('refuses an add when the current placement time is missing without importing or writing', () => {
    state.playback.currentTime = Number.NaN;

    render(<ShotTimelineMediaControls occurrenceId="occ-1" parentDocumentId="document-1" />);
    fireEvent.click(screen.getByRole('button', { name: 'Add media' }));

    expect(screen.getByRole('alert')).toHaveTextContent('placement time is unavailable');
    expect(state.assets.uploadImageGeneration).not.toHaveBeenCalled();
    expect(state.commands.addClip).not.toHaveBeenCalled();
  });

  it('refuses an empty current project scope without importing or writing', () => {
    state.runtime.project.projectId = ' ';

    render(<ShotTimelineMediaControls occurrenceId="occ-1" parentDocumentId="document-1" />);

    expect(screen.getByRole('button', { name: 'Add media' })).toBeDisabled();
    expect(state.assets.uploadImageGeneration).not.toHaveBeenCalled();
    expect(state.commands.addClip).not.toHaveBeenCalled();
  });

  it.each(['add', 'swap'] as const)('routes %s through the real mounted command receiver with a semantic placement', async kind => {
    const config: TimelineConfig = {
      ...createDefaultTimelineConfig(),
      tracks: [{ id: 'V1', kind: 'visual' }],
      clips: [{ id: 'clip-old', track: 'V1', at: 0.75, hold: 2, asset: 'asset-old', clipType: 'media' }],
    };
    const registry: AssetRegistry = { assets: {
        'asset-old': { file: 'asset-old', type: 'video/mp4' },
      } };
    const current = await buildTimelineData(config, registry, async file => file);
    const dataRef = { current };
    const data = {
      data: current,
      dataRef,
      selectedTrackId: 'V1',
      resolvedConfig: current.resolvedConfig,
    };
    const applied = vi.fn((mutation: {
      type: string;
      command: Parameters<typeof applyPreparedMediaCommand>[1];
    }) => {
      expect(mutation.type).toBe('prepared-media');
      // The real receiver has already validated this command; apply the same
      // mounted command effect that the editor's A2 save observer receives.
      expect(mutation.command.payload.asset).toMatchObject({ assetKey: 'asset-new' });
      const result = applyPreparedMediaCommand(dataRef.current, mutation.command);
      if (!result) throw new Error('The real mounted command receiver rejected its own preview.');
      dataRef.current = result.nextData;
      data.data = result.nextData;
      data.resolvedConfig = result.nextData.resolvedConfig;
    });
    const store = {
      getState: () => ({
        availability: { mounted: true },
        data,
        ops: { applyEdit: applied },
      }),
    } as never;
    const { createTimelineCommands } = await vi.importActual<typeof import('@/tools/video-editor/hooks/useTimelineCommandsService.ts')>(
      '@/tools/video-editor/hooks/useTimelineCommandsService.ts',
    );
    const receiver = createTimelineCommands(store);
    state.commands.addClip = vi.fn(receiver.addClip);
    state.data.current = current;
    state.editor.resolvedConfig = current.resolvedConfig;
    state.editor.selectedClipIds = kind === 'swap' ? new Set(['clip-old']) : new Set();
    state.assets.uploadImageGeneration.mockResolvedValue({ generationId: 'generation-new', variantId: 'variant-new' });
    state.assets.prepareGenerationAsset.mockReturnValue({
      assetKey: 'asset-new', mediaType: 'image', entry: { file: 'asset-new', type: 'image/png' },
    });

    render(<ShotTimelineMediaControls occurrenceId="occ-1" parentDocumentId="document-1" />);
    fireEvent.click(screen.getByRole('button', { name: kind === 'swap' ? 'Swap selected clip' : 'Add media' }));
    fireEvent.change(screen.getByLabelText('Choose media for shot timeline'), {
      target: { files: [new File(['image'], `${kind}.png`, { type: 'image/png' })] },
    });

    await waitFor(() => expect(applied).toHaveBeenCalledTimes(1));
    expect(state.commands.addClip).toHaveBeenCalledWith(expect.objectContaining({
      preparedAsset: expect.objectContaining({ assetKey: 'asset-new' }),
      time: kind === 'swap' ? 0.75 : 1.25,
      ...(kind === 'swap' ? { replaceClipId: 'clip-old' } : {}),
    }));
    expect(applied).toHaveBeenCalledWith(expect.objectContaining({
      type: 'prepared-media',
      command: expect.objectContaining({
        type: 'place-prepared-media',
        payload: expect.objectContaining({
          at: kind === 'swap' ? 0.75 : 1.25,
          ...(kind === 'swap' ? { replaceClipId: 'clip-old' } : {}),
        }),
      }),
    }), expect.objectContaining({ semantic: true }));
  });
});
