import { test } from 'bun:test';
import assert from 'node:assert/strict';
import { chmodSync, mkdtempSync, readFileSync, realpathSync, rmSync, writeFileSync } from 'node:fs';
import { createServer } from 'node:http';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createAstridAcpHttpServer } from './astrid-acp-bridge.ts';
import type { ProjectChatRegistry } from './astrid-project-chat.ts';

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
type CliInvocation = { args: string[]; cwd: string; profile: string | null };

function invocations(path: string): CliInvocation[] {
  return readFileSync(path, 'utf8').trim().split('\n').filter(Boolean).map(line => JSON.parse(line) as CliInvocation);
}

function fakeAstrid(directory: string): { command: string; invocationsPath: string; selectedPath: string } {
  const executable = join(directory, 'astrid');
  const invocationsPath = join(directory, 'invocations.jsonl');
  const selectedPath = join(directory, 'selected-model.txt');
  writeFileSync(selectedPath, 'openai/gpt-4.1');
  const script = `#!/usr/bin/env node
const fs = require('node:fs');
const args = process.argv.slice(2);
fs.appendFileSync(${JSON.stringify(invocationsPath)}, JSON.stringify({args, cwd:process.cwd(), profile:process.env.OMP_PROFILE ?? null}) + '\\n');
const snapshot = currentModel => ({schemaVersion:1,currentModel,providers:[
  {id:'openai',name:'OpenAI',signedIn:true,models:[
    {id:'gpt-4.1',name:'GPT 4.1',selector:'openai/gpt-4.1'},
    {id:'gpt-4.1-mini',name:'GPT 4.1 mini',selector:'openai/gpt-4.1-mini'}
  ]},
  {id:'anthropic',name:'Anthropic',signedIn:false,models:[{id:'claude-sonnet',name:'Claude Sonnet',selector:'anthropic/claude-sonnet'}]}
]});
if (process.env.ASTRID_FAKE_FAIL === '1' && args[1] === 'use') {
  process.stderr.write('credential-secret-should-never-escape');
  process.exit(7);
}
if (args.length === 3 && args[0] === 'agent' && args[1] === 'models' && args[2] === '--json') {
  process.stdout.write(JSON.stringify(snapshot(fs.readFileSync(${JSON.stringify(selectedPath)},'utf8'))));
} else if (args.length === 4 && args[0] === 'agent' && args[1] === 'use' && args[3] === '--json') {
  if (!['openai/gpt-4.1', 'openai/gpt-4.1-mini', 'anthropic/claude-sonnet'].includes(args[2])) {
    process.stderr.write('credential-secret-should-never-escape');
    process.exit(7);
  }
  fs.writeFileSync(${JSON.stringify(selectedPath)}, args[2]);
  process.stdout.write(JSON.stringify(snapshot(args[2])));
} else {
  process.stderr.write('credential-secret-should-never-escape');
  process.exit(7);
}
`;
  writeFileSync(executable, script, { mode: 0o755 });
  chmodSync(executable, 0o755);
  return { command: executable, invocationsPath, selectedPath };
}

async function listen(server: ReturnType<typeof createServer>): Promise<string> {
  await new Promise<void>(resolve => server.listen(0, '127.0.0.1', resolve));
  return `http://127.0.0.1:${(server.address() as { port: number }).port}`;
}

