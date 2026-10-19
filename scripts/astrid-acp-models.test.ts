import { test } from 'node:test';
import assert from 'node:assert/strict';
import { chmodSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { createServer } from 'node:http';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createAstridAcpHttpServer } from './astrid-acp-bridge.ts';

const token = 'test-bridge-token';
const protocolHeader = 'X-Astrid-Bridge-Version';
const configOptions = [{
  id: 'model',
  currentValue: 'openai/gpt-4.1',
  options: [
    { value: 'openai/gpt-4.1', name: 'GPT 4.1' },
    { value: 'openai/gpt-4.1-mini', name: 'GPT 4.1 mini' },
  ],
}];

type HostCall = { connection: string; method: string; params: unknown };
type HostRecord = { connection: string; calls: HostCall[]; disposed: number; releasePrompt?: () => void; promptStarted?: () => void };

function fakeOmp(directory: string): { command: string; rolesPath: string } {
  const packageRoot = join(directory, 'node_modules', '@oh-my-pi', 'pi-coding-agent');
  const executable = join(packageRoot, 'dist', 'cli.js');
  const catalogDirectory = join(directory, 'node_modules', '@oh-my-pi', 'pi-catalog', 'src');
  const rolesPath = join(directory, 'model-roles.json');
  mkdirSync(join(packageRoot, 'dist'), { recursive: true });
  mkdirSync(catalogDirectory, { recursive: true });
  writeFileSync(join(catalogDirectory, 'models.json'), JSON.stringify({
    openai: {
      'gpt-4.1': { name: 'GPT 4.1' },
      'gpt-4.1-mini': { name: 'GPT 4.1 mini' },
    },
    anthropic: { 'claude-sonnet': { name: 'Claude Sonnet' } },
  }));
  writeFileSync(rolesPath, JSON.stringify({ default: 'openai/gpt-4.1', smol: 'openai/gpt-4.1-mini', slow: 'anthropic/claude-sonnet' }));
  const script = `#!/usr/bin/env node
const fs = require('node:fs');
const args = process.argv.slice(2).filter(arg => !arg.startsWith('--profile='));
if (process.env.OMP_FAKE_FAIL === '1') {
  process.stderr.write('credential-secret-should-never-escape');
  process.exit(7);
}
if (args[0] === 'models' && args[1] === 'ls' && args.includes('--json')) {
  process.stdout.write(JSON.stringify({models:[
    {provider:'openai',id:'gpt-4.1',selector:'openai/gpt-4.1',name:'GPT 4.1'},
    {provider:'openai',id:'gpt-4.1-mini',selector:'openai/gpt-4.1-mini',name:'GPT 4.1 mini'}
  ]}));
} else if (args[0] === 'config' && args[1] === 'get' && args[2] === 'modelRoles') {
  process.stdout.write(JSON.stringify({key:'modelRoles',value:JSON.parse(fs.readFileSync(${JSON.stringify(rolesPath)},'utf8'))}));
} else if (args[0] === 'config' && args[1] === 'set' && args[2] === 'modelRoles') {
  fs.writeFileSync(${JSON.stringify(rolesPath)}, args[3]);
} else if (args[0] === 'usage' && args.includes('--json')) {
  process.stdout.write(JSON.stringify({reports:[],accountsWithoutUsage:[],disabledCredentials:[],capacity:{}}));
} else {
  process.stderr.write('credential-secret-should-never-escape');
  process.exit(7);
}
`;
  writeFileSync(executable, script, { mode: 0o755 });
  chmodSync(executable, 0o755);
  return { command: executable, rolesPath };
}

function fakeBun(directory: string): void {
  const bin = join(directory, 'bin');
  mkdirSync(bin, { recursive: true });
  const metadata = {
    providers: [
      { id: 'openai', name: 'OpenAI', models: [{ id: 'gpt-4.1', name: 'GPT 4.1' }, { id: 'gpt-4.1-mini', name: 'GPT 4.1 mini' }] },
      { id: 'anthropic', name: 'Anthropic', models: [{ id: 'claude-sonnet', name: 'Claude Sonnet' }] },
    ],
    loginProviders: [{ id: 'openai-codex', name: 'ChatGPT Plus/Pro (Codex Subscription)' }],
  };
  const executable = join(bin, 'bun');
  writeFileSync(executable, `#!/usr/bin/env node\nprocess.stdout.write(${JSON.stringify(JSON.stringify(metadata))});\n`, { mode: 0o755 });
  chmodSync(executable, 0o755);
}

