// @vitest-environment jsdom
import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClient, QueryClientProvider, useQuery } from '@tanstack/react-query';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import type { AgentTurn } from '@/tools/video-editor/types/agent-session';
import { BridgeRouteError } from '@/integrations/astrid/transport.ts';
import { AgentChatPanel } from './AgentChat';

const mocks = vi.hoisted(() => ({
  useAgentChatBridge: vi.fn(),
  useAgentChatActionsRegistry: vi.fn(),
  useVideoEditorRuntime: vi.fn(),
  useAgentSessions: vi.fn(),
  useProjectChat: vi.fn(),
  useSaveProjectDraft: vi.fn(),
  useSelectProjectSession: vi.fn(),
  useSetMainProjectSession: vi.fn(),
  useRenameProjectSession: vi.fn(),
  useUnassignedProjectSessions: vi.fn(),
  useAssociateProjectSession: vi.fn(),
  useCreateSession: vi.fn(),
  useAgentSession: vi.fn(),
  useSendMessage: vi.fn(),
  useAgentModels: vi.fn(),
  useSetAgentModel: vi.fn(),
  useLocalAgents: vi.fn(),
  useSetLocalAgent: vi.fn(),
  modelRefetch: vi.fn(),
  useCancelSession: vi.fn(),
  useTakeOverSession: vi.fn(),
  useCurrentAttachmentSet: vi.fn(),
  composerRemoveAttachment: vi.fn(),
  composerClearAttachments: vi.fn(),
  useAgentVoice: vi.fn(),
  loadGenerationForLightbox: vi.fn(),
  agentSessionsAvailable: true,
  // Mutable so individual tests can flip isTasksPaneLocked to satisfy the
  // engagement gate that drives auto-create.
  panesState: { isTasksPaneLocked: false, setIsTasksPaneOpen: vi.fn() },
}));

vi.mock('@/shared/contexts/AgentChatContext', () => ({
  useAgentChatBridge: (...args: unknown[]) => mocks.useAgentChatBridge(...args),
  useAgentChatActionsRegistry: (...args: unknown[]) => mocks.useAgentChatActionsRegistry(...args),
}));

vi.mock('@/tools/video-editor/contexts/VideoEditorRuntimeContext', () => ({
  useVideoEditorRuntime: (...args: unknown[]) => mocks.useVideoEditorRuntime(...args),
}));

vi.mock('@/tools/video-editor/hooks/useAgentSession', () => ({
  isTimelineAgentSessionsAvailable: () => mocks.agentSessionsAvailable,
  useAgentSessions: (...args: unknown[]) => mocks.useAgentSessions(...args),
  useProjectChat: (...args: unknown[]) => mocks.useProjectChat(...args),
  useSaveProjectDraft: (...args: unknown[]) => mocks.useSaveProjectDraft(...args),
  useSelectProjectSession: (...args: unknown[]) => mocks.useSelectProjectSession(...args),
  useSetMainProjectSession: (...args: unknown[]) => mocks.useSetMainProjectSession(...args),
  useRenameProjectSession: (...args: unknown[]) => mocks.useRenameProjectSession(...args),
  useUnassignedProjectSessions: (...args: unknown[]) => mocks.useUnassignedProjectSessions(...args),
  useAssociateProjectSession: (...args: unknown[]) => mocks.useAssociateProjectSession(...args),
  useCreateSession: (...args: unknown[]) => mocks.useCreateSession(...args),
  useAgentSession: (...args: unknown[]) => mocks.useAgentSession(...args),
  useSendMessage: (...args: unknown[]) => mocks.useSendMessage(...args),
  useAgentModels: (...args: unknown[]) => mocks.useAgentModels(...args),
  useSetAgentModel: (...args: unknown[]) => mocks.useSetAgentModel(...args),
  useLocalAgents: (...args: unknown[]) => mocks.useLocalAgents(...args),
  useSetLocalAgent: (...args: unknown[]) => mocks.useSetLocalAgent(...args),
  useCancelSession: (...args: unknown[]) => mocks.useCancelSession(...args),
  useTakeOverSession: (...args: unknown[]) => mocks.useTakeOverSession(...args),
}));

vi.mock('@/shared/state/selectionStore', () => ({
  composerRemoveAttachment: (...args: unknown[]) => mocks.composerRemoveAttachment(...args),
  composerClearAttachments: (...args: unknown[]) => mocks.composerClearAttachments(...args),
}));

vi.mock('@/shared/state/currentAttachmentSet', () => ({
  useCurrentAttachmentSet: (...args: unknown[]) => mocks.useCurrentAttachmentSet(...args),
}));

vi.mock('@/shared/state/panesStore', () => ({
  usePanesStore: (selector: (state: typeof mocks.panesState) => unknown) => selector(mocks.panesState),
}));

vi.mock('@/tools/video-editor/hooks/useAgentVoice', () => ({
  useAgentVoice: (...args: unknown[]) => mocks.useAgentVoice(...args),
}));

vi.mock('@/tools/video-editor/lib/generation-utils', () => ({
  loadGenerationForLightbox: (...args: unknown[]) => mocks.loadGenerationForLightbox(...args),
}));

vi.mock('@/domains/media-lightbox/MediaLightbox', () => ({
  MediaLightbox: ({ media }: { media: { id: string } }) => <div data-testid="media-lightbox">{media.id}</div>,
}));

vi.mock('./AgentChatMessage', () => ({
  AgentChatMessage: ({ turn }: { turn: { content: string } }) => <div>{turn.content}</div>,
  AgentChatToolGroup: () => null,
  AgentChatAttachmentStrip: ({
    attachments,
    onRemoveAttachment,
    onRemoveShot,
  }: {
    attachments: Array<{ clipId: string; shotId?: string }>;
    onRemoveAttachment?: (attachment: { clipId: string; shotId?: string }) => void;
    onRemoveShot?: (shotId: string) => void;
  }) => (
    <div>
      {attachments.map((attachment) => (
        <button
          key={`remove-${attachment.clipId}`}
          type="button"
          onClick={() => onRemoveAttachment?.(attachment)}
        >
          {`remove-${attachment.clipId}`}
        </button>
      ))}
      {attachments
        .filter((attachment) => attachment.shotId)
        .map((attachment) => (
          <button
            key={`remove-shot-${attachment.shotId}`}
            type="button"
            onClick={() => onRemoveShot?.(attachment.shotId!)}
          >
            {`remove-shot-${attachment.shotId}`}
          </button>
        ))}
    </div>
  ),
}));

function iso(timestampMs: number) {
  return new Date(timestampMs).toISOString();
}

function createUserTurn(content: string, timestampMs: number): AgentTurn {
  return {
    role: 'user',
    content,
    timestamp: iso(timestampMs),
  };
}

function createTimelineClip(clipId: string) {
  return {
    clipId,
    assetKey: `asset-${clipId}`,
    url: `https://example.com/${clipId}.png`,
    mediaType: 'image' as const,
    isTimelineBacked: true,
  };
}

function createState() {
  return {
    projectId: 'project-1' as string | null,
    projectChats: {
      'project-1': { project_id: 'project-1', scope_key: 'scope-1', revision: 1, selected_session_id: 'session-1', sessions: [{ id: 'session-1' }], draft: { text: '', revision: 0, queued_messages: [] as Array<{ id: string; text: string; session_id: string; attachments?: unknown[] }> } },
      'project-2': { project_id: 'project-2', scope_key: 'scope-2', revision: 1, selected_session_id: 'session-1', sessions: [{ id: 'session-1' }], draft: { text: '', revision: 0, queued_messages: [] as Array<{ id: string; text: string; session_id: string; attachments?: unknown[] }> } },
    },
    timelineId: 'timeline-1' as string | null,
    timelineClips: [] as Array<ReturnType<typeof createTimelineClip>>,
    sessionsData: [{ id: 'session-1', status: 'waiting_user' }],
    activeSessionData: {
      id: 'session-1',
      status: 'waiting_user',
      turns: [] as AgentTurn[],
      durableAcceptedRequestIds: undefined as string[] | undefined,
      control: undefined as { role: 'writer' | 'follower'; active: boolean; activeRequestId: string | null } | undefined,
    },
    createSession: {
      isPending: false,
      mutate: vi.fn(),
      mutateAsync: vi.fn().mockResolvedValue({ id: 'session-2' }),
    },
    sendMessage: {
      mutateAsync: vi.fn().mockResolvedValue(undefined),
      isPending: false,
      localError: null as string | null,
    },
    cancelSession: {
      mutate: vi.fn(),
      isPending: false,
    },
    takeOverSession: {
      mutate: vi.fn(),
      isPending: false,
      error: null as Error | null,
    },
    voice: {
      startRecording: vi.fn(),
      stopRecording: vi.fn(),
      cancelRecording: vi.fn(),
      isRecording: false,
      isProcessing: false,
      remainingSeconds: 30,
    },
  };
}

