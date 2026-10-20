import { execFileSync, spawnSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import path from 'node:path';

export const APP13 = Object.freeze({
  source: 'b1ef4b9b910ba72375c34cf319692f90d22edc25',
  tree: '8d8a10b057ed31fed69517e18a23b8ec3811447a',
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
  source: 'af98594d',
  artifact: '9412ae25',
});
export const CHROME155 = Object.freeze({
  version: '155.0.8059.84',
  executable: '/opt/google/chrome/chrome',
  sha256: 'cb19b599',
});

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
  for (const [name, root] of Object.entries({ app: appRoot, agent: agentRoot, runtime: runtimeRoot })) {
    if (git(root, ['status', '--porcelain'])) throw new Error(`${name} source must be clean before capture`);
  }
  assertAppOwnLeaf(appRoot);
  return { app: git(appRoot, ['rev-parse', 'HEAD']), agent: AGENT13.source, runtime: RUNTIME13.source };
}

export function assertChrome155(binary = CHROME155.executable, expectedSha = CHROME155.sha256) {
  const version = execFileSync(binary, ['--version'], { encoding: 'utf8' }).trim();
  if (!version.includes(`Chrome ${CHROME155.version}`)) throw new Error(`unexpected Chrome: ${version}`);
  const digest = execFileSync('sha256sum', [binary], { encoding: 'utf8' }).split(/\s+/)[0];
  if (!digest.startsWith(expectedSha)) throw new Error(`unexpected Chrome digest: ${digest}`);
  return { version, digest };
}

export function discover(appRoot) {
  const playwright = path.resolve(appRoot, 'node_modules', '@playwright', 'test', 'cli.js');
  const result = spawnSync(process.execPath, [playwright, 'test', '--config', 'playwright.viewing-parity.native-codec.config.ts', '--list'], {
    cwd: appRoot, stdio: 'inherit',
  });
  if (result.status !== 0) throw new Error('offline Playwright discovery failed');
  const cases = readFileSync(path.join(appRoot, 'tests/e2e/timeline/viewing-parity/cases.ts'), 'utf8');
  if (!cases.includes("test('captures the actual Player page as one native-PTS VP8/Opus tab stream")) {
    throw new Error('offline discovery did not find the tab capture case');
  }
  return 'discovered native-codec-chrome155 tab capture case';
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
    assertExactGraph({ appRoot, agentRoot, runtimeRoot });
    assertChrome155();
    process.stdout.write('READY literal: offline controls passed; App13 consumer remains pending; physical mix remains unclaimed\n');
  } else {
    throw new Error('usage: tab-audio.controller.mjs --discover <app-root> | --ready <app-root> <agent-root> <runtime-root>');
  }
}
