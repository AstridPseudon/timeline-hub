import { createHash } from 'node:crypto';
import { execFileSync, spawnSync } from 'node:child_process';
import { closeSync, lstatSync, mkdtempSync, openSync, readFileSync, readlinkSync, readdirSync, realpathSync, rmSync, statfsSync, statSync } from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

export const APP13 = Object.freeze({
  source: '30b8df2895536c471e270faf83ce710acd847065',
  tree: '0bf9c9f7fb849cb0938bf29fc72eca069014f623',
  status: 'pending-consumer-adoption',
});
export const AGENT13 = Object.freeze({
  source: 'd8749a9ce12a699672faf3ad96b4e4cbea9245c2',
  tree: '75354d38c898729bac09619679f5421faba319ed',
});
export const RUNTIME13 = Object.freeze({
  source: '2c4ac180c2220bdad966bc01e95ad230e99ce26a',
  tree: '7ab412cc4bcbe517efcfa806e092336390312e18',
});
export const COMPOSITION13 = Object.freeze({
  source: 'af98594dce80c0350a1fc21dfc44839b2279edf1',
  artifact: '9412ae25',
});
export const CHROME155 = Object.freeze({
  version: '155.0.8059.84',
  packageVersion: '155.0.8059.84-1',
  executable: '/opt/google/chrome/chrome',
  sha256: 'cb19b59995072b86cc7f887b3b1c7ab1f63518a7f2ed9f0d33249e1a040e2c76',
  treeSha256: '5b9b48fad617dc414d4a18ccfe9c7933c7bc4a8efd78c70d4f7a9e853808de0e',
  treeFileCount: 255,
});
export const NODE20 = Object.freeze({
  version: 'v20.19.4',
  executable: '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node',
  sha256: '43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490',
});
export const MIN_FREE_BYTES = 10 * 1024 ** 3;
export const SHORT_TEMP_PREFIX = 'timeline-tab-audio-';

export const CONTROL = Object.freeze({
  ownLeafOnly: true,
  wholeGraphPinned: true,
  all77BytesPinned: true,
  browserAndNodePinned: true,
  failClosedBeforeCapture: true,
  physicalMixClaim: false,
  app13Consumer: 'pending',
});

const OWN_LEAF = new Set([
  'tests/e2e/timeline/viewing-parity/cases.ts',
  'tests/e2e/timeline/viewing-parity/canvas.test.ts',
  'tests/e2e/timeline/viewing-parity/tab-audio.ts',
  'tests/e2e/timeline/viewing-parity/tab-audio.test.ts',
  'tests/e2e/timeline/viewing-parity/tab-audio.controller.mjs',
  'tests/e2e/timeline/viewing-parity/tab-audio.controller.test.mjs',
]);

function git(root, args) {
  return execFileSync('git', ['-C', root, ...args], { encoding: 'utf8' }).trim();
}

function sha256(bytes) {
  return createHash('sha256').update(bytes).digest('hex');
}

export function hashTree(root) {
  const entries = [];
  function visit(directory, prefix = '') {
    for (const name of readdirSync(directory).sort()) {
      const absolute = path.join(directory, name);
      const relative = `${prefix}${name}`;
      const stat = lstatSync(absolute);
      if (stat.isDirectory()) visit(absolute, `${relative}/`);
      else if (stat.isFile()) entries.push([relative, stat.mode & 0o111 ? 'executable' : 'file', sha256(readFileSync(absolute))]);
      else if (stat.isSymbolicLink()) entries.push([relative, 'symlink', sha256(Buffer.from(readlinkSync(absolute)))]);
      else throw new Error(`unsupported tree member: ${absolute}`);
    }
  }
  visit(root);
  entries.sort(([left], [right]) => left < right ? -1 : left > right ? 1 : 0);
  return { sha256: sha256(Buffer.from(JSON.stringify(entries))), fileCount: entries.length };
}

