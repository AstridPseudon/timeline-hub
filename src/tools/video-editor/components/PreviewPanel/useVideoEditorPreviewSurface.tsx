import { boundCanonicalRenderConfig } from '../../lib/canonicalRenderBounds.ts';
import { compilePlayerTransitions } from '../../compositions/playerEvaluation.ts';
import type { ReactPortal } from 'react';
import { createPortal } from 'react-dom';
import {
  useCallback,
  useLayoutEffect,
  useMemo,
  useState,
  type RefCallback,
} from 'react';
import { shallow } from 'zustand/shallow';
import { RemotionPreview } from '@/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx';
import { useTimelineChromeSelector, useTimelineDataSelector, useTimelinePlaybackSelector } from '@/tools/video-editor/hooks/timelineStore.ts';
import { useOptionalVideoEditorRuntime } from '@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx';
import { useVideoEditorPreviewComposition } from './useVideoEditorPreviewComposition.ts';
import { previewUnavailableLabel, type PreviewRevision } from './previewRevision.ts';

export interface VideoEditorPreviewSurface {
  slotRef: RefCallback<HTMLDivElement>;
  portal: ReactPortal | null;
  hasConfig: boolean;
  /** Why the surface has no Player-backed preview yet. */
  availability?: 'loading' | 'unavailable' | 'ready';
  unavailableReason?: string;
}

