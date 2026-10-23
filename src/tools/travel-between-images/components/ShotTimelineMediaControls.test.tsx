// @vitest-environment jsdom
import React from 'react';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
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
    state.runtime.provider.prepareMediaImport = vi.fn();
    state.assets.uploadImageGeneration.mockReset();
    state.assets.uploadVideoGeneration.mockReset();
    state.assets.prepareGenerationAsset.mockReset();
    state.commands.addClip.mockReset().mockReturnValue({ ok: true, data: { clipId: 'clip-new', trackId: 'V1' } });
  });

  it('imports selected media and sends an add command through the mounted editor', async () => {
    const uploaded = { generationId: 'generation-new', variantId: 'variant-new' };
    const preparedAsset = { assetKey: 'asset-new', mediaType: 'image', entry: { file: 'asset-new' } };
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
      clips: [{ id: 'clip-old', track: 'V1', asset: 'asset-old', clipType: 'media' }],
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
      replaceClipId: 'clip-old',
    }));
  });
});
