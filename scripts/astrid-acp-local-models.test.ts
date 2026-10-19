import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createAstridAcpHttpServer } from './astrid-acp-bridge.ts';

async function listen(server: import('node:http').Server): Promise<string> {
  await new Promise<void>(resolve => server.listen(0, '127.0.0.1', resolve));
  return `http://127.0.0.1:${(server.address() as { port: number }).port}`;
}

test('local ACP models are scoped, selectable and used as the connection default for new sessions', async t => {
  for (const adapter of ['config', 'models'] as const) await t.test(`${adapter} adapter`, async () => {
    const calls: Array<{ method: string; params: unknown }> = [];
    let failSet = false;
    let returnedSetModel: string | undefined;
    let releasePrompt: (() => void) | undefined;
    let signalPromptStarted: (() => void) | undefined;
    let nextSession = 0;
    const { server, bridge } = createAstridAcpHttpServer({
      config: { token: 'local-model-token', port: 0, cwd: '/tmp/local' },
      idFactory: () => 'c1',
      localAgentHostFactory: async () => ({
        initialize: async () => ({ protocolVersion: 1 }),
        request: async (method: string, params: unknown) => {
          calls.push({ method, params });
          if (method === 'session/new') {
            const sessionId = `s${++nextSession}`;
            return adapter === 'config'
              ? { sessionId, configOptions: [{ id: 'model', currentValue: 'alpha', options: [{ group: 'g', options: [{ value: 'alpha', name: 'Alpha' }, { value: 'beta', name: 'Beta' }] }] }], models: { currentModelId: 'legacy/alpha-high', availableModels: [{ modelId: 'legacy/alpha-high', name: 'Alpha high' }] } }
              : { sessionId, models: { currentModelId: 'alpha', availableModels: [{ modelId: 'alpha', name: 'Alpha' }, { modelId: 'beta', name: 'Beta' }] } };
          }
          if (method === 'session/load') return adapter === 'config'
            ? { sessionId: (params as { sessionId: string }).sessionId, configOptions: [{ id: 'model', currentValue: 'beta', options: [{ group: 'g', options: [{ value: 'alpha', name: 'Alpha' }, { value: 'beta', name: 'Beta' }] }] }], models: { currentModelId: 'legacy/beta-high', availableModels: [{ modelId: 'legacy/beta-high', name: 'Beta high' }] } }
            : { sessionId: (params as { sessionId: string }).sessionId, models: { currentModelId: 'beta', availableModels: [{ modelId: 'alpha', name: 'Alpha' }, { modelId: 'beta', name: 'Beta' }] } };
          if (method === 'session/prompt') {
            signalPromptStarted?.();
            await new Promise<void>(resolve => { releasePrompt = resolve; });
          }
          if (method === 'session/set_model' || method === 'session/set_config_option') {
            if (failSet) throw new Error('adapter rejected model');
            const modelId = returnedSetModel ?? (params as { modelId?: string; value?: string }).modelId ?? (params as { value?: string }).value!;
            return adapter === 'config'
              ? { configOptions: [{ id: 'model', currentValue: modelId, options: [{ group: 'g', options: [{ value: 'alpha', name: 'Alpha' }, { value: 'beta', name: 'Beta' }] }] }], models: { currentModelId: `legacy/${modelId}-high`, availableModels: [{ modelId: `legacy/${modelId}-high`, name: 'legacy' }] } }
              : returnedSetModel === undefined ? {} : { models: { currentModelId: modelId, availableModels: [{ modelId: 'alpha', name: 'Alpha' }, { modelId: 'beta', name: 'Beta' }] } };
          }
          return {};
        },
        cancel: async () => {},
        dispose: async () => {},
      } as never),
    });
    try {
      const base = await listen(server);
      const call = (path: string, body?: unknown, method = body === undefined ? 'GET' : 'POST') => fetch(base + path, {
        method, headers: { Authorization: 'Bearer local-model-token', 'X-Astrid-Bridge-Version': 'v1', 'Content-Type': 'application/json' },
        ...(body === undefined ? {} : { body: JSON.stringify(body) }),
      });
      const connected = await call('/connect', { agent: 'claude-code', defaultModelId: 'beta' });
      assert.equal(connected.status, 200);
      const created = await call('/c1/rpc', { method: 'session/new', params: {} });
      assert.equal(created.status, 200);
      assert.deepEqual((await created.json() as { result: { models?: { currentModelId: string } } }).result.models?.currentModelId, 'beta');
      const defaultSelection = calls.find(call => call.method === (adapter === 'config' ? 'session/set_config_option' : 'session/set_model'))!;
      assert.ok(defaultSelection);
      assert.deepEqual(defaultSelection.params, adapter === 'config'
        ? { sessionId: 's1', configId: 'model', value: 'beta' }
        : { sessionId: 's1', modelId: 'beta' });
      const initialModelState = await (await call('/c1/models?sessionId=s1')).json() as { models: { currentModelId: string; availableModels: Array<{ modelId: string }> } };
      assert.equal(initialModelState.models.currentModelId, 'beta');
      assert.deepEqual(initialModelState.models.availableModels.map(model => model.modelId), ['alpha', 'beta']);
      assert.equal((await call('/c1/models?sessionId=foreign')).status, 400);
      assert.equal((await call('/c1/model', { sessionId: 'foreign', modelId: 'alpha' })).status, 403);
      assert.equal((await call('/c1/model', { sessionId: 's1', modelId: 'missing' })).status, 409);

      failSet = true;
      assert.equal((await call('/c1/model', { sessionId: 's1', modelId: 'alpha' })).status, 500);
      assert.equal((await (await call('/c1/models?sessionId=s1')).json() as { models: { currentModelId: string } }).models.currentModelId, 'beta');
      failSet = false;
      assert.equal((await call('/c1/model', { sessionId: 's1', modelId: 'alpha' })).status, 200);
      returnedSetModel = 'alpha';
      assert.equal((await call('/c1/model', { sessionId: 's1', modelId: 'beta' })).status, 409);
      assert.equal((await (await call('/c1/models?sessionId=s1')).json() as { models: { currentModelId: string } }).models.currentModelId, 'alpha');
      returnedSetModel = undefined;

      const promptStarted = new Promise<void>(resolve => { signalPromptStarted = resolve; });
      const pending = call('/c1/rpc', { method: 'session/prompt', params: { sessionId: 's1', prompt: [] } });
      await promptStarted;
      assert.equal((await call('/c1/model', { sessionId: 's1', modelId: 'beta' })).status, 409);
      releasePrompt?.();
      assert.equal((await pending).status, 200);

      const nextCreated = await call('/c1/rpc', { method: 'session/new', params: {} });
      assert.equal(nextCreated.status, 200);
      const nextSet = calls.filter(call => call.method === (adapter === 'config' ? 'session/set_config_option' : 'session/set_model')).at(-1)!;
      assert.deepEqual(nextSet.params, adapter === 'config'
        ? { sessionId: 's2', configId: 'model', value: 'alpha' }
        : { sessionId: 's2', modelId: 'alpha' });

      // Loading a saved chat retains its reported model and ignores the connection default.
      const loaded = await call('/c1/rpc', { method: 'session/load', params: { sessionId: 'saved' } });
      assert.equal(loaded.status, 200);
      const loadedModels = await (await call('/c1/models?sessionId=saved')).json() as { models: { currentModelId: string } };
      assert.equal(loadedModels.models.currentModelId, 'beta');
      assert.equal((await call('/c1/rpc', { method: 'session/close', params: { sessionId: 'saved' } })).status, 200);
      assert.equal((await call('/c1/models?sessionId=saved')).status, 400);
    } finally {
      releasePrompt?.();
      await bridge.close();
      server.closeAllConnections();
      await new Promise<void>(resolve => server.close(() => resolve()));
    }
  });
});

