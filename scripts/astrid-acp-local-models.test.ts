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
            const sessionId = `claude-code:s${++nextSession}`;
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
        ? { sessionId: 'claude-code:s1', configId: 'model', value: 'beta' }
        : { sessionId: 'claude-code:s1', modelId: 'beta' });
      const initialModelState = await (await call('/c1/models?sessionId=claude-code%3As1')).json() as { models: { currentModelId: string; availableModels: Array<{ modelId: string }> } };
      assert.equal(initialModelState.models.currentModelId, 'beta');
      assert.deepEqual(initialModelState.models.availableModels.map(model => model.modelId), ['alpha', 'beta']);
      assert.equal((await call('/c1/models?sessionId=foreign')).status, 400);
      assert.equal((await call('/c1/model', { sessionId: 'foreign', modelId: 'alpha' })).status, 403);
      assert.equal((await call('/c1/model', { sessionId: 'claude-code:s1', modelId: 'missing' })).status, 409);

      failSet = true;
      assert.equal((await call('/c1/model', { sessionId: 'claude-code:s1', modelId: 'alpha' })).status, 500);
      assert.equal((await (await call('/c1/models?sessionId=claude-code%3As1')).json() as { models: { currentModelId: string } }).models.currentModelId, 'beta');
      failSet = false;
      assert.equal((await call('/c1/model', { sessionId: 'claude-code:s1', modelId: 'alpha' })).status, 200);
      returnedSetModel = 'alpha';
      assert.equal((await call('/c1/model', { sessionId: 'claude-code:s1', modelId: 'beta' })).status, 409);
      assert.equal((await (await call('/c1/models?sessionId=claude-code%3As1')).json() as { models: { currentModelId: string } }).models.currentModelId, 'alpha');
      returnedSetModel = undefined;

      const promptStarted = new Promise<void>(resolve => { signalPromptStarted = resolve; });
      const pending = call('/c1/rpc', { method: 'session/prompt', params: { sessionId: 'claude-code:s1', prompt: [] } });
      await promptStarted;
      assert.equal((await call('/c1/model', { sessionId: 'claude-code:s1', modelId: 'beta' })).status, 409);
      releasePrompt?.();
      assert.equal((await pending).status, 200);

      const nextCreated = await call('/c1/rpc', { method: 'session/new', params: {} });
      assert.equal(nextCreated.status, 200);
      const nextSet = calls.filter(call => call.method === (adapter === 'config' ? 'session/set_config_option' : 'session/set_model')).at(-1)!;
      assert.deepEqual(nextSet.params, adapter === 'config'
        ? { sessionId: 'claude-code:s2', configId: 'model', value: 'alpha' }
        : { sessionId: 'claude-code:s2', modelId: 'alpha' });

      // Loading a saved chat retains its reported model and ignores the connection default.
      const loaded = await call('/c1/rpc', { method: 'session/load', params: { sessionId: 'claude-code:saved' } });
      assert.equal(loaded.status, 200);
      const loadedModels = await (await call('/c1/models?sessionId=claude-code%3Asaved')).json() as { models: { currentModelId: string } };
      assert.equal(loadedModels.models.currentModelId, 'beta');
      assert.equal((await call('/c1/rpc', { method: 'session/close', params: { sessionId: 'claude-code:saved' } })).status, 200);
      assert.equal((await call('/c1/models?sessionId=claude-code%3Asaved')).status, 400);
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
      request: async (method: string) => { calls.push(method); return method === 'session/new' ? { sessionId: 'codex:plain' } : {}; },
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
    assert.deepEqual(await (await call('/c1/models?sessionId=codex%3Aplain')).json(), { models: null });
  } finally {
    await bridge.close(); server.closeAllConnections(); await new Promise<void>(resolve => server.close(() => resolve()));
  }
});

