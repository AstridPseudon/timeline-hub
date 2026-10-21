import { useCallback } from 'react';
import { toast } from '@/shared/components/ui/runtime/sonner.tsx';
import { isLiteralParentClip, splitParentClip } from '../../commands/clipSplitGesture.ts';
import { canSplitClipAtTime, splitClipAtPlayhead } from '@/tools/video-editor/lib/editor-utils.ts';
import { splitIntersectingClipsAtPlayhead } from '@/tools/video-editor/lib/clip-editing-utils.ts';
import type { ClipEditingContext } from './types.ts';

export function useClipSplitting(ctx: ClipEditingContext) {
  const {
    clipSplit,
    selectClip,
    applyConfigEdit,
    dataRef,
    resolvedConfig,
    selectedClipId,
    currentTimeRef,
    getValidClipIds,
    isPinnedGroupMember,
    notifyPinnedGroupEditBlocked,
  } = ctx;

  const handleSplitClipAtTime = useCallback((clipId: string, timeSeconds: number) => {
    if (!resolvedConfig) return;
    if (isPinnedGroupMember(clipId)) {
      notifyPinnedGroupEditBlocked();
      return;
    }
    const current = dataRef.current;
    const clip = current?.resolvedConfig.clips.find((entry) => entry.id === clipId);
    const nativeSupported = current !== null && clipSplit?.supports?.({ clipId, current }) === true;
    if (current && isLiteralParentClip(current, clipId) && !nativeSupported) {
      toast.error('Native clip split is unavailable for this parent clip.');
      return;
    }
    if (current && nativeSupported) {
      if (!clip || !canSplitClipAtTime(clip, timeSeconds)) return;
      try {
        selectClip(splitParentClip(clipSplit, current, clipId, timeSeconds));
      } catch (error) {
        toast.error(error instanceof Error ? error.message : 'Clip split failed');
      }
      return;
    }
    const splitResult = splitClipAtPlayhead(resolvedConfig, clipId, timeSeconds);
    if (!splitResult.nextSelectedClipId) return;
    applyConfigEdit(splitResult.config, { selectedClipId: splitResult.nextSelectedClipId });
  }, [applyConfigEdit, clipSplit, dataRef, isPinnedGroupMember, notifyPinnedGroupEditBlocked, resolvedConfig, selectClip]);

  const handleSplitSelectedClip = useCallback(() => {
    if (selectedClipId) handleSplitClipAtTime(selectedClipId, currentTimeRef.current);
  }, [currentTimeRef, handleSplitClipAtTime, selectedClipId]);

  const handleSplitClipsAtPlayhead = useCallback((clipIds: string[]) => {
    const current = dataRef.current;
    if (!current || !resolvedConfig) {
      return;
    }

    const validClipIds = getValidClipIds(clipIds);
    if (validClipIds.length === 0) {
      return;
    }

    if (validClipIds.some((clipId) => isPinnedGroupMember(clipId))) {
      notifyPinnedGroupEditBlocked();
      return;
    }

    if (validClipIds.length === 1) {
      const clipId = validClipIds[0];
      const nativeSupported = clipSplit?.supports?.({ clipId, current }) === true;
      if (isLiteralParentClip(current, clipId) && !nativeSupported) {
        toast.error('Native clip split is unavailable for this parent clip.');
        return;
      }
      if (nativeSupported) {
        handleSplitClipAtTime(clipId, currentTimeRef.current);
        return;
      }
    }

    const { config: nextResolvedConfig, didSplit } = splitIntersectingClipsAtPlayhead(
      resolvedConfig,
      current.rows,
      validClipIds,
      currentTimeRef.current,
    );
    if (!didSplit) {
      return;
    }

    applyConfigEdit(nextResolvedConfig);
  }, [applyConfigEdit, clipSplit, currentTimeRef, dataRef, getValidClipIds, handleSplitClipAtTime, isPinnedGroupMember, notifyPinnedGroupEditBlocked, resolvedConfig]);

  return { handleSplitSelectedClip, handleSplitClipAtTime, handleSplitClipsAtPlayhead };
}
