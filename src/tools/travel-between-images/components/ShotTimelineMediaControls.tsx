import { useEffect, useRef, useState } from 'react';
import { Button } from '@/shared/components/ui/button.tsx';
import { useOptionalVideoEditorRuntime, useVideoEditorRuntime } from '@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx';
import { useAssetManagement } from '@/tools/video-editor/hooks/useAssetManagement.ts';
import { useTimelineCommandsService } from '@/tools/video-editor/hooks/useTimelineCommandsService.ts';
import {
  useTimelineChromeContext,
  useTimelineEditorData,
  useTimelineEditorOps,
  useTimelinePlaybackContext,
} from '@/tools/video-editor/hooks/timelineStore.ts';
import type { DataProvider } from '@/tools/video-editor/data/DataProvider.ts';
import type { TimelineDataRef } from '@/tools/video-editor/hooks/timeline-state-types.ts';
import type { TimelineData } from '@/tools/video-editor/lib/timeline-data.ts';
import type { JSON, MediaSelection } from '@/integrations/runtime/timeline-commit-types.ts';
import type { OccurrenceMediaCapturePort, OccurrenceMediaRequest } from '@/tools/video-editor/commands/occurrenceMediaGesture.ts';
import { captureOccurrenceMediaEdit, submitOccurrenceMediaEdit } from '@/tools/video-editor/commands/occurrenceMediaGesture.ts';
import type { TimelineClip } from '@/tools/video-editor/types/index.ts';

type Props = {
  occurrenceId: string;
  occurrenceMediaPort?: OccurrenceMediaCapturePort;
  mediaSelectionReader?: Pick<DataProvider, 'getProjectMediaSelection' | 'getProjectVerifiedMedia'>;
  mediaImportProvider?: Pick<DataProvider, 'prepareMediaImport'>;
  hostTimelineDataRef?: TimelineDataRef;
};

type Target = {
  parentData: TimelineData | null;
  saveStatus: string;
  trackId: string;
  time: number;
  replaceClip?: TimelineClip;
};

function reservedChildId(): string {
  const random = globalThis.crypto?.randomUUID?.() ?? `${Date.now()}-${Math.random().toString(36).slice(2)}`;
  return `popup-child-${random}`;
}

function asRecord(value: unknown): Record<string, unknown> | null {
  return value !== null && typeof value === 'object' && !Array.isArray(value)
    ? value as Record<string, unknown>
    : null;
}

function canonicalIdentity(clip: TimelineClip): Record<string, unknown> | null {
  return asRecord(asRecord(clip.app)?.canonical);
}

function mediaRow(
  selection: MediaSelection,
  mediaType: 'image' | 'video',
  track: string,
  at: number,
  duration: number,
): Record<string, JSON> {
  const row: Record<string, JSON> = {
    id: reservedChildId(),
    clipType: mediaType,
    track,
    at,
    asset: selection.asset,
    hold: duration,
  };
  if (mediaType === 'video') {
    row.from = 0;
    row.to = duration;
    row.speed = 1;
  }
  return row;
}

/**
 * Popup ADD/SWAP controls. The parent editor installs the native branch only
 * for a canonical occurrence caller; all other popup callers retain the
 * existing prepared-media writer.
 */
export function ShotTimelineMediaControls(props: Props) {
  if (!useOptionalVideoEditorRuntime()) return null;
  return <ShotTimelineMediaControlsInner {...props} />;
}