test('shared external session model catalog follows the writer and takeover for config and legacy model APIs', async t => {
  for (const adapter of ['config', 'models'] as const) await t.test(`${adapter} adapter`, async () => {
    const hostCalls: Array<Array<{ method: string; params: unknown }>> = [];
    const nativeNotify: Array<((notification: unknown) => void) | undefined> = [];
    let hostNumber = 0;
    const configOptions = (currentValue: string) => [{
      id: 'model', currentValue,
      options: [{ group: 'models', options: ['alpha', 'beta'].map(value => ({ value, name: value.toUpperCase() })) }],
    }];
    const modelList = (currentModelId: string, available = ['alpha', 'beta']) => ({ currentModelId, availableModels: available.map(modelId => ({ modelId, name: modelId.toUpperCase() })) });
    const { server, bridge } = createAstridAcpHttpServer({
      config: { token: 'shared-model-token', port: 0, cwd: '/tmp/local' },
      idFactory: (() => { let id = 0; return () => `c${++id}`; })(),
      localAgentHostFactory: async (_agent, options) => {
        const index = hostNumber++;
        const calls: Array<{ method: string; params: unknown }> = [];
        hostCalls[index] = calls;
        nativeNotify[index] = options.callbacks?.onNotification as ((notification: unknown) => void) | undefined;
        return {
          initialize: async () => ({ protocolVersion: 1 }),
          request: async (method: string, params: unknown) => {
            calls.push({ method, params });
            if (method === 'session/new') return {
              sessionId: 'claude-code:shared-model-session',
              ...(adapter === 'config' ? { configOptions: configOptions('alpha') } : { models: modelList('alpha') }),
            };
            if (method === 'session/load') return {
              sessionId: (params as { sessionId: string }).sessionId,
              ...(adapter === 'config' ? { configOptions: configOptions('alpha') } : { models: modelList('alpha') }),
            };
            if (method === 'session/set_config_option') return { configOptions: configOptions((params as { value: string }).value) };
            if (method === 'session/set_model') return { models: modelList((params as { modelId: string }).modelId) };
            return {};
          },
          cancel: async () => {}, dispose: async () => {},
        } as never;
      },
    });
    try {
      const base = await listen(server);
      const call = (path: string, body?: unknown) => fetch(base + path, {
        method: body === undefined ? 'GET' : 'POST',
        headers: { Authorization: 'Bearer shared-model-token', 'X-Astrid-Bridge-Version': 'v1', 'Content-Type': 'application/json' },
        ...(body === undefined ? {} : { body: JSON.stringify(body) }),
      });
      assert.equal((await call('/connect', { agent: 'claude-code' })).status, 200);
      assert.equal((await call('/connect', { agent: 'claude-code' })).status, 200);
      const sessionId = 'claude-code:shared-model-session';
      assert.equal((await call('/c1/rpc', { method: 'session/new', params: {} })).status, 200);
      assert.equal((await call('/c2/rpc', { method: 'session/load', params: { sessionId } })).status, 200);
      const modelsUrl = `/c2/models?sessionId=${encodeURIComponent(sessionId)}`;
      const formerWriterModelsUrl = `/c1/models?sessionId=${encodeURIComponent(sessionId)}`;
      await call('/c2/events');
      const attachedModels = await (await call(modelsUrl)).json() as { models: { currentModelId: string; availableModels: Array<{ modelId: string }> } };
      assert.equal(attachedModels.models.currentModelId, 'alpha');
      assert.deepEqual(attachedModels.models.availableModels.map(model => model.modelId), ['alpha', 'beta']);
      assert.equal(hostCalls[1]!.length, 0); // follower attached from bridge cache

      const update = async (clientId: string, modelId: string) => adapter === 'config'
        ? call(`/${clientId}/rpc`, { method: 'session/set_config_option', params: { sessionId, configId: 'model', value: modelId } })
        : call(`/${clientId}/model`, { sessionId, modelId });
      assert.equal((await update('c1', 'beta')).status, 200);
      assert.equal(((await (await call(modelsUrl)).json() as { models: { currentModelId: string } }).models.currentModelId), 'beta');
      const setterEvents = (await (await call('/c2/events')).json() as { notifications: Array<{ params?: { update?: Record<string, unknown> } }> }).notifications;
      const setterUpdate = setterEvents.find(event => event.params?.update?.sessionUpdate === (adapter === 'config' ? 'config_option_update' : 'current_model_update'))?.params?.update;
      assert.ok(setterUpdate);
      if (adapter === 'config') assert.equal((setterUpdate!.configOptions as Array<{ currentValue: string }>)[0]!.currentValue, 'beta');
      else assert.equal(setterUpdate!.currentModelId, 'beta');
      const callsBeforeDenied = hostCalls.flat().length;
      const denied = await update('c2', 'alpha');
      assert.equal(denied.status, 409);
      assert.equal((await denied.json() as { error: string }).error, 'session_read_only');
      assert.equal(hostCalls.flat().length, callsBeforeDenied);
      await call('/c1/events'); // consume the first writer's beta update before takeover

      assert.equal((await call('/c2/rpc', { method: 'session/takeover', params: { sessionId } })).status, 200);
      assert.equal((await update('c2', 'alpha')).status, 200);
      const writerState = await (await call(modelsUrl)).json() as { models: { currentModelId: string } };
      assert.equal(writerState.models.currentModelId, 'alpha');
      const formerWriterEvents = (await (await call('/c1/events')).json() as { notifications: Array<{ params?: { update?: Record<string, unknown> } }> }).notifications;
      const alphaUpdate = formerWriterEvents.find(event => event.params?.update?.sessionUpdate === (adapter === 'config' ? 'config_option_update' : 'current_model_update'))?.params?.update;
      assert.ok(alphaUpdate);
      if (adapter === 'config') assert.equal((alphaUpdate!.configOptions as Array<{ currentValue: string }>)[0]!.currentValue, 'alpha');
      else assert.equal(alphaUpdate!.currentModelId, 'alpha');
      await call('/c2/events');
      const expectedSetter = adapter === 'config' ? 'session/set_config_option' : 'session/set_model';
      const nativeUpdates = hostCalls[0]!.filter(item => item.method === expectedSetter);
      assert.equal(nativeUpdates.length, 2);
      assert.equal(hostCalls[1]!.length, 0);
      assert.equal((nativeUpdates[1]!.params as Record<string, unknown>).sessionId, sessionId);

      const changedCatalog = adapter === 'config'
        ? { sessionUpdate: 'config_option_update', configOptions: configOptions('gamma').map(item => ({ ...item, options: [{ group: 'models', options: ['beta', 'gamma'].map(value => ({ value, name: value.toUpperCase() })) }] })) }
        : { sessionUpdate: 'current_model_update', currentModelId: 'gamma', models: modelList('gamma', ['beta', 'gamma']) };
      nativeNotify[0]?.({ jsonrpc: '2.0', method: 'session/update', params: { sessionId, update: changedCatalog } });
      const nativeEvents = (await (await call('/c1/events')).json() as { notifications: Array<{ params?: { update?: Record<string, unknown> } }> }).notifications;
      const nativeUpdate = nativeEvents.find(event => event.params?.update?.sessionUpdate === changedCatalog.sessionUpdate)?.params?.update;
      assert.ok(nativeUpdate);
      if (adapter === 'config') {
        assert.equal((nativeUpdate!.configOptions as Array<{ currentValue: string }>)[0]!.currentValue, 'gamma');
        assert.deepEqual(((nativeUpdate!.configOptions as Array<{ options: Array<{ options: Array<{ value: string }> }> }>)[0]!.options[0]!.options).map(item => item.value), ['beta', 'gamma']);
      } else {
        assert.equal(nativeUpdate!.currentModelId, 'gamma');
        assert.deepEqual(((nativeUpdate!.models as { availableModels: Array<{ modelId: string }> }).availableModels).map(item => item.modelId), ['beta', 'gamma']);
      }
      const nativeLoadCount = hostCalls[0]!.filter(item => item.method === 'session/load').length;
      const reload = await call('/c1/rpc', { method: 'session/load', params: { sessionId } });
      assert.equal(reload.status, 200);
      const reloadResult = (await reload.json() as { result: Record<string, unknown> }).result;
      if (adapter === 'config') assert.equal((reloadResult.configOptions as Array<{ currentValue: string }>)[0]!.currentValue, 'gamma');
      else assert.equal((reloadResult.models as { currentModelId: string }).currentModelId, 'gamma');
      assert.equal(hostCalls[0]!.filter(item => item.method === 'session/load').length, nativeLoadCount);
      assert.equal(((await (await call(formerWriterModelsUrl)).json() as { models: { currentModelId: string } }).models.currentModelId), 'gamma');
    } finally {
      await bridge.close(); server.closeAllConnections(); await new Promise<void>(resolve => server.close(() => resolve()));
    }
  });
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
        if (method === 'session/new') return { sessionId: `claude-code:project-${++sessionNumber}`, configOptions: [{ id: 'model', currentValue: 'alpha', options: [{ value: 'alpha', name: 'Alpha' }] }] };
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
    assert.equal((await created.json() as { operation_session_id: string }).operation_session_id, 'claude-code:project-1');
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
    assert.equal((await call('/notify-connection/rpc', { method: 'session/load', params: { sessionId: 'claude-code:owned' } })).status, 200);
    assert.deepEqual(await (await call('/notify-connection/models?sessionId=claude-code%3Aowned')).json(), {
      models: { currentModelId: 'alpha', availableModels: [{ modelId: 'alpha', name: 'ALPHA' }, { modelId: 'beta', name: 'BETA' }] },
    });
    onNotification?.({
      jsonrpc: '2.0', method: 'session/update',
      params: { sessionId: 'claude-code:owned', update: { sessionUpdate: 'config_option_update', configOptions: configOptions('gamma', ['beta', 'gamma']) } },
    });
    assert.deepEqual(await (await call('/notify-connection/models?sessionId=claude-code%3Aowned')).json(), {
      models: { currentModelId: 'gamma', availableModels: [{ modelId: 'beta', name: 'BETA' }, { modelId: 'gamma', name: 'GAMMA' }] },
    });
    onNotification?.({
      jsonrpc: '2.0', method: 'session/update',
      params: { sessionId: 'claude-code:unowned', update: { sessionUpdate: 'config_option_update', configOptions: configOptions('gamma', ['gamma']) } },
    });
    assert.equal((await call('/notify-connection/models?sessionId=claude-code%3Aunowned')).status, 400);
  } finally {
    await bridge.close(); server.closeAllConnections(); await new Promise<void>(resolve => server.close(() => resolve()));
  }
});
