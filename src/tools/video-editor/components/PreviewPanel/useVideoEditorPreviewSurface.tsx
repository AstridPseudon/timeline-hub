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
import type { PreviewRevision } from './previewRevision.ts';

export interface VideoEditorPreviewSurface {
  slotRef: RefCallback<HTMLDivElement>;
  portal: ReactPortal | null;
  hasConfig: boolean;
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
  const compositionResolution = useVideoEditorPreviewComposition(resolvedConfig);
  const previewConfig = compositionResolution.config;
  const previewSource = compositionResolution.source;
  const previewRevision = useMemo<PreviewRevision>(() => {
    const error = runtime?.userId === null ? runtime.shots?.canonicalCompositionError : null;
    const unavailableTarget = error && typeof error === 'object'
      && 'targetRevisionId' in error && typeof error.targetRevisionId === 'string'
      ? { targetRevisionId: error.targetRevisionId, reason: error.message }
      : error ? { reason: error.message } : undefined;
    const canonicalDraft = runtime?.userId === null ? runtime.shots?.canonicalDraft : null;
    const canonicalComposition = runtime?.userId === null ? runtime.shots?.canonicalComposition : null;

    if (previewSource === 'canonical') {
      if (canonicalDraft) {
        return {
          kind: 'local',
          baseRevisionId: canonicalComposition?.headRevisionId ?? null,
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
  }, [compositionResolution.error?.message, previewSource, runtime?.shots?.canonicalComposition,
    runtime?.shots?.canonicalCompositionError, runtime?.shots?.canonicalDraft, runtime?.userId,
    saveStatus, timelineData?.head?.headRevisionId]);
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
  const [{slotNode, attachmentGeneration}, setAttachment] = useState<{
    slotNode: HTMLDivElement | null;
    attachmentGeneration: number;
  }>({slotNode: null, attachmentGeneration: 0});
  const [hostNode] = useState<HTMLDivElement | null>(() => {
    if (typeof document === 'undefined') {
      return null;
    }

    const host = document.createElement('div');
    host.style.display = 'contents';
    return host;
  });

  const slotRef = useCallback<RefCallback<HTMLDivElement>>((node) => {
    setAttachment((current) => current.slotNode === node
      ? current
      : {slotNode: node, attachmentGeneration: current.attachmentGeneration + 1});
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
    if (!hostNode || !hasConfig || !previewConfig || !slotNode) {
      return null;
    }

    return createPortal(
      <RemotionPreview
        // A physical slot move is a new preview attachment. Remount the
        // player-owned subtree at the current paused playhead for that case,
        // while ordinary config updates retain the existing DOM attachment.
        key={`${runtime?.project?.projectId ?? ''}:${runtime?.timelineId ?? ''}:${previewSource}:${attachmentGeneration}`}
        ref={previewRef}
        config={previewConfig}
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
    previewRevision,
    previewSource,
    attachmentGeneration,
    slotNode,
    runtime?.project?.projectId,
    runtime?.timelineId,
  ]);

  return useMemo(() => ({
    slotRef,
    portal,
    hasConfig: Boolean(previewConfig),
  }), [portal, previewConfig, slotRef]);
}
