import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createAstridAcpHttpServer, resolveAstridAcpBridgeConfig, assertLocalMediaOnly } from './astrid-acp-bridge.ts';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { Readable } from 'node:stream';
import { ProjectChatRegistry } from './astrid-project-chat.ts';
import { ApiError, type Project } from '../src/integrations/runtime/generated.ts';
import type { AcpProcessHostCallbacks } from '../src/tools/video-editor/runtime/processes/acpProcessHost.ts';

function deferred<T = void>() {
  let resolve!: (value: T) => void;
  const promise = new Promise<T>(yes => { resolve = yes; });
  return { promise, resolve };
}

const mediaForms = [
  { type: 'image', data: 'aGVsbG8=', mimeType: 'image/png' },
  { type: 'audio', data: 'aGVsbG8=', mimeType: 'audio/wav' },
  { type: 'resource', resource: { uri: 'local:video', mimeType: 'video/mp4', blob: 'aGVsbG8=' } },
  { type: 'resource', resource: { uri: 'local:unknown', blob: 'aGVsbG8=' } },
  { type: 'resource', resource: { uri: 'local:nested', text: 'context', _meta: { embedded: { type: 'resource', resource: { uri: 'local:audio', mimeType: 'audio/wav', blob: 'aGVsbG8=' } } } } },
  { type: 'resource_link', name: 'inline', uri: 'data:video/mp4;base64,aGVsbG8=' },
];
const textMetadata = [
  { type: 'text', text: 'Keep image/audio/video media local. Use object id obj_a.' },
  { type: 'resource', resource: { uri: 'workspace:timeline_a', mimeType: 'application/json', text: '{"project_id":"p"}' } },
  { type: 'resource_link', name: 'video', mimeType: 'video/mp4', uri: 'workspace:object_a', _meta: { project_id: 'p' } },
];

test('ACP uses dedicated token, legacy fallback, explicit hosted-only policy and known binary forms', () => {
  const env = { ASTRID_BRIDGE_TOKEN: 'runtime', ASTRID_ACP_BRIDGE_TOKEN: 'acp', ASTRID_ACP_CWD: '/tmp/project' };
  assert.equal(resolveAstridAcpBridgeConfig(env).token, 'acp');
  assert.equal(resolveAstridAcpBridgeConfig({ ...env, ASTRID_ACP_BRIDGE_TOKEN: undefined }).token, 'runtime');
  assert.equal(resolveAstridAcpBridgeConfig(env).localMediaOnly, false);
  assert.equal('systemPromptFile' in resolveAstridAcpBridgeConfig(env), false);
  assert.equal(
    resolveAstridAcpBridgeConfig({ ...env, ASTRID_ACP_SYSTEM_PROMPT_FILE: '/opt/astrid/profile.md' }).systemPromptFile,
    '/opt/astrid/profile.md',
  );
  assert.equal(resolveAstridAcpBridgeConfig({ ...env, ASTRID_ACP_LOCAL_MEDIA_ONLY: '1' }).localMediaOnly, true);
  assert.throws(() => resolveAstridAcpBridgeConfig({ ...env, ASTRID_ACP_LOCAL_MEDIA_ONLY: 'yes' }));
  for (const part of mediaForms) assert.throws(() => assertLocalMediaOnly({ prompt: [part] }), /Hosted local-only ACP/);
  assert.doesNotThrow(() => assertLocalMediaOnly({ prompt: textMetadata }));
});

