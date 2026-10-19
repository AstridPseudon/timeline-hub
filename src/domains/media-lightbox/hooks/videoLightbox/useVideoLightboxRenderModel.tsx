import type { ComponentProps, ReactNode } from 'react';
import { useMemo } from 'react';
import type { VideoLightboxPropsWithMedia } from '../../types';
import type {
  VideoLightboxSharedStateModel,
  VideoLightboxInfoModel,
} from './useVideoLightboxController';
import type { VideoLightboxEnvironment, VideoLightboxModeModel } from './useVideoLightboxEnvironment';
import { useVideoLightboxActions } from './useVideoLightboxActions';
import { useAddToVideoEditor } from '../useAddToVideoEditor';
import { buildVideoLightboxLayoutState } from '../../model/buildVideoLightboxLayoutState';
import { InfoPanel } from '../../components/InfoPanel';
import type { WorkflowControlsBarProps } from '../../components/WorkflowControlsBar';
import type { LightboxStateValue } from '../../contexts/LightboxStateContext';

type InfoPanelModel = ComponentProps<typeof InfoPanel>;

function getVideoLightboxAccessibility(
  media: VideoLightboxPropsWithMedia['media'],
): { accessibilityTitle: string; accessibilityDescription: string } {
  return {
    accessibilityTitle: `Video Lightbox - ${media.id.substring(0, 8)}`,
    accessibilityDescription: 'View and interact with video in full screen. Use arrow keys to navigate, Escape to close.',
  };
}

