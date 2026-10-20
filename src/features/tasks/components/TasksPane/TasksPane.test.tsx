// @vitest-environment jsdom
import React from 'react';
import { fireEvent, render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { TasksPane } from './TasksPane';

const useLocationMock = vi.fn();
const useTasksPaneControllerMock = vi.fn();
const useAgentChatActionsMock = vi.fn();
const useOptionalAgentChatBridgeMock = vi.fn();
const usePanesStoreMock = vi.fn();
const openPaneMock = vi.fn();
const toggleLockMock = vi.fn();
const handlePaneEnterMock = vi.fn();
const handlePaneLeaveMock = vi.fn();
const closePaneMock = vi.fn();
const handleFilterChangeMock = vi.fn();
const handleTaskTypeChangeMock = vi.fn();
const handlePageChangeMock = vi.fn();
const handleCancelAllPendingMock = vi.fn();
const setProjectScopeMock = vi.fn();
const setMobileActiveTaskIdMock = vi.fn();
const setIsTasksPaneOpenProgrammaticMock = vi.fn();
const setIsTasksPaneLockedMock = vi.fn();
const setActiveTaskIdMock = vi.fn();
const setLightboxSelectedShotIdMock = vi.fn();
const handleOpenImageLightboxMock = vi.fn();
const handleOpenVideoLightboxMock = vi.fn();
const handleOpenRuntimeTaskOutputMock = vi.fn();
const handleCloseLightboxMock = vi.fn();
const handleOpenExternalGenerationMock = vi.fn();
const handleAddToShotMock = vi.fn();
const handleAddToShotWithoutPositionMock = vi.fn();
const handleOptimisticPositionedMock = vi.fn();
const handleOptimisticUnpositionedMock = vi.fn();
const useTasksPaneSlidingPaneOptionsMock = vi.fn();

let paneControlProps: any = null;
let runtimeListProps: any = null;
let runtimeDockProps: any = null;
let mediaLightboxProps: any = null;
let lightboxOpen = false;
let runtimeRecoverySource: unknown;

vi.mock('react-dom', async () => {
  const actual = await vi.importActual<typeof import('react-dom')>('react-dom');
  return {
    ...actual,
    createPortal: (node: React.ReactNode) => node,
  };
});

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual<typeof import('react-router-dom')>('react-router-dom');
  return {
    ...actual,
    useLocation: () => useLocationMock(),
  };
});

vi.mock('@/shared/lib/debug/debugRendering', () => ({
  useRenderLogger: vi.fn(),
}));

vi.mock('@/shared/dev/useRenderBudget', () => ({
  useRenderBudget: vi.fn(),
}));

vi.mock('@/shared/components/ui/contracts/cn', () => ({
  cn: (...parts: Array<string | false | null | undefined>) => parts.filter(Boolean).join(' '),
}));

vi.mock('@/shared/components/ui/button', () => ({
  Button: ({ children, ...props }: any) => <button type="button" {...props}>{children}</button>,
}));

vi.mock('@/shared/components/ui/tooltip', () => ({
  Tooltip: ({ children }: any) => <>{children}</>,
  TooltipContent: ({ children }: any) => <>{children}</>,
  TooltipTrigger: ({ children }: any) => <>{children}</>,
}));

vi.mock('@/shared/components/PaneControlTab', () => ({
  PaneControlTab: (props: any) => {
    paneControlProps = props;
    const splitButton = props.actions?.splitButton;
    return (
      <div data-testid="pane-control-tab">
        <span data-testid="split-available">{String(Boolean(splitButton))}</span>
        {splitButton ? (
          <button type="button" onClick={splitButton.primary.onClick}>
            {splitButton.primary.ariaLabel}
          </button>
        ) : null}
      </div>
    );
  },
}));

vi.mock('@/shared/contexts/AgentChatContext', () => ({
  useOptionalAgentChatBridge: (...args: unknown[]) => useOptionalAgentChatBridgeMock(...args),
  useAgentChatActions: (...args: unknown[]) => useAgentChatActionsMock(...args),
}));

vi.mock('@/tools/video-editor/components/AgentChat', () => ({
  AgentChatPanel: ({ isExpanded, onSessionSelectorOpenChange }: {
    isExpanded?: boolean;
    onSessionSelectorOpenChange?: (open: boolean) => void;
  }) => (
    <div data-testid="agent-chat-panel" data-expanded={String(Boolean(isExpanded))}>
      <button type="button" onClick={() => onSessionSelectorOpenChange?.(true)}>Open chat selector</button>
      <button type="button" onClick={() => onSessionSelectorOpenChange?.(false)}>Close chat selector</button>
    </div>
  ),
}));