test('PATCH chat rename route validates the body without opening a listener', async () => {
  let project: Project = { project_id: 'p', realm_id: 'r', slug: 'p', name: 'p', metadata: {
    astrid_agent_chat_v1: { 'http-test': { revision: 0, selected_session_id: 's1', main_session_id: null, sessions: [{ id: 's1' }], draft: { text: '', revision: 0, queued_messages: [] } } },
  }, version: 1, created_at: '', updated_at: '' };
  const registry = new ProjectChatRegistry({
    getProject: async () => structuredClone(project),
    listProjects: async () => ({ items: [structuredClone(project)], next_cursor: null }),
    updateProject: async (_id, _key, version, _name, metadata) => {
      assert.equal(version, project.version);
      project = { ...project, version: version + 1, metadata: metadata! };
      return structuredClone(project);
    },
  }, 'http-test');
  const { server, bridge } = createAstridAcpHttpServer({
    config: { token: 'direct-test', port: 0, cwd: '/tmp/local' }, chatRegistry: registry,
  });
  const invoke = async (body: unknown) => {
    const request = Object.assign(Readable.from([Buffer.from(JSON.stringify(body))]), {
      method: 'PATCH', url: '/projects/p/chat', headers: {
        authorization: 'Bearer direct-test', 'x-astrid-bridge-version': 'v1', 'content-type': 'application/json',
      },
    });
    let responseBody = '';
    const response = {
      statusCode: 200, headers: {} as Record<string, string>,
      setHeader(name: string, value: string | number) { this.headers[name] = String(value); },
      end(value?: string) { responseBody = value ?? ''; },
    };
    await bridge.handle(request as never, response as never);
    return { status: response.statusCode, body: JSON.parse(responseBody) as Json };
  };
  try {
    assert.equal((await invoke({ expected_revision: 0, session_id: 's1', title: ' First ' })).status, 200);
    assert.equal((await invoke({ expected_revision: 0, session_id: 's1', title: 'stale' })).status, 409);
    assert.equal((await invoke({ expected_revision: 1, session_id: 's1', title: '   ' })).status, 400);
    assert.equal((await invoke({ expected_revision: 1, session_id: 's1', title: 'x'.repeat(121) })).status, 400);
    assert.equal((await invoke({ expected_revision: 1, session_id: 'foreign', title: 'Nope' })).status, 403);
    const malformed = await invoke({ expected_revision: 1, session_id: 's1', title: 5, selected_session_id: null });
    assert.equal(malformed.status, 400);
    const saved = await registry.get('p');
    assert.equal(saved.selected_session_id, 's1');
    assert.equal(saved.sessions[0]?.title, 'First');
    assert.equal(saved.revision, 1);
  } finally {
    await bridge.close();
    server.close();
  }
});

async function listen(server: import('node:http').Server) {
  await new Promise<void>(resolve => server.listen(0, '127.0.0.1', resolve));
  return `http://127.0.0.1:${(server.address() as { port: number }).port}`;
}

