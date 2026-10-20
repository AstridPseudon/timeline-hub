import { useCallback } from 'react';
import { toast } from '@/shared/components/ui/runtime/sonner.tsx';
import { captureClipDeleteEdit, submitClipDeleteEdit } from '../../commands/clipDeleteGesture.ts';
import type { ClipEditingContext, DeleteClipOptions } from './types.ts';

export function useClipDeletion(ctx: ClipEditingContext) {
  const {
    applyRowsEdit,
    clipDeletePort,
    editability,
    dataRef,
    getValidClipIds,
    isPinnedGroupMember,
    notifyPinnedGroupEditBlocked,
  } = ctx;

  const handleDeleteClips = useCallback((clipIds: string[], options?: DeleteClipOptions) => {
    const current = dataRef.current;
    if (!current) {
      return;
    }

    const validClipIds = getValidClipIds(clipIds);
    const clipIdSet = new Set(validClipIds);
    if (clipIdSet.size === 0) {
      return;
    }

    if (!options?.allowPinnedGroupDelete && validClipIds.some((clipId) => isPinnedGroupMember(clipId))) {
      notifyPinnedGroupEditBlocked();
      return;
    }

    if (clipDeletePort && clipIds.length === 1 && !isPinnedGroupMember(clipIds[0])) {
      try {
        const decision = editability?.checkTimeline('edit');
        if (decision && !decision.allowed) throw new Error(`Timeline edit refused: ${decision.reason}`);
        submitClipDeleteEdit(captureClipDeleteEdit(clipDeletePort, current, clipIds[0]));
      } catch (error) {
        toast.error(error instanceof Error ? error.message : 'Clip delete failed.');
      }
      return;
    }

    // Group and multi-delete keep their existing writer until native group support is qualified.
    const nextRows = current.rows.map((row) => ({
      ...row,
      actions: row.actions.filter((action) => !clipIdSet.has(action.id)),
    }));
    applyRowsEdit(nextRows, undefined, [...clipIdSet], undefined, { semantic: true });
  }, [applyRowsEdit, clipDeletePort, dataRef, editability, getValidClipIds, isPinnedGroupMember, notifyPinnedGroupEditBlocked]);

  const handleDeleteClip = useCallback((clipId: string, options?: DeleteClipOptions) => {
    handleDeleteClips([clipId], options);
  }, [handleDeleteClips]);

  return { handleDeleteClips, handleDeleteClip };
}
