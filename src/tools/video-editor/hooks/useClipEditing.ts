import { continuousBatchGestureCommands, continuousEffectGestureCommands, compositeEffectGestureCommands, propertyGestureCommands, moveGestureCommands } from '../commands/semanticGestures.ts';
import { useCallback, useLayoutEffect, useRef } from 'react';
import type { Dispatch, MutableRefObject, SetStateAction } from 'react';
import { toast } from '@/shared/components/ui/runtime/sonner.tsx';
import type { SelectClipOptions } from '@/shared/state/selectionStore.ts';
import {
  patchAffectsDuration,
  recalcActionEnd,
} from '@/tools/video-editor/lib/clip-editing-utils.ts';
import { findEnclosingPinnedGroup } from '@/tools/video-editor/lib/pinned-group-projection.ts';
import {
  type ClipMeta,
  type ClipEditorPatch,
  type TimelineData,
} from '@/tools/video-editor/lib/timeline-data.ts';
import { useOptionalVideoEditorRuntime } from '@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx';
import type { ApplyEditOptions } from '@/tools/video-editor/hooks/useTimelineCommit.ts';
import type {
  TimelineApplyEdit,
  TimelineSelectedTrack,
} from '@/tools/video-editor/hooks/timeline-state-types.ts';
import {
  useClipAudioManagement,
  useClipDeletion,
  useClipPositioning,
  useClipSplitting,
  useClipTextOverlay,
} from './clip-editing/index.ts';
import type { ClipEditingContext } from './clip-editing/index.ts';
import type { DeleteClipOptions } from './clip-editing/types.ts';

export interface UseClipEditingArgs {
  dataRef: MutableRefObject<TimelineData | null>;
  resolvedConfig: TimelineData['resolvedConfig'] | null;
  selectedClipId: string | null;
  selectedTrack: TimelineSelectedTrack;
  currentTime: number;
  selectClip: (clipId: string, opts?: SelectClipOptions) => void;
  setSelectedTrackId: Dispatch<SetStateAction<string | null>>;
  applyEdit: TimelineApplyEdit;
}

export interface UseClipEditingResult {
  onOverlayChange: (actionId: string, patch: Partial<ClipMeta>) => void;
  handleUpdateClips: (clipIds: string[], patch: Partial<ClipMeta>) => void;
  handleUpdateClipsDeep: (clipIds: string[], patchFn: (existing: ClipMeta) => Partial<ClipMeta>) => void;
  handleDeleteClips: (clipIds: string[], options?: DeleteClipOptions) => void;
  handleDeleteClip: (clipId: string, options?: DeleteClipOptions) => void;
  handleSelectedClipChange: (patch: ClipEditorPatch) => void;
  handleResetClipPosition: () => void;
  handleResetClipsPosition: (clipIds: string[]) => void;
  handleSplitSelectedClip: () => void;
  handleSplitClipAtTime: (clipId: string, timeSeconds: number) => void;
  handleSplitClipsAtPlayhead: (clipIds: string[]) => void;
  handleToggleMuteClips: (clipIds: string[]) => void;
  handleToggleMute: () => void;
  handleDetachAudioClip: (clipId: string) => void;
  handleAddText: () => void;
  handleAddTextAt: (trackId: string, time: number) => void;
}

export { DURATION_KEYS, patchAffectsDuration, recalcActionEnd } from '@/tools/video-editor/lib/clip-editing-utils.ts';
export type { DeleteClipOptions } from './clip-editing/types.ts';

const PINNED_GROUP_EDIT_MESSAGE = 'Use Delete shot from the shot menu';

