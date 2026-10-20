import { createHash } from 'node:crypto';
import { execFileSync, spawnSync } from 'node:child_process';
import {
  closeSync,
  existsSync,
  lstatSync,
  openSync,
  readFileSync,
  readlinkSync,
  readdirSync,
  realpathSync,
  statSync,
  writeFileSync,
} from 'node:fs';
import { createRequire } from 'node:module';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

export const PROFILE = 'native-codec-chrome155';
export const NODE_VERSION = 'v20.19.4';
export const NODE_EXECUTABLE = '/tmp/vw-m3-agent-gate-node20.19.4/bin/node';
export const BROWSER_EXECUTABLE = '/opt/google/chrome/chrome';
export const BROWSER_VERSION = '155.0.8059.84';
export const REPO_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../../..');
export const SOURCE_FILES = [
  'tests/e2e/timeline/tab-audio-capture.analysis.mjs',
  'tests/e2e/timeline/tab-audio-capture.analysis.test.mjs',
  'tests/e2e/timeline/tab-audio-capture.probe.ts',
  'tests/e2e/timeline/tab-audio-capture.config.ts',
  'tests/e2e/timeline/tab-audio-capture.controller.mjs',
  'tests/e2e/timeline/setup-tab-audio-capture.sh',
];
const INPUT_FILE_PREFIXES = [
  'playwright.config.ts',
  'package.json',
  'package-lock.json',
  'tests/e2e/timeline/support.ts',
  'tests/e2e/timeline/tab-audio-capture.config.ts',
  'tests/e2e/fake-runtime/',
  ...SOURCE_FILES,
];
const REQUIRED_PACKAGES = [
  '@playwright/test',
  'playwright',
  'playwright-core',
  'react',
  'react-dom',
  'remotion',
  '@remotion/player',
  '@banodoco/timeline-composition',
];
const EXPECTED_PACKAGE_VERSIONS = {
  '@playwright/test': '1.60.0',
  playwright: '1.60.0',
  react: '18.3.1',
  'react-dom': '18.3.1',
  remotion: '4.0.509',
  '@remotion/player': '4.0.509',
  '@remotion/media': '4.0.509',
  '@remotion/web-renderer': '4.0.509',
  '@remotion/layout-utils': '4.0.509',
  '@banodoco/timeline-composition': '0.0.8',
};
const FROZEN_BROWSER = {
  packageVersion: '155.0.8059.84-1',
  executableSha256: 'cb19b59995072b86cc7f887b3b1c7ab1f63518a7f2ed9f0d33249e1a040e2c76',
  tree: {sha256: '5b9b48fad617dc414d4a18ccfe9c7933c7bc4a8efd78c70d4f7a9e853808de0e', fileCount: 255},
};
const FROZEN_PLAYWRIGHT_CORE = {
  version: '1.60.0',
  tree: {sha256: '6a78060c81886b7ba6f631d5b1193d50f0362c779f5b2dff2d784a31a6acc46d', fileCount: 106},
};
const FROZEN_RENDER_GRAPH_HASHES = {
  '@remotion/player/dist/cjs/PlayerUI.js': '5dc9b4b89310609f57a718c641334d530b72ecf284fc1682610afcec208a4fbb',
  '@remotion/player/dist/cjs/use-player-methods.js': 'ff50ab8b4ae86423fab18aa1ecf6c48c41501c4f7b527f05a55c2c36598def46',
  '@remotion/player/dist/cjs/use-playback.js': '6c8369a19d7a29eab5dab4642799172d4f2a7e11dad39125edcb673ec5729fb0',
  '@remotion/player/dist/esm/index.mjs': 'd3ef9728584c78e0e01cdb71ad72e3c6ddb36f96bfef90a4231d8b795e906b12',
  'remotion/dist/esm/index.mjs': '5a1584f7660fa8fffa7eb8fe016b82a4d719e67d4b7904d4fa4f299eb1355f28',
  'remotion/dist/cjs/audio/shared-audio-tags.js': '949ccec3419398183e8e22f63820a4a57cb8379befb184fbac9a3acde040c5b8',
};

const ORCH_ROOT = process.env.ORCH_ROOT
  ?? '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch';
const QUIET_FILES = [join(ORCH_ROOT, 'QUIET.md'), join(ORCH_ROOT, 'managers/viewing/QUIET.md')];
const require = createRequire(import.meta.url);