function mockFromState(state: ReturnType<typeof createState>) {
  mocks.useVideoEditorRuntime.mockImplementation(() => ({
    mediaLightbox: {
      loadGenerationForLightbox: mocks.loadGenerationForLightbox,
      Lightbox: ({ media }: { media: { id: string } }) => <div data-testid="media-lightbox">{media.id}</div>,
    },
  }));
  mocks.useAgentChatBridge.mockImplementation(() => ({
    timelineId: state.timelineId,
    editorContext: state.projectId ? { tool: 'video-editor', projectId: state.projectId, projectSlug: 'project-one', timelineId: state.timelineId, timelineName: null } : null,
  }));
  mocks.useAgentChatActionsRegistry.mockImplementation(() => ({
    registerHandlers: vi.fn(),
    publishState: vi.fn(),
    unregister: vi.fn(),
  }));
  mocks.useAgentSessions.mockImplementation(() => ({
    data: state.sessionsData,
    isLoading: false,
  }));
  mocks.useProjectChat.mockImplementation((projectId: string | null) => ({ data: projectId ? state.projectChats[projectId as 'project-1' | 'project-2'] : undefined }));
  mocks.useSaveProjectDraft.mockImplementation((projectId: string | null) => ({ mutateAsync: vi.fn().mockImplementation(async (input: { text: string; queuedMessages: Array<{ id: string; text: string; session_id: string; attachments?: unknown[] }> }) => {
    const chat = state.projectChats[projectId as 'project-1' | 'project-2'];
    chat.draft = { text: input.text, revision: chat.draft.revision + 1, queued_messages: input.queuedMessages };
    return chat;
  }) }));
  mocks.useSelectProjectSession.mockImplementation(() => ({ mutateAsync: vi.fn().mockResolvedValue(undefined) }));
  mocks.useSetMainProjectSession.mockImplementation(() => ({ isPending: false, mutateAsync: vi.fn().mockResolvedValue(undefined) }));
  mocks.useRenameProjectSession.mockImplementation(() => ({ mutateAsync: vi.fn().mockResolvedValue(undefined) }));
  mocks.useUnassignedProjectSessions.mockImplementation(() => ({ data: undefined, isLoading: false }));
  mocks.useAssociateProjectSession.mockImplementation(() => ({ mutate: vi.fn(), isPending: false }));
  mocks.useCreateSession.mockImplementation(() => state.createSession);
  mocks.useAgentSession.mockImplementation(() => ({
    data: state.activeSessionData,
    isLoading: false,
    error: (state as typeof state & { activeError?: Error }).activeError ?? null,
  }));
  mocks.useAgentModels.mockImplementation(() => ({ data: { currentModel: 'openai/gpt-5', providers: [{ id: 'openai', name: 'OpenAI', signedIn: true, models: [{ id: 'gpt-5', name: 'GPT 5' }, { id: 'gpt-5-mini', name: 'GPT 5 Mini' }] }] }, isLoading: false, error: null, refetch: mocks.modelRefetch }));
  mocks.useSetAgentModel.mockImplementation(() => ({ mutateAsync: vi.fn().mockResolvedValue({ currentModel: 'openai/gpt-5-mini' }), isPending: false, error: null }));
  mocks.useLocalAgents.mockImplementation(() => ({ data: { agents: [], selectedAgent: 'astrid' }, isLoading: false, error: null, refetch: vi.fn() }));
  mocks.useSetLocalAgent.mockImplementation(() => ({ mutateAsync: vi.fn().mockResolvedValue(undefined), isPending: false, error: null }));
  mocks.useSendMessage.mockImplementation(() => state.sendMessage);
  mocks.useCancelSession.mockImplementation(() => state.cancelSession);
  mocks.useTakeOverSession.mockImplementation(() => state.takeOverSession);
  mocks.useCurrentAttachmentSet.mockImplementation(() => ({
    clips: state.timelineClips,
    summary: state.timelineClips.length > 0 ? `attaching ${state.timelineClips.length} image` : '',
  }));
  mocks.useAgentVoice.mockImplementation(() => state.voice);
}

function renderAgentChat(isExpanded = false) {
  return render(<AgentChatPanel isExpanded={isExpanded} />);
}

function rerenderAgentChat(rerender: ReturnType<typeof render>['rerender'], isExpanded = false) {
  rerender(<AgentChatPanel isExpanded={isExpanded} />);
}

async function getInput() {
  const textbox = await screen.findByRole('textbox');
  await waitFor(() => expect(textbox).not.toBeDisabled());
  return textbox;
}

async function queueMessage(textbox: HTMLElement, text: string) {
  fireEvent.change(textbox, { target: { value: text } });
  fireEvent.keyDown(textbox, { key: 'Enter' });
  await waitFor(() => expect((textbox as HTMLTextAreaElement).value).toBe(''));
}

function getQueuedTexts() {
  return Array.from(document.querySelectorAll('.line-clamp-2')).map((node) => node.textContent);
}

