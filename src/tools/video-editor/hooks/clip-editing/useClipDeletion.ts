import { useCallback } from 'react';
import { toast } from '@/shared/components/ui/runtime/sonner.tsx';
import { captureClipDeleteEdit, submitClipDeleteEdit } from '../../commands/clipDeleteGesture.ts';
import type { TimelineApplyEdit } from '../timeline-state-types.ts';
import type { ClipEditingContext, DeleteClipOptions } from './types.ts';

/** Public snapshot callers (including expanded keyboard groups) cannot delete rows. */
export function applyEditWithClipDeleteGuard(
  applyEdit: TimelineApplyEdit,
  ...args: Parameters<TimelineApplyEdit>
): void {
  const [mutation] = args;
  if (mutation.type === 'rows' && mutation.metaDeletes?.length) {
    toast.error('Clip deletion requires captured commands; grouped and mixed deletes require shared batch support.');
    return;
  }
  // Prepared-media replacement remains its separate, unconverted writer.
  applyEdit(...args);
}

export function useClipDeletion(ctx: ClipEditingContext) {
  const {
    clipDeletePort,
    editability,
    dataRef,
    getValidClipIds,
    isPinnedGroupMember,
    notifyPinnedGroupEditBlocked,
  } = ctx;

  const handleDeleteClips = useCallback((clipIds: string[], _options?: DeleteClipOptions) => {
    const current = dataRef.current;
    if (!current) {
      return;
    }

    const requested = [...new Set(clipIds)];
    if (requested.length === 0) {
      return;
    }

    // The keyboard's expanded shot selection must not bypass this boundary.
    if (requested.some((clipId) => isPinnedGroupMember(clipId))) {
      notifyPinnedGroupEditBlocked();
      return;
    }

    if (requested.length !== 1) {
      toast.error('Deleting multiple clips requires shared batch command support.');
      return;
    }
    if (getValidClipIds(requested).length !== 1) return;

    try {
      const permission = editability?.checkTimeline?.();
      if (permission?.allowed === false) {
        throw new Error(`Timeline delete denied (${permission.reason ?? 'read_only'}).`);
      }
      const captured = captureClipDeleteEdit(clipDeletePort, current, requested[0]);
      submitClipDeleteEdit(captured);
    } catch (cause) {
      toast.error(cause instanceof Error ? cause.message : 'Clip delete failed.');
    }
  }, [clipDeletePort, dataRef, editability, getValidClipIds, isPinnedGroupMember, notifyPinnedGroupEditBlocked]);

  const handleDeleteClip = useCallback((clipId: string, options?: DeleteClipOptions) => {
    handleDeleteClips([clipId], options);
  }, [handleDeleteClips]);

  return { handleDeleteClips, handleDeleteClip };
}
