import { EmptyWorkspaceGuidance } from '@/shared/components/RuntimeConnection/EmptyWorkspaceGuidance.tsx';
import { useNativeEditorRecovery } from '../hooks/useNativeEditorRecovery.ts';
import { assertNativeEditorConnection } from "@/integrations/astrid/nativeEditorConnection.ts";
import type { ExtensionPendingWorkState } from "@/sdk/context.ts";
import {
  useRuntimeEditorDiscovery,
  chooseRuntimeTimeline,
} from "../hooks/useRuntimeEditorDiscovery.ts";
// Layer map & invariants: docs/structure_detail/tool_video_editor.md
/**
 * Internal Astrid App route adapter for the in-app video editor page.
 * Not part of the supported public SDK surface.
 */
import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  useSyncExternalStore,
} from "react";
import { formatDistanceToNowStrict } from "date-fns";
import { useLocation, useSearchParams } from "react-router-dom";
import { useHomeNavigation } from "@/shared/hooks/useHomeNavigation.ts";
import { isHomeToolPathActive } from "@/shared/lib/tooling/homeNavigation.ts";
import { Button } from "@/shared/components/ui/button.tsx";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/shared/components/ui/card.tsx";
import { useOptionalAgentChatRegistry } from "@/shared/contexts/AgentChatContext.tsx";
import { useOptionalGlobalHeaderSlot } from "@/shared/contexts/ToolPageHeaderContext.tsx";
import { toast } from "@/shared/components/ui/toast.tsx";
import type { DataProvider } from "@/tools/video-editor/data/DataProvider.ts";
import { VideoEditorProvider } from "@/tools/video-editor/contexts/VideoEditorProvider.tsx";
import { devLocalExtensions } from "@/tools/video-editor/dev/localExtensions.ts";
import {
  TRANSCRIPT_LANE_FIXTURE_PARAM,
  withTranscriptFixture,
} from "@/tools/video-editor/dev/transcript-lane/fixtureProvider.ts";
import {
  getSnapshot as getDevDisabledSnapshot,
  subscribe as subscribeDevDisabled,
} from "@/tools/video-editor/dev/devExtensionEnablement.ts";
import { useExtensionLoaderWiring } from "@/tools/video-editor/runtime/useExtensionLoaderWiring";
import { AstridVideoEditorShell } from "@/tools/video-editor/components/AstridVideoEditorShell.tsx";
import {
  ProjectTimelinePicker,
} from "@/shared/components/ProjectTimelineSelectors.tsx";
import { ProjectHeaderActions } from "@/shared/components/ProjectHeaderActions.tsx";
import {
  AstridRuntimeClient,
  RuntimeUnavailableError,
  type RuntimeConnectorError,
} from "@/integrations/runtime/client.ts";
import {
  createCanonicalTimeline,
  ensureProjectHasTimeline,
} from "@/integrations/runtime/createDefaultTimeline.ts";
import { ApiError } from "@/integrations/runtime/generated.ts";
import { generateUUID } from "@/shared/lib/taskCreation/ids.ts";
import { AppHeader } from "@/shared/components/AppHeader.tsx";
import { runtimeOrigin } from "@/integrations/runtime/connection.ts";
import { RuntimeConnectorRecoveryBanner } from "@/shared/components/RuntimeConnection/RuntimeConnectorRecoveryBanner.tsx";
import { RuntimeDataProvider } from "@/integrations/runtime/dataProvider.ts";
import type { SaveStatus } from "@/tools/video-editor/hooks/useTimelinePersistence.ts";
import { publishLocalTestExtensionDiagnostics } from "@/app/localTestRuntime.ts";
import {
  getExtensionReleaseFlags,
  selectReleaseEnabledExtensions,
} from "@/tools/video-editor/runtime/extensionReleaseControls.ts";

type ProviderSelection = {
  dataProvider: DataProvider;
  projectId: string | null;
  projectSlug: string | null;
  timelineId: string;
  timelineName: string | null;
  userId: string | null;
  remountKey: string;
  runtimeReconnect?: () => Promise<void>;
};

/** Keep existing browser resume preferences; values are now canonical IDs. */
export const LAST_OPENED_PROJECT_STORAGE_KEY =
  "astrid:lastOpenedLocalProjectSlug";

type EditorProject = {
  slug: string;
  name: string;
  created_at?: string;
  project_id?: string;
  metadata?: Record<string, unknown>;
};

function mostRecentlyCreatedProject(
  projects: EditorProject[],
): EditorProject | null {
  return (
    projects
      .map((project) => ({
        project,
        createdAt: project.created_at
          ? Date.parse(project.created_at)
          : Number.NaN,
      }))
      .sort(
        (left, right) =>
          (Number.isFinite(right.createdAt) ? right.createdAt : -Infinity) -
          (Number.isFinite(left.createdAt) ? left.createdAt : -Infinity) ||
          left.project.slug.localeCompare(right.project.slug),
      )[0]?.project ?? null
  );
}

