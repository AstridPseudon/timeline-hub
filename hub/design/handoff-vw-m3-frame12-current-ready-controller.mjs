import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {access, readFile, readdir, stat} from 'node:fs/promises';
import {join, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';

const own = resolve(fileURLToPath(new URL('.', import.meta.url)));
const contractPath = join(own, 'handoff-vw-m3-frame12-current-ready-contract.json');
const app = resolve(process.env.VW_FRAME12_APP_ROOT ?? process.cwd());
const tuplePath = resolve(process.env.VW_FRAME12_SOURCE_TUPLE ?? join(own, 'frame12-source-tuple.json'));
const contract = JSON.parse(await readFile(contractPath, 'utf8'));
const digest = bytes => `sha256:${createHash('sha256').update(bytes).digest('hex')}`;
const git = (...args) => execFileSync('git', args, {cwd: app, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe']}).trim();
const pending = [];

function requireString(value, name) {
  if (typeof value !== 'string' || value.trim() === '') pending.push(name);
  return value;
}

async function fileCount(root) {
  let count = 0;
  async function visit(path) {
    for (const entry of await readdir(path, {withFileTypes: true})) {
      const child = join(path, entry.name);
      if (entry.isDirectory()) await visit(child);
      else if (entry.isFile()) count += 1;
      else pending.push(`regular file: ${child}`);
    }
  }
  await visit(root);
  return count;
}

async function present(path, name) {
  try { await stat(path); }
  catch { pending.push(name); }
}

async function assertArtifact(path, name) {
  try {
    const bytes = await readFile(path);
    assert.equal(digest(bytes), contract.source.composition_artifact_sha256, `${name} must be the immutable 0.0.12 artifact`);
    const listing = execFileSync('tar', ['-tzf', path], {encoding: 'utf8'}).trim().split('\n')
      .filter(entry => entry && !entry.endsWith('/'));
    assert.equal(listing.length, contract.source.composition_artifact_files, `${name} must contain all 77 files`);
  } catch (error) {
    pending.push(`${name}: ${error.message}`);
  }
}

async function main() {
  if (process.argv[2] !== '--check-ready') {
    throw new Error('This controller is READY-only. The manager must publish the final tuple and create the run controller separately.');
  }
  try {
    await access('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/viewing/QUIET.md');
    throw new Error('QUIET marker is present; no preparation check may proceed');
  } catch (error) {
    if (error.code !== 'ENOENT') throw error;
  }

  let tuple;
  try { tuple = JSON.parse(await readFile(tuplePath, 'utf8')); }
  catch { tuple = null; }
  if (!tuple) pending.push(`source tuple: ${tuplePath}`);
  else {
    requireString(tuple.app?.commit, 'actual App consumer12 commit');
    requireString(tuple.app?.tree, 'actual App consumer12 tree');
    requireString(tuple.agent?.commit, 'Agent consumer12 commit');
    requireString(tuple.agent?.tree, 'Agent consumer12 tree');
    requireString(tuple.runtime?.official_source_commit, 'official Runtime source commit');
    requireString(tuple.runtime?.official_client_commit, 'official generated client commit');
    if (tuple.runtime?.matching_official_pins !== true) pending.push('matching official Runtime/client pin attestation');
    if (tuple.peers?.app && Object.keys(tuple.peers.app).length !== contract.environment.peer_files_per_consumer) pending.push('App six-file peer manifest');
    if (tuple.peers?.agent && Object.keys(tuple.peers.agent).length !== contract.environment.peer_files_per_consumer) pending.push('Agent six-file peer manifest');
    if (tuple.source_freeze !== true) pending.push('final source freeze');
  }

  await assertArtifact(join(app, 'vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz'), 'App Composition artifact');
  const agentRoot = tuple?.agent?.root;
  if (typeof agentRoot === 'string' && agentRoot) {
    await assertArtifact(join(resolve(agentRoot), 'remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz'), 'Agent Composition artifact');
  } else pending.push('Agent checkout containing the 0.0.12 artifact');

  if (process.version !== `v${contract.environment.node}`) pending.push(`Node ${contract.environment.node}`);
  const expectedPaths = [
    ['playwright.viewing-parity.config.ts', 'existing parity controller config'],
    [contract.fixture.config, 'normal-profile-native1920 config'],
    ['tests/e2e/timeline/player-export-normal-profile-native1920.spec.ts', 'four-case normal profile spec'],
    ['tests/e2e/timeline/viewing-parity/frames.ts', 'existing Player capture helper'],
  ];
  for (const [path, name] of expectedPaths) await present(join(app, path), name);

  const appHead = git('rev-parse', 'HEAD');
  if (tuple?.app?.commit && appHead !== tuple.app.commit) pending.push(`App HEAD ${tuple.app.commit} (observed ${appHead})`);
  if (pending.length) {
    console.log(JSON.stringify({status: contract.status, actual_run: false, grant: false, pending_inputs: pending}, null, 2));
    process.exitCode = 78;
    return;
  }
  console.log(JSON.stringify({status: 'READY_ONLY_PENDING_MANAGER_GRANT', actual_run: false, grant: false, app: appHead}, null, 2));
}

await main();
