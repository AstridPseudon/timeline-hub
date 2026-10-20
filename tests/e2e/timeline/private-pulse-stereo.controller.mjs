import {createHash, randomBytes} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {
  chmodSync,
  chownSync,
  existsSync,
  lstatSync,
  mkdtempSync,
  readFileSync,
  realpathSync,
  rmSync,
  statSync,
  statfsSync,
  writeFileSync,
} from 'node:fs';
import {dirname, join, resolve} from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {
  BROWSER_EXECUTABLE,
  BROWSER_VERSION,
  FROZEN_PRIVATE_GRAPH,
  MIN_FREE_BYTES,
  NODE_EXECUTABLE,
  NODE_EXECUTABLE_SHA256,
  REPO_ROOT,
  RUN_MODE,
  assertPhysicalGraph,
  assertResources,
  hashTree,
  sourceFingerprint,
} from './tab-audio-capture.controller.mjs';

// This controller is intentionally offline. It validates the selected App
// source and toolchain, but never starts PulseAudio, Chrome, ffmpeg, a socket,
// or a grant-backed run. The central launcher owns the later capture path.
export const APP_ROOT = resolve(process.env.TAB_AUDIO_APP_ROOT ?? REPO_ROOT);
export const BASE_CONTROLLER = join(APP_ROOT, 'tests/e2e/timeline/tab-audio-capture.controller.mjs');
export const APP_SOURCE = join(APP_ROOT, 'tests/e2e/timeline/private-pulse-stereo.probe.ts');
export const RUN_MODE_VALUE = RUN_MODE;
export const REVIEWED_SOURCE_SHA = 'cd966437a7a4811d8fdea248aced9b109fbcb967';
export const DAEMON_USER = 'nobody';
export const DAEMON_UID = 65534;
export const DAEMON_GID = 65534;
export const TOOL_NAMES = Object.freeze(['pulseaudio', 'pactl', 'ffmpeg', 'ffprobe']);

const CONTROLLER_PATH = fileURLToPath(import.meta.url);
const SOURCE_CONTROLLER = join(APP_ROOT, 'tests/e2e/timeline/private-pulse-stereo.controller.mjs');

function sha256(bytes) {
  return createHash('sha256').update(bytes).digest('hex');
}

