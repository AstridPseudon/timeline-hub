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
import { EditorTourTimelineDriver } from '@/tools/video-editor/tour/timeline/EditorTourTimelineDriver.tsx';
import { EditorTourRunner } from '@/tools/video-editor/tour/runner/EditorTourRunner.tsx';
import { registerBrowserTourFinish } from '@/tools/video-editor/tour/runner/tourBeats.ts';
import { startEditorTour, exitEditorTour } from '@/shared/state/editorTourStore.ts';
import { TourChatPanel } from '@/tools/video-editor/components/AgentChat/TourChatPanel.tsx';
import { RemotionPreview } from '@/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx';
import { TimelineEditorCoreBody } from '@/tools/video-editor/components/TimelineEditor/TimelineEditorCoreBody.tsx';
import { useTimelineDataSelector, useTimelineEditorData, useTimelinePlaybackContext } from '@/tools/video-editor/hooks/timelineStore.ts';
import { useTimelineEditorOps } from '@/tools/video-editor/hooks/timelineStore.ts';
import { VideoEditorRightPanelDock } from '@/tools/video-editor/components/PropertiesPanel/VideoEditorRightPanelDock.tsx';
import { HOST_EXTENSIONS_PANEL_KEY, HOST_PROPERTIES_PANEL_KEY } from '@/tools/video-editor/components/PropertiesPanel/VideoEditorPanelDisplayControl.tsx';
import { AppHeader } from '@/shared/components/AppHeader.tsx';
import { ProjectHeaderControls } from '@/shared/components/ProjectHeaderControls.tsx';
import { ProjectTimelinePicker } from '@/shared/components/ProjectTimelineSelectors.tsx';
import { tourHeaderProps } from '@/tools/video-editor/tour/timeline/tourHeaderProps.ts';

export const BROWSER_TOUR_EXTENSIONS = Object.freeze(ASTRID_EDITOR_EXTENSIONS.filter(extension => extension.manifest.id === 'haus.astrid.threejs-live-editor'));
if (BROWSER_TOUR_EXTENSIONS.length !== 1) throw new Error('The bundled Lantern Valley world renderer is missing.');
const EFFECTS = createVideoEditorEffectCatalog();
const SEQUENCES = createVideoEditorSequenceComponentCatalog();
const noOp = () => undefined;

function Preview() {
  const { resolvedConfig } = useTimelineEditorData();
  const { currentTime, previewRef, playerContainerRef, onPreviewTimeUpdate } = useTimelinePlaybackContext();
  return resolvedConfig ? <RemotionPreview ref={previewRef} config={resolvedConfig}
    initialTime={currentTime} currentTime={currentTime} onTimeUpdate={onPreviewTimeUpdate}
    playerContainerRef={playerContainerRef} compact touchChrome /> : null;
}