test('local ACP connections without advertised models keep the ordinary session path', async () => {
  const calls: string[] = [];
  const { server, bridge } = createAstridAcpHttpServer({
    config: { token: 'local-model-token', port: 0, cwd: '/tmp/local' },
    idFactory: () => 'c1',
    localAgentHostFactory: async () => ({
      initialize: async () => ({ protocolVersion: 1 }),
      request: async (method: string) => { calls.push(method); return method === 'session/new' ? { sessionId: 'plain' } : {}; },
      cancel: async () => {}, dispose: async () => {},
    } as never),
  });
  try {
    const base = await listen(server);
    const call = (path: string, body?: unknown) => fetch(base + path, {
      method: body === undefined ? 'GET' : 'POST', headers: { Authorization: 'Bearer local-model-token', 'X-Astrid-Bridge-Version': 'v1', 'Content-Type': 'application/json' },
      ...(body === undefined ? {} : { body: JSON.stringify(body) }),
    });
    assert.equal((await call('/connect', { agent: 'codex', defaultModelId: 'missing' })).status, 200);
    assert.equal((await call('/c1/rpc', { method: 'session/new', params: {} })).status, 200);
    assert.deepEqual(calls, ['session/new']);
    assert.deepEqual(await (await call('/c1/models?sessionId=plain')).json(), { models: null });
  } finally {
    await bridge.close(); server.closeAllConnections(); await new Promise<void>(resolve => server.close(() => resolve()));
  }
});

