import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  toast: { success: vi.fn(), info: vi.fn(), error: vi.fn() },
  createShot: vi.fn(),
  navigate: vi.fn(),
  duplicateShotGroup: vi.fn(async () => ({})),
  promotePrimaryVariant: vi.fn(async () => []),
  duplicateGenerationAsset: vi.fn(),
  prepareGenerationAsset: vi.fn(),
  registerGenerationAsset: vi.fn(),
  reloadFromServer: vi.fn(async () => undefined),
  parentClipAddMedia: undefined as {
    prepare: () => unknown;
    assertPreparationCurrent: (preparation: unknown) => void;
  } | undefined,
  addClip: vi.fn(),
  galleryGet: vi.fn(async () => ({
    generation_id: 'gen-a',
    variants: [
      { id: 'variant-current', is_primary: true },
      { id: 'variant-next', is_primary: false },
    ],
  })),
  canonicalMode: false,
  canonicalOccurrence: {
    projectId: 'project-001',
    occurrenceId: 'occ-1',
    parentDocumentId: 'timeline-1',
    shotId: 'shot-1',
    revisionId: 'rev-1',
    ordinal: 0,
    atMs: 0,
    durationMs: 1000,
    stableDeepLink: 'project/project-001/document/timeline-1/shot/shot-1/revision/rev-1/occurrence/occ-1',
    outputIdentity: 'project/project-001/document/timeline-1/occurrence/occ-1/output/final-video',
    revision: {},
  },
}));

const data = {
  config: {
    output: { resolution: '1280x720', fps: 30, file: 'out.mp4' },
    tracks: [{ id: 'V1', kind: 'visual', label: 'Visual' }],
    clips: [{ id: 'clip-source', clipType: 'media', track: 'V1', at: 0, hold: 2, asset: 'asset-source' }],
    pinnedShotGroups: [],
  },
  configVersion: 13,
  registry: { assets: {
    'asset-source': { file: 'https://example.test/source.mp4', type: 'video/mp4', generationId: 'generation-source', variantId: 'variant-source', duration: 2 },
  } },
  resolvedConfig: { registry: {}, clips: [{ id: 'clip-source', clipType: 'media', track: 'V1', at: 0, hold: 2, asset: 'asset-source' }] },
  rows: [{ id: 'V1', actions: [{ id: 'clip-source', start: 0, end: 2 }] }],
  meta: { 'clip-source': { asset: 'asset-source', track: 'V1', clipType: 'media' } },
};
const dataRef = { current: data };

