import { test } from 'node:test';
import assert from 'node:assert/strict';
import { chmodSync, existsSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { discoverLocalAgents, localAgentLaunch } from './astrid-local-agents.ts';

function fake(directory: string, name: string, output: string | { json: string; text: string }, exit = 0, stream: 'stdout' | 'stderr' = 'stdout'): string {
  const path = join(directory, name);
  const expectedArgs = name === 'claude' ? null : name === 'codex' ? 'login status' : null;
  const response = typeof output === 'string'
    ? `printf '%s' ${JSON.stringify(output)}`
    : `[ "$*" = "auth status" ] && printf '%s' ${JSON.stringify(output.json)} || { [ "$*" = "auth status --text" ] && printf '%s' ${JSON.stringify(output.text)} || exit 99; }`;
  writeFileSync(path, `#!/bin/sh\n${expectedArgs ? `[ "$*" = "${expectedArgs}" ] || exit 99\n` : ''}${response}${stream === 'stderr' ? ' >&2' : ''}\nexit ${exit}\n`);
  chmodSync(path, 0o755);
  return path;
}

test('discovers CLIs, adapters, and safe auth status without installing or launching adapters', async () => {
  const directory = mkdtempSync(join(tmpdir(), 'astrid-local-agents-'));
  try {
    fake(directory, 'astrid', '', 0);
    fake(directory, 'claude', { json: '{"loggedIn":false}', text: 'Not logged in. Run claude auth login to authenticate.' });
    fake(directory, 'codex', 'Logged in using ChatGPT');
    const marker = join(directory, 'adapter-started');
    writeFileSync(join(directory, 'codex-acp'), `#!/bin/sh\nprintf started > "${marker}"\n`, { mode: 0o755 });
    const agents = await discoverLocalAgents({ env: { ...process.env, PATH: directory }, cwd: directory });
    assert.deepEqual(agents, [
      { id: 'astrid', name: 'Astrid', installed: true, authStatus: 'unknown', adapterInstalled: true, installCommand: null, loginCommand: null },
      { id: 'claude-code', name: 'Claude Code', installed: true, authStatus: 'signed-out', adapterInstalled: false, installCommand: 'npm install -g @agentclientprotocol/claude-agent-acp', loginCommand: 'claude auth login' },
      { id: 'codex', name: 'Codex', installed: true, authStatus: 'signed-in', adapterInstalled: true, installCommand: 'npm install -g @agentclientprotocol/codex-acp', loginCommand: 'codex login' },
    ]);
    assert.equal(existsSync(marker), false);
  } finally { rmSync(directory, { recursive: true, force: true }); }
});

test('reports unknown auth for missing CLIs and unrecognized status output', async () => {
  const directory = mkdtempSync(join(tmpdir(), 'astrid-local-agents-'));
  try {
    fake(directory, 'claude', { json: 'diagnostic omitted', text: 'diagnostic omitted' });
    fake(directory, 'codex', 'diagnostic omitted', 1);
    const agents = await discoverLocalAgents({ env: { ...process.env, PATH: directory } });
    assert.equal(agents[0]?.installed, false);
    assert.equal(agents[0]?.adapterInstalled, false);
    assert.equal(agents[1]?.authStatus, 'unknown');
    assert.equal(agents[2]?.installed, true);
    assert.equal(agents[2]?.authStatus, 'unknown');
    assert.equal(agents[2]?.adapterInstalled, false);
  } finally { rmSync(directory, { recursive: true, force: true }); }
});

test('reads Claude JSON login status and falls back to text only when JSON is invalid', async () => {
  const directory = mkdtempSync(join(tmpdir(), 'astrid-local-agents-'));
  try {
    fake(directory, 'claude', { json: '{"loggedIn":true}', text: 'Not logged in' });
    let agents = await discoverLocalAgents({ env: { ...process.env, PATH: directory } });
    assert.equal(agents[1]?.authStatus, 'signed-in');

    fake(directory, 'claude', { json: '{invalid json', text: 'Authenticated with Claude Pro account' });
    agents = await discoverLocalAgents({ env: { ...process.env, PATH: directory } });
    assert.equal(agents[1]?.authStatus, 'signed-in');
  } finally { rmSync(directory, { recursive: true, force: true }); }
});

test('reads successful Codex status from stderr and does not trust failed diagnostics', async () => {
  const directory = mkdtempSync(join(tmpdir(), 'astrid-local-agents-'));
  try {
    fake(directory, 'codex', 'Logged in using ChatGPT', 0, 'stderr');
    let agents = await discoverLocalAgents({ env: { ...process.env, PATH: directory } });
    assert.equal(agents[2]?.authStatus, 'signed-in');

    fake(directory, 'codex', 'Not logged in. Run codex login to authenticate.', 1, 'stderr');
    agents = await discoverLocalAgents({ env: { ...process.env, PATH: directory } });
    assert.equal(agents[2]?.authStatus, 'signed-out');

    fake(directory, 'codex', 'Diagnostic: Logged in using ChatGPT', 1, 'stderr');
    agents = await discoverLocalAgents({ env: { ...process.env, PATH: directory } });
    assert.equal(agents[2]?.authStatus, 'unknown');
  } finally { rmSync(directory, { recursive: true, force: true }); }
});

test('launch requires installed adapters and pins each adapter to the discovered CLI', async () => {
  const directory = mkdtempSync(join(tmpdir(), 'astrid-local-launch-'));
  try {
    const codex = fake(directory, 'codex', '');
    const claude = fake(directory, 'claude', '');
    const adapter = fake(directory, 'claude-agent-acp', '');
    const env = { ...process.env, PATH: directory };
    assert.deepEqual(await localAgentLaunch('claude-code', env), { command: adapter, args: [], env: {}, cliPath: claude });
    const codexAdapter = fake(directory, 'codex-acp', '');
    assert.deepEqual(await localAgentLaunch('codex', env), { command: codexAdapter, args: [], env: { CODEX_PATH: codex }, cliPath: codex });
    rmSync(codexAdapter);
    await assert.rejects(localAgentLaunch('codex', env), /Install it explicitly with: npm install -g @agentclientprotocol\/codex-acp/);
  } finally { rmSync(directory, { recursive: true, force: true }); }
});