export function useVideoLightboxRenderModel(
  props: VideoLightboxPropsWithMedia,
  modeModel: VideoLightboxModeModel,
  env: VideoLightboxEnvironment,
  sharedState: VideoLightboxSharedStateModel,
  infoModel: VideoLightboxInfoModel,
) {
  const {
    media,
    onClose,
    readOnly = false,
    adjacentSegments,
    showTickForImageId,
    showTickForSecondaryImageId,
    actions,
    shotWorkflow,
  } = props;

  const navigation = props.navigation;
  const features = props.features;
  const addToVideoEditor = useAddToVideoEditor(media);
  const showNavigation = navigation?.showNavigation ?? true;
  const showTaskDetails = features?.showTaskDetails ?? true;

  const lightboxVariants = useMemo<LightboxStateValue['variants']>(() => ({
    variants: sharedState.variants.list,
    activeVariant: sharedState.variants.activeVariant,
    primaryVariant: sharedState.variants.primaryVariant,
    isLoadingVariants: sharedState.variants.isLoading,
    handleVariantSelect: sharedState.variants.setActiveVariantId,
    handleMakePrimary: sharedState.variants.setPrimaryVariant,
    handleDeleteVariant: sharedState.variants.deleteVariant,
    promoteSuccess: sharedState.variants.promoteSuccess,
    isPromoting: sharedState.variants.isPromoting,
    handlePromoteToGeneration: sharedState.variants.handlePromoteToGeneration,
    isMakingMainVariant: sharedState.makeMainVariant.isMaking,
    canMakeMainVariant: sharedState.makeMainVariant.canMake,
    handleMakeMainVariant: sharedState.makeMainVariant.handle,
    pendingTaskCount: infoModel.variantBadges.pendingTaskCount,
    unviewedVariantCount: infoModel.variantBadges.unviewedVariantCount,
    onMarkAllViewed: infoModel.variantBadges.handleMarkAllViewed,
    variantsSectionRef: env.variantsSectionRef,
  }), [
    env.variantsSectionRef,
    infoModel.variantBadges.handleMarkAllViewed,
    infoModel.variantBadges.pendingTaskCount,
    infoModel.variantBadges.unviewedVariantCount,
    sharedState.makeMainVariant.canMake,
    sharedState.makeMainVariant.handle,
    sharedState.makeMainVariant.isMaking,
    sharedState.variants.activeVariant,
    sharedState.variants.deleteVariant,
    sharedState.variants.handlePromoteToGeneration,
    sharedState.variants.isLoading,
    sharedState.variants.isPromoting,
    sharedState.variants.list,
    sharedState.variants.primaryVariant,
    sharedState.variants.promoteSuccess,
    sharedState.variants.setActiveVariantId,
    sharedState.variants.setPrimaryVariant,
  ]);

  const lightboxStateValue = useMemo<LightboxStateValue>(() => ({
    core: {
      onClose,
      readOnly,
      isMobile: env.isMobile,
      isTabletOrLarger: sharedState.layout.isTabletOrLarger,
      selectedProjectId: env.selectedProjectId,
      actualGenerationId: env.actualGenerationId,
    },
    media: {
      media,
      isVideo: true,
      effectiveMediaUrl: sharedState.effectiveMedia.mediaUrl ?? '',
      effectiveVideoUrl: sharedState.effectiveMedia.videoUrl ?? '',
      effectiveImageDimensions: sharedState.effectiveMedia.imageDimensions,
      imageDimensions: env.imageDimensions,
      setImageDimensions: env.setImageDimensions,
    },
    variants: lightboxVariants,
    navigation: {
      showNavigation,
      hasNext: modeModel.hasNext,
      hasPrevious: modeModel.hasPrevious,
      handleSlotNavNext: modeModel.handleSlotNavNext,
      handleSlotNavPrev: modeModel.handleSlotNavPrev,
      swipeNavigation: sharedState.navigation.swipeNavigation,
    },
  }), [
    env.actualGenerationId,
    env.imageDimensions,
    env.isMobile,
    env.selectedProjectId,
    env.setImageDimensions,
    lightboxVariants,
    media,
    modeModel.handleSlotNavNext,
    modeModel.handleSlotNavPrev,
    modeModel.hasNext,
    modeModel.hasPrevious,
    onClose,
    readOnly,
    sharedState.effectiveMedia.imageDimensions,
    sharedState.effectiveMedia.mediaUrl,
    sharedState.effectiveMedia.videoUrl,
    sharedState.layout.isTabletOrLarger,
    sharedState.navigation.swipeNavigation,
    showNavigation,
  ]);

  const { handleDownload, handleDelete, handleNavigateToShotFromSelector } = useVideoLightboxActions({
    props,
    env,
    sharedState,
  });

  const layoutFlags = buildVideoLightboxLayoutState({
    isMobile: env.isMobile,
    isFormOnlyMode: modeModel.isFormOnlyMode,
    isTabletOrLarger: sharedState.layout.isTabletOrLarger,
    isPortraitMode: sharedState.layout.isPortraitMode,
    shouldShowSidePanel: sharedState.layout.shouldShowSidePanel,
    hasSegmentVideo: modeModel.hasSegmentVideo,
    showTaskDetails,
    isSegmentSlotMode: modeModel.isSegmentSlotMode,
    effectiveTasksPaneOpen: env.effectiveTasksPaneOpen,
    isTasksPaneLocked: env.isTasksPaneLocked,
  });

  const {
    shouldShowSidePanel,
    showPanel,
    needsFullscreenLayout,
    needsTasksPaneOffset,
    panelVariant,
  } = layoutFlags;
  const { accessibilityTitle, accessibilityDescription } = getVideoLightboxAccessibility(media);
  const panelTaskId = infoModel.adjustedTaskDetailsData?.taskId || media.source_task_id || null;
  const selectedShotId = shotWorkflow?.selectedShotId;

  const videoInfoPanelModel = useMemo<InfoPanelModel>(() => ({
    variant: panelVariant,
    taskPanel: {
      taskDetailsData: infoModel.adjustedTaskDetailsData,
    },
    taskId: panelTaskId,
  }), [infoModel.adjustedTaskDetailsData, panelTaskId, panelVariant]);

  const controlsPanelContent = useMemo<ReactNode | undefined>(() => {
    return showPanel ? <InfoPanel {...videoInfoPanelModel} /> : undefined;
  }, [showPanel, videoInfoPanelModel]);

  const workflowBar = useMemo<WorkflowControlsBarProps>(() => ({
    core: {
      isVideo: true,
      onAddToVideoEditor: actions?.onAddToVideoEditor ?? addToVideoEditor.onClick,
      addToVideoEditorPhase: actions?.onAddToVideoEditor ? 'idle' : addToVideoEditor.phase,
    },
    shotSelector: shotWorkflow?.onAddToShot
      ? {
          mediaId: env.actualGenerationId ?? media.id,
          imageUrl: sharedState.effectiveMedia.mediaUrl ?? '',
          thumbUrl: media.thumbUrl,
          allShots: shotWorkflow.allShots ?? [],
          selectedShotId,
          onShotChange: shotWorkflow.onShotChange,
          onCreateShot: shotWorkflow.onCreateShot,
          isAlreadyPositionedInSelectedShot: sharedState.shots.isAlreadyPositionedInSelectedShot,
          isAlreadyAssociatedWithoutPosition: sharedState.shots.isAlreadyAssociatedWithoutPosition,
          showTickForImageId,
          showTickForSecondaryImageId,
          onAddToShot: shotWorkflow.onAddToShot,
          onAddToShotWithoutPosition: shotWorkflow.onAddToShotWithoutPosition,
          onAddVariantAsNewGeneration: sharedState.variants.handleAddVariantAsNewGenerationToShot,
          activeVariantId: sharedState.variants.activeVariant?.id || sharedState.variants.primaryVariant?.id,
          currentTimelineFrame: media.timeline_frame ?? undefined,
          onShowTick: shotWorkflow.onShowTick,
          onOptimisticPositioned: shotWorkflow.onOptimisticPositioned,
          onShowSecondaryTick: shotWorkflow.onShowSecondaryTick,
          onOptimisticUnpositioned: shotWorkflow.onOptimisticUnpositioned,
          isAdding: false,
          isAddingWithoutPosition: false,
          contentRef: env.contentRef,
          onNavigateToShot: handleNavigateToShotFromSelector,
          onClose,
        }
      : undefined,
  }), [
    actions?.onAddToVideoEditor,
    addToVideoEditor.onClick,
    addToVideoEditor.phase,
    env.actualGenerationId,
    env.contentRef,
    handleNavigateToShotFromSelector,
    media.id,
    media.thumbUrl,
    media.timeline_frame,
    onClose,
    selectedShotId,
    sharedState.effectiveMedia.mediaUrl,
    sharedState.shots.isAlreadyAssociatedWithoutPosition,
    sharedState.shots.isAlreadyPositionedInSelectedShot,
    sharedState.variants.activeVariant?.id,
    sharedState.variants.handleAddVariantAsNewGenerationToShot,
    sharedState.variants.primaryVariant?.id,
    shotWorkflow?.allShots,
    shotWorkflow?.onAddToShot,
    shotWorkflow?.onAddToShotWithoutPosition,
    shotWorkflow?.onCreateShot,
    shotWorkflow?.onOptimisticPositioned,
    shotWorkflow?.onOptimisticUnpositioned,
    shotWorkflow?.onShotChange,
    shotWorkflow?.onShowSecondaryTick,
    shotWorkflow?.onShowTick,
    showTickForImageId,
    showTickForSecondaryImageId,
  ]);

  const layoutProps = useMemo(() => ({
    showPanel,
    shouldShowSidePanel,
    effectiveTasksPaneOpen: env.effectiveTasksPaneOpen,
    effectiveTasksPaneWidth: env.effectiveTasksPaneWidth,
    workflowBar,
    buttonGroups: {
      bottomLeft: sharedState.buttonGroupProps.bottomLeft,
      bottomRight: sharedState.buttonGroupProps.bottomRight,
      topRight: {
        ...sharedState.buttonGroupProps.topRight,
        handleDownload,
        handleDelete,
      },
    },
    customOverlay: props.customOverlay,
    adjacentSegments,
    segmentSlotMode: modeModel.hasSegmentVideo ? props.segmentSlotMode : undefined,
  }), [
    adjacentSegments,
    props.customOverlay,
    env.effectiveTasksPaneOpen,
    env.effectiveTasksPaneWidth,
    handleDelete,
    handleDownload,
    modeModel.hasSegmentVideo,
    props.segmentSlotMode,
    sharedState.buttonGroupProps.bottomLeft,
    sharedState.buttonGroupProps.bottomRight,
    sharedState.buttonGroupProps.topRight,
    shouldShowSidePanel,
    showPanel,
    workflowBar,
  ]);

  return {
    lightboxStateValue,
    controlsPanelContent,
    layoutProps,
    needsFullscreenLayout,
    needsTasksPaneOffset,
    accessibilityTitle,
    accessibilityDescription,
  };
}
