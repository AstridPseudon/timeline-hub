import { useEffect, useRef, useState } from 'react';
import { Button } from '@/shared/components/ui/button.tsx';
import { useVideoEditorRuntime } from '@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx';
import { useAssetManagement } from '@/tools/video-editor/hooks/useAssetManagement.ts';
import { useTimelineCommandsService } from '@/tools/video-editor/hooks/useTimelineCommandsService.ts';
import {
  useTimelineChromeContext,
  useTimelineEditorData,
  useTimelineEditorOps,
  useTimelinePlaybackContext,
} from '@/tools/video-editor/hooks/timelineStore.ts';

type ShotTimelineMediaControlsProps = {
  occurrenceId: string;
  parentDocumentId: string;
};

/** File selection uses Runtime import and the mounted editor's A2 command route. */
export function ShotTimelineMediaControls({
  occurrenceId,
  parentDocumentId,
}: ShotTimelineMediaControlsProps) {
  const runtime = useVideoEditorRuntime();
  const editor = useTimelineEditorData();
  const { saveStatus } = useTimelineChromeContext();
  const saveStatusRef = useRef(saveStatus);
  saveStatusRef.current = saveStatus;
  const ops = useTimelineEditorOps();
  const { currentTime } = useTimelinePlaybackContext();
  const commands = useTimelineCommandsService();
  const assets = useAssetManagement({
    dataRef: editor.dataRef,
    selectedTrackId: editor.selectedTrackId,
    selectedProjectId: runtime.project.projectId,
    selectClip: ops.selectClip,
    setSelectedTrackId: ops.setSelectedTrackId,
    applyEdit: ops.applyEdit,
    patchRegistry: ops.patchRegistry,
    invalidateAssetRegistry: async () => {},
    resolveAssetUrl: async file => runtime.assetResolver.resolveAssetUrl(file),
  });
  const inputRef = useRef<HTMLInputElement>(null);
  const mounted = useRef(true);
  useEffect(() => {
    mounted.current = true;
    return () => { mounted.current = false; };
  }, []);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const visualTracks = editor.resolvedConfig?.tracks.filter(track => track.kind === 'visual' && track.role !== 'source') ?? [];
  const trackId = visualTracks.find(track => track.id === editor.selectedTrackId)?.id ?? visualTracks[0]?.id;
  const selectedClip = editor.selectedClipIds.size === 1
    ? editor.resolvedConfig?.clips.find(clip => editor.selectedClipIds.has(clip.id))
    : undefined;
  const canSwap = Boolean(selectedClip?.asset)
    && !['text', 'hold', 'effect-layer'].includes(selectedClip?.clipType ?? '')
    && visualTracks.some(track => track.id === selectedClip?.track);
  const supported = Boolean(runtime.provider.prepareMediaImport);
  const editable = runtime.timelineEditability?.checkTimeline?.().allowed !== false;
  type Target = {
    data: typeof editor.data;
    saveStatus: typeof saveStatus;
    projectId: string;
    timelineId: string;
    occurrenceId: string;
    parentDocumentId: string;
    trackId: string;
    time: number;
    replaceClipId?: string;
  };
  const targetRef = useRef<Target | null>(null);

  const choose = (swap: boolean) => {
    setError(null);
    try {
      if (!supported || !editable || !trackId || !editor.dataRef.current || (swap && !canSwap)) return;
      // Capture the mounted document and physical occurrence before any async import.
      targetRef.current = {
        data: editor.dataRef.current,
        saveStatus,
        projectId: runtime.project.projectId,
        timelineId: runtime.timelineId,
        occurrenceId,
        parentDocumentId,
        trackId: swap ? selectedClip!.track : trackId,
        time: currentTime,
        ...(swap ? { replaceClipId: selectedClip!.id } : {}),
      };
      inputRef.current?.click();
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'The shot media target is unavailable.');
    }
  };

  const importFile = async (file: File) => {
    const target = targetRef.current;
    targetRef.current = null;
    if (!target || busy) return;
    setBusy(true);
    try {
      if (!file.type.startsWith('image/') && !file.type.startsWith('video/')) {
        throw new Error('Choose an image or video file.');
      }
      const uploaded = file.type.startsWith('image/')
        ? await assets.uploadImageGeneration(file)
        : await assets.uploadVideoGeneration(file);
      if (!mounted.current) return;
      if (editor.dataRef.current !== target.data
        || saveStatusRef.current !== target.saveStatus
        || runtime.project.projectId !== target.projectId
        || runtime.timelineId !== target.timelineId
        || occurrenceId !== target.occurrenceId
        || parentDocumentId !== target.parentDocumentId) {
        throw new Error('The shot changed while choosing media. Choose the target again.');
      }
      const preparedAsset = assets.prepareGenerationAsset(uploaded);
      if (!preparedAsset) throw new Error('Could not resolve the registered project media selection.');
      const result = commands.addClip({
        preparedAsset,
        trackId: target.trackId,
        ...(target.replaceClipId ? { replaceClipId: target.replaceClipId } : { time: target.time }),
      });
      if (!result.ok) throw new Error(result.error.message);
    } catch (cause) {
      if (mounted.current) setError(cause instanceof Error ? cause.message : 'Could not place shot media.');
    } finally {
      if (mounted.current) setBusy(false);
    }
  };

  return <div className="space-y-1" data-shot-timeline-media-controls="true">
    <div className="flex flex-wrap items-center gap-2">
      <Button type="button" size="sm" variant="outline" disabled={!supported || !editable || busy || !trackId} onClick={() => choose(false)}>
        Add media
      </Button>
      <Button type="button" size="sm" variant="outline" disabled={!supported || !editable || busy || !canSwap} onClick={() => choose(true)}>
        Swap selected clip
      </Button>
      <span className="text-xs text-muted-foreground">
        {busy ? 'Importing media…' : canSwap ? `Selected clip: ${selectedClip!.id}` : `Add at ${currentTime.toFixed(2)}s on ${trackId ?? 'a visual track'}; select one media clip to swap.`}
      </span>
      <input
        ref={inputRef}
        type="file"
        accept="image/*,video/*"
        className="hidden"
        aria-label="Choose media for shot timeline"
        disabled={!supported || !editable || busy}
        onChange={event => {
          const file = event.currentTarget.files?.[0];
          event.currentTarget.value = '';
          if (file) void importFile(file);
        }}
      />
    </div>
    {!supported ? <p className="text-xs text-muted-foreground">This provider does not support shot media Add or swap.</p> : null}
    {error ? <p role="alert" className="text-xs text-destructive">{error}</p> : null}
  </div>;
}