test('real HTTP bridge enforces RPC and project policy for hosted calls and preserves project session/config ownership', async () => {
  const claimDirectory = mkdtempSync(join(tmpdir(), 'astrid-http-chat-'));
  const projects = new Map<string, Project>(['p1', 'p2'].map(project_id => [project_id, {
    project_id, realm_id: 'test-realm', slug: project_id, name: project_id,
    metadata: {}, version: 1, created_at: '', updated_at: '',
  }]));
  const store = {
    getProject: async (id: string) => { const project = projects.get(id); assert.ok(project); return structuredClone(project); },
    listProjects: async () => ({ items: structuredClone([...projects.values()]), next_cursor: null }),
    updateProject: async (id: string, _key: string, version: number, _name?: string, metadata?: Record<string, unknown>) => {
      const project = projects.get(id); assert.ok(project);
      if (project.version !== version) throw new ApiError(409, 'version_conflict', 'changed');
      const updated = { ...project, metadata: metadata ?? project.metadata, version: version + 1 };
      projects.set(id, updated); return structuredClone(updated);
    },
  };
  const registry = new ProjectChatRegistry(store, 'http-test', Date.now, claimDirectory);
  const forwarded: Array<{ method: string; params: unknown }> = [];
  const configOptions = [
    { id: 'model', options: [{ value: 'model-a' }] },
    { id: 'thinking', options: [{ value: 'high' }] },
  ];
  let callbacks: AcpProcessHostCallbacks = {};
  let disposed = 0;
  let nextSession = 0;
  const promptStarted = deferred();
  const releasePrompt = deferred();
  const { server, bridge } = createAstridAcpHttpServer({
    config: { token: 'dedicated', port: 0, cwd: '/tmp/local' },
    chatRegistry: registry,
    idFactory: (() => { let next = 0; return () => `c${++next}`; })(),
    hostFactory: options => {
      const hostCallbacks = options.callbacks ?? {};
      callbacks = hostCallbacks;
      if (options.env) {
        assert.equal(options.env.PI_BASH_NO_LOGIN, '1');
        assert.match(options.env.PI_CONFIG_FILES!, /astrid-acp-local-only.yml$/);
      }
      return {
        initialize: async () => ({ protocolVersion: 1 }),
        request: async (method: string, params: unknown) => {
          forwarded.push({ method, params });
          if (method === 'session/new') return { sessionId: `s${++nextSession}`, configOptions };
          if (method === 'session/resume') return { sessionId: (params as { sessionId: string }).sessionId, configOptions };
          if (method === 'session/list') return { sessions: [{ sessionId: 'unassigned' }] };
          if (method !== 'session/prompt') return {};
          hostCallbacks.onNotification?.({ jsonrpc: '2.0', method: 'session/update', params: { sessionId: (params as { sessionId: string }).sessionId, update: { sessionUpdate: 'agent_message_chunk', content: { type: 'text', text: 'CPU in progress' } } } });
          promptStarted.resolve();
          await releasePrompt.promise;
          return { stopReason: 'end_turn' };
        },
        cancel: async () => {},
        dispose: async () => { disposed++; },
      } as never;
    },
  });
  let pendingPrompt: Promise<Response> | undefined;
  try {
    const acpBase = await listen(server);
    // A hosted call as the Runtime's browser door forwards it (astrid-runtime runtime_protocol/door.py): the bridge's
    // own credential, the protocol version, and the hosted local-media-only policy on every request.
    const call = (path: string, body?: unknown, method = body === undefined ? 'GET' : 'POST') => fetch(acpBase + path, {
      method,
      headers: { Authorization: 'Bearer dedicated', 'X-Astrid-Bridge-Version': 'v1', 'X-Astrid-Local-Media-Only': '1', 'Content-Type': 'application/json' },
      ...(body === undefined ? {} : { body: JSON.stringify(body) }),
    });
    // Direct follow-up deliberately omits the hosted-policy header.
    const direct = (path: string, body: unknown) => fetch(acpBase + path, {
      method: 'POST', headers: { Authorization: 'Bearer dedicated', 'X-Astrid-Bridge-Version': 'v1', 'Content-Type': 'application/json' }, body: JSON.stringify(body),
    });
    assert.equal((await fetch(acpBase + '/health', { headers: { Authorization: 'Bearer runtime', 'X-Astrid-Bridge-Version': 'v1' } })).status, 401);
    assert.equal((await call('/connect', {})).status, 200);
    const hostedCallbacks = callbacks;
    const created = await call('/projects/p1/chat/sessions', { connection_id: 'c1', mode: 'ensure', operation_id: 'create-one' });
    assert.equal(created.status, 200);
    assert.equal((await created.json()).operation_session_id, 's1');
    assert.equal((await registry.get('p1')).selected_session_id, 's1');
    const createdState = await registry.get('p1');
    const rename = (projectId: string, expected_revision: number, session_id: string, title: string) => call(`/projects/${projectId}/chat`, { expected_revision, session_id, title }, 'PATCH');
    assert.equal((await rename('p1', createdState.revision, 's1', '  First chat  ')).status, 200);
    assert.equal((await registry.get('p1')).sessions[0]?.title, 'First chat');
    assert.equal((await rename('p1', createdState.revision, 's1', 'Stale')).status, 409);
    const renamedState = await registry.get('p1');
    for (const title of ['', '   ', 'x'.repeat(121)]) assert.equal((await rename('p1', renamedState.revision, 's1', title)).status, 400);
    assert.equal((await rename('p2', 0, 's1', 'Foreign')).status, 403);
    const rpc = (connection: string, configId: string, value: string, sessionId = 's1') => call(`/${connection}/rpc`, { method: 'session/set_config_option', params: { sessionId, configId, value } });
    assert.equal((await rpc('c1', 'model', 'model-a')).status, 200);
    assert.equal((await rpc('c1', 'thinking', 'high')).status, 200);
    const protectedState = await registry.get('p1');
    const forwardedBeforeMedia = forwarded.length;
    for (const form of mediaForms) {
      for (const response of [
        await call('/c1/rpc', { method: 'session/prompt', params: { sessionId: 's1', prompt: [form] } }),
        await call('/projects/p1/chat/prompt', { connection_id: 'c1', session_id: 's1', prompt: [form] }),
        await direct('/projects/p1/chat/prompt', { connection_id: 'c1', session_id: 's1', prompt: [form] }),
        await direct('/projects/p1/chat/sessions', { connection_id: 'c1', mode: 'new', operation_id: 'blocked', _meta: { form } }),
        await direct('/projects/p1/chat/associate', { connection_id: 'c1', session_id: 'unassigned', expected_revision: protectedState.revision, _meta: { form } }),
        await call('/projects/p1/chat/draft', { expected_revision: 0, text: 'blocked', queued_messages: [{ id: 'q', text: 'queued', session_id: 's1', attachments: [form] }] }, 'PATCH'),
      ]) {
        assert.equal(response.status, 415); assert.equal((await response.json()).error, 'local_media_required');
      }
    }
    assert.equal(forwarded.length, forwardedBeforeMedia);
    assert.deepEqual(await registry.get('p1'), protectedState);
    assert.equal((await call('/projects/p2/chat/prompt', { connection_id: 'c1', session_id: 's1', prompt: textMetadata })).status, 403);
    assert.equal((await call('/projects/p2/chat/associate', { connection_id: 'c1', session_id: 's1', expected_revision: 0 })).status, 409);
    assert.equal(forwarded.length, forwardedBeforeMedia);
    pendingPrompt = call('/projects/p1/chat/prompt', { connection_id: 'c1', session_id: 's1', prompt: textMetadata });
    await promptStarted.promise;
    const events = await (await call('/c1/events')).json();
    assert.equal(events.disconnected, false);
    assert.ok(events.notifications.some((event: Json) => JSON.stringify(event).includes('CPU in progress')));
    assert.ok(events.notifications.some((event: Json) => ((event.params as Json)?.update as Json)?.sessionUpdate === 'astrid_session_control' && ((event.params as Json)?.update as Json)?.active === true));
    releasePrompt.resolve();
    assert.equal((await pendingPrompt).status, 200);
    assert.deepEqual((forwarded[forwarded.length - 1].params as { prompt: unknown }).prompt, textMetadata);
    assert.equal((await direct('/projects/p1/chat/prompt', { connection_id: 'c1', session_id: 's1', prompt: textMetadata })).status, 200);
    assert.equal((await call('/c1/rpc', { method: 'session/prompt', params: { sessionId: 's1', prompt: textMetadata } })).status, 200);
    assert.deepEqual((forwarded[forwarded.length - 1].params as { prompt: unknown }).prompt, textMetadata);
    // Reattach the saved project session through ensure. Its advertised
    // options are shared, while config writes require taking over its writer role.
    assert.equal((await call('/connect', {})).status, 200);
    assert.equal((await rpc('c2', 'model', 'model-a')).status, 400);
    const resumed = await call('/projects/p1/chat/sessions', { connection_id: 'c2', mode: 'ensure', operation_id: 'resume-one' });
    assert.equal(resumed.status, 200); assert.equal((await resumed.json()).operation_session_id, 's1');
    assert.equal(forwarded.filter(item => item.method === 'session/new').length, 1);
    assert.equal(forwarded.filter(item => item.method === 'session/resume').length, 0);
    assert.equal((await rpc('c2', 'model', 'model-a')).status, 409);
    assert.equal((await call('/c2/rpc', { method: 'session/takeover', params: { sessionId: 's1' } })).status, 200);
    assert.equal((await rpc('c2', 'model', 'model-a')).status, 200);
    assert.equal((await rpc('c2', 'thinking', 'high')).status, 200);
    const beforeBadConfig = forwarded.length;
    assert.equal((await rpc('c2', 'model', 'unadvertised')).status, 400);
    assert.equal((await rpc('c2', 'thinking', 'high', 'foreign')).status, 400);
    assert.equal(forwarded.length, beforeBadConfig);
    // Separately configured non-hosted ACP preserves supported media prompts.
    assert.equal((await direct('/connect', {})).status, 200);
    assert.equal((await call('/c3/rpc', { method: 'session/list', params: {} })).status, 409);
    const directCreated = await direct('/projects/p1/chat/sessions', { connection_id: 'c3', mode: 'new', operation_id: 'direct-one' });
    assert.equal(directCreated.status, 200);
    const directSessionId = (await directCreated.json() as Json).operation_session_id as string;
    assert.notEqual(directSessionId, 's1');
    assert.equal((await direct('/c3/rpc', { method: 'session/prompt', params: { sessionId: directSessionId, prompt: [mediaForms[0]] } })).status, 200);
    assert.equal((await direct('/projects/p1/chat/prompt', { connection_id: 'c3', session_id: directSessionId, prompt: [mediaForms[0]] })).status, 200);
    hostedCallbacks.onNotification?.({ jsonrpc: '2.0', method: 'session/update', params: { text: 'x'.repeat(1024 * 1024) } });
    const overflow = await (await call('/c1/events')).json();
    assert.equal(overflow.disconnected, true); assert.equal(overflow.notifications[0].params.code, 'acp_event_overflow');
    assert.equal(disposed, 0); // c2 still follows s1, so c1 remains the physical owner
    assert.equal((await call('/c1/reconnect', {})).status, 502);
    assert.equal((await call('/c1', undefined, 'DELETE')).status, 200);
  } finally {
    releasePrompt.resolve();
    await (pendingPrompt ?? Promise.resolve()).catch(() => {});
    try { await bridge.close(); }
    finally {
      const servers = [server];
      for (const owned of servers) owned.closeAllConnections();
      try { await Promise.all(servers.map(owned => new Promise<void>(resolve => owned.close(() => resolve())))); }
      finally { rmSync(claimDirectory, { recursive: true, force: true }); }
    }
  }
});

