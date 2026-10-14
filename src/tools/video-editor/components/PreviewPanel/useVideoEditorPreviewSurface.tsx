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
import { useTimelineDataSelector, useTimelinePlaybackSelector } from '@/tools/video-editor/hooks/timelineStore.ts';
import { useOptionalVideoEditorRuntime } from '@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx';
import { resolveCanonicalComposition } from '@/tools/video-editor/data/canonicalCompositionState.ts';

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
  const runtime = useOptionalVideoEditorRuntime();
  const hasShotClips = Boolean(resolvedConfig?.clips.some((clip) => clip.clipType === 'shot'));
  // Interactive preview should reflect an in-progress child-shot edit before
  // its canonical publication is acknowledged. Export/save still consume the
  // acknowledged composition through their own paths.
  const previewComposition = runtime?.userId === null
    ? runtime.shots?.canonicalDraft?.composition ?? runtime.shots?.canonicalComposition
    : null;
  const compositionResolution = useMemo(() => resolveCanonicalComposition({
    userId: runtime?.userId,
    hasShotClips,
    hasShotComposition: Boolean(runtime?.shots?.shotComposition),
    composition: previewComposition,
    compositionError: runtime?.userId === null ? runtime.shots?.canonicalCompositionError : null,
    baseConfig: resolvedConfig,
  }), [hasShotClips, previewComposition, resolvedConfig, runtime?.shots?.canonicalCompositionError,
    runtime?.shots?.shotComposition, runtime?.userId]);
  const previewConfig = compositionResolution.config;
  const previewSource = compositionResolution.source;
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
        key={`${previewSource}:${attachmentGeneration}`}
        ref={previewRef}
        config={previewConfig}
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
    previewSource,
    attachmentGeneration,
    slotNode,
  ]);

  return useMemo(() => ({
    slotRef,
    portal,
    hasConfig: Boolean(previewConfig),
  }), [portal, previewConfig, slotRef]);
}
