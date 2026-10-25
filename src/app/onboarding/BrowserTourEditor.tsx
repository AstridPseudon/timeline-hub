import { useLayoutEffect, useRef, useState, type CSSProperties } from 'react';
import { AppFrame } from '@/app/components/AppFrame.tsx';
import { AppMainContent } from '@/app/components/AppMainContent.tsx';
import { TasksPaneSurface, TasksPaneChatSlot } from '@/features/tasks/components/TasksPane/components/TasksPaneSurface';
import { usePanesStore } from '@/shared/state/panesStore';
import { usePaneControlsHosted } from '@/shared/state/paneControlsHost';
import { useEditorTour, startEditorTour, exitEditorTour } from '@/shared/state/editorTourStore.ts';
import { UI_Z_LAYERS } from '@/shared/lib/uiLayers.ts';
import { ASTRID_EDITOR_EXTENSIONS } from '@astrid/packs/rendering/editor/catalog';
import { EditorRuntimeProvider } from '@/tools/video-editor/contexts/EditorRuntimeProvider.tsx';
import { PUBLIC_ASTRID_ELEMENT_HOST } from '@/pages/Home/astrid-public-host.tsx';
import { ProjectHeaderControls } from '@/shared/components/ProjectHeaderControls.tsx';
import { ProjectTimelinePicker } from '@/shared/components/ProjectTimelineSelectors.tsx';
import { tourHeaderProps } from '@/tools/video-editor/tour/timeline/tourHeaderProps.ts';
import { PUBLIC_TIMELINE_SERVICE_HOOKS } from '@/tools/video-editor/runtime/timelineHostServiceHooks.ts';
import { PUBLIC_TIMELINE_OBSERVATIONS } from '@/tools/video-editor/runtime/editorHostObservations.ts';
import { createVideoEditorEffectCatalog } from '@/tools/video-editor/lib/effect-catalog.ts';
import { createVideoEditorSequenceComponentCatalog } from '@/tools/video-editor/lib/sequence-component-catalog.ts';
import { createEditorTourDataProvider } from '@/tools/video-editor/tour/timeline/tourDataProvider.ts';
import { EDITOR_TOUR_TIMELINE_ID } from '@/tools/video-editor/tour/timeline/tourStages.ts';
import { EditorTourTimelineDriver } from '@/tools/video-editor/tour/timeline/EditorTourTimelineDriver.tsx';
import { EditorTourRunner } from '@/tools/video-editor/tour/runner/EditorTourRunner.tsx';
import { registerBrowserTourFinish } from '@/tools/video-editor/tour/runner/tourBeats.ts';
import { useEditorDeviceClass } from '@/tools/video-editor/tour/runner/useIsDesktopEditor.ts';
import { TourChatPanel } from '@/tools/video-editor/components/AgentChat/TourChatPanel.tsx';
import { TimelineEditorShellCore } from '@/tools/video-editor/components/TimelineEditorShellCore.tsx';
import { TimelineEditorCoreBody } from '@/tools/video-editor/components/TimelineEditor/TimelineEditorCoreBody.tsx';
import { useTimelineEditorOps, useTimelineDataSelector } from '@/tools/video-editor/hooks/timelineStore.ts';
import { HOST_EXTENSIONS_PANEL_KEY, HOST_PROPERTIES_PANEL_KEY } from '@/tools/video-editor/components/PropertiesPanel/VideoEditorPanelDisplayControl.tsx';

export const BROWSER_TOUR_EXTENSIONS = Object.freeze(ASTRID_EDITOR_EXTENSIONS.filter(extension => extension.manifest.id === 'haus.astrid.threejs-live-editor'));
if (BROWSER_TOUR_EXTENSIONS.length !== 1) throw new Error('The bundled Lantern Valley world renderer is missing.');
const EFFECTS = createVideoEditorEffectCatalog();
const SEQUENCES = createVideoEditorSequenceComponentCatalog();
const HEADER = tourHeaderProps();
const noOp = () => undefined;

const TOUR_PICKER_PROPS = {
  projects: [], timelines: [], ...HEADER,
  onSelectProject: noOp, onSelectTimeline: noOp,
} as const;