export function assertPhysicalPrivateGraph(root) {
  if (realpathSync(root) !== path.resolve(root) || !lstatSync(root).isDirectory()) {
    throw new Error('private dependency graph must be a real directory');
  }
  const links = new Map();
  function visit(directory) {
    for (const name of readdirSync(directory)) {
      const absolute = path.join(directory, name);
      const stat = lstatSync(absolute);
      if (stat.isDirectory()) visit(absolute);
      else if (stat.isSymbolicLink()) {
        const target = realpathSync(absolute);
        if (readlinkSync(absolute).startsWith('/') || !target.startsWith(`${path.resolve(root)}/`) || !statSync(target).isFile()) {
          throw new Error(`private dependency link escapes graph: ${absolute}`);
        }
      } else if (stat.isFile()) {
        const key = `${stat.dev}:${stat.ino}`;
        const entry = links.get(key) ?? { count: 0, links: stat.nlink, path: absolute };
        entry.count += 1;
        links.set(key, entry);
      } else throw new Error(`private dependency graph has unsupported member: ${absolute}`);
    }
  }
  visit(root);
  for (const entry of links.values()) {
    if (entry.count !== entry.links) throw new Error(`private dependency graph shares a file: ${entry.path}`);
  }
  return hashTree(root);
}

export function assertCandidateTuple(tuple = { app: APP13, agent: AGENT13, runtime: RUNTIME13, composition: COMPOSITION13 }) {
  for (const [name, expected] of Object.entries({ app: APP13, agent: AGENT13, runtime: RUNTIME13 })) {
    if (tuple[name]?.source !== expected.source || tuple[name]?.tree !== expected.tree) {
      throw new Error(`${name}13 candidate tuple changed; expected ${expected.source}/${expected.tree}`);
    }
  }
  if (tuple.composition?.source !== COMPOSITION13.source || tuple.composition?.artifact !== COMPOSITION13.artifact) {
    throw new Error(`composition13 candidate changed; expected ${COMPOSITION13.source}/${COMPOSITION13.artifact}`);
  }
  return tuple;
}

export function assertAppOwnLeaf(appRoot, base = APP13.source) {
  const changed = git(appRoot, ['diff', '--name-only', `${base}...HEAD`]).split('\n').filter(Boolean);
  const forbidden = changed.filter(file => !OWN_LEAF.has(file));
  if (forbidden.length) throw new Error(`App product/root/pin/DTO/source changes are not owned by this leaf: ${forbidden.join(', ')}`);
  return changed;
}

export function assertExactGraph({ appRoot, agentRoot, runtimeRoot }) {
  const appBase = git(appRoot, ['merge-base', APP13.source, 'HEAD']);
  if (appBase !== APP13.source) throw new Error(`App is not based on pending App13 candidate ${APP13.source}`);
  if (git(agentRoot, ['rev-parse', 'HEAD']) !== AGENT13.source) throw new Error('Agent13 source is not the approved keeper');
  if (git(runtimeRoot, ['rev-parse', 'HEAD']) !== RUNTIME13.source) throw new Error('Runtime13 source is not the approved producer');
  if (git(agentRoot, ['rev-parse', 'HEAD^{tree}']) !== AGENT13.tree) throw new Error('Agent13 tree is not the approved keeper');
  if (git(runtimeRoot, ['rev-parse', 'HEAD^{tree}']) !== RUNTIME13.tree) throw new Error('Runtime13 tree is not the approved producer');
  for (const [name, root] of Object.entries({ app: appRoot, agent: agentRoot, runtime: runtimeRoot })) {
    if (git(root, ['status', '--porcelain'])) throw new Error(`${name} source must be clean before capture`);
  }
  assertAppOwnLeaf(appRoot);
  return { app: git(appRoot, ['rev-parse', 'HEAD']), agent: AGENT13.source, runtime: RUNTIME13.source };
}

export function assertNode20(executable = process.execPath) {
  const actual = realpathSync(executable);
  if (process.version !== NODE20.version || actual !== realpathSync(NODE20.executable)) {
    throw new Error(`selected Node must be ${NODE20.version} at ${NODE20.executable}`);
  }
  const digest = sha256(readFileSync(actual));
  if (digest !== NODE20.sha256) throw new Error(`unexpected Node executable digest: ${digest}`);
  return { version: process.version, executable: actual, sha256: digest };
}