vi.mock('@/tools/video-editor/hooks/useAgentSession', () => ({
  useProjectAgentTaskLinks: () => ({ data: [] }),
}));

vi.mock('@/shared/contexts/ProjectContext', () => ({
  useProjectSelectionContext: () => ({ selectedProjectId: 'project-1' }),
  useProjectCrudContext: () => ({ projects: [{ id: 'project-1', name: 'Project 1', createdAt: '2026-05-01T00:00:00.000Z' }] }),
}));

vi.mock('@/shared/contexts/IncomingTasksContext', () => ({
  useIncomingTasks: () => ({ incomingTasks: [], cancelAllIncoming: vi.fn() }),
}));

vi.mock('@/shared/components/ProcessingWarnings', () => ({
  TasksPaneProcessingWarning: () => <div data-testid="processing-warning" />,
}));

vi.mock('@/shared/hooks/layout/useBottomOffset', () => ({
  useBottomOffset: () => 0,
}));

vi.mock('@/domains/media-lightbox/MediaLightbox', () => ({
  MediaLightbox: (props: any) => {
    mediaLightboxProps = props;
    return <div data-testid="media-lightbox" />;
  },
}));

vi.mock('@/shared/contexts/ShotsContext', () => ({
  useShots: () => ({ shots: [] }),
}));

vi.mock('@/shared/hooks/shots/useLastAffectedShot', () => ({
  useLastAffectedShot: () => ({ lastAffectedShotId: null }),
}));

vi.mock('@/shared/state/selectionStore', () => ({
  useCurrentShot: () => ({ currentShotId: null }),
}));

vi.mock('@/shared/components/panes/usePaneInteractionLifecycle', () => ({
  usePaneInteractionLifecycle: () => ({ isPointerEventsEnabled: true }),
}));

vi.mock('@/shared/components/panes/PaneBackdrop', () => ({
  PaneBackdrop: () => null,
}));

vi.mock('@/shared/components/ui/select', () => ({
  Select: ({ children }: any) => <div>{children}</div>,
  SelectContent: ({ children }: any) => <div>{children}</div>,
  SelectItem: ({ children }: any) => <div>{children}</div>,
  SelectTrigger: ({ children }: any) => <button type="button">{children}</button>,
  SelectValue: ({ placeholder }: any) => <span>{placeholder ?? 'value'}</span>,
  SelectSeparator: () => <div data-testid="select-separator" />,
}));

vi.mock('./TaskList', () => ({
  TaskList: () => <div data-testid="task-list" />,
}));

vi.mock('./RuntimeTaskList', () => ({
  RuntimeTaskList: (props: any) => {
    runtimeListProps = props;
    const { tasks } = props;
    return (
    <div data-testid="runtime-task-list" data-runtime-task-id={tasks[0]?.task_id ?? ''}>
      {tasks.length === 0 ? 'No tasks yet' : null}
    </div>
    );
  },
}));

vi.mock('./RuntimeActivityDock', () => ({
  RuntimeActivityDock: (props: any) => {
    runtimeDockProps = props;
    return <div data-testid="runtime-activity-dock" data-runtime-activity-dock="true" onMouseLeave={props.onTemporaryHistoryLeave} onBlur={props.onTemporaryHistoryLeave}>
    <button type="button" aria-label={props.isPinned ? 'Stop keeping tasks open' : 'Keep tasks open'} title={props.isPinned ? 'Stop keeping tasks open' : 'Keep tasks open'} aria-pressed={props.isPinned} onClick={props.onTogglePinned}>Toggle activity history</button>
    <button type="button" aria-label={props.isHistoryOpen ? 'Stop peeking at tasks' : 'Peek at tasks'} title={props.isHistoryOpen ? 'Stop peeking at tasks' : 'Peek at tasks'} aria-expanded={props.isHistoryOpen} onClick={props.onToggleHistory}>Toggle task history</button>
    <button type="button" onClick={props.onOpenHistory}>Open activity history</button>
  </div>;
  },
}));

vi.mock('./components/PaginationControls', () => ({
  PaginationControls: () => <div data-testid="pagination-controls" />,
}));

vi.mock('./hooks/useTasksLightbox', () => ({
  useTasksLightbox: () => ({
    lightboxData: lightboxOpen ? { task: { id: 'task-output' }, runtimeRecoverySource } : null,
    lightboxSelectedShotId: null,
    setLightboxSelectedShotId: setLightboxSelectedShotIdMock,
    taskDetailsData: null,
    lightboxProps: lightboxOpen ? { media: { id: 'generation-output' } } : null,
    handleOpenImageLightbox: handleOpenImageLightboxMock,
    handleOpenVideoLightbox: handleOpenVideoLightboxMock,
    handleOpenRuntimeTaskOutput: handleOpenRuntimeTaskOutputMock,
    handleCloseLightbox: handleCloseLightboxMock,
    handleOpenExternalGeneration: handleOpenExternalGenerationMock,
  }),
}));