describe('AgentChat', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mocks.agentSessionsAvailable = true;
    // Default: pane is locked so the engagement gate is satisfied and the
    // existing auto-create assertions still hold. Tests that need the unengaged
    // baseline flip this back to false.
    mocks.panesState.isTasksPaneLocked = true;
    vi.spyOn(window, 'requestAnimationFrame').mockImplementation((callback: FrameRequestCallback) => {
      callback(0);
      return 1;
    });
    if (!Element.prototype.scrollIntoView) {
      Element.prototype.scrollIntoView = vi.fn();
    }
    Object.defineProperty(HTMLElement.prototype, 'scrollTo', {
      configurable: true,
      value: vi.fn(),
    });

    mocks.loadGenerationForLightbox.mockResolvedValue({
      id: 'gen-1',
      generation_id: 'gen-1',
      location: 'https://example.com/shared.png',
      imageUrl: 'https://example.com/shared.png',
      thumbUrl: 'https://example.com/shared.png',
      type: 'image',
      primary_variant_id: null,
      name: 'Shared image',
    });
  });

  it('shows a quiet agent name and reveals the model only in its info tooltip', async () => {
    const state = createState();
    const sessionId = 'codex:session-1';
    const projectId = 'project-1';
    state.projectChats[projectId].selected_session_id = sessionId;
    state.projectChats[projectId].sessions = [{ id: sessionId }];
    state.sessionsData = [{ id: sessionId, status: 'waiting_user' }];
    state.activeSessionData.id = sessionId;
    mockFromState(state);
    mocks.useAgentModels.mockImplementation(() => ({
      data: {
        currentModel: 'openai/gpt-5',
        providers: [{ id: 'openai', name: 'OpenAI', signedIn: true, models: [{ id: 'gpt-5', name: 'GPT 5' }] }],
        localModels: {
          currentModelId: 'vendor/codex-current',
          thoughtLevel: { configId: 'reasoning_effort', name: 'Reasoning effort', currentValue: 'high', options: [{ value: 'high', name: 'High' }] },
          availableModels: [
            { modelId: 'vendor/codex-current', name: 'Codex Current' },
            { modelId: 'vendor/codex-target', name: 'Codex Target', description: 'For focused coding' },
          ],
        },
      },
      isLoading: false,
      error: null,
      refetch: mocks.modelRefetch,
    }));
    const mutateAsync = vi.fn().mockResolvedValue(undefined);
    mocks.useSetAgentModel.mockImplementation(() => ({ mutateAsync, isPending: false, error: null }));

    renderAgentChat();
    const identity = await screen.findByTestId('agent-chat-identity');
    expect(identity).toHaveTextContent(/^Codex$/);
    expect(identity).toHaveClass('text-xs');
    expect(identity.parentElement).toHaveClass('text-muted-foreground');
    expect(screen.queryByText('Codex Current', { exact: true })).toBeNull();
    const user = userEvent.setup();
    await user.hover(screen.getByRole('button', { name: 'Chat model information' }));
    const tooltip = (await screen.findByText('Codex Current · High', { exact: true })).parentElement;
    expect(tooltip).toHaveTextContent('To use another model, start a new chat.');
    expect(screen.queryByRole('combobox', { name: 'Agent model' })).toBeNull();

    await waitFor(() => {
      expect(mocks.useAgentModels).toHaveBeenCalledWith(true, sessionId, projectId);
      expect(mocks.useSetAgentModel).toHaveBeenCalledWith(sessionId, projectId);
    });
    expect(mutateAsync).not.toHaveBeenCalled();
  });

  it('starts a chat with another agent from the New chat menu and shows what an empty chat runs with', async () => {
    const state = createState();
    state.createSession.mutateAsync.mockImplementationOnce(async () => {
      state.projectChats['project-1'] = {
        ...state.projectChats['project-1'],
        revision: 2,
        selected_session_id: 'codex:session-2',
        sessions: [{ id: 'session-1' }, { id: 'codex:session-2' }],
      };
      return { id: 'codex:session-2' };
    });
    mockFromState(state);
    const setAgent = vi.fn().mockResolvedValue(undefined);
    mocks.useLocalAgents.mockImplementation(() => ({
      data: { agents: [{ id: 'codex', name: 'Codex', state: 'ready', line: null }], selectedAgent: 'astrid' },
      isLoading: false, error: null, refetch: vi.fn(),
    }));
    mocks.useSetLocalAgent.mockImplementation(() => ({ mutateAsync: setAgent, isPending: false, error: null }));

    renderAgentChat();
    const identity = await screen.findByTestId('agent-chat-identity');
    expect(identity).toHaveTextContent(/^Astrid$/);
    expect(screen.getByRole('button', { name: 'Chat model information' })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'New chat with…' }));
    fireEvent.click(await screen.findByRole('option', { name: /Codex/ }));
    await waitFor(() => expect(setAgent).toHaveBeenCalledWith('codex'));
    await waitFor(() => expect(state.createSession.mutateAsync).toHaveBeenCalled());
    expect(setAgent.mock.invocationCallOrder[0]).toBeLessThan(state.createSession.mutateAsync.mock.invocationCallOrder[0]);
    await waitFor(() => expect(mocks.useAgentSession).toHaveBeenLastCalledWith('codex:session-2', 'project-1'));
  });

  it('omits model information when no model is known', async () => {
    mockFromState(createState());
    mocks.useAgentModels.mockReturnValue({ data: undefined, isLoading: false });
    renderAgentChat();
    expect(await screen.findByTestId('agent-chat-identity')).toHaveTextContent(/^Astrid$/);
    expect(screen.queryByRole('button', { name: 'Chat model information' })).toBeNull();
  });

  it.each(['success', 'failure'] as const)('passes the chosen model and effort to startup and holds the composer (%s)', async outcome => {
    const state = createState();
    const oldId = 'codex:old';
    const newId = 'codex:new';
    state.projectChats['project-1'].selected_session_id = oldId;
    state.projectChats['project-1'].sessions = [{ id: oldId }];
    state.activeSessionData.id = oldId;
    state.createSession.mutateAsync.mockImplementationOnce(async () => {
      state.projectChats['project-1'].selected_session_id = newId;
      state.projectChats['project-1'].sessions.push({ id: newId });
      return { id: newId };
    });
    mockFromState(state);
    mocks.useAgentModels.mockReturnValue({ data: { providers: [], currentModel: null, localModels: {
      currentModelId: 'sol', availableModels: [{ modelId: 'sol', name: 'Sol' }], thoughtLevel: { configId: 'reasoning_effort', name: 'Effort', currentValue: 'low',
        recommendedValue: 'high', options: [{ value: 'low', name: 'Low' }, { value: 'high', name: 'High' }] },
    } }, isLoading: false });
    let resolve!: () => void;
    let reject!: (error: Error) => void;
    const selection = vi.fn(() => new Promise<void>((yes, no) => { resolve = yes; reject = no; }));
    mocks.useSetAgentModel.mockReturnValue({ mutateAsync: selection });
    renderAgentChat();
    await screen.findByRole('button', { name: 'Chat model information' });
    fireEvent.click(screen.getByRole('button', { name: 'New chat with…' }));
    fireEvent.click(screen.getByRole('button', { name: 'Choose a Codex model' }));
    fireEvent.click(await screen.findByRole('button', { name: 'Choose a thinking level for Sol' }));
    fireEvent.click(screen.getByRole('option', { name: 'Low' }));
    expect(selection).not.toHaveBeenCalled();
    expect(screen.getByRole('button', { name: 'Choose a thinking level for Sol' })).toHaveTextContent('Low');
    fireEvent.click(screen.getByRole('option', { name: /Sol/ }));
    await waitFor(() => expect(selection).toHaveBeenCalledWith({ sessionId: newId, model: 'sol', thoughtLevel: 'low' }));
    expect(screen.getByRole('textbox')).toBeDisabled();
    await act(async () => { if (outcome === 'success') resolve(); else reject(new Error('Effort rejected')); });
    if (outcome === 'failure') {
      expect(screen.getByRole('alert')).toHaveTextContent('Effort rejected');
      expect(screen.getByRole('textbox')).toBeDisabled();
    } else await waitFor(() => expect(screen.getByRole('textbox')).toBeEnabled());
  });

  it.each(['success', 'failure'] as const)('locks the composer and shows the chosen agent during slow startup (%s)', async (outcome) => {
    const state = createState();
    state.activeSessionData.turns = [createUserTurn('Previous chat transcript', 1)];
    let resolve!: (value: { id: string }) => void;
    let reject!: (error: Error) => void;
    state.createSession.mutateAsync.mockImplementationOnce(() => new Promise((yes, no) => { resolve = yes; reject = no; }));
    mockFromState(state);
    mocks.useLocalAgents.mockReturnValue({
      data: { agents: [{ id: 'codex', name: 'Codex', state: 'ready', line: null }], selectedAgent: 'astrid' },
      isLoading: false, error: null, refetch: vi.fn(),
    });
    renderAgentChat();
    const input = await getInput();
    fireEvent.change(input, { target: { value: 'Retain this draft' } });
    expect(screen.getByText('Previous chat transcript')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'New chat with…' }));
    fireEvent.click(await screen.findByRole('option', { name: /Codex/ }));
    await waitFor(() => expect(state.createSession.mutateAsync).toHaveBeenCalled());
    vi.useFakeTimers();
    try {
      await act(async () => { await vi.advanceTimersByTimeAsync(24_000); });
      expect(screen.getByTestId('agent-chat-identity')).toHaveTextContent(/^Codex$/);
      expect(screen.queryByText('Previous chat transcript')).toBeNull();
      expect(input).toBeDisabled();
      expect(input).toHaveAttribute('placeholder', 'Starting Codex…');
      expect(input).toHaveValue('');
      expect(screen.getByRole('button', { name: 'Send' })).toBeDisabled();
      expect(screen.getByRole('button', { name: 'Voice input (Cmd+Shift+R)' })).toBeDisabled();
      fireEvent.keyDown(input, { key: 'Enter' });
      fireEvent.keyDown(window, { key: 'r', metaKey: true, shiftKey: true });
      expect(state.sendMessage.mutateAsync).not.toHaveBeenCalled();
      expect(state.voice.startRecording).not.toHaveBeenCalled();
      await act(async () => {
        if (outcome === 'failure') reject(new Error('Slow adapter failed'));
        else {
          state.projectChats['project-1'] = { ...state.projectChats['project-1'], revision: 2, selected_session_id: 'codex:session-2', sessions: [{ id: 'session-1' }, { id: 'codex:session-2' }] };
          state.activeSessionData = { ...state.activeSessionData, id: 'codex:session-2', turns: [] };
          resolve({ id: 'codex:session-2' });
        }
      });
      expect(input).not.toBeDisabled();
      expect(input).toHaveValue('Retain this draft');
      if (outcome === 'failure') {
        expect(screen.getByRole('alert')).toHaveTextContent("Codex didn't start.");
        expect(screen.getByTestId('agent-chat-identity')).toHaveTextContent(/^Astrid$/);
        expect(screen.getByText('Previous chat transcript')).toBeInTheDocument();
        expect(mocks.useAgentSession).toHaveBeenLastCalledWith('session-1', 'project-1');
      } else {
        expect(screen.getByTestId('agent-chat-identity')).toHaveTextContent(/^Codex$/);
        expect(screen.queryByText('Previous chat transcript')).toBeNull();
        expect(mocks.useAgentSession).toHaveBeenLastCalledWith('codex:session-2', 'project-1');
      }
    } finally {
      vi.useRealTimers();
    }
  });

  it('shows the failed agent start details and retries the same new chat', async () => {
    const state = createState();
    state.createSession.mutateAsync.mockRejectedValueOnce(new Error('adapter failed'));
    mockFromState(state);
    mocks.useLocalAgents.mockImplementation(() => ({
      data: { agents: [{ id: 'codex', name: 'Codex', state: 'ready', line: null }], selectedAgent: 'astrid' },
      isLoading: false, error: null, refetch: vi.fn(),
    }));
    const setAgent = vi.fn().mockResolvedValue(undefined);
    mocks.useSetLocalAgent.mockImplementation(() => ({ mutateAsync: setAgent, isPending: false, error: null }));

    renderAgentChat();
    fireEvent.click(screen.getByRole('button', { name: 'New chat with…' }));
    fireEvent.click(await screen.findByRole('option', { name: /Codex/ }));
    const alert = await screen.findByRole('alert');
    expect(alert).toHaveTextContent("Codex didn't start.");
    expect(alert).toHaveTextContent('Details: adapter failed');
    state.createSession.mutateAsync.mockResolvedValueOnce({ id: 'codex:session-2' });
    fireEvent.click(screen.getByRole('button', { name: 'Try again' }));
    await waitFor(() => expect(state.createSession.mutateAsync).toHaveBeenCalledTimes(2));
  });

  it.each([
    ['provider auth failure', 'Provider authentication failed (401)'],
    ['provider balance failure', 'insufficient credits'],
    ['ordinary failure', 'Unexpected turn failure'],
    ['authoring failure', 'Element authoring failed'],
  ])('does not offer mid-chat model switching after %s', async (_label, message) => {
    const state = createState() as ReturnType<typeof createState> & { activeError?: Error };
    state.activeSessionData.status = 'error';
    state.activeError = new Error(message);
    mockFromState(state);
    renderAgentChat();
    const alert = await screen.findByRole('alert');
    expect(alert).toHaveTextContent(message);
    expect(screen.queryByRole('button', { name: 'Switch model' })).toBeNull();
  });

  it('keeps saying chat is unavailable once a conversation has turns: the same plain line, no alert', async () => {
    const state = createState() as ReturnType<typeof createState> & { activeError?: Error };
    state.activeSessionData.turns = [{ role: 'assistant', content: 'Earlier answer', timestamp: iso(1_000) }] as AgentTurn[];
    state.activeError = new BridgeRouteError('Read chat session', 503, { error: 'acp_unavailable' });
    mockFromState(state);
    renderAgentChat();
    expect(await screen.findByText('Earlier answer')).toBeInTheDocument();
    expect(screen.getByText("Chat isn't running on this computer right now.")).toBeInTheDocument();
    expect(screen.queryByRole('alert')).toBeNull();
  });

  it('renders one Astrid-managed notice and never starts unavailable session work', async () => {
    mocks.agentSessionsAvailable = false;
    const state = createState();
    state.sessionsData = [];
    mockFromState(state);

    const view = renderAgentChat();
    expect(await screen.findByText('Timeline agent chat is managed in Astrid')).toBeInTheDocument();
    expect(screen.getByText(/Run the agent workflow in Astrid/)).toBeInTheDocument();

    view.rerender(<AgentChatPanel />);
    await new Promise((resolve) => setTimeout(resolve, 0));
    expect(mocks.useAgentSessions).not.toHaveBeenCalled();
    expect(mocks.useCreateSession).not.toHaveBeenCalled();
    expect(state.createSession.mutate).not.toHaveBeenCalled();
  });

  it('creates project chat without a timeline when engaged', async () => {
    const state = createState();
    state.timelineId = null;
    state.sessionsData = [];
    state.projectChats['project-1'].sessions = [];
    state.projectChats['project-1'].selected_session_id = null;
    state.createSession = {
      isPending: false,
      mutate: vi.fn(),
      mutateAsync: vi.fn(),
    };
    mockFromState(state);

    const view = renderAgentChat();

    expect(screen.getByTestId('agent-chat-identity')).toHaveTextContent('Astrid');
    expect(view.container.querySelector('img[src="/astrid-avatar.png"]')).toBeNull();

    expect(screen.queryByText('Select a project to start chatting.')).not.toBeInTheDocument();
    await waitFor(() => expect(state.createSession.mutate).toHaveBeenCalledTimes(1));
    expect(mocks.useCreateSession).toHaveBeenCalledWith(null, 'project-1', 'ensure');
  });

  it('uses a timeline-style chat dropdown and keeps attach inside the New chat menu in the narrow header', async () => {
    const state = createState();
    state.sessionsData = [
      { id: 'session-1', status: 'waiting_user' },
      { id: 'session-2', status: 'waiting_user' },
    ];
    state.projectChats['project-1'].sessions = [{ id: 'session-1' }, { id: 'session-2' }];
    mockFromState(state);
    const selectSession = vi.fn().mockResolvedValue(undefined);
    const onSelectorOpenChange = vi.fn();
    mocks.useSelectProjectSession.mockReturnValue({ mutateAsync: selectSession });

    render(<AgentChatPanel onSessionSelectorOpenChange={onSelectorOpenChange} />);

    const selectors = screen.getAllByRole('combobox', { name: 'Project chat session' });
    expect(selectors).toHaveLength(1);
    expect(selectors[0]).toHaveClass('max-w-40', 'min-w-0', 'shrink', 'bg-card/80', 'focus-visible:ring-2');
    expect(screen.getByTestId('agent-chat-header')).toHaveClass('min-w-0');
    expect(selectors[0]).toHaveTextContent('Chat 1');
    expect(screen.queryByText('session-1')).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Attach existing' })).toBeNull();
    expect(screen.getByRole('button', { name: 'New chat' })).toBeInTheDocument();

    const user = userEvent.setup();
    await user.click(selectors[0]);
    expect(await screen.findByPlaceholderText('Search chats...')).toBeInTheDocument();
    expect(onSelectorOpenChange).toHaveBeenLastCalledWith(true);
    expect(await screen.findByRole('option', { name: /^Chat 1/ })).toBeInTheDocument();
    await user.click(screen.getByRole('option', { name: /^Chat 2/ }));
    await waitFor(() => expect(selectSession).toHaveBeenCalledWith({ expectedRevision: 1, sessionId: 'session-2' }));
    expect(onSelectorOpenChange).toHaveBeenLastCalledWith(false);
  });

  it('uses registry titles and creation numbers even when inventory is reordered or missing a chat', async () => {
    const state = createState();
    state.sessionsData = [{ id: 'unregistered', status: 'waiting_user' }, { id: 'missing', status: 'waiting_user' }, { id: 'session-1', status: 'waiting_user' }];
    Object.assign(state.projectChats['project-1'], {
      selected_session_id: 'session-3', main_session_id: 'session-3',
      sessions: [{ id: 'session-1', title: 'Planning' }, { id: 'missing', missing: true }, { id: 'session-3' }],
    });
    mockFromState(state);
    const view = renderAgentChat();
    const selector = await screen.findByRole('combobox', { name: 'Project chat session' });
    await waitFor(() => expect(selector).toHaveTextContent('Chat 3'));
    await userEvent.setup().click(selector);
    expect(screen.getAllByRole('option').map(row => row.textContent)).toEqual([
      expect.stringContaining('Planning'), expect.stringContaining('Chat 3'),
    ]);
    state.sessionsData = [{ id: 'session-4', status: 'waiting_user' }, ...state.sessionsData];
    state.projectChats['project-1'].sessions.push({ id: 'session-4' });
    rerenderAgentChat(view.rerender);
    expect(selector).toHaveTextContent('Chat 3');
    expect(screen.getByRole('option', { name: /^Chat 4/ })).toBeInTheDocument();
  });

  it('opens on Main, preserves a local chat choice across refetch, and can promote that chat', async () => {
    const state = createState();
    state.sessionsData = [
      { id: 'session-1', status: 'waiting_user' },
      { id: 'session-2', status: 'waiting_user' },
    ];
    Object.assign(state.projectChats['project-1'], {
      selected_session_id: 'session-2',
      main_session_id: 'session-2',
      sessions: [{ id: 'session-1' }, { id: 'session-2' }],
    });
    mockFromState(state);
    const selectSession = vi.fn().mockResolvedValue(undefined);
    const setMainSession = vi.fn().mockResolvedValue(undefined);
    mocks.useSelectProjectSession.mockReturnValue({ mutateAsync: selectSession });
    mocks.useSetMainProjectSession.mockReturnValue({ isPending: false, mutateAsync: setMainSession });

    const view = renderAgentChat();
    const selector = await screen.findByRole('combobox', { name: 'Project chat session' });
    await waitFor(() => expect(selector).toHaveTextContent('Chat 2'));

    const user = userEvent.setup();
    await user.click(selector);
    expect(screen.getByText('Main', { exact: true })).toBeInTheDocument();
    await user.click(await screen.findByRole('option', { name: /Chat 1/ }));
    await waitFor(() => expect(selector).toHaveTextContent('Chat 1'));

    view.rerender(<AgentChatPanel isExpanded={false} />);
    await waitFor(() => expect(selector).toHaveTextContent('Chat 1'));
    const priorSelectCount = selectSession.mock.calls.length;
    await user.click(selector);
    await user.click(screen.getByRole('button', { name: 'Make Chat 1 main' }));
    await waitFor(() => expect(setMainSession).toHaveBeenCalledWith({ expectedRevision: 1, sessionId: 'session-1' }));
    await waitFor(() => expect(selector).toHaveTextContent('Chat 1'));
    expect(selectSession).toHaveBeenCalledTimes(priorSelectCount);
    expect(screen.getByRole('option', { name: /Chat 1/ })).toBeInTheDocument();
  });

  it('waits for persisted selection when history resolves before the project registry', async () => {
    const state = createState();
    state.sessionsData = [
      { id: 'session-1', status: 'waiting_user' },
      { id: 'session-2', status: 'waiting_user' },
    ];
    Object.assign(state.projectChats['project-1'], {
      selected_session_id: 'session-1', main_session_id: 'session-2',
      sessions: [{ id: 'session-1' }, { id: 'session-2' }],
    });
    mockFromState(state);
    mocks.useProjectChat.mockReturnValue({ data: undefined, isLoading: true });
    const view = renderAgentChat();
    expect(screen.queryByRole('combobox', { name: 'Project chat session' })).toBeNull();
    expect(mocks.useAgentSession).not.toHaveBeenCalledWith('session-1', 'project-1');
    expect(state.createSession.mutate).not.toHaveBeenCalled();

    mocks.useProjectChat.mockReturnValue({ data: state.projectChats['project-1'], isLoading: false });
    view.rerender(<AgentChatPanel isExpanded={false} />);
    const selector = await screen.findByRole('combobox', { name: 'Project chat session' });
    await waitFor(() => expect(selector).toHaveTextContent('Chat 1'));

    const user = userEvent.setup();
    await user.click(selector);
    await user.click(await screen.findByRole('option', { name: /Chat 2/ }));
    await waitFor(() => expect(selector).toHaveTextContent('Chat 2'));
    mocks.useProjectChat.mockReturnValue({ data: undefined, isLoading: true });
    view.rerender(<AgentChatPanel isExpanded={false} />);
    expect(selector).toHaveTextContent('Chat 2');
    mocks.useProjectChat.mockReturnValue({ data: state.projectChats['project-1'], isLoading: false });
    view.rerender(<AgentChatPanel isExpanded={false} />);
    expect(selector).toHaveTextContent('Chat 2');
  });

  it('reopens the persisted selected chat when Main is unset', async () => {
    const state = createState();
    state.sessionsData = [{ id: 'session-1', status: 'waiting_user' }];
    Object.assign(state.projectChats['project-1'], {
      selected_session_id: 'session-1', main_session_id: null, sessions: [{ id: 'session-1' }],
    });
    mockFromState(state);
    mocks.useProjectChat.mockReturnValue({ data: undefined, isLoading: true });
    const view = renderAgentChat();
    expect(mocks.useAgentSession).not.toHaveBeenCalledWith('session-1', 'project-1');
    expect(state.createSession.mutate).not.toHaveBeenCalled();

    mocks.useProjectChat.mockReturnValue({ data: state.projectChats['project-1'], isLoading: false });
    view.rerender(<AgentChatPanel isExpanded={false} />);
    const selector = await screen.findByRole('combobox', { name: 'Project chat session' });
    await waitFor(() => expect(selector).toHaveTextContent('Chat 1'));
    expect(state.createSession.mutate).not.toHaveBeenCalled();
    expect(mocks.useAgentSession).toHaveBeenCalledWith('session-1', 'project-1');
  });

  it('keeps project chats selectable when Main is unset without creating a replacement Main', async () => {
    const state = createState();
    state.sessionsData = [{ id: 'session-1', status: 'waiting_user' }, { id: 'session-2', status: 'waiting_user' }];
    Object.assign(state.projectChats['project-1'], {
      selected_session_id: 'session-2', main_session_id: null, sessions: [{ id: 'session-1' }, { id: 'session-2' }],
    });
    mockFromState(state);
    const view = renderAgentChat();
    const selector = await screen.findByRole('combobox', { name: 'Project chat session' });
    await waitFor(() => expect(selector).toHaveTextContent('Chat 2'));
    expect(state.createSession.mutate).not.toHaveBeenCalled();
    const user = userEvent.setup();
    await user.click(selector);
    await user.click(await screen.findByRole('option', { name: /Chat 1/ }));
    await waitFor(() => expect(selector).toHaveTextContent('Chat 1'));
    const priorRevision = state.projectChats['project-1'].revision;
    state.projectChats['project-1'] = {
      ...state.projectChats['project-1'], selected_session_id: 'session-1', revision: priorRevision + 1,
    };
    view.rerender(<AgentChatPanel isExpanded={false} />);
    expect(selector).toHaveTextContent('Chat 1');
    await user.click(selector);
    expect(screen.getByRole('button', { name: 'Make Chat 1 main' })).toBeEnabled();
  });

  it('does not create or assign Main when existing project chats have no Main', async () => {
    mocks.panesState.isTasksPaneLocked = false;
    const state = createState();
    state.sessionsData = [{ id: 'session-1', status: 'waiting_user' }];
    Object.assign(state.projectChats['project-1'], { main_session_id: null });
    mockFromState(state);
    renderAgentChat();
    await waitFor(() => expect(mocks.useCreateSession).toHaveBeenCalledWith('timeline-1', 'project-1', 'ensure'));
    expect(state.createSession.mutate).not.toHaveBeenCalled();
    expect(state.projectChats['project-1'].main_session_id).toBeNull();
  });

  it('waits for authoritative project chat state before attempting Main creation', async () => {
    const state = createState();
    state.sessionsData = [];
    mockFromState(state);
    mocks.useProjectChat.mockReturnValue({ data: undefined, isLoading: true });
    renderAgentChat();
    await new Promise(resolve => setTimeout(resolve, 0));
    expect(state.createSession.mutate).not.toHaveBeenCalled();
  });

  it('restores the local project draft after switching A→B→A while the host save is pending', async () => {
    mocks.panesState.isTasksPaneLocked = false;
    const state = createState();
    state.sessionsData = [{ id: 'session-1', status: 'waiting_user' }];
    mockFromState(state);
    const view = renderAgentChat();
    const textbox = await getInput();
    fireEvent.change(textbox, { target: { value: 'A local draft' } });

    state.projectId = 'project-2';
    rerenderAgentChat(view.rerender);
    await waitFor(() => expect(screen.getByRole('textbox')).toHaveValue(''));
    fireEvent.change(screen.getByRole('textbox'), { target: { value: 'B draft' } });

    state.projectId = 'project-1';
    rerenderAgentChat(view.rerender);
    await waitFor(() => expect(screen.getByRole('textbox')).toHaveValue('A local draft'));
    expect(state.projectChats['project-2'].draft.text).not.toBe('A local draft');
  });

  it('shows saved-chat load failures and retries only when the user clicks Retry saved chat', async () => {
    const state = createState();
    mockFromState(state);
    const refetch = vi.fn();
    mocks.useAgentSession.mockReturnValue({ data: undefined, error: new Error('ACP session not found: saved-chat'), isFetching: false, refetch });
    renderAgentChat();
    expect(await screen.findByText('ACP session not found: saved-chat')).toBeInTheDocument();
    expect(refetch).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole('button', { name: 'Retry saved chat' }));
    expect(refetch).toHaveBeenCalledTimes(1);
  });

  it('uses four composer rows in split view and eight when chat fills the pane', async () => {
    const state = createState();
    mockFromState(state);

    const view = renderAgentChat();
    const textbox = await getInput();
    expect(textbox.tagName).toBe('TEXTAREA');
    expect(textbox).toHaveAttribute('rows', '4');

    view.rerender(<AgentChatPanel isExpanded />);
    expect(await screen.findByRole('textbox')).toHaveAttribute('rows', '8');
  });

  it('auto-creates a session when the engagement gate fires (pane locked) with a timeline available', async () => {
    const state = createState();
    state.sessionsData = [];
    state.projectChats['project-1'].sessions = [];
    state.projectChats['project-1'].selected_session_id = null;
    state.createSession = {
      isPending: false,
      mutate: vi.fn(),
      mutateAsync: vi.fn().mockResolvedValue({ id: 'session-2' }),
    };
    mockFromState(state);

    renderAgentChat();

    await waitFor(() => expect(state.createSession.mutate).toHaveBeenCalledTimes(1));
  });

  it('keeps a pre-dispatch cancelled session eligible for normal selection', async () => {
    const state = createState();
    state.sessionsData = [
      { id: 'cancelled-session', status: 'cancelled' },
      { id: 'predispatch-cancel-session', status: 'waiting_user' },
    ];
    Object.assign(state.projectChats['project-1'], {
      selected_session_id: null, main_session_id: null,
      sessions: [{ id: 'cancelled-session' }, { id: 'predispatch-cancel-session' }],
    });
    mockFromState(state);

    renderAgentChat();

    await waitFor(() => expect(mocks.useAgentSession).toHaveBeenCalledWith('predispatch-cancel-session', 'project-1'));
  });

  it('does not auto-create when unengaged (pane unlocked, no voice, no markEngaged)', async () => {
    mocks.panesState.isTasksPaneLocked = false;
    const state = createState();
    state.sessionsData = [];
    state.createSession = {
      isPending: false,
      mutate: vi.fn(),
      mutateAsync: vi.fn(),
    };
    mockFromState(state);

    renderAgentChat();

    // Give the auto-create effect time to NOT fire.
    await new Promise((resolve) => setTimeout(resolve, 0));
    expect(state.createSession.mutate).not.toHaveBeenCalled();
  });

  it('Cmd+Shift+R remains available for project chat without a timeline', async () => {
    const state = createState();
    state.timelineId = null;
    state.sessionsData = [];
    state.voice = {
      startRecording: vi.fn(),
      stopRecording: vi.fn(),
      cancelRecording: vi.fn(),
      isRecording: false,
      isProcessing: false,
      remainingSeconds: 30,
    };
    mockFromState(state);

    renderAgentChat();

    fireEvent.keyDown(window, {
      key: 'r',
      metaKey: true,
      shiftKey: true,
    });

    expect(state.voice.startRecording).toHaveBeenCalledTimes(1);
  });

  it('routes attachment removal through the composer intent', async () => {
    const state = createState();
    state.timelineClips = [
      createTimelineClip('clip-1'),
      createTimelineClip('clip-2'),
    ];
    mockFromState(state);

    renderAgentChat();

    fireEvent.click(screen.getByRole('button', { name: 'remove-clip-1' }));

    expect(mocks.composerRemoveAttachment).toHaveBeenCalledWith(expect.objectContaining({
      clipId: 'clip-1',
      url: 'https://example.com/clip-1.png',
      mediaType: 'image',
    }));
  });

  it('allows typing while processing and queues without sending immediately', async () => {
    const state = createState();
    state.activeSessionData.status = 'processing';
    mockFromState(state);

    renderAgentChat();

    const textbox = await getInput();
    expect(textbox).not.toBeDisabled();

    await queueMessage(textbox, 'queued while processing');

    expect(state.sendMessage.mutateAsync).not.toHaveBeenCalled();
    expect(screen.getByText('queued while processing')).toBeInTheDocument();
  });

  it('auto-sends the queued head with attachments snapshotted at queue time', async () => {
    const state = createState();
    state.activeSessionData.status = 'processing';
    state.timelineClips = [createTimelineClip('clip-1')];
    mockFromState(state);

    const view = renderAgentChat();
    const textbox = await getInput();

    await queueMessage(textbox, 'send old attachment');
    expect(state.sendMessage.mutateAsync).not.toHaveBeenCalled();

    state.timelineClips = [createTimelineClip('clip-2')];
    state.activeSessionData.status = 'waiting_user';
    rerenderAgentChat(view.rerender);

    await waitFor(() => {
      expect(state.sendMessage.mutateAsync).toHaveBeenCalledWith({
        input: { message: 'send old attachment', attachments: [expect.objectContaining({ clipId: 'clip-1' })], requestId: expect.any(String) },
        projectId: 'project-1',
        sessionId: 'session-1',
        context: expect.objectContaining({ projectId: 'project-1' }),
      });
    });
  });

  it('settles optimism after completion without requiring an echoed user turn', async () => {
    const state = createState();
    state.activeSessionData.status = 'processing';
    state.activeSessionData.turns = [createUserTurn('same text', 9_000)];
    mockFromState(state);
    const view = renderAgentChat();
    const textbox = await getInput();
    await queueMessage(textbox, 'same text');
    await queueMessage(textbox, 'same text');
    state.activeSessionData.status = 'waiting_user';
    rerenderAgentChat(view.rerender);
    await waitFor(() => expect(state.sendMessage.mutateAsync).toHaveBeenCalledTimes(2));
    expect(screen.queryByText('Thinking...')).not.toBeInTheDocument();
  });

  it('keeps a failed head queued, shows an error, and only resumes draining after the failed head is removed', async () => {
    const state = createState();
    state.activeSessionData.status = 'processing';
    state.sendMessage.mutateAsync = vi.fn().mockImplementation(async ({ input: { message } }: { input: { message: string } }) => {
      if (message === 'first queued') {
        state.sendMessage.localError = 'Send failed';
        throw new Error('Send failed');
      }

      return undefined;
    });
    mockFromState(state);

    const view = renderAgentChat();
    const textbox = await getInput();

    await queueMessage(textbox, 'first queued');
    await queueMessage(textbox, 'second queued');

    state.activeSessionData.status = 'waiting_user';
    rerenderAgentChat(view.rerender);

    await waitFor(() => expect(state.sendMessage.mutateAsync).toHaveBeenCalledTimes(1));
    await waitFor(() => expect(screen.getByText('Send failed')).toBeInTheDocument());
    expect(getQueuedTexts()).toEqual(['first queued', 'second queued']);

    fireEvent.click(screen.getAllByTitle('Remove queued message')[0]);

    await waitFor(() => {
      expect(state.sendMessage.mutateAsync).toHaveBeenNthCalledWith(2, {
        input: { message: 'second queued', attachments: [], requestId: expect.any(String) },
        projectId: 'project-1',
        sessionId: 'session-1',
        context: expect.objectContaining({ projectId: 'project-1' }),
      });
    });
  });

  it('keeps the original empty prompt visible while failed queued work is paused', async () => {
    const state = createState();
    state.activeSessionData.status = 'processing';
    state.sendMessage.mutateAsync = vi.fn().mockImplementation(async () => {
      state.sendMessage.localError = 'Send failed';
      throw new Error('Send failed');
    });
    mockFromState(state);

    const view = renderAgentChat();
    const textbox = await getInput();
    await queueMessage(textbox, 'failed queued message');

    state.activeSessionData.status = 'waiting_user';
    rerenderAgentChat(view.rerender);

    await waitFor(() => expect(screen.getByText('Send failed')).toBeInTheDocument());
    expect(screen.getByText('✨ I can do almost anything')).toBeInTheDocument();
    expect(screen.getByText('failed queued message')).toBeInTheDocument();
  });

  it('reorders and deletes queued messages in the rendered stack', async () => {
    const state = createState();
    state.activeSessionData.status = 'processing';
    mockFromState(state);

    renderAgentChat();

    const textbox = await getInput();

    await queueMessage(textbox, 'first');
    await queueMessage(textbox, 'second');
    await queueMessage(textbox, 'third');

    expect(getQueuedTexts()).toEqual(['first', 'second', 'third']);

    fireEvent.click(screen.getAllByTitle('Move queued message down')[0]);
    expect(getQueuedTexts()).toEqual(['second', 'first', 'third']);

    fireEvent.click(screen.getAllByTitle('Remove queued message')[1]);
    expect(getQueuedTexts()).toEqual(['second', 'third']);
  });

  it('keeps an active foreign request read-only through takeover and completion without replaying saved queue work', async () => {
    const state = createState();
    state.projectChats['project-1'].draft = { text: 'Saved text', revision: 4, queued_messages: [
      { id: 'active-request', text: 'Already running', session_id: 'session-1', attachments: [] },
      { id: 'queued-next', text: 'Waiting behind it', session_id: 'session-1', attachments: [] },
    ] };
    state.activeSessionData.status = 'waiting_user'; // Control data must still report the live turn.
    state.activeSessionData.turns = [{ role: 'assistant', content: 'Live assistant update', timestamp: iso(12_000) }];
    state.activeSessionData.control = { role: 'follower', active: true, activeRequestId: 'active-request' };
    state.activeSessionData.durableAcceptedRequestIds = ['active-request'];
    mockFromState(state);

    const view = renderAgentChat();
    await screen.findByText('Live assistant update');
    await screen.findByText('Already running');
    await screen.findByText('In progress in another tab');
    expect(screen.getByRole('button', { name: 'Active in another tab — take over' })).toBeEnabled();
    expect(screen.getByPlaceholderText('Type to queue next message...')).toBeDisabled();
    expect(screen.queryByText(/Delivery not confirmed/)).toBeNull();
    expect(screen.queryByRole('button', { name: 'Retry saved message' })).toBeNull();
    expect(screen.queryByTitle('Stop agent')).toBeNull();
    expect(screen.getByTitle('Voice input (Cmd+Shift+R)')).toBeDisabled();
    expect(screen.queryByRole('combobox', { name: 'Agent model' })).toBeNull();
    expect(getQueuedTexts()).toEqual(['Already running', 'Waiting behind it']);
    expect(state.projectChats['project-1'].draft.queued_messages.map(row => row.id)).toEqual(['active-request', 'queued-next']);
    expect(state.sendMessage.mutateAsync).not.toHaveBeenCalled();
    expect(mocks.useTakeOverSession).toHaveBeenCalledWith('session-1', 'project-1');

    fireEvent.click(screen.getByRole('button', { name: 'Active in another tab — take over' }));
    expect(state.takeOverSession.mutate).toHaveBeenCalledTimes(1);

    state.activeSessionData.control = { role: 'writer', active: true, activeRequestId: 'active-request' };
    rerenderAgentChat(view.rerender);
    expect(await screen.findByText('In progress')).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Active in another tab — take over' })).toBeNull();
    expect(screen.queryByText(/Delivery not confirmed/)).toBeNull();
    expect(state.sendMessage.mutateAsync).not.toHaveBeenCalled();

    state.activeSessionData.control = { role: 'writer', active: false, activeRequestId: null };
    state.activeSessionData.status = 'waiting_user';
    rerenderAgentChat(view.rerender);
    await waitFor(() => expect(state.projectChats['project-1'].draft.queued_messages.map(row => row.id)).toEqual(['queued-next']));
    expect(getQueuedTexts()).toEqual(['Waiting behind it']);
    expect(screen.getByText(/Delivery not confirmed/)).toBeInTheDocument();
    expect(state.sendMessage.mutateAsync).not.toHaveBeenCalled();

    // Another tab may take ownership after this panel has completed its takeover.
    state.activeSessionData.control = { role: 'follower', active: false, activeRequestId: null };
    rerenderAgentChat(view.rerender);
    expect(screen.getByRole('button', { name: 'Active in another tab — take over' })).toBeEnabled();
    expect(screen.getByRole('textbox')).toBeDisabled();
    expect(screen.queryByRole('button', { name: 'Retry saved message' })).toBeNull();
    expect(screen.getByTitle('Remove queued message')).toBeDisabled();
    expect(state.sendMessage.mutateAsync).not.toHaveBeenCalled();
  });

  it('shows the active external session model to a follower with takeover available', async () => {
    const state = createState();
    const sessionId = 'codex:chat-3';
    state.projectChats['project-1'].selected_session_id = sessionId;
    state.projectChats['project-1'].sessions = [{ id: sessionId }];
    state.sessionsData = [{ id: sessionId, status: 'waiting_user' }];
    state.activeSessionData.id = sessionId;
    state.activeSessionData.status = 'waiting_user';
    state.activeSessionData.control = { role: 'follower', active: false, activeRequestId: null };
    mockFromState(state);

    const modelSelection = vi.fn();
    mocks.useSetAgentModel.mockReturnValue({ mutateAsync: modelSelection, isPending: false, error: null });
    const localModels = { currentModelId: 'vendor/alpha-precise', availableModels: [
      { modelId: 'vendor/alpha-precise', name: 'Alpha Precise', description: 'Careful code review' },
      { modelId: 'vendor/beta-fast', name: 'Beta Fast', description: 'Quick drafts' },
    ] };
    mocks.useAgentModels.mockReturnValue({
      data: { currentModel: null, providers: [], localModels },
      isLoading: false,
      error: null,
      refetch: mocks.modelRefetch,
    });

    renderAgentChat();
    const identity = screen.getByTestId('agent-chat-identity');
    expect(identity).toHaveTextContent(/^Codex$/);
    await userEvent.setup().hover(screen.getByRole('button', { name: 'Chat model information' }));
    expect(await screen.findByText('Alpha Precise', { exact: true })).toBeInTheDocument();
    expect(screen.queryByRole('combobox', { name: 'Agent model' })).toBeNull();
    expect(mocks.useAgentModels).toHaveBeenCalledWith(true, sessionId, 'project-1');
    expect(mocks.useSetAgentModel).toHaveBeenLastCalledWith(sessionId, 'project-1');
    expect(screen.getByRole('button', { name: 'Active in another tab — take over' })).toBeEnabled();
    expect(modelSelection).not.toHaveBeenCalled();

    fireEvent.click(screen.getByRole('button', { name: 'Active in another tab — take over' }));
    expect(state.takeOverSession.mutate).toHaveBeenCalledTimes(1);
  });
});


