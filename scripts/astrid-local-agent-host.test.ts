import { test } from 'node:test';
import assert from 'node:assert/strict';
import { chmodSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createAstridAcpHttpServer } from './astrid-acp-bridge.ts';
import { createLocalAgentAcpProcessHost } from './astrid-local-agent-host.ts';

type Json = Record<string, unknown>;

function executable(path: string, contents: string): void {
  writeFileSync(path, contents);
  chmodSync(path, 0o755);
}

function fixture(directory: string) {
  const bin = join(directory, 'bin');
  const cwd = join(directory, 'project');
  const logs = join(directory, 'adapter.jsonl');
  const profile = join(directory, 'astrid-profile.md');
  mkdirSync(bin);
  mkdirSync(cwd);
  writeFileSync(profile, '# Packaged Astrid profile\nPROFILE_SENTINEL');
  executable(join(bin, 'claude'), `#!${process.execPath}\nprocess.stdout.write('Logged in\\n');\n`);
  executable(join(bin, 'codex'), `#!${process.execPath}\nprocess.stderr.write('Logged in using ChatGPT\\n');\n`);
  for (const name of ['claude-agent-acp', 'codex-acp']) {
    executable(join(bin, name), `#!${process.execPath}
const fs = require('node:fs');
const readline = require('node:readline');
const log = ${JSON.stringify(logs)};
const agent = ${JSON.stringify(name)};
const write = value => process.stdout.write(JSON.stringify(value) + '\\n');
const record = value => fs.appendFileSync(log, JSON.stringify({agent, value}) + '\\n');
const waiting = new Map();
let nextPermission = 0;
record({startup: true, cliPath: process.env.CODEX_PATH ?? null});
const askPermission = params => new Promise(resolve => {
  const id = 'permission-' + (++nextPermission);
  waiting.set(id, resolve);
  write({jsonrpc:'2.0', id, method:'session/request_permission', params});
});
const rl = readline.createInterface({input: process.stdin, crlfDelay: Infinity});
rl.on('line', async line => {
  const message = JSON.parse(line);
  if (message.method === undefined && message.id !== undefined) {
    record({permissionResponse:message});
    waiting.get(message.id)?.(message.result);
    waiting.delete(message.id);
    return;
  }
  if (message.id === undefined) { record({notification:message}); return; }
  if (message.method === 'initialize') {
    record({method:message.method, params:message.params});
    write({jsonrpc:'2.0',id:message.id,result:{protocolVersion:1,agentCapabilities:{loadSession:true,sessionCapabilities:{list:{},resume:{},close:{}}}}});
    return;
  }
  record({method:message.method, params:message.params});
  if (message.method === 'session/new') { write({jsonrpc:'2.0',id:message.id,result:{sessionId:'shared-native-id'}}); return; }
  if (message.method === 'session/list') { write({jsonrpc:'2.0',id:message.id,result:{sessions:[{sessionId:'shared-native-id'}]}}); return; }
  if (message.method === 'session/load' || message.method === 'session/resume') { write({jsonrpc:'2.0',id:message.id,result:{sessionId:message.params.sessionId}}); return; }
  if (message.method === 'session/prompt') {
    record({receivedPrompt:message.params.prompt});
    await askPermission({sessionId:'shared-native-id',toolCall:{title:'Read file'},options:[{optionId:'offered-allow-once',kind:'allow_once'},{optionId:'offered-allow-always',kind:'allow_always'}]});
    await askPermission({sessionId:'shared-native-id',toolCall:{title:'Delete file'},options:[{optionId:'offered-reject-once',kind:'reject_once'},{optionId:'offered-reject-always',kind:'reject_always'}]});
    write({jsonrpc:'2.0',method:'session/update',params:{sessionId:'shared-native-id',update:{sessionUpdate:'agent_message_chunk',content:{type:'text',text:'adapter notification'}}}});
    write({jsonrpc:'2.0',id:message.id,result:{stopReason:'end_turn'}});
    return;
  }
  write({jsonrpc:'2.0',id:message.id,result:{}});
});
rl.on('close', () => process.exit(0));
`);
  }
  return { bin, cwd, logs, profile };
}

