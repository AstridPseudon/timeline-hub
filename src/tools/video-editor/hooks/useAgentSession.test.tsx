// @vitest-environment jsdom
import React from 'react';
import { focusManager, QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { act, renderHook, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import {
  appendAcpAssistantDraft,
  appendAcpTextTurn,
  AstridAgentSessionStore,
  extractAstridElementOperations,
  isTimelineAgentSessionsAvailable,
  projectChatQueryKey,
  stripAstridEditorContext,
  useCancelSession,
  useCreateSession,
  useProjectChat,
  useRenameProjectSession,
  useSaveProjectDraft,
  useSelectProjectSession,
  useSetMainProjectSession,
  useSendMessage,
  useAgentSession,
  useAgentModels,
  useSetAgentModel,
  useTakeOverSession,
  useLocalAgents,
  localAgentsQueryKey,
  agentSessionQueryKey,
} from './useAgentSession.ts';
import type { ProjectChatState } from '@/integrations/astrid/acpRoutes.ts';
import { BridgeRouteError } from '@/integrations/astrid/transport.ts';
import { LOCAL_AGENT_IDS, LOCAL_AGENT_SETTING_KEY, LOCAL_AGENT_TABLE, localAgentModelSettingKey, saveLocalAgent, savedLocalAgent, savedLocalAgentModel } from '@/integrations/astrid/localAgents.ts';

function wrapper({ children }: { children: React.ReactNode }) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return React.createElement(QueryClientProvider, { client }, children);
}

function wrapperWithClient(client: QueryClient) {
  return function QueryClientWrapper({ children }: { children: React.ReactNode }) {
    return React.createElement(QueryClientProvider, { client }, children);
  };
}

function createStorage(): Storage {
  const values = new Map<string, string>();
  return {
    get length() { return values.size; },
    clear: () => values.clear(),
    getItem: (key) => values.get(key) ?? null,
    key: (index) => [...values.keys()][index] ?? null,
    removeItem: (key) => { values.delete(key); },
    setItem: (key, value) => { values.set(key, String(value)); },
  };
}

let testStorage: Storage;
beforeEach(() => {
  testStorage = createStorage();
  vi.stubGlobal('localStorage', testStorage);
});

afterEach(() => {
  vi.restoreAllMocks();
  testStorage.removeItem(LOCAL_AGENT_SETTING_KEY);
  for (const agent of LOCAL_AGENT_IDS) testStorage.removeItem(localAgentModelSettingKey(agent));
  vi.unstubAllGlobals();
});

describe('timeline agent ACP chat', () => {
  it.each([
    ['load', 'not_found'], ['events', 'not_found'],
    ['load', 'connection_not_found'], ['events', 'connection_not_found'],
  ])('reconnects a lost bridge during %s (%s) without sending a prompt', async (stage, code) => {
    const missing = new BridgeRouteError('ACP events', 404, { error: code, detail: 'ACP connection is not available; reconnect' });
    const acp = {
      projectChat: vi.fn(async () => ({ project_id: 'p', sessions: [{ id: 'chat-1' }] })),
      connect: vi.fn().mockResolvedValueOnce({ connection_id: 'old' }).mockResolvedValue({ connection_id: 'new' }),
      loadSession: vi.fn(async (id: string) => { if (id === 'old' && stage === 'load') throw missing; return {}; }),
      events: vi.fn(async (id: string) => { if (id === 'old' && stage === 'events') throw missing; return { notifications: [], disconnected: false }; }),
      promptProjectSession: vi.fn(),
    };
    const store = new AstridAgentSessionStore({ acp } as never);
    expect((await store.get('p', 'chat-1')).id).toBe('chat-1');
    expect(acp.connect).toHaveBeenCalledTimes(2);
    expect(acp.loadSession).toHaveBeenLastCalledWith('new', 'chat-1');
    expect(acp.promptProjectSession).not.toHaveBeenCalled();
  });

  it('stops read-only recovery after one fresh connection also disappears', async () => {
    const missing = new BridgeRouteError('ACP rpc', 404, { error: 'connection_not_found', detail: 'ACP connection expired while idle; reconnect' });
    const acp = {
      projectChat: vi.fn(async () => ({ project_id: 'p', sessions: [{ id: 'chat-1' }] })),
      connect: vi.fn(async () => ({ connection_id: 'missing' })),
      loadSession: vi.fn(async () => { throw missing; }),
    };
    await expect(new AstridAgentSessionStore({ acp } as never).get('p', 'chat-1')).rejects.toBe(missing);
    expect(acp.connect).toHaveBeenCalledTimes(2);
  });

  it('does not reconnect or hide an unknown saved session', async () => {
    const missing = new BridgeRouteError('ACP rpc', 404, { error: 'not_found', detail: 'ACP session not found: chat-1' });
    const acp = {
      projectChat: vi.fn(async () => ({ project_id: 'p', sessions: [{ id: 'chat-1' }] })),
      connect: vi.fn(async () => ({ connection_id: 'valid' })),
      loadSession: vi.fn(async () => { throw missing; }),
    };
    await expect(new AstridAgentSessionStore({ acp } as never).get('p', 'chat-1')).rejects.toBe(missing);
    expect(acp.connect).toHaveBeenCalledTimes(1);
  });

  it('streams live follower turns without recording replay receipts, blocks writes, and takes over explicitly', async () => {
    const projectChat = { project_id: 'p', scope_key: 'project:p', revision: 1, selected_session_id: 'chat-1', sessions: [{ id: 'chat-1' }], draft: { text: '', revision: 1, queued_messages: [] } };
    let eventsRead = false;
    const acp = {
      connect: vi.fn(async () => ({ connection_id: 'follower-connection' })),
      projectChat: vi.fn(async () => projectChat),
      loadSession: vi.fn(async () => ({ _astridSession: { role: 'follower', active: true, activeRequestId: 'remote-request' } })),
      events: vi.fn(async () => {
        if (eventsRead) return { disconnected: false, notifications: [] };
        eventsRead = true;
        return { disconnected: false, notifications: [
          { jsonrpc: '2.0', method: 'session/update', params: { sessionId: 'chat-1', update: { sessionUpdate: 'user_message_chunk', live: true, requestId: 'remote-request', messageId: 'astrid-live:remote-request', content: { type: 'text', text: 'Remote request' } } } },
          { jsonrpc: '2.0', method: 'session/update', params: { sessionId: 'chat-1', update: { sessionUpdate: 'agent_message_chunk', messageId: 'remote-reply', content: { type: 'text', text: 'Remote reply' } } } },
        ] };
      }),
      promptProjectSession: vi.fn(),
      cancelSession: vi.fn(),
      takeOverSession: vi.fn(async () => ({ _astridSession: { role: 'writer', active: false, activeRequestId: null } })),
    };
    const store = new AstridAgentSessionStore({ acp } as never);
    const follower = await store.get('p', 'chat-1');
    expect(follower.control).toEqual({ role: 'follower', active: true, activeRequestId: 'remote-request' });
    expect(follower.status).toBe('processing');
    expect(follower.turns).toEqual([
      expect.objectContaining({ role: 'user', content: 'Remote request', request_id: 'remote-request', messageId: 'astrid-live:remote-request' }),
      expect.objectContaining({ role: 'assistant', content: 'Remote reply', messageId: 'remote-reply' }),
    ]);
    expect(follower.durableAcceptedRequestIds).not.toContain('remote-request');
    await expect(store.prompt('chat-1', { message: 'duplicate' }, { tool: 'video-editor', projectId: 'p', projectSlug: null, timelineId: null, timelineName: null })).rejects.toThrow('Take over');
    await expect(store.cancel('chat-1')).rejects.toThrow('Take over');
    expect(acp.promptProjectSession).not.toHaveBeenCalled();
    expect(acp.cancelSession).not.toHaveBeenCalled();
    const owned = await store.takeOver('p', 'chat-1');
    expect(acp.takeOverSession).toHaveBeenCalledWith('follower-connection', 'chat-1');
    expect(owned.control).toEqual({ role: 'writer', active: false, activeRequestId: null });
    expect(owned.turns).toHaveLength(2);
  });

  it('keeps live assistant output when the current writer is taken over mid-turn', async () => {
    const projectChat = { project_id: 'p', scope_key: 'project:p', revision: 1, selected_session_id: 'chat-2', sessions: [{ id: 'chat-2' }], draft: { text: '', revision: 1, queued_messages: [] } };
    const requestId = 'writer-request';
    let promptReturned = false;
    const acp = {
      connect: vi.fn(async () => ({ connection_id: 'writer-connection' })),
      projectChat: vi.fn(async () => projectChat),
      loadSession: vi.fn(async () => ({ _astridSession: { role: 'writer', active: false, activeRequestId: null } })),
      events: vi.fn(async () => {
        if (!promptReturned) return { disconnected: false, notifications: [] };
        promptReturned = false;
        return { disconnected: false, notifications: [
          { jsonrpc: '2.0', method: 'session/update', params: { sessionId: 'chat-2', update: { sessionUpdate: 'astrid_session_control', role: 'follower', active: true, activeRequestId: requestId } } },
          { jsonrpc: '2.0', method: 'session/update', params: { sessionId: 'chat-2', update: { sessionUpdate: 'agent_message_chunk', live: true, messageId: 'reply-2', content: { type: 'text', text: 'Streamed once' } } } },
        ] };
      }),
      promptProjectSession: vi.fn(async () => { promptReturned = true; return {}; }),
    };
    const store = new AstridAgentSessionStore({ acp } as never);
    await store.prompt('chat-2', { message: 'hello', requestId }, { tool: 'video-editor', projectId: 'p', projectSlug: null, timelineId: null, timelineName: null });
    const saved = await store.get('p', 'chat-2');
    expect(acp.promptProjectSession).toHaveBeenCalledWith('p', 'writer-connection', 'chat-2', expect.any(Array), requestId);
    expect(saved.turns.filter(turn => turn.role === 'assistant')).toEqual([expect.objectContaining({ content: 'Streamed once', messageId: 'reply-2' })]);
    expect(saved.control).toEqual({ role: 'follower', active: true, activeRequestId: requestId });
    expect(saved.status).toBe('processing');
  });

  it('allows the active writer to cancel and lets its prompt finish across active control updates', async () => {
    const projectChat = { project_id: 'p', scope_key: 'project:p', revision: 1, selected_session_id: 'chat-active', sessions: [{ id: 'chat-active' }], draft: { text: '', revision: 1, queued_messages: [] } };
    let releasePrompt!: () => void;
    let notification: unknown;
    const promptWait = new Promise<void>(resolve => { releasePrompt = resolve; });
    const acp = {
      connect: vi.fn(async () => ({ connection_id: 'active-connection' })),
      projectChat: vi.fn(async () => projectChat),
      loadSession: vi.fn(async () => ({ _astridSession: { role: 'writer', active: false, activeRequestId: null } })),
      events: vi.fn(async () => ({ disconnected: false, notifications: notification ? [notification] : [] })),
      promptProjectSession: vi.fn(async () => { await promptWait; return {}; }),
      cancelSession: vi.fn(async () => ({})),
    };
    const store = new AstridAgentSessionStore({ acp } as never);
    const prompt = store.prompt('chat-active', { message: 'hello', requestId: 'local-request' }, { tool: 'video-editor', projectId: 'p', projectSlug: null, timelineId: null, timelineName: null });
    await vi.waitFor(() => expect(acp.promptProjectSession).toHaveBeenCalled());
    notification = { jsonrpc: '2.0', method: 'session/update', params: { sessionId: 'chat-active', update: { sessionUpdate: 'astrid_session_control', role: 'writer', active: true, activeRequestId: 'local-request' } } };
    await store.get('p', 'chat-active');
    await expect(store.cancel('chat-active')).resolves.toBeUndefined();
    notification = { jsonrpc: '2.0', method: 'session/update', params: { sessionId: 'chat-active', update: { sessionUpdate: 'astrid_session_control', role: 'writer', active: false, activeRequestId: null } } };
    releasePrompt();
    await expect(prompt).resolves.toBeUndefined();
  });

  it('returns quietly when takeover arrives during an in-flight writer prompt', async () => {
    const projectChat = { project_id: 'p', scope_key: 'project:p', revision: 1, selected_session_id: 'chat-taken', sessions: [{ id: 'chat-taken' }], draft: { text: '', revision: 1, queued_messages: [] } };
    let releasePrompt!: () => void;
    const notification: { value: unknown } = { value: undefined };
    const promptWait = new Promise<void>(resolve => { releasePrompt = resolve; });
    const acp = {
      connect: vi.fn(async () => ({ connection_id: 'taken-connection' })),
      projectChat: vi.fn(async () => projectChat),
      loadSession: vi.fn(async () => ({ _astridSession: { role: 'writer', active: false, activeRequestId: null } })),
      events: vi.fn(async () => ({ disconnected: false, notifications: notification.value ? [notification.value] : [] })),
      promptProjectSession: vi.fn(async () => { await promptWait; return {}; }),
    };
    const store = new AstridAgentSessionStore({ acp } as never);
    const prompt = store.prompt('chat-taken', { message: 'hello', requestId: 'remote-request' }, { tool: 'video-editor', projectId: 'p', projectSlug: null, timelineId: null, timelineName: null });
    await vi.waitFor(() => expect(acp.promptProjectSession).toHaveBeenCalled());
    notification.value = { jsonrpc: '2.0', method: 'session/update', params: { sessionId: 'chat-taken', update: { sessionUpdate: 'astrid_session_control', role: 'follower', active: true, activeRequestId: 'remote-request' } } };
    await store.get('p', 'chat-taken');
    releasePrompt();
    await expect(prompt).resolves.toBeUndefined();
    expect(acp.promptProjectSession).toHaveBeenCalledTimes(1);
  });

  it('does not replay a request already active in a follower session', async () => {
    const get = vi.spyOn(AstridAgentSessionStore.prototype, 'get').mockResolvedValue({
      id: 'chat-3', status: 'processing', turns: [], taskLinks: [],
      control: { role: 'follower', active: true, activeRequestId: 'queued-request' },
    } as never);
    const hook = renderHook(() => useSendMessage('chat-3', { tool: 'video-editor', projectId: 'p', projectSlug: null, timelineId: null, timelineName: null }, 'p'), { wrapper });
    await expect(hook.result.current.checkAcceptedRequest('queued-request')).resolves.toBe(false);
    expect(get).toHaveBeenCalledTimes(1);
    expect(get).toHaveBeenCalledWith('p', 'chat-3');
    hook.unmount();
  });

  it('persists a ready local agent default and rejects non-ready choices', async () => {
    const acp = {
      agents: vi.fn(async () => ({ agents: [
        { id: 'claude-code', name: 'Claude Code', state: 'ready' as const, line: null },
        { id: 'codex', name: 'Codex', state: 'sign-in' as const, line: LOCAL_AGENT_TABLE.codex.signInLine },
      ] })),
    };
    const store = new AstridAgentSessionStore({ acp } as never);
    localStorage.removeItem(LOCAL_AGENT_SETTING_KEY);
    await store.setAgent('claude-code');
    expect(localStorage.getItem(LOCAL_AGENT_SETTING_KEY)).toBe('claude-code');
    await expect(store.setAgent('codex')).rejects.toThrow('not signed in');
    acp.agents.mockResolvedValue({ agents: [{ id: 'claude-code', name: 'Claude Code', state: 'not-installed', line: LOCAL_AGENT_TABLE['claude-code'].notInstalledLine! }] });
    await expect(store.setAgent('claude-code')).rejects.toThrow('not installed');
  });

  it('updates mounted agent selection when the shared default saver runs', async () => {
    const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    vi.spyOn(AstridAgentSessionStore.prototype, 'agents').mockImplementation(async () => ({
      agents: [{ id: 'hermes', name: 'Hermes', state: 'ready', line: null }],
      selectedAgent: savedLocalAgent(),
    }));
    client.setQueryData(localAgentsQueryKey, {
      agents: [{ id: 'hermes', name: 'Hermes', state: 'ready' as const, line: null }],
      selectedAgent: 'astrid' as const,
    });
    const hook = renderHook(() => useLocalAgents(), { wrapper: wrapperWithClient(client) });
    await waitFor(() => expect(hook.result.current.data?.selectedAgent).toBe('astrid'));

    act(() => saveLocalAgent('hermes'));
    await waitFor(() => expect(hook.result.current.data?.selectedAgent).toBe('hermes'));
    expect(localStorage.getItem(LOCAL_AGENT_SETTING_KEY)).toBe('hermes');
    hook.unmount();
  });

  it.each(['claude-code', 'codex', 'hermes'] as const)('routes saved sessions by their original agent while new sessions use the saved %s default', async (agent) => {
    saveLocalAgent(agent);
    const newSessionId = `${agent}:new-1`;
    const connects: Array<string | undefined> = [];
    const projectChat = { project_id: 'p', revision: 1, selected_session_id: null, main_session_id: null, sessions: [], draft: { revision: 1 } };
    const acp = {
      connect: vi.fn(async (agent?: string) => { connects.push(agent); return { connection_id: `conn-${agent ?? 'astrid'}` }; }),
      createProjectSession: vi.fn(async (_project: string, _connection: string) => ({ ...projectChat, operation_session_id: newSessionId, selected_session_id: newSessionId, sessions: [{ id: newSessionId }] })),
      projectChat: vi.fn(async (project: string) => ({ ...projectChat, project_id: project, sessions: [{ id: 'astrid-old' }, { id: newSessionId }] })),
      loadSession: vi.fn(async () => ({})),
      events: vi.fn(async () => ({ disconnected: false, notifications: [] })),
    };
    const store = new AstridAgentSessionStore({ acp } as never);
    await store.create('p', 'new', 'op-1');
    await store.get('p', 'astrid-old');
    await store.get('p', newSessionId);
    expect(connects).toEqual([agent, undefined]);
    expect(acp.loadSession.mock.calls.map(call => call[0])).toEqual(['conn-astrid', `conn-${agent}`]);
  });

  it('lists saved Astrid chats without connecting to an unavailable selected default', async () => {
    localStorage.setItem(LOCAL_AGENT_SETTING_KEY, 'codex');
    const connects: Array<string | undefined> = [];
    const chat = { project_id: 'p', revision: 1, selected_session_id: 'astrid-saved', main_session_id: 'astrid-saved', sessions: [{ id: 'astrid-saved' }], draft: { revision: 1 } };
    const acp = {
      projectChat: vi.fn(async () => chat),
      connect: vi.fn(async (agent?: string) => {
        connects.push(agent);
        if (agent === 'codex') throw new Error('Codex adapter is unavailable');
        return { connection_id: 'conn-astrid' };
      }),
      loadSession: vi.fn(async () => ({})),
      events: vi.fn(async () => ({ disconnected: false, notifications: [] })),
    };
    const store = new AstridAgentSessionStore({ acp } as never);
    await expect(store.list('p')).resolves.toEqual([{ id: 'astrid-saved', status: 'waiting_user' }]);
    expect(connects).toEqual([]);
    await store.get('p', 'astrid-saved');
    expect(connects).toEqual([undefined]);
    expect(acp.loadSession).toHaveBeenCalledWith('conn-astrid', 'astrid-saved');
  });

  it('keeps ensure_main on the existing main session agent after the default changes', async () => {
    localStorage.setItem(LOCAL_AGENT_SETTING_KEY, 'claude-code');
    const connects: Array<string | undefined> = [];
    const priorChat = { project_id: 'p', revision: 1, selected_session_id: 'astrid-selected', main_session_id: 'codex:main', sessions: [{ id: 'astrid-selected' }, { id: 'codex:main' }], draft: { revision: 1 } };
    const acp = {
      projectChat: vi.fn(async () => priorChat),
      connect: vi.fn(async (agent?: string) => { connects.push(agent); return { connection_id: `conn-${agent ?? 'astrid'}` }; }),
      createProjectSession: vi.fn(async () => priorChat),
      events: vi.fn(async () => ({ disconnected: false, notifications: [] })),
    };
    const store = new AstridAgentSessionStore({ acp } as never);
    await store.create('p', 'ensure_main', 'op-2');
    expect(connects).toEqual(['codex']);
  });

  it('loads the model catalog and refreshes it after a model selection', async () => {
    let currentModel = 'deepseek/deepseek-chat';
    const models = vi.spyOn(AstridAgentSessionStore.prototype, 'models').mockImplementation(async () => ({
      currentModel,
      providers: [{ id: 'deepseek', name: 'DeepSeek', signedIn: true, models: [{ id: 'deepseek-chat', name: 'DeepSeek' }] }],
    }));
    const setModel = vi.spyOn(AstridAgentSessionStore.prototype, 'setModel').mockImplementation(async model => {
      currentModel = model;
      return { currentModel };
    });
    const hook = renderHook(() => ({ models: useAgentModels(), selection: useSetAgentModel() }), { wrapper });
    try {
      await waitFor(() => expect(hook.result.current.models.data?.currentModel).toBe('deepseek/deepseek-chat'));
      await act(async () => { await hook.result.current.selection.mutateAsync('openai-codex/gpt-5'); });
      await waitFor(() => expect(hook.result.current.models.data?.currentModel).toBe('openai-codex/gpt-5'));
      expect(setModel).toHaveBeenCalledWith('openai-codex/gpt-5');
      expect(models).toHaveBeenCalledTimes(2);
    } finally {
      hook.unmount();
    }
  });

  it('uses the active chat agent for session models and switches its exact model without reconnecting', async () => {
    localStorage.setItem(LOCAL_AGENT_SETTING_KEY, 'claude-code');
    const chat = { project_id: 'p', revision: 1, selected_session_id: 'codex:chat-1', main_session_id: null, sessions: [{ id: 'codex:chat-1' }], draft: { revision: 1 } };
    const acp = {
      projectChat: vi.fn(async () => chat),
      connect: vi.fn(async () => ({ connection_id: 'codex-connection' })),
      loadSession: vi.fn(async () => ({})),
      events: vi.fn(async () => ({ notifications: [], disconnected: false })),
      sessionModels: vi.fn(async (_connectionId: string, sessionId: string) => ({ models: { currentModelId: `${sessionId}/model-a`, availableModels: [{ modelId: 'provider/model-a', name: 'Model A' }] } })),
      setSessionModel: vi.fn(async (_connectionId: string, _sessionId: string, modelId: string) => ({ models: { currentModelId: modelId, availableModels: [{ modelId, name: 'Model' }] } })),
    };
    const store = new AstridAgentSessionStore({ acp } as never);
    await expect(store.models('codex:chat-1', 'p')).resolves.toMatchObject({ localModels: { currentModelId: 'codex:chat-1/model-a' } });
    await expect(store.setModel('provider/model-exact', 'codex:chat-1', 'p')).resolves.toEqual({ currentModel: 'provider/model-exact' });
    expect(acp.connect).toHaveBeenCalledOnce();
    expect(acp.connect).toHaveBeenCalledWith('codex', undefined);
    expect(acp.loadSession).toHaveBeenCalledWith('codex-connection', 'codex:chat-1');
    expect(acp.sessionModels).toHaveBeenCalledWith('codex-connection', 'codex:chat-1');
    expect(acp.setSessionModel).toHaveBeenCalledWith('codex-connection', 'codex:chat-1', 'provider/model-exact', 'p');
    expect(acp).not.toHaveProperty('models');
  });

  it('stores model defaults per agent and passes the saved preference when a fresh store connects', async () => {
    localStorage.setItem(LOCAL_AGENT_SETTING_KEY, 'claude-code');
    const chat = { project_id: 'p', revision: 1, selected_session_id: 'codex:chat-2', main_session_id: null, sessions: [{ id: 'codex:chat-2' }], draft: { revision: 1 } };
    const makeClient = () => ({ acp: {
      projectChat: vi.fn(async () => chat),
      connect: vi.fn(async () => ({ connection_id: 'conn' })),
      loadSession: vi.fn(async () => ({})),
      events: vi.fn(async () => ({ notifications: [], disconnected: false })),
      setSessionModel: vi.fn(async (_connectionId: string, _sessionId: string, modelId: string) => ({ models: { currentModelId: modelId, availableModels: [] } })),
      sessionModels: vi.fn(async () => ({ models: { currentModelId: 'model', availableModels: [] } })),
    } });
    const firstClient = makeClient();
    const firstStore = new AstridAgentSessionStore(firstClient as never);
    await firstStore.setModel('codex-preference', 'codex:chat-2', 'p');
    expect(savedLocalAgentModel('codex')).toBe('codex-preference');
    expect(savedLocalAgentModel('claude-code')).toBeUndefined();

    const freshClient = makeClient();
    const freshStore = new AstridAgentSessionStore(freshClient as never);
    await freshStore.models('codex:chat-2', 'p');
    expect(freshClient.acp.connect).toHaveBeenCalledWith('codex', 'codex-preference');
  });

  it('does not replace a saved model preference when the session switch fails', async () => {
    localStorage.setItem(localAgentModelSettingKey('codex'), 'old-model');
    const chat = { project_id: 'p', revision: 1, selected_session_id: 'codex:chat-3', main_session_id: null, sessions: [{ id: 'codex:chat-3' }], draft: { revision: 1 } };
    const store = new AstridAgentSessionStore({ acp: {
      projectChat: vi.fn(async () => chat), connect: vi.fn(async () => ({ connection_id: 'conn' })), loadSession: vi.fn(async () => ({})), events: vi.fn(async () => ({ notifications: [], disconnected: false })),
      setSessionModel: vi.fn(async () => { throw new Error('switch failed'); }),
    } } as never);
    await expect(store.setModel('new-model', 'codex:chat-3', 'p')).rejects.toThrow('switch failed');
    expect(savedLocalAgentModel('codex')).toBe('old-model');
  });

  it('returns the empty local-model fallback without opening a session when no local chat is active', async () => {
    localStorage.setItem(LOCAL_AGENT_SETTING_KEY, 'codex');
    const connect = vi.fn();
    const store = new AstridAgentSessionStore({ acp: { connect } } as never);
    await expect(store.models()).resolves.toEqual({ providers: [], currentModel: null, localModels: null });
    expect(connect).not.toHaveBeenCalled();
  });

  it('keeps the model query scoped to the active session and refreshes it after a switch', async () => {
    const catalogs: string[] = [];
    const models = vi.spyOn(AstridAgentSessionStore.prototype, 'models').mockImplementation(async (sessionId) => {
      catalogs.push(sessionId ?? 'default');
      return { providers: [], currentModel: null, localModels: { currentModelId: sessionId === 'codex:chat-a' ? 'model-a' : 'model-b', availableModels: [] } };
    });
    const setModel = vi.spyOn(AstridAgentSessionStore.prototype, 'setModel').mockImplementation(async model => ({ currentModel: model }));
    const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const hook = renderHook(({ sessionId }: { sessionId: string }) => ({ models: useAgentModels(true, sessionId, 'p'), selection: useSetAgentModel(sessionId, 'p') }), {
      wrapper: wrapperWithClient(client), initialProps: { sessionId: 'codex:chat-a' },
    });
    try {
      await waitFor(() => expect(hook.result.current.models.data?.localModels?.currentModelId).toBe('model-a'));
      hook.rerender({ sessionId: 'codex:chat-b' });
      await waitFor(() => expect(hook.result.current.models.data?.localModels?.currentModelId).toBe('model-b'));
      expect(client.getQueryData(['agent-models', 'codex:chat-a', 'p'])).toMatchObject({ localModels: { currentModelId: 'model-a' } });
      const beforeSwitch = catalogs.length;
      await act(async () => { await hook.result.current.selection.mutateAsync('model-b2'); });
      await waitFor(() => expect(catalogs.length).toBeGreaterThan(beforeSwitch));
      expect(setModel).toHaveBeenCalledWith('model-b2', 'codex:chat-b', 'p');
    } finally {
      hook.unmount();
      client.clear();
    }
  });

  it('refreshes a follower model catalog from live model updates and blocks model changes', async () => {
    const sessionId = 'codex:chat-model-follower';
    const project = { project_id: 'p', scope_key: 'project:p', revision: 1, selected_session_id: sessionId, sessions: [{ id: sessionId }], draft: { text: '', revision: 1, queued_messages: [] } };
    let eventPending = true;
    const acp = {
      connect: vi.fn(async () => ({ connection_id: 'model-connection' })),
      projectChat: vi.fn(async () => project),
      loadSession: vi.fn(async () => ({ _astridSession: { role: 'follower', active: true, activeRequestId: 'remote-model-turn' } })),
      events: vi.fn(async () => ({ disconnected: false, notifications: eventPending ? (eventPending = false, [{ jsonrpc: '2.0', method: 'session/update', params: { sessionId, update: { sessionUpdate: 'current_model_update', currentModelId: 'model-b', models: { currentModelId: 'model-b', availableModels: [{ modelId: 'model-b', name: 'Model B' }] } } } }]) : [] })),
      sessionModels: vi.fn(async () => ({ models: { currentModelId: 'model-b', availableModels: [{ modelId: 'model-b', name: 'Model B' }] } })),
      setSessionModel: vi.fn(),
    };
    const store = new AstridAgentSessionStore({ acp } as never);
    const catalogs = vi.spyOn(AstridAgentSessionStore.prototype, 'models').mockImplementation(async () => ({ providers: [], currentModel: null, localModels: { currentModelId: eventPending ? 'model-a' : 'model-b', availableModels: [] } }));
    const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    client.setQueryData(agentSessionQueryKey(sessionId, 'p'), { id: sessionId, status: 'processing', turns: [], taskLinks: [], control: { role: 'follower', active: true, activeRequestId: 'remote-model-turn' } });
    const hook = renderHook(() => useAgentModels(true, sessionId, 'p'), { wrapper: wrapperWithClient(client) });
    try {
      await waitFor(() => expect(hook.result.current.data?.localModels?.currentModelId).toBe('model-a'));
      await store.get('p', sessionId);
      await waitFor(() => expect(hook.result.current.data?.localModels?.currentModelId).toBe('model-b'));
      expect(catalogs).toHaveBeenCalledTimes(2);
      await expect(store.setModel('model-c', sessionId, 'p')).rejects.toThrow('Take over');
      expect(acp.setSessionModel).not.toHaveBeenCalled();
    } finally {
      hook.unmount();
      client.clear();
    }
  });

  it('advertises the local Astrid ACP implementation', () => {
    expect(isTimelineAgentSessionsAvailable()).toBe(true);
  });

  it('keeps missing identifiers as input errors before contacting ACP', async () => {
    const create = renderHook(() => useCreateSession(null), { wrapper });
    await expect(act(async () => create.result.current.mutateAsync(undefined))).rejects.toThrow('Select a project or timeline to start chatting.');
    create.unmount();

    const send = renderHook(() => useSendMessage(null), { wrapper });
    await expect(act(async () => send.result.current.mutateAsync({ message: 'hello' }))).rejects.toThrow('sessionId is required');
    send.unmount();

    const cancel = renderHook(() => useCancelSession(null), { wrapper });
    await expect(act(async () => cancel.result.current.mutateAsync())).rejects.toThrow('sessionId is required');
  });

  it('stops saved-chat load polling after failure and lets an explicit retry restore the transcript', async () => {
    let loads = 0;
    let missing = true;
    vi.stubGlobal('fetch', vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.endsWith('/chat')) return Response.json({project_id: 'saved-project', scope_key: 'project:saved-project', revision: 1, selected_session_id: 'saved-chat-retry', sessions: [{id: 'saved-chat-retry', pending_first_message: false}], draft: {text: '', revision: 1, queued_messages: []}});
      if (url.endsWith('/connect')) return Response.json({ connection_id: 'saved-chat-connection', initialize: {} });
      if (url.endsWith('/rpc')) {
        const body = JSON.parse(String(init?.body));
        expect(body.method).toBe('session/load');
        loads++;
        return missing
          ? Response.json({ error: 'acp_transport', detail: 'ACP request "session/load" failed: ACP session not found: saved-chat-retry' }, { status: 502 })
          : Response.json({ result: {} });
      }
      return Response.json({ disconnected: false, notifications: [{ jsonrpc: '2.0', method: 'session/update', params: {
        sessionId: 'saved-chat-retry', update: { sessionUpdate: 'agent_message_chunk', messageId: 'old-reply', content: { type: 'text', text: 'Persisted reply' } },
      } }] });
    }));
    vi.useFakeTimers();
    const hook = renderHook(() => useAgentSession('saved-chat-retry', 'saved-project'), { wrapper });
    try {
      await act(async () => { await vi.advanceTimersByTimeAsync(10); });
      expect(hook.result.current.error?.message).toContain('ACP session not found');
      const eventReads = () => vi.mocked(globalThis.fetch).mock.calls.filter(([input]) => String(input).endsWith('/events')).length;
      const baseline = eventReads();
      await act(async () => { await vi.advanceTimersByTimeAsync(30_000); });
      expect(loads).toBe(1);
      expect(eventReads()).toBe(baseline + 2);
      missing = false;
      await act(async () => { await hook.result.current.refetch(); await vi.advanceTimersByTimeAsync(10); });
      expect(loads).toBe(2);
      expect(hook.result.current.error).toBeNull();
      expect(hook.result.current.data?.turns).toEqual([expect.objectContaining({ role: 'assistant', content: 'Persisted reply' })]);
    } finally {
      hook.unmount();
      vi.useRealTimers();
      vi.unstubAllGlobals();
    }
  });

  it.each([
    ['claude-code', 'Resource not found'],
    ['codex', 'no rollout found for thread ID'],
  ] as const)('recovers a legacy empty %s chat after session/load proves its transcript is missing', async (agent, missingDetail) => {
    localStorage.setItem(LOCAL_AGENT_SETTING_KEY, agent);
    localStorage.setItem(localAgentModelSettingKey(agent), 'model-beta');
    const oldId = `${agent}:empty-before-reload`;
    const freshId = `${agent}:fresh-after-reload`;
    let projectChat = { project_id: 'reload-project', scope_key: 'project:reload-project', revision: 4, selected_session_id: oldId, main_session_id: 'other-chat', sessions: [{ id: oldId, title: 'Untitled', model_id: 'model-beta' }, { id: 'other-chat', title: 'Other' }], draft: { text: '', revision: 0, queued_messages: [] } };
    const calls: Array<{ url: string; body?: Record<string, unknown> }> = [];
    vi.stubGlobal('fetch', vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      const body = init?.body ? JSON.parse(String(init.body)) as Record<string, unknown> : undefined;
      calls.push({ url, body });
      if (url.endsWith('/chat') && init?.method !== 'POST') return Response.json(projectChat);
      if (url.endsWith('/connect')) return Response.json({ connection_id: 'claude-reload', initialize: {} });
      if (url.endsWith('/rpc')) return Response.json({ error: 'acp_transport', detail: `ACP request "session/load" failed: ${missingDetail}: ${oldId}` }, { status: 502 });
      if (url.endsWith('/chat/sessions')) {
        expect(body?.recover_session_id).toBe(oldId);
        projectChat = { ...projectChat, revision: 5, selected_session_id: freshId, sessions: [{ ...projectChat.sessions[0], id: freshId, pending_first_message: true }, projectChat.sessions[1]] };
        return Response.json({ ...projectChat, operation_session_id: freshId });
      }
      if (url.endsWith('/events')) return Response.json({ disconnected: false, notifications: [] });
      throw new Error(`Unexpected request: ${url}`);
    }));
    const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const hook = renderHook(() => useAgentSession(oldId, 'reload-project'), { wrapper: wrapperWithClient(client) });
    try {
      await waitFor(() => expect(hook.result.current.data?.id).toBe(freshId));
      const recovery = calls.find(call => call.url.endsWith('/chat/sessions'));
      expect(recovery?.body).toMatchObject({ mode: 'ensure', recover_session_id: oldId });
      expect(calls.some(call => call.url.endsWith('/rpc') && call.body?.method === 'session/new')).toBe(false);
      expect(calls.filter(call => call.url.endsWith('/chat')).length).toBeGreaterThanOrEqual(1);
      expect(client.getQueryData<ProjectChatState>(projectChatQueryKey('reload-project'))).toMatchObject({
        selected_session_id: freshId,
        main_session_id: 'other-chat',
        sessions: [{ id: freshId, title: 'Untitled', model_id: 'model-beta', pending_first_message: true }, { id: 'other-chat' }],
      });
      expect(calls.find(call => call.url.endsWith('/connect'))?.body).toMatchObject({ agent, defaultModelId: 'model-beta' });
    } finally {
      hook.unmount();
      client.clear();
      vi.unstubAllGlobals();
    }
  });

  it.each(['pagehide', 'beforeunload'])('releases tab ownership with keepalive on %s and reconnects on return', async (event) => {
    const release = vi.spyOn(AstridAgentSessionStore.prototype, 'closeConnectionOnPageHide');
    window.dispatchEvent(new Event(event));
    expect(release).toHaveBeenCalledTimes(1);
    const acp = {
      projectChat: vi.fn(async () => ({ sessions: [{ id: 'chat' }] })),
      connect: vi.fn().mockResolvedValueOnce({ connection_id: 'old' }).mockResolvedValue({ connection_id: 'new' }),
      loadSession: vi.fn(async () => ({})),
      events: vi.fn(async () => ({ notifications: [], disconnected: false })),
      disconnect: vi.fn().mockResolvedValue(undefined),
    };
    const store = new AstridAgentSessionStore({ acp } as never);
    await store.get('project', 'chat');
    store.closeConnectionOnPageHide();
    store.closeConnectionOnPageHide();
    expect(acp.disconnect).toHaveBeenCalledExactlyOnceWith('old', { keepalive: true });
    await store.get('project', 'chat');
    expect(acp.connect).toHaveBeenCalledTimes(2);
    expect(acp.loadSession).toHaveBeenLastCalledWith('new', 'chat');
  });

  it('renews the heartbeat in a background tab and observes automatic writer promotion', async () => {
    vi.useFakeTimers();
    focusManager.setFocused(false);
    const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    let role: 'writer' | 'follower' = 'follower';
    const get = vi.spyOn(AstridAgentSessionStore.prototype, 'get').mockImplementation(async (_projectId, id) => ({
      id, status: 'waiting_user', turns: [], taskLinks: [], control: { role, active: false, activeRequestId: null },
    }));
    const hook = renderHook(() => useAgentSession('background-chat', 'project'), { wrapper: wrapperWithClient(client) });
    try {
      await act(async () => { await vi.advanceTimersByTimeAsync(1); });
      expect(hook.result.current.data?.control?.role).toBe('follower');
      const baseline = get.mock.calls.length;
      await act(async () => { await vi.advanceTimersByTimeAsync(60_000); });
      expect(get.mock.calls.length).toBeGreaterThanOrEqual(baseline + 4);
      role = 'writer';
      await act(async () => { await vi.advanceTimersByTimeAsync(15_000); });
      expect(hook.result.current.data?.control?.role).toBe('writer');
    } finally {
      hook.unmount();
      client.clear();
      focusManager.setFocused(undefined);
      vi.useRealTimers();
    }
  });

  it('polls an idle session slowly and an active turn at the streaming cadence', async () => {
    vi.useFakeTimers();
    const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const get = vi.spyOn(AstridAgentSessionStore.prototype, 'get').mockImplementation(async (_projectId, sessionId) => ({
      id: sessionId, status: sessionId === 'active-session' ? 'processing' : 'waiting_user', turns: [], taskLinks: [],
    } as never));
    client.setQueryData(['timeline-agent-session', 'idle-session', 'project-1'], {
      id: 'idle-session', status: 'waiting_user', turns: [], taskLinks: [],
    });
    const idle = renderHook(() => useAgentSession('idle-session', 'project-1'), { wrapper: wrapperWithClient(client) });
    try {
      await act(async () => { await Promise.resolve(); });
      const idleBaseline = get.mock.calls.length;
      expect(idleBaseline).toBeGreaterThan(0);
      await act(async () => { await vi.advanceTimersByTimeAsync(14_999); });
      expect(get).toHaveBeenCalledTimes(idleBaseline);
      await act(async () => { await vi.advanceTimersByTimeAsync(1); });
      expect(get).toHaveBeenCalledTimes(idleBaseline + 1);
      idle.unmount();

      client.setQueryData(['timeline-agent-session', 'active-session', 'project-1'], {
        id: 'active-session', status: 'processing', turns: [], taskLinks: [],
      });
      const active = renderHook(() => useAgentSession('active-session', 'project-1'), { wrapper: wrapperWithClient(client) });
      await act(async () => { await Promise.resolve(); });
      const activeBaseline = get.mock.calls.length;
      await act(async () => { await vi.advanceTimersByTimeAsync(499); });
      expect(get).toHaveBeenCalledTimes(activeBaseline);
      await act(async () => { await vi.advanceTimersByTimeAsync(1); });
      expect(get).toHaveBeenCalledTimes(activeBaseline + 1);
      active.unmount();
    } finally {
      idle.unmount();
      client.clear();
      vi.useRealTimers();
    }
  });

  it('polls project chat at the idle or active turn cadence', async () => {
    vi.useFakeTimers();
    const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const projectChat = vi.spyOn(AstridAgentSessionStore.prototype, 'projectChat').mockImplementation(async (projectId) => ({
      project_id: projectId,
      revision: 1,
      draft: { revision: 1 },
    } as never));
    try {
      const idle = renderHook(() => useProjectChat('project-1'), { wrapper: wrapperWithClient(client) });
      await act(async () => { await Promise.resolve(); });
      const idleBaseline = projectChat.mock.calls.length;
      expect(idleBaseline).toBeGreaterThan(0);
      await act(async () => { await vi.advanceTimersByTimeAsync(14_999); });
      expect(projectChat).toHaveBeenCalledTimes(idleBaseline);
      await act(async () => { await vi.advanceTimersByTimeAsync(1); });
      expect(projectChat).toHaveBeenCalledTimes(idleBaseline + 1);
      idle.unmount();

      client.setQueryData(['timeline-agent-session', 'active-session', 'project-1'], {
        id: 'active-session', status: 'processing', turns: [], taskLinks: [],
      });
      const active = renderHook(() => useProjectChat('project-1'), { wrapper: wrapperWithClient(client) });
      await act(async () => { await Promise.resolve(); });
      const activeBaseline = projectChat.mock.calls.length;
      await act(async () => { await vi.advanceTimersByTimeAsync(499); });
      expect(projectChat).toHaveBeenCalledTimes(activeBaseline);
      await act(async () => { await vi.advanceTimersByTimeAsync(1); });
      expect(projectChat).toHaveBeenCalledTimes(activeBaseline + 1);
      active.unmount();
    } finally {
      client.clear();
      vi.useRealTimers();
    }
  });

  it('switches an idle session to fast polling as soon as a message is sent', async () => {
    vi.useFakeTimers();
    const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const sessionKey = ['timeline-agent-session', 'send-session', 'project-1'] as const;
    let turnActive = false;
    const get = vi.spyOn(AstridAgentSessionStore.prototype, 'get').mockImplementation(async (_projectId, sessionId) => ({
      id: sessionId, status: turnActive ? 'processing' : 'waiting_user', turns: [], taskLinks: [],
    } as never));
    let finishPrompt!: () => void;
    const prompt = vi.spyOn(AstridAgentSessionStore.prototype, 'prompt').mockImplementation(async () => {
      turnActive = true;
      await new Promise<void>(resolve => { finishPrompt = resolve; });
    });
    client.setQueryData(sessionKey, { id: 'send-session', status: 'waiting_user', turns: [], taskLinks: [] });
    const hook = renderHook(() => ({
      session: useAgentSession('send-session', 'project-1'),
      send: useSendMessage('send-session', { tool: 'video-editor', projectId: 'project-1', projectSlug: null, timelineId: null, timelineName: null }, 'project-1'),
    }), { wrapper: wrapperWithClient(client) });
    try {
      await act(async () => { await Promise.resolve(); });
      const baseline = get.mock.calls.length;
      await act(async () => { await vi.advanceTimersByTimeAsync(1_000); });
      expect(get).toHaveBeenCalledTimes(baseline);
      let sending!: Promise<unknown>;
      act(() => { sending = hook.result.current.send.mutateAsync({ message: 'hello' }); });
      await act(async () => { await Promise.resolve(); await Promise.resolve(); });
      expect(prompt).toHaveBeenCalled();
      expect(client.getQueryData(sessionKey)).toMatchObject({ status: 'processing' });
      const afterSend = get.mock.calls.length;
      await act(async () => { await vi.advanceTimersByTimeAsync(500); });
      expect(get).toHaveBeenCalledTimes(afterSend + 1);
      await act(async () => { finishPrompt(); await sending; });
    } finally {
      hook.unmount();
      client.clear();
      vi.useRealTimers();
    }
  });

  it('restores project chat reads and writes through the existing ACP routes', async () => {
    const chat = {
      project_id: 'project-1',
      scope_key: 'project:project-1',
      revision: 4,
      selected_session_id: 'session-1',
      sessions: [{ id: 'session-1' }],
      draft: { text: 'draft', revision: 2, queued_messages: [] },
    };
    const acp = {
      projectChat: vi.fn(async () => chat),
      saveProjectDraft: vi.fn(async () => chat),
      selectProjectSession: vi.fn(async () => chat),
      renameProjectSession: vi.fn(async () => chat),
    };
    const store = new AstridAgentSessionStore({ acp } as never);

    await expect(store.projectChat('project-1')).resolves.toBe(chat);
    await expect(store.saveProjectDraft('project-1', 2, 'new draft', [])).resolves.toBe(chat);
    await expect(store.selectProjectSession('project-1', 4, null)).resolves.toBe(chat);
    await expect(store.renameProjectSession('project-1', 5, 'session-1', 'Renamed')).resolves.toBe(chat);
    expect(acp.projectChat).toHaveBeenCalledWith('project-1');
    expect(acp.saveProjectDraft).toHaveBeenCalledWith('project-1', 2, 'new draft', []);
    expect(acp.selectProjectSession).toHaveBeenCalledWith('project-1', 4, null);
    expect(acp.renameProjectSession).toHaveBeenCalledWith('project-1', 5, 'session-1', 'Renamed');
  });

  it('keeps chat association order stable when selected and Main pointers change', async () => {
    const chat = { selected_session_id: 'second', main_session_id: 'second', sessions: [{ id: 'first' }, { id: 'second' }] };
    const acp = {
      projectChat: vi.fn(async () => chat),
      connect: vi.fn(async () => ({ connection_id: 'connection' })),
      events: vi.fn(async () => ({ notifications: [], disconnected: false })),
    };
    const store = new AstridAgentSessionStore({ acp } as never);
    expect((await store.list('project')).map(s => s.id)).toEqual(['first', 'second']);
    chat.selected_session_id = 'first';
    expect((await store.list('project')).map(s => s.id)).toEqual(['first', 'second']);
  });

  it('assigns Main through the existing revisioned project chat cache', async () => {
    const chat = {project_id: 'project-1', revision: 5, main_session_id: 'chosen', selected_session_id: 'chosen'} as ProjectChatState;
    const assign = vi.spyOn(AstridAgentSessionStore.prototype, 'setMainProjectSession').mockResolvedValue(chat);
    const client = new QueryClient({defaultOptions: {queries: {retry: false}}});
    const {result, unmount} = renderHook(() => useSetMainProjectSession('project-1'), {wrapper: wrapperWithClient(client)});
    await act(async () => result.current.mutateAsync({expectedRevision: 4, sessionId: 'chosen'}));
    expect(assign).toHaveBeenCalledWith('project-1', 4, 'chosen');
    expect(client.getQueryData(projectChatQueryKey('project-1'))).toEqual(chat);
    unmount();
    client.clear();
  });

  it('renames a project session and refreshes the scoped chat cache, while preserving errors', async () => {
    const chat = {project_id: 'project-1', revision: 6, sessions: [{id: 'session-2', title: 'Renamed'}]} as ProjectChatState;
    const rename = vi.spyOn(AstridAgentSessionStore.prototype, 'renameProjectSession').mockResolvedValue(chat);
    const client = new QueryClient({defaultOptions: {queries: {retry: false}}});
    const {result, unmount} = renderHook(() => useRenameProjectSession('project-1'), {wrapper: wrapperWithClient(client)});
    await act(async () => result.current.mutateAsync({expectedRevision: 5, sessionId: 'session-2', title: 'Renamed'}));
    expect(rename).toHaveBeenCalledWith('project-1', 5, 'session-2', 'Renamed');
    expect(client.getQueryData(projectChatQueryKey('project-1'))).toBe(chat);

    const conflict = new BridgeRouteError('Rename project chat session', 409, {error: 'revision_conflict'});
    rename.mockRejectedValueOnce(conflict);
    await expect(act(async () => result.current.mutateAsync({expectedRevision: 4, sessionId: 'session-2', title: 'Stale'}))).rejects.toBe(conflict);
    expect(client.getQueryData(projectChatQueryKey('project-1'))).toBe(chat);
    unmount();
    client.clear();
  });

  it('loads project chat through the query hook and uses the project-scoped cache key', async () => {
    const chat = {project_id: 'project-1', revision: 4} as ProjectChatState;
    const projectChat = vi.spyOn(AstridAgentSessionStore.prototype, 'projectChat').mockResolvedValue(chat);
    const client = new QueryClient({defaultOptions: {queries: {retry: false}}});
    const {result, unmount} = renderHook(() => useProjectChat('project-1'), {wrapper: wrapperWithClient(client)});

    await waitFor(() => expect(result.current.data).toBe(chat));
    expect(projectChat).toHaveBeenCalledWith('project-1');
    expect(client.getQueryData(projectChatQueryKey('project-1'))).toBe(chat);
    unmount();
    client.clear();
  });

  it('saves project drafts through the mutation hook and refreshes the scoped chat cache', async () => {
    const chat = {project_id: 'project-1', revision: 5} as ProjectChatState;
    const saveProjectDraft = vi.spyOn(AstridAgentSessionStore.prototype, 'saveProjectDraft').mockResolvedValue(chat);
    const client = new QueryClient({defaultOptions: {queries: {retry: false}}});
    const {result, unmount} = renderHook(() => useSaveProjectDraft('project-1'), {wrapper: wrapperWithClient(client)});

    await act(async () => result.current.mutateAsync({expectedRevision: 4, text: 'draft update', queuedMessages: []}));
    expect(saveProjectDraft).toHaveBeenCalledWith('project-1', 4, 'draft update', []);
    expect(client.getQueryData(projectChatQueryKey('project-1'))).toBe(chat);
    unmount();
    client.clear();
  });

  it('selects a project session through the mutation hook and refreshes the scoped chat cache', async () => {
    const chat = {project_id: 'project-1', revision: 5} as ProjectChatState;
    const selectProjectSession = vi.spyOn(AstridAgentSessionStore.prototype, 'selectProjectSession').mockResolvedValue(chat);
    const client = new QueryClient({defaultOptions: {queries: {retry: false}}});
    const {result, unmount} = renderHook(() => useSelectProjectSession('project-1'), {wrapper: wrapperWithClient(client)});

    await act(async () => result.current.mutateAsync({expectedRevision: 4, sessionId: 'session-2'}));
    expect(selectProjectSession).toHaveBeenCalledWith('project-1', 4, 'session-2');
    expect(client.getQueryData(projectChatQueryKey('project-1'))).toBe(chat);
    unmount();
    client.clear();
  });

  it('preserves ACP message boundaries when adjacent replies arrive', () => {
    const turns = [] as Parameters<typeof appendAcpTextTurn>[0];
    appendAcpTextTurn(turns, 'user', 'first', '2026-09-18T15:00:00.000Z', 'user-1');
    appendAcpTextTurn(turns, 'assistant', 'one', '2026-09-18T15:00:01.000Z', 'assistant-1');
    appendAcpTextTurn(turns, 'assistant', ' plus', '2026-09-18T15:00:01.100Z', 'assistant-1');
    appendAcpTextTurn(turns, 'user', 'second', '2026-09-18T15:00:02.000Z', 'user-2');
    appendAcpTextTurn(turns, 'assistant', 'two', '2026-09-18T15:00:03.000Z', 'assistant-2');

    expect(turns.map(({ role, content }) => ({ role, content }))).toEqual([
      { role: 'user', content: 'first' },
      { role: 'assistant', content: 'one plus' },
      { role: 'user', content: 'second' },
      { role: 'assistant', content: 'two' },
    ]);
  });

  it('keeps streamed assistant narration transient and starts a new final candidate at a new message boundary', () => {
    const preamble = appendAcpAssistantDraft(undefined, 'Checking the timeline…', 'assistant-1');
    expect(appendAcpAssistantDraft(preamble, ' reading the compact summary', 'assistant-1')).toEqual({
      content: 'Checking the timeline… reading the compact summary',
      messageId: 'assistant-1',
    });

    expect(appendAcpAssistantDraft(preamble, 'Done — moved the clip.', 'assistant-2')).toEqual({
      content: 'Done — moved the clip.',
      messageId: 'assistant-2',
    });
  });

  it('hides the model-only editor context from the rendered transcript', () => {
    expect(stripAstridEditorContext('make the first clip start later\n\n<astrid_editor_context>\n{}\n</astrid_editor_context>'))
      .toBe('make the first clip start later');
    expect(stripAstridEditorContext('<astrid_editor_context>\n{}\n</astrid_editor_context>')).toBe('');
    expect(stripAstridEditorContext('hello\n<astrid_agent_context>private</astrid_agent_context>')).toBe('hello');
    expect(stripAstridEditorContext('hello\n<astrid_agent_context>private</astrid_agent_context>\n<astrid_editor_context>{}</astrid_editor_context>')).toBe('hello');
    expect(stripAstridEditorContext('make the first clip start later\n\nAstrid editor context:\nTimeline ID: timeline-1'))
      .toBe('make the first clip start later');
  });

  it('extracts host-executable element operations without leaking markers into chat', () => {
    const result = extractAstridElementOperations([
      'I will apply the effect.',
      '<astrid_element_operation>{"name":"elements.list"}</astrid_element_operation>',
      '<astrid_element_operation>{"name":"elements.validate","draft_id":"draft-glow"}</astrid_element_operation>',
    ].join('\n'));
    expect(result.visibleContent).toBe('I will apply the effect.');
    expect(result.operations).toEqual([
      { name: 'elements.list' },
      { name: 'elements.validate', draft_id: 'draft-glow' },
    ]);
    expect(result.parseErrors).toEqual([]);
  });

  it('reports malformed operation markers while preserving surrounding narration', () => {
    const result = extractAstridElementOperations(
      'Done. <astrid_element_operation>{not json}</astrid_element_operation>',
    );
    expect(result.visibleContent).toBe('Done.');
    expect(result.operations).toEqual([]);
    expect(result.parseErrors).toHaveLength(1);
  });
});