export function useVideoEditorPreviewSurface({
  compact = false,
  touchChrome = false,
}: {
  compact?: boolean;
  touchChrome?: boolean;
} = {}): VideoEditorPreviewSurface {
  const resolvedConfig = useTimelineDataSelector((timeline) => timeline.resolvedConfig);
  const timelineData = useTimelineDataSelector((timeline) => timeline.data);
  const saveStatus = useTimelineChromeSelector((chrome) => chrome.saveStatus);
  const runtime = useOptionalVideoEditorRuntime();
  const compositionResolution = useVideoEditorPreviewComposition(resolvedConfig, timelineData);
  const sourceConfig = compositionResolution.config;
  const previewConfig = useMemo(() => compositionResolution.source === 'canonical' && sourceConfig
    ? boundCanonicalRenderConfig(sourceConfig) : sourceConfig, [sourceConfig, compositionResolution.source]);
  const previewSource = compositionResolution.source;
  const compiledTransitions = useMemo(() => previewSource === 'canonical' && previewConfig
    ? compilePlayerTransitions(previewConfig) : undefined, [previewConfig, previewSource]);
  const previewRevision = useMemo<PreviewRevision>(() => {
    const fact = timelineData?.editProjection;
    const paired = fact && sourceConfig === timelineData.resolvedConfig;
    const error = runtime?.userId === null ? runtime.shots?.canonicalCompositionError : null;
    const unavailableTarget = fact && !paired
      ? {
        ...(fact.kind === 'accepted' ? { targetRevisionId: fact.head.revisionId } : {}),
        reason: compositionResolution.error?.message ?? 'The command projection is unavailable.',
      }
      : error && typeof error === 'object'
      && 'targetRevisionId' in error && typeof error.targetRevisionId === 'string'
      ? { targetRevisionId: error.targetRevisionId, reason: error.message }
      : error ? { reason: error.message } : undefined;
    if (paired) {
      return {
        ...(fact.kind === 'accepted'
          ? { kind: 'committed' as const, revisionId: fact.head.revisionId }
          : { kind: 'local' as const, baseRevisionId: fact.base.revisionId }),
        ...(unavailableTarget ? { unavailableTarget } : {}),
      };
    }
    const canonicalDraft = runtime?.userId === null ? runtime.shots?.canonicalDraft : null;
    const canonicalComposition = runtime?.userId === null ? runtime.shots?.canonicalComposition : null;

    if (previewSource === 'canonical') {
      if (canonicalDraft) {
        return {
          kind: 'local',
          // The server head may advance while this draft remains the pixels
          // being projected. Its own graph head is the only known base for
          // the draft; the server snapshot is not an acknowledgement of it.
          baseRevisionId: canonicalDraft.composition.headRevisionId,
          ...(unavailableTarget ? { unavailableTarget } : {}),
        };
      }
      if (canonicalComposition) {
        return {
          kind: 'committed',
          revisionId: canonicalComposition.headRevisionId,
          ...(unavailableTarget ? { unavailableTarget } : {}),
        };
      }
      return unavailableTarget
        ? { kind: 'unavailable', unavailableTarget }
        : { kind: 'unknown', reason: compositionResolution.error?.message };
    }

    const baseRevisionId = timelineData?.head?.headRevisionId;
    if (saveStatus !== 'saved') {
      return {
        kind: 'local',
        baseRevisionId: baseRevisionId ?? null,
        ...(unavailableTarget ? { unavailableTarget } : {}),
      };
    }
    if (baseRevisionId) {
      return {
        kind: 'committed',
        revisionId: baseRevisionId,
        ...(unavailableTarget ? { unavailableTarget } : {}),
      };
    }
    return unavailableTarget
      ? { kind: 'unavailable', unavailableTarget }
      : { kind: 'unknown', reason: 'The loaded timeline has no committed revision identity.' };
  }, [compositionResolution.error?.message, sourceConfig, previewSource, runtime?.shots?.canonicalComposition,
    runtime?.shots?.canonicalCompositionError, runtime?.shots?.canonicalDraft, runtime?.userId,
    saveStatus, timelineData]);
  const {
    currentTime,
    previewRef,
    playerContainerRef,
    onPreviewTimeUpdate,
  } = useTimelinePlaybackSelector((playback) => ({
    currentTime: playback.currentTime,
    previewRef: playback.previewRef,
    playerContainerRef: playback.playerContainerRef,
    onPreviewTimeUpdate: playback.onPreviewTimeUpdate,
  }), shallow);
  const hasConfig = Boolean(previewConfig);
  const [slotNode, setSlotNode] = useState<HTMLDivElement | null>(null);
  const [hostNode] = useState<HTMLDivElement | null>(() => {
    if (typeof document === 'undefined') {
      return null;
    }

    const host = document.createElement('div');
    host.style.display = 'contents';
    return host;
  });

  const slotRef = useCallback<RefCallback<HTMLDivElement>>((node) => {
    setSlotNode(node);
  }, []);

  useLayoutEffect(() => {
    if (!hostNode || !hasConfig || !slotNode) {
      return;
    }

    if (hostNode.parentElement !== slotNode) {
      slotNode.appendChild(hostNode);
    }

    return () => {
      hostNode.remove();
    };
  }, [hasConfig, hostNode, slotNode]);

  const portal = useMemo(() => {
    if (!hostNode || !hasConfig || !previewConfig) {
      return null;
    }

    return createPortal(
      <RemotionPreview
        // Only a content scope change replaces the player. Moving its host
        // between layout slots retains playback and the player-owned DOM.
        key={`${runtime?.project?.projectId ?? ''}:${runtime?.timelineId ?? ''}:${previewSource}`}
        ref={previewRef}
        config={previewConfig}
        compiledTransitions={compiledTransitions}
        previewRevision={previewRevision}
        compact={compact}
        touchChrome={touchChrome}
        initialTime={currentTime}
        onTimeUpdate={onPreviewTimeUpdate}
        playerContainerRef={playerContainerRef}
      />,
      hostNode,
    );
  }, [
    compact,
    currentTime,
    touchChrome,
    hostNode,
    hasConfig,
    onPreviewTimeUpdate,
    playerContainerRef,
    previewRef,
    previewConfig,
    compiledTransitions,
    previewRevision,
    previewSource,
    runtime?.project?.projectId,
    runtime?.timelineId,
  ]);

  return useMemo(() => ({
    slotRef,
    portal,
    hasConfig: Boolean(previewConfig),
    availability: previewConfig
      ? 'ready'
      : compositionResolution.status === 'error'
        ? 'unavailable'
        : 'loading',
    ...(compositionResolution.status === 'error' && compositionResolution.error?.message
      ? { unavailableReason: timelineData?.editProjection && previewRevision.unavailableTarget
        ? `${previewUnavailableLabel(previewRevision.unavailableTarget)}: ${compositionResolution.error.message}`
        : compositionResolution.error.message }
      : {}),
  }), [compositionResolution.error?.message, compositionResolution.status, portal, previewConfig,
    previewRevision.unavailableTarget, slotRef, timelineData?.editProjection]);
}
