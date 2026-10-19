import { execFile } from 'node:child_process';
import { access, constants } from 'node:fs/promises';
import { delimiter, join } from 'node:path';
import { promisify } from 'node:util';
import type { LocalAgentChoice, LocalAgentId } from '../src/integrations/astrid/localAgents.ts';

type Options = { env?: NodeJS.ProcessEnv; cwd?: string };
const execFileAsync = promisify(execFile);

async function executable(name: string, env: NodeJS.ProcessEnv): Promise<string | null> {
  for (const directory of (env.PATH ?? '').split(delimiter)) {
    if (!directory) continue;
    const candidate = join(directory, name);
    try {
      await access(candidate, constants.X_OK);
      return candidate;
    } catch { /* Keep searching PATH. */ }
  }
  return null;
}

async function status(command: string | null, args: string[], env: NodeJS.ProcessEnv, signedIn: RegExp, signedOut: RegExp, cwd?: string): Promise<LocalAgentChoice['authStatus']> {
  if (!command) return 'unknown';
  try {
    const { stdout, stderr } = await execFileAsync(command, args, { env, cwd, encoding: 'utf8' });
    const output = `${stdout}\n${stderr}`;
    if (signedOut.test(output)) return 'signed-out';
    if (signedIn.test(output)) return 'signed-in';
  } catch (error) {
    // Some CLI versions return non-zero when signed out. Recognize only their
    // explicit signed-out wording; never trust failure text as signed-in.
    const output = typeof error === 'object' && error !== null
      ? [Reflect.get(error, 'stdout'), Reflect.get(error, 'stderr')].filter(value => typeof value === 'string').join('\n')
      : '';
    return signedOut.test(output) ? 'signed-out' : 'unknown';
  }
  return 'unknown';
}

async function claudeStatus(command: string | null, env: NodeJS.ProcessEnv, cwd?: string): Promise<LocalAgentChoice['authStatus']> {
  if (!command) return 'unknown';
  try {
    const { stdout } = await execFileAsync(command, ['auth', 'status'], { env, cwd, encoding: 'utf8' });
    try {
      const result: unknown = JSON.parse(stdout);
      if (typeof result === 'object' && result !== null && typeof Reflect.get(result, 'loggedIn') === 'boolean') {
        return Reflect.get(result, 'loggedIn') ? 'signed-in' : 'signed-out';
      }
      return 'unknown';
    } catch { /* Older Claude versions may emit text; use their explicit text status. */ }
  } catch (error) {
    const stdout = typeof error === 'object' && error !== null ? Reflect.get(error, 'stdout') : undefined;
    if (typeof stdout === 'string') {
      try {
        const result: unknown = JSON.parse(stdout);
        if (typeof result === 'object' && result !== null && typeof Reflect.get(result, 'loggedIn') === 'boolean') {
          return Reflect.get(result, 'loggedIn') ? 'signed-in' : 'signed-out';
        }
        return 'unknown';
      } catch { /* Fall back to text only when the JSON output cannot be parsed. */ }
    }
  }
  return status(command, ['auth', 'status', '--text'], env, /Logged in|Authenticated/i, /Not logged in|Run `?claude auth login/i, cwd);
}

export async function discoverLocalAgents(options: Options = {}): Promise<LocalAgentChoice[]> {
  const env = options.env ?? process.env;
  const [astrid, claude, codex, claudeAdapter, codexAdapter] = await Promise.all([
    executable('astrid', env), executable('claude', env), executable('codex', env),
    executable('claude-agent-acp', env), executable('codex-acp', env),
  ]);
  const [claudeAuth, codexAuth] = await Promise.all([
    claudeStatus(claude, env, options.cwd),
    status(codex, ['login', 'status'], env, /Logged in using/i, /Not logged in|Run `?codex login/i, options.cwd),
  ]);
  return [
    { id: 'astrid', name: 'Astrid', installed: Boolean(astrid), authStatus: 'unknown', adapterInstalled: Boolean(astrid), installCommand: null, loginCommand: null },
    { id: 'claude-code', name: 'Claude Code', installed: Boolean(claude), authStatus: claudeAuth, adapterInstalled: Boolean(claudeAdapter), installCommand: 'npm install -g @agentclientprotocol/claude-agent-acp', loginCommand: 'claude auth login' },
    { id: 'codex', name: 'Codex', installed: Boolean(codex), authStatus: codexAuth, adapterInstalled: Boolean(codexAdapter), installCommand: 'npm install -g @agentclientprotocol/codex-acp', loginCommand: 'codex login' },
  ];
}

export async function localAgentLaunch(agentId: Exclude<LocalAgentId, 'astrid'>, env: NodeJS.ProcessEnv = process.env): Promise<{ command: string; args: string[]; env: Record<string, string | undefined>; cliPath: string }> {
  const adapterName = agentId === 'claude-code' ? 'claude-agent-acp' : 'codex-acp';
  const [adapter, cli] = await Promise.all([
    executable(adapterName, env), executable(agentId === 'claude-code' ? 'claude' : 'codex', env),
  ]);
  if (!cli) throw new Error(`${agentId} CLI is not installed or not executable on PATH.`);
  if (!adapter) {
    const installCommand = agentId === 'claude-code'
      ? 'npm install -g @agentclientprotocol/claude-agent-acp'
      : 'npm install -g @agentclientprotocol/codex-acp';
    throw new Error(`${adapterName} is not installed or executable. Install it explicitly with: ${installCommand}`);
  }
  return {
    command: adapter,
    args: [],
    env: agentId === 'codex' ? { CODEX_PATH: cli } : {},
    cliPath: cli,
  };
}