async function listen(server: import('node:http').Server): Promise<string> {
  await new Promise<void>(resolve => server.listen(0, '127.0.0.1', resolve));
  return `http://127.0.0.1:${(server.address() as { port: number }).port}`;
}

function records(path: string): Json[] {
  return readFileSync(path, 'utf8').trim().split('\n').filter(Boolean).map(line => JSON.parse(line) as Json);
}

test('external ACP bridge namespaces sessions and routes context, permissions, and cancellation through real adapter processes', async () => {
  const directory = mkdtempSync(join(tmpdir(), 'astrid-local-agent-host-'));
  const f = fixture(directory);
  let nextConnection = 0;
  const { server, bridge } = createAstridAcpHttpServer({
    config: { token: 'test-token', port: 0, cwd: f.cwd },
    idFactory: () => `connection-${++nextConnection}`,
    localAgentHostFactory: (agent, options) => createLocalAgentAcpProcessHost(agent, {
      ...options,
      env: { PATH: f.bin, ...options.env },
      profileFileForCommand: () => f.profile,
    }),
  });
  try {
    const base = await listen(server);
    const call = (path: string, body?: unknown, method = body === undefined ? 'GET' : 'POST') => fetch(base + path, {
      method, headers: { Authorization: 'Bearer test-token', 'X-Astrid-Bridge-Version': 'v1', 'Content-Type': 'application/json' },
      ...(body === undefined ? {} : { body: JSON.stringify(body) }),
    });
    const connected = await Promise.all([
      call('/connect', { agent: 'claude-code' }), call('/connect', { agent: 'codex' }),
    ]);
    assert.deepEqual(connected.map(response => response.status), [200, 200]);
    const claudeId = (await connected[0]!.json() as Json).connection_id as string;
    const codexId = (await connected[1]!.json() as Json).connection_id as string;
    const rpc = async (connection: string, method: string, params: unknown = {}) => call(`/${connection}/rpc`, { method, params });

    const created = await Promise.all([rpc(claudeId, 'session/new'), rpc(codexId, 'session/new')]);
    const sessionIds = await Promise.all(created.map(async response => (await response.json() as Json).result as Json));
    assert.deepEqual(sessionIds.map(result => result.sessionId), ['claude-code:shared-native-id', 'codex:shared-native-id']);
    assert.equal((await rpc(claudeId, 'session/load', { sessionId: 'claude-code:shared-native-id' })).status, 200);
    assert.equal((await rpc(codexId, 'session/load', { sessionId: 'codex:shared-native-id' })).status, 200);
    assert.equal((await rpc(claudeId, 'session/resume', { sessionId: 'claude-code:shared-native-id' })).status, 200);
    assert.equal((await rpc(codexId, 'session/resume', { sessionId: 'codex:shared-native-id' })).status, 200);
    const claudeList = await rpc(claudeId, 'session/list');
    const codexList = await rpc(codexId, 'session/list');
    const claudeSessions = (((await claudeList.json() as Json).result as Json).sessions as Json[]);
    const codexSessions = (((await codexList.json() as Json).result as Json).sessions as Json[]);
    assert.equal(claudeSessions[0]!.sessionId, 'claude-code:shared-native-id');
    assert.equal(codexSessions[0]!.sessionId, 'codex:shared-native-id');

    const crossAgent = await rpc(codexId, 'session/load', { sessionId: 'claude-code:shared-native-id' });
    assert.equal(crossAgent.status, 502);
    assert.match((await crossAgent.json() as Json).detail as string, /different agent/);

    const prompt = await rpc(claudeId, 'session/prompt', {
      sessionId: 'claude-code:shared-native-id',
      prompt: [{ type: 'text', text: '<astrid_editor_context>EDITOR_CONTEXT_SENTINEL</astrid_editor_context>' }],
    });
    assert.equal(prompt.status, 200);
    const events = await call(`/${claudeId}/events`, undefined, 'GET');
    const notifications = (await events.json() as Json).notifications as Json[];
    assert.equal((notifications[0]!.params as Json).sessionId, 'claude-code:shared-native-id');

    const cancel = await call(`/${codexId}/cancel`, { sessionId: 'codex:shared-native-id' });
    assert.equal(cancel.status, 200);
    assert.equal((await call(`/${claudeId}`, {}, 'DELETE')).status, 200);
    assert.equal((await call(`/${codexId}`, {}, 'DELETE')).status, 200);

    const logged = records(f.logs);
    const claudeRecords = logged.filter(row => row.agent === 'claude-agent-acp').map(row => row.value as Json);
    const codexRecords = logged.filter(row => row.agent === 'codex-acp').map(row => row.value as Json);
    const claudeNew = claudeRecords.find(row => row.method === 'session/new')!.params as Json;
    assert.equal((((claudeNew._meta as Json).claudeCode as Json).options as Json).pathToClaudeCodeExecutable, join(f.bin, 'claude'));
    const claudePrompt = claudeRecords.find(row => row.receivedPrompt)!.receivedPrompt as Json[];
    const sentText = claudePrompt.map(part => part.text).join('\n');
    assert.match(sentText, /PROFILE_SENTINEL/);
    assert.match(sentText, /Load the relevant Astrid SKILL\.md/);
    assert.match(sentText, /EDITOR_CONTEXT_SENTINEL/);
    assert.deepEqual(claudeRecords.filter(row => row.permissionResponse).map(row => ((((row.permissionResponse as Json).result as Json).outcome as Json).optionId)), ['offered-allow-always', 'offered-reject-once']);
    assert.equal((codexRecords.find(row => row.startup)!).cliPath, join(f.bin, 'codex'));
    assert.deepEqual(codexRecords.find(row => row.notification)!.notification, { jsonrpc: '2.0', method: 'session/cancel', params: { sessionId: 'shared-native-id' } });
    for (const method of ['session/load', 'session/resume', 'session/list']) {
      assert.ok(claudeRecords.some(row => row.method === method));
      assert.ok(codexRecords.some(row => row.method === method));
    }
  } finally {
    await bridge.close();
    await new Promise<void>(resolve => server.close(() => resolve()));
    rmSync(directory, { recursive: true, force: true });
  }
});