describe('explicit third-argument project routing', () => {
  const context = (projectId: string, timelineId: string | null = null) => ({
    tool: 'video-editor' as const, projectId, projectSlug: `${projectId}-slug`, timelineId, timelineName: timelineId,
  });

  it('keeps a failed request on its captured route/context and rejects a later project even if the session ID is unchanged', async () => {
    vi.resetModules();
    const { useSendMessage: scopedSend } = await import('./useAgentSession.ts');
    const prompts: Array<{ url: string; body: { session_id: string; prompt: Array<{ text: string }> } }> = [];
    let fail = true;
    const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.endsWith('/chat')) return Response.json({project_id: url.includes('route-a') ? 'route-a' : 'route-b', scope_key: 'project:route', revision: 1, selected_session_id: 'same-session', sessions: [{id: 'same-session'}], draft: {text: '', revision: 1, queued_messages: []}});
      if (url.endsWith('/connect')) return Response.json({ connection_id: 'route-connection', initialize: {} });
      if (url.endsWith('/rpc')) {
        expect(JSON.parse(String(init?.body)).method).toBe('session/load');
        return Response.json({ result: {} });
      }
      if (url.endsWith('/chat/prompt')) {
        prompts.push({ url, body: JSON.parse(String(init?.body)) });
        return fail ? Response.json({ error: 'acp_transport', detail: 'reply lost' }, { status: 502 }) : Response.json({ result: {} });
      }
      return Response.json({ disconnected: false, notifications: [] });
    });
    vi.stubGlobal('fetch', fetchMock);
    const hook = renderHook(({ scope, route }) => scopedSend('same-session', scope, route), {
      wrapper, initialProps: { scope: context('route-a', 'timeline-original'), route: 'route-a' },
    });
    try {
      await expect(act(async () => { await hook.result.current.mutateAsync({ message: 'captured message' }); })).rejects.toThrow('reply lost');
      expect(prompts).toHaveLength(1);
      expect(prompts[0].url).toContain('/projects/route-a/chat/prompt');
      expect(prompts[0].body.session_id).toBe('same-session');
      const captured = prompts[0].body.prompt[1].text;
      expect(captured).toContain('timeline-original');
      // Changing the route and scope while keeping the same opaque session must
      // not dispatch the old payload to the new project.
      hook.rerender({ scope: context('route-b', 'timeline-new'), route: 'route-b' });
      const callsBeforeRetry = fetchMock.mock.calls.length;
      await expect(act(async () => { await hook.result.current.retryLastMessage(); })).rejects.toThrow('original project');
      expect(fetchMock).toHaveBeenCalledTimes(callsBeforeRetry);
      expect(prompts).toHaveLength(1);
      // Returning to the original project permits retry while retaining the
      // original captured timeline, even though the current timeline changed.
      fail = false;
      hook.rerender({ scope: context('route-a', 'timeline-current'), route: 'route-a' });
      await act(async () => { await hook.result.current.retryLastMessage(); });
      expect(prompts).toHaveLength(2);
      expect(prompts[1].url).toBe(prompts[0].url);
      expect(prompts[1].body.session_id).toBe('same-session');
      expect(prompts[1].body.prompt[0].text).toBe('captured message');
      expect(prompts[1].body.prompt[1].text).toContain('timeline-original');
      expect(prompts[1].body.prompt[1].text).not.toContain('timeline-current');
      expect(hook.result.current.hasRetryableMessage).toBe(false);
    } finally {
      hook.unmount(); vi.unstubAllGlobals(); vi.resetModules();
    }
  });

  it('rejects a mixed project route/context before any ACP dispatch', async () => {
    vi.resetModules();
    const { useSendMessage: scopedSend } = await import('./useAgentSession.ts');
    const fetchMock = vi.fn();
    vi.stubGlobal('fetch', fetchMock);
    const hook = renderHook(() => scopedSend('mixed-session', context('context-a'), 'route-b'), { wrapper });
    try {
      await expect(act(async () => { await hook.result.current.mutateAsync({ message: 'never forward' }); })).rejects.toThrow('routing project does not match');
      expect(fetchMock).not.toHaveBeenCalled();
    } finally {
      hook.unmount(); vi.unstubAllGlobals(); vi.resetModules();
    }
  });
});


