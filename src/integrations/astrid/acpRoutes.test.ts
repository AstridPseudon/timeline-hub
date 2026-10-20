import { describe, expect, it, vi } from 'vitest';

import { AstridLocalAcpRoutes } from './acpRoutes.ts';
import { LOCAL_AGENT_TABLE } from './localAgents.ts';
import { BridgeRouteError, type AstridBridgeTransport } from './transport.ts';

describe('AstridLocalAcpRoutes', () => {
  it('takes over the loaded session and preserves submission identity on prompt requests', async () => {
    const requestJson = vi.fn(async (_path: string, _request: unknown, schema: { parse: (value: unknown) => unknown }) => schema.parse({ result: { _astridSession: { role: 'writer', active: true, activeRequestId: 'queued-1' } } }));
    const routes = new AstridLocalAcpRoutes({ requestJson } as unknown as AstridBridgeTransport);
    await routes.takeOverSession('second-tab', 'codex:chat-3');
    await routes.promptProjectSession('p', 'second-tab', 'codex:chat-3', [{ type: 'text', text: 'hello' }], 'queued-1');
    expect(requestJson.mock.calls.map(([path, request]) => ({ path, request }))).toEqual([
      { path: '/acp/second-tab/rpc', request: { method: 'POST', body: { method: 'session/takeover', params: { sessionId: 'codex:chat-3' } } } },
      { path: '/acp/projects/p/chat/prompt', request: { method: 'POST', body: { connection_id: 'second-tab', session_id: 'codex:chat-3', prompt: [{ type: 'text', text: 'hello' }], request_id: 'queued-1' } } },
    ]);
  });
  it('carries a local agent default and scopes model discovery and selection to the chat', async () => {
    const models = { availableModels: [{ modelId: 'model/a', name: 'Model A', description: 'A model' }], currentModelId: 'model/a' };
    const requestJson = vi.fn(async (path: string, _request: unknown, schema: { parse: (value: unknown) => unknown }) =>
      schema.parse(path === '/acp/connect' ? { connection_id: 'c 1', initialize: {} } : { models }));
    const routes = new AstridLocalAcpRoutes({ requestJson } as unknown as AstridBridgeTransport);
    await routes.connect('codex', 'model/a');
    await expect(routes.sessionModels('c 1', 'codex:chat/1')).resolves.toEqual({ models });
    await expect(routes.setSessionModel('c 1', 'codex:chat/1', 'model/a')).resolves.toEqual({ models });
    expect(requestJson.mock.calls.map(([path, request]) => ({ path, request }))).toEqual([
      { path: '/acp/connect', request: { method: 'POST', body: { agent: 'codex', defaultModelId: 'model/a' } } },
      { path: '/acp/c%201/models?sessionId=codex%3Achat%2F1', request: { method: 'GET' } },
      { path: '/acp/c%201/model', request: { method: 'POST', body: { sessionId: 'codex:chat/1', modelId: 'model/a' } } },
    ]);
  });
  it('discovers local agents and launches the exact selected agent', async () => {
    const catalog = { agents: [{ id: 'codex', name: LOCAL_AGENT_TABLE.codex.name, state: 'ready' as const, line: null }] };
    const requestJson = vi.fn(async (path: string, _request: unknown, schema: { parse: (value: unknown) => unknown }) => schema.parse(path === '/acp/agents' ? catalog : { connection_id: 'c1', initialize: {} }));
    const routes = new AstridLocalAcpRoutes({ requestJson } as unknown as AstridBridgeTransport);
    await expect(routes.agents()).resolves.toEqual(catalog);
    await routes.connect('codex');
    expect(requestJson.mock.calls.map(([path, request]) => ({ path, request }))).toEqual([
      { path: '/acp/agents', request: { method: 'GET' } },
      { path: '/acp/connect', request: { method: 'POST', body: { agent: 'codex' } } },
    ]);
  });
  it('reads the provider catalog through the shared ACP transport', async () => {
    const catalog = { currentModel: 'openai/gpt-5', providers: [{ id: 'openai', name: 'OpenAI', signedIn: true, models: [{ id: 'gpt-5', name: 'GPT 5' }], usage: { limits: [{ usedFraction: 0.5, unit: 'percent' }] } }] };
    const requestJson = vi.fn(async (path: string, request: unknown, schema: { parse: (value: unknown) => unknown }) => {
      if (path === '/acp/models') return schema.parse(catalog);
      expect(request).toMatchObject({ method: 'POST', body: { model: 'openai/gpt-5' } });
      return schema.parse({ currentModel: 'openai/gpt-5' });
    });
    const routes = new AstridLocalAcpRoutes({ requestJson } as unknown as AstridBridgeTransport);
    await expect(routes.models()).resolves.toEqual(catalog);
    expect(requestJson.mock.calls.map(([path]) => path)).toEqual(['/acp/models']);
  });

  it('keeps project chat association, durable drafts, and owned prompts on the ACP transport', async () => {
    const requestJson = vi.fn(async (path: string, request: unknown, _schema: unknown) => {
      if (path.endsWith('/unassigned?connection_id=connection-1')) return { sessions: [{ id: 'legacy-1' }] };
      if (path.endsWith('/chat/prompt')) return { result: { accepted: true } };
      return {
        project_id: 'project-1', scope_key: 'realm:store:project-1', revision: 2,
        selected_session_id: 'session-1', sessions: [{ id: 'session-1' }],
        draft: { text: 'draft', revision: 1, queued_messages: [] },
      };
    });
    const routes = new AstridLocalAcpRoutes({ requestJson } as unknown as AstridBridgeTransport);

    await routes.projectChat('project-1');
    await routes.createProjectSession('project-1', 'connection-1', 'ensure', 'op-1');
    await expect(routes.unassignedProjectSessions('project-1', 'connection-1')).resolves.toEqual([{ id: 'legacy-1' }]);
    await routes.associateProjectSession('project-1', 'connection-1', 1, 'legacy-1');
    await routes.saveProjectDraft('project-1', 1, 'draft', [{ id: 'q1', text: 'queued', session_id: 'session-1' }]);
    await routes.selectProjectSession('project-1', 2, 'session-1');
    await routes.setMainProjectSession('project-1', 2, 'session-1');
    await expect(routes.promptProjectSession('project-1', 'connection-1', 'session-1', [{ type: 'text', text: 'hello' }])).resolves.toEqual({ accepted: true });

    expect(requestJson.mock.calls.map(([path, request]) => ({ path, method: (request as { method?: string }).method ?? 'GET' }))).toEqual([
      { path: '/acp/projects/project-1/chat', method: 'GET' },
      { path: '/acp/projects/project-1/chat/sessions', method: 'POST' },
      { path: '/acp/projects/project-1/chat/unassigned?connection_id=connection-1', method: 'GET' },
      { path: '/acp/projects/project-1/chat/associate', method: 'POST' },
      { path: '/acp/projects/project-1/chat/draft', method: 'PATCH' },
      { path: '/acp/projects/project-1/chat', method: 'PATCH' },
      { path: '/acp/projects/project-1/chat/main', method: 'PATCH' },
      { path: '/acp/projects/project-1/chat/prompt', method: 'POST' },
    ]);
  });

  it('renames a project session through the revisioned project chat route and preserves route errors', async () => {
    const chat = {
      project_id: 'project/one', scope_key: 'realm:project/one', revision: 8,
      selected_session_id: 'opaque:session/1', sessions: [{ id: 'opaque:session/1', title: 'New title' }],
      draft: { text: '', revision: 0, queued_messages: [] },
    };
    const requestJson = vi.fn(async (_path: string, _request: unknown, schema: { parse: (value: unknown) => unknown }) => schema.parse(chat));
    const routes = new AstridLocalAcpRoutes({ requestJson } as unknown as AstridBridgeTransport);

    await expect(routes.renameProjectSession('project/one', 7, 'opaque:session/1', 'New title')).resolves.toEqual(chat);
    expect(requestJson).toHaveBeenCalledWith('/acp/projects/project%2Fone/chat', {
      method: 'PATCH', body: { expected_revision: 7, session_id: 'opaque:session/1', title: 'New title' },
    }, expect.anything(), 'Rename project chat session');

    const conflict = new BridgeRouteError('Rename project chat session', 409, { error: 'revision_conflict', detail: 'Project chat changed' });
    const rejectingRoutes = new AstridLocalAcpRoutes({ requestJson: vi.fn(async () => { throw conflict; }) } as unknown as AstridBridgeTransport);
    await expect(rejectingRoutes.renameProjectSession('project/one', 6, 'opaque:session/1', 'Stale title')).rejects.toBe(conflict);
  });

  it('keeps browser lifecycle controls on the same-origin ACP transport', async () => {
    let connectionCount = 0;
    const requestJson = vi.fn(async (
      _path: string,
      _request: unknown,
      _schema: unknown,
      what: string,
    ) => {
      if (what === 'ACP connect') {
        connectionCount += 1;
        return { connection_id: `connection-${connectionCount}`, initialize: { protocolVersion: 1 } };
      }
      if (what === 'ACP cancel session') return { cancelled: true, session_id: 'omp-session-opaque' };
      if (what === 'ACP disconnect') return { connection_id: 'connection-1', closed: true };
      if (what === 'ACP reconnect') return { connection_id: 'connection-1', reused: true };
      if (what === 'ACP events') return { notifications: [], disconnected: false };
      return { result: { sessionId: 'omp-session-opaque' } };
    });
    const routes = new AstridLocalAcpRoutes({ requestJson } as unknown as AstridBridgeTransport);

    await expect(routes.connect()).resolves.toMatchObject({ connection_id: 'connection-1' });
    await expect(routes.createSession('connection-1', { mcpServers: [] })).resolves.toEqual({ sessionId: 'omp-session-opaque' });
    await expect(routes.resumeSession('connection-1', 'omp-session-opaque')).resolves.toEqual({ sessionId: 'omp-session-opaque' });
    await expect(routes.promptSession('connection-1', 'omp-session-opaque', [{ type: 'text', text: 'hello' }])).resolves.toEqual({ sessionId: 'omp-session-opaque' });
    await expect(routes.setConfigOption('connection-1', 'omp-session-opaque', 'thinking', 'xhigh')).resolves.toEqual({ sessionId: 'omp-session-opaque' });
    await expect(routes.cancelSession('connection-1', 'omp-session-opaque')).resolves.toEqual({
      cancelled: true,
      session_id: 'omp-session-opaque',
    });
    await expect(routes.closeSession('connection-1', 'omp-session-opaque')).resolves.toEqual({ sessionId: 'omp-session-opaque' });
    await expect(routes.events('connection-1')).resolves.toEqual({ notifications: [], disconnected: false });
    await expect(routes.disconnect('connection-1')).resolves.toEqual({ connection_id: 'connection-1', closed: true });
    await expect(routes.reconnect('connection-1')).resolves.toEqual({ connection_id: 'connection-1', reused: true });
    await expect(routes.reconnect()).resolves.toMatchObject({ connection_id: 'connection-2' });

    expect(requestJson.mock.calls.map(([path, request]) => ({
      path,
      method: (request as { method?: string }).method ?? 'GET',
      body: (request as { body?: unknown }).body,
    }))).toEqual([
      { path: '/acp/connect', method: 'POST', body: {} },
      { path: '/acp/connection-1/rpc', method: 'POST', body: { method: 'session/new', params: { mcpServers: [] } } },
      { path: '/acp/connection-1/rpc', method: 'POST', body: { method: 'session/resume', params: { sessionId: 'omp-session-opaque' } } },
      { path: '/acp/connection-1/rpc', method: 'POST', body: { method: 'session/prompt', params: { sessionId: 'omp-session-opaque', prompt: [{ type: 'text', text: 'hello' }] } } },
      { path: '/acp/connection-1/rpc', method: 'POST', body: { method: 'session/set_config_option', params: { sessionId: 'omp-session-opaque', configId: 'thinking', value: 'xhigh' } } },
      { path: '/acp/connection-1/cancel', method: 'POST', body: { sessionId: 'omp-session-opaque' } },
      { path: '/acp/connection-1/rpc', method: 'POST', body: { method: 'session/close', params: { sessionId: 'omp-session-opaque' } } },
      { path: '/acp/connection-1/events', method: 'GET', body: undefined },
      { path: '/acp/connection-1', method: 'DELETE', body: undefined },
      { path: '/acp/connection-1/reconnect', method: 'POST', body: {} },
      { path: '/acp/connect', method: 'POST', body: {} },
    ]);
  });
});