test('project registry session creation applies the connection default and rejects unavailable defaults', async () => {
  const calls: Array<{ method: string; params: unknown }> = [];
  let sessionNumber = 0;
  let connectionNumber = 0;
  const { server, bridge } = createAstridAcpHttpServer({
    config: { token: 'local-model-token', port: 0, cwd: '/tmp/local' },
    idFactory: () => `c${++connectionNumber}`,
    chatRegistry: {
      create: async (_projectId: string, _mode: string, _operationId: string, createSession: () => Promise<unknown>) => {
        const result = await createSession() as { sessionId: string };
        return { operation_session_id: result.sessionId };
      },
    } as never,
    localAgentHostFactory: async () => ({
      initialize: async () => ({ protocolVersion: 1 }),
      request: async (method: string, params: unknown) => {
        calls.push({ method, params });
        if (method === 'session/new') return { sessionId: `project-${++sessionNumber}`, configOptions: [{ id: 'model', currentValue: 'alpha', options: [{ value: 'alpha', name: 'Alpha' }] }] };
        if (method === 'session/set_config_option') return { configOptions: [{ id: 'model', currentValue: 'alpha', options: [{ value: 'alpha', name: 'Alpha' }] }] };
        return {};
      },
      cancel: async () => {}, dispose: async () => {},
    } as never),
  });
  try {
    const base = await listen(server);
    const call = (path: string, body?: unknown) => fetch(base + path, {
      method: body === undefined ? 'GET' : 'POST', headers: { Authorization: 'Bearer local-model-token', 'X-Astrid-Bridge-Version': 'v1', 'Content-Type': 'application/json' },
      ...(body === undefined ? {} : { body: JSON.stringify(body) }),
    });
    assert.equal((await call('/connect', { agent: 'claude-code', defaultModelId: 'alpha' })).status, 200);
    const created = await call('/projects/p1/chat/sessions', { connection_id: 'c1', mode: 'new', operation_id: 'project-create' });
    assert.equal(created.status, 200);
    assert.equal((await created.json() as { operation_session_id: string }).operation_session_id, 'project-1');
    assert.deepEqual(calls.map(call => call.method), ['session/new', 'session/set_config_option']);

    // A separate connection with an unavailable default fails closed when the
    // new session reports its supported model config.
    assert.equal((await call('/connect', { agent: 'claude-code', defaultModelId: 'missing' })).status, 200);
    const unavailable = await call('/projects/p1/chat/sessions', { connection_id: 'c2', mode: 'new', operation_id: 'project-unavailable' });
    assert.equal(unavailable.status, 409);
  } finally {
    await bridge.close(); server.closeAllConnections(); await new Promise<void>(resolve => server.close(() => resolve()));
  }
});

test('config model update notifications refresh only an owned session model cache', async () => {
  let onNotification: ((notification: unknown) => void) | undefined;
  const configOptions = (currentValue: string, values: string[]) => [{
    id: 'model', currentValue,
    options: [{ group: 'models', options: values.map(value => ({ value, name: value.toUpperCase() })) }],
  }];
  const { server, bridge } = createAstridAcpHttpServer({
    config: { token: 'local-model-token', port: 0, cwd: '/tmp/local' },
    idFactory: () => 'notify-connection',
    localAgentHostFactory: async (_agent, options) => {
      onNotification = options.callbacks?.onNotification;
      return {
        initialize: async () => ({ protocolVersion: 1 }),
        request: async (method: string, params: unknown) => method === 'session/load'
          ? { sessionId: (params as { sessionId: string }).sessionId, configOptions: configOptions('alpha', ['alpha', 'beta']) }
          : {},
        cancel: async () => {}, dispose: async () => {},
      } as never;
    },
  });
  try {
    const base = await listen(server);
    const call = (path: string, body?: unknown) => fetch(base + path, {
      method: body === undefined ? 'GET' : 'POST', headers: { Authorization: 'Bearer local-model-token', 'X-Astrid-Bridge-Version': 'v1', 'Content-Type': 'application/json' },
      ...(body === undefined ? {} : { body: JSON.stringify(body) }),
    });
    assert.equal((await call('/connect', { agent: 'claude-code' })).status, 200);
    assert.equal((await call('/notify-connection/rpc', { method: 'session/load', params: { sessionId: 'owned' } })).status, 200);
    assert.deepEqual(await (await call('/notify-connection/models?sessionId=owned')).json(), {
      models: { currentModelId: 'alpha', availableModels: [{ modelId: 'alpha', name: 'ALPHA' }, { modelId: 'beta', name: 'BETA' }] },
    });
    onNotification?.({
      jsonrpc: '2.0', method: 'session/update',
      params: { sessionId: 'owned', update: { sessionUpdate: 'config_option_update', configOptions: configOptions('gamma', ['beta', 'gamma']) } },
    });
    assert.deepEqual(await (await call('/notify-connection/models?sessionId=owned')).json(), {
      models: { currentModelId: 'gamma', availableModels: [{ modelId: 'beta', name: 'BETA' }, { modelId: 'gamma', name: 'GAMMA' }] },
    });
    onNotification?.({
      jsonrpc: '2.0', method: 'session/update',
      params: { sessionId: 'unowned', update: { sessionUpdate: 'config_option_update', configOptions: configOptions('gamma', ['gamma']) } },
    });
    assert.equal((await call('/notify-connection/models?sessionId=unowned')).status, 400);
  } finally {
    await bridge.close(); server.closeAllConnections(); await new Promise<void>(resolve => server.close(() => resolve()));
  }
});