async function listen(server: ReturnType<typeof createServer>): Promise<string> {
  await new Promise<void>(resolve => server.listen(0, '127.0.0.1', resolve));
  return `http://127.0.0.1:${(server.address() as { port: number }).port}`;
}

async function fixture(advertisedModels?: string[]) {
  const directory = mkdtempSync(join(tmpdir(), 'astrid-acp-model-http-'));
  const omp = fakeOmp(directory);
  fakeBun(directory);
  const originalPath = process.env.PATH;
  process.env.PATH = `${join(directory, 'bin')}${originalPath ? `:${originalPath}` : ''}`;
  const hosts: HostRecord[] = [];
  let nextConnection = 0;
  const registry = { assertOwned: async (_projectId: string, sessionId: string) => assert.equal(sessionId, 'saved-session') };
  const { server, bridge } = createAstridAcpHttpServer({
    config: { token, port: 0, cwd: directory, ompCommand: omp.command, profile: 'test-profile' },
    chatRegistry: registry as never,
    idFactory: () => `c${++nextConnection}`,
    hostFactory: () => {
      const record: HostRecord = { connection: `c${nextConnection}`, calls: [], disposed: 0 };
      hosts.push(record);
      return {
        initialize: async () => ({ protocolVersion: 1 }),
        request: async (method: string, params: unknown) => {
          record.calls.push({ connection: record.connection, method, params });
          if (method === 'session/load' || method === 'session/resume') {
            return { sessionId: 'saved-session', configOptions: advertisedModels
              ? [{ ...configOptions[0], options: configOptions[0].options.filter(option => advertisedModels.includes(option.value)) }]
              : configOptions };
          }
          if (method === 'session/prompt' && record.promptStarted) {
            record.promptStarted();
            await new Promise<void>(resolve => { record.releasePrompt = resolve; });
          }
          return {};
        },
        cancel: async () => {},
        dispose: async () => { record.disposed++; },
      } as never;
    },
  });
  const base = await listen(server);
  const call = (path: string, body?: unknown, init: { method?: string; auth?: boolean; protocol?: string } = {}) => fetch(base + path, {
    method: init.method ?? (body === undefined ? 'GET' : 'POST'),
    headers: {
      ...(init.auth === false ? {} : { Authorization: `Bearer ${token}` }),
      [protocolHeader]: init.protocol ?? 'v1',
      'Content-Type': 'application/json',
    },
    ...(body === undefined ? {} : { body: JSON.stringify(body) }),
  });
  return { directory, omp, hosts, server, bridge, call, originalPath };
}

async function closeFixture(value: Awaited<ReturnType<typeof fixture>>): Promise<void> {
  try { await value.bridge.close(); }
  finally {
    value.server.closeAllConnections();
    await new Promise<void>(resolve => value.server.close(() => resolve()));
    if (value.originalPath === undefined) delete process.env.PATH;
    else process.env.PATH = value.originalPath;
    rmSync(value.directory, { recursive: true, force: true });
  }
}

test('model HTTP routes require the bridge token and protocol, reject unavailable selectors without fallback, and redact OMP stderr', async () => {
  const value = await fixture();
  try {
    assert.equal((await value.call('/models', undefined, { auth: false })).status, 401);
    assert.equal((await value.call('/models', undefined, { protocol: 'v0' })).status, 400);
    const modelsResponse = await value.call('/models');
    assert.equal(modelsResponse.status, 200);
    const models = await modelsResponse.json() as { providers: Array<{ id: string; signedIn: boolean; models: Array<{ id: string }> }>; currentModel: string };
    assert.equal(models.currentModel, 'openai/gpt-4.1');
    assert.ok(models.providers.some(provider => provider.id === 'openai' && provider.signedIn && provider.models.some(model => model.id === 'gpt-4.1-mini')));

    const unavailable = await value.call('/model', { model: 'openai/not-available' });
    assert.equal(unavailable.status, 400);
    const errorBody = await unavailable.text();
    assert.equal(errorBody.includes('credential-secret'), false);
    assert.equal(JSON.parse(readFileSync(value.omp.rolesPath, 'utf8')).default, 'openai/gpt-4.1');
    process.env.OMP_FAKE_FAIL = '1';
    try {
      const failed = await value.call('/model', { model: 'openai/gpt-4.1-mini' });
      assert.equal(failed.status, 500);
      assert.equal((await failed.text()).includes('credential-secret'), false);
    } finally { delete process.env.OMP_FAKE_FAIL; }
    assert.equal((await value.call('/model', { model: 'openai/gpt-4.1-mini' }, { auth: false })).status, 401);
    assert.equal((await value.call('/model', { model: 'openai/gpt-4.1-mini' }, { protocol: 'v0' })).status, 400);
  } finally { await closeFixture(value); }
});

