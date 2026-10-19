import { execFile } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { access, constants } from 'node:fs/promises';
import { userInfo } from 'node:os';
import { delimiter, join, win32 as win32Path } from 'node:path';
import { promisify } from 'node:util';
import { LOCAL_AGENT_TABLE, type LocalAgentChoice, type LocalAgentId } from './localAgents.ts';
import { LOCAL_AGENT_ADAPTERS } from './astrid-local-agent-adapters.ts';

type RegistryReader = (key: string, env: NodeJS.ProcessEnv) => Promise<string>;
type Options = { env?: NodeJS.ProcessEnv; cwd?: string; platform?: NodeJS.Platform; registryReader?: RegistryReader; passwdReader?: () => string };
type AuthStatus = 'signed-in' | 'signed-out' | 'unknown';
type ExternalAgent = Exclude<LocalAgentId, 'astrid'>;
const execFileAsync = promisify(execFile);
const LOGIN_PATH_MARKER = '__ASTRID_LOGIN_PATH__';

function pathDelimiter(platform: NodeJS.Platform): string {
  return platform === 'win32' ? ';' : delimiter;
}

function combinedPath(platform: NodeJS.Platform, ...paths: Array<string | undefined>): string {
  const separator = pathDelimiter(platform);
  return [...new Set(paths.flatMap(path => path?.split(separator) ?? []).filter(Boolean))].join(separator);
}

export function defaultShellFromPasswd(passwd = readFileSync('/etc/passwd', 'utf8'), username = userInfo().username, uid = typeof process.getuid === 'function' ? String(process.getuid()) : ''): string | null {
  for (const line of passwd.split(/\r?\n/)) {
    const fields = line.split(':');
    if (fields.length >= 7 && (fields[0] === username || (uid && fields[2] === uid))) {
      return fields[6] || null;
    }
  }
  return null;
}

function parseRegistryEnvironment(output: string): Record<string, string> {
  const values: Record<string, string> = {};
  for (const line of output.split(/\r?\n/)) {
    const match = line.match(/^\s*(.*?)\s{2,}REG_(?:EXPAND_)?(?:SZ|DWORD|BINARY|MULTI_SZ)\s{2,}(.*)$/i);
    if (match?.[1]) values[match[1]] = match[2] ?? '';
  }
  return values;
}

async function readRegistryKey(key: string, env: NodeJS.ProcessEnv): Promise<string> {
  const windowsDirectory = env.SystemRoot ?? env.WINDIR ?? 'C:\\Windows';
  const regExe = win32Path.join(windowsDirectory, 'System32', 'reg.exe');
  const { stdout } = await execFileAsync(regExe, ['query', key], {
    env, encoding: 'utf8', timeout: 5_000, maxBuffer: 1024 * 1024,
  });
  return stdout;
}

function expandWindowsEnvironment(value: string, ...sources: Array<Record<string, string | undefined>>): string {
  const variables = new Map<string, string>();
  for (const source of sources) {
    for (const [key, entry] of Object.entries(source)) if (entry !== undefined) variables.set(key.toLowerCase(), entry);
  }
  let expanded = value;
  for (let pass = 0; pass < 10; pass++) {
    const next = expanded.replace(/%([^%]+)%/g, (match, key: string) => variables.get(key.toLowerCase()) ?? match);
    if (next === expanded) break;
    expanded = next;
  }
  return expanded;
}

/** Resolve PATH from the user's and machine's Windows environment registry keys. */
export async function windowsLoginPath(env: NodeJS.ProcessEnv, registryReader: RegistryReader = readRegistryKey): Promise<string> {
  const [userOutput, systemOutput] = await Promise.all([
    registryReader('HKCU\\Environment', env).catch(() => ''),
    registryReader('HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment', env).catch(() => ''),
  ]);
  const user = parseRegistryEnvironment(userOutput);
  const system = parseRegistryEnvironment(systemOutput);
  const pathValue = (values: Record<string, string>, source: Record<string, string>) => {
    const key = Object.keys(values).find(name => name.toLowerCase() === 'path');
    return key ? expandWindowsEnvironment(values[key] ?? '', env, source, system, user) : '';
  };
  return [pathValue(user, user), pathValue(system, system)].filter(Boolean).join(';');
}

