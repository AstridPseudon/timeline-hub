import { deleteGestureCommands } from '../../commands/semanticGestures.ts';
import { buildDeleteShotGroupCommand } from '../../commands/shotGroupCommands.ts';
import { useCallback } from 'react';
import type { ClipEditingContext, DeleteClipOptions } from './types.ts';

export function useClipDeletion(ctx: ClipEditingContext) {
  const {
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

    // Full explicit group deletion uses the same atomic producer as Delete shot.
    // Ordinary deletion and the keyboard/member guard retain their own paths.
    let groupCommand;
    if (options?.allowPinnedGroupDelete && validClipIds.some(isPinnedGroupMember)) {
      const group = current.config.pinnedShotGroups?.find(group => group.clipIds.length === clipIdSet.size
        && group.clipIds.every(id => clipIdSet.has(id)));
      if (group) {
        const command = buildDeleteShotGroupCommand(current, group);
        if (!command) { notifyPinnedGroupEditBlocked(); return; }
        groupCommand = command;
      }
    }

    const nextRows = current.rows.map((row) => ({
      ...row,
      actions: row.actions.filter((action) => !clipIdSet.has(action.id)),
    }));
    applyRowsEdit(nextRows, undefined, [...clipIdSet], undefined, { semantic: true, editCommands: groupCommand ? [groupCommand] : deleteGestureCommands(current, [...clipIdSet]) });
  }, [applyRowsEdit, dataRef, getValidClipIds, isPinnedGroupMember, notifyPinnedGroupEditBlocked]);

  const handleDeleteClip = useCallback((clipId: string, options?: DeleteClipOptions) => {
    handleDeleteClips([clipId], options);
  }, [handleDeleteClips]);

  return { handleDeleteClips, handleDeleteClip };
}
