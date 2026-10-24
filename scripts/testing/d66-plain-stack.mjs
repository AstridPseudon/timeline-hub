import assert from 'node:assert/strict';
import { execFileSync, spawn } from 'node:child_process';
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync, realpathSync, statSync } from 'node:fs';
import { createServer } from 'node:net';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const orch = '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch';
const nodeDir = '/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin';
const node = path.join(nodeDir, 'node');
const readiness = 'tests/e2e/local/three-products.mounted-readiness.spec.ts';
const suites = {
  p1: { files: ['tests/e2e/local/three-products.p1-chain.spec.ts'], count: 2 },
  p2: { files: ['tests/e2e/local/three-products.p2-popup.spec.ts', 'tests/e2e/local/three-products.p2-tour.spec.ts', 'tests/e2e/local/three-products.p2-elements-assets.spec.ts'], count: 8 },
  'p2-element': {
    files: ['tests/e2e/local/three-products.p2-elements-assets.spec.ts'], count: 1,
    grep: 'P2 mounted element edit: real catalog apply, exact params patch, reload and guarded Undo$',
    retainRuntimeLogs: true,
  },
  p3: { files: ['tests/e2e/local/three-products.spec.ts'], count: 1,
    grep: 'M2 real gate 5 \\(M1 real mounted path\\): Agent edit, lost ACK, newer local gesture, exact retry, restart and undo preserve intent$' },
};

const normalHomes = {
  agent: process.env.D66_NORMAL_AGENT_HOME ?? '/home/user/work/agent',
  runtime: process.env.D66_NORMAL_RUNTIME_HOME ?? '/home/user/work/runtime',
};

const checkoutPrefixes = { agent: 'agt-pin', runtime: 'rt-pin' };

const selectedEnvironment = {
  agent: ['D66_AGENT_CHECKOUT', 'ASTRID_CHECKOUT'],
  runtime: ['D66_RUNTIME_CHECKOUT', 'ASTRID_RUNTIME_CHECKOUT'],
};

