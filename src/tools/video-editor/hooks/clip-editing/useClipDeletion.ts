import { useCallback } from 'react';
import { toast } from '@/shared/components/ui/runtime/sonner.tsx';
import { object } from '../../commands/clipMovePrimitives.ts';
import type { ClipEditingContext, DeleteClipOptions } from './types.ts';

function isParentClipDeleteTarget(current: ClipEditingContext['dataRef']['current'], clipId: string): boolean {
  if (!current || current.config.pinnedShotGroups?.some((group) => group.clipIds.includes(clipId))) return false;
  const clip = current.resolvedConfig.clips.find((candidate) => candidate.id === clipId);
  if (!clip) return false;
  const canonical = clip.app?.canonical;
  if (!object(canonical)) return true;
  const ownerRef = canonical.ownerRef;
  const clipRef = canonical.clipRef;
  return ![ownerRef, clipRef].some((ref) => typeof ref === 'string' && ref.startsWith('occurrence:'));
}

export function useClipDeletion(ctx: ClipEditingContext) {
  const {
    applyRowsEdit,
    genericPatchPort,
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

    if (genericPatchPort && clipIds.length === 1 && isParentClipDeleteTarget(current, clipIds[0])) {
      try {
        const decision = editability?.checkTimeline?.();
        if (decision && !decision.allowed) throw new Error(`Timeline edit refused: ${decision.reason}`);
        const patch = { version: current.configVersion, operations: [{ op: 'clip.remove' as const, target: clipIds[0] }] };
        const captured = genericPatchPort.capture({ patch, current });
        genericPatchPort.submit(genericPatchPort.finish(captured));
      } catch (error) {
        toast.error(error instanceof Error ? error.message : 'Clip delete failed.');
      }
      return;
    }

    const nextRows = current.rows.map((row) => ({
      ...row,
      actions: row.actions.filter((action) => !clipIdSet.has(action.id)),
    }));
    applyRowsEdit(nextRows, undefined, [...clipIdSet], undefined, { semantic: true });
  }, [applyRowsEdit, dataRef, editability, genericPatchPort, getValidClipIds, isPinnedGroupMember, notifyPinnedGroupEditBlocked]);

  const handleDeleteClip = useCallback((clipId: string, options?: DeleteClipOptions) => {
    handleDeleteClips([clipId], options);
  }, [handleDeleteClips]);

  return { handleDeleteClips, handleDeleteClip };
}