/** Resolve the PATH a person sees in their interactive login shell. */
async function loginShellPath(env: NodeJS.ProcessEnv, platform: NodeJS.Platform, registryReader?: RegistryReader, passwdReader?: () => string): Promise<string> {
  if (platform === 'win32') return windowsLoginPath(env, registryReader);
  let shell = env.SHELL;
  if (!shell) {
    try { shell = defaultShellFromPasswd(passwdReader?.()) ?? undefined; } catch { /* passwd may not be readable in a service context. */ }
  }
  if (!shell) return env.PATH ?? '';
  try {
    const { stdout } = await execFileAsync(shell, ['-lic', `printf '\\n${LOGIN_PATH_MARKER}%s\\n' "$PATH"`], {
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

export function executableNames(name: string, platform = process.platform, pathExt = process.env.PATHEXT): string[] {
  if (platform !== 'win32') return [name];
  const extensions = (pathExt || '.com;.exe;.bat;.cmd').split(';').filter(Boolean);
  const names = [...extensions.map(extension => `${name}${extension.startsWith('.') ? extension : `.${extension}`}`), name];
  const seen = new Set<string>();
  return names.filter(filename => {
    const normalized = filename.toLowerCase();
    if (seen.has(normalized)) return false;
    seen.add(normalized);
    return true;
  });
}

async function executable(name: string, pathValue: string, platform: NodeJS.Platform, pathExt?: string): Promise<string | null> {
  for (const directory of pathValue.split(pathDelimiter(platform))) {
    if (!directory) continue;
    for (const filename of executableNames(name, platform, pathExt)) {
      const candidate = join(directory, filename);
      try {
        await access(candidate, platform === 'win32' ? constants.F_OK : constants.X_OK);
        return candidate;
      } catch { /* Keep searching PATH. */ }
    }
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

function choice(id: LocalAgentId, state: LocalAgentChoice['state'], platform: NodeJS.Platform): LocalAgentChoice {
  const definition = LOCAL_AGENT_TABLE[id];
  const line = state === 'ready' ? null
    : state === 'sign-in' ? definition.signInLine
      : platform === 'win32' ? definition.windowsNotInstalledLine ?? definition.notInstalledLine ?? definition.signInLine
        : definition.notInstalledLine ?? definition.signInLine;
  return { id, name: definition.name, state, line };
}

export async function discoverLocalAgents(options: Options = {}): Promise<LocalAgentChoice[]> {
  const baseEnv = options.env ?? process.env;
  const platform = options.platform ?? process.platform;
  const loginPath = await loginShellPath(baseEnv, platform, options.registryReader, options.passwdReader);
  const path = combinedPath(platform, loginPath, baseEnv.PATH);
  const env = { ...baseEnv, PATH: path };
  const [claude, codex] = await Promise.all([
    executable('claude', path, platform, baseEnv.PATHEXT), executable('codex', path, platform, baseEnv.PATHEXT),
  ]);
  const [claudeAuth, codexAuth] = await Promise.all([
    claudeStatus(claude, env, options.cwd),
    status(codex, ['login', 'status'], env, /Logged in using/i, /Not logged in|Run `?codex login/i, options.cwd),
  ]);
  return [
    choice('astrid', 'ready', platform),
    choice('claude-code', !claude ? 'not-installed' : claudeAuth === 'signed-out' ? 'sign-in' : 'ready', platform),
    choice('codex', !codex ? 'not-installed' : codexAuth === 'signed-out' ? 'sign-in' : 'ready', platform),
  ];
}

export async function localAgentLaunch(agentId: ExternalAgent, env: NodeJS.ProcessEnv = process.env): Promise<{ command: string; args: string[]; env: Record<string, string | undefined>; cliPath: string }> {
  const platform = process.platform;
  const loginPath = await loginShellPath(env, platform);
  const path = combinedPath(platform, loginPath, env.PATH);
  const bunPath = combinedPath(platform, env.PATH, loginPath);
  const [bun, cli] = await Promise.all([
    executable('bun', bunPath, platform, env.PATHEXT),
    executable(agentId === 'claude-code' ? 'claude' : 'codex', path, platform, env.PATHEXT),
  ]);
  if (!cli) throw new Error(`${LOCAL_AGENT_TABLE[agentId].name} is not installed on PATH.`);
  if (!bun) throw new Error('Bun is not installed on PATH.');
  return {
    command: bun,
    args: ['x', '--bun', LOCAL_AGENT_ADAPTERS[agentId]],
    env: { PATH: path, ...(agentId === 'codex' ? { CODEX_PATH: cli } : {}) },
    cliPath: cli,
  };
}