function sha256(bytes) {
  return createHash('sha256').update(bytes).digest('hex');
}

function git(...args) {
  return execFileSync('git', args, { cwd: REPO_ROOT, encoding: 'utf8' }).trim();
}

function trackedFiles() {
  return git('ls-files', '-z').split('\0').filter(Boolean);
}

function hashFiles(files, root = REPO_ROOT) {
  const hash = createHash('sha256');
  for (const relativePath of [...files].sort()) {
    const bytes = readFileSync(join(root, relativePath));
    hash.update(relativePath).update('\0').update(bytes).update('\0');
  }
  return {sha256: hash.digest('hex'), fileCount: files.length};
}

function inputFiles(allTracked) {
  const files = allTracked.filter((path) => INPUT_FILE_PREFIXES.some((prefix) =>
    prefix.endsWith('/') ? path.startsWith(prefix) : path === prefix));
  if (files.length === 0) throw new Error('No tracked probe input files were found');
  return files;
}

export function hashTree(root) {
  const entries = [];
  function visit(directory, prefix = '') {
    for (const name of readdirSync(directory).sort()) {
      const absolute = join(directory, name);
      const relativePath = `${prefix}${name}`;
      const stat = lstatSync(absolute);
      if (stat.isDirectory()) visit(absolute, `${relativePath}/`);
      else if (stat.isFile()) entries.push([relativePath, stat.mode & 0o111 ? 'executable' : 'file', sha256(readFileSync(absolute))]);
      else if (stat.isSymbolicLink()) entries.push([relativePath, 'symlink', sha256(Buffer.from(readlinkSync(absolute)))]);
      else throw new Error(`Unsupported dependency tree entry: ${absolute}`);
    }
  }
  visit(root);
  return {sha256: sha256(Buffer.from(JSON.stringify(entries))), fileCount: entries.length};
}

function packageFingerprint(name) {
  const packageJson = require.resolve(`${name}/package.json`);
  const packageRoot = realpathSync(dirname(packageJson));
  const metadata = JSON.parse(readFileSync(packageJson, 'utf8'));
  return {
    version: metadata.version,
    tree: hashTree(packageRoot),
  };
}

function packageGraphFingerprint() {
  const packages = Object.fromEntries(REQUIRED_PACKAGES.map((name) => [name, packageFingerprint(name)]));
  return {
    packages,
    sha256: sha256(Buffer.from(JSON.stringify(packages))),
  };
}

function browserFingerprint() {
  if (!existsSync(BROWSER_EXECUTABLE)) throw new Error(`Pinned Chrome executable is missing: ${BROWSER_EXECUTABLE}`);
  const executable = realpathSync(BROWSER_EXECUTABLE);
  const root = dirname(executable);
  const stat = statSync(executable);
  if (!stat.isFile() || (stat.mode & 0o111) === 0) throw new Error('Pinned Chrome executable is not executable');
  const versionOutput = execFileSync(BROWSER_EXECUTABLE, ['--version'], {
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'ignore'],
  });
  const version = versionOutput.match(/Chrome\s+(\d+\.\d+\.\d+\.\d+)/)?.[1];
  const packageVersion = execFileSync('dpkg-query', ['-W', '-f=${Version}', 'google-chrome-stable'], {encoding: 'utf8'}).trim();
  const fingerprint = {
    executable: BROWSER_EXECUTABLE,
    version,
    packageVersion,
    executableSha256: sha256(readFileSync(executable)),
    tree: hashTree(root),
  };
  if (fingerprint.version !== BROWSER_VERSION || fingerprint.packageVersion !== FROZEN_BROWSER.packageVersion
    || fingerprint.executableSha256 !== FROZEN_BROWSER.executableSha256
    || JSON.stringify(fingerprint.tree) !== JSON.stringify(FROZEN_BROWSER.tree)) {
    throw new Error('Chrome155 executable/version/full tree does not match the frozen environment');
  }
  return fingerprint;
}

export function renderGraphFingerprint() {
  const nodeModules = dirname(dirname(dirname(require.resolve('@remotion/player/package.json'))));
  return Object.fromEntries(Object.entries(FROZEN_RENDER_GRAPH_HASHES).map(([relativePath]) => [
    relativePath,
    sha256(readFileSync(join(nodeModules, relativePath))),
  ]));
}