export function assertChrome155(binary = CHROME155.executable) {
  const version = execFileSync(binary, ['--version'], { encoding: 'utf8' }).trim();
  if (!version.includes(`Chrome ${CHROME155.version}`)) throw new Error(`unexpected Chrome: ${version}`);
  const packageVersion = execFileSync('dpkg-query', ['-W', '-f=${Version}', 'google-chrome-stable'], { encoding: 'utf8' }).trim();
  if (packageVersion !== CHROME155.packageVersion) throw new Error(`unexpected Chrome package: ${packageVersion}`);
  const digest = sha256(readFileSync(binary));
  if (digest !== CHROME155.sha256) throw new Error(`unexpected Chrome digest: ${digest}`);
  const tree = hashTree(path.dirname(realpathSync(binary)));
  if (tree.sha256 !== CHROME155.treeSha256 || tree.fileCount !== CHROME155.treeFileCount) {
    throw new Error(`unexpected Chrome155 full tree: ${tree.sha256}/${tree.fileCount}`);
  }
  return { version, packageVersion, digest, tree };
}

export function assertResources(root) {
  const { bavail, bsize } = statfsSync(root);
  if (bavail * bsize < MIN_FREE_BYTES) throw new Error('standing 10 GiB free-disk floor is not met');
  return bavail * bsize;
}

export function assertOwnedShortTemp() {
  const directory = mkdtempSync(path.join('/tmp', SHORT_TEMP_PREFIX));
  try {
    const stat = statSync(directory);
    if ((stat.mode & 0o777) !== 0o700 || path.dirname(directory) !== '/tmp') {
      throw new Error('tab capture temp must be an owned direct /tmp directory with mode 0700');
    }
    if (directory.length + '/com.google.Chrome/SingletonSocket'.length >= 108) {
      throw new Error('tab capture temp leaves Chrome singleton socket path too long');
    }
    return directory;
  } finally {
    rmSync(directory, { recursive: true, force: true });
  }
}

export function assertCompletedAppConsumer(appRoot) {
  if (APP13.status !== 'adopted') {
    throw new Error('App13 consumer adoption is pending; --ready remains refused');
  }
  if (git(appRoot, ['rev-parse', 'HEAD']) !== APP13.source || git(appRoot, ['rev-parse', 'HEAD^{tree}']) !== APP13.tree) {
    throw new Error('App13 consumer source/tree is not the completed approved candidate');
  }
}

export function assertFreshGrantAndMarker(appRoot) {
  const grantPath = process.env.TAB_AUDIO_GRANT_PATH;
  const markerPath = process.env.TAB_AUDIO_RUN_MARKER;
  if (!grantPath || !markerPath) throw new Error('fresh tab-audio grant and one-shot marker are required');
  const grant = JSON.parse(readFileSync(grantPath, 'utf8'));
  if (grant.approved !== true || grant.profile !== 'native-codec-chrome155'
    || grant.browserExecutable !== CHROME155.executable || grant.browserVersion !== CHROME155.version
    || grant.browserExecutableSha256 !== CHROME155.sha256 || grant.browserTreeSha256 !== CHROME155.treeSha256
    || grant.nodeVersion !== NODE20.version || grant.nodeExecutableSha256 !== NODE20.sha256
    || grant.sourceSha !== git(appRoot, ['rev-parse', 'HEAD']) || grant.sourceTree !== git(appRoot, ['rev-parse', 'HEAD^{tree}'])) {
    throw new Error('tab-audio grant does not match the selected source and environment');
  }
  const marker = JSON.parse(readFileSync(markerPath, 'utf8'));
  if (marker.sourceSha !== grant.sourceSha || marker.sourceTree !== grant.sourceTree) {
    throw new Error('one-shot marker does not match the fresh tab-audio grant');
  }
  return { grant, marker };
}

