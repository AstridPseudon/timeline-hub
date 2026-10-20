import { useCallback } from 'react';
import { toast } from '@/shared/components/ui/runtime/sonner.tsx';
import { captureClipSplitBatchEdit, submitClipSplitBatchEdit } from '../../commands/clipSplitBatchGesture.ts';
import { object } from '../../commands/clipMovePrimitives.ts';
import { captureClipSplitEdit, submitClipSplitEdit } from '../../commands/clipSplitGesture.ts';
import { canSplitClipAtTime, createSplitClipId, splitClipAtPlayhead } from '@/tools/video-editor/lib/editor-utils.ts';
import { splitIntersectingClipsAtPlayhead } from '@/tools/video-editor/lib/clip-editing-utils.ts';
import type { ClipEditingContext } from './types.ts';

// These forms keep the pre-existing batch ingress until their native contracts are qualified.
function requiresLegacyBatchSplit(clip: Record<string, unknown>): boolean {
  if (clip.clipType !== 'media' || typeof clip.asset !== 'string') return true;
  if (['clip_type', 'asset_id', 'media_id', 'object_id', 'at_ms', 'from_ms', 'to_ms',
    'duration', 'duration_ms', 'time_map', 'timeMap', 'clips', 'children', 'transition', 'effects',
    'animation', 'animations', 'keyframes', 'enter', 'exit', 'continuous'].some((key) => clip[key] != null)) return true;
  const params = object(clip.params) ? clip.params : undefined;
  if (params && ['keyframes', 'animation', 'animations', 'effects', 'fade_in', 'fade_out',
    'volume_curve', 'fadeIn', 'fadeOut', 'fadeInCurve', 'fadeOutCurve'].some((key) => params[key] != null)) return true;
  const app = object(clip.app) ? clip.app : undefined;
  for (const container of [clip, app, object(app?.astrid) ? app.astrid : undefined]) {
    if (container && (container.fixed_start != null && container.fixed_start !== true
      || container.for != null && typeof container.for !== 'number')) return true;
    if (container && ['on', 'until', 'until_film_end', 'cut', 'sequence', 'sequence_index', 'sequence_fit',
      'orphan', 'formulas', 'anchor', 'standin', 'standin_intent', 'words', 'beats'].some((key) => container[key] != null)) return true;
  }
  const source = object(clip.assetEntry) ? clip.assetEntry : undefined;
  const kind = typeof source?.type === 'string'
    ? source.type.trim().toLowerCase().split(';', 1)[0].split('/', 1)[0].split('-', 1)[0] : undefined;
  if (!kind || !['image', 'video', 'audio'].includes(kind)) return true;
  return (clip.from == null || clip.to == null) && source?.type !== 'image';
}

export function useClipSplitting(ctx: ClipEditingContext) {
  const {
    applyConfigEdit,
    clipSplitPort,
    clipSplitBatchPort,
    editability,
    selectClip,
    dataRef,
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
      const rightId = createSplitClipId(current.resolvedConfig.clips.map((entry) => entry.id), clipId);
      // Plain nonmedia editing keeps its original ingress; canonical rows require the session's raw guards.
      if ((!current.head && !clipSplitPort && clip.clipType !== 'media')
        || clipSplitPort?.useLegacy({ current, clipId, rightId })) {
        const splitResult = splitClipAtPlayhead(current.resolvedConfig, clipId, timeSeconds, rightId);
        if (splitResult.nextSelectedClipId) {
          applyConfigEdit(splitResult.config, { selectedClipId: splitResult.nextSelectedClipId });
        }
        return;
      }
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
    if (!current) return;
    const on = currentTimeRef.current;
    const validClipIds = getValidClipIds(clipIds);
    if (!validClipIds.length) return;
    if (validClipIds.some((clipId) => isPinnedGroupMember(clipId))) {
      notifyPinnedGroupEditBlocked();
      return;
    }
    const intersecting = new Set(current.rows.flatMap((row) => row.actions)
      .filter((action) => action.start <= on && on < action.end).map((action) => action.id));
    const targets = validClipIds.flatMap((id) => {
      const clip = current.resolvedConfig.clips.find((entry) => entry.id === id);
      return clip && intersecting.has(id) && canSplitClipAtTime(clip, on) ? [clip] : [];
    });
    if (!targets.length) return;

    try {
      const allowed = editability?.checkTimeline?.() ?? { allowed: true };
      if (!allowed.allowed || targets.some((clip) => editability?.check({
        clipId: clip.id, sourceTrackId: clip.track, targetTrackId: clip.track,
      }).allowed === false)) {
        throw new Error('These clips cannot be split while timeline editing is locked.');
      }
      if (targets.some(requiresLegacyBatchSplit) || current.config.clips.some((clip) => clip.transition != null)) {
        const result = splitIntersectingClipsAtPlayhead(current.resolvedConfig, current.rows, validClipIds, on);
        if (result.didSplit) applyConfigEdit(result.config);
        return;
      }
      const captured = captureClipSplitBatchEdit(clipSplitBatchPort, current, validClipIds, on);
      if (captured) submitClipSplitBatchEdit(captured);
    } catch (error) {
      toast.error(error instanceof Error ? error.message : 'Failed to split clips.');
    }
  }, [applyConfigEdit, clipSplitBatchPort, currentTimeRef, dataRef, editability, getValidClipIds,
    isPinnedGroupMember, notifyPinnedGroupEditBlocked]);

  return { handleSplitSelectedClip, handleSplitClipAtTime, handleSplitClipsAtPlayhead };
}