test('a valid model switch retires old hosts and project prompts load the same transcript with the selected model first', async () => {
  const value = await fixture();
  try {
    await value.call('/models');
    assert.equal((await value.call('/connect', {})).status, 200);
    const loaded = await value.call('/c1/rpc', { method: 'session/load', params: { sessionId: 'saved-session', cwd: '/client/must/not/override' } });
    assert.equal(loaded.status, 200);

    const switched = await value.call('/model', { model: 'openai/gpt-4.1-mini' });
    assert.equal(switched.status, 200);
    assert.deepEqual(JSON.parse(readFileSync(value.omp.rolesPath, 'utf8')), {
      default: 'openai/gpt-4.1-mini', smol: 'openai/gpt-4.1-mini', slow: 'anthropic/claude-sonnet',
    });
    assert.equal(value.hosts[0]?.disposed, 1);
    const oldEvents = await value.call('/c1/events');
    assert.equal(oldEvents.status, 200);
    assert.equal((await oldEvents.json() as { disconnected: boolean }).disconnected, true);

    assert.equal((await value.call('/connect', {})).status, 200);
    assert.equal((await value.call('/c2/rpc', { method: 'session/load', params: { sessionId: 'saved-session' } })).status, 200);
    const prompted = await value.call('/projects/project-1/chat/prompt', { connection_id: 'c2', session_id: 'saved-session', prompt: [{ type: 'text', text: 'continue' }] });
    assert.equal(prompted.status, 200);
    assert.deepEqual(value.hosts[1]?.calls.map(call => call.method), [
      'session/load', 'session/set_config_option', 'session/prompt',
    ]);
    assert.deepEqual(value.hosts[1]?.calls[1]?.params, {
      sessionId: 'saved-session', configId: 'model', value: 'openai/gpt-4.1-mini',
    });
    assert.deepEqual(value.hosts[1]?.calls[2]?.params, {
      sessionId: 'saved-session', prompt: [{ type: 'text', text: 'continue' }],
    });
  } finally { await closeFixture(value); }
});

test('model switching returns conflict while an ACP prompt is active', async () => {
  const value = await fixture();
  let notifyPromptStarted: () => void = () => {};
  const promptStarted = new Promise<void>(resolve => { notifyPromptStarted = resolve; });
  try {
    await value.call('/models');
    assert.equal((await value.call('/connect', {})).status, 200);
    await value.call('/c1/rpc', { method: 'session/load', params: { sessionId: 'saved-session' } });
    value.hosts[0]!.promptStarted = notifyPromptStarted;
    const prompt = value.call('/c1/rpc', { method: 'session/prompt', params: { sessionId: 'saved-session', prompt: [{ type: 'text', text: 'busy' }] } });
    await promptStarted;
    const switched = await value.call('/model', { model: 'openai/gpt-4.1-mini' });
    assert.equal(switched.status, 409);
    assert.equal((await switched.json() as { error: string }).error, 'model_change_during_request');
    assert.equal(JSON.parse(readFileSync(value.omp.rolesPath, 'utf8')).default, 'openai/gpt-4.1');
    value.hosts[0]!.releasePrompt?.();
    assert.equal((await prompt).status, 200);
  } finally {
    value.hosts[0]?.releasePrompt?.();
    await closeFixture(value);
  }
});

test('an ACP session missing the selected model cannot silently prompt on its old model', async () => {
  const value = await fixture(['openai/gpt-4.1']);
  try {
    assert.equal((await value.call('/model', { model: 'openai/gpt-4.1-mini' })).status, 200);
    assert.equal((await value.call('/connect', {})).status, 200);
    assert.equal((await value.call('/c1/rpc', { method: 'session/load', params: { sessionId: 'saved-session' } })).status, 200);
    const response = await value.call('/projects/project-1/chat/prompt', {
      connection_id: 'c1', session_id: 'saved-session', prompt: [{ type: 'text', text: 'hello' }],
    });
    assert.equal(response.status, 409);
    assert.equal((await response.json() as { error: string }).error, 'model_unavailable');
    assert.equal(value.hosts[0].calls.some(call => call.method === 'session/prompt'), false);
  } finally { await closeFixture(value); }
});