function command(name, args) {
  return execFileSync(name, args, {encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe']}).trim();
}

function git(...args) {
  return command('git', ['-C', APP_ROOT, ...args]);
}

function toolVersions() {
  return Object.fromEntries(TOOL_NAMES.map((name) => [name, {
    path: command('which', [name]),
    version: command(name, name === 'pulseaudio' || name === 'pactl' ? ['--version'] : ['-version']).split('\n')[0],
  }]));
}

export function installedTools() {
  return toolVersions();
}

function reviewedSource() {
  const sourceSha = git('rev-parse', 'HEAD');
  try {
    execFileSync('git', ['-C', APP_ROOT, 'merge-base', '--is-ancestor', REVIEWED_SOURCE_SHA, sourceSha], {stdio: 'ignore'});
  } catch {
    throw new Error(`Selected source must descend from independently reviewed daemon-only UID source ${REVIEWED_SOURCE_SHA}`);
  }
  return sourceSha;
}

function assertSourceRoot() {
  if (realpathSync(APP_ROOT) !== REPO_ROOT || APP_ROOT !== REPO_ROOT) {
    throw new Error(`Source authority must be this exact App worktree: ${REPO_ROOT}`);
  }
  if (realpathSync(dirname(CONTROLLER_PATH)) !== realpathSync(dirname(SOURCE_CONTROLLER))) {
    throw new Error('Controller path does not belong to the selected source worktree');
  }
  if (!existsSync(BASE_CONTROLLER) || !existsSync(APP_SOURCE)) {
    throw new Error('Exact source worktree is missing the reviewed controller or probe');
  }
  if (git('status', '--porcelain', '--untracked-files=all')) {
    throw new Error('Selected App source must be a clean committed worktree');
  }
}

function assertOfflineEnvironment() {
  if (process.env.TAB_AUDIO_RUN === '1') throw new Error('Pure final preflight cannot run the capture');
  if (process.env.TAB_AUDIO_GRANT_PATH) throw new Error('Pure final preflight must not read a grant');
  const source = readFileSync(APP_SOURCE, 'utf8');
  for (const required of ['finally', 'module-null-sink', 'PULSE_SERVER', 'PULSE_SINK', 'pcm_f32le', 'player.monitor']) {
    if (!source.includes(required)) throw new Error(`Reviewed fallback source lost required lifecycle/control: ${required}`);
  }
  for (const forbidden of ['--system', 'set-default-sink', 'PULSE_DEFAULT', "'-ac'", 'aresample', 'pan=']) {
    if (source.includes(forbidden)) throw new Error(`Reviewed fallback source contains forbidden global operation: ${forbidden}`);
  }
}

function assertSelectedGraph() {
  const selected = realpathSync(join(APP_ROOT, 'node_modules'));
  if (selected !== FROZEN_PRIVATE_GRAPH.root) {
    throw new Error(`Selected source must resolve to the approved private graph, not ${selected}`);
  }
  assertPhysicalGraph(selected);
  const tree = hashTree(selected);
  if (JSON.stringify(tree) !== JSON.stringify(FROZEN_PRIVATE_GRAPH.tree)) {
    throw new Error('Whole private dependency graph does not match the approved READY graph');
  }
  return {root: selected, sha256: tree.sha256, fileCount: tree.fileCount};
}

function privateDirectoryLifecycle() {
  if (process.getuid?.() !== 0) throw new Error('Private Pulse lifecycle preflight requires the original root launcher UID');
  const parent = '/tmp';
  const parentBefore = lstatSync(parent);
  const privatePaths = [];
  const allocatePrivatePath = (prefix) => {
    const path = mkdtempSync(prefix);
    privatePaths.push(path);
    return path;
  };
  let paths;
  try {
    paths = {
      runtime: allocatePrivatePath('/tmp/timeline-private-pulse-uid-runtime-'),
      home: allocatePrivatePath('/tmp/timeline-private-pulse-uid-home-'),
      cookieDir: allocatePrivatePath('/tmp/timeline-private-pulse-uid-cookie-'),
    };
    const cookie = join(paths.cookieDir, 'cookie');
    for (const path of privatePaths) {
      chmodSync(path, 0o700);
      const fresh = lstatSync(path);
      if (!fresh.isDirectory() || fresh.uid !== 0 || fresh.gid !== 0 || (fresh.mode & 0o077) !== 0
        || realpathSync(path) !== path || dirname(path) !== parent) {
        throw new Error(`Private Pulse scope is not a fresh root-owned 0700 directory: ${path}`);
      }
      chownSync(path, DAEMON_UID, DAEMON_GID);
    }
    writeFileSync(cookie, randomBytes(32), {flag: 'wx', mode: 0o600});
    chmodSync(cookie, 0o600);
    chownSync(cookie, DAEMON_UID, DAEMON_GID);
    for (const path of privatePaths) {
      const stat = lstatSync(path);
      if (!stat.isDirectory() || stat.uid !== DAEMON_UID || stat.gid !== DAEMON_GID || (stat.mode & 0o077) !== 0) {
        throw new Error(`Private Pulse directory is not nobody-owned and 0700: ${path}`);
      }
      if (realpathSync(path) !== path) throw new Error(`Private Pulse directory is not a real scope: ${path}`);
      command('runuser', ['-u', DAEMON_USER, '--', 'test', '-r', path]);
    }
    const cookieStat = lstatSync(cookie);
    if (!cookieStat.isFile() || cookieStat.uid !== DAEMON_UID || cookieStat.gid !== DAEMON_GID || (cookieStat.mode & 0o077) !== 0) {
      throw new Error('Private Pulse cookie is not nobody-owned and private');
    }
    command('runuser', ['-u', DAEMON_USER, '--', 'test', '-r', cookie]);
    const parentAfterChown = lstatSync(parent);
    if (parentAfterChown.uid !== 0 || parentAfterChown.gid !== 0 || parentAfterChown.mode !== parentBefore.mode) {
      throw new Error('The /tmp parent changed ownership or mode during private Pulse setup');
    }
    return {
      directoryMode: '0700',
      cookieMode: '0600',
      privateOwner: `${DAEMON_USER}:${DAEMON_GID}`,
      privatePaths,
      privateReadProbe: 'runuser -u nobody -- test -r <private-path>',
    };
  } finally {
    for (const path of privatePaths) {
      if (existsSync(path)) {
        if (!lstatSync(path).isDirectory() || realpathSync(path) !== path || dirname(path) !== parent) {
          throw new Error(`Refusing to clean a non-private Pulse scope: ${path}`);
        }
        rmSync(path, {recursive: true, force: true});
      }
    }
    if (privatePaths.some((path) => existsSync(path))) throw new Error('Private Pulse scopes were not cleaned up');
    const parentAfterCleanup = lstatSync(parent);
    if (parentAfterCleanup.uid !== 0 || parentAfterCleanup.gid !== 0 || parentAfterCleanup.mode !== parentBefore.mode) {
      throw new Error('The /tmp parent changed ownership or mode during private Pulse cleanup');
    }
  }
}

function assertNobodyDrop() {
  const record = command('getent', ['passwd', String(DAEMON_UID)]).split(':');
  if (record[0] !== DAEMON_USER || record[2] !== String(DAEMON_UID) || record[3] !== String(DAEMON_GID)) {
    throw new Error(`getent passwd ${DAEMON_UID} must resolve to nobody:${DAEMON_UID}:${DAEMON_GID}`);
  }
  const uid = command('runuser', ['-u', DAEMON_USER, '--', 'id', '-u']);
  if (uid !== String(DAEMON_UID)) throw new Error(`runuser -u ${DAEMON_USER} -- id -u returned ${uid}, expected ${DAEMON_UID}`);
  return {daemonUser: DAEMON_USER, daemonUid: DAEMON_UID, daemonGid: DAEMON_GID, runuserProbe: `runuser -u ${DAEMON_USER} -- id -u`};
}

export function uidWitness() {
  const parentUidBefore = process.getuid?.();
  const parentGidBefore = process.getgid?.();
  if (parentUidBefore !== 0 || parentGidBefore !== 0) {
    throw new Error('Pure UID witness requires the original root launcher UID/GID');
  }
  if (process.env.TAB_AUDIO_RUN === '1') throw new Error('Pure UID witness cannot run a capture');
  if (process.env.TAB_AUDIO_GRANT_PATH) throw new Error('Pure UID witness must not read a grant');
  const identity = assertNobodyDrop();
  const lifecycle = privateDirectoryLifecycle();
  if (process.getuid?.() !== 0 || process.getgid?.() !== 0) {
    throw new Error('Original root launcher UID/GID changed during the pure UID witness');
  }
  return {
    status: 'READY_PURE_UID_WITNESS',
    parentUidBefore,
    parentUidAfter: process.getuid(),
    parentGidBefore,
    parentGidAfter: process.getgid(),
    ...identity,
    ...lifecycle,
    cleanupVerified: lifecycle.privatePaths.every((path) => !existsSync(path)),
  };
}

function outputPath(path) {
  if (!path) return undefined;
  const absolute = resolve(path);
  const parent = dirname(absolute);
  const parentStat = existsSync(parent) ? statSync(parent) : undefined;
  const realParent = parentStat ? realpathSync(parent) : undefined;
  if (!parentStat || parentStat.uid !== process.getuid?.() || (parentStat.mode & 0o022) !== 0
    || realParent === FROZEN_PRIVATE_GRAPH.root || realParent?.startsWith(`${FROZEN_PRIVATE_GRAPH.root}/`)) {
    throw new Error('Pure preflight output must use an existing owned scope outside the dependency graph');
  }
  return absolute;
}

function baseReport() {
  const sourceSha = reviewedSource();
  const filesystem = statfsSync(APP_ROOT);
  return {
    sourceSha,
    controllerSha: sha256(readFileSync(CONTROLLER_PATH)),
    reviewedSourceSha: REVIEWED_SOURCE_SHA,
    sourceRoot: APP_ROOT,
    runMode: RUN_MODE_VALUE,
    diskFloorBytes: MIN_FREE_BYTES,
    diskFreeBytes: filesystem.bavail * filesystem.bsize,
    browserExecutable: BROWSER_EXECUTABLE,
    browserVersion: BROWSER_VERSION,
    nodeExecutable: NODE_EXECUTABLE,
    nodeVersion: process.version,
    nodeExecutableSha256: NODE_EXECUTABLE_SHA256,
    command: process.argv.join(' '),
  };
}

export function prepare() {
  const report = baseReport();
  const blockers = [];
  const check = (name, fn) => {
    try {
      const value = fn();
      if (value && typeof value === 'object') Object.assign(report, value);
    } catch (error) {
      blockers.push(`${name}: ${error instanceof Error ? error.message : String(error)}`);
    }
  };

  check('disk', () => { assertResources(); return {}; });
  // A low-disk machine is a deliberate hard stop. Do not perform graph,
  // identity, or lifecycle work and accidentally present a partial approval.
  if (blockers.length > 0) {
    report.status = 'BLOCKED_PURE_PREFLIGHT';
    report.blockers = blockers;
    report.diskOnlyBlocker = true;
    return report;
  }
  check('source', () => { assertSourceRoot(); assertOfflineEnvironment(); return {}; });
  check('run-mode', () => {
    if (process.env.TAB_AUDIO_RUN_MODE !== RUN_MODE_VALUE) throw new Error(`TAB_AUDIO_RUN_MODE must be ${RUN_MODE_VALUE}`);
    return {};
  });
  check('private-graph', () => {
    const graph = assertSelectedGraph();
    return {privateGraphRoot: graph.root, privateGraphSha256: graph.sha256, privateGraphFileCount: graph.fileCount};
  });
  check('node', () => {
    if (process.version !== 'v20.19.4' || realpathSync(process.execPath) !== realpathSync(NODE_EXECUTABLE)
      || sha256(readFileSync(process.execPath)) !== NODE_EXECUTABLE_SHA256) {
      throw new Error(`Probe must run with pinned Node v20.19.4 at ${NODE_EXECUTABLE}`);
    }
    return {};
  });
  check('source-fingerprint', () => {
    const fingerprint = sourceFingerprint();
    return {
      sourceTree: fingerprint.sourceTree,
      fullTrackedHash: fingerprint.fullTrackedHash,
      trackedFileCount: fingerprint.trackedFileCount,
      inputHash: fingerprint.inputHash,
      packageGraphHash: fingerprint.packageGraphHash,
      browserTreeSha256: fingerprint.browser.tree.sha256,
      browserExecutableSha256: fingerprint.browser.executableSha256,
      compositionFileCount: fingerprint.packages['@banodoco/timeline-composition']?.tree.fileCount,
    };
  });
  check('runuser', () => assertNobodyDrop());
  check('private-lifecycle', () => privateDirectoryLifecycle());
  check('tools', () => ({tools: toolVersions()}));

  report.status = blockers.length === 0 ? 'READY_PURE_PREFLIGHT' : 'BLOCKED_PURE_PREFLIGHT';
  report.blockers = blockers;
  report.diskOnlyBlocker = blockers.length === 1 && blockers[0].startsWith('disk:');
  return report;
}

export function preflight() {
  const report = prepare();
  const path = outputPath(process.env.TAB_AUDIO_PREFLIGHT_PATH);
  if (path) writeFileSync(path, JSON.stringify(report, null, 2), {flag: 'wx'});
  return report;
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  const action = process.argv[2] ?? '--prepare';
  if (action === '--prepare') console.log(JSON.stringify(prepare(), null, 2));
  else if (action === '--preflight') console.log(JSON.stringify(preflight(), null, 2));
  else if (action === '--uid-witness') console.log(JSON.stringify(uidWitness(), null, 2));
  else throw new Error(`Unknown controller command: ${action}`);
}