export function runParityPreflight(appRoot, agentRoot, runtimeRoot) {
  const helper = path.join(appRoot, 'tests/e2e/timeline/viewing-parity/harness.ts');
  const script = `import { assertRunBoundary, assertSourceVersionsUnchanged, sourceVersions } from ${JSON.stringify(pathToFileURL(helper).href)};\nconst profile = 'native-codec-chrome155';\nawait assertRunBoundary();\nconst before = await sourceVersions(profile);\nawait assertRunBoundary();\nconst after = await sourceVersions(profile);\nassertSourceVersionsUnchanged(before, after);\n`;
  const result = spawnSync(NODE20.executable, ['--import', 'tsx', '--input-type=module', '--eval', script], {
    cwd: appRoot,
    env: { ...process.env, ASTRID_CHECKOUT: agentRoot, ASTRID_RUNTIME_CHECKOUT: runtimeRoot },
    encoding: 'utf8',
  });
  if (result.status !== 0) throw new Error(`existing viewing-parity preflight failed: ${result.stderr || result.stdout}`);
  return result.stdout;
}

export function discover(appRoot) {
  const playwright = path.resolve(appRoot, 'node_modules', '@playwright', 'test', 'cli.js');
  const directory = mkdtempSync(path.join('/tmp', SHORT_TEMP_PREFIX));
  const stdoutPath = path.join(directory, 'discovery.stdout');
  const stderrPath = path.join(directory, 'discovery.stderr');
  let result;
  let output;
  try {
    const stdout = openSync(stdoutPath, 'w');
    const stderr = openSync(stderrPath, 'w');
    try {
      result = spawnSync(NODE20.executable, [playwright, 'test', '--config', 'playwright.viewing-parity.native-codec.config.ts', '--list'], {
        cwd: appRoot, stdio: ['ignore', stdout, stderr],
      });
    } finally {
      closeSync(stdout);
      closeSync(stderr);
    }
    output = `${readFileSync(stdoutPath, 'utf8')}${readFileSync(stderrPath, 'utf8')}`;
  } finally {
    rmSync(directory, { recursive: true, force: true });
  }
  if (result.status !== 0 || result.error) {
    throw new Error(`offline Playwright discovery failed: ${result.error?.message ?? output}`);
  }
  if (!/^Total: 5 tests in 1 file$/m.test(output)) throw new Error('offline discovery must find exactly five parity cases');
  const cases = readFileSync(path.join(appRoot, 'tests/e2e/timeline/viewing-parity/cases.ts'), 'utf8');
  const required = [
    "test('normal App Render action downloads",
    "test('fixture readiness seeks",
    "test('compares native-size actual Player frames",
    "test('captures the actual Player page as one native-PTS VP8/Opus tab stream",
    "test('picture-only one-host patch",
  ];
  if (required.some(testName => !cases.includes(testName))
    || cases.indexOf(required[3]) > cases.indexOf(required[4])) {
    throw new Error('offline discovery did not find the tab capture case');
  }
  return 'discovered exactly five native-codec-chrome155 parity cases';
}

export function readControlReport(reportPath) {
  const report = JSON.parse(readFileSync(reportPath, 'utf8'));
  if (report.physicalMixClaim === true || report.app13Consumer === 'adopted') {
    throw new Error('controller report must not promote the pending App13 consumer or physical mix');
  }
  return report;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const [command, appRoot = process.cwd(), agentRoot, runtimeRoot] = process.argv.slice(2);
  if (command === '--discover') {
    process.stdout.write(discover(appRoot));
  } else if (command === '--ready') {
    if (!agentRoot || !runtimeRoot) throw new Error('--ready requires app, agent, and runtime roots');
    assertCandidateTuple();
    assertCompletedAppConsumer(appRoot);
    assertExactGraph({ appRoot, agentRoot, runtimeRoot });
    assertResources(appRoot);
    assertOwnedShortTemp();
    const remotionProject = process.env.ASTRID_REMOTION_PROJECT_DIR;
    if (!remotionProject) throw new Error('ASTRID_REMOTION_PROJECT_DIR must select the frozen private graph');
    assertPhysicalPrivateGraph(path.join(appRoot, 'node_modules'));
    assertPhysicalPrivateGraph(path.join(remotionProject, 'node_modules'));
    assertNode20();
    assertChrome155();
    discover(appRoot);
    runParityPreflight(appRoot, agentRoot, runtimeRoot);
    assertFreshGrantAndMarker(appRoot);
    process.stdout.write('READY: offline preflight passed; no capture or physical-mix claim made\n');
  } else {
    throw new Error('usage: tab-audio.controller.mjs --discover <app-root> | --ready <app-root> <agent-root> <runtime-root>');
  }
}