test('external agent readiness fails closed for missing CLIs, sign-in, or adapter without starting an installer', async () => {
  const directory = mkdtempSync(join(tmpdir(), 'astrid-local-agent-readiness-'));
  try {
    const bin = join(directory, 'bin');
    const cwd = join(directory, 'project');
    mkdirSync(bin); mkdirSync(cwd);
    const options = { cwd, env: { PATH: bin }, profileFileForCommand: () => join(directory, 'unused-profile.md') };
    await assert.rejects(createLocalAgentAcpProcessHost('claude-code', options), /not installed on PATH/);
    executable(join(bin, 'claude'), `#!${process.execPath}\nprocess.stdout.write('Not logged in. Run claude auth login to authenticate.');\n`);
    executable(join(bin, 'claude-agent-acp'), `#!${process.execPath}\nprocess.exit(99);\n`);
    await assert.rejects(createLocalAgentAcpProcessHost('claude-code', options), /sign-in is required/);
    executable(join(bin, 'claude'), `#!${process.execPath}\nprocess.stdout.write('Logged in');\n`);
    rmSync(join(bin, 'claude-agent-acp'));
    await assert.rejects(createLocalAgentAcpProcessHost('claude-code', options), /Install the ACP adapter explicitly/);
  } finally { rmSync(directory, { recursive: true, force: true }); }
});
