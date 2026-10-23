import React from 'react';
import { COARSE_TOUCH_TARGET } from '@/shared/components/ui/contracts/touchTarget';
import { cn } from '@/shared/components/ui/contracts/cn';
import type { Shot } from '@/domains/generation/types';
import { MediaGallery, type GalleryFilterState } from '@/shared/components/MediaGallery';
import type { GalleryConfig } from '@/shared/components/MediaGallery/types';
import { useShots } from '@/shared/contexts/ShotsContext';
import { SelectionContextMenu } from '@/shared/components/SelectionContextMenu';
import { SkeletonGallery } from '@/shared/components/ui/composed/skeleton-gallery';
import { useShotNavigation } from '@/shared/hooks/shots/useShotNavigation';
import { VideoGenerationModal } from '@/tools/travel-between-images/components/VideoGenerationModal';
import { useLassoSelection } from '../hooks/useLassoSelection';
import { useRenderBudget } from '@/shared/dev/useRenderBudget';
import { RuntimeAuthorityProvider } from '@/app/runtime/RuntimeAuthorityProvider';
import {
  userSelectGalleryItem,
  userSelectGalleryItems,
  useGallerySelection,
} from '@/shared/state/selectionStore';

type MediaGalleryProps = React.ComponentProps<typeof MediaGallery>;

interface GenerationsPaneLayoutModel {
  columns: number;
  itemsPerPage: number;
}

interface GenerationsPaneLoadingModel {
  isLoading: boolean;
  expectedItemCount?: number;
}

interface GenerationsPanePageModel {
  page: number;
  totalCount: number;
}

interface GenerationsPaneGalleryModel {
  runtimeProjectId: string | null;
  runtimeAuthority: boolean;
  items: MediaGalleryProps['images'];
  allShots: NonNullable<MediaGalleryProps['allShots']>;
  lastShotId?: string;
  filters: GalleryFilterState;
  onFiltersChange: (newFilters: GalleryFilterState) => void;
  onAddToShot: NonNullable<MediaGalleryProps['onAddToLastShot']>;
  onAddToShotWithoutPosition: NonNullable<MediaGalleryProps['onAddToLastShotWithoutPosition']>;
  onServerPageChange: NonNullable<
    NonNullable<MediaGalleryProps['pagination']>['onServerPageChange']
  >;
  generationFilters: MediaGalleryProps['generationFilters'];
  currentViewingShotId?: string;
  onAddGenerationToTimeline?: (generationId: string) => void;
  /** The selected editor belongs to another project than this gallery, so adding to it is refused. */
  addTargetProjectMismatch?: boolean;
  config?: Partial<GalleryConfig>;
  readOnly?: boolean;
  emptyStateMessage?: string;
}

interface GenerationsPaneGalleryProps {
  containerRef: React.Ref<HTMLDivElement>;
  projectAspectRatio?: string;
  layout: GenerationsPaneLayoutModel;
  loading: GenerationsPaneLoadingModel;
  pagination: GenerationsPanePageModel;
  error: Error | null;
  gallery: GenerationsPaneGalleryModel;
}

