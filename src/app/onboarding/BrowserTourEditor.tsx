import { useLayoutEffect, useState } from 'react';
import { ASTRID_EDITOR_EXTENSIONS } from '@astrid/packs/rendering/editor/catalog';
import { EditorRuntimeProvider } from '@/tools/video-editor/contexts/EditorRuntimeProvider.tsx';
import { PUBLIC_ASTRID_ELEMENT_HOST } from '@/pages/Home/astrid-public-host.tsx';
import { PUBLIC_TIMELINE_SERVICE_HOOKS } from '@/tools/video-editor/runtime/timelineHostServiceHooks.ts';
import { PUBLIC_TIMELINE_OBSERVATIONS } from '@/tools/video-editor/runtime/editorHostObservations.ts';
import { createVideoEditorEffectCatalog } from '@/tools/video-editor/lib/effect-catalog.ts';
import { createVideoEditorSequenceComponentCatalog } from '@/tools/video-editor/lib/sequence-component-catalog.ts';
import { createEditorTourDataProvider } from '@/tools/video-editor/tour/timeline/tourDataProvider.ts';
import { EDITOR_TOUR_TIMELINE_ID } from '@/tools/video-editor/tour/timeline/tourStages.ts';
import { EditorTourTimelineDriver } from '@/tools/video-editor/tour/timeline/EditorTourTimelineDriver.tsx';
import { EditorTourRunner } from '@/tools/video-editor/tour/runner/EditorTourRunner.tsx';
import { registerBrowserTourFinish } from '@/tools/video-editor/tour/runner/tourBeats.ts';
import { startEditorTour, exitEditorTour } from '@/shared/state/editorTourStore.ts';
import { TourChatPanel } from '@/tools/video-editor/components/AgentChat/TourChatPanel.tsx';
import { RemotionPreview } from '@/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx';
import { TimelineEditorCoreBody } from '@/tools/video-editor/components/TimelineEditor/TimelineEditorCoreBody.tsx';
import { useTimelineEditorData, useTimelinePlaybackContext } from '@/tools/video-editor/hooks/timelineStore.ts';

export const BROWSER_TOUR_EXTENSIONS = Object.freeze(ASTRID_EDITOR_EXTENSIONS.filter(extension => extension.manifest.id === 'haus.astrid.threejs-live-editor'));
if (BROWSER_TOUR_EXTENSIONS.length !== 1) throw new Error('The bundled Lantern Valley world renderer is missing.');
const EFFECTS = createVideoEditorEffectCatalog();
const SEQUENCES = createVideoEditorSequenceComponentCatalog();

function Preview() {
  const { resolvedConfig } = useTimelineEditorData();
  const { currentTime, previewRef, playerContainerRef, onPreviewTimeUpdate } = useTimelinePlaybackContext();
  return resolvedConfig ? <RemotionPreview ref={previewRef} config={resolvedConfig}
    initialTime={currentTime} currentTime={currentTime} onTimeUpdate={onPreviewTimeUpdate}
    playerContainerRef={playerContainerRef} /> : null;
}

/** Bundled media, in-memory operations and the bundled world renderer; no workspace services. */
export function BrowserTourEditor({ onFinish }: { onFinish: () => void }) {
  const [dataProvider] = useState(createEditorTourDataProvider);
  useLayoutEffect(() => {
    const unregister = registerBrowserTourFinish(onFinish);
    startEditorTour();
    return () => { exitEditorTour(); unregister(); };
  }, [onFinish]);
  return <EditorRuntimeProvider astridElementHost={PUBLIC_ASTRID_ELEMENT_HOST}
    dataProvider={dataProvider} timelineId={EDITOR_TOUR_TIMELINE_ID} timelineName="Lantern Valley"
    timelineServices={PUBLIC_TIMELINE_SERVICE_HOOKS} effectCatalog={EFFECTS} sequenceComponentCatalog={SEQUENCES}
    extensions={BROWSER_TOUR_EXTENSIONS} extensionStateRepository={null}
    runtime={{ assetResolver: dataProvider, exporter: null, hostContext: null }}
    enableMutationServices enableLiveServices={false} enableRenderExport={false}>
    <main className="grid h-dvh grid-rows-[40%_60%] md:grid-rows-1 md:grid-cols-[minmax(280px,32%)_1fr] overflow-hidden bg-background text-foreground" aria-label="Lantern Valley guided demo">
      <aside className="min-h-0 border-r"><TourChatPanel /></aside>
      <div className="grid min-h-0 min-w-0 grid-rows-[minmax(0,1fr)_minmax(180px,35%)]">
        <section className="relative min-h-0 min-w-0" data-editor-tour="preview"><Preview /></section>
        <section className="min-h-0 min-w-0" data-editor-tour="timeline"><TimelineEditorCoreBody hostObservations={PUBLIC_TIMELINE_OBSERVATIONS} /></section>
      </div>
    </main>
    <EditorTourTimelineDriver />
    <EditorTourRunner />
  </EditorRuntimeProvider>;
}