export function useClipEditing({
  dataRef,
  resolvedConfig,
  selectedClipId,
  selectedTrack,
  currentTime,
  selectClip,
  setSelectedTrackId,
  applyEdit,
}: UseClipEditingArgs): UseClipEditingResult {
  const currentTimeRef = useRef(currentTime);
  const elementHost = useOptionalVideoEditorRuntime()?.astridElementHost;

  const applyRowsEdit = useCallback((
    rows: TimelineData['rows'],
    metaUpdates?: Record<string, Partial<ClipMeta>>,
    metaDeletes?: string[],
    clipOrderOverride?: TimelineData['clipOrder'],
    options?: ApplyEditOptions,
  ) => {
    const mutation = {
      type: 'rows',
      rows,
      ...(metaUpdates ? { metaUpdates } : {}),
      ...(metaDeletes ? { metaDeletes } : {}),
      ...(clipOrderOverride ? { clipOrderOverride } : {}),
    } as const;

    if (options) {
      applyEdit(mutation, options);
      return;
    }

    applyEdit(mutation);
  }, [applyEdit]);

  const applyConfigEdit = useCallback((
    resolvedConfig: TimelineData['resolvedConfig'],
    options?: ApplyEditOptions,
  ) => {
    const mutation = {
      type: 'config',
      resolvedConfig,
    } as const;

    if (options) {
      applyEdit(mutation, options);
      return;
    }

    applyEdit(mutation);
  }, [applyEdit]);

  const isPinnedGroupMember = useCallback((clipId: string): boolean => {
    const current = dataRef.current;
    if (!current) {
      return false;
    }

    return findEnclosingPinnedGroup(current.config, clipId) !== null;
  }, [dataRef]);

  const notifyPinnedGroupEditBlocked = useCallback(() => {
    toast.error(PINNED_GROUP_EDIT_MESSAGE);
  }, []);

  useLayoutEffect(() => {
    currentTimeRef.current = currentTime;
  }, [currentTime]);

  const onOverlayChange = useCallback((actionId: string, patch: Partial<ClipMeta>) => {
    const current = dataRef.current;
    if (!current) {
      return;
    }

    applyRowsEdit(current.rows, { [actionId]: patch }, undefined, undefined, { editCommands: propertyGestureCommands(current, actionId, patch) });
  }, [applyRowsEdit, dataRef]);

  const getValidClipIds = useCallback((clipIds: string[]) => {
    const current = dataRef.current;
    if (!current) {
      return [];
    }

    const uniqueClipIds = new Set<string>();
    for (const clipId of clipIds) {
      if (clipId.startsWith('uploading-') || !current.meta[clipId]) {
        continue;
      }

      uniqueClipIds.add(clipId);
    }

    return [...uniqueClipIds];
  }, [dataRef]);

  const handleUpdateClips = useCallback((clipIds: string[], patch: Partial<ClipMeta>) => {
    const current = dataRef.current;
    if (!current) {
      return;
    }

    const validClipIds = getValidClipIds(clipIds);
    if (validClipIds.length === 0) {
      return;
    }

    const metaUpdates = Object.fromEntries(
      validClipIds.map((clipId) => [clipId, patch]),
    ) as Record<string, Partial<ClipMeta>>;

    const commandGroups = validClipIds.map((id) => {
      const continuous = continuousEffectGestureCommands(current, id, patch);
      return continuous.handled ? (validClipIds.length === clipIds.length ? continuous.commands : undefined) : propertyGestureCommands(current, id, patch);
    });
    const editCommands = continuousBatchGestureCommands(current, commandGroups);
    if (!patchAffectsDuration(patch)) {
      applyRowsEdit(current.rows, metaUpdates, undefined, undefined, { editCommands });
      return;
    }

    const validClipIdSet = new Set(validClipIds);
    const nextRows = current.rows.map((row) => ({
      ...row,
      actions: row.actions.map((action) => {
        if (!validClipIdSet.has(action.id)) {
          return action;
        }

        const existing = current.meta[action.id];
        if (!existing) {
          return action;
        }

        return {
          ...action,
          end: recalcActionEnd(action, { ...existing, ...patch }),
        };
      }),
    }));

    applyRowsEdit(nextRows, metaUpdates, undefined, undefined, { editCommands });
  }, [applyRowsEdit, dataRef, getValidClipIds]);

  const handleUpdateClipsDeep = useCallback((
    clipIds: string[],
    patchFn: (existing: ClipMeta) => Partial<ClipMeta>,
  ) => {
    const current = dataRef.current;
    if (!current) {
      return;
    }

    const validClipIds = getValidClipIds(clipIds);
    if (validClipIds.length === 0) {
      return;
    }

    const metaUpdates: Record<string, Partial<ClipMeta>> = {};

    for (const clipId of validClipIds) {
      const existing = current.meta[clipId];
      if (!existing) {
        continue;
      }

      metaUpdates[clipId] = patchFn(existing);
    }

    if (Object.keys(metaUpdates).length === 0) {
      return;
    }

    const groups = validClipIds.map(id => {
      const patch = metaUpdates[id];
      if (!patch) return undefined;
      const continuous = continuousEffectGestureCommands(current, id, patch);
      return continuous.handled ? (validClipIds.length === clipIds.length ? continuous.commands : undefined) : propertyGestureCommands(current, id, patch);
    });
    applyRowsEdit(current.rows, metaUpdates, undefined, undefined, {
      editCommands: continuousBatchGestureCommands(current, groups),
    });
  }, [applyRowsEdit, dataRef, getValidClipIds]);

  const handleSelectedClipChange = useCallback((patch: ClipEditorPatch) => {
    const current = dataRef.current;
    if (!current || !selectedClipId) {
      return;
    }

    const clipRow = current.rows.find((row) => row.actions.some((action) => action.id === selectedClipId));
    if (!clipRow) {
      return;
    }

    const { at: _at, ...metaPatch } = patch;
    const composite = compositeEffectGestureCommands(current, selectedClipId, metaPatch, { elementHost });
    if (composite.refused) return;
    const effectivePatch = composite.commands?.length && composite.localPatch ? composite.localPatch : metaPatch;
    const affectsDuration = patchAffectsDuration(effectivePatch as Partial<ClipMeta>);
    const nextRows = current.rows.map((row) => {
      if (row.id !== clipRow.id || (patch.at === undefined && !affectsDuration)) {
        return row;
      }

      return {
        ...row,
        actions: row.actions.map((action) => {
          if (action.id !== selectedClipId) {
            return action;
          }

          const nextStart = patch.at ?? action.start;
          const nextAction = {
            ...action,
            start: nextStart,
            end: patch.at === undefined
              ? action.end
              : nextStart + (action.end - action.start),
          };

          if (!affectsDuration) {
            return nextAction;
          }

          const merged = { ...current.meta[selectedClipId], ...effectivePatch };
          return {
            ...nextAction,
            end: recalcActionEnd(nextAction, merged),
          };
        }),
      };
    });

    const properties = composite.handled
      ? composite.commands
      : propertyGestureCommands(current, selectedClipId, metaPatch as Partial<ClipMeta>);
    const movement = patch.at === undefined ? [] : moveGestureCommands(current, selectedClipId, patch.at);
    applyRowsEdit(nextRows, { [selectedClipId]: effectivePatch as Partial<ClipMeta> }, undefined, undefined, {
      editCommands: properties && movement ? [...movement, ...properties] : undefined,
    });
  }, [applyRowsEdit, dataRef, elementHost, selectedClipId]);

  const clipEditingContext: ClipEditingContext = {
    dataRef,
    resolvedConfig,
    selectedClipId,
    selectedTrack,
    currentTimeRef,
    applyRowsEdit,
    applyConfigEdit,
    isPinnedGroupMember,
    notifyPinnedGroupEditBlocked,
    getValidClipIds,
    selectClip,
    setSelectedTrackId,
  };

  const clipDeletion = useClipDeletion(clipEditingContext);
  const clipPositioning = useClipPositioning(clipEditingContext);
  const clipSplitting = useClipSplitting(clipEditingContext);
  const clipAudioManagement = useClipAudioManagement(clipEditingContext);
  const clipTextOverlay = useClipTextOverlay(clipEditingContext);

  return {
    onOverlayChange,
    handleUpdateClips,
    handleUpdateClipsDeep,
    ...clipDeletion,
    handleSelectedClipChange,
    ...clipPositioning,
    ...clipSplitting,
    ...clipAudioManagement,
    ...clipTextOverlay,
  };
}