vi.mock('@/shared/components/ui/runtime/sonner.tsx', () => ({ toast: mocks.toast }));
vi.mock('@/shared/contexts/ShotsContext.tsx', () => ({ useShots: () => ({ shots: [] }) }));
vi.mock('@/shared/hooks/shotCreation/useShotCreation.ts', () => ({
  useShotCreation: () => ({ createShot: mocks.createShot, isCreating: false }),
}));
vi.mock('@/shared/hooks/shots/useShotNavigation.ts', () => ({ useShotNavigation: () => ({ navigateToShot: vi.fn() }) }));
vi.mock('react-router-dom', () => ({ useNavigate: () => mocks.navigate }));
vi.mock('@/shared/contexts/ProjectContext.tsx', () => ({
  useProjectSelectionContext: () => ({ selectedProjectId: 'astrid-project' }),
}));
vi.mock('@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx', () => ({
  useVideoEditorRuntime: () => ({
    userId: null,
    timelineId: 'active-non-default',
    project: { projectId: 'astrid-project' },
    provider: { apiBaseUrl: 'http://bridge.fake' },
    shots: mocks.canonicalMode
      ? {
          canonicalOccurrences: [mocks.canonicalOccurrence],
          shotComposition: {},
          canonicalComposition: {},
        }
      : undefined,
  }),
}));
vi.mock('@/tools/video-editor/hooks/timelineStore.ts', () => ({
  useTimelineConfigVersion: () => 13,
  useTimelineDataSelector: (selector: (value: unknown) => unknown) => selector({
    data,
    resolvedConfig: data.resolvedConfig,
    dataRef,
    selectedClipIds: new Set<string>(),
    interactionStateRef: { current: { drag: false, resize: false } },
  }),
  useTimelineOpsSelector: (selector: (value: unknown) => unknown) => selector({
    applyEdit: vi.fn(),
    patchRegistry: vi.fn(),
    unpatchRegistry: vi.fn(),
    registerAsset: vi.fn(),
    prepareGenerationAsset: mocks.prepareGenerationAsset,
    registerGenerationAsset: mocks.registerGenerationAsset,
    parentClipAddMedia: mocks.parentClipAddMedia,
    reloadFromServer: mocks.reloadFromServer,
  }),
  useTimelineChromeSelector: (selector: (value: unknown) => unknown) => selector({
    reloadFromServer: mocks.reloadFromServer,
  }),
}));
vi.mock('@/tools/video-editor/hooks/useTimelineCommandsService.ts', () => ({
  useTimelineCommandsService: () => ({ addClip: mocks.addClip }),
}));
vi.mock('@/tools/video-editor/hooks/usePinnedShotGroups.ts', () => ({
  usePinnedShotGroups: () => ({ pinGroup: vi.fn(), unpinGroup: vi.fn() }),
  usePinnedShotGroupViews: () => [],
  usePinnedGroupSync: vi.fn(),
}));
vi.mock('@/tools/video-editor/hooks/useShotGroups.ts', () => ({
  useShotGroups: () => [{
    shotId: mocks.canonicalMode ? mocks.canonicalOccurrence.shotId : 'shot-a',
    shotName: mocks.canonicalMode ? 'Opening' : 'Shot A',
    rowId: 'V1',
    rowIndex: 0,
    start: 0,
    clipIds: [],
    children: [],
    color: '#fff',
    poolGenerationIds: [],
    variantIdsByGenerationId: { 'gen-a': 'variant-current' },
    ...(mocks.canonicalMode ? { canonicalIdentity: mocks.canonicalOccurrence } : {}),
  }],
  projectCanonicalShotRows: (rows: unknown[]) => rows,
}));
vi.mock('@/tools/video-editor/hooks/useActiveTaskClips.ts', () => ({ useActiveTaskClips: () => ({ activeTaskAssetKeys: new Set() }) }));
vi.mock('@/tools/video-editor/hooks/useFinalVideoAvailable.ts', () => ({
  useFinalVideoAvailable: () => ({ finalVideoMap: new Map(), dismissFinalVideo: vi.fn() }),
}));
vi.mock('@/tools/video-editor/hooks/useSwitchToFinalVideo.ts', () => ({
  useSwitchToFinalVideo: () => ({ switchToFinalVideo: vi.fn(), updateToLatestVideo: vi.fn(), switchToImages: vi.fn() }),
}));
vi.mock('@/tools/video-editor/hooks/useShotGroupHandlers.ts', () => ({
  useShotGroupHandlers: () => ({
    shotGroupClipIds: new Set(), activeTaskClipIds: new Set(), staleShotGroupIds: new Set(),
    handleShotGroupNavigate: vi.fn(), handleShotGroupGenerateVideo: vi.fn(), handleDeleteShotGroup: vi.fn(),
    handleUpdateToLatestVideo: vi.fn(), handleShotGroupUnpin: vi.fn(), handleShotGroupSwitchToFinalVideo: vi.fn(),
    handleShotGroupSwitchToImages: vi.fn(),
  }),
}));
vi.mock('@/tools/video-editor/lib/shot-group-pack-commands.ts', () => ({
  duplicateShotGroup: mocks.duplicateShotGroup,
  promotePrimaryVariant: mocks.promotePrimaryVariant,
}));
vi.mock('@/integrations/astrid/client.ts', () => ({
  AstridLocalClient: class {
    gallery = { get: mocks.galleryGet };
  },
}));
vi.mock('@/tools/video-editor/components/TimelineEditor/TimelineEditorCore.tsx', () => ({
  resolveSelectedGenerationIdsForShotCreation: () => ({ canCreateShot: false, generationIds: [] }),
  TimelineEditorCore: (props: {
    onShotGroupDuplicate?: (locator: { shotId: string; trackId: string }) => void;
    onShotGroupPromotePrimary?: (locator: { shotId: string; trackId: string }) => void;
    onShotGroupNavigate?: unknown;
    onShotGroupGenerateVideo?: unknown;
    onShotGroupOpen?: (occurrence: typeof mocks.canonicalOccurrence) => void;
    onDuplicateGenerationClip?: (clipId: string) => void | Promise<void>;
  }) => (
    <div>
      <button onClick={() => props.onShotGroupDuplicate?.({ shotId: 'shot-a', trackId: 'V1' })}>Duplicate document shot</button>
      <button onClick={() => props.onShotGroupPromotePrimary?.({ shotId: 'shot-a', trackId: 'V1' })}>Promote document variant</button>
      <button onClick={() => props.onDuplicateGenerationClip?.('clip-source')}>Duplicate generation</button>
      {props.onShotGroupOpen && (
        <button onClick={() => props.onShotGroupOpen?.(mocks.canonicalOccurrence)}>Open canonical document shot</button>
      )}
      <output data-testid="relational-actions">{String(Boolean(props.onShotGroupNavigate || props.onShotGroupGenerateVideo))}</output>
    </div>
  ),
}));
vi.mock('@/tools/video-editor/lib/generation-utils.ts', () => ({ duplicateGenerationAsset: mocks.duplicateGenerationAsset }));
vi.mock('@/tools/travel-between-images/components/VideoGenerationModal.tsx', () => ({ VideoGenerationModal: () => null }));
vi.mock('@/tools/travel-between-images/pages/LocalTimelineShotBrowser.tsx', () => ({
  LocalTimelineShotBrowser: (props: { shotRef?: string; onClose?: () => void }) => (
    <div data-testid="canonical-shot-editor">
      <output>{props.shotRef}</output>
      <button type="button" onClick={props.onClose}>Close canonical shot editor</button>
    </div>
  ),
}));

