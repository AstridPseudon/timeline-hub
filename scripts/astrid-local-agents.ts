import { execFile } from 'node:child_process';
import { access, constants } from 'node:fs/promises';
import { delimiter, join } from 'node:path';
import { promisify } from 'node:util';
import { EXTERNAL_AGENT_IDS, LOCAL_AGENT_IDS, LOCAL_AGENT_TABLE, localAgentInstallLine, type LocalAgentChoice, type LocalAgentId } from '../src/integrations/astrid/localAgents.ts';
import { LOCAL_AGENT_ADAPTERS } from './astrid-local-agent-adapters.ts';

type Options = { env?: NodeJS.ProcessEnv; cwd?: string };
type AuthStatus = 'signed-in' | 'signed-out' | 'unknown';
type ExternalAgent = typeof EXTERNAL_AGENT_IDS[number];
const execFileAsync = promisify(execFile);
const LOGIN_PATH_MARKER = '__ASTRID_LOGIN_PATH__';

function combinedPath(...paths: Array<string | undefined>): string {
  return [...new Set(paths.flatMap(path => path?.split(delimiter) ?? []).filter(Boolean))].join(delimiter);
}

/** Resolve the PATH a person sees in their interactive login shell. */
async function loginShellPath(env: NodeJS.ProcessEnv): Promise<string> {
  if (!env.SHELL) return env.PATH ?? '';
  try {
    const { stdout } = await execFileAsync(env.SHELL, ['-lic', `printf '\\n${LOGIN_PATH_MARKER}%s\\n' "$PATH"`], {
      env,
      encoding: 'utf8',
      timeout: 5_000,
      maxBuffer: 1024 * 1024,
    });
    const marker = stdout.lastIndexOf(LOGIN_PATH_MARKER);
    if (marker < 0) return env.PATH ?? '';
    const value = stdout.slice(marker + LOGIN_PATH_MARKER.length).split(/\r?\n/, 1)[0]?.trim();
    return value || env.PATH || '';
  } catch {
    return env.PATH ?? '';
  }
}

async function executable(name: string, pathValue: string): Promise<string | null> {
  for (const directory of pathValue.split(delimiter)) {
    if (!directory) continue;
    const candidate = join(directory, name);
    try {
      await access(candidate, constants.X_OK);
      return candidate;
    } catch { /* Keep searching PATH. */ }
  }
  return null;
}

async function status(command: string | null, args: string[], env: NodeJS.ProcessEnv, signedIn: RegExp, signedOut: RegExp, cwd?: string): Promise<AuthStatus> {
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

async function claudeStatus(command: string | null, env: NodeJS.ProcessEnv, cwd?: string): Promise<AuthStatus> {
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

function choice(id: LocalAgentId, state: LocalAgentChoice['state']): LocalAgentChoice {
  const definition = LOCAL_AGENT_TABLE[id];
  const line = state === 'ready' ? null
    : state === 'sign-in' ? definition.signInLine
      : localAgentInstallLine(id, process.platform === 'win32' ? 'windows' : 'posix') ?? definition.signInLine;
  return { id, name: definition.name, state, line };
}

export async function discoverLocalAgents(options: Options = {}): Promise<LocalAgentChoice[]> {
  const baseEnv = options.env ?? process.env;
  const loginPath = await loginShellPath(baseEnv);
  const path = combinedPath(loginPath, baseEnv.PATH);
  const env = { ...baseEnv, PATH: path };
  const [claude, codex, hermes] = await Promise.all([
    executable('claude', path), executable('codex', path),
    executable('hermes', path),
  ]);
  const [claudeAuth, codexAuth, hermesAuth] = await Promise.all([
    claudeStatus(claude, env, options.cwd),
    status(codex, ['login', 'status'], env, /Logged in using/i, /Not logged in|Run `?codex login/i, options.cwd),
    hermesStatus(hermes, env, options.cwd),
  ]);
  const installed: Record<typeof EXTERNAL_AGENT_IDS[number], string | null> = { 'claude-code': claude, codex, hermes };
  const auth: Record<typeof EXTERNAL_AGENT_IDS[number], AuthStatus> = { 'claude-code': claudeAuth, codex: codexAuth, hermes: hermesAuth };
  return LOCAL_AGENT_IDS.map(id => id === 'astrid'
    ? choice(id, 'ready')
    : choice(id, !installed[id] ? 'not-installed' : auth[id] === 'signed-out' ? 'sign-in' : 'ready'));
}

async function hermesStatus(command: string | null, env: NodeJS.ProcessEnv, cwd?: string): Promise<AuthStatus> {
  if (!command) return 'unknown';
  try {
    await execFileAsync(command, ['acp', '--check'], { env, cwd, encoding: 'utf8', timeout: 3_000, maxBuffer: 1024 * 1024 });
    return 'signed-in';
  } catch (error) {
    if (typeof error === 'object' && error !== null && !Reflect.get(error, 'killed') && typeof Reflect.get(error, 'code') === 'number') return 'signed-out';
    // A slow check or an unfamiliar CLI response is inconclusive; keep the native CLI usable.
    return 'unknown';
  }
}

export async function localAgentLaunch(agentId: ExternalAgent, env: NodeJS.ProcessEnv = process.env): Promise<{ command: string; args: string[]; env: Record<string, string | undefined>; cliPath: string }> {
  const loginPath = await loginShellPath(env);
  const path = combinedPath(loginPath, env.PATH);
  const cli = await executable(agentId === 'claude-code' ? 'claude' : agentId === 'codex' ? 'codex' : 'hermes', path);
  if (!cli) throw new Error(`${LOCAL_AGENT_TABLE[agentId].name} is not installed on PATH.`);
  if (agentId === 'hermes') return { command: cli, args: ['acp'], env: { PATH: path }, cliPath: cli };
  const bun = await executable('bun', path);
  if (!bun) throw new Error('Bun is not installed on PATH.');
  return {
    command: bun,
    args: ['x', '--bun', LOCAL_AGENT_ADAPTERS[agentId]],
    env: { PATH: path, ...(agentId === 'codex' ? { CODEX_PATH: cli } : {}) },
    cliPath: cli,
  };
}
