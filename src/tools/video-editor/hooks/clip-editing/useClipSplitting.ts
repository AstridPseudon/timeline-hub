import { useCallback } from 'react';
import { toast } from '@/shared/components/ui/toast.tsx';
import { splitClipAtPlayhead } from '@/tools/video-editor/lib/editor-utils.ts';
import { attachGestureCommands, gestureCommandsFor, occurrenceIdentityFor, splitGestureCommands, structuralChildId } from '../../commands/semanticGestures.ts';
import type { ClipEditingContext } from './types.ts';

export function useClipSplitting(ctx: ClipEditingContext) {
  const { applyConfigEdit, dataRef, selectedClipId, currentTimeRef, getValidClipIds,
    isPinnedGroupMember, notifyPinnedGroupEditBlocked } = ctx;

  const splitClips = useCallback((ids: string[], at: number) => {
    const current = dataRef.current;
    if (!current) return;
    const requested = [...new Set(ids)];
    const valid = getValidClipIds(requested);
    if (valid.length !== requested.length) {
      toast.warning('Split selection is no longer available in its captured base');
      return;
    }
    if (valid.some(isPinnedGroupMember)) {
      notifyPinnedGroupEditBlocked();
      return;
    }
    const scopes = valid.map(id => occurrenceIdentityFor(current, id)?.occurrenceId ?? 'parent');
    if (new Set(scopes).size > 1) {
      toast.warning('Split selection must belong to one captured occurrence or parent');
      return;
    }
    let config = current.resolvedConfig;
    const editCommands = [];
    let selected: string | null = null;
    for (const id of valid) {
      const child = structuralChildId(current, id);
      const split = splitClipAtPlayhead(config, id, at, child);
      if (!split.nextSelectedClipId) continue;
      const commands = splitGestureCommands(current, id, at, child);
      if (!commands) {
        toast.warning('Split requires one literal, independent clip at a frame boundary', {
          description: 'Tied, grouped, animated or ambiguous clips need an explicit split choice.',
        });
        return; // Whole-batch refusal: no partial visual or semantic edit.
      }
      config = split.config;
      if (current.config.clips.find(clip => clip.id === id)?.app?.canonical) {
        // Optimistic geometry is not a new canonical source identity. Until
        // readback, this reserved scoped display ID cannot become a parent row.
        config = { ...config, clips: config.clips.map(clip => {
          if (clip.id !== child || !clip.app) return clip;
          const app = { ...clip.app }; delete app.canonical;
          return { ...clip, app };
        }) };
      }
      selected = child;
      editCommands.push(...commands);
    }
    if (editCommands.length) {
      // Validate the entire captured scope before any local/history/save effect.
      const probe = { ...current };
      attachGestureCommands(probe, editCommands, current);
      if (!gestureCommandsFor(probe)) {
        toast.warning('Split requires one exact current occurrence or parent scope');
        return;
      }
      applyConfigEdit(config, { selectedClipId: selected, semantic: true, editCommands });
    }
  }, [applyConfigEdit, dataRef, getValidClipIds, isPinnedGroupMember, notifyPinnedGroupEditBlocked]);

  const handleSplitSelectedClip = useCallback(() => {
    if (selectedClipId) splitClips([selectedClipId], currentTimeRef.current);
  }, [selectedClipId, splitClips, currentTimeRef]);
  const handleSplitClipAtTime = useCallback((id: string, at: number) => splitClips([id], at), [splitClips]);
  const handleSplitClipsAtPlayhead = useCallback((ids: string[]) => splitClips(ids, currentTimeRef.current), [splitClips, currentTimeRef]);
  return { handleSplitSelectedClip, handleSplitClipAtTime, handleSplitClipsAtPlayhead };
}