import { installRuntimeErrorPresenter } from '@/shared/lib/errorHandling/runtimeErrorPresenter.ts';
import {
  AstridTimelineEditor,
  shouldKeepPublishedCanonicalCompositionOverride,
} from './AstridTimelineEditor.tsx';

describe('AstridTimelineEditor document-derived shot consumer', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mocks.canonicalMode = false;
    mocks.parentClipAddMedia = undefined;
  });

  it('holds a just-published graph only while the host still reports a known pre-publish head', () => {
    const staleHeads = ['host-before-save', 'expected-head'];
    expect(shouldKeepPublishedCanonicalCompositionOverride('published-head', staleHeads, 'host-before-save')).toBe(true);
    expect(shouldKeepPublishedCanonicalCompositionOverride('published-head', staleHeads, 'expected-head')).toBe(true);
    expect(shouldKeepPublishedCanonicalCompositionOverride('published-head', staleHeads, 'published-head')).toBe(false);
    expect(shouldKeepPublishedCanonicalCompositionOverride('published-head', staleHeads, 'later-head')).toBe(false);
    expect(shouldKeepPublishedCanonicalCompositionOverride('published-head', staleHeads, null)).toBe(true);
  });

  it('targets the active timeline/version, refreshes, and leaves relational shot actions dormant', async () => {
    render(<AstridTimelineEditor />);
    expect(screen.getByTestId('relational-actions')).toHaveTextContent('false');

    fireEvent.click(screen.getByText('Duplicate document shot'));
    await waitFor(() => expect(mocks.duplicateShotGroup).toHaveBeenCalledWith(expect.objectContaining({
      projectSlug: 'astrid-project',
      timelineRef: 'active-non-default',
      configVersion: 13,
      source: { shotId: 'shot-a', trackId: 'V1' },
    })));

    fireEvent.click(screen.getByText('Promote document variant'));
    await waitFor(() => expect(mocks.promotePrimaryVariant).toHaveBeenCalledWith({
      projectSlug: 'astrid-project',
      timelineRef: 'active-non-default',
      configVersion: 13,
      generationId: 'gen-a',
      variantId: 'variant-next',
    }));

    expect(mocks.reloadFromServer).toHaveBeenCalledTimes(2);
    expect(mocks.createShot).not.toHaveBeenCalled();
  });

  it('passes the original duplicated-media selection to one native insert intent without registering a legacy asset', async () => {
    const mediaSelection = {
      asset: 'asset-duplicated',
      generation_id: 'generation-duplicated',
      variant_id: 'variant-duplicated',
      object_id: `sha256:${'a'.repeat(64)}`,
      catalog_digest: `sha256:${'b'.repeat(64)}`,
    };
    const preparedAsset = {
      assetKey: 'asset-duplicated',
      mediaType: 'video' as const,
      durationSeconds: 2,
      entry: { file: 'https://example.test/duplicated.mp4', type: 'video/mp4', duration: 2 },
      source: 'registered' as const,
      mediaSelection,
    };
    mocks.duplicateGenerationAsset.mockResolvedValueOnce({
      generationId: 'generation-duplicated',
      variantId: 'variant-duplicated',
      variantType: 'video',
      imageUrl: 'https://example.test/duplicated.mp4',
      thumbUrl: 'https://example.test/duplicated-thumb.jpg',
      mediaSelection,
    });
    mocks.prepareGenerationAsset.mockReturnValueOnce(preparedAsset);
    mocks.addClip.mockResolvedValueOnce({ ok: true, data: { clipId: 'clip-duplicated', trackId: 'V1' } });
    render(<AstridTimelineEditor />);

    fireEvent.click(screen.getByText('Duplicate generation'));

    await waitFor(() => expect(mocks.addClip).toHaveBeenCalledTimes(1));
    expect(mocks.prepareGenerationAsset).toHaveBeenCalledWith(expect.objectContaining({ mediaSelection }));
    expect(mocks.addClip).toHaveBeenCalledWith({ preparedAsset, afterClipId: 'clip-source' });
    expect(mocks.registerGenerationAsset).not.toHaveBeenCalled();
  });

  it('refuses a duplicate when the parent head changes during generation duplication', async () => {
    const presenter = vi.fn(() => true);
    installRuntimeErrorPresenter(presenter);
    let resolveDuplicate!: (value: {
      generationId: string;
      variantId: string;
      variantType: 'video';
      imageUrl: string;
      thumbUrl: string;
    }) => void;
    mocks.duplicateGenerationAsset.mockImplementationOnce(() => new Promise((resolve) => {
      resolveDuplicate = resolve;
    }));
    render(<AstridTimelineEditor />);

    fireEvent.click(screen.getByText('Duplicate generation'));
    dataRef.current = { ...data, head: { revision_id: 'changed-before-insert' } };
    resolveDuplicate({
      generationId: 'generation-duplicated',
      variantId: 'variant-duplicated',
      variantType: 'video',
      imageUrl: 'https://example.test/duplicated.mp4',
      thumbUrl: 'https://example.test/duplicated-thumb.jpg',
    });

    await waitFor(() => expect(presenter).toHaveBeenCalledWith(
      expect.objectContaining({ message: expect.stringContaining('timeline changed') }),
      'Failed to duplicate generation',
    ));
    expect(mocks.prepareGenerationAsset).not.toHaveBeenCalled();
    expect(mocks.addClip).not.toHaveBeenCalled();
    dataRef.current = data;
  });

  it('refuses a duplicate when a pending native move advances the session generation during preparation', async () => {
    const presenter = vi.fn(() => true);
    installRuntimeErrorPresenter(presenter);
    let sessionGeneration = 0;
    const preparation = { localGeneration: 0 };
    mocks.parentClipAddMedia = {
      prepare: vi.fn(() => preparation),
      assertPreparationCurrent: vi.fn((captured) => {
        if ((captured as typeof preparation).localGeneration !== sessionGeneration) {
          throw new Error('Timeline changed during parent clip.add-media preparation');
        }
      }),
    };
    let resolveDuplicate!: (value: {
      generationId: string;
      variantId: string;
      variantType: 'video';
      imageUrl: string;
      thumbUrl: string;
      mediaSelection: Record<string, string>;
    }) => void;
    mocks.duplicateGenerationAsset.mockImplementationOnce(() => new Promise((resolve) => {
      resolveDuplicate = resolve;
    }));
    render(<AstridTimelineEditor />);

    fireEvent.click(screen.getByText('Duplicate generation'));
    sessionGeneration = 1;
    resolveDuplicate({
      generationId: 'generation-duplicated',
      variantId: 'variant-duplicated',
      variantType: 'video',
      imageUrl: 'https://example.test/duplicated.mp4',
      thumbUrl: 'https://example.test/duplicated-thumb.jpg',
      mediaSelection: {
        asset: 'asset-duplicated',
        generation_id: 'generation-duplicated',
        variant_id: 'variant-duplicated',
        object_id: `sha256:${'e'.repeat(64)}`,
        catalog_digest: `sha256:${'f'.repeat(64)}`,
      },
    });

    await waitFor(() => expect(presenter).toHaveBeenCalledWith(
      expect.objectContaining({ message: expect.stringContaining('parent clip.add-media preparation') }),
      'Failed to duplicate generation',
    ));
    expect(mocks.parentClipAddMedia.prepare).toHaveBeenCalledOnce();
    expect(mocks.parentClipAddMedia.assertPreparationCurrent).toHaveBeenCalledOnce();
    expect(mocks.prepareGenerationAsset).not.toHaveBeenCalled();
    expect(mocks.addClip).not.toHaveBeenCalled();
    expect(mocks.registerGenerationAsset).not.toHaveBeenCalled();
  });

  it('surfaces the native exact-placement refusal and does not write the legacy registry', async () => {
    const presenter = vi.fn(() => true);
    installRuntimeErrorPresenter(presenter);
    const mediaSelection = {
      asset: 'asset-duplicated',
      generation_id: 'generation-duplicated',
      variant_id: 'variant-duplicated',
      object_id: `sha256:${'c'.repeat(64)}`,
      catalog_digest: `sha256:${'d'.repeat(64)}`,
    };
    mocks.duplicateGenerationAsset.mockResolvedValueOnce({
      generationId: 'generation-duplicated',
      variantId: 'variant-duplicated',
      variantType: 'video',
      imageUrl: 'https://example.test/duplicated.mp4',
      thumbUrl: 'https://example.test/duplicated-thumb.jpg',
      mediaSelection,
    });
    mocks.prepareGenerationAsset.mockReturnValueOnce({
      assetKey: 'asset-duplicated',
      mediaType: 'video',
      durationSeconds: 2,
      entry: { file: 'https://example.test/duplicated.mp4', type: 'video/mp4', duration: 2 },
      source: 'registered',
      mediaSelection,
    });
    mocks.addClip.mockResolvedValueOnce({
      ok: false,
      error: {
        code: 'invalid_argument',
        message: 'Native prepared parent media cannot represent exact afterClip placement yet.',
      },
    });
    render(<AstridTimelineEditor />);

    fireEvent.click(screen.getByText('Duplicate generation'));

    await waitFor(() => expect(presenter).toHaveBeenCalledWith(
      expect.objectContaining({ message: expect.stringContaining('exact afterClip placement') }),
      'Failed to duplicate generation',
    ));
    expect(mocks.addClip).toHaveBeenCalledWith(expect.objectContaining({ afterClipId: 'clip-source' }));
    expect(mocks.registerGenerationAsset).not.toHaveBeenCalled();
  });

  it.each([
    {
      action: 'Promote document variant',
      title: 'Failed to promote primary variant',
      success: 'Primary variant promoted',
      fail: () => mocks.galleryGet.mockRejectedValueOnce(new Error('generation was not found')),
    },
    {
      action: 'Duplicate document shot',
      title: 'Failed to duplicate shot',
      success: 'Shot duplicated',
      fail: () => mocks.duplicateShotGroup.mockRejectedValueOnce(new Error('unknown family')),
    },
  ])('$action: a bridge failure shows the error toast, never a success toast, and leaves the document alone', async ({ action, title, success, fail }) => {
    const presenter = vi.fn(() => true);
    installRuntimeErrorPresenter(presenter);
    fail();
    render(<AstridTimelineEditor />);

    fireEvent.click(screen.getByText(action));

    await waitFor(() => expect(presenter).toHaveBeenCalledWith(expect.objectContaining({ message: expect.any(String) }), title));
    expect(mocks.toast.success).not.toHaveBeenCalledWith(success);
    expect(mocks.reloadFromServer).not.toHaveBeenCalled();
    expect(mocks.promotePrimaryVariant).not.toHaveBeenCalled();
  });

  it('opens a canonical shot editor overlay without reloading the document', () => {
    mocks.canonicalMode = true;
    render(<AstridTimelineEditor />);

    fireEvent.click(screen.getByText('Open canonical document shot'));

    expect(screen.getByTestId('canonical-shot-editor')).toBeInTheDocument();
    expect(screen.getByTestId('canonical-shot-editor')).toHaveTextContent(mocks.canonicalOccurrence.stableDeepLink);
    expect(mocks.navigate).not.toHaveBeenCalled();

    const dialog = screen.getByRole('dialog');
    expect(dialog).toHaveClass('max-w-4xl');
    fireEvent.keyDown(dialog, { key: 'Escape' });
    expect(screen.queryByTestId('canonical-shot-editor')).not.toBeInTheDocument();
  });
});
