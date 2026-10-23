import { useLayoutEffect, useRef, useState, type CSSProperties } from 'react';
import { TasksPaneSurface, TasksPaneChatSlot } from '@/features/tasks/components/TasksPane/components/TasksPaneSurface';
import { usePanesStore } from '@/shared/state/panesStore';
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
import { useTimelineEditorOps } from '@/tools/video-editor/hooks/timelineStore.ts';
import { VideoEditorRightPanelDock } from '@/tools/video-editor/components/PropertiesPanel/VideoEditorRightPanelDock.tsx';
import { HOST_EXTENSIONS_PANEL_KEY, HOST_PROPERTIES_PANEL_KEY } from '@/tools/video-editor/components/PropertiesPanel/VideoEditorPanelDisplayControl.tsx';

export const BROWSER_TOUR_EXTENSIONS = Object.freeze(ASTRID_EDITOR_EXTENSIONS.filter(extension => extension.manifest.id === 'haus.astrid.threejs-live-editor'));
if (BROWSER_TOUR_EXTENSIONS.length !== 1) throw new Error('The bundled Lantern Valley world renderer is missing.');
const EFFECTS = createVideoEditorEffectCatalog();
const SEQUENCES = createVideoEditorSequenceComponentCatalog();

function Preview() {
  const { resolvedConfig } = useTimelineEditorData();
  const { currentTime, previewRef, playerContainerRef, onPreviewTimeUpdate } = useTimelinePlaybackContext();
  return resolvedConfig ? <RemotionPreview ref={previewRef} config={resolvedConfig}
    initialTime={currentTime} currentTime={currentTime} onTimeUpdate={onPreviewTimeUpdate}
    playerContainerRef={playerContainerRef} compact touchChrome /> : null;
}

function BrowserTourEditorSurface() {
  const ops = useTimelineEditorOps();
  const opsRef = useRef(ops);
  opsRef.current = ops;

  useLayoutEffect(() => {
    // The tour runs on an in-memory timeline, so this only opens the bundled
    // extension panel in the tour host; no user preference or workspace state is saved.
    opsRef.current.setRightPanelLayoutSlot(HOST_PROPERTIES_PANEL_KEY, 'dock');
    opsRef.current.setSelectedRightPanelId(HOST_EXTENSIONS_PANEL_KEY);
  }, []);

  return <div className="grid min-h-0 min-w-0 grid-cols-1 grid-rows-[minmax(0,1fr)_minmax(0,.8fr)_minmax(0,1fr)] md:grid-cols-[minmax(0,1fr)_minmax(220px,min(calc(32vw_+_12px),432px))] md:grid-rows-[minmax(0,1fr)_minmax(180px,35%)]">
    <section className="relative min-h-0 min-w-0" data-editor-tour="preview"><Preview /></section>
    <section className="min-h-0 min-w-0" data-editor-tour="extensions">
      <VideoEditorRightPanelDock leftPanelPresent={false} />
    </section>
    <section className="min-h-0 min-w-0 md:col-span-2 md:row-start-2" data-editor-tour="timeline">
      <TimelineEditorCoreBody hostObservations={PUBLIC_TIMELINE_OBSERVATIONS} />
    </section>
  </div>;
}

/** Bundled media, in-memory operations and the bundled world renderer; no workspace services. */
export function BrowserTourEditor({ onFinish }: { onFinish: () => void }) {
  const [dataProvider] = useState(createEditorTourDataProvider);
  const tasksPaneWidth = usePanesStore(state => state.tasksPaneWidth);
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
    <main className="grid h-dvh grid-rows-[minmax(0,1fr)_45%] md:grid-rows-1 md:grid-cols-[minmax(0,1fr)_var(--tasks-pane-width)] overflow-hidden bg-background text-foreground"
      style={{ '--tasks-pane-width': `${tasksPaneWidth}px` } as CSSProperties} aria-label="Lantern Valley guided demo">
      <BrowserTourEditorSurface />
      <TasksPaneSurface role="complementary" aria-label="Task and chat pane" className="relative min-h-0 min-w-0">
        <TasksPaneChatSlot><TourChatPanel /></TasksPaneChatSlot>
      </TasksPaneSurface>
    </main>
    <EditorTourTimelineDriver />
    <EditorTourRunner />
  </EditorRuntimeProvider>;
}
