import { useOptionalVideoEditorRuntime } from '@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx';
import { readGalleryGenerationSelection } from '@/tools/video-editor/commands/selectedProjectMedia.ts';
import { useCallback, useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from '@/shared/components/ui/runtime/sonner';
import type { GenerationRow } from '@/domains/generation/types';
import { getGenerationId } from '@/shared/lib/media/mediaTypeHelpers';
import { useToolSettings } from '@/shared/hooks/settings/useToolSettings';
import { getClipTimelineDuration } from '@/tools/video-editor';
import { videoEditorPathWithTimeline } from '@/tools/video-editor/lib/video-editor-path';
import { videoEditorSettings } from '@/tools/video-editor/settings/videoEditorDefaults';
import {
  getPlayableAssetKind,
  planGenerationAssetRegistration,
} from '@/tools/video-editor/lib/timeline-asset-plans';
import {
  hasMountedTimelineAvailability,
  useTimelineAvailabilityState,
  useTimelineEditorDataSafe,
  useTimelineEditorOpsSafe,
} from '@/tools/video-editor/hooks/timelineStore';
import { useTimelineCommandsServiceSafe } from '@/tools/video-editor/hooks/useTimelineCommandsService';
import {
  ADD_GENERATION_QUERY_PARAM,
  readPendingAdds,
  writePendingAdds,
  PENDING_ADDS_STORAGE_KEY,
} from './addToVideoEditorConstants';

export { ADD_GENERATION_QUERY_PARAM };

export type AddToVideoEditorPhase = 'idle' | 'staged';

interface UseAddToVideoEditorResult {
  onClick: () => void;
  phase: AddToVideoEditorPhase;
}

/**
 * Handler for adding the given media to the video editor timeline.
 *
 * Three branches:
 * 1. Editor is mounted (Timeline context available) → drop on the timeline immediately.
 * 2. Editor not mounted, first click → stage the generationId in localStorage and
 *    enter 'staged' phase (button shows a success state). No navigation.
 * 3. Editor not mounted, second click (already staged) → navigate to the editor;
 *    VideoEditorProvider drains the staged queue on mount.
 */
export function useAddToVideoEditor(media: GenerationRow | undefined): UseAddToVideoEditorResult {
  const runtime = useOptionalVideoEditorRuntime();
  const mountedRef = useRef(true);
  useEffect(() => { mountedRef.current = true; return () => { mountedRef.current = false; }; }, []);
  const ops = useTimelineEditorOpsSafe();
  const data = useTimelineEditorDataSafe();
  const commands = useTimelineCommandsServiceSafe();
  const availability = useTimelineAvailabilityState();
  const navigate = useNavigate();
  const { settings: videoSettings } = useToolSettings(videoEditorSettings.id);
  const hasMountedEditor = hasMountedTimelineAvailability(availability);

  const generationId = media ? (getGenerationId(media) ?? media.id) : null;

  const [phase, setPhase] = useState<AddToVideoEditorPhase>(() => {
    if (!generationId) return 'idle';
    return readPendingAdds().includes(generationId) ? 'staged' : 'idle';
  });

  useEffect(() => {
    if (!generationId) {
      setPhase('idle');
      return;
    }
    setPhase(readPendingAdds().includes(generationId) ? 'staged' : 'idle');
  }, [generationId]);

  useEffect(() => {
    const onStorage = (e: StorageEvent) => {
      if (e.key !== PENDING_ADDS_STORAGE_KEY) return;
      if (!generationId) return;
      setPhase(readPendingAdds().includes(generationId) ? 'staged' : 'idle');
    };
    window.addEventListener('storage', onStorage);
    return () => window.removeEventListener('storage', onStorage);
  }, [generationId]);

  const onClick = useCallback(async () => {
    if (!media || !generationId) return;

    const hasMountedCommandSurface = hasMountedEditor
      && commands !== null
      && ops !== null
      && data !== null;

    if (hasMountedCommandSurface && commands && ops && data) {
      // Resolve identity before registration; URLs and generation labels are
      // not authority for a semantic media command. Capture this mounted base
      // across the asynchronous selection so it cannot move to another film.
      const captured = JSON.stringify({ config: data.dataRef.current?.config, head: data.dataRef.current?.head });
      const selection = runtime?.provider?.semanticCommandSaving
        ? media.media_id && media.primary_variant_id && runtime.project.projectId
          ? await readGalleryGenerationSelection(runtime.provider, { projectId: runtime.project.projectId,
            asset: media.media_id, generationId, variantId: media.primary_variant_id }) : null
        : undefined;
      if (!mountedRef.current || selection === null || runtime?.provider?.semanticCommandSaving && !selection
        || captured !== JSON.stringify({ config: data.dataRef.current?.config, head: data.dataRef.current?.head })) {
        toast.error('Could not resolve the registered project media selection');
        return;
      }
      const registrationPlan = planGenerationAssetRegistration({
        ...(selection ? { assetId: selection.asset, variantId: selection.variant_id } : {}),
        generationId,
        mediaId: media.media_id,
        variantType: media.type === 'video' ? 'video' : 'image',
        imageUrl: media.location ?? media.imageUrl ?? '',
        thumbUrl: media.thumbUrl ?? media.imageUrl ?? media.location ?? '',
      });
      if (!registrationPlan.ok) {
        toast.error('Could not register asset');
        return;
      }

      const mediaType = getPlayableAssetKind(registrationPlan.assetEntry);
      if (!mediaType) {
        toast.error('Could not determine the asset media type');
        return;
      }

      const clips = data.resolvedConfig?.clips ?? [];
      const timelineEnd = clips.reduce(
        (max, clip) => Math.max(max, clip.at + getClipTimelineDuration(clip)),
        0,
      );
      const insertResult = commands.addClip({
        preparedAsset: {
          assetKey: registrationPlan.assetId,
          mediaType,
          durationSeconds: registrationPlan.assetEntry.duration ?? null,
          entry: registrationPlan.assetEntry,
          source: 'registered',
          ...(selection ? { selectedMedia: selection } : {}),
        },
        time: timelineEnd,
      });
      if (!insertResult.ok) {
        toast.error(insertResult.error.message);
      }
      return;
    }

    if (phase === 'staged') {
      const basePath = videoEditorPathWithTimeline(videoSettings?.lastTimelineId);
      const separator = basePath.includes('?') ? '&' : '?';
      navigate(`${basePath}${separator}${ADD_GENERATION_QUERY_PARAM}=${encodeURIComponent(generationId)}`);
      return;
    }

    const current = readPendingAdds();
    if (!current.includes(generationId)) {
      writePendingAdds([...current, generationId]);
    }
    setPhase('staged');
  }, [runtime, commands, data, generationId, hasMountedEditor, media, navigate, ops, phase, videoSettings?.lastTimelineId]);

  return { onClick, phase };
}
