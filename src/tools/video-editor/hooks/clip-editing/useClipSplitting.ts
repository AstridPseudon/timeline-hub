import { useCallback } from 'react';
import { toast } from '@/shared/components/ui/runtime/sonner.tsx';
import { captureClipSplitEdit, submitClipSplitEdit } from '../../commands/clipSplitGesture.ts';
import { canSplitClipAtTime, createSplitClipId, splitClipAtPlayhead } from '@/tools/video-editor/lib/editor-utils.ts';
import { splitIntersectingClipsAtPlayhead } from '@/tools/video-editor/lib/clip-editing-utils.ts';
import type { ClipEditingContext } from './types.ts';

export function useClipSplitting(ctx: ClipEditingContext) {
  const {
    applyConfigEdit,
    clipSplitPort,
    editability,
    selectClip,
    dataRef,
    resolvedConfig,
    selectedClipId,
    currentTimeRef,
    getValidClipIds,
    isPinnedGroupMember,
    notifyPinnedGroupEditBlocked,
  } = ctx;

  const handleSplitClipAtTime = useCallback((clipId: string, timeSeconds: number) => {
    const current = dataRef.current;
    if (!current) return;
    const clip = current.resolvedConfig.clips.find((entry) => entry.id === clipId);
    if (!clip) return;

    if (isPinnedGroupMember(clipId)) {
      notifyPinnedGroupEditBlocked();
      return;
    }
    if (!canSplitClipAtTime(clip, timeSeconds)) return;

    try {
      const allowed = editability?.checkTimeline?.() ?? { allowed: true };
      const target = editability?.check({ clipId, sourceTrackId: clip.track, targetTrackId: clip.track });
      if (!allowed.allowed || target?.allowed === false) {
        throw new Error('This clip cannot be split while timeline editing is locked.');
      }
      // Nonmedia splitting has no native contract yet; keep its existing ingress.
      if (clip.clipType !== 'media') {
        const splitResult = splitClipAtPlayhead(current.resolvedConfig, clipId, timeSeconds);
        if (splitResult.nextSelectedClipId) {
          applyConfigEdit(splitResult.config, { selectedClipId: splitResult.nextSelectedClipId });
        }
        return;
      }
      const rightId = createSplitClipId(current.resolvedConfig.clips.map((entry) => entry.id), clipId);
      const captured = captureClipSplitEdit(clipSplitPort, current, clipId, timeSeconds, rightId);
      submitClipSplitEdit(captured);
      selectClip(rightId);
    } catch (error) {
      toast.error(error instanceof Error ? error.message : 'Failed to split clip.');
    }
  }, [applyConfigEdit, clipSplitPort, dataRef, editability, isPinnedGroupMember, notifyPinnedGroupEditBlocked, selectClip]);

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
  }, [applyConfigEdit, dataRef, getValidClipIds, isPinnedGroupMember, notifyPinnedGroupEditBlocked, resolvedConfig]);

  return { handleSplitSelectedClip, handleSplitClipAtTime, handleSplitClipsAtPlayhead };
}