function BrowserTourEditorSurface({ header }: { header: ReturnType<typeof tourHeaderProps> }) {
  const ops = useTimelineEditorOps();
  const opsRef = useRef(ops);
  opsRef.current = ops;
  const hasWorld = useTimelineDataSelector((timeline) => timeline.data?.resolvedConfig.clips.some(
    (clip) => clip.clipType === 'haus.astrid.liveScene',
  ) ?? false);

  useLayoutEffect(() => {
    // The tour runs on an in-memory timeline, so nothing here is saved. The dock shows Inspector while the demo timeline is empty, then Extensions once the world lands.
    opsRef.current.setRightPanelLayoutSlot(HOST_PROPERTIES_PANEL_KEY, 'dock');
    opsRef.current.setSelectedRightPanelId(hasWorld ? HOST_EXTENSIONS_PANEL_KEY : HOST_PROPERTIES_PANEL_KEY);
  }, [hasWorld]);

  return <div className="grid min-h-0 min-w-0 grid-cols-1 grid-rows-[minmax(0,1fr)_minmax(0,.8fr)_minmax(0,1fr)] md:grid-cols-[minmax(0,1fr)_minmax(220px,min(calc(32vw_+_12px),432px))] md:grid-rows-[minmax(0,1fr)_minmax(180px,35%)]">
    <section className="relative min-h-0 min-w-0" data-editor-tour="preview">
      <div className="pointer-events-none absolute inset-x-0 top-0 z-20 flex items-start px-3 py-3">
        <div className="pointer-events-auto flex min-w-0 max-w-[min(75%,32rem)] flex-col items-start gap-1" data-testid="video-editor-preview-navigation-controls">
          <ProjectTimelinePicker
            projects={[]}
            timelines={[]}
            {...header}
            onSelectProject={noOp}
            onSelectTimeline={noOp}
            showProjectSelector={false}
          />
        </div>
      </div>
      <Preview />
    </section>
    <section className="min-h-0 min-w-0" data-editor-tour="extensions">
      <VideoEditorRightPanelDock leftPanelPresent={false} />
    </section>
    <section className="min-h-0 min-w-0 md:col-span-2 md:row-start-2" data-editor-tour="timeline">
      <TimelineEditorCoreBody hostObservations={PUBLIC_TIMELINE_OBSERVATIONS} />
    </section>
  </div>;
}

function BrowserTourEditorHeader({ header }: { header: ReturnType<typeof tourHeaderProps> }) {
  const projectControls = (
    <ProjectHeaderControls
      projects={[]}
      projectId={header.projectId}
      projectName={header.projectName}
      onSelectProject={noOp}
      selectedProject={null}
      pickerDisabled={header.disabled}
      actionsDisabled={header.disabled}
      showDialogs={false}
    />
  );

  return <AppHeader navigationControls={projectControls} settingsDisabled={header.disabled} />;
}

/** Bundled media, in-memory operations and the bundled world renderer; no workspace services. */
export function BrowserTourEditor({ onFinish }: { onFinish: () => void }) {
  const [dataProvider] = useState(createEditorTourDataProvider);
  const header = tourHeaderProps();
  const tasksPaneWidth = usePanesStore(state => state.tasksPaneWidth);
  useLayoutEffect(() => {
    const unregister = registerBrowserTourFinish(onFinish);
    startEditorTour();
    return () => { exitEditorTour(); unregister(); };
  }, [onFinish]);
  return <EditorRuntimeProvider astridElementHost={PUBLIC_ASTRID_ELEMENT_HOST}
    dataProvider={dataProvider} timelineId={header.timelineId} timelineName={header.timelineName}
    timelineServices={PUBLIC_TIMELINE_SERVICE_HOOKS} effectCatalog={EFFECTS} sequenceComponentCatalog={SEQUENCES}
    extensions={BROWSER_TOUR_EXTENSIONS} extensionStateRepository={null}
    runtime={{ assetResolver: dataProvider, exporter: null, hostContext: null }}
    enableMutationServices enableLiveServices={false} enableRenderExport={false}>
    <div className="flex h-dvh min-h-0 w-full flex-col overflow-hidden bg-background text-foreground">
      <BrowserTourEditorHeader header={header} />
      <main className="grid min-h-0 w-full flex-1 grid-rows-[minmax(0,1fr)_45%] overflow-hidden md:grid-rows-1 md:grid-cols-[minmax(0,1fr)_var(--tasks-pane-width)]"
      style={{ '--tasks-pane-width': `${tasksPaneWidth}px` } as CSSProperties} aria-label="Lantern Valley guided demo">
      <BrowserTourEditorSurface header={header} />
      <TasksPaneSurface role="complementary" aria-label="Task and chat pane" className="relative min-h-0 min-w-0">
        <TasksPaneChatSlot><TourChatPanel /></TasksPaneChatSlot>
      </TasksPaneSurface>
      </main>
    </div>
    <EditorTourTimelineDriver />
    <EditorTourRunner />
  </EditorRuntimeProvider>;
}