function useVideoEditorProviderSelection({
  projectId, projectSlug, timelineId, timelineName, onRuntimeError,
}: {
  projectId: string | null;
  projectSlug: string | null;
  timelineId: string | null;
  timelineName: string | null;
  onRuntimeError: (error: RuntimeConnectorError) => void;
}): ProviderSelection | null {
  // Only a document identity change replaces the stateful provider. Display
  // metadata and connection recovery must leave pending reads and drafts mounted.
  const connection = useMemo(() => {
    if (!projectId || !timelineId) return null;
    const dataProvider = new RuntimeDataProvider({ projectId, onRuntimeError });
    return { dataProvider, runtimeReconnect: () => dataProvider.reconnect() };
  }, [projectId, timelineId, onRuntimeError]);
  return useMemo(() => connection && projectId && timelineId ? {
    ...connection, projectId, projectSlug, timelineId, timelineName,
    userId: null,
    remountKey: `runtime:${projectId}:${timelineId}`,
  } : null, [connection, projectId, projectSlug, timelineId, timelineName]);
}

export default function VideoEditorPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  // ---- Reviewed extension bundle + smoke wiring ----------------------------
  // Production defaults closed and can only be enabled by the deployment-owned
  // runtime document loaded before React mounts. DEV defaults open for authoring. URL or browser
  // storage cannot override the production rollout contract.
  //
  // Dev-local enablement is an external store (`devExtensionEnablement.ts`):
  // subscribing via useSyncExternalStore makes the disabled-ID snapshot part of
  // this component's render inputs, so a toggle in the ExtensionManager updates
  // the direct-extension memo below without a searchParams change or a loader
  // refresh key. The snapshot is a stable cached Set — unchanged reads never
  // re-render the page, and disabling an extension drops it from the list, which
  // tears its runtime lifecycle down (the lifecycle host disposes on removal).
  const devDisabledIds = useSyncExternalStore(
    subscribeDevDisabled,
    getDevDisabledSnapshot,
    getDevDisabledSnapshot,
  );

  const extensionReleaseFlags = getExtensionReleaseFlags();
  const smokeDirectExtensions = useMemo(() => {
    // The routed native editor uses the same admitted catalog for every backend.
    const disabled = import.meta.env.DEV ? devDisabledIds : new Set<string>();
    // Arbitrary scratchpad manifests remain usable in DEV. Production alone
    // applies the frozen reviewed inventory in addition to the runtime flags.
    const releaseEnabledExtensions = (
      import.meta.env.DEV
        ? devLocalExtensions
        : selectReleaseEnabledExtensions(
            devLocalExtensions,
            extensionReleaseFlags,
          )
    ).filter((extension) => !disabled.has(extension.manifest.id as string));
    const direct = [...releaseEnabledExtensions];
    return direct.length > 0 ? direct : undefined;
  }, [
    searchParams,
    devDisabledIds,
    extensionReleaseFlags.extensionHostEnabled,
    extensionReleaseFlags.transcriptCaptionFoundryEnabled,
    extensionReleaseFlags.runawayTypedTimelineEnabled,
  ]);

  // ---- Timeline-overlay host gate -----------------------------------------
  // An enabled, reviewed overlay contribution turns on the host in every
  // environment. The URL canary remains DEV-only and cannot bypass the parent
  // deployment kill switch.
  const timelineOverlaysEnabled =
    extensionReleaseFlags.extensionHostEnabled &&
    (smokeDirectExtensions ?? []).some((ext) =>
      ext.manifest.contributions?.some(
        (contribution) => contribution.kind === "timelineOverlay",
      ),
    );

  // ---- M14: extension loader wiring (host-owned) --------------------------
  // Resolves direct-local extensions + optional repository state through the
  // ExtensionLoader pipeline.  When no repository is provided, direct-local
  // extensions pass through unchanged (backward compatible).
  const {
    resolvedExtensions,
    diagnostics: loaderDiagnostics,
  } = useExtensionLoaderWiring({
    directExtensions: smokeDirectExtensions,
    repository: null,
    bundleStore: null,
  });
  useEffect(() => {
    publishLocalTestExtensionDiagnostics("loader", loaderDiagnostics);
  }, [loaderDiagnostics]);
  const { pathname } = useLocation();
  const { targetPath } = useHomeNavigation();
  const globalHeaderSlot = useOptionalGlobalHeaderSlot();
  const hasGlobalHeader = globalHeaderSlot.hasProvider;

  const projectId = searchParams.get("project")?.trim() || null;
  const timelineId = searchParams.get("timeline")?.trim() || null;
  const isHomeTool = isHomeToolPathActive(pathname, targetPath);
  const [selectorsOpen, setSelectorsOpen] = useState(false);
  const runtimeDiscovery = useRuntimeEditorDiscovery({
    enabled: true, projectId, open: selectorsOpen,
  });
  const projects = runtimeDiscovery.projectsQuery.data;
  const timelines = runtimeDiscovery.timelinesQuery.data;
  const selectedProject = runtimeDiscovery.project;
  const selectedTimeline = timelines?.find(t => t.timeline_id === timelineId) ?? null;

  useEffect(() => {
    if (projectId || timelineId || !projects || runtimeDiscovery.projectsQuery.error) return;
    let previous: string | null = null;
    try { previous = window.localStorage.getItem(LAST_OPENED_PROJECT_STORAGE_KEY); } catch { /* Storage is optional. */ }
    const project = projects.find(p => p.project_id === previous)
      ?? projects.find(p => p.slug === previous)
      ?? mostRecentlyCreatedProject(projects);
    if (!project?.project_id) return;
    setSearchParams(current => {
      if (current.has("project")) return current;
      const next = new URLSearchParams(current);
      next.set("project", project.project_id!);
      return next;
    }, { replace: true });
  }, [projectId, timelineId, projects, runtimeDiscovery.projectsQuery.error, setSearchParams]);

  useEffect(() => {
    if (!selectedProject) return;
    try { window.localStorage.setItem(LAST_OPENED_PROJECT_STORAGE_KEY, selectedProject.project_id); } catch { /* Storage is optional. */ }
  }, [selectedProject]);

  // Chat, the gallery and the editor all use the same canonical project,
  // including projects which have not created their first timeline yet.
  const agentChatRegistry = useOptionalAgentChatRegistry();
  const chatProjectId = projectId;
  const chatProjectSlug = selectedProject?.slug ?? null;
  useEffect(() => {
    if (!agentChatRegistry) return;
    agentChatRegistry.registerProject({
      timelineId: null,
      editorContext: chatProjectId ? {
        tool: "video-editor", projectId: chatProjectId, projectSlug: chatProjectSlug,
        timelineId: null, timelineName: null,
        deepLink: typeof globalThis.location?.href === "string" ? globalThis.location.href : null,
      } : null,
    });
    return agentChatRegistry.unregisterProject;
  }, [agentChatRegistry, chatProjectId, chatProjectSlug]);

  const [mountedSaveStatus, setMountedSaveStatus] =
    useState<SaveStatus>("saved");
  const [settingPrimaryTimelineId, setSettingPrimaryTimelineId] = useState<
    string | null
  >(null);
  const [runtimeConnectorError, setRuntimeConnectorError] =
    useState<RuntimeConnectorError | null>(null);
  const [runtimeRetrying, setRuntimeRetrying] = useState(false);
  const [nativeRecoveryError, setNativeRecoveryError] = useState<string | null>(
    null,
  );
  const [creatingFirstTimeline, setCreatingFirstTimeline] = useState(false);
  const [firstTimelineError, setFirstTimelineError] = useState<string | null>(
    null,
  );
  const timelineSelectionRef = useRef({
    projectId: projectId,
    timelineId: timelineId,
  });
  timelineSelectionRef.current = {
    projectId: projectId,
    timelineId: timelineId,
  };
  const attemptedFirstTimelineProjects = useRef(new Set<string>());
  const pendingAdditionalTimeline = useRef<{
    projectId: string;
    timelineId: string;
    name: string;
  } | null>(null);
  const projectsPending = !projects && !runtimeDiscovery.projectsQuery.error;
  const timelinesPending = !!selectedProject && !timelines && !runtimeDiscovery.timelinesQuery.error;
  const projectMissing = !!projectId && !!projects && !selectedProject;
  const timelineMissing = !!timelineId && !!timelines && !selectedTimeline;
  // Resolve both identities before mounting a document. Cached discovery data
  // stays available during connection failures, preserving an already mounted
  // editor, but an unverified or cross-project URL must never open a provider.
  const selectionVerified = !!selectedProject && !!selectedTimeline;
  const workspaceSettling = !runtimeDiscovery.projectsQuery.error && !runtimeDiscovery.timelinesQuery.error
    && (projectsPending || timelinesPending || (!projectId && !timelineId && (projects?.length ?? 0) > 0)
      || (!!selectedProject && !timelineId && (timelines?.some(t => !t.is_shot) ?? false)));
  const connectorScope = JSON.stringify([projectId, timelineId]);
  const currentConnectorScope = useRef(connectorScope);
  currentConnectorScope.current = connectorScope;
  const reportNativeFailure = useRef<() => void>(() => undefined);
  const onRuntimeError = useCallback((error: RuntimeConnectorError) => {
    if (currentConnectorScope.current !== connectorScope) return;
    setRuntimeConnectorError(error);
    setRuntimeRetrying(false);
    reportNativeFailure.current();
  }, [connectorScope]);
  const providerSelection = useVideoEditorProviderSelection({
    projectId: selectionVerified ? projectId : null,
    projectSlug: selectedProject?.slug ?? projectId,
    timelineId: selectionVerified ? timelineId : null,
    timelineName: selectedTimeline?.name?.trim() || selectedTimeline?.slug || "Untitled timeline",
    onRuntimeError,
  });

  // dataKind V1 golden path (groken round 4): DEV-only fixture provider so the
  // transcript-lane example paints on any project with a media clip. Opt-in
  // via `?transcriptLaneFixture=1`; production builds drop the branch.
  const pageDataProvider = useMemo(() => {
    if (!providerSelection) return null;
    if (!import.meta.env.DEV) return providerSelection.dataProvider;
    const fixtureMode =
      import.meta.env.MODE === "test"
        ? new URLSearchParams(window.location.search).get(
            TRANSCRIPT_LANE_FIXTURE_PARAM,
          )
        : null;
    return fixtureMode !== null
      ? withTranscriptFixture(providerSelection.dataProvider, {
          dense: fixtureMode === "dense",
          renderMatrix: fixtureMode === "render-matrix",
        })
      : providerSelection.dataProvider;
  }, [providerSelection]);

  const nativeRecovery = useNativeEditorRecovery({
    enabled: !!providerSelection,
    scope: connectorScope,
    onRecovered: () => {
      setRuntimeConnectorError(null);
      setNativeRecoveryError(null);
      setRuntimeRetrying(false);
    },
  });
  reportNativeFailure.current = nativeRecovery.reportFailure;

  useEffect(() => {
    setRuntimeConnectorError(null);
    setNativeRecoveryError(null);
    setRuntimeRetrying(false);
  }, [providerSelection?.remountKey]);

  const handleRuntimeRetry = useCallback(async () => {
    if (runtimeRetrying || nativeRecovery.retrying) {
      return;
    }
    const attempt = nativeRecovery.beginManualAttempt();
    setRuntimeRetrying(true);
    try {
      await assertNativeEditorConnection();
      if (providerSelection?.runtimeReconnect)
        await providerSelection.runtimeReconnect();
      await runtimeDiscovery.reconnect();
      nativeRecovery.completeRecovery(attempt);
    } catch (error) {
      if (currentConnectorScope.current !== attempt.scope) return;
      nativeRecovery.reportFailure();
      setNativeRecoveryError(error instanceof Error ? error.message : String(error));
    } finally {
      setRuntimeRetrying(false);
    }
  }, [providerSelection, runtimeRetrying, runtimeDiscovery, nativeRecovery]);

  useEffect(() => {
    setMountedSaveStatus("saved");
  }, [providerSelection?.remountKey]);

  const [extensionPendingWork, setExtensionPendingWork] = useState<{
    scope: string;
    state: ExtensionPendingWorkState;
  } | null>(null);
  const scope = providerSelection?.remountKey ?? "";
  const onPendingWorkChange = useCallback(
    (state: ExtensionPendingWorkState) =>
      setExtensionPendingWork((previous) =>
        previous?.scope === scope &&
        JSON.stringify(previous.state) === JSON.stringify(state)
          ? previous
          : { scope, state },
      ),
    [scope],
  );
  const extensionWork =
    extensionPendingWork?.scope === scope ? extensionPendingWork.state : null;
  const extensionWriting = extensionWork?.writing ?? false;
  const extensionUnsaved = extensionWork?.unsaved ?? false;
  const isSwitchBlockedBySave =
    mountedSaveStatus === "saving" ||
    mountedSaveStatus === "retrying" ||
    extensionWriting;
  const confirmEditorRemount = useCallback(() => {
    if (!providerSelection) {
      return true;
    }
    // A save round-trip is in flight or a transport retry is scheduled —
    // switching would abandon it and lose the edit. Block like `saving`.
    if (
      mountedSaveStatus === "saving" ||
      mountedSaveStatus === "retrying" ||
      extensionWriting
    ) {
      return false;
    }
    if (
      extensionUnsaved &&
      !window.confirm(
        "You have an unsaved project transcript draft or conflict. Your draft will remain available for this source. Switch editors?",
      )
    )
      return false;
    if (mountedSaveStatus === "dirty") {
      return window.confirm(
        "You have unsaved timeline changes. Switch editors and discard them?",
      );
    }
    if (mountedSaveStatus === "error") {
      return window.confirm(
        "The last timeline save failed. Switch editors anyway?",
      );
    }
    return true;
  }, [mountedSaveStatus, providerSelection, extensionWriting, extensionUnsaved]);

  const confirmRemountRef = useRef(confirmEditorRemount);
  confirmRemountRef.current = confirmEditorRemount;
  useEffect(() => setFirstTimelineError(null), [projectId]);

  const handleSelectProject = useCallback((id: string) => {
    if (id === projectId || !projects?.some(p => p.project_id === id) || !confirmEditorRemount()) return;
    setSearchParams(current => {
      const next = new URLSearchParams(current);
      next.set("project", id);
      next.delete("timeline");
      return next;
    }, { replace: true });
  }, [projectId, projects, confirmEditorRemount, setSearchParams]);
  const handleSelectTimeline = useCallback((id: string) => {
    if (id === timelineId || !timelines?.some(t => t.timeline_id === id) || !confirmEditorRemount()) return;
    setSearchParams(current => {
      if (current.get("project") !== projectId) return current;
      const next = new URLSearchParams(current);
      next.set("timeline", id);
      return next;
    }, { replace: true });
  }, [timelineId, timelines, projectId, confirmEditorRemount, setSearchParams]);

  const handleCreateFirstTimeline = useCallback(async () => {
    if (!selectedProject || !projectId || creatingFirstTimeline || isSwitchBlockedBySave) {
      return;
    }
    setCreatingFirstTimeline(true);
    setFirstTimelineError(null);
    try {
      const timelineRef = await ensureProjectHasTimeline(
        projectId,
        new AstridRuntimeClient(),
      );
      await Promise.all([
        runtimeDiscovery.projectsQuery.refetch(),
        runtimeDiscovery.timelinesQuery.refetch(),
      ]);
      if (
        timelineSelectionRef.current.projectId === projectId &&
        !timelineSelectionRef.current.timelineId
      ) {
        setSearchParams(current => {
          if (current.get("project") !== projectId || current.has("timeline")) return current;
          const next = new URLSearchParams(current); next.set("timeline", timelineRef); return next;
        }, { replace: true });
      }
      toast.success("Timeline ready");
    } catch (error) {
      const safeDetail =
        error instanceof ApiError
          ? `${error.status} ${error.code}: ${error.message.replace(/[\r\n]+/g, " ").slice(0, 120)}`
          : error instanceof RuntimeUnavailableError
            ? `${error.status ?? "unavailable"} ${error.causeCode ?? error.code}`
            : error instanceof Error
              ? error.name
              : "unknown error";
      if (timelineSelectionRef.current.projectId === projectId) setFirstTimelineError(safeDetail);
      toast.error("Could not create the first timeline. You can retry here.");
    } finally {
      setCreatingFirstTimeline(false);
    }
  }, [
    creatingFirstTimeline,
    runtimeDiscovery.projectsQuery,
    runtimeDiscovery.timelinesQuery,
    setSearchParams,
    projectId,
    selectedProject,
    isSwitchBlockedBySave,
  ]);

  // Only authoritative empty project results trigger setup. Bound attempts per
  // mounted project prevent failed creation from becoming a background loop.
  useEffect(() => {
    if (
      !projectId ||
      timelineId ||
      runtimeDiscovery.timelinesQuery.isLoading ||
      runtimeDiscovery.timelinesQuery.isFetching ||
      runtimeDiscovery.timelinesQuery.error ||
      runtimeDiscovery.timelinesQuery.data?.length !== 0 ||
      creatingFirstTimeline ||
      attemptedFirstTimelineProjects.current.has(projectId)
    )
      return;
    attemptedFirstTimelineProjects.current.add(projectId);
    void handleCreateFirstTimeline();
  }, [
    projectId,
    timelineId,
    runtimeDiscovery.timelinesQuery.data,
    runtimeDiscovery.timelinesQuery.isLoading,
    runtimeDiscovery.timelinesQuery.isFetching,
    runtimeDiscovery.timelinesQuery.error,
    creatingFirstTimeline,
    handleCreateFirstTimeline,
  ]);

  const handleCreateAdditionalTimeline = useCallback(async () => {
    if (!selectedProject || !projectId || creatingFirstTimeline || isSwitchBlockedBySave) {
      return;
    }
    setCreatingFirstTimeline(true);
    setFirstTimelineError(null);
    const startingTimelineId = timelineId;
    const knownTimelines = runtimeDiscovery.timelinesQuery.data ?? [];
    const timelineCount = knownTimelines.filter(
      (timeline) => !timeline.is_shot,
    ).length;
    const pending =
      pendingAdditionalTimeline.current?.projectId === projectId
        ? pendingAdditionalTimeline.current
        : {
            projectId: projectId,
            timelineId: generateUUID(),
            name: `Timeline ${timelineCount + 1}`,
          };
    pendingAdditionalTimeline.current = pending;
    try {
      const timelineRef = await createCanonicalTimeline(
        projectId,
        {
          name: pending.name,
          timelineId: pending.timelineId,
          idempotencyKey: `astrid-timeline-create-${projectId}-${pending.timelineId}`,
        },
        new AstridRuntimeClient(),
      );
      await runtimeDiscovery.timelinesQuery.refetch();
      pendingAdditionalTimeline.current = null;
      if (timelineSelectionRef.current.projectId === projectId && timelineSelectionRef.current.timelineId === startingTimelineId && confirmRemountRef.current()) {
        setSearchParams(current => {
          if (current.get("project") !== projectId) return current;
          const next = new URLSearchParams(current); next.set("timeline", timelineRef); return next;
        }, { replace: true });
      }
      toast.success("Timeline ready");
    } catch (error) {
      const safeDetail =
        error instanceof ApiError
          ? `${error.status} ${error.code}: ${error.message.replace(/[\r\n]+/g, " ").slice(0, 120)}`
          : error instanceof RuntimeUnavailableError
            ? `${error.status ?? "unavailable"} ${error.causeCode ?? error.code}`
            : error instanceof Error
              ? error.name
              : "unknown error";
      if (timelineSelectionRef.current.projectId === projectId) setFirstTimelineError(safeDetail);
      toast.error(`Could not create timeline (${safeDetail}). Retry here.`);
    } finally {
      setCreatingFirstTimeline(false);
    }
  }, [
    creatingFirstTimeline,
    runtimeDiscovery.timelinesQuery,
    setSearchParams,
    projectId,
    timelineId,
    selectedProject,
    isSwitchBlockedBySave,
  ]);

  const handleSetPrimaryTimeline = useCallback(
    async (primaryTimelineId: string) => {
      if (!providerSelection?.dataProvider.setPrimaryTimeline || !timelines?.some(t => t.timeline_id === primaryTimelineId) || isSwitchBlockedBySave || settingPrimaryTimelineId !== null) {
        return;
      }
      const startingTimelineId = timelineId;
      setSettingPrimaryTimelineId(primaryTimelineId);
      try {
        await providerSelection.dataProvider.setPrimaryTimeline(primaryTimelineId);
        await Promise.all([
          runtimeDiscovery.projectsQuery.refetch(),
          runtimeDiscovery.timelinesQuery.refetch(),
        ]);
        if (timelineSelectionRef.current.projectId === projectId && timelineSelectionRef.current.timelineId === startingTimelineId && confirmRemountRef.current()) {
          setSearchParams(current => {
            if (current.get("project") !== projectId) return current;
            const next = new URLSearchParams(current); next.set("timeline", primaryTimelineId); return next;
          }, { replace: true });
        }
        toast.success("Primary timeline updated");
      } catch (error) {
        console.error("[video-editor] Failed to set primary timeline", error);
        toast.error("Failed to set the primary timeline");
      } finally {
        setSettingPrimaryTimelineId(null);
      }
    },
    [
      runtimeDiscovery.projectsQuery,
      runtimeDiscovery.timelinesQuery,
      providerSelection,
      timelines,
      isSwitchBlockedBySave,
      settingPrimaryTimelineId,
      projectId,
      timelineId,
      setSearchParams,
    ],
  );

  // Only an absent timeline is auto-selected. Explicit unknown or cross-project
  // selections remain errors instead of opening a different document.
  useEffect(() => {
    if (!selectedProject || timelineId || !timelines || runtimeDiscovery.timelinesQuery.error) return;
    const timeline = chooseRuntimeTimeline(selectedProject, timelines);
    if (!timeline) return;
    setSearchParams(current => {
      if (current.get("project") !== projectId || current.has("timeline")) return current;
      const next = new URLSearchParams(current); next.set("timeline", timeline.timeline_id); return next;
    }, { replace: true });
  }, [selectedProject, timelineId, timelines, runtimeDiscovery.timelinesQuery.error, projectId, setSearchParams]);

  const runtimePickerProps = {
    projects: (runtimeDiscovery.projectsQuery.data ?? []).map((p) => ({
      id: p.project_id,
      name: p.name || "Untitled project",
      detail: p.slug,
    })),
    timelines: (runtimeDiscovery.timelinesQuery.data ?? [])
      .map((t, index) => {
        const name =
          t.name?.trim() ||
          t.slug ||
          (!/^[0-9A-HJKMNP-TV-Z]{26}$/i.test(t.timeline_id)
            ? t.timeline_id
            : "Untitled timeline");
        const editAt = runtimeDiscovery.timelineEditQueries?.[index]?.data;
        const date = editAt ? new Date(editAt) : null;
        const validDate = date && Number.isFinite(date.getTime()) ? date : null;
        return {
          id: t.timeline_id,
          name,
          isPrimary: t.is_default,
          detail: validDate
            ? `edited ${formatDistanceToNowStrict(validDate, { addSuffix: true })}`
            : undefined,
          editTime: validDate?.getTime() ?? null,
        };
      })
      .filter((row, index) => {
        const timeline = runtimeDiscovery.timelinesQuery.data?.[index];
        return !!timeline && (!timeline.is_shot || timeline.timeline_id === timelineId);
      })
      .sort((a, b) => {
        if (a.editTime === null && b.editTime !== null) return 1;
        if (a.editTime !== null && b.editTime === null) return -1;
        if (a.editTime !== null && b.editTime !== null && a.editTime !== b.editTime)
          return b.editTime - a.editTime;
        return a.name.localeCompare(b.name);
      })
      .map(({ editTime: _editTime, ...row }) => row),
    projectId: projectId,
    timelineId: timelineId,
    projectName: selectedProject?.name,
    timelineName:
      selectedTimeline?.name?.trim() || selectedTimeline?.slug,
    projectsLoading:
      runtimeDiscovery.projectsQuery.isLoading,
    // The timeline list waits on the project list; a timeline named by the URL
    // is still loading until then, never "unavailable".
    timelinesLoading:
      (!!timelineId && runtimeDiscovery.projectsQuery.isLoading) ||
      (!!selectedProject && runtimeDiscovery.timelinesQuery.isLoading),
    projectsError: runtimeDiscovery.projectsQuery.error?.message,
    timelinesError: runtimeDiscovery.timelinesQuery.error?.message,
    onSelectProject: handleSelectProject,
    onSelectTimeline: handleSelectTimeline,
    onRenameTimeline: async (timelineId: string, name: string) => {
      if (!selectedProject || !timelines?.some(t => t.timeline_id === timelineId)) {
        throw new Error("This timeline is no longer available in the selected project.");
      }
      await new AstridRuntimeClient().renameTimeline(selectedProject.project_id, timelineId, name);
      await runtimeDiscovery.timelinesQuery.refetch();
    },
    onCreateTimeline: timelines?.some(t => !t.is_shot) ? handleCreateAdditionalTimeline : handleCreateFirstTimeline,
    creatingTimeline: creatingFirstTimeline,
    onSetPrimaryTimeline: handleSetPrimaryTimeline,
    settingPrimaryTimelineId,
    onRetry: () => void handleRuntimeRetry(),
    disabled: isSwitchBlockedBySave,
    onOpenChange: setSelectorsOpen,
  };
  const runtimeProjectControls = (
    <div className="flex min-w-0 max-w-full flex-wrap items-center gap-2">
      <img
        src="/astrid-favicon.svg"
        alt="Astrid"
        className="h-[30px] w-[30px] shrink-0"
        data-testid="astrid-project-row-logo"
        data-boot-mink-target=""
      />
      <ProjectTimelinePicker
        {...runtimePickerProps}
        showProjectLabel={false}
        showTimelineSelector={false}
      />
      <ProjectHeaderActions
        selectedProject={selectedProject}
        onProjectCreated={() => void runtimeDiscovery.projectsQuery.refetch()}
        onProjectUpdated={() => void runtimeDiscovery.projectsQuery.refetch()}
        disabled={isSwitchBlockedBySave || runtimeDiscovery.projectsQuery.isLoading}
        confirmNavigation={() => confirmRemountRef.current()}
      />
    </div>
  );
  const runtimeTimelineControls = (
    <>
      <ProjectTimelinePicker
        {...runtimePickerProps}
        showProjectSelector={false}
      />
    </>
  );

  const projectHeaderControls = runtimeProjectControls;
  const timelinePreviewControls = runtimeTimelineControls;
  const headerControlsRef = useRef(projectHeaderControls);
  headerControlsRef.current = projectHeaderControls;
  const headerIdentity = JSON.stringify([
    projectId, timelineId, projects, timelines,
    runtimeDiscovery.projectsQuery.isLoading, runtimeDiscovery.timelinesQuery.isLoading,
    runtimeDiscovery.projectsQuery.error?.message, runtimeDiscovery.timelinesQuery.error?.message,
    isSwitchBlockedBySave, extensionUnsaved, mountedSaveStatus, creatingFirstTimeline, settingPrimaryTimelineId,
    runtimeRetrying, nativeRecovery.retrying,
  ]);

  useEffect(() => {
    if (!hasGlobalHeader) {
      return;
    }
    globalHeaderSlot.setGlobalHeaderContent(headerControlsRef.current);
    return () => globalHeaderSlot.clearGlobalHeaderContent();
  }, [
    headerIdentity,
    globalHeaderSlot.clearGlobalHeaderContent,
    globalHeaderSlot.setGlobalHeaderContent,
    hasGlobalHeader,
  ]);

  // The same header is used for the loaded editor and every page-level
  // fallback, so switching between loading, empty, and editing states does
  // not change the navigation chrome.
  const selectorsHeader = !hasGlobalHeader ? (
    <AppHeader
      navigationMode={isHomeTool ? "tools" : "home"}
      onNavigate={undefined}
      navigationControls={projectHeaderControls}
      timelineName={null}
      showProjectControls={false}
    />
  ) : null;

  const discoveryError = runtimeDiscovery.projectsQuery.error ?? runtimeDiscovery.timelinesQuery.error;
  const recoveryError = runtimeConnectorError ?? discoveryError;
  const connectionFailed = !!(recoveryError || nativeRecoveryError);
  return (
    <div className="flex h-full w-full flex-col overflow-hidden bg-transparent">
      {connectionFailed && (
        <RuntimeConnectorRecoveryBanner
          error={recoveryError ?? new Error(nativeRecoveryError ?? "Workspace unavailable")}
          onRetry={handleRuntimeRetry}
          retrying={runtimeRetrying || nativeRecovery.retrying}
          projectId={projectId}
          timelineId={timelineId}
          connectionUrl={runtimeOrigin() || (typeof location === "undefined" ? null : location.origin)}
        />
      )}
      {providerSelection ? (
        <div className="min-h-0 flex-1 overflow-hidden">
          <VideoEditorProvider
            key={providerSelection.remountKey}
            dataProvider={pageDataProvider ?? providerSelection.dataProvider}
            projectId={providerSelection.projectId}
            projectSlug={providerSelection.projectSlug}
            timelineId={providerSelection.timelineId}
            timelineName={providerSelection.timelineName}
            userId={providerSelection.userId}
            onSaveStatusChange={setMountedSaveStatus}
            onPendingWorkChange={onPendingWorkChange}
            extensions={resolvedExtensions}
            timelineOverlaysEnabled={timelineOverlaysEnabled}
            extensionHostEnabled={extensionReleaseFlags.extensionHostEnabled}
            extensionReleaseRevision={extensionReleaseFlags.configurationRevision}
          >
            <AstridVideoEditorShell
              mode="full"
              timelineId={providerSelection.timelineId}
              onCreateTimeline={() => void handleCreateAdditionalTimeline()}
              headerNavigationControls={hasGlobalHeader ? undefined : projectHeaderControls}
              previewNavigationControls={timelinePreviewControls}
              navigationMode={isHomeTool ? "tools" : "home"}
              showHeader={!hasGlobalHeader}
            />
          </VideoEditorProvider>
        </div>
      ) : (
        <>
          {selectorsHeader}
          {workspaceSettling ? <span data-boot-hold="" hidden /> : (
            <>
              <div className="px-4 py-2">{timelinePreviewControls}</div>
              <div className="flex flex-1 items-center justify-center px-6">
                <Card className="w-full max-w-md">
                  <CardHeader>
                    <CardTitle>{projectMissing ? "Project not found"
                      : discoveryError ? selectedProject ? "Timelines unavailable" : "Workspace unavailable"
                      : !projectId ? projects?.length === 0 ? "No projects yet" : "Select a project"
                      : timelineMissing ? "Timeline not found"
                      : "No timeline yet"}</CardTitle>
                    <CardDescription>{projectMissing
                      ? `“${projectId}” is not available in this workspace. Choose an existing project or create one.`
                      : timelineMissing ? "The selected timeline is not available in this project. Choose another timeline."
                      : discoveryError ? discoveryError.message
                      : !projectId ? "Create a project with New project above, or choose an existing project."
                      : "Create a blank timeline for this project to open it in the editor."}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    {!projectId && projects?.length === 0 && <EmptyWorkspaceGuidance onRefresh={() => void runtimeDiscovery.projectsQuery.refetch()} />}
                    {selectedProject && !timelineId && !discoveryError && <Button
                      onClick={() => void handleCreateFirstTimeline()}
                      disabled={creatingFirstTimeline}
                    >{creatingFirstTimeline ? "Creating timeline…" : "Create first timeline"}</Button>}
                    {firstTimelineError && <p className="mt-3 text-xs text-destructive" role="alert">
                      Timeline setup failed ({firstTimelineError}). Retry here or check the connected Astrid Runtime.
                    </p>}
                    {discoveryError && <Button onClick={() => void handleRuntimeRetry()}>Retry workspace discovery</Button>}
                  </CardContent>
                </Card>
              </div>
            </>
          )}
        </>
      )}
    </div>
  );
}