async function fixture(advertisedModels?: string[]) {
  const directory = realpathSync(mkdtempSync(join(tmpdir(), 'astrid-acp-model-http-')));
  const astrid = fakeAstrid(directory);
  const hosts: HostRecord[] = [];
  let nextConnection = 0;
  const registry = {
    assertOwned: async (projectId: string, sessionId: string) => {
      assert.equal(projectId, 'project-1');
      assert.equal(sessionId, 'saved-session');
    },
    markSessionStarted: async (projectId: string, sessionId: string) => {
      assert.equal(projectId, 'project-1');
      assert.equal(sessionId, 'saved-session');
    },
  } satisfies Pick<ProjectChatRegistry, 'assertOwned' | 'markSessionStarted'>;
  const { server, bridge } = createAstridAcpHttpServer({
    config: { token, port: 0, cwd: directory, command: astrid.command, profile: 'test-profile' },
    chatRegistry: registry as unknown as ProjectChatRegistry,
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
  return { directory, astrid, hosts, server, bridge, call };
}

async function closeFixture(value: Awaited<ReturnType<typeof fixture>>): Promise<void> {
  try { await value.bridge.close(); }
  finally {
    value.server.closeAllConnections();
    await new Promise<void>(resolve => value.server.close(() => resolve()));
    rmSync(value.directory, { recursive: true, force: true });
  }
}

test('model HTTP routes require the bridge token and protocol, reject unavailable selectors without fallback, and redact CLI stderr', async () => {
  const value = await fixture();
  try {
    assert.equal((await value.call('/models', undefined, { auth: false })).status, 401);
    assert.equal((await value.call('/models', undefined, { protocol: 'v0' })).status, 400);
    const modelsResponse = await value.call('/models');
    assert.equal(modelsResponse.status, 200);
    const models = await modelsResponse.json() as { providers: Array<{ id: string; signedIn: boolean; models: Array<{ id: string }> }>; currentModel: string };
    assert.equal(models.currentModel, 'openai/gpt-4.1');
    assert.ok(models.providers.some(provider => provider.id === 'openai' && provider.signedIn && provider.models.some(model => model.id === 'gpt-4.1-mini')));
    assert.deepEqual(invocations(value.astrid.invocationsPath), [{
      args: ['agent', 'models', '--json'], cwd: value.directory, profile: 'test-profile',
    }]);

    const unavailable = await value.call('/model', { model: 'openai/not-available' });
    assert.equal(unavailable.status, 500);
    const errorBody = await unavailable.text();
    assert.equal(errorBody.includes('credential-secret'), false);
    assert.equal(readFileSync(value.astrid.selectedPath, 'utf8'), 'openai/gpt-4.1');
    process.env.ASTRID_FAKE_FAIL = '1';
    try {
      const failed = await value.call('/model', { model: 'openai/gpt-4.1-mini' });
      assert.equal(failed.status, 500);
      assert.equal((await failed.text()).includes('credential-secret'), false);
    } finally { delete process.env.ASTRID_FAKE_FAIL; }
    assert.deepEqual(invocations(value.astrid.invocationsPath).map(({ args, cwd, profile }) => ({ args, cwd, profile })), [
      { args: ['agent', 'models', '--json'], cwd: value.directory, profile: 'test-profile' },
      { args: ['agent', 'use', 'openai/not-available', '--json'], cwd: value.directory, profile: 'test-profile' },
      { args: ['agent', 'use', 'openai/gpt-4.1-mini', '--json'], cwd: value.directory, profile: 'test-profile' },
    ]);
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
    assert.equal(readFileSync(value.astrid.selectedPath, 'utf8'), 'openai/gpt-4.1-mini');
    assert.deepEqual(invocations(value.astrid.invocationsPath).map(({ args, cwd, profile }) => ({ args, cwd, profile })), [
      { args: ['agent', 'models', '--json'], cwd: value.directory, profile: 'test-profile' },
      { args: ['agent', 'use', 'openai/gpt-4.1-mini', '--json'], cwd: value.directory, profile: 'test-profile' },
    ]);
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
    assert.equal(readFileSync(value.astrid.selectedPath, 'utf8'), 'openai/gpt-4.1');
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

test('reading the CLI saved default does not change a loaded session model', async () => {
  const value = await fixture(['openai/gpt-4.1-mini']);
  try {
    const modelsResponse = await value.call('/models');
    assert.equal(modelsResponse.status, 200);
    assert.equal((await modelsResponse.json() as { currentModel: string }).currentModel, 'openai/gpt-4.1');
    assert.equal((await value.call('/connect', {})).status, 200);
    assert.equal((await value.call('/c1/rpc', { method: 'session/load', params: { sessionId: 'saved-session' } })).status, 200);
    const prompted = await value.call('/projects/project-1/chat/prompt', {
      connection_id: 'c1', session_id: 'saved-session', prompt: [{ type: 'text', text: 'continue' }],
    });
    assert.equal(prompted.status, 200);
    assert.deepEqual(value.hosts[0]?.calls.map(call => call.method), ['session/load', 'session/prompt']);
  } finally { await closeFixture(value); }
});