vi.mock('./hooks/useShotActions', () => ({
  useShotActions: () => ({
    optimisticPositionedIds: [],
    optimisticUnpositionedIds: [],
    handleAddToShot: handleAddToShotMock,
    handleAddToShotWithoutPosition: handleAddToShotWithoutPositionMock,
    handleOptimisticPositioned: handleOptimisticPositionedMock,
    handleOptimisticUnpositioned: handleOptimisticUnpositionedMock,
  }),
}));

vi.mock('./hooks/useTasksPaneController', () => ({
  useTasksPaneController: (...args: unknown[]) => useTasksPaneControllerMock(...args),
}));

const legacyControllerState = {
    selectedFilter: 'Processing',
    selectedTaskType: null,
    projectScope: 'current',
    currentPage: 1,
    mobileActiveTaskId: null,
    setProjectScope: setProjectScopeMock,
    setMobileActiveTaskId: setMobileActiveTaskIdMock,
    handleFilterChange: handleFilterChangeMock,
    handleTaskTypeChange: handleTaskTypeChangeMock,
    handlePageChange: handlePageChangeMock,
    handleCancelAllPending: handleCancelAllPendingMock,
    isCancelAllPending: false,
    paginatedData: [],
    isPaginatedLoading: false,
    displayStatusCounts: {
      recentSuccesses: 0,
      recentFailures: 0,
    },
    isStatusCountsDegraded: false,
    failedStatusQueries: 0,
    taskTypeOptions: [],
    totalTasks: 0,
    totalPages: 1,
    cancellableTaskCount: 2,
    isAllProjectsMode: false,
    projectNameMap: {},
    isRuntimeMode: false,
    runtimeTaskData: undefined,
    runtimeActivityTasks: [],
    runtimeTaskError: null,
    runtimeTaskActionError: null,
    runtimeTaskActions: {
      cancelTask: vi.fn(),
      retryTask: vi.fn(),
      isTaskActionPending: vi.fn().mockReturnValue(false),
      exportManagedOutput: vi.fn(),
      isExportTaskPending: vi.fn().mockReturnValue(false),
    },
};

vi.mock('./hooks/useTasksPaneSlidingPane', () => ({
  useTasksPaneSlidingPane: (options: any) => {
    useTasksPaneSlidingPaneOptionsMock(options);
    return {
      isLocked: false,
      isOpen: true,
      toggleLock: toggleLockMock,
      openPane: openPaneMock,
      paneProps: {},
      transformClass: '',
      handlePaneEnter: handlePaneEnterMock,
      handlePaneLeave: handlePaneLeaveMock,
      showBackdrop: false,
      closePane: closePaneMock,
    };
  },
}));

vi.mock('@/shared/state/panesStore', () => ({
  usePanesStore: (selector: (state: any) => unknown) => selector(usePanesStoreMock()),
}));

function renderTasksPane() {
  return render(<TasksPane onOpenSettings={vi.fn()} />);
}

