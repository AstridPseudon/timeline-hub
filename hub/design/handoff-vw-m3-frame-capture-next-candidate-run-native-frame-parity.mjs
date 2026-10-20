import assert from 'node:assert/strict';
import { execFileSync, spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { lstat, readFile, readdir, readlink, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const own = dirname(fileURLToPath(import.meta.url));
const sourceSnapshot = process.cwd();
const app = sourceSnapshot;
const qualification = 'DIAGNOSTIC ONLY: native-codec Chrome155 Player + leased b70/9f9/f816 + installed8; no current tuple/public10/public11/gate6/adoption';
const profile = 'native-codec-chrome155';
const config = 'playwright.viewing-parity.normal-profile-native1920.config.ts';
const fixtureName = 'normal-profile-native1920';
const oneShot = 'vw-m3-frame-capture-next-candidate-20261020';
const expectedAppSHA = '7989ee28242c866fe8ea34f28e2e116faeaa0d86';
const expectedAppTree = '5f8d7059ebc8d2422a85f53b675f316fd83ce147';
const grantPath = join(own, `READY_GRANTED__${oneShot}`);
let grantBytes;
const quiet = '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/viewing/QUIET.md';
try {
  const marker = await readFile(quiet, 'utf8');
  await writeFile(join(own, 'PAUSED_ACK'), new Date().toISOString() + '\n');
  console.error(marker);
  process.exit(75);
} catch (error) { if (error.code !== 'ENOENT') throw error; }

const freezePath = join(own, 'source-freeze.json');
const git = (root, ...args) => execFileSync('git', args, { cwd: root, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
const sha256 = bytes => createHash('sha256').update(bytes).digest('hex');

// Content identity survives the central service's synthetic snapshot commit.
async function appSource() {
  const names = execFileSync('git', ['ls-files', '-z', '--cached', '--others', '--exclude-standard'],
    { cwd: app, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).split('\0').filter(Boolean).sort();
  const files = [];
  for (const name of names) {
    const absolute = join(app, name);
    const stat = await lstat(absolute);
    assert.ok(stat.isFile() || stat.isSymbolicLink(), `unexpected source member ${name}`);
    files.push([name, stat.isSymbolicLink() ? 'symlink' : stat.mode & 0o111 ? 'executable' : 'file',
      sha256(stat.isSymbolicLink() ? await readlink(absolute) : await readFile(absolute))]);
  }
  return { files: files.length, sha256: sha256(JSON.stringify(files)) };
}

// Directory hashes include every selected browser support file, not just ELF prefixes.
async function directoryHash(root) {
  const files = [];
  async function visit(directory, prefix = '') {
    for (const name of (await readdir(directory)).sort()) {
      const path = join(directory, name), relative = prefix + name, stat = await lstat(path);
      if (stat.isDirectory()) await visit(path, relative + '/');
      else {
        assert.ok(stat.isFile() || stat.isSymbolicLink(), `unexpected environment member: ${path}`);
        files.push([relative, stat.isSymbolicLink() ? 'symlink' : stat.mode & 0o111 ? 'executable' : 'file',
          sha256(stat.isSymbolicLink() ? await readlink(path) : await readFile(path))]);
      }
    }
  }
  await visit(root);
  return { files: files.length, sha256: sha256(JSON.stringify(files)) };
}
async function environment() {
  assert.equal(process.version, 'v20.19.4');
  const chromePackage = execFileSync('dpkg-query', ['-W', '-f=${Version}', 'google-chrome-stable'],
    { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
  assert.equal(chromePackage, '155.0.8059.84-1');
  return {
    profile, config, chromePackage, node: { version: process.version, executable: process.execPath,
      sha256: sha256(await readFile(process.execPath)) },
    playerDirectory: await directoryHash('/opt/google/chrome'),
    exportDirectory: await directoryHash('/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux'),
    playwright: await directoryHash(join(app, 'node_modules/playwright-core')),
  };
}

if (process.argv[2] === '--freeze') {
  assert.equal(git(app, 'rev-parse', 'HEAD'), expectedAppSHA, 'freeze must run on the final clean App branch');
  assert.equal(git(app, 'status', '--porcelain', '--untracked-files=normal'), '', 'freeze requires a clean App branch');
  await writeFile(freezePath, JSON.stringify({
    candidate: { fixture: fixtureName, config, profile },
    base: git(app, 'rev-parse', 'HEAD'), baseTree: git(app, 'rev-parse', 'HEAD^{tree}'),
    app: await appSource(), environment: await environment(),
  }, null, 2) + '\n');
} else {
  const checkOnly = process.argv[2] === '--verify-sources';
  assert.ok(checkOnly || process.argv.length === 2, 'unknown controller mode');
  assert.equal((await readFile(join(own, '../vw-m3-runtime-source-lease2/exit'), 'utf8')).trim(), '0');
  if (!checkOnly) {
    grantBytes = await readFile(grantPath, 'utf8');
    const grant = JSON.parse(grantBytes);
    assert.equal(grant.oneShot, oneShot);
    assert.equal(grant.fixture, fixtureName);
    assert.equal(typeof grant.fixtureDecisionReference, 'string');
    assert.ok(grant.fixtureDecisionReference.trim(), 'manager fixture decision reference required');
    assert.equal(grant.nativeCodecEnvironmentApproved, true, 'orchestrator approval of the explicit Chrome155 environment is required');
    assert.equal(grant.dimensionUnitReviewed, true, 'the separately reviewed native-dimension unit is required');
    assert.equal(grant.combinedCandidateReviewed, true, 'manager must freeze the final combined candidate after both reviews');
    assert.equal(typeof grant.environmentApprovalReference, 'string');
    assert.ok(grant.environmentApprovalReference.trim(), 'record the environment approval reference');
    assert.equal(grant.profile, profile);
    assert.deepEqual(grant.app, JSON.parse(await readFile(freezePath, 'utf8')).app,
      'grant must select the final reviewed combined App source');
    assert.match(sourceSnapshot, /^\/home\/user\/work\/wt\/\.test-[^/]+$/, 'actual run requires a central sourceSnapshot');
    assert.ok(process.env.VIEWING_BROWSER_FLOCK_HELD, 'central browser flock marker required');
    assert.equal(spawnSync('flock', ['-n', '/tmp/timeline-viewing-browser.lock', 'true'], { stdio: 'ignore' }).status, 1,
      'central browser flock must remain held');
  }
  assert.equal(process.version, 'v20.19.4');
  const frozen = JSON.parse(await readFile(freezePath, 'utf8'));
  assert.deepEqual(frozen.candidate, { fixture: fixtureName, config, profile });
  assert.equal(frozen.base, expectedAppSHA);
  assert.equal(frozen.baseTree, expectedAppTree);
  assert.deepEqual(frozen.app, {"files": 5959, "sha256": "47f87b3686d594899233865f96ed55785c378c54a59eb735996c26332c658717"});
  const { sourceVersions, assertSourceVersionsUnchanged } = await import(
    pathToFileURL(join(app, 'tests/e2e/timeline/viewing-parity/harness.ts')).href);
  function committedSource(root, revision, tree) {
    assert.equal(git(root, 'rev-parse', 'HEAD'), revision, `selected source revision: ${root}`);
    assert.equal(git(root, 'rev-parse', 'HEAD^{tree}'), tree, `selected source tree: ${root}`);
    assert.equal(git(root, 'status', '--porcelain', '--untracked-files=normal'), '', `dirty selected source: ${root}`);
    return { root, revision, tree };
  }
  const snapshotDirectory = await lstat(sourceSnapshot);
  const snapshotGitPath = join(sourceSnapshot, '.git');
  const snapshotGitStat = await lstat(snapshotGitPath);
  const snapshotGitFile = await readFile(snapshotGitPath, 'utf8');
  async function snapshot() {
    // The central shell must stay foreground until this controller's finally finishes.
    // Never substitute another App root if the service snapshot disappears.
    const directory = await lstat(sourceSnapshot);
    assert.equal(directory.dev, snapshotDirectory.dev, 'sourceSnapshot device changed');
    assert.equal(directory.ino, snapshotDirectory.ino, 'sourceSnapshot directory replaced');
    const gitStat = await lstat(snapshotGitPath);
    assert.equal(gitStat.dev, snapshotGitStat.dev, 'sourceSnapshot .git device changed');
    assert.equal(gitStat.ino, snapshotGitStat.ino, 'sourceSnapshot .git inode changed');
    assert.equal(await readFile(snapshotGitPath, 'utf8'), snapshotGitFile, 'sourceSnapshot git identity changed');
    const versions = await sourceVersions(profile);
    const { NORMAL_PROFILE_NATIVE1920 } = await import(pathToFileURL(join(app, 'tests/e2e/timeline/viewing-parity/canvas.ts')).href);
    assert.deepEqual(NORMAL_PROFILE_NATIVE1920, { width: 1920, height: 1080, viewport: { width: 2000, height: 1200 } });
    const selectedConfig = (await import(pathToFileURL(join(app, config)).href)).default;
    assert.equal(selectedConfig.testMatch, 'player-export-normal-profile-native1920.spec.ts');
    assert.deepEqual(selectedConfig.projects, [{ name: profile, metadata: { viewingParityBrowserProfile: profile } }]);
    assert.deepEqual(await environment(), frozen.environment, 'selected browser/Node/Playwright environment changed');
    assert.deepEqual(await appSource(), frozen.app, 'App differs from reviewed source freeze');
    if (!checkOnly) assert.equal(git(app, 'status', '--porcelain', '--untracked-files=normal'), '', 'central App snapshot must be clean');
    assert.deepEqual(versions.roots, { app,
      agent: '/home/user/work/wt/vw-m3-host-agent-source', runtime: '/home/user/work/wt/vw-m3-runtime-source-lease2',
      composition: '/home/user/work/composition',
    });
    assert.equal(versions.remotionProject, '/home/user/work/wt/vw-m1-ssr-snapshot/remotion');
    const selected = {
      agent: committedSource(versions.roots.agent, 'b70b9d569b2c80885d72734c61cd57e64c3715a8', '687f077c4771e3dbb66bfb7ff2b98f310ac054b6'),
      runtime: committedSource(versions.roots.runtime, '9f9b25c000485e919f30f1411831fe2d5a3c1316', '5c3a7e7141047d7295ab130a8f05359f4fcb34bc'),
      composition: committedSource(versions.roots.composition, 'ff0536bb53d84db5008b859be304b932b1dd5252', 'cc5491fbd9289d63554a92061a99d7a1822b95b5'),
      remotion: committedSource(dirname(versions.remotionProject), 'f8164bef73215272562c4d6974acadbd82c2898a', '4946dfa80999f3f9d828840c701544a67c8fe2b8'),
    };
    assert.equal(versions.playerBrowser.profile, profile);
    assert.equal(versions.playerBrowserExecutable, '/opt/google/chrome/chrome');
    assert.equal(versions.playerBrowser.version, '155.0.8059.84');
    assert.equal(versions.node, 'v20.19.4');
    if (!checkOnly) {
      assert.equal(await readFile(grantPath, 'utf8'), grantBytes, 'one-shot grant changed');
      assert.equal(spawnSync('flock', ['-n', '/tmp/timeline-viewing-browser.lock', 'true'], { stdio: 'ignore' }).status, 1, 'central browser flock lost');
      try {
        await readFile(quiet);
        await writeFile(join(own, 'PAUSED_ACK'), new Date().toISOString() + '\n');
        assert.fail('manager QUIET is active');
      } catch (error) { if (error.code !== 'ENOENT') throw error; }
    }
    return { qualification, fixture: fixtureName, sourceSnapshot, versions, selected, app: { root: app, revision: git(app, 'rev-parse', 'HEAD'),
      tree: git(app, 'rev-parse', 'HEAD^{tree}'), content: frozen.app } };
  }
  const proofPath = join(own, 'native-frame-source-result.json');
  const before = await snapshot(); // Exact graphs and selected sources BEFORE Playwright, including globalSetup.
  if (checkOnly) {
    await writeFile(join(own, 'source-preflight.json'), JSON.stringify(before, null, 2) + '\n');
    console.log(qualification);
    console.log('Explicit diagnostic sources, installed Composition (77 files each), six Remotion/Player hashes per consumer and App source freeze verified; no browser started.');
    process.exit(0);
  }
  await writeFile(proofPath, JSON.stringify({ before, postflight: 'pending' }, null, 2) + '\n');
  // Check QUIET again after hashing, immediately before any browser work.
  try {
    await readFile(quiet);
    await writeFile(join(own, 'PAUSED_ACK'), new Date().toISOString() + '\n');
    process.exit(75);
  } catch (error) { if (error.code !== 'ENOENT') throw error; }
  // Exclusive creation consumes this candidate's new grant exactly once.
  await writeFile(join(own, `RUN_STARTED__${oneShot}`), new Date().toISOString() + '\n', { flag: 'wx' });
  console.log(qualification);
  let result;
  let failure;
  try {
    result = spawnSync(process.execPath, [join(app, 'node_modules/playwright/cli.js'), 'test',
      '--config', config, 'player-export-normal-profile-native1920.spec.ts',
      '--project', profile, '--workers=1', '--retries=0', '--max-failures=0', '--reporter=list,json'], { cwd: app,
      env: { ...process.env, PLAYWRIGHT_JSON_OUTPUT_NAME: join(own, 'native-frame-tests.json') },
      stdio: 'inherit' });
    if (result.error) throw result.error;
    const report = JSON.parse(await readFile(join(own, 'native-frame-tests.json'), 'utf8'));
    assert.equal(report.stats.expected, 4, 'all four separately named native1920 cases must pass');
    for (const field of ['unexpected', 'flaky', 'skipped']) assert.equal(report.stats[field], 0);
    assert.equal(result.status, 0, `render door four-case baseline failed (status=${result.status}, signal=${result.signal})`);
  } catch (error) {
    failure = error;
  } finally {
    // Check after failure too; a failed render never waives graph/source checks.
    try {
      const after = await snapshot();
      assertSourceVersionsUnchanged(before.versions, after.versions);
      assert.deepEqual(after, before);
      await writeFile(proofPath, JSON.stringify({ before, after, postflight: 'passed',
        playwright: { status: result?.status, signal: result?.signal, error: failure?.message } }, null, 2) + '\n');
    } catch (error) {
      await writeFile(proofPath, JSON.stringify({ before, postflight: 'failed', postflightError: error.message,
        playwright: { status: result?.status, signal: result?.signal, error: failure?.message } }, null, 2) + '\n');
      failure = failure ? new AggregateError([failure, error], 'render door four-case baseline and source postflight failed') : error;
    }
  }
  if (failure) throw failure;
}