function BrowserTourEditorSurface() {
  const ops = useTimelineEditorOps();
  const opsRef = useRef(ops);
  opsRef.current = ops;
  const hasWorld = useTimelineDataSelector((timeline) => timeline.data?.resolvedConfig.clips.some(
    (clip) => clip.clipType === 'haus.astrid.liveScene',
  ) ?? false);

  useLayoutEffect(() => {
    // The in-memory demo starts with the Inspector and switches to the world extension when it lands.
    opsRef.current.setRightPanelLayoutSlot(HOST_PROPERTIES_PANEL_KEY, 'dock');
    opsRef.current.setRightPanelLayoutSlot(HOST_EXTENSIONS_PANEL_KEY, 'dock');
    opsRef.current.setSelectedRightPanelId(hasWorld ? HOST_EXTENSIONS_PANEL_KEY : HOST_PROPERTIES_PANEL_KEY);
  }, [hasWorld]);

  return <TimelineEditorShellCore
    timelineId={EDITOR_TOUR_TIMELINE_ID}
    isOnEditorPage
    showHeader={false}
    previewNavigationControls={<ProjectTimelinePicker {...TOUR_PICKER_PROPS} showProjectSelector={false} showProjectLabel={false} />}
    renderTimeline={actions => <TimelineEditorCoreBody hostObservations={PUBLIC_TIMELINE_OBSERVATIONS} {...actions} />}
  />;
}

function BrowserTourFrame() {
  const tasksPaneWidth = usePanesStore(state => state.tasksPaneWidth);
  const touchPane = usePaneControlsHosted();
  const beat = useEditorTour(state => state.beat);
  // The demo editor is a picture behind the tour: the spotlight already takes every pointer, so keep focus and
  // assistive tech on the card (and the chat's Send) too.
  const touring = useEditorTour(state => state.status === 'running');
  const phone = useEditorDeviceClass() === 'phone';
  const chatVisible = !touchPane || beat === 'compose' || beat === 'respond';
  const tasksPaneReserve = touchPane ? '0px' : `${tasksPaneWidth}px`;
  const contentStyle = { marginRight: tasksPaneReserve, willChange: 'margin, padding' } as CSSProperties;
  const projectControls = <ProjectHeaderControls
    projects={[]}
    projectId={HEADER.projectId}
    projectName={HEADER.projectName}
    onSelectProject={noOp}
    selectedProject={null}
    pickerDisabled={HEADER.disabled}
    actionsDisabled={HEADER.disabled}
    showDialogs={false}
  />;

  return <AppFrame fullEditor>
    <div className="contents" {...(touring ? { inert: '' } : {})}><AppMainContent
      headerContent={projectControls}
      tasksPaneReserve={tasksPaneReserve}
      contentStyle={contentStyle}
      isEditorRoute
      isFullEditorSurface
      navigationMode="tools"
      showProjectControls={false}
      settingsDisabled={HEADER.disabled}
      nonEditorMainClassName=""
      mainLabel="Lantern Valley guided demo"
    >
      <BrowserTourEditorSurface />
    </AppMainContent></div>
    <div className="pointer-events-none" style={{
      position: 'fixed', right: 0, top: 0, bottom: 0,
      // A phone's chat takes the whole screen while it has the spotlight, rather than leaving a sliver of editor.
      width: phone ? '100vw' : touchPane ? 'min(28rem, calc(100vw - 3rem))' : `${tasksPaneWidth}px`,
      zIndex: UI_Z_LAYERS.TASKS_PANE_CONTENT,
    }}>
      <TasksPaneSurface role="complementary" aria-label="Task and chat pane" aria-hidden={!chatVisible}
        {...(!chatVisible ? { inert: '' } : {})}
        className={`absolute top-0 right-0 transform transition-transform duration-300 ease-smooth ${chatVisible ? 'translate-x-0' : 'translate-x-full'}`}>
        <TasksPaneChatSlot><TourChatPanel /></TasksPaneChatSlot>
      </TasksPaneSurface>
    </div>
  </AppFrame>;
}

/** The shared app/editor shell backed by bundled media and in-memory operations. */
export function BrowserTourEditor({ onFinish }: { onFinish: () => void }) {
  const [dataProvider] = useState(createEditorTourDataProvider);
  useLayoutEffect(() => {
    const unregister = registerBrowserTourFinish(onFinish);
    startEditorTour();
    return () => { exitEditorTour(); unregister(); };
  }, [onFinish]);
  return <EditorRuntimeProvider astridElementHost={PUBLIC_ASTRID_ELEMENT_HOST}
    dataProvider={dataProvider} timelineId={HEADER.timelineId} timelineName={HEADER.timelineName}
    timelineServices={PUBLIC_TIMELINE_SERVICE_HOOKS} effectCatalog={EFFECTS} sequenceComponentCatalog={SEQUENCES}
    extensions={BROWSER_TOUR_EXTENSIONS} extensionStateRepository={null}
    runtime={{ assetResolver: dataProvider, exporter: null, hostContext: null }}
    enableMutationServices enableLiveServices={false} enableRenderExport={false}>
    <BrowserTourFrame />
    <EditorTourTimelineDriver />
    <EditorTourRunner />
  </EditorRuntimeProvider>;
}