function git(dir, args) {
  return execFileSync('git', ['-C', dir, ...args], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
}

function optionalGit(dir, args) {
  try { return git(dir, args); } catch { return null; }
}

export function exactCheckoutPath(role, head, checkoutRoot = '/home/user/work/wt') {
  return path.join(checkoutRoot, `${checkoutPrefixes[role]}-${head.slice(0, 8)}`);
}

function missingCheckoutError(role, head, checkout) {
  return new Error(`D66 ${role} current normal HEAD ${head} needs a detached exact checkout at ${checkout}; request-checkout ${role} ${head} "D66 current ${role} source"`);
}

function sourcePath(env, role, normalState) {
  const key = selectedEnvironment[role].find((candidate) => env[candidate]?.trim());
  const requested = key
    ? env[key].trim()
    : exactCheckoutPath(role, normalState.head);
  if (!key && !existsSync(requested)) throw missingCheckoutError(role, normalState.head, requested);
  if (!path.isAbsolute(requested)) throw new Error(`D66 ${role} source must be an absolute checkout path: ${requested}`);
  return { key: key ?? 'automatic exact checkout route', requested };
}

/** Pure control shared by the launcher and its focused tests. */
export function validateSelectedSource({ role, selected, normal, normalState, selectedState }) {
  if (!selected || selected === normal) throw new Error(`D66 ${role} source must be a per-request checkout, not its mutable normal home`);
  if (selectedState.root !== selected) throw new Error(`D66 ${role} source root mismatch: ${selectedState.root}`);
  if (selectedState.branch) throw new Error(`D66 ${role} source must be detached: ${selected}`);
  if (selectedState.dirty) throw new Error(`D66 ${role} source is dirty: ${selected}`);
  if (selectedState.head !== normalState.head || selectedState.tree !== normalState.tree) {
    throw new Error(`D66 ${role} source is not the current normal head: selected ${selectedState.head}/${selectedState.tree}, current ${normalState.head}/${normalState.tree}; use detached exact checkout ${exactCheckoutPath(role, normalState.head)}`);
  }
  return { checkout: selected, head: selectedState.head, tree: selectedState.tree, normal_home: normal, normal_head: normalState.head, normal_tree: normalState.tree };
}

function checkoutState(checkout) {
  const resolved = realpathSync(checkout);
  if (!statSync(resolved).isDirectory()) throw new Error(`D66 source is not a directory: ${checkout}`);
  const rootPath = realpathSync(git(resolved, ['rev-parse', '--show-toplevel']));
  const state = {
    root: rootPath,
    head: git(resolved, ['rev-parse', 'HEAD']),
    tree: git(resolved, ['rev-parse', 'HEAD^{tree}']),
    branch: optionalGit(resolved, ['symbolic-ref', '--quiet', '--short', 'HEAD']),
    dirty: Boolean(git(resolved, ['status', '--porcelain=v1', '--untracked-files=all'])),
  };
  if (state.root !== resolved) throw new Error(`D66 source Git root differs from path: ${resolved}`);
  return state;
}

function selectSources(env = process.env) {
  const selected = {};
  for (const role of ['agent', 'runtime']) {
    const normal = realpathSync(normalHomes[role]);
    const normalState = checkoutState(normal);
    const requested = sourcePath(env, role, normalState).requested;
    const selectedRoot = realpathSync(requested);
    selected[role] = validateSelectedSource({
      role, selected: selectedRoot, normal,
      normalState, selectedState: checkoutState(selectedRoot),
    });
  }
  return selected;
}

function assertSourcesUnchanged(sources) {
  for (const role of ['agent', 'runtime']) {
    const state = checkoutState(sources[role].checkout);
    assert.equal(state.head, sources[role].head, `D66 ${role} checkout HEAD changed during run`);
    assert.equal(state.tree, sources[role].tree, `D66 ${role} checkout tree changed during run`);
    assert.equal(state.branch, null, `D66 ${role} checkout became attached during run`);
    assert.equal(state.dirty, false, `D66 ${role} checkout became dirty during run`);
  }
}

function requireExecutable(file, label) {
  if (!path.isAbsolute(file) || !existsSync(file) || !statSync(file).isFile()) throw new Error(`D66 ${label} is unavailable: ${file}`);
  return file;
}

function importReadback(sources, python, pythonpath) {
  const probe = [
    'import astrid, astrid_runtime, astrid_runtime_client, runtime_protocol, json',
    'print(json.dumps({"astrid": {"file": astrid.__file__, "version": getattr(astrid, "__version__", None)}, "astrid_runtime": {"file": astrid_runtime.__file__, "version": getattr(astrid_runtime, "__version__", None)}, "astrid_runtime_client": {"file": astrid_runtime_client.__file__, "version": getattr(astrid_runtime_client, "__version__", None)}, "runtime_protocol": {"file": runtime_protocol.__file__, "version": getattr(runtime_protocol, "__version__", None)}}))',
  ].join('; ');
  const env = { ...process.env,
    ASTRID_CHECKOUT: sources.agent.checkout, ASTRID_RUNTIME_CHECKOUT: sources.runtime.checkout,
    PYTHONPATH: pythonpath.join(path.delimiter),
    PYTHONDONTWRITEBYTECODE: '1', PYTHONUNBUFFERED: '1' };
  const value = JSON.parse(execFileSync(python, ['-c', probe], { cwd: sources.runtime.checkout, env, encoding: 'utf8' }).trim());
  const under = (file, checkout) => typeof file === 'string' && file.startsWith(checkout + path.sep);
  if (!under(value.astrid.file, sources.agent.checkout) || !under(value.astrid_runtime_client.file, sources.agent.checkout)
    || !under(value.astrid_runtime.file, sources.runtime.checkout) || !under(value.runtime_protocol.file, sources.runtime.checkout)) {
    throw new Error(`D66 import readback escaped selected sources: ${JSON.stringify(value)}`);
  }
  return value;
}

function repoHeads(sources) {
  return { app: git(root, ['rev-parse', 'HEAD']), agent: sources.agent.head, runtime: sources.runtime.head, composition: git('/home/user/work/composition', ['rev-parse', 'HEAD']) };
}

function repoTrees(sources) {
  return { app: git(root, ['rev-parse', 'HEAD^{tree}']), agent: sources.agent.tree, runtime: sources.runtime.tree, composition: git('/home/user/work/composition', ['rev-parse', 'HEAD^{tree}']) };
}

async function main() {
  const [name, mode = 'run'] = process.argv.slice(2);
  assert(suites[name], 'choose p1, p2, p2-element or p3');
  assert(['run', '--collect', '--launch'].includes(mode), 'unknown mode');
  const suite = suites[name];
  // Collection is a source-independent descriptor check. Service launch still
  // requires the detached exact current Agent/Runtime checkouts below.
  const sources = mode === '--collect' ? null : selectSources();
  if (sources) assertSourcesUnchanged(sources);
  const agentPython = requireExecutable(process.env.ASTRID_PYTHON ?? '/home/user/work/venv-agent/bin/python', 'Agent Python');
  const runtimePython = requireExecutable(process.env.ASTRID_RUNTIME_PYTHON ?? '/home/user/work/venv-runtime/bin/python', 'Runtime Python');
  const importVersions = sources ? {
    runtime: importReadback(sources, runtimePython, [sources.runtime.checkout, sources.agent.checkout]),
    agent: importReadback(sources, agentPython, [sources.agent.checkout, sources.runtime.checkout]),
  } : undefined;
  const snapshot = path.basename(root);
  const output = process.env.D66_OUTPUT_DIR ?? (snapshot.startsWith('.test-')
    ? path.join(orch, 'tests', snapshot.slice(6), 'd66')
    : path.join(process.env.TMPDIR ?? '/tmp', `d66-${name}`));
  mkdirSync(output, { recursive: true });

  for (const key of ['NODE_PATH', 'ASTRID_QUICK_DESCRIPTOR', 'ASTRID_APP_DIRECT_DIST', 'APP_DIRECT_DIST',
    'ASTRID_LOCAL_DATA_ROOT', 'ASTRID_RUNTIME_DATA_ROOT', 'ASTRID_LOCAL_SOURCE_MANIFEST', 'ASTRID_RUNTIME_SOURCE_MANIFEST',
    'BANODOCO_LOCAL_DATA_ROOT', 'BANODOCO_RUNTIME_DATA_ROOT', 'BANODOCO_LOCAL_SOURCE_MANIFEST', 'BANODOCO_RUNTIME_SOURCE_MANIFEST']) delete process.env[key];
  if (sources) Object.assign(process.env, {
    PATH: `${nodeDir}:${root}/node_modules/.bin:${process.env.PATH}`,
    ASTRID_CHECKOUT: sources.agent.checkout, ASTRID_PYTHON: agentPython,
    ASTRID_RUNTIME_CHECKOUT: sources.runtime.checkout, ASTRID_RUNTIME_PYTHON: runtimePython,
    ASTRID_REMOTION_PROJECT_DIR: '/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830',
    ASTRID_NODE_EXECUTABLE: node,
    ASTRID_TIMELINE_SCHEMA_PYTHONPATH: process.env.ASTRID_TIMELINE_SCHEMA_PYTHONPATH ?? '/home/user/work/venv-agent/lib/python3.13/site-packages',
    PYTHONDONTWRITEBYTECODE: '1', NODE_OPTIONS: '--max-old-space-size=6144',
    PLAYWRIGHT_BROWSERS_PATH: process.env.PLAYWRIGHT_BROWSERS_PATH ?? '/home/user/work/pw-browsers',
    TIMELINE_BUNDLE_AGENT_HEAD: sources.agent.head, TIMELINE_BUNDLE_RUNTIME_HEAD: sources.runtime.head,
  });
  const hashes = () => Object.fromEntries([...suite.files, readiness].map((file) =>
    [file, createHash('sha256').update(readFileSync(path.join(root, file))).digest('hex')]));
  const manifest = {
    suite: name, started_at: new Date().toISOString(),
    repo_heads: sources ? repoHeads(sources) : { app: git(root, ['rev-parse', 'HEAD']), composition: git('/home/user/work/composition', ['rev-parse', 'HEAD']) },
    repo_trees: sources ? repoTrees(sources) : { app: git(root, ['rev-parse', 'HEAD^{tree}']), composition: git('/home/user/work/composition', ['rev-parse', 'HEAD^{tree}']) },
    ...(sources ? { source_checkouts: sources } : {}),
    test_sha256_before: hashes(), service_versions: importVersions ? { imports: importVersions } : {},
    junit: { readiness: path.join(output, 'readiness.xml'), original: path.join(output, `${name}.xml`) },
  };
  const save = () => writeFileSync(path.join(output, 'manifest.json'), `${JSON.stringify(manifest, null, 2)}\n`);
  let stage = 'collection';
  save();

  function playwright(files, { grep, list = false, stage = name } = {}) {
    const args = [path.join(root, 'node_modules/@playwright/test/cli.js'), 'test', '--config', 'playwright.three-products.config.ts', ...files];
    if (grep) args.push('--grep', grep);
    args.push('--reporter', list ? 'list' : 'list,./config/testing/playwrightSkipGuard.ts,junit');
    if (list) args.push('--list');
    const env = { ...process.env, PLAYWRIGHT_OUTPUT_DIR: path.join(output, stage), PLAYWRIGHT_JUNIT_OUTPUT_FILE: manifest.junit[stage === 'readiness' ? 'readiness' : 'original'] };
    if (suite.retainRuntimeLogs && stage === name) env.D66_RUNTIME_LOG_DIR = path.join(output, 'runtime-private');
    return { args, env };
  }

  async function run(command, args, env = process.env) {
    const child = spawn(command, args, { cwd: root, env, stdio: 'inherit' });
    return new Promise((resolve, reject) => {
      child.once('error', reject);
      child.once('exit', (code, signal) => resolve(code ?? (signal ? 128 : 1)));
    });
  }

  async function launch() {
    stage = 'hosted-build';
    process.env.ASTRID_APP_DIRECT_DOOR_PORT = await new Promise((resolve, reject) => {
      const server = createServer();
      server.once('error', reject);
      server.listen(0, '127.0.0.1', () => { const port = server.address().port; server.close(() => resolve(String(port))); });
    });
    const { resolveHostedRuntimeOrigin } = await import('../hosted-build-origin.mjs');
    Object.assign(process.env, {
      VITE_RUNTIME_ORIGIN: resolveHostedRuntimeOrigin(),
      VITE_WORKSPACE_RUNTIME_EXPECTED_ACTOR_ID: '', VITE_WORKSPACE_RUNTIME_EXPECTED_REALM_ID: '', VITE_WORKSPACE_RUNTIME_EXPECTED_INSTANCE_ID: '',
      ASTRID_APP_DIRECT_DIST: path.join(output, 'dist'),
    });
    const { build } = await import('vite');
    await build({ configFile: path.join(root, 'config/vite/vite.config.ts'), cacheDir: path.join(output, 'vite-cache'), build: { outDir: process.env.ASTRID_APP_DIRECT_DIST, emptyOutDir: false } });
    const { startDirectHarness } = await import('../../tests/e2e/local/support/harness.ts');
    const { AstridCli } = await import('../../tests/e2e/local/support/astrid.ts');
    const { expect } = await import('@playwright/test');
    assertSourcesUnchanged(sources);
    manifest.repo_heads = repoHeads(sources);
    manifest.repo_trees = repoTrees(sources);
    manifest.service_versions.imports = {
      runtime: importReadback(sources, runtimePython, [sources.runtime.checkout, sources.agent.checkout]),
      agent: importReadback(sources, agentPython, [sources.agent.checkout, sources.runtime.checkout]),
    };
    process.env.TIMELINE_BUNDLE_AGENT_HEAD = manifest.repo_heads.agent;
    process.env.TIMELINE_BUNDLE_RUNTIME_HEAD = manifest.repo_heads.runtime;
    stage = 'normal-service-start';
    save();
    const harness = await startDirectHarness({ deferTimelineInitialization: true });
    try {
      const healthResponse = await fetch(`${harness.runtimeUrl}/v1/health`);
      assert.equal(healthResponse.status, 200);
      const health = await healthResponse.json();
      manifest.service_versions = { ...manifest.service_versions, node: process.version,
        npm: execFileSync(path.join(nodeDir, 'npm'), ['--version'], { encoding: 'utf8' }).trim(),
        runtime_server: healthResponse.headers.get('server'), protocol: health.protocol, schema_digest: health.schema_digest };
      stage = 'native-seed';
      save();
      const seed = await harness.seedThreeProducts();
      stage = 'agent-preflight';
      const astrid = await AstridCli.create(harness);
      const identity = await astrid.preflight();
      assert.equal(identity.astrid_head, sources.agent.head, 'Agent identity must be the selected current checkout');
      const packets = readdirSync(harness.tmp).filter((file) => file.startsWith('seed-') && file.endsWith('-accepted.json'))
        .map((file) => JSON.parse(readFileSync(path.join(harness.tmp, file), 'utf8')));
      const result = packets.find((packet) => packet.data?.accepted_revision_id === seed.headRevisionId);
      expect(result).toBeTruthy();
      const { data, receipt, request } = result;
      const history = await harness.runtimeJson('GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/commits?limit=50`);
      expect(history.status).toBe(200);
      expect(history.body.head).toEqual({ revision_id: data.accepted_revision_id, publication_id: receipt.receipt_id });
      const entry = history.body.items.find((item) => item.publication_id === receipt.receipt_id);
      expect(entry).toMatchObject({ publication_id: receipt.receipt_id, revision_id: data.accepted_revision_id,
        previous: { revision_id: data.previous_revision_id, publication_id: data.previous_publication_id }, receipt,
        intent: 'recorded', provider_version: data.provider_version, compiler_version: data.compiler_version,
        merge: request.merge, merge_mode: data.merge_mode, steps: data.steps, publisher: data.publisher, label: data.label,
        records: { schema_version: 1, label: data.label, merge_mode: data.merge_mode, steps: data.steps,
          commands: expect.any(Array), undo_of: [], restored_from: null } });
      expect(data.commands).toEqual(entry.records.commands.map((record) => record.command));
      expect(entry.reads).toEqual(request.reads);
      expect(entry.steps).toEqual(data.steps);
      expect(entry.records.steps).toEqual(data.steps);
      expect(entry.records.commands).toHaveLength(request.commands.length);
      expect(data.steps).toHaveLength(request.steps.length);
      Object.assign(manifest.service_versions, {
        agent_head: identity.astrid_head, agent_schema_digest: identity.schema_digest,
        provider: data.provider_version, compiler: data.compiler_version });
      assertSourcesUnchanged(sources);
      save();
      console.log('D66 normal launch, native seed, Agent identity and authoritative history PASS');
    } finally {
      await harness.stop();
    }
  }

  try {
    const collection = playwright(suite.files, { grep: suite.grep, list: true });
    const listed = execFileSync(node, collection.args, { cwd: root, env: collection.env, encoding: 'utf8' });
    writeFileSync(path.join(output, 'collection.txt'), listed);
    assert.match(listed, new RegExp(`Total: ${suite.count} tests? in `));
    console.log(listed.trim());
    if (mode !== '--collect') await launch();
    if (mode === 'run') {
      stage = 'mounted-readiness';
      const ready = playwright([readiness], { stage: 'readiness' });
      manifest.readiness_exit = await run(node, ready.args, ready.env);
      if (manifest.readiness_exit === 0) {
        stage = name;
        const original = playwright(suite.files, { grep: suite.grep });
        manifest.original_exit = await run(node, original.args, original.env);
      }
      process.exitCode = manifest.readiness_exit || manifest.original_exit || 0;
    }
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    const mismatch = message.match(/runtime health schema digest sha256:[a-f0-9]+ does not match this Astrid client's expected sha256:[a-f0-9]+|contract mismatch: the App vendors schema sha256:[a-f0-9]+ but Astrid vendors sha256:[a-f0-9]+/);
    manifest.failure = { stage, error: error?.name ?? 'Error', message: mismatch?.[0] ?? message };
    console.error(`D66 ${stage}: ${manifest.failure.message}`);
    process.exitCode = 1;
  } finally {
    manifest.test_sha256_after = hashes();
    assert.deepEqual(manifest.test_sha256_after, manifest.test_sha256_before);
    manifest.finished_at = new Date().toISOString();
    save();
    console.log(`D66 manifest: ${path.join(output, 'manifest.json')}`);
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    await main();
  } catch (error) {
    console.error(`D66 source selection: ${error instanceof Error ? error.message : String(error)}`);
    process.exitCode = 1;
  }
}