describe('scoped project membership and independent revision receipts', () => {
  it('refuses a missing or foreign project session before connection, load or prompt', async () => {
    const acp = {
      projectChat: vi.fn(async () => ({sessions: [{id: 'missing-session', missing: true}]})),
      connect: vi.fn(), loadSession: vi.fn(), promptProjectSession: vi.fn(),
    };
    const store = new AstridAgentSessionStore({acp} as never);
    await expect(store.get('project-a', 'foreign-session')).rejects.toThrow('does not belong');
    await expect(store.prompt('missing-session', {message: 'never dispatch'}, {
      tool: 'video-editor', projectId: 'project-a', projectSlug: null, timelineId: null, timelineName: null,
    })).rejects.toThrow('does not belong');
    expect(acp.connect).not.toHaveBeenCalled();
    expect(acp.loadSession).not.toHaveBeenCalled();
    expect(acp.promptProjectSession).not.toHaveBeenCalled();
  });

  it('keeps a late draft receipt in its captured project and preserves a newer session selection', async () => {
    const client = new QueryClient({defaultOptions: {queries: {retry: false}}});
    const newer = {project_id: 'old-project', revision: 8, selected_session_id: 'new-selection', sessions: [],
      draft: {revision: 2, text: 'previous', queued_messages: []}} as ProjectChatState;
    client.setQueryData(projectChatQueryKey('old-project'), newer);
    let resolve!: (value: ProjectChatState) => void;
    vi.spyOn(AstridAgentSessionStore.prototype, 'saveProjectDraft').mockImplementation(() => new Promise(done => { resolve = done; }));
    const hook = renderHook(({project}) => useSaveProjectDraft(project), {wrapper: wrapperWithClient(client), initialProps: {project: 'old-project'}});
    let pending!: Promise<ProjectChatState>;
    act(() => { pending = hook.result.current.mutateAsync({expectedRevision: 2, text: 'captured draft', queuedMessages: []}); });
    await waitFor(() => expect(resolve).toBeTypeOf('function'));
    hook.rerender({project: 'new-project'});
    await act(async () => {
      resolve({...newer, revision: 7, selected_session_id: 'obsolete-selection', draft: {revision: 3, text: 'captured draft', queued_messages: []}});
      await pending;
    });
    expect(client.getQueryData(projectChatQueryKey('old-project'))).toMatchObject({revision: 8, selected_session_id: 'new-selection', draft: {revision: 3, text: 'captured draft'}});
    expect(client.getQueryData(projectChatQueryKey('new-project'))).toBeUndefined();
    hook.unmount(); client.clear();
  });
});
