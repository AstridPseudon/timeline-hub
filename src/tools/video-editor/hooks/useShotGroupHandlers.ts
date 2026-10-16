import { useCallback, useMemo } from 'react';
import type { Shot } from '@/domains/generation/types/index.ts';
import { buildDeleteShotGroupMutation } from '@/tools/video-editor/lib/shot-group-commands.ts';
import type { TimelineApplyEdit, TimelineDataRef } from '@/tools/video-editor/hooks/timeline-state-types.ts';
import type { ShotFinalVideo } from '@/tools/video-editor/hooks/useFinalVideoAvailable.ts';
import { shotGroupVideoKey, type ShotGroup } from '@/tools/video-editor/hooks/useShotGroups.ts';
import { buildDeleteShotGroupCommand } from '@/tools/video-editor/commands/shotGroupCommands.ts';
import type { CanonicalShotOccurrence } from '@/tools/video-editor/data/shotCompositionAdapter.ts';
import type { ResolvedAssetRegistryEntry, PinnedShotGroup } from '@/tools/video-editor/types/index.ts';
import type { TimelineRow } from '@/tools/video-editor/types/timeline-canvas.ts';

interface UseShotGroupHandlersArgs {
  shots: Shot[] | undefined;
  shotGroups: ShotGroup[];
  data: {
    rows: TimelineRow[];
    meta: Record<string, { asset?: string; track?: string }>;
    config: { pinnedShotGroups?: PinnedShotGroup[] };
  } | null;
  resolvedRegistry: Record<string, ResolvedAssetRegistryEntry> | undefined;
  activeTaskAssetKeys: Set<string>;
  finalVideoMap: Map<string, ShotFinalVideo>;
  applyEdit: TimelineApplyEdit;
  dataRef: TimelineDataRef;
  dismissFinalVideo: (finalVideoId: string) => void;
  switchToFinalVideo: (group: { shotId: string; clipIds: string[]; rowId: string; canonicalIdentity?: CanonicalShotOccurrence }) => void;
  switchToImages: (group: { shotId: string; rowId: string }) => void;
  updateToLatestVideo: (group: { shotId: string; rowId: string; canonicalIdentity?: CanonicalShotOccurrence }) => void;
  unpinGroup: (shotId: string, trackId: string) => void;
  setVideoModalShot: (shot: Shot | null) => void;
  setVideoModalShowImages: (show: boolean) => void;
  semanticCommands?: boolean;
}

export function useShotGroupHandlers({
  shots,
  shotGroups,
  data,
  resolvedRegistry,
  activeTaskAssetKeys,
  finalVideoMap,
  applyEdit,
  dataRef,
  dismissFinalVideo,
  switchToFinalVideo,
  switchToImages,
  updateToLatestVideo,
  unpinGroup,
  setVideoModalShot,
  setVideoModalShowImages,
  semanticCommands = false,
}: UseShotGroupHandlersArgs) {
  const shotGroupClipIds = useMemo(() => {
    const ids = new Set<string>();
    for (const group of shotGroups) {
      for (const clipId of group.clipIds) {
        ids.add(clipId);
      }
    }
    return ids;
  }, [shotGroups]);

  const activeTaskClipIds = useMemo(() => {
    if (activeTaskAssetKeys.size === 0 || !data?.rows || !data?.meta) return new Set<string>();
    const clipIds = new Set<string>();
    for (const row of data.rows) {
      for (const action of row.actions) {
        const assetKey = data.meta[action.id]?.asset;
        if (assetKey && activeTaskAssetKeys.has(assetKey)) {
          clipIds.add(action.id);
        }
      }
    }
    return clipIds;
  }, [activeTaskAssetKeys, data?.rows, data?.meta]);

  const staleShotGroupIds = useMemo(() => {
    const pinnedShotGroups = data?.config.pinnedShotGroups ?? [];
    const registry = resolvedRegistry;
    if (pinnedShotGroups.length === 0 || !registry) {
      return new Set<string>();
    }

    const staleIds = new Set<string>();
    for (const group of pinnedShotGroups) {
      if (group.mode !== 'video' || !group.videoAssetKey) {
        continue;
      }

      const currentGenerationId = registry[group.videoAssetKey]?.generationId;
      const latestFinalVideoId = finalVideoMap.get(shotGroupVideoKey(group))?.id;
      if (!currentGenerationId || !latestFinalVideoId) {
        continue;
      }

      if (currentGenerationId !== latestFinalVideoId) {
        staleIds.add(`${group.shotId}:${group.trackId}`);
      }
    }

    return staleIds;
  }, [data?.config.pinnedShotGroups, finalVideoMap, resolvedRegistry]);

  const handleShotGroupNavigate = useCallback((shotId: string) => {
    const shot = shots?.find((s) => s.id === shotId);
    if (shot) {
      setVideoModalShowImages(true);
      setVideoModalShot(shot);
    }
  }, [shots, setVideoModalShot, setVideoModalShowImages]);

  const handleShotGroupGenerateVideo = useCallback((shotId: string) => {
    const shot = shots?.find((s) => s.id === shotId);
    if (shot) setVideoModalShot(shot);
  }, [shots, setVideoModalShot]);

  const handleDeleteShotGroup = useCallback((group: { shotId: string; trackId: string; clipIds: string[] }) => {
    if (semanticCommands) {
      const command = buildDeleteShotGroupCommand(dataRef.current, group);
      if (command) applyEdit({ type: 'commands' }, { editCommands: [command], semantic: true });
      return;
    }
    const mutation = buildDeleteShotGroupMutation({
      currentData: dataRef.current,
      group,
    });
    if (!mutation) {
      return;
    }

    applyEdit(mutation, { semantic: true });
  }, [applyEdit, dataRef, semanticCommands]);

  const handleUpdateToLatestVideo = useCallback((group: { shotId: string; rowId: string; canonicalIdentity?: CanonicalShotOccurrence }) => {
    const finalVideo = finalVideoMap.get(shotGroupVideoKey(group));
    if (finalVideo && !semanticCommands) {
      dismissFinalVideo(finalVideo.id);
    }
    updateToLatestVideo(group);
  }, [dismissFinalVideo, finalVideoMap, semanticCommands, updateToLatestVideo]);

  const handleShotGroupUnpin = useCallback((group: { shotId: string; trackId: string }) => {
    unpinGroup(group.shotId, group.trackId);
  }, [unpinGroup]);

  const handleShotGroupSwitchToFinalVideo = useCallback((group: { shotId: string; clipIds: string[]; rowId: string; canonicalIdentity?: CanonicalShotOccurrence }) => {
    const finalVideo = finalVideoMap.get(shotGroupVideoKey(group));
    if (finalVideo && !semanticCommands) {
      dismissFinalVideo(finalVideo.id);
    }
    switchToFinalVideo(group);
  }, [dismissFinalVideo, finalVideoMap, semanticCommands, switchToFinalVideo]);

  const handleShotGroupSwitchToImages = useCallback((group: { shotId: string; rowId: string }) => {
    switchToImages(group);
  }, [switchToImages]);

  return {
    shotGroupClipIds,
    activeTaskClipIds,
    staleShotGroupIds,
    handleShotGroupNavigate,
    handleShotGroupGenerateVideo,
    handleDeleteShotGroup,
    handleUpdateToLatestVideo,
    handleShotGroupUnpin,
    handleShotGroupSwitchToFinalVideo,
    handleShotGroupSwitchToImages,
  };
}
