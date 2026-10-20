import { test } from 'node:test';
import assert from 'node:assert/strict';
import { chmodSync, existsSync, mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { LOCAL_AGENT_TABLE } from '../src/integrations/astrid/localAgents.ts';
import { LOCAL_AGENT_ADAPTERS } from './astrid-local-agent-adapters.ts';
import { discoverLocalAgents, localAgentLaunch } from './astrid-local-agents.ts';

function executable(directory: string, name: string, contents: string): string {
  const path = join(directory, name);
  writeFileSync(path, contents);
  chmodSync(path, 0o755);
  return path;
}

function fake(directory: string, name: string, output: string | { json: string; text: string }, exit = 0, stream: 'stdout' | 'stderr' = 'stdout'): string {
  const expectedArgs = name === 'claude' ? null : name === 'codex' ? 'login status' : null;
  const response = typeof output === 'string'
    ? `printf '%s' ${JSON.stringify(output)}`
    : `[ "$*" = "auth status" ] && printf '%s' ${JSON.stringify(output.json)} || { [ "$*" = "auth status --text" ] && printf '%s' ${JSON.stringify(output.text)} || exit 99; }`;
  return executable(directory, name, `#!/bin/sh\n${expectedArgs ? `[ "$*" = "${expectedArgs}" ] || exit 99\n` : ''}${response}${stream === 'stderr' ? ' >&2' : ''}\nexit ${exit}\n`);
}

function loginShell(directory: string): string {
  return executable(directory, 'login-shell', `#!/bin/sh\n[ "$1" = "-lic" ] || exit 98\nprintf '\\n__ASTRID_LOGIN_PATH__%s\\n' "$ASTRID_TEST_LOGIN_PATH"\n`);
}

function testEnv(shell: string, ownPath: string, loginPath = ownPath): NodeJS.ProcessEnv {
  return { ...process.env, PATH: ownPath, SHELL: shell, ASTRID_TEST_LOGIN_PATH: loginPath };
}

test('reports Not installed when external CLIs are absent and has no adapter fields', async () => {
  const directory = mkdtempSync(join(tmpdir(), 'astrid-local-agents-'));
  try {
    const shell = loginShell(directory);
    const agents = await discoverLocalAgents({ env: testEnv(shell, directory), cwd: directory });
    assert.deepEqual(agents, [
      { id: 'astrid', name: LOCAL_AGENT_TABLE.astrid.name, state: 'ready', line: null },
      { id: 'claude-code', name: LOCAL_AGENT_TABLE['claude-code'].name, state: 'not-installed', line: LOCAL_AGENT_TABLE['claude-code'].notInstalledLine },
      { id: 'codex', name: LOCAL_AGENT_TABLE.codex.name, state: 'not-installed', line: LOCAL_AGENT_TABLE.codex.notInstalledLine },
      { id: 'hermes', name: LOCAL_AGENT_TABLE.hermes.name, state: 'not-installed', line: LOCAL_AGENT_TABLE.hermes.notInstalledLine },
    ]);
    assert.equal('adapterInstalled' in agents[1]!, false);
    assert.equal('installCommand' in agents[1]!, false);
  } finally { rmSync(directory, { recursive: true, force: true }); }
});

test('signed-in CLIs are Ready with no adapters installed and launch uses each pinned Bun command', async () => {
  const directory = mkdtempSync(join(tmpdir(), 'astrid-local-launch-'));
  try {
    const shell = loginShell(directory);
    const claude = fake(directory, 'claude', { json: '{"loggedIn":true}', text: '' });
    const codex = fake(directory, 'codex', 'Logged in using ChatGPT');
    const bun = executable(directory, 'bun', '#!/bin/sh\nexit 0\n');
    const env = testEnv(shell, directory);
    const agents = await discoverLocalAgents({ env });
    assert.deepEqual(agents.slice(1, 3).map(({ id, state, line }) => ({ id, state, line })), [
      { id: 'claude-code', state: 'ready', line: null },
      { id: 'codex', state: 'ready', line: null },
    ]);
    assert.equal(existsSync(join(directory, 'claude-agent-acp')), false);
    assert.equal(existsSync(join(directory, 'codex-acp')), false);
    assert.deepEqual(await localAgentLaunch('claude-code', env), {
      command: bun, args: ['x', '--bun', LOCAL_AGENT_ADAPTERS['claude-code']], env: { PATH: directory }, cliPath: claude,
    });
    assert.deepEqual(await localAgentLaunch('codex', env), {
      command: bun, args: ['x', '--bun', LOCAL_AGENT_ADAPTERS.codex], env: { PATH: directory, CODEX_PATH: codex }, cliPath: codex,
    });
  } finally { rmSync(directory, { recursive: true, force: true }); }
});

test('finds CLIs and Bun on the login-shell PATH before falling back to the service PATH', async () => {
  const directory = mkdtempSync(join(tmpdir(), 'astrid-login-path-'));
  try {
    const servicePath = join(directory, 'service-bin');
    const loginPath = join(directory, 'login-bin');
    const shellDir = join(directory, 'shell-bin');
    for (const path of [servicePath, loginPath, shellDir]) mkdirSync(path);
    const shell = loginShell(shellDir);
    const claude = fake(loginPath, 'claude', { json: '{"loggedIn":true}', text: '' });
    fake(loginPath, 'codex', 'Logged in using ChatGPT');
    const bun = executable(servicePath, 'bun', '#!/bin/sh\nexit 0\n');
    const env = testEnv(shell, servicePath, loginPath);
    const agents = await discoverLocalAgents({ env });
    assert.equal(agents[1]?.state, 'ready');
    assert.equal(agents[2]?.state, 'ready');
    assert.deepEqual(await localAgentLaunch('claude-code', env), {
      command: bun,
      args: ['x', '--bun', LOCAL_AGENT_ADAPTERS['claude-code']],
      env: { PATH: `${loginPath}:${servicePath}` },
      cliPath: claude,
    });
  } finally { rmSync(directory, { recursive: true, force: true }); }
});

test('reads Claude JSON login status and falls back to text only when JSON is invalid', async () => {
  const directory = mkdtempSync(join(tmpdir(), 'astrid-local-agents-'));
  try {
    const shell = loginShell(directory);
    fake(directory, 'claude', { json: '{"loggedIn":false}', text: 'Not logged in. Run claude auth login to authenticate.' });
    let agents = await discoverLocalAgents({ env: testEnv(shell, directory) });
    assert.equal(agents[1]?.state, 'sign-in');
    assert.equal(agents[1]?.line, LOCAL_AGENT_TABLE['claude-code'].signInLine);

    fake(directory, 'claude', { json: '{invalid json', text: 'Authenticated with Claude Pro account' });
    agents = await discoverLocalAgents({ env: testEnv(shell, directory) });
    assert.equal(agents[1]?.state, 'ready');
  } finally { rmSync(directory, { recursive: true, force: true }); }
});

test('reads successful Codex status from stderr and does not trust failed diagnostics', async () => {
  const directory = mkdtempSync(join(tmpdir(), 'astrid-local-agents-'));
  try {
    const shell = loginShell(directory);
    fake(directory, 'codex', 'Logged in using ChatGPT', 0, 'stderr');
    let agents = await discoverLocalAgents({ env: testEnv(shell, directory) });
    assert.equal(agents[2]?.state, 'ready');

    fake(directory, 'codex', 'Not logged in. Run codex login to authenticate.', 1, 'stderr');
    agents = await discoverLocalAgents({ env: testEnv(shell, directory) });
    assert.equal(agents[2]?.state, 'sign-in');

    fake(directory, 'codex', 'Diagnostic: Logged in using ChatGPT', 1, 'stderr');
    agents = await discoverLocalAgents({ env: testEnv(shell, directory) });
    assert.equal(agents[2]?.state, 'ready');
  } finally { rmSync(directory, { recursive: true, force: true }); }
});

test('discovers Hermes with hermes acp --check and launches its native ACP command', async () => {
  const directory = mkdtempSync(join(tmpdir(), 'astrid-hermes-'));
  try {
    const shell = loginShell(directory);
    const hermes = executable(directory, 'hermes', '#!/bin/sh\n[ "$*" = "acp --check" ] || exit 91\nexit "${HERMES_CHECK_EXIT:-0}"\n');
    const env = testEnv(shell, directory);
    assert.equal((await discoverLocalAgents({ env }))[3]?.state, 'ready');
    assert.deepEqual(await localAgentLaunch('hermes', env), { command: hermes, args: ['acp'], env: { PATH: directory }, cliPath: hermes });
    assert.equal((await discoverLocalAgents({ env: { ...env, HERMES_CHECK_EXIT: '7' } }))[3]?.state, 'sign-in');
  } finally { rmSync(directory, { recursive: true, force: true }); }
});

test('keeps Hermes ready when ACP check is inconclusive or times out', async () => {
  const directory = mkdtempSync(join(tmpdir(), 'astrid-hermes-check-'));
  try {
    const shell = loginShell(directory);
    executable(directory, 'hermes', '#!/bin/sh\n[ "$*" = "acp --check" ] || exit 91\ncase "$HERMES_CHECK_MODE" in unknown) kill -TERM $$ ;; timeout) /bin/sleep 10 ;; esac\n');
    for (const mode of ['unknown', 'timeout']) {
      const agents = await discoverLocalAgents({ env: { ...testEnv(shell, directory), HERMES_CHECK_MODE: mode } });
      assert.equal(agents[3]?.state, 'ready', `${mode} check should remain usable`);
    }
  } finally { rmSync(directory, { recursive: true, force: true }); }
});