export function GenerationsPaneGallery({
  containerRef,
  projectAspectRatio,
  layout,
  loading,
  pagination,
  error,
  gallery,
}: GenerationsPaneGalleryProps): React.ReactElement {
  useRenderBudget('GenerationsPaneGallery', 5);
  const gallerySurfaceRef = React.useRef<HTMLDivElement | null>(null);
  const [contextMenuPosition, setContextMenuPosition] = React.useState<{ x: number; y: number } | null>(null);
  const [videoModalShot, setVideoModalShot] = React.useState<Shot | null>(null);
  const {
    selectedGalleryIds,
    gallerySelectionMap,
  } = useGallerySelection();
  const { shots } = useShots();
  const { navigateToShot } = useShotNavigation();
  const { selectionRect, handleMouseDown } = useLassoSelection({
    containerRef: gallerySurfaceRef,
    items: gallery.items,
    onSelectItems: (items, options) => {
      userSelectGalleryItems(items, { additive: options?.additive ?? false });
    },
  });

  const buildSelectionMeta = React.useCallback((image: MediaGalleryProps['images'][number]) => ({
    url: image.url ?? image.thumbUrl ?? '',
    type: image.type ?? image.contentType ?? (image.isVideo ? 'video/mp4' : 'image/png'),
    generationId: image.generation_id ?? image.id,
    variantId: image.primary_variant_id,
  }), []);

  const handleImageClick = React.useCallback((
    image: MediaGalleryProps['images'][number],
    modifiers?: { multiSelect: boolean },
  ) => {
    userSelectGalleryItem({
      id: image.id,
      ...buildSelectionMeta(image),
    }, { additive: modifiers?.multiSelect ?? false });
  }, [buildSelectionMeta]);

  const resolveSelectedGenerationIds = React.useCallback(() => (
    Array.from(gallerySelectionMap.values()).map((entry) => entry.generationId)
  ), [gallerySelectionMap]);

  const selectedGenerationIds = React.useMemo(() => resolveSelectedGenerationIds(), [resolveSelectedGenerationIds]);
  const selectedGenerationId = selectedGenerationIds[0];

  const existingShotsForSelection = React.useMemo(() => {
    if (selectedGenerationIds.length === 0 || !shots?.length) {
      return [] as Shot[];
    }

    return shots.filter((shot) => {
      const shotGenerationIds = new Set(
        (shot.images ?? [])
          .map((image) => image.generation_id)
          .filter((generationId): generationId is string => typeof generationId === 'string' && generationId.length > 0),
      );

      return selectedGenerationIds.every((generationId) => shotGenerationIds.has(generationId));
    });
  }, [selectedGenerationIds, shots]);

  const handleContextMenu = React.useCallback((
    event: React.MouseEvent,
    image: MediaGalleryProps['images'][number],
  ) => {
    event.preventDefault();
    if (!selectedGalleryIds.has(image.id)) {
      userSelectGalleryItem({
        id: image.id,
        ...buildSelectionMeta(image),
      }, { additive: false });
    }
    setContextMenuPosition({ x: event.clientX, y: event.clientY });
  }, [buildSelectionMeta, selectedGalleryIds]);

  const handleNavigateToShot = React.useCallback((shot: Shot) => {
    navigateToShot(shot, { isNewlyCreated: true });
  }, [navigateToShot]);

  const handleOpenGenerateVideo = React.useCallback((shot: Shot) => {
    setVideoModalShot(shot);
  }, []);

  return (
    <>
      <div
        ref={containerRef}
        className="flex-grow px-1 sm:px-3 overflow-y-auto overscroll-contain flex flex-col"
        style={{ WebkitOverflowScrolling: 'touch' }}
      >
        {loading.isLoading && gallery.items.length === 0 && (
          <SkeletonGallery
            count={loading.expectedItemCount ?? layout.itemsPerPage}
            fixedColumns={layout.columns}
            gapClasses="gap-2 sm:gap-4"
            darkSurface
            showControls={false}
            projectAspectRatio={projectAspectRatio}
            className="space-y-0 pb-4 pt-2"
          />
        )}

        {error && <p className="text-red-500 text-center">Error: {error.message}</p>}

        {gallery.items.length > 0 && (
          <div className={loading.isLoading ? 'opacity-60 pointer-events-none transition-opacity duration-200' : ''}>
            {gallery.onAddGenerationToTimeline && selectedGenerationId && (
              <div className="flex justify-end px-1 pt-2">
                <button
                  type="button"
                  className={cn(
                    'rounded border border-sky-400/60 px-2 py-1 text-[11px] text-sky-100 hover:bg-sky-500/15',
                    // On touch it is the way a tapped item reaches the timeline: a full-size target.
                    '[@media(pointer:coarse)]:px-4 [@media(pointer:coarse)]:text-sm',
                    COARSE_TOUCH_TARGET,
                    'disabled:cursor-not-allowed disabled:opacity-50 disabled:hover:bg-transparent',
                  )}
                  onClick={() => gallery.onAddGenerationToTimeline?.(selectedGenerationId)}
                  disabled={gallery.addTargetProjectMismatch}
                  title={gallery.addTargetProjectMismatch ? "This gallery's project is not the selected editor's project" : undefined}
                  data-testid="add-selected-generation-to-timeline"
                >
                  Add selected to timeline
                </button>
              </div>
            )}
            <div
              ref={gallerySurfaceRef}
              className="relative"
              onMouseDown={handleMouseDown}
            >
              <RuntimeAuthorityProvider value={{
                runtimeProjectId: gallery.runtimeProjectId,
                runtimeAuthority: gallery.runtimeAuthority,
              }}>
                <MediaGallery
                  images={gallery.items}
                  allShots={gallery.allShots}
                  lastShotId={gallery.lastShotId}
                  filters={gallery.filters}
                  onFiltersChange={gallery.onFiltersChange}
                  columnsPerRow={layout.columns}
                  onImageClick={handleImageClick}
                  onContextMenu={gallery.readOnly ? undefined : handleContextMenu}
                  onAddToLastShot={gallery.onAddToShot}
                  onAddToLastShotWithoutPosition={gallery.onAddToShotWithoutPosition}
                  className="space-y-0 pb-8"
                  selectedIds={selectedGalleryIds}
                  config={{
                    darkSurface: true,
                    reducedSpacing: true,
                    hidePagination: true,
                    hideTopFilters: true,
                    enableSingleClick: true,
                    ...gallery.config,
                  }}
                  pagination={{
                    offset: (pagination.page - 1) * layout.itemsPerPage,
                    totalCount: pagination.totalCount,
                    itemsPerPage: layout.itemsPerPage,
                    serverPage: pagination.page,
                    onServerPageChange: gallery.onServerPageChange,
                  }}
                  generationFilters={gallery.generationFilters}
                  currentViewingShotId={gallery.currentViewingShotId}
                />
              </RuntimeAuthorityProvider>
              {selectionRect && (
                <div
                  className="pointer-events-none absolute border border-sky-400 bg-sky-400/10"
                  style={{
                    left: selectionRect.left,
                    top: selectionRect.top,
                    width: selectionRect.width,
                    height: selectionRect.height,
                  }}
                />
              )}
            </div>
          </div>
        )}

        {gallery.items.length === 0 && !loading.isLoading && !error && (
          <div className="flex-1 flex items-center justify-center text-zinc-500">
            {gallery.emptyStateMessage}
          </div>
        )}
      </div>

      {!gallery.readOnly && (
        <SelectionContextMenu
          position={contextMenuPosition}
          onClose={() => setContextMenuPosition(null)}
          onNavigateToShot={handleNavigateToShot}
          onOpenGenerateVideo={handleOpenGenerateVideo}
          existingShots={existingShotsForSelection}
        />
      )}

      {videoModalShot && (
        <>
          {/* VideoGenerationModal only uses app-wide providers, so it can open from gallery selection flow. */}
          <VideoGenerationModal
            isOpen={true}
            onClose={() => setVideoModalShot(null)}
            shot={videoModalShot}
          />
        </>
      )}
    </>
  );
}