export function sourceFingerprint() {
  const allTracked = trackedFiles();
  const selectedInputs = inputFiles(allTracked);
  const fullTracked = hashFiles(allTracked);
  const inputs = hashFiles(selectedInputs);
  const sourceSha = git('rev-parse', 'HEAD');
  const sourceTree = git('rev-parse', 'HEAD^{tree}');
  const packages = packageGraphFingerprint();
  if (process.version !== NODE_VERSION || realpathSync(process.execPath) !== realpathSync(NODE_EXECUTABLE)) {
    throw new Error(`Probe must run with pinned Node ${NODE_VERSION} at ${NODE_EXECUTABLE}`);
  }
  if (packages.packages['playwright-core'].version !== FROZEN_PLAYWRIGHT_CORE.version
    || JSON.stringify(packages.packages['playwright-core'].tree) !== JSON.stringify(FROZEN_PLAYWRIGHT_CORE.tree)) {
    throw new Error('Underlying playwright-core graph does not match the frozen environment');
  }
  const renderGraphHashes = renderGraphFingerprint();
  if (JSON.stringify(renderGraphHashes) !== JSON.stringify(FROZEN_RENDER_GRAPH_HASHES)) {
    throw new Error('Remotion/Player render graph does not match the frozen environment');
  }
  return {
    sourceSha,
    sourceTree,
    fullTrackedHash: fullTracked.sha256,
    trackedFileCount: fullTracked.fileCount,
    inputHash: inputs.sha256,
    inputFiles: selectedInputs,
    node: {
      version: process.version,
      executable: process.execPath,
      executableSha256: sha256(readFileSync(process.execPath)),
    },
    browser: browserFingerprint(),
    packages: packages.packages,
    packageGraphHash: packages.sha256,
    renderGraphHashes,
  };
}

function assertFingerprintField(grant, fingerprint, field) {
  if (grant[field] !== fingerprint[field]) {
    throw new Error(`Tab-audio grant ${field} does not match the selected source`);
  }
}

export function assertGrant(grant, fingerprint, finalSha = process.env.TAB_AUDIO_FINAL_SHA) {
  if (grant?.approved !== true) throw new Error('Tab-audio grant is not approved');
  if (grant.profile !== PROFILE || grant.browserExecutable !== BROWSER_EXECUTABLE || grant.browserVersion !== BROWSER_VERSION) {
    throw new Error('Tab-audio grant does not name the approved Chrome155 profile');
  }
  if (grant.backendOrder?.join(',') !== 'tab,private-pulse') {
    throw new Error('Tab-audio grant must preserve tab capture before private PulseAudio fallback');
  }
  for (const field of ['sourceSha', 'sourceTree', 'fullTrackedHash', 'inputHash', 'packageGraphHash']) {
    assertFingerprintField(grant, fingerprint, field);
  }
  if (grant.finalSha !== fingerprint.sourceSha || finalSha !== fingerprint.sourceSha) {
    throw new Error('Tab-audio grant final SHA does not match the committed source SHA');
  }
  if (fingerprint.node.version !== NODE_VERSION) throw new Error(`Unsupported Node version: ${fingerprint.node.version}`);
  if (grant.nodeVersion !== fingerprint.node.version || grant.nodeExecutableSha256 !== fingerprint.node.executableSha256) {
    throw new Error('Tab-audio grant Node identity is stale');
  }
  if (grant.browserTreeSha256 !== fingerprint.browser.tree.sha256
    || grant.browserExecutableSha256 !== fingerprint.browser.executableSha256) {
    throw new Error('Tab-audio grant Chrome155 tree is stale');
  }
  if (JSON.stringify(grant.packages) !== JSON.stringify(fingerprint.packages)) {
    throw new Error('Tab-audio grant package graph is stale');
  }
  if (JSON.stringify(grant.renderGraphHashes) !== JSON.stringify(fingerprint.renderGraphHashes)) {
    throw new Error('Tab-audio grant Remotion/Player render graph is stale');
  }
  for (const [name, version] of Object.entries(EXPECTED_PACKAGE_VERSIONS)) {
    if (fingerprint.packages[name]?.version !== version) throw new Error(`Unexpected ${name} version`);
  }
  if (fingerprint.packages['@banodoco/timeline-composition']?.tree.fileCount !== 77) {
    throw new Error('Composition package must contain the approved 77-file graph');
  }
  if (!grant.environmentApprovalReference) throw new Error('Tab-audio grant lacks environment approval reference');
  return grant;
}