describe('project-only Astrid chat', () => {
  it('enables sending in a project without a timeline and forwards its explicit context', async () => {
    const state = createState();
    state.timelineId = null;
    mockFromState(state);
    const context = { tool: 'video-editor', projectId: 'project-1', projectSlug: 'first', timelineId: null, timelineName: null };
    mocks.useAgentChatBridge.mockReturnValue({ timelineId: null, editorContext: context });
    render(<AgentChatPanel isExpanded />);
    const composer = screen.getByPlaceholderText('Type or press Cmd+Shift+R to talk...');
    expect(composer).not.toBeDisabled();
    fireEvent.change(composer, { target: { value: 'Remember model B for this project' } });
    fireEvent.keyDown(composer, { key: 'Enter', code: 'Enter' });
    await waitFor(() => expect(state.sendMessage.mutateAsync).toHaveBeenCalled());
    expect(mocks.useAgentSessions).toHaveBeenCalledWith(null, 'project-1');
    expect(mocks.useCreateSession).toHaveBeenCalledWith(null, 'project-1', 'ensure');
    expect(mocks.useSendMessage).toHaveBeenCalledWith('session-1', context, 'project-1');
  });
});


describe('project draft consumer ownership', () => {
  it('hydrates each project draft/queue, flushes to its original owner on switch, and reopens retained local text', async () => {
    vi.clearAllMocks();
    mocks.agentSessionsAvailable = true;
    mocks.panesState.isTasksPaneLocked = true;
    const state = createState();
    state.activeSessionData.status = 'processing';
    mockFromState(state);
    const context = (projectId: string) => ({ tool: 'video-editor' as const, projectId, projectSlug: projectId, timelineId: null, timelineName: null });
    let currentProject = 'draft-owner-a';
    mocks.useAgentChatBridge.mockImplementation(() => ({ timelineId: null, editorContext: context(currentProject) }));
    const drafts = new Map(['draft-owner-a', 'draft-owner-b'].map((projectId) => [projectId, {
      project_id: projectId, scope_key: `realm:store:${projectId}`, revision: 1,
      selected_session_id: `session-${projectId}`, sessions: [{ id: `session-${projectId}` }],
      draft: { text: `saved ${projectId}`, revision: 3, queued_messages: [
        { id: `queue-${projectId}`, text: `queued ${projectId}`, session_id: `session-${projectId}`, attachments: [] },
      ] },
    }]));
    mocks.useProjectChat.mockImplementation((projectId: string) => ({ data: drafts.get(projectId), refetch: vi.fn() }));
    mocks.useAgentSessions.mockImplementation((_timelineId: null, projectId: string) => ({ data: [{ id: `session-${projectId}`, status: 'processing' }], isLoading: false }));
    const saved: Array<{ projectId: string; text: string; queuedMessages: Array<{ session_id: string }> }> = [];
    mocks.useSaveProjectDraft.mockImplementation((projectId: string) => ({ isPending: false, mutateAsync: vi.fn(async (input: {
      expectedRevision: number; text: string; queuedMessages: Array<{ id: string; text: string; session_id: string; attachments: never[] }>;
    }) => {
      saved.push({ projectId, text: input.text, queuedMessages: input.queuedMessages });
      const previous = drafts.get(projectId)!;
      const next = { ...previous, draft: { text: input.text, revision: input.expectedRevision + 1, queued_messages: input.queuedMessages } };
      drafts.set(projectId, next); return next;
    }) }));
    const view = renderAgentChat();
    try {
      await waitFor(() => expect(screen.getByRole('textbox')).toHaveValue('saved draft-owner-a'));
      expect(getQueuedTexts()).toEqual(['queued draft-owner-a']);
      fireEvent.change(screen.getByRole('textbox'), { target: { value: 'local text for A' } });
      currentProject = 'draft-owner-b';
      rerenderAgentChat(view.rerender);
      await waitFor(() => expect(screen.getByRole('textbox')).toHaveValue('saved draft-owner-b'));
      await waitFor(() => expect(saved).toContainEqual(expect.objectContaining({ projectId: 'draft-owner-a', text: 'local text for A' })));
      expect(getQueuedTexts()).toEqual(['queued draft-owner-b']);
      expect(mocks.useSendMessage).toHaveBeenCalledWith('session-draft-owner-b', context('draft-owner-b'), 'draft-owner-b');
      fireEvent.change(screen.getByRole('textbox'), { target: { value: 'local text for B' } });
      currentProject = 'draft-owner-a';
      rerenderAgentChat(view.rerender);
      await waitFor(() => expect(screen.getByRole('textbox')).toHaveValue('local text for A'));
      await waitFor(() => expect(saved).toContainEqual(expect.objectContaining({ projectId: 'draft-owner-b', text: 'local text for B' })));
      expect(getQueuedTexts()).toEqual(['queued draft-owner-a']);
      expect(saved.every(({ projectId, queuedMessages }) => queuedMessages.every(item => item.session_id === `session-${projectId}`))).toBe(true);
      expect(state.sendMessage.mutateAsync).not.toHaveBeenCalled();
    } finally { view.unmount(); }
  });

  it.each(['plain', 'another agent'])('keeps New (%s) on the new registry snapshot while the sessions cache is stale', async (choice) => {
    vi.clearAllMocks();
    Element.prototype.scrollIntoView ??= vi.fn();
    Object.defineProperty(HTMLElement.prototype, 'scrollTo', { configurable: true, value: vi.fn() });
    vi.spyOn(window, 'requestAnimationFrame').mockImplementation(callback => { callback(0); return 1; });
    const state = createState();
    mockFromState(state);
    const openPane = vi.fn();
    mocks.panesState.setIsTasksPaneOpen = openPane;
    state.projectChats['project-1'] = { ...state.projectChats['project-1'], main_session_id: 'session-1' } as typeof state.projectChats['project-1'];
    const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const key = ['project-agent-chat', 'project-1'];
    client.setQueryData(key, state.projectChats['project-1']);
    mocks.useProjectChat.mockImplementation(() => useQuery({ queryKey: key, queryFn: async () => state.projectChats['project-1'], enabled: false }));
    mocks.useLocalAgents.mockReturnValue({ data: { agents: [{ id: 'codex', name: 'Codex', state: 'ready', line: null }], selectedAgent: 'astrid' }, refetch: vi.fn() });
    let finish!: (session: { id: string }) => void;
    state.createSession.mutateAsync.mockImplementationOnce(() => new Promise(resolve => { finish = resolve; }));
    const newId = choice === 'plain' ? 'session-2' : 'codex:session-2';
    mocks.useAgentSession.mockImplementation((id: string) => ({ data: { id, status: 'waiting_user', turns: [] }, isLoading: false }));
    const view = render(<QueryClientProvider client={client}><AgentChatPanel /></QueryClientProvider>);
    const composer = screen.getByRole('textbox');
    fireEvent.change(composer, { target: { value: 'Keep my unsent draft' } });
    await waitFor(() => expect(mocks.useAgentSession).toHaveBeenLastCalledWith('session-1', 'project-1'));
    if (choice === 'plain') fireEvent.click(screen.getByRole('button', { name: 'New chat', exact: true }));
    else {
      fireEvent.click(screen.getByRole('button', { name: 'New chat with…' }));
      fireEvent.click(await screen.findByRole('option', { name: /^Codex/ }));
    }
    await waitFor(() => expect(state.createSession.mutateAsync).toHaveBeenCalledOnce());
    // useCreateSession publishes its registry receipt before handleNewSession's
    // local selection applies. Commit that snapshot while the separate 5s
    // sessions query still contains only Chat 1, with no creation receipt in UI state.
    const created = {
      ...state.projectChats['project-1'],
      selected_session_id: newId,
      main_session_id: newId,
      sessions: [{ id: 'session-1' }, { id: newId }],
      revision: state.projectChats['project-1'].revision + 1,
    };
    await act(async () => { client.setQueryData(key, created); });
    const selector = screen.getByRole('combobox', { name: 'Project chat session' });
    expect(selector).toBeDisabled();
    await act(async () => { finish({ id: newId }); });
    expect(selector).not.toBeDisabled();
    expect(composer).toHaveFocus();
    fireEvent.click(selector);
    expect(await screen.findByRole('option', { name: /^Chat 2/ })).toHaveTextContent('Main');
    fireEvent.click(selector);
    await waitFor(() => expect(mocks.useAgentSession).toHaveBeenLastCalledWith(newId, 'project-1'));
    expect(selector).toHaveTextContent('Chat 2');
    view.rerender(<QueryClientProvider client={client}><AgentChatPanel isExpanded /></QueryClientProvider>);
    expect(mocks.useAgentSession).toHaveBeenLastCalledWith(newId, 'project-1');
    expect(state.createSession.mutate).not.toHaveBeenCalled();
    expect(composer).toHaveValue('Keep my unsent draft');
    expect(openPane).toHaveBeenCalledWith(true);
    expect(state.sessionsData).toEqual([
      { id: 'session-1', status: 'waiting_user' },
    ]);
    expect(state.sendMessage.mutateAsync).not.toHaveBeenCalled();
    view.unmount();
    client.clear();
  });
  it.each([false, true])('ignores a delayed New completion after a project transition (return to origin: %s)', async (returnToOrigin) => {
    const state = createState();
    mockFromState(state);
    const openPane = vi.fn();
    mocks.panesState.setIsTasksPaneOpen = openPane;
    mocks.useAgentSession.mockImplementation((id: string) => ({ data: { id, status: 'waiting_user', turns: [] }, isLoading: false }));
    let finish!: (value: { id: string }) => void;
    state.createSession.mutateAsync.mockImplementationOnce(() => new Promise(resolve => { finish = resolve; }));
    const view = renderAgentChat();
    await waitFor(() => expect(mocks.useAgentSession).toHaveBeenLastCalledWith('session-1', 'project-1'));
    fireEvent.click(screen.getByRole('button', { name: 'New chat', exact: true }));
    state.projectId = 'project-2';
    rerenderAgentChat(view.rerender);
    if (returnToOrigin) { state.projectId = 'project-1'; rerenderAgentChat(view.rerender); }
    fireEvent.change(screen.getByRole('textbox'), { target: { value: 'Current project draft' } });
    await act(async () => { finish({ id: 'late-project-1-session' }); });
    expect(mocks.useAgentSession).not.toHaveBeenLastCalledWith('late-project-1-session', state.projectId);
    expect(screen.getByRole('textbox')).toHaveValue('Current project draft');
    expect(openPane).not.toHaveBeenCalled();
    expect(state.sendMessage.mutateAsync).not.toHaveBeenCalled();
    view.unmount();
  });
  it('keeps the prior chat and unsent composer when creation fails', async () => {
    vi.clearAllMocks();
    const state = createState();
    mockFromState(state);
    state.createSession.mutateAsync.mockRejectedValue(new Error('Connection lost'));
    render(<AgentChatPanel />);
    const composer = screen.getByRole('textbox');
    fireEvent.change(composer, { target: { value: 'Still my draft' } });
    await waitFor(() => expect(mocks.useAgentSession).toHaveBeenLastCalledWith('session-1', 'project-1'));
    fireEvent.click(screen.getByRole('button', { name: 'New chat', exact: true }));
    await waitFor(() => expect(state.createSession.mutateAsync).toHaveBeenCalledOnce());
    expect(mocks.useAgentSession).toHaveBeenLastCalledWith('session-1', 'project-1');
    expect(composer).toHaveValue('Still my draft');
    expect(state.sendMessage.mutateAsync).not.toHaveBeenCalled();
  });
});
