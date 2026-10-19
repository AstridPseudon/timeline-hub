import { execFile } from 'node:child_process';
import { chmod, cp, mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { promisify } from 'node:util';

const execute = promisify(execFile);
export const repo = fileURLToPath(new URL('../../', import.meta.url));
export const failure = 'Astrid could not finish; your workspace and any update backup have been kept.';
const mockUv = `#!/usr/bin/env python3
import json, os, pathlib, shutil, subprocess, sys
args = sys.argv[1:]
with open(os.environ['MOCK_CALLS'], 'a') as stream: stream.write(json.dumps(args) + '\\n')
print('native progress on stderr', file=sys.stderr)
if args == ['--version']:
    print(os.environ.get('MOCK_UV_VERSION', 'uv 0.11.32 (x86_64-unknown-linux-gnu)'))
    sys.exit(0)
if args[:2] == ['python', 'install']:
    size = int(os.environ.get('MOCK_VOLUME_BYTES', '0'))
    if size:
        print('o' * size)
        print('e' * size, file=sys.stderr)
    sys.exit(int(os.environ.get('MOCK_PYTHON_EXIT', '0')))
if '-c' in args:
    start = args.index('-c')
    sys.exit(subprocess.call([sys.executable, '-I', '-c', args[start + 1], *args[start + 2:]]))
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
  for (const key of ['MOCK_PYTHON_EXIT', 'MOCK_CORE_EXIT', 'MOCK_REMOVE_BOOTSTRAP', 'MOCK_FETCH_EXIT', 'MOCK_VOLUME_BYTES', 'MOCK_UV_VERSION']) delete env[key];
  await writeFile(path.join(bootstrap, 'uv'), mockUv, { mode: 0o755 });
  await writeFile(path.join(bin, 'curl'), `#!/usr/bin/env python3
import os, pathlib, shutil, sys
if os.environ.get('MOCK_FETCH_EXIT'): sys.exit(int(os.environ['MOCK_FETCH_EXIT']))
pathlib.Path(os.environ['MOCK_FETCHED']).write_text(sys.argv[5])
shutil.copyfile(os.environ['MOCK_MANIFEST'], sys.argv[sys.argv.index('--output') + 1])
`, { mode: 0o755 });
  env.MOCK_FETCHED = path.join(root, 'fetched-url');
  return {
    root, home, bootstrap, manifest, env,
    async run(file, args, overrides = {}) {
      await writeFile(manifestFile, JSON.stringify(manifest));
      try {
        const result = await execute(file, args, { cwd: repo, env: { ...env, ...overrides }, timeout: 30_000 });
        return { ...result, code: 0 };
      } catch (error) {
        if (typeof error.code !== 'number') throw error;
        return { stdout: error.stdout, stderr: error.stderr, code: error.code };
      }
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
    [IO.File]::WriteAllText($env:MOCK_FETCHED, $Uri)
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
`);
      env.MOCK_INSTALL_SCRIPT = path.join(repo, 'public/install.ps1');
      return harness;
    },
    cleanup() { return rm(root, { recursive: true, force: true }); },
  };
}