export function assertFingerprintUnchanged(before, after) {
  for (const field of ['sourceSha', 'sourceTree', 'fullTrackedHash', 'inputHash', 'node', 'browser', 'packages', 'packageGraphHash', 'renderGraphHashes']) {
    if (JSON.stringify(before[field]) !== JSON.stringify(after[field])) {
      throw new Error(`Probe dependency identity changed during capture: ${field}`);
    }
  }
}

function assertQuietAbsent() {
  const present = QUIET_FILES.filter((path) => existsSync(path));
  if (present.length > 0) throw new Error(`QUIET guard is active: ${present.join(', ')}`);
}

function requiredEnv(name) {
  const value = process.env[name];
  if (!value) throw new Error(`Missing required guard environment: ${name}`);
  return value;
}

function readGrant() {
  const path = requiredEnv('TAB_AUDIO_GRANT_PATH');
  const grant = JSON.parse(readFileSync(path, 'utf8'));
  const fingerprint = sourceFingerprint();
  assertGrant(grant, fingerprint);
  return {grant, fingerprint};
}

function assertCleanSource() {
  if (git('status', '--porcelain', '--untracked-files=all')) {
    throw new Error('Selected App source must be a clean committed worktree');
  }
}

function ensureFlock() {
  if (process.env.VIEWING_BROWSER_FLOCK_HELD !== '1' || process.env.TAB_AUDIO_LOCK_FD !== '9') {
    throw new Error('The central browser flock is not declared held by the shared lock FD');
  }
  const lockPath = requiredEnv('TAB_AUDIO_LOCK_PATH');
  const probe = spawnSync('flock', ['-n', lockPath, '-c', 'true'], {stdio: 'ignore'});
  if (probe.status !== 1) throw new Error('The shared browser flock is not held by the invoking shell');
}

function preflight() {
  assertQuietAbsent();
  ensureFlock();
  assertCleanSource();
  const {grant, fingerprint} = readGrant();
  const statePath = requiredEnv('TAB_AUDIO_PREFLIGHT_PATH');
  writeFileSync(statePath, JSON.stringify({profile: PROFILE, grant, fingerprint}, null, 2), {flag: 'wx'});
  return {status: 'READY_GRANTED', profile: PROFILE, sourceSha: fingerprint.sourceSha, sourceTree: fingerprint.sourceTree};
}

function claim() {
  assertQuietAbsent();
  ensureFlock();
  assertCleanSource();
  const markerPath = requiredEnv('TAB_AUDIO_RUN_MARKER');
  const {grant, fingerprint} = readGrant();
  const markerFd = openSync(markerPath, 'wx');
  closeSync(markerFd);
  writeFileSync(markerPath, JSON.stringify({profile: PROFILE, finalSha: grant.finalSha,
    sourceSha: fingerprint.sourceSha, sourceTree: fingerprint.sourceTree, inputHash: fingerprint.inputHash, pid: process.pid}, null, 2));
  return {status: 'RUN_STARTED', markerPath, sourceSha: fingerprint.sourceSha};
}

function postflight() {
  assertQuietAbsent();
  const state = JSON.parse(readFileSync(requiredEnv('TAB_AUDIO_PREFLIGHT_PATH'), 'utf8'));
  assertCleanSource();
  const {fingerprint} = readGrant();
  assertFingerprintUnchanged(state.fingerprint, fingerprint);
  if (process.env.TAB_AUDIO_RUN === '1' && !existsSync(requiredEnv('TAB_AUDIO_RUN_MARKER'))) {
    throw new Error('One-shot run marker was not retained');
  }
  return {status: 'POSTFLIGHT_OK', sourceSha: fingerprint.sourceSha, sourceTree: fingerprint.sourceTree};
}

const invokedAsScript = process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href;
if (invokedAsScript) {
  const command = process.argv[2] ?? '--fingerprint';
  if (command === '--fingerprint') console.log(JSON.stringify(sourceFingerprint(), null, 2));
  else if (command === '--preflight') console.log(JSON.stringify(preflight(), null, 2));
  else if (command === '--claim') console.log(JSON.stringify(claim(), null, 2));
  else if (command === '--postflight') console.log(JSON.stringify(postflight(), null, 2));
  else throw new Error(`Unknown controller command: ${command}`);
}
