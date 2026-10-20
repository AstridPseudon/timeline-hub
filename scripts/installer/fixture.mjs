import { execFile, spawn } from 'node:child_process';
import { chmod, cp, mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { promisify } from 'node:util';

const execute = promisify(execFile);
export const repo = fileURLToPath(new URL('../../', import.meta.url));
export const failure = 'Astrid could not finish; your workspace and any update backup have been kept.';
const mockUv = `#!/usr/bin/env python3
import json, os, pathlib, shutil, subprocess, sys, time
args = sys.argv[1:]
with open(os.environ['MOCK_CALLS'], 'a') as stream: stream.write(json.dumps(args) + '\\n')
print('native progress on stderr', file=sys.stderr)
if os.environ.get('MOCK_UNICODE_OUTPUT') and args[:1] == ['run']:
    sys.stdout.buffer.write('Workspace: 测试/Zoë\\n'.encode('utf-8'))
    sys.stdout.buffer.flush()
    sys.stderr.buffer.write('Diagnostic: 测试/Zoë\\n'.encode('utf-8'))
    sys.stderr.buffer.flush()
if args == ['--version']:
    print(os.environ.get('MOCK_UV_VERSION', 'uv 0.11.32 (x86_64-unknown-linux-gnu)'))
    sys.exit(0)
if args[:2] == ['python', 'install']:
    size = int(os.environ.get('MOCK_VOLUME_BYTES', '0'))
    if size:
        print('o' * size)
        print('e' * size, file=sys.stderr)
    sys.exit(int(os.environ.get('MOCK_PYTHON_EXIT', '0')))
if args[:1] == ['venv'] or args[:2] == ['pip', 'install']:
    if args[:2] == ['pip', 'install'] and '--require-hashes' in args and os.environ.get('MOCK_EXPECTED_LOCK_CONTENT') is not None:
        lock = pathlib.Path(args[args.index('-r') + 1]).read_text()
        if lock != os.environ['MOCK_EXPECTED_LOCK_CONTENT']:
            print('bootstrap did not use the lock from the pinned agent commit', file=sys.stderr)
            sys.exit(41)
    sys.exit(0)
if '-c' in args:
    start = args.index('-c')
    os.execv(sys.executable, [sys.executable, '-u', '-I', '-c', args[start + 1], *args[start + 2:]])
if os.environ.get('MOCK_REQUIRE_TTY'):
    assert sys.stdin.isatty(), 'uv must see terminal stdin to avoid duplicate SIGINT'
if os.environ.get('MOCK_CORE_APPEND_LOG'):
    with open(os.environ['MOCK_LOG'], 'a') as stream:
        if os.name == 'posix':
            import fcntl
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        stream.write('core opened its own log\\n')
        stream.flush()
        print('Core is writing its log.', flush=True)
        stream.write('core kept its own diagnostic\\n')
if os.environ.get('MOCK_STAGE_RELEASE'):
    # Emulate Python's stdout buffering according to the forwarded -u flag.
    sys.stdout.reconfigure(line_buffering='-u' in args)
    try:
        print('Installing the pinned Astrid version.')
        while not pathlib.Path(os.environ['MOCK_STAGE_RELEASE']).exists(): time.sleep(0.01)
    except KeyboardInterrupt:
        pathlib.Path(os.environ['MOCK_INTERRUPTED']).write_text('KeyboardInterrupt reached installer')
        time.sleep(0.4)  # Cooperative rollback must finish before readers close.
        print(${JSON.stringify(failure)})
        print('Details: ' + os.environ['MOCK_LOG'])
        sys.exit(19)
if os.environ.get('MOCK_CORE_RAW_EXIT'):
    print('raw core diagnostic', file=sys.stderr)
    sys.exit(int(os.environ['MOCK_CORE_RAW_EXIT']))
if os.environ.get('MOCK_CORE_DISK_FAILURE'):
    print('There is not enough free disk space to back up your workspace.')
    print('Details: ' + os.environ['MOCK_LOG'])
    sys.exit(1)
if os.environ.get('MOCK_REMOVE_BOOTSTRAP'):
    shutil.rmtree(pathlib.Path(sys.argv[0]).parent)
if os.environ.get('MOCK_CORE_EXIT'):
    print(${JSON.stringify(failure)})
    print('Details: ' + os.environ['MOCK_LOG'])
    sys.exit(int(os.environ['MOCK_CORE_EXIT']))
print('Astrid was uninstalled.' if '--uninstall' in args else 'Astrid is ready.')
`;

export async function fixture() {
  const root = await mkdtemp(path.join(os.tmpdir(), 'astrid-bootstrap-test-'));
  const home = path.join(root, 'home');
  const data = path.join(root, 'data');
  const bootstrap = path.join(data, 'astrid/bootstrap');
  const bin = path.join(root, 'bin');
  await Promise.all([mkdir(home), mkdir(bin), mkdir(bootstrap, { recursive: true })]);
  const manifest = JSON.parse(await readFile(path.join(repo, 'public/install-manifest.json'), 'utf8'));
  const manifestFile = path.join(root, 'source-manifest.json');
  const env = {
    ...process.env,
    HOME: home,
    PATH: `${bin}${path.delimiter}${process.env.PATH}`,
    XDG_DATA_HOME: data,
    XDG_STATE_HOME: path.join(root, 'state'),
    XDG_CACHE_HOME: path.join(root, 'cache'),
    XDG_CONFIG_HOME: path.join(root, 'config'),
    ASTRID_INSTALL_MANIFEST_URL: 'http://127.0.0.1:17427/developer-manifest.json',
    MOCK_MANIFEST: manifestFile,
    MOCK_CALLS: path.join(root, 'calls.jsonl'),
    MOCK_LOG: path.join(root, 'state/astrid-runtime/logs/install.log'),
  };
  for (const key of ['MOCK_PYTHON_EXIT', 'MOCK_CORE_EXIT', 'MOCK_REMOVE_BOOTSTRAP', 'MOCK_FETCH_EXIT', 'MOCK_VOLUME_BYTES', 'MOCK_UV_VERSION', 'MOCK_STAGE_RELEASE', 'MOCK_INTERRUPTED', 'MOCK_CORE_RAW_EXIT', 'MOCK_CORE_APPEND_LOG', 'MOCK_REQUIRE_TTY', 'MOCK_EXPECTED_LOCK_CONTENT', 'MOCK_CORE_DISK_FAILURE', 'MOCK_UNICODE_OUTPUT', 'MOCK_ACL_FAILURE']) delete env[key];
  await writeFile(path.join(bootstrap, 'uv'), mockUv, { mode: 0o755 });
  await writeFile(path.join(bin, 'curl'), `#!/usr/bin/env python3
import os, pathlib, shutil, sys
if os.environ.get('MOCK_FETCH_EXIT'): sys.exit(int(os.environ['MOCK_FETCH_EXIT']))
if sys.argv[5].endswith('/developer-manifest.json') or sys.argv[5].endswith('/install-manifest.json'):
    pathlib.Path(os.environ['MOCK_FETCHED']).write_text(sys.argv[5])
shutil.copyfile(os.environ['MOCK_MANIFEST'], sys.argv[sys.argv.index('--output') + 1])
`, { mode: 0o755 });
  env.MOCK_FETCHED = path.join(root, 'fetched-url');
  return {
    root, home, bootstrap, manifest, env,
    async run(file, args, overrides = {}, timeout = 30_000) {
      await writeFile(manifestFile, JSON.stringify(manifest));
      try {
        const result = await execute(file, args, { cwd: repo, env: { ...env, ...overrides }, timeout });
        return { ...result, code: 0 };
      } catch (error) {
        if (typeof error.code !== 'number') throw error;
        return { stdout: error.stdout, stderr: error.stderr, code: error.code };
      }
    },
    async start(file, args, overrides = {}) {
      await writeFile(manifestFile, JSON.stringify(manifest));
      return spawn(file, args, { cwd: repo, env: { ...env, ...overrides }, timeout: 30_000 });
    },
    async calls() {
      try { return (await readFile(env.MOCK_CALLS, 'utf8')).trim().split('\n').map((line) => JSON.parse(line)); }
      catch (error) { if (error.code === 'ENOENT') return []; throw error; }
    },
    async powershell() {
      env.LOCALAPPDATA = path.join(root, 'Windows Local Data');
      env.MOCK_LOG = path.join(env.LOCALAPPDATA, 'Astrid Runtime/logs/install.log');
      const windowsBootstrap = path.join(env.LOCALAPPDATA, 'Astrid/bootstrap');
      await mkdir(windowsBootstrap, { recursive: true });
      await cp(path.join(bootstrap, 'uv'), path.join(windowsBootstrap, 'uv.exe'));
      await chmod(path.join(windowsBootstrap, 'uv.exe'), 0o755);
      const harness = path.join(root, 'invoke.ps1');
      await writeFile(harness, `
$ErrorActionPreference = 'Continue'
function Invoke-WebRequest {
    param([switch]$UseBasicParsing, [Parameter(Position=0)][string]$Uri, [string]$OutFile)
    if ($env:MOCK_FETCH_EXIT) { throw 'The fixture download failed.' }
    if ($Uri.EndsWith('/developer-manifest.json') -or $Uri.EndsWith('/install-manifest.json')) { [IO.File]::WriteAllText($env:MOCK_FETCHED, $Uri) }
    Copy-Item $env:MOCK_MANIFEST $OutFile
}
try {
    if ($args.Count) {
        & ([scriptblock]::Create([IO.File]::ReadAllText($env:MOCK_INSTALL_SCRIPT))) @args
    } else {
        Invoke-Expression ([IO.File]::ReadAllText($env:MOCK_INSTALL_SCRIPT))
    }
} catch {
    [Console]::WriteLine('CAUGHT: ' + $_.Exception.Message)
}
[Console]::WriteLine('SHELL-ALIVE')
[Console]::WriteLine('PREFERENCE: ' + $ErrorActionPreference)
[Console]::WriteLine('NATIVE-STATUS: ' + $global:LASTEXITCODE)
`);
      env.MOCK_INSTALL_SCRIPT = path.join(repo, 'public/install.ps1');
      return harness;
    },
    cleanup() { return rm(root, { recursive: true, force: true }); },
  };
}

export function observe(child) {
  let stdout = '';
  let stderr = '';
  const waiting = [];
  child.stdout.on('data', (chunk) => {
    stdout += chunk;
    for (const item of waiting) if (stdout.includes(item.marker)) item.resolve();
  });
  child.stderr.on('data', (chunk) => { stderr += chunk; });
  const result = new Promise((resolve, reject) => {
    child.once('error', reject);
    child.once('close', (code, signal) => {
      for (const item of waiting) if (!stdout.includes(item.marker)) item.reject(new Error(`Exited before ${item.marker}: ${stderr}`));
      resolve({ stdout, stderr, code, signal });
    });
  });
  return {
    result,
    until(marker) {
      if (stdout.includes(marker)) return Promise.resolve();
      return new Promise((resolve, reject) => waiting.push({ marker, resolve, reject }));
    },
  };
}

export async function createPinnedRepo(repoPath, lockContent) {
  await mkdir(path.join(repoPath, 'requirements'), { recursive: true });
  await writeFile(path.join(repoPath, 'requirements/runtime.lock'), lockContent);
  await execute('git', ['init', '--quiet'], { cwd: repoPath });
  await execute('git', ['config', 'user.name', 'Astrid bootstrap test'], { cwd: repoPath });
  await execute('git', ['config', 'user.email', 'bootstrap-test@example.invalid'], { cwd: repoPath });
  await execute('git', ['add', 'requirements/runtime.lock'], { cwd: repoPath });
  await execute('git', ['commit', '--quiet', '-m', 'pin runtime lock'], { cwd: repoPath });
  return (await execute('git', ['rev-parse', 'HEAD'], { cwd: repoPath })).stdout.trim();
}

// pty.fork supplies a real controlling terminal. Writing ^C exercises the
// terminal's foreground process-group delivery instead of killing one PID.
export const terminalInterrupt = `
import errno, json, os, pty, select, signal, sys, time
pid, terminal = pty.fork()
if pid == 0:
    os.execvp(sys.argv[1], sys.argv[1:])
output = bytearray()
interrupted = False
startup_deadline = time.monotonic() + 90
recovery_deadline = None
try:
    while True:
        now = time.monotonic()
        deadline = recovery_deadline if interrupted else startup_deadline
        if now >= deadline:
            if interrupted:
                raise TimeoutError('installer did not recover within 20 seconds after terminal Ctrl+C: ' + output.decode(errors='replace'))
            raise TimeoutError('installer did not reach its streamed stage within 90 seconds: ' + output.decode(errors='replace'))
        readable, _, _ = select.select([terminal], [], [], min(0.05, deadline - now))
        if readable:
            try: chunk = os.read(terminal, 65536)
            except OSError as error:
                if error.errno != errno.EIO: raise
                break
            if not chunk: break
            output.extend(chunk)
            if not interrupted and b'Installing the pinned Astrid version.' in output:
                os.write(terminal, b'\\x03')
                interrupted = True
                recovery_deadline = time.monotonic() + 20
        finished, status = os.waitpid(pid, os.WNOHANG)
        if finished:
            pid = None
            break
    if pid is not None:
        _, status = os.waitpid(pid, 0)
        pid = None
    print(json.dumps(dict(output=output.decode(errors='replace'), code=os.waitstatus_to_exitcode(status), interrupted=interrupted)))
finally:
    if pid is not None:
        os.killpg(pid, signal.SIGKILL)
        os.waitpid(pid, 0)
    os.close(terminal)
`;