function ShotTimelineMediaControlsInner({ occurrenceId, occurrenceMediaPort, mediaSelectionReader, mediaImportProvider, hostTimelineDataRef }: Props) {
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
  useEffect(() => { mounted.current = true; return () => { mounted.current = false; }; }, []);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const visualTracks = editor.resolvedConfig?.tracks.filter(track => track.kind === 'visual' && track.role !== 'source') ?? [];
  const trackId = visualTracks.find(track => track.id === editor.selectedTrackId)?.id ?? visualTracks[0]?.id;
  const selectedClip = editor.selectedClipIds.size === 1
    ? editor.resolvedConfig?.clips.find(clip => editor.selectedClipIds.has(clip.id))
    : undefined;
  const canSwap = Boolean(selectedClip?.asset && selectedClip?.clipType !== 'effect-layer'
    && visualTracks.some(track => track.id === selectedClip?.track));
  const legacySupported = runtime.provider.preparedMediaPlacementEnabled === true
    && Boolean(runtime.provider.prepareMediaImport && runtime.provider.getProjectMediaSelection);
  const nativeSupported = Boolean(occurrenceMediaPort && mediaSelectionReader?.getProjectMediaSelection
    && mediaImportProvider?.prepareMediaImport && hostTimelineDataRef);
  const editable = runtime.timelineEditability?.checkTimeline?.().allowed !== false;
  const targetRef = useRef<Target | null>(null);

  const choose = (swap: boolean) => {
    setError(null);
    try {
      if (!editable || !trackId || !editor.dataRef.current || (swap && !canSwap)) return;
      targetRef.current = {
        parentData: hostTimelineDataRef?.current,
        saveStatus,
        trackId: swap ? selectedClip!.track : trackId,
        time: currentTime,
        ...(swap ? { replaceClip: selectedClip } : {}),
      } as Target;
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
      const uploaded = mediaImportProvider?.prepareMediaImport
        ? (() => mediaImportProvider.prepareMediaImport!(file, { filename: file.name, mediaType: file.type }))()
        : file.type.startsWith('image/')
          ? assets.uploadImageGeneration(file)
          : assets.uploadVideoGeneration(file);
      const imported = await uploaded;
      const uploadedGeneration = 'mediaImport' in imported
        ? imported
        : {
          generationId: imported.generationId,
          variantId: imported.variantId,
          variantType: file.type.startsWith('video/') ? 'video' as const : 'image' as const,
          durationSeconds: imported.entry.duration,
          imageUrl: imported.entry.file ?? imported.assetId,
          metadata: { content_type: file.type, original_filename: file.name },
          mediaImport: imported,
        };
      if (!mounted.current) return;
      const parentData = hostTimelineDataRef?.current;
      if (parentData !== target.parentData || saveStatusRef.current !== target.saveStatus) {
        throw new Error('The shot changed while choosing media. Choose the target again.');
      }
      const preparedAsset = assets.prepareGenerationAsset(uploadedGeneration);
      if (!preparedAsset) throw new Error('Could not resolve the registered project media.');

      if (nativeSupported && occurrenceMediaPort && mediaSelectionReader?.getProjectMediaSelection && parentData) {
        if (!uploadedGeneration.mediaImport) throw new Error('Runtime media import did not return an immutable selection basis.');
        const selection = await mediaSelectionReader.getProjectMediaSelection({
          asset: uploadedGeneration.mediaImport.assetId,
          generation_id: uploadedGeneration.generationId,
          variant_id: uploadedGeneration.mediaImport.variantId,
        });
        const ownerRef = `occurrence:${occurrenceId}` as `occurrence:${string}`;
        const trackRef = `${ownerRef}/track:${target.trackId}` as `occurrence:${string}/track:${string}`;
        const duration = Math.max(0.001, preparedAsset.durationSeconds ?? uploadedGeneration.durationSeconds ?? 5);
        let request: OccurrenceMediaRequest;
        if (target.replaceClip) {
            const identity = canonicalIdentity(target.replaceClip);
            if (identity?.occurrenceId !== occurrenceId || identity.ownerRef !== ownerRef
              || typeof identity.clipRef !== 'string' || typeof identity.rawClipId !== 'string'
              || identity.clipRef !== `${ownerRef}/clip:${identity.rawClipId}`) {
              throw new Error('The selected popup clip has no unambiguous canonical occurrence binding.');
            }
            const oldEntry = parentData.registry.assets[target.replaceClip.asset ?? ''];
            if (!oldEntry?.generationId || !oldEntry.variantId) {
              throw new Error('The selected clip has no immutable media selection to swap.');
            }
            const oldMedia = await mediaSelectionReader.getProjectMediaSelection({
              asset: target.replaceClip.asset!,
              generation_id: oldEntry.generationId,
              variant_id: oldEntry.variantId,
            });
            request = {
              kind: 'swap',
              ownerRef,
              trackRef,
              clipRef: identity.clipRef as `occurrence:${string}/clip:${string}`,
              oldMedia,
              media: selection,
            };
        } else {
          request = {
            kind: 'add',
            ownerRef,
            trackRef,
            media: selection,
            row: mediaRow(selection, file.type.startsWith('video/') ? 'video' : 'image', target.trackId, target.time, duration),
          };
        }
        const captured = captureOccurrenceMediaEdit(occurrenceMediaPort, parentData, request);
        await submitOccurrenceMediaEdit(captured);
      } else {
        const result = commands.addClip({ preparedAsset, trackId: target.trackId,
          ...(target.replaceClip ? { replaceClipId: target.replaceClip.id } : { time: target.time }) });
        if (!result.ok) throw new Error(result.error.message);
      }
    } catch (cause) {
      if (mounted.current) setError(cause instanceof Error ? cause.message : 'Could not place shot media.');
    } finally {
      if (mounted.current) setBusy(false);
    }
  };

  const supported = nativeSupported || legacySupported;
  return <div className="space-y-1" data-shot-timeline-media-controls="true">
    <div className="flex flex-wrap items-center gap-2">
      <Button type="button" size="sm" variant="outline" disabled={!supported || !editable || busy || !trackId} onClick={() => choose(false)}>Add media</Button>
      <Button type="button" size="sm" variant="outline" disabled={!supported || !editable || busy || !canSwap} onClick={() => choose(true)}>Swap selected clip</Button>
      <span className="text-xs text-muted-foreground">{busy ? 'Importing media…' : canSwap ? `Selected clip: ${selectedClip!.id}` : `Add at ${currentTime.toFixed(2)}s on ${trackId ?? 'a visual track'}; select one media clip to swap.`}</span>
      <input ref={inputRef} type="file" accept="image/*,video/*" className="hidden" aria-label="Choose media for shot timeline" disabled={!supported || !editable || busy} onChange={event => {
        const file = event.currentTarget.files?.[0]; event.currentTarget.value = '';
        if (file) void importFile(file);
      }} />
    </div>
    {!supported ? <p className="text-xs text-muted-foreground">This provider does not support shot media Add or swap.</p> : null}
    {error ? <p role="alert" className="text-xs text-destructive">{error}</p> : null}
  </div>;
}

