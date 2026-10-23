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

type ClipSelectionSnapshot = {
  id: string;
  track: string;
  at: number;
  asset?: string;
  ownerRef?: string;
  clipRef?: string;
};

type SelectionSnapshot = {
  selectedIds: string[];
  selectedTrackId: string | null;
  clip: ClipSelectionSnapshot | null;
};

function clipSelectionSnapshot(
  selectedIds: ReadonlySet<string>,
  selectedTrackId: string | null,
  clip: { id: string; track: string; at: number; asset?: string; app?: Record<string, unknown> } | undefined,
): SelectionSnapshot {
  const canonical = clip?.app?.canonical;
  const identity = canonical && typeof canonical === 'object' && !Array.isArray(canonical)
    ? canonical as Record<string, unknown>
    : undefined;
  return {
    selectedIds: [...selectedIds].sort(),
    selectedTrackId,
    clip: clip
      ? {
          id: clip.id,
          track: clip.track,
          at: clip.at,
          ...(clip.asset !== undefined ? { asset: clip.asset } : {}),
          ...(typeof identity?.ownerRef === 'string' ? { ownerRef: identity.ownerRef } : {}),
          ...(typeof identity?.clipRef === 'string' ? { clipRef: identity.clipRef } : {}),
        }
      : null,
  };
}

function sameSelection(left: SelectionSnapshot, right: SelectionSnapshot): boolean {
  if (left.selectedTrackId !== right.selectedTrackId
    || left.selectedIds.length !== right.selectedIds.length
    || left.selectedIds.some((id, index) => id !== right.selectedIds[index])) {
    return false;
  }
  if (left.clip === null || right.clip === null) return left.clip === right.clip;
  return left.clip.id === right.clip.id
    && left.clip.track === right.clip.track
    && left.clip.at === right.clip.at
    && left.clip.asset === right.clip.asset
    && left.clip.ownerRef === right.clip.ownerRef
    && left.clip.clipRef === right.clip.clipRef;
}

function validatedProjectId(projectId: string | null): string | null {
  return typeof projectId === 'string' && projectId.trim().length > 0 ? projectId : null;
}

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
  const editorRef = useRef(editor);
  editorRef.current = editor;
  const runtimeRef = useRef(runtime);
  runtimeRef.current = runtime;
  const contextRef = useRef({ occurrenceId, parentDocumentId });
  contextRef.current = { occurrenceId, parentDocumentId };
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
  const assetsRef = useRef(assets);
  assetsRef.current = assets;
  const commandsRef = useRef(commands);
  commandsRef.current = commands;
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
  const projectId = validatedProjectId(runtime.project.projectId);
  const displayTime = typeof currentTime === 'number' && Number.isFinite(currentTime)
    ? `${currentTime.toFixed(2)}s`
    : 'an available time';
  type Target = {
    data: NonNullable<typeof editor.dataRef.current>;
    saveStatus: typeof saveStatus;
    projectId: string;
    timelineId: string;
    occurrenceId: string;
    parentDocumentId: string;
    trackId: string;
    time: number;
    selection: SelectionSnapshot;
    replaceClipId?: string;
  };
  const targetRef = useRef<Target | null>(null);

  const choose = (swap: boolean) => {
    setError(null);
    try {
      const currentProjectId = validatedProjectId(runtime.project.projectId);
      const data = editor.dataRef.current;
      const selection = clipSelectionSnapshot(editor.selectedClipIds, editor.selectedTrackId, selectedClip);
      const time = swap ? selectedClip?.at : currentTime;
      if (!supported || !editable || !trackId || !data || (swap && !canSwap)) return;
      if (!currentProjectId) {
        setError('The current project scope is unavailable. Choose the target again.');
        return;
      }
      if (data.head?.projectId !== undefined && data.head.projectId !== currentProjectId) {
        setError('The current project scope does not match this shot. Choose the target again.');
        return;
      }
      if (typeof time !== 'number' || !Number.isFinite(time)) {
        setError('The current media placement time is unavailable. Choose the target again.');
        return;
      }
      // Capture the mounted document and physical occurrence before any async import.
      targetRef.current = {
        data,
        saveStatus,
        projectId: currentProjectId,
        timelineId: runtime.timelineId,
        occurrenceId,
        parentDocumentId,
        trackId: swap ? selectedClip!.track : trackId,
        time,
        selection,
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
      const currentEditor = editorRef.current;
      const currentRuntime = runtimeRef.current;
      const currentData = currentEditor.dataRef.current;
      const currentConfig = currentData?.resolvedConfig ?? currentEditor.resolvedConfig;
      const currentSelectedClip = currentEditor.selectedClipIds.size === 1
        ? currentConfig?.clips.find(clip => currentEditor.selectedClipIds.has(clip.id))
        : undefined;
      const currentSelection = clipSelectionSnapshot(
        currentEditor.selectedClipIds,
        currentEditor.selectedTrackId,
        currentSelectedClip,
      );
      const currentProjectId = validatedProjectId(currentRuntime.project.projectId);
      const currentHead = currentData?.head;
      const dataStillCurrent = currentData === target.data
        && currentData.configVersion === target.data.configVersion
        && currentData.signature === target.data.signature
        && currentData.stableSignature === target.data.stableSignature
        && currentHead?.projectId === target.data.head?.projectId
        && currentHead?.headRevisionId === target.data.head?.headRevisionId
        && currentHead?.headPublicationId === target.data.head?.headPublicationId;
      const editabilityStillCurrent = currentRuntime.timelineEditability?.checkTimeline?.().allowed !== false;
      if (!dataStillCurrent
        || saveStatusRef.current !== target.saveStatus
        || currentProjectId !== target.projectId
        || currentRuntime.timelineId !== target.timelineId
        || contextRef.current.occurrenceId !== target.occurrenceId
        || contextRef.current.parentDocumentId !== target.parentDocumentId
        || !sameSelection(currentSelection, target.selection)
        || !editabilityStillCurrent
        || (currentData?.head?.projectId !== undefined && currentData.head.projectId !== target.projectId)) {
        throw new Error('The shot changed while choosing media. Choose the target again.');
      }
      const preparedAsset = assetsRef.current.prepareGenerationAsset(uploaded);
      if (!preparedAsset) throw new Error('Could not resolve the registered project media selection.');
      const result = commandsRef.current.addClip({
        preparedAsset,
        trackId: target.trackId,
        time: target.time,
        ...(target.replaceClipId ? { replaceClipId: target.replaceClipId } : {}),
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
      <Button type="button" size="sm" variant="outline" disabled={!supported || !editable || !projectId || busy || !trackId} onClick={() => choose(false)}>
        Add media
      </Button>
      <Button type="button" size="sm" variant="outline" disabled={!supported || !editable || !projectId || busy || !canSwap} onClick={() => choose(true)}>
        Swap selected clip
      </Button>
      <span className="text-xs text-muted-foreground">
        {busy ? 'Importing media…' : canSwap ? `Selected clip: ${selectedClip!.id}` : `Add at ${displayTime} on ${trackId ?? 'a visual track'}; select one media clip to swap.`}
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
