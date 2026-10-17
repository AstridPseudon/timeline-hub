import { useCallback } from 'react';
import { positionResetCommands } from '../../commands/positionResetCommands.ts';
import { updateClipInConfig } from '@/tools/video-editor/lib/editor-utils.ts';
import type { ClipMeta } from '@/tools/video-editor/lib/timeline-data.ts';
import type { ClipEditingContext } from './types.ts';

export function useClipPositioning(ctx: ClipEditingContext) {
  const {
    applyConfigEdit,
    applyRowsEdit,
    dataRef,
    resolvedConfig,
    selectedClipId,
    getValidClipIds,
  } = ctx;

  const handleResetClipPosition = useCallback(() => {
    if (!selectedClipId || !resolvedConfig) {
      return;
    }

    const current = dataRef.current;
    if (!current) return;
    const editCommands = positionResetCommands(current, [selectedClipId]);
    if (!editCommands) return;

    const nextConfig = updateClipInConfig(current.resolvedConfig, selectedClipId, (clip) => ({
      ...clip,
      x: undefined,
      y: undefined,
      width: undefined,
      height: undefined,
      cropTop: undefined,
      cropBottom: undefined,
      cropLeft: undefined,
      cropRight: undefined,
    }));
    applyConfigEdit(nextConfig, { selectedClipId, editCommands });
  }, [applyConfigEdit, dataRef, resolvedConfig, selectedClipId]);

  const handleResetClipsPosition = useCallback((clipIds: string[]) => {
    const current = dataRef.current;
    if (!current) {
      return;
    }

    const validClipIds = getValidClipIds(clipIds);
    if (validClipIds.length === 0) {
      return;
    }

    // Preserve uploading-placeholder filtering, but never partially reset a stale member.
    if (clipIds.some(id => !id.startsWith('uploading-') && !validClipIds.includes(id))) return;
    const editCommands = positionResetCommands(current, validClipIds);
    if (!editCommands) return;

    const metaUpdates = Object.fromEntries(
      validClipIds.map((clipId) => [clipId, {
        x: undefined,
        y: undefined,
        width: undefined,
        height: undefined,
        cropTop: undefined,
        cropBottom: undefined,
        cropLeft: undefined,
        cropRight: undefined,
      }]),
    ) as Record<string, Partial<ClipMeta>>;

    applyRowsEdit(current.rows, metaUpdates, undefined, undefined, { editCommands });
  }, [applyRowsEdit, dataRef, getValidClipIds]);

  return { handleResetClipPosition, handleResetClipsPosition };
}