test('idle sweep disposes abandoned connections, keeps polled and in-flight ones, and answers late polls as disconnected', async () => {
  let clock = 0;
  let nextId = 0;
  const disposed: string[] = [];
  const started = deferred();
  const releasePrompt = deferred();
  let pendingPrompt: Promise<Response> | undefined;
  const { server, bridge } = createAstridAcpHttpServer({
    config: { token: 'dedicated', port: 0, cwd: '/tmp/local' },
    chatRegistry: {} as never,
    now: () => clock,
    idFactory: () => `c${++nextId}`,
    hostFactory: () => {
      const id = `c${nextId}`;
      return {
        initialize: async () => ({ protocolVersion: 1 }),
        request: async (method: string, params: unknown) => {
          if (method === 'session/load') return { sessionId: (params as { sessionId: string }).sessionId };
          if (method === 'session/prompt') { started.resolve(); await releasePrompt.promise; }
          return {};
        },
        cancel: async () => {},
        dispose: async () => { disposed.push(id); },
      } as never;
    },
  });
  try {
    const base = await listen(server);
    const call = (path: string, init: RequestInit = {}) => fetch(base + path, {
      ...init, headers: { Authorization: 'Bearer dedicated', 'X-Astrid-Bridge-Version': 'v1', 'Content-Type': 'application/json' },
    });
    for (let i = 0; i < 4; i++) assert.equal((await call('/connect', { method: 'POST', body: '{}' })).status, 200);
    // c1 abandoned, c2 keeps polling, c3 has a prompt in flight, c4 is fresh.
    clock = 10 * 60_000;
    assert.equal((await call('/c2/events')).status, 200);
    assert.equal((await call('/c3/rpc', { method: 'POST', body: JSON.stringify({ method: 'session/load', params: { sessionId: 's' } }) })).status, 200);
    pendingPrompt = call('/c3/rpc', { method: 'POST', body: JSON.stringify({ method: 'session/prompt', params: { sessionId: 's', prompt: [] } }) });
    await started.promise;
    clock = 16 * 60_000;
    assert.equal((await call('/c4/events')).status, 200);
    await bridge.reapIdle();
    assert.deepEqual(disposed, ['c1']);
    assert.equal((await call('/c2/events')).status, 200);
    assert.deepEqual(await (await call('/c1/events')).json(), { notifications: [], disconnected: true });
    assert.equal((await call('/c1/rpc', { method: 'POST', body: '{}' })).status, 404);
    // The in-flight prompt restarts its idle clock when it finishes, not before.
    clock = 60 * 60_000;
    await bridge.reapIdle();
    assert.deepEqual(disposed, ['c1', 'c2', 'c4']);
    releasePrompt.resolve();
    assert.equal((await pendingPrompt).status, 200);
    await bridge.reapIdle();
    assert.deepEqual(disposed, ['c1', 'c2', 'c4']);
    clock = 120 * 60_000;
    await bridge.reapIdle();
    assert.deepEqual(disposed, ['c1', 'c2', 'c4', 'c3']);
  } catch (error) {
    console.error(error);
    throw error;
  } finally {
    releasePrompt.resolve();
    await (pendingPrompt ?? Promise.resolve()).catch(() => {});
    await bridge.close();
    server.closeAllConnections();
    server.close();
  }
});
