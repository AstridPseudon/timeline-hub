// @vitest-environment jsdom
import React from 'react';
import { act, cleanup, fireEvent, render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { RUNTIME_REQUEST_WAIT_MS } from '@/integrations/runtime/useRuntimeRequestWait.ts';
import VideoEditorPage from './VideoEditorPage.tsx';
import { assertNativeEditorConnection } from '@/integrations/astrid/nativeEditorConnection.ts';

const harness = vi.hoisted(() => ({
  mode: 'projects' as 'projects' | 'timelines',
  projectsPending: true,
  projectsError: null as Error | null,
  timelinesPending: false,
  projects: undefined as Array<Record<string, unknown>> | undefined,
  timelines: undefined as Array<Record<string, unknown>> | undefined,
  reconnect: vi.fn(),
  disabledIds: new Set<string>(),
}));

vi.mock('@/tools/video-editor/hooks/useRuntimeEditorDiscovery.ts', async () => {
  const ReactModule = await import('react');
  return {
    chooseRuntimeTimeline: (_project: unknown, rows: Array<Record<string, unknown>>) => rows[0],
    useRuntimeEditorDiscovery: ({ projectId }: { projectId: string | null }) => {
      const [, refresh] = ReactModule.useState(0);
      const project = harness.projects?.find((row) => row.project_id === projectId) ?? null;
      const reconnect = async () => {
        harness.reconnect();
        harness.projectsError = null;
        if (harness.mode === 'projects') {
          harness.projectsPending = false;
          harness.projects = [];
        } else {
          harness.timelinesPending = false;
          harness.timelines = [{ timeline_id: 'timeline-1', name: 'Main', slug: 'main' }];
        }
        refresh((value) => value + 1);
      };
      return {
        project,
        projectsQuery: {
          data: harness.projectsPending ? undefined : harness.projects,
          isSuccess: !harness.projectsPending,
          isLoading: harness.projectsPending,
          isFetching: harness.projectsPending,
          error: harness.projectsError,
          refetch: vi.fn(),
        },
        timelinesQuery: {
          data: project && !harness.timelinesPending ? harness.timelines : undefined,
          isSuccess: !!project && !harness.timelinesPending,
          isLoading: !!project && harness.timelinesPending,
          isFetching: !!project && harness.timelinesPending,
          error: null,
          refetch: vi.fn(),
        },
        timelineEditQueries: [],
        reconnect,
      };
    },
  };
});

vi.mock('@/tools/video-editor/hooks/useNativeEditorRecovery.ts', () => ({
  useNativeEditorRecovery: () => ({
    retrying: false,
    beginManualAttempt: () => ({ scope: 'test' }),
    completeRecovery: vi.fn(),
    reportFailure: vi.fn(),
  }),
}));
vi.mock('@/integrations/astrid/nativeEditorConnection.ts', () => ({ assertNativeEditorConnection: vi.fn(async () => undefined) }));
vi.mock('@/shared/hooks/useHomeNavigation.ts', () => ({ useHomeNavigation: () => ({ targetPath: '/tools/video-editor', navigateHome: vi.fn() }) }));
vi.mock('@/shared/lib/tooling/homeNavigation.ts', () => ({ isHomeToolPathActive: () => false }));
vi.mock('@/shared/contexts/AgentChatContext.tsx', () => ({ useOptionalAgentChatRegistry: () => null }));
vi.mock('@/shared/contexts/ToolPageHeaderContext.tsx', () => ({ useOptionalGlobalHeaderSlot: () => ({ hasProvider: false, setGlobalHeaderContent: vi.fn(), clearGlobalHeaderContent: vi.fn() }) }));
vi.mock('@/tools/video-editor/runtime/useExtensionLoaderWiring', () => ({ useExtensionLoaderWiring: () => ({ resolvedExtensions: [], diagnostics: {} }) }));
vi.mock('@/tools/video-editor/runtime/builtInExtensionEnablement.ts', () => ({
  getSnapshot: () => harness.disabledIds,
  subscribe: () => () => undefined,
  setBuiltInExtensionEnabled: vi.fn(),
}));
vi.mock('@/tools/video-editor/dev/localExtensions.ts', () => ({ devLocalExtensions: [] }));
vi.mock('@/tools/video-editor/dev/transcript-lane/fixtureProvider.ts', () => ({ TRANSCRIPT_LANE_FIXTURE_PARAM: 'transcriptLaneFixture', withTranscriptFixture: (value: unknown) => value }));
vi.mock('@/tools/video-editor/runtime/extensionReleaseControls.ts', () => ({ selectReviewedExtensions: (items: unknown[]) => items }));
vi.mock('@/app/localTestRuntime.ts', () => ({ publishLocalTestExtensionDiagnostics: vi.fn() }));
vi.mock('@/shared/state/editorTourStore.ts', () => ({
  useEditorTour: (selector: (state: { runId: number }) => unknown) => selector({ runId: 0 }),
  useEditorTourRunning: () => false,
}));
vi.mock('@/tools/video-editor/tour/runner/useEditorTourHost.ts', () => ({ useEditorTourHost: vi.fn() }));
vi.mock('@/tools/video-editor/tour/timeline/editorTourSlot.tsx', () => ({ EditorTourSlot: () => null }));
vi.mock('@/tools/video-editor/tour/timeline/EditorTourTimelineDriver.tsx', () => ({ EditorTourTimelineDriver: () => null }));
vi.mock('@/tools/video-editor/tour/timeline/tourDataProvider.ts', () => ({ createEditorTourDataProvider: () => ({}) }));
vi.mock('@/tools/video-editor/tour/timeline/tourStages.ts', () => ({ EDITOR_TOUR_PROJECT_NAME: 'Tour', EDITOR_TOUR_TIMELINE_ID: 'tour-timeline', EDITOR_TOUR_TIMELINE_NAME: 'Tour' }));
vi.mock('@/integrations/runtime/dataProvider.ts', () => ({ RuntimeDataProvider: class { kind = 'runtime'; reconnect = vi.fn(async () => undefined); } }));
vi.mock('@/tools/video-editor/contexts/VideoEditorProvider.tsx', () => ({ VideoEditorProvider: ({ children }: { children: React.ReactNode }) => <div data-testid="video-editor-provider">{children}</div> }));
vi.mock('@/tools/video-editor/components/AstridVideoEditorShell.tsx', () => ({ AstridVideoEditorShell: () => <div>Editor mounted</div> }));
vi.mock('@/shared/components/AppHeader.tsx', () => ({ AppHeader: () => <header /> }));
vi.mock('@/shared/components/ProjectTimelineSelectors.tsx', () => ({ ProjectTimelinePicker: () => null }));
vi.mock('@/shared/components/ProjectHeaderActions.tsx', () => ({ ProjectHeaderActions: () => null }));
vi.mock('@/shared/components/RuntimeConnection/EmptyWorkspaceGuidance.tsx', () => ({ EmptyWorkspaceGuidance: () => <div>Empty workspace help</div> }));
vi.mock('@/shared/components/RuntimeConnection/RuntimeConnectorRecoveryBanner.tsx', () => ({
  RuntimeConnectorRecoveryBanner: ({ onRetry }: { onRetry: () => void }) => <button onClick={onRetry}>Retry Runtime connection</button>,
}));
vi.mock('@/integrations/runtime/client.ts', () => ({ AstridRuntimeClient: class {}, RuntimeUnavailableError: class extends Error {}, RuntimeAuthenticationError: class extends Error {} }));
vi.mock('@/integrations/runtime/createDefaultTimeline.ts', () => ({ ensureProjectHasTimeline: vi.fn(), createCanonicalTimeline: vi.fn() }));
vi.mock('@/integrations/runtime/generated.ts', () => ({ ApiError: class extends Error {} }));
vi.mock('@/integrations/runtime/connection.ts', () => ({ runtimeOrigin: () => null }));
vi.mock('@/shared/lib/taskCreation/ids.ts', () => ({ generateUUID: () => 'generated-id' }));
vi.mock('@/shared/components/ui/toast.tsx', () => ({ toast: { success: vi.fn(), error: vi.fn() } }));

function PageHarness({ entry }: { entry: string }) {
  return <MemoryRouter initialEntries={[entry]} future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
    <VideoEditorPage />
  </MemoryRouter>;
}

describe('VideoEditorPage workspace settling', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    harness.mode = 'projects';
    harness.projectsPending = true;
    harness.projectsError = null;
    harness.timelinesPending = false;
    harness.projects = undefined;
    harness.timelines = undefined;
    harness.reconnect.mockClear();
    vi.mocked(assertNativeEditorConnection).mockClear();
  });
  afterEach(() => {
    cleanup();
    vi.useRealTimers();
  });

  it('releases the boot hold after stalled project discovery and retries into authoritative empty workspace', async () => {
    render(<PageHarness entry="/tools/video-editor" />);

    expect(document.querySelector('[data-boot-hold]')).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Opening your workspace…' })).toBeInTheDocument();
    expect(screen.queryByText('No projects yet')).toBeNull();
    act(() => vi.advanceTimersByTime(RUNTIME_REQUEST_WAIT_MS));
    expect(screen.getByRole('heading', { name: 'Still waiting for your workspace' })).toBeInTheDocument();
    expect(document.querySelector('[data-boot-hold]')).toBeNull();

    fireEvent.click(screen.getByRole('button', { name: 'Retry workspace discovery' }));
    expect(harness.reconnect).toHaveBeenCalledOnce();
    expect(screen.getByText('No projects yet')).toBeInTheDocument();
    expect(screen.getByText('Empty workspace help')).toBeInTheDocument();
    expect(document.querySelector('[data-boot-hold]')).toBeNull();
  });

  it('releases the boot hold for stalled timeline discovery and retry mounts the verified editor', async () => {
    harness.mode = 'timelines';
    harness.projectsPending = false;
    harness.projects = [{ project_id: 'project-1', slug: 'project-1', name: 'Project One', metadata: {} }];
    harness.timelinesPending = true;
    render(<PageHarness entry="/tools/video-editor?project=project-1&timeline=timeline-1" />);

    expect(screen.getByRole('heading', { name: 'Opening your workspace…' })).toBeInTheDocument();
    expect(screen.queryByText('No timeline yet')).toBeNull();
    act(() => vi.advanceTimersByTime(RUNTIME_REQUEST_WAIT_MS));
    expect(screen.getByRole('heading', { name: 'Still waiting for your workspace' })).toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: 'Retry workspace discovery' }));
    expect(harness.reconnect).toHaveBeenCalledOnce();
    expect(screen.getByTestId('video-editor-provider')).toBeInTheDocument();
    expect(screen.getByText('Editor mounted')).toBeInTheDocument();
    expect(document.querySelector('[data-boot-hold]')).toBeNull();
  });

  it('routes a discovery-error banner retry through cancellable discovery', async () => {
    harness.projectsPending = false;
    harness.projectsError = new Error('Workspace did not answer');
    render(<PageHarness entry="/tools/video-editor" />);

    fireEvent.click(screen.getByRole('button', { name: 'Retry Runtime connection' }));
    expect(harness.reconnect).toHaveBeenCalledOnce();
    expect(assertNativeEditorConnection).not.toHaveBeenCalled();
    expect(screen.getByText('No projects yet')).toBeInTheDocument();
  });
});
