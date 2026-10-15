import { memo, useMemo } from 'react';
import AssetPanel from '@/tools/video-editor/components/PropertiesPanel/AssetPanel.tsx';
import {
  useTimelineEditorData,
  useTimelineEditorOps,
  useTimelineStoreApiSafe,
} from '@/tools/video-editor/hooks/timelineStore.ts';
import {
  useVideoEditorAssetPanels,
  useVideoEditorPanelRegistry,
} from '@/tools/video-editor/runtime/useVideoEditorRenderContext.ts';
import { useOptionalVideoEditorRuntime } from '@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx';
import type { ContributionErrorInfo } from '@/tools/video-editor/runtime/ContributionErrorBoundary.tsx';
import { findContributionOwnerId } from '@/tools/video-editor/runtime/extensionSurface.ts';
import { ExtensionPanelHost, getPanelKey } from '@/tools/video-editor/runtime/ExtensionPanelHost';
import { bindTranscriptPanelVideo } from '@/tools/video-editor/lib/transcript-panel-binding.ts';
import type { PanelVideoAdapter } from '@reigh/editor-sdk';

export interface VideoEditorAssetPanelSurfaceProps {
  includeBuiltIn?: boolean;
  /** Controlled visibility seam; selection UI/preferences belong to the shell. */
  activePanelKey?: string | null;
  video?: PanelVideoAdapter;
}

function VideoEditorAssetPanelSurfaceComponent({
  includeBuiltIn = true,
  activePanelKey,
  video,
}: VideoEditorAssetPanelSurfaceProps) {
  const runtime = useOptionalVideoEditorRuntime();
  const store = useTimelineStoreApiSafe();
  const view = runtime?.timelineViewStore;
  const panelVideo = useMemo(() => {
    const base = video ?? (store && view ? {
      view,
      seek: (seconds: number) => { store.getState().ops.onClickTimeArea(seconds); },
    } : undefined);
    return base && store ? bindTranscriptPanelVideo(store, base) : base;
  }, [video, store, view]);
  const contributionIndex = runtime?.extensionRuntime?.contributionIndex;
  const assetPanels = useVideoEditorAssetPanels();
  const panelRegistry = useVideoEditorPanelRegistry();
  const panels = panelRegistry.panels
    .filter((panel) => typeof panel.render === 'function')
    .map((panel) => ({
      ...panel,
      extensionId: panel.extensionId ?? findContributionOwnerId(contributionIndex, 'panel', panel.id),
    }));
  const visiblePanelKeys = new Set(assetPanels
    .map((panel) => getPanelKey({
      ...panel,
      extensionId: panel.extensionId ?? findContributionOwnerId(contributionIndex, 'panel', panel.id),
    }))
    .filter((key) => activePanelKey === undefined || key === activePanelKey));
  const { data, preferences } = useTimelineEditorData();
  const { setAssetPanelState, uploadFiles } = useTimelineEditorOps();

  const builtInPanel = includeBuiltIn && data ? (
    <div className="rounded-xl border border-border bg-card/80 p-3">
      <AssetPanel
        assetMap={data.assetMap}
        rows={data.rows}
        meta={data.meta}
        backgroundAsset={data.output.background ?? undefined}
        showAll={preferences.assetPanel.showAll}
        showHidden={preferences.assetPanel.showHidden}
        hidden={preferences.assetPanel.hidden}
        setPanelState={setAssetPanelState}
        onUploadFiles={uploadFiles}
        registry={data.registry.assets}
      />
    </div>
  ) : null;

  if (!builtInPanel && panels.length === 0) {
    return null;
  }

  const handleContributionError = (info: ContributionErrorInfo) => {
    if (typeof console !== 'undefined') {
      console.warn(
        '[VideoEditorAssetPanelSurface] Panel error captured by boundary:',
        info,
      );
    }
  };

  return (
    <div className="flex flex-col gap-3">
      {builtInPanel}
      <ExtensionPanelHost panels={panels} visiblePanelKeys={visiblePanelKeys} video={panelVideo} onError={handleContributionError} />
    </div>
  );
}

export const VideoEditorAssetPanelSurface = memo(VideoEditorAssetPanelSurfaceComponent);