describe('TasksPane', () => {
  beforeEach(() => {
    paneControlProps = null;
    runtimeListProps = null;
    runtimeDockProps = null;
    mediaLightboxProps = null;
    lightboxOpen = false;
    runtimeRecoverySource = undefined;
    Object.defineProperty(window, 'localStorage', {
      configurable: true,
      value: {
        clear: vi.fn(),
        getItem: vi.fn().mockReturnValue(null),
        setItem: vi.fn(),
        removeItem: vi.fn(),
      },
    });
    window.localStorage.clear();
    useLocationMock.mockReset();
    useAgentChatActionsMock.mockReset();
    useOptionalAgentChatBridgeMock.mockReset();
    useTasksPaneSlidingPaneOptionsMock.mockReset();
    openPaneMock.mockReset();
    toggleLockMock.mockReset();
    handlePaneEnterMock.mockReset();
    handlePaneLeaveMock.mockReset();
    closePaneMock.mockReset();
    handleFilterChangeMock.mockReset();
    handleTaskTypeChangeMock.mockReset();
    handlePageChangeMock.mockReset();
    handleCancelAllPendingMock.mockReset();
    setProjectScopeMock.mockReset();
    setMobileActiveTaskIdMock.mockReset();
    setIsTasksPaneOpenProgrammaticMock.mockReset();
    setIsTasksPaneLockedMock.mockReset();
    setActiveTaskIdMock.mockReset();
    setLightboxSelectedShotIdMock.mockReset();
    handleOpenImageLightboxMock.mockReset();
    handleOpenVideoLightboxMock.mockReset();
    handleOpenRuntimeTaskOutputMock.mockReset();
    handleCloseLightboxMock.mockReset();
    handleOpenExternalGenerationMock.mockReset();
    handleAddToShotMock.mockReset();
    handleAddToShotWithoutPositionMock.mockReset();
    handleOptimisticPositionedMock.mockReset();
    handleOptimisticUnpositionedMock.mockReset();
    useLocationMock.mockReturnValue({ pathname: '/tools/video-editor' });
    useOptionalAgentChatBridgeMock.mockReturnValue(null);
    useTasksPaneControllerMock.mockReset();
    useTasksPaneControllerMock.mockReturnValue(legacyControllerState);
    usePanesStoreMock.mockReturnValue({
      isTasksPaneLocked: false,
      setIsTasksPaneLocked: setIsTasksPaneLockedMock,
      tasksPaneWidth: 360,
      activeTaskId: null,
      setActiveTaskId: setActiveTaskIdMock,
      isTasksPaneOpen: true,
      setIsTasksPaneOpen: setIsTasksPaneOpenProgrammaticMock,
    });
    vi.stubGlobal('requestAnimationFrame', vi.fn((callback: FrameRequestCallback) => {
      callback(0);
      return 1;
    }));
  });

  it('defaults to the status strip above expanded chat and peeks without remounting chat', () => {
    const { container } = renderTasksPane();
    const chat = screen.getByTestId('agent-chat-panel');
    const strip = container.querySelector('[data-task-peek-surface="header"]')!;
    expect(chat).toHaveAttribute('data-expanded', 'true');
    expect(screen.queryByTestId('task-list')).toBeNull();
    expect(screen.getAllByRole('button', { name: 'Lock tasks open' })[0]).toBeTruthy();
    expect(paneControlProps.actions.thirdButton.ariaLabel).toBe('Open Action pane (2 active tasks)');

    fireEvent.mouseEnter(strip);
    expect(screen.getByTestId('task-list')).toBeTruthy();
    const taskPanel = container.querySelector('[data-task-peek-surface="tasks"]')!;
    expect(taskPanel.classList.contains('relative')).toBe(true);
    expect(taskPanel.classList.contains('absolute')).toBe(false);
    expect(taskPanel.classList.contains('h-[calc(50%_-_5rem)]')).toBe(true);
    expect(chat).toHaveAttribute('data-expanded', 'false');
    fireEvent.mouseLeave(strip, { relatedTarget: taskPanel });
    fireEvent.mouseEnter(taskPanel);
    expect(screen.getByTestId('task-list')).toBeTruthy();
    const popupView = render(<div role="listbox" />);
    const popup = screen.getByRole('listbox');
    fireEvent.mouseLeave(taskPanel, { relatedTarget: popup });
    expect(screen.getByTestId('task-list')).toBeTruthy();
    popupView.unmount();
    fireEvent.mouseLeave(taskPanel, { relatedTarget: chat });
    expect(screen.queryByTestId('task-list')).toBeNull();
    expect(screen.getByTestId('agent-chat-panel')).toBe(chat);
    expect(chat).toHaveAttribute('data-expanded', 'true');
    expect(toggleLockMock).not.toHaveBeenCalled();
  });

  it('status clicks and keyboard focus peek tasks; pinning restores the persistent split', () => {
    renderTasksPane();
    const processing = screen.getByRole('button', { name: 'Show processing tasks (2)' });
    fireEvent.focus(processing);
    expect(screen.getByTestId('task-list')).toBeTruthy();
    fireEvent.blur(processing, { relatedTarget: document.body });
    expect(screen.queryByTestId('task-list')).toBeNull();
    for (const filter of ['Processing', 'Succeeded', 'Failed']) {
      fireEvent.click(screen.getByRole('button', { name: new RegExp(`Show ${filter.toLowerCase()} tasks`) }));
      expect(handleFilterChangeMock).toHaveBeenLastCalledWith(filter);
      expect(screen.getByTestId('task-list')).toBeTruthy();
    }
    fireEvent.click(screen.getAllByRole('button', { name: 'Lock tasks open' })[0]);
    expect(screen.getByTestId('agent-chat-panel')).toHaveAttribute('data-expanded', 'false');
    expect(screen.getByTestId('task-list')).toBeTruthy();
    expect(window.localStorage.setItem).toHaveBeenCalledWith('tasksPane:expandedHalf', 'split');
  });

  it('the sole header lock reserves half the pane including its header, and unlock restores compact mode', () => {
    const { container } = renderTasksPane();
    const chat = screen.getByTestId('agent-chat-panel');
    fireEvent.click(screen.getByRole('button', { name: 'Show processing tasks (2)' }));
    const panel = container.querySelector<HTMLElement>('[data-task-peek-surface="tasks"]')!;
    const header = container.querySelector<HTMLElement>('[data-task-peek-surface="header"]')!;
    // The 5rem header is included in the task half, not added on top of it.
    expect(header.classList.contains('h-20')).toBe(true);
    expect(panel.classList.contains('h-[calc(50%_-_5rem)]')).toBe(true);
    expect(screen.getAllByRole('button', { name: 'Lock tasks open' })).toHaveLength(1);
    expect(within(panel).queryByRole('button', { name: 'Lock tasks open' })).toBeNull();
    const lock = within(header).getByRole('button', { name: 'Lock tasks open' });
    expect(lock.className).toContain('group-hover/tasks-header:opacity-100');
    expect(lock.className).toContain('focus-visible:opacity-100');
    fireEvent.click(lock);
    expect(panel.classList.contains('h-[calc(50%_-_5rem)]')).toBe(true);
    expect(panel.classList.contains('absolute')).toBe(false);
    fireEvent.mouseLeave(panel, { relatedTarget: chat });
    expect(screen.getByTestId('task-list')).toBeTruthy();
    expect(screen.getByTestId('agent-chat-panel')).toBe(chat);
    expect(within(header).getByRole('button', { name: 'Unlock tasks' })).toHaveAttribute('aria-pressed', 'true');
    expect(screen.queryByRole('button', { name: 'Expand chat to fill pane' })).toBeNull();
    expect(screen.queryByRole('button', { name: 'Expand tasks to fill pane' })).toBeNull();
    fireEvent.click(within(header).getByRole('button', { name: 'Unlock tasks' }));
    expect(screen.queryByTestId('task-list')).toBeNull();
    expect(screen.getByTestId('agent-chat-panel')).toBe(chat);
    expect(window.localStorage.setItem).toHaveBeenCalledWith('tasksPane:expandedHalf', 'chat');
  });

  it('migrates the old tasks-full preference into pinned half-height with chat visible', () => {
    (window.localStorage.getItem as ReturnType<typeof vi.fn>).mockImplementation((key: string) => key === 'tasksPane:expandedHalf' ? 'tasks' : null);
    renderTasksPane();
    expect(screen.getByTestId('agent-chat-panel')).toBeTruthy();
    expect(screen.getByTestId('task-list')).toBeTruthy();
    expect(window.localStorage.setItem).toHaveBeenCalledWith('tasksPane:expandedHalf', 'split');
  });

  it('preserves an explicit split preference and shows tasks on non-tool routes', () => {
    (window.localStorage.getItem as ReturnType<typeof vi.fn>).mockImplementation((key: string) => key === 'tasksPane:expandedHalf' ? 'split' : null);
    const view = renderTasksPane();
    expect(screen.getByTestId('agent-chat-panel')).toHaveAttribute('data-expanded', 'false');
    expect(screen.getByTestId('task-list')).toBeTruthy();
    view.unmount();
    useLocationMock.mockReturnValue({ pathname: '/projects' });
    (window.localStorage.getItem as ReturnType<typeof vi.fn>).mockReturnValue('chat');
    renderTasksPane();
    expect(screen.queryByTestId('agent-chat-panel')).toBeNull();
    expect(screen.getByTestId('task-list')).toBeTruthy();
  });

  it('lets the arrow open and close empty task history independently from the persistent lock', async () => {
    useLocationMock.mockReturnValue({
      pathname: '/tools/video-editor',
      search: '?runtime=1&runtimeProject=runtime-project&runtimeTimeline=timeline-1',
    });
    useTasksPaneControllerMock.mockReturnValue({
      ...legacyControllerState,
      isRuntimeMode: true,
      runtimeActivityTasks: [],
      runtimeTaskData: { tasks: [], total: 0, totalPages: 0 },
      runtimeTaskActions: {
        cancelTask: vi.fn(), retryTask: vi.fn(), isTaskActionPending: vi.fn().mockReturnValue(false),
        exportManagedOutput: vi.fn(), isExportTaskPending: vi.fn().mockReturnValue(false),
      },
    });

    renderTasksPane();
    const dock = screen.getByTestId('runtime-activity-dock');
    expect(screen.queryByTestId('runtime-task-list')).toBeNull();
    fireEvent.mouseEnter(dock);
    expect(screen.queryByTestId('runtime-task-list')).toBeNull();
    const user = userEvent.setup();
    await user.click(screen.getByRole('button', { name: 'Peek at tasks' }));
    expect(screen.getByTestId('runtime-task-history-empty')).toBeInTheDocument();
    expect(screen.queryByTestId('runtime-task-list')).toBeNull();
    expect(screen.getByRole('button', { name: 'Stop peeking at tasks' })).toHaveAttribute('aria-expanded', 'true');
    expect(screen.getByRole('button', { name: 'Stop peeking at tasks' })).toHaveFocus();

    const taskArea = screen.getByTestId('runtime-task-history-empty').closest('[data-task-peek-surface="tasks"]')!;
    const chat = screen.getByTestId('agent-chat-panel');
    fireEvent.mouseLeave(dock, { relatedTarget: taskArea });
    expect(screen.getByTestId('runtime-task-history-empty')).toBeInTheDocument();
    fireEvent.mouseLeave(taskArea, { relatedTarget: chat });
    expect(screen.queryByTestId('runtime-task-history-empty')).toBeNull();
    expect(screen.getByRole('button', { name: 'Peek at tasks' })).toHaveFocus();

    fireEvent.click(screen.getByRole('button', { name: 'Peek at tasks' }));
    expect(screen.getByTestId('runtime-task-history-empty')).toBeInTheDocument();
    fireEvent.mouseLeave(dock, { relatedTarget: document.body });
    expect(screen.queryByTestId('runtime-task-history-empty')).toBeNull();

    fireEvent.click(screen.getByRole('button', { name: 'Peek at tasks' }));
    expect(screen.getByTestId('runtime-task-history-empty')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Stop peeking at tasks' }));
    expect(screen.queryByTestId('runtime-task-history-empty')).toBeNull();
    expect(screen.getByRole('button', { name: 'Peek at tasks' })).toHaveAttribute('aria-expanded', 'false');

    fireEvent.click(screen.getByRole('button', { name: 'Keep tasks open' }));
    expect(screen.getByTestId('runtime-task-history-empty')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Stop keeping tasks open' })).toHaveAttribute('aria-pressed', 'true');
    fireEvent.mouseLeave(dock, { relatedTarget: chat });
    expect(screen.getByTestId('runtime-task-history-empty')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Stop peeking at tasks' }));
    expect(screen.queryByTestId('runtime-task-history-empty')).toBeNull();
    expect(screen.getByRole('button', { name: 'Stop keeping tasks open' })).toHaveAttribute('aria-pressed', 'true');
    fireEvent.click(screen.getByRole('button', { name: 'Peek at tasks' }));
    fireEvent.click(screen.getByRole('button', { name: 'Stop keeping tasks open' }));
    expect(screen.getByTestId('runtime-task-history-empty')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Keep tasks open' })).toHaveAttribute('aria-pressed', 'false');
  });

  it('ignores old split and transient-open preferences when initializing Runtime history', () => {
    (window.localStorage.getItem as ReturnType<typeof vi.fn>).mockImplementation((key: string) => {
      if (key === 'tasksPane:expandedHalf') return 'split';
      if (key === 'tasksPane:runtimeHistoryOpen') return 'open';
      return null;
    });
    useLocationMock.mockReturnValue({
      pathname: '/tools/video-editor',
      search: '?runtime=1&runtimeProject=runtime-project&runtimeTimeline=timeline-1',
    });
    useTasksPaneControllerMock.mockReturnValue({
      ...legacyControllerState,
      isRuntimeMode: true,
      runtimeActivityTasks: [],
      runtimeTaskData: { tasks: [], total: 0, totalPages: 0 },
      runtimeTaskActions: {
        cancelTask: vi.fn(), retryTask: vi.fn(), isTaskActionPending: vi.fn().mockReturnValue(false),
        exportManagedOutput: vi.fn(), isExportTaskPending: vi.fn().mockReturnValue(false),
      },
    });

    renderTasksPane();

    expect(screen.getByTestId('runtime-activity-dock')).toBeInTheDocument();
    expect(screen.queryByTestId('runtime-task-list')).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /show (processing|succeeded|failed) tasks/i })).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Keep tasks open' })).toHaveAttribute('aria-pressed', 'false');
    expect(window.localStorage.setItem).toHaveBeenCalledWith('tasksPane:runtimeHistoryPinned', 'unpinned');
  });

  it('restores a pinned-history preference and leaves visibility to the arrow when unlocked', () => {
    (window.localStorage.getItem as ReturnType<typeof vi.fn>).mockImplementation((key: string) =>
      key === 'tasksPane:runtimeHistoryPinned' ? 'pinned' : null,
    );
    useLocationMock.mockReturnValue({
      pathname: '/tools/video-editor',
      search: '?runtime=1&runtimeProject=runtime-project&runtimeTimeline=timeline-1',
    });
    useTasksPaneControllerMock.mockReturnValue({
      ...legacyControllerState,
      isRuntimeMode: true,
      runtimeActivityTasks: [],
      runtimeTaskData: { tasks: [], total: 0, totalPages: 0 },
      runtimeTaskActions: {
        cancelTask: vi.fn(), retryTask: vi.fn(), isTaskActionPending: vi.fn().mockReturnValue(false),
        exportManagedOutput: vi.fn(), isExportTaskPending: vi.fn().mockReturnValue(false),
      },
    });

    renderTasksPane();
    expect(screen.getByTestId('runtime-task-history-empty')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Stop keeping tasks open' })).toHaveAttribute('aria-pressed', 'true');
    fireEvent.click(screen.getByRole('button', { name: 'Stop keeping tasks open' }));

    expect(screen.getByTestId('runtime-task-history-empty')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Stop peeking at tasks' }));
    expect(screen.queryByTestId('runtime-task-list')).not.toBeInTheDocument();
    expect(window.localStorage.setItem).toHaveBeenCalledWith('tasksPane:runtimeHistoryPinned', 'unpinned');
  });

  it('keeps the split button hidden until AgentChatPanel registers actions', () => {
    useAgentChatActionsMock.mockReturnValue(null);

    renderTasksPane();

    expect(screen.getByTestId('split-available')).toHaveTextContent('false');
    expect(screen.queryByRole('button', { name: 'Open message composer' })).not.toBeInTheDocument();
    expect(screen.getByTestId('agent-chat-panel')).toBeInTheDocument();
  });

  it('holds the action pane open for the chat selector portal without locking it', () => {
    renderTasksPane();
    expect(useTasksPaneSlidingPaneOptionsMock.mock.lastCall?.[0].overlayOpen).toBe(false);

    fireEvent.click(screen.getByRole('button', { name: 'Open chat selector' }));
    expect(useTasksPaneSlidingPaneOptionsMock.mock.lastCall?.[0].overlayOpen).toBe(true);

    fireEvent.click(screen.getByRole('button', { name: 'Close chat selector' }));
    expect(useTasksPaneSlidingPaneOptionsMock.mock.lastCall?.[0].overlayOpen).toBe(false);
    expect(setIsTasksPaneLockedMock).not.toHaveBeenCalled();
  });

  it('marks engaged, opens the pane, and focuses the composer once AgentChat actions are registered', () => {
    const callOrder: string[] = [];
    const markEngaged = vi.fn(() => {
      callOrder.push('mark');
    });
    const focusComposer = vi.fn(() => {
      callOrder.push('focus');
    });
    const toggleRecording = vi.fn();

    openPaneMock.mockImplementation(() => {
      callOrder.push('open');
    });
    useAgentChatActionsMock.mockReturnValue({
      toggleRecording,
      focusComposer,
      markEngaged,
      isRecording: false,
      isProcessing: false,
    });

    renderTasksPane();

    fireEvent.click(screen.getByRole('button', { name: 'Open message composer' }));

    expect(markEngaged).toHaveBeenCalledTimes(1);
    expect(openPaneMock).toHaveBeenCalledTimes(1);
    expect(globalThis.requestAnimationFrame).toHaveBeenCalledTimes(1);
    expect(focusComposer).toHaveBeenCalledTimes(1);
    expect(toggleRecording).not.toHaveBeenCalled();
    expect(callOrder).toEqual(['mark', 'open', 'focus']);
    expect(paneControlProps.actions.splitButton.primary.ariaLabel).toBe('Open message composer');
  });

  it('restores the chat-filled layout preference and persists it when toggled', () => {
    (window.localStorage.getItem as ReturnType<typeof vi.fn>).mockReturnValue('chat');

    renderTasksPane();

    expect(screen.getByTestId('agent-chat-panel')).toHaveAttribute('data-expanded', 'true');
    expect(window.localStorage.setItem).toHaveBeenCalledWith('tasksPane:expandedHalf', 'chat');
    fireEvent.click(screen.getAllByRole('button', { name: 'Lock tasks open' })[0]);
    expect(window.localStorage.setItem).toHaveBeenCalledWith('tasksPane:expandedHalf', 'split');
  });

  it('routes the explicit Runtime editor identity to the Runtime task list', () => {
    useLocationMock.mockReturnValue({
      pathname: '/tools/video-editor',
      search: '?runtime=1&runtimeProject=runtime-project&runtimeTimeline=timeline-1',
    });
    useTasksPaneControllerMock.mockReturnValue({
      ...legacyControllerState,
      isRuntimeMode: true,
      runtimeTaskData: {
        tasks: [{ task_id: 'runtime-task-1' }],
        total: 1,
        totalPages: 1,
      },
    });

    renderTasksPane();

    expect(useTasksPaneControllerMock).toHaveBeenCalledWith(expect.objectContaining({
      runtimeProjectId: 'runtime-project',
    }));
    fireEvent.click(screen.getByRole('button', { name: 'Keep tasks open' }));
    expect(screen.getByTestId('runtime-task-list')).toHaveAttribute('data-runtime-task-id', 'runtime-task-1');
    expect(screen.queryByTestId('task-list')).not.toBeInTheDocument();
  });

  it('wires both Runtime surfaces to the existing lightbox and withholds the legacy chooser writer', () => {
    lightboxOpen = true;
    useLocationMock.mockReturnValue({
      pathname: '/tools/video-editor',
      search: '?runtime=1&runtimeProject=runtime-project&runtimeTimeline=timeline-1',
    });
    useTasksPaneControllerMock.mockReturnValue({
      ...legacyControllerState,
      isRuntimeMode: true,
      runtimeTaskData: { tasks: [{ task_id: 'runtime-task-1' }], total: 1, totalPages: 1 },
    });
    renderTasksPane();
    fireEvent.click(screen.getByRole('button', { name: 'Keep tasks open' }));
    expect(runtimeListProps.projectId).toBe('runtime-project');
    expect(runtimeListProps.onOpenOutput).toBe(handleOpenRuntimeTaskOutputMock);
    expect(runtimeDockProps.onOpenOutput).toBe(handleOpenRuntimeTaskOutputMock);
    expect(screen.getByTestId('media-lightbox')).toBeInTheDocument();
    expect(mediaLightboxProps.features).toEqual({ showDownload: true, showTaskDetails: true });
    expect(mediaLightboxProps.shotWorkflow).toBeUndefined();
    expect(handleAddToShotMock).not.toHaveBeenCalled();
    expect(handleAddToShotWithoutPositionMock).not.toHaveBeenCalled();
  });

  it('retains the existing manual shot workflow outside Runtime mode', () => {
    lightboxOpen = true;
    renderTasksPane();
    expect(mediaLightboxProps.shotWorkflow.onAddToShot).toBe(handleAddToShotMock);
    expect(mediaLightboxProps.shotWorkflow.onAddToShotWithoutPosition).toBe(handleAddToShotWithoutPositionMock);
  });

  it('passes the explicit editor scope and opened source to the existing lightbox overlay with no native callback', () => {
    lightboxOpen = true;
    runtimeRecoverySource = { mediaTuple: { generation_id: 'original-generation', variant_id: 'original-variant' } };
    useLocationMock.mockReturnValue({
      pathname: '/tools/video-editor',
      search: '?runtime=1&runtimeProject=runtime-project&runtimeTimeline=selected-timeline',
    });
    useTasksPaneControllerMock.mockReturnValue({ ...legacyControllerState, isRuntimeMode: true });
    renderTasksPane();
    expect(mediaLightboxProps.customOverlay.props).toEqual({ projectId: 'runtime-project', timelineId: 'selected-timeline', source: runtimeRecoverySource });
    expect(mediaLightboxProps.shotWorkflow).toBeUndefined();
    expect(handleAddToShotMock).not.toHaveBeenCalled();
  });

  it('opens Runtime history on the newest completed task status', () => {
    useLocationMock.mockReturnValue({
      pathname: '/tools/video-editor',
      search: '?runtime=1&runtimeProject=runtime-project&runtimeTimeline=timeline-1',
    });
    useTasksPaneControllerMock.mockReturnValue({
      ...legacyControllerState,
      isRuntimeMode: true,
      runtimeActivityTasks: [
        { state: 'succeeded', updated_at: '2026-10-13T10:00:00Z' },
        { state: 'failed', updated_at: '2026-10-14T10:00:00Z' },
      ],
      runtimeTaskData: { tasks: [], total: 0, totalPages: 0 },
    });

    renderTasksPane();
    fireEvent.click(screen.getByRole('button', { name: 'Open activity history' }));

    expect(handleFilterChangeMock).toHaveBeenCalledWith('Failed');
    expect(screen.getByTestId('runtime-task-list')).toBeInTheDocument();
  });

  it('routes the active editor identity ahead of a stale primary route', () => {
    useLocationMock.mockReturnValue({
      pathname: '/tools/video-editor',
      search: '?runtime=1&runtimeProject=project-A&runtimeTimeline=timeline-A',
    });
    useOptionalAgentChatBridgeMock.mockReturnValue({
      editorContext: { projectId: 'project-B', timelineId: 'timeline-B' },
    });
    useTasksPaneControllerMock.mockReturnValue({
      ...legacyControllerState,
      isRuntimeMode: true,
      runtimeTaskData: { tasks: [], total: 0, totalPages: 0 },
    });

    renderTasksPane();

    expect(useTasksPaneControllerMock).toHaveBeenCalledWith(expect.objectContaining({
      runtimeProjectId: 'project-B',
    }));
  });
});
