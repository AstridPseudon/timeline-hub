import { useCallback } from 'react';
import { toast } from '@/shared/components/ui/runtime/sonner.tsx';
import { captureClipDeleteEdit, submitClipDeleteEdit } from '../../commands/clipDeleteGesture.ts';
import type { ClipEditingContext, DeleteClipOptions } from './types.ts';

export function useClipDeletion(ctx: ClipEditingContext) {
  const {
    clipDeletePort,
    applyRowsEdit,
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

    // Group, occurrence and multi-clip deletion remain separate, unconverted ingresses.
    if (clipIdSet.size === 1 && !isPinnedGroupMember(validClipIds[0])) {
      try {
        if (!clipDeletePort) throw new Error('clip.delete capture is unavailable.');
        if (clipDeletePort.resolveOwner({ clipId: validClipIds[0], current }) === 'parent') {
          submitClipDeleteEdit(captureClipDeleteEdit(clipDeletePort, current, validClipIds[0], 'parent'));
          return;
        }
      } catch (error) {
        toast.error(error instanceof Error ? error.message : 'Clip deletion failed.');
        return;
      }
    }

    const nextRows = current.rows.map((row) => ({
      ...row,
      actions: row.actions.filter((action) => !clipIdSet.has(action.id)),
    }));
    applyRowsEdit(nextRows, undefined, [...clipIdSet], undefined, { semantic: true });
  }, [applyRowsEdit, clipDeletePort, dataRef, getValidClipIds, isPinnedGroupMember, notifyPinnedGroupEditBlocked]);

  const handleDeleteClip = useCallback((clipId: string, options?: DeleteClipOptions) => {
    handleDeleteClips([clipId], options);
  }, [handleDeleteClips]);

  return { handleDeleteClips, handleDeleteClip };
}
