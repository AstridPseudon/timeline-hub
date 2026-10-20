import { useCallback } from 'react';
import { toast } from '@/shared/components/ui/runtime/sonner.tsx';
import { captureClipDeleteEdit, submitClipDeleteEdit } from '../../commands/clipDeleteGesture.ts';
import { captureClipDeleteBatchEdit, submitClipDeleteBatchEdit } from '../../commands/clipDeleteBatchGesture.ts';
import type { ClipEditingContext, DeleteClipOptions } from './types.ts';

export function useClipDeletion(ctx: ClipEditingContext) {
  const {
    clipDeletePort,
    clipDeleteBatchPort,
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

    const validClipIds = Object.freeze(getValidClipIds(clipIds, current));
    const clipIdSet = new Set(validClipIds);
    if (clipIdSet.size === 0) {
      return;
    }

    const hasPinnedMember = validClipIds.some((clipId) => isPinnedGroupMember(clipId, current));
    if (!options?.allowPinnedGroupDelete && hasPinnedMember) {
      notifyPinnedGroupEditBlocked();
      return;
    }

    // Group, occurrence and mixed ownership remain separate, unconverted ingresses.
    if (!hasPinnedMember) {
      try {
        if (!clipDeletePort) throw new Error('clip.delete capture is unavailable.');
        const members = validClipIds.map((clipId) => ({ clipId, ownerRef: clipDeletePort.resolveOwner({ clipId, current }) }));
        if (members.every(({ ownerRef }) => ownerRef === 'parent')) {
          if (members.length === 1) {
            submitClipDeleteEdit(captureClipDeleteEdit(clipDeletePort, current, validClipIds[0], 'parent'));
          } else {
            submitClipDeleteBatchEdit(captureClipDeleteBatchEdit(clipDeleteBatchPort, current,
              members.map(({ clipId }) => ({ clipId, ownerRef: 'parent' }))));
          }
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
  }, [applyRowsEdit, clipDeletePort, clipDeleteBatchPort, dataRef, getValidClipIds, isPinnedGroupMember, notifyPinnedGroupEditBlocked]);

  const handleDeleteClip = useCallback((clipId: string, options?: DeleteClipOptions) => {
    handleDeleteClips([clipId], options);
  }, [handleDeleteClips]);

  return { handleDeleteClips, handleDeleteClip };
}
