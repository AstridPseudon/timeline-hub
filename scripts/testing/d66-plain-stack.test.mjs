import assert from 'node:assert/strict';
import test from 'node:test';
import { execFileSync, spawnSync } from 'node:child_process';
import { mkdtempSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { appCheckoutTarget, buildSubmitPlan, captureSubmitPins, exactCheckoutPath, playwrightLaunchEnv, preflightSources, receiptCheckout, registerSubmitRecipes, selectPinnedSources, serviceRecipe, suites, submit, validatePinnedSource, validatePinnedSources, validateSelectedSource, waitForSubmitReceipts } from './d66-plain-stack.mjs';

const state = (overrides = {}) => ({
  root: '/snapshot/agent', head: 'a'.repeat(40), tree: 'b'.repeat(40), branch: null, dirty: false, ...overrides,
});

test('D66 full P2 launch retains bounded Runtime phase logs while other suites stay opt-in', () => {
  const junit = { readiness: '/tmp/readiness.xml', original: '/tmp/original.xml' };
  const launch = (suiteName, stage = suiteName, output = `/tmp/d66-${suiteName}-launch`) => playwrightLaunchEnv({
    suite: suites[suiteName], suiteName, output, junit, stage,
    baseEnv: { NODE_ENV: 'test', D66_RUNTIME_LOG_DIR: '/tmp/inherited-observer-must-not-leak' },
  });

  assert.equal(launch('p2').D66_RUNTIME_LOG_DIR, path.join('/tmp/d66-p2-launch', 'runtime-private'));
  assert.equal(launch('p2', 'readiness').D66_RUNTIME_LOG_DIR, undefined);
  assert.equal(launch('p2-element').D66_RUNTIME_LOG_DIR, path.join('/tmp/d66-p2-element-launch', 'runtime-private'));
  assert.equal(launch('p1').D66_RUNTIME_LOG_DIR, undefined);
  assert.equal(launch('p3').D66_RUNTIME_LOG_DIR, undefined);
  assert.notEqual(launch('p2').D66_RUNTIME_LOG_DIR, launch('p2-element').D66_RUNTIME_LOG_DIR);
});

test('D80 focused P2 descriptors select one exact original test each', () => {
  const expected = {
    'p2-register-asset': ['tests/e2e/local/three-products.p2-elements-assets.spec.ts', 'P2 mounted registerAsset save: real file drop, exact media/registry fields, reload and guarded Undo$'],
    'p2-automatic-child-placement': ['tests/e2e/local/three-products.p2-elements-assets.spec.ts', 'P2 mounted automatic child placement: embedded shot file gesture, occurrence command, closure and guarded Undo$'],
    'p2-popup-swap': ['tests/e2e/local/three-products.p2-popup.spec.ts', 'P2 popup mounted SWAP on selected child uses authenticated old/new media selections$'],
    'p2-transition-none-single': ['tests/e2e/local/three-products.p2-tour.spec.ts', 'P2 mounted transition None single: raw clear preserves opaque data/order and guarded Undo$'],
    'p2-transition-none-bulk': ['tests/e2e/local/three-products.p2-tour.spec.ts', 'P2 mounted transition None bulk: atomic raw clears preserve unknown fields/order and guarded Undo$'],
  };
  for (const [name, [file, grep]] of Object.entries(expected)) {
    assert.deepEqual(suites[name].files, [file]);
    assert.equal(suites[name].count, 1);
    assert.equal(suites[name].grep, grep);
    assert.equal(suites[name].retainRuntimeLogs, true);
  }
});

test('D66 accepts a detached clean checkout matching the normal head and tree', () => {
  assert.deepEqual(validateSelectedSource({
    role: 'agent', selected: '/snapshot/agent', normal: '/home/user/work/agent',
    normalState: state(), selectedState: state(),
  }), {
    checkout: '/snapshot/agent', head: 'a'.repeat(40), tree: 'b'.repeat(40),
    normal_home: '/home/user/work/agent', normal_head: 'a'.repeat(40), normal_tree: 'b'.repeat(40),
  });
});

test('D66 refuses a source that is the mutable normal home', () => {
  assert.throws(() => validateSelectedSource({
    role: 'runtime', selected: '/home/user/work/runtime', normal: '/home/user/work/runtime',
    normalState: state(), selectedState: state({ root: '/home/user/work/runtime' }),
  }), /per-request checkout/);
});

test('D66 refuses a selected source after the normal home advances', () => {
  assert.throws(() => validateSelectedSource({
    role: 'agent', selected: '/snapshot/agent', normal: '/home/user/work/agent',
    normalState: state({ head: 'c'.repeat(40), tree: 'd'.repeat(40) }), selectedState: state(),
  }), /not the current normal head/);
});

test('D66 refuses attached or dirty source checkouts', () => {
  assert.throws(() => validateSelectedSource({
    role: 'agent', selected: '/snapshot/agent', normal: '/home/user/work/agent',
    normalState: state(), selectedState: state({ branch: 'tl/integration' }),
  }), /must be detached/);
  assert.throws(() => validateSelectedSource({
    role: 'runtime', selected: '/snapshot/runtime', normal: '/home/user/work/runtime',
    normalState: state(), selectedState: state({ root: '/snapshot/runtime', dirty: true }),
  }), /dirty/);
});

test('D66 derives the supported detached route from the captured normal head', () => {
  assert.equal(exactCheckoutPath('app', 'c'.repeat(40)), '/home/user/work/wt/app-pin-cccccccc');
  assert.equal(exactCheckoutPath('agent', 'a'.repeat(40)), '/home/user/work/wt/agt-pin-aaaaaaaa');
  assert.equal(exactCheckoutPath('runtime', 'b'.repeat(40), '/tmp/checkouts'), '/tmp/checkouts/rt-pin-bbbbbbbb');
  assert.equal(exactCheckoutPath('composition', 'd'.repeat(40)), '/home/user/work/wt/vw-pin-dddddddd');
});

const pinned = (role, head, tree) => ({
  checkout: `/snapshot/${role}`, normal_home: `/home/user/work/${role}`,
  head, tree, state: state({ root: `/snapshot/${role}`, head, tree }),
});

test('D73 accepts one immutable four-repository tuple and does not consult moving normal heads', () => {
  const sources = {
    app: pinned('app', 'a'.repeat(40), '1'.repeat(40)),
    agent: pinned('agent', 'b'.repeat(40), '2'.repeat(40)),
    runtime: pinned('runtime', 'c'.repeat(40), '3'.repeat(40)),
    composition: pinned('composition', 'd'.repeat(40), '4'.repeat(40)),
  };
  assert.deepEqual(validatePinnedSources({ sources, appRootState: state({ tree: sources.app.tree }) }), sources);
  assert.throws(() => validatePinnedSources({ sources, appRootState: state({ head: 'f'.repeat(40), tree: sources.app.tree }) }), /App service source/);
  // A normal-home movement after this validation is irrelevant: launch uses the tuple above.
  assert.deepEqual(validatePinnedSource({ role: 'agent', selected: sources.agent.checkout,
    normal: sources.agent.normal_home, expectedHead: sources.agent.head, expectedTree: sources.agent.tree,
    selectedState: sources.agent.state }), {
    checkout: sources.agent.checkout, head: sources.agent.head, tree: sources.agent.tree, normal_home: sources.agent.normal_home,
  });
});

test('D73 refuses stale, missing, tampered, or wrong selected pins before any gesture can run', () => {
  const source = pinned('composition', 'd'.repeat(40), '4'.repeat(40));
  assert.throws(() => validatePinnedSource({ role: 'composition', selected: source.checkout,
    normal: source.normal_home, expectedHead: 'e'.repeat(40), expectedTree: source.tree, selectedState: source.state }), /does not match/);
  assert.throws(() => validatePinnedSource({ role: 'composition', selected: source.checkout,
    normal: source.normal_home, expectedHead: source.head, expectedTree: '5'.repeat(40), selectedState: source.state }), /does not match/);
  assert.throws(() => validatePinnedSource({ role: 'composition', selected: source.normal_home,
    normal: source.normal_home, expectedHead: source.head, expectedTree: source.tree, selectedState: source.state }), /per-request checkout/);
  assert.throws(() => validatePinnedSources({ sources: { app: source } }), /agent exact source is required/);
});

test('D73 service recipe carries full SHA/tree and all four exact checkout paths', () => {
  const pins = {
    app: { head: 'a'.repeat(40), tree: '1'.repeat(40) }, agent: { head: 'b'.repeat(40), tree: '2'.repeat(40) },
    runtime: { head: 'c'.repeat(40), tree: '3'.repeat(40) }, composition: { head: 'd'.repeat(40), tree: '4'.repeat(40) },
  };
  const recipe = serviceRecipe({ name: 'p3', target: 'app-P-D73', pins, checkouts: {
    app: '/snapshot/app', agent: '/snapshot/agent', runtime: '/snapshot/runtime', composition: '/snapshot/composition',
  } });
  for (const role of ['APP', 'AGENT', 'RUNTIME', 'COMPOSITION']) {
    assert.match(recipe, new RegExp(`D66_${role}_SHA='[a-f0-9]{40}'`));
    assert.match(recipe, new RegExp(`D66_${role}_TREE='[a-f0-9]{40}'`));
    assert.match(recipe, new RegExp(`D66_${role}_CHECKOUT='[^']+'`));
  }
  assert.doesNotMatch(recipe, /current normal|gesture|POST|publish/);
  assert.equal(serviceRecipe({ name: 'p3', pins, checkouts: {
    app: '/snapshot/app', agent: '/snapshot/agent', runtime: '/snapshot/runtime', composition: '/snapshot/composition',
  }, preflight: true }), `${recipe} --preflight`);
});

test('D78 service recipes select the Runtime watchdog only for the intended P2 route', () => {
  const pins = {
    app: { head: 'a'.repeat(40), tree: '1'.repeat(40) }, agent: { head: 'b'.repeat(40), tree: '2'.repeat(40) },
    runtime: { head: 'c'.repeat(40), tree: '3'.repeat(40) }, composition: { head: 'd'.repeat(40), tree: '4'.repeat(40) },
  };
  const checkouts = { app: '/snapshot/app', agent: '/snapshot/agent', runtime: '/snapshot/runtime', composition: '/snapshot/composition' };
  const watchdog = (name) => serviceRecipe({ name, pins, checkouts }).match(/ASTRID_P2_COMMIT_PHASE_CAPTURE_WATCHDOG_SECONDS='([^']*)'/)?.[1];
  assert.equal(watchdog('p2-element'), '2');
  assert.equal(watchdog('p2'), '20');
  assert.equal(watchdog('p1'), '');
  assert.equal(watchdog('p3'), '');
});

function runGit(directory, ...args) {
  return execFileSync('git', ['-C', directory, ...args], { encoding: 'utf8' }).trim();
}

function fixtureRepo(directory, name) {
  mkdirSync(directory, { recursive: true });
  runGit(directory, 'init', '-q');
  runGit(directory, 'config', 'user.email', 'd73@example.test');
  runGit(directory, 'config', 'user.name', 'D73 fixture');
  writeFileSync(path.join(directory, `${name}.txt`), `${name}\n`);
  if (name === 'app') {
    mkdirSync(path.join(directory, 'scripts/testing'), { recursive: true });
    writeFileSync(path.join(directory, 'scripts/testing/d66-plain-stack.mjs'), readFileSync(new URL('./d66-plain-stack.mjs', import.meta.url)));
  }
  runGit(directory, 'add', '.');
  runGit(directory, 'commit', '-qm', 'fixture');
  return { head: runGit(directory, 'rev-parse', 'HEAD'), tree: runGit(directory, 'rev-parse', 'HEAD^{tree}') };
}

function detachedFixture(normal, checkout) {
  execFileSync('git', ['clone', '-q', normal, checkout]);
  runGit(checkout, 'config', 'user.email', 'd73@example.test');
  runGit(checkout, 'config', 'user.name', 'D73 fixture');
  runGit(checkout, 'checkout', '--detach', '-q', 'HEAD');
}

test('D73 dry-preflight selects env paths and parses genuine checkout receipts before launch', () => {
  const base = mkdtempSync(path.join(os.tmpdir(), 'd73-preflight-'));
  const homes = Object.fromEntries(['app', 'agent', 'runtime', 'composition'].map((role) => [role, path.join(base, `${role}-normal`)]));
  const checkouts = Object.fromEntries(Object.keys(homes).map((role) => [role, path.join(base, `${role}-checkout`)]));
  const pins = Object.fromEntries(Object.entries(homes).map(([role, home]) => [role, fixtureRepo(home, role)]));
  for (const role of Object.keys(homes)) detachedFixture(homes[role], checkouts[role]);
  const env = Object.fromEntries(Object.keys(homes).flatMap((role) => [
    [`D66_${role.toUpperCase()}_SHA`, pins[role].head], [`D66_${role.toUpperCase()}_TREE`, pins[role].tree],
    [`D66_${role.toUpperCase()}_CHECKOUT`, `  ${checkouts[role]}  `],
  ]));
  const selected = selectPinnedSources(env, homes, checkouts.app);
  assert.deepEqual(Object.fromEntries(Object.entries(selected).map(([role, source]) => [role, source.checkout])), checkouts);
  writeFileSync(path.join(base, 'created-receipt'), `created ${checkouts.agent} (detached at ${pins.agent.head}, KEEP)\n`);
  writeFileSync(path.join(base, 'exists-receipt'), `exists: ${checkouts.runtime} at ${pins.runtime.head}\n`);
  assert.equal(receiptCheckout(path.join(base, 'created-receipt'), 'agent', pins.agent.head), checkouts.agent);
  assert.equal(receiptCheckout(path.join(base, 'exists-receipt'), 'runtime', pins.runtime.head), checkouts.runtime);
  assert.throws(() => selectPinnedSources({ ...env, D66_AGENT_CHECKOUT: checkouts.runtime }, homes, checkouts.app), /does not match/);
  const missingPinEnv = { ...env };
  delete missingPinEnv.D66_RUNTIME_TREE;
  assert.throws(() => selectPinnedSources(missingPinEnv, homes, checkouts.app), /runtime tree must be a full 40-character SHA/);
});

function serviceFixture() {
  const base = mkdtempSync(path.join(os.tmpdir(), 'd73-service-'));
  const roles = ['app', 'agent', 'runtime', 'composition'];
  const homes = Object.fromEntries(roles.map((role) => [role, path.join(base, `${role}-normal`)]));
  for (const role of roles) fixtureRepo(homes[role], role);
  const pins = captureSubmitPins(homes);
  const checkouts = Object.fromEntries(roles.map((role) => [role, exactCheckoutPath(role, pins[role].head, base)]));
  const receiptRoot = path.join(base, 'receipts');
  const workerRoot = path.join(base, 'workers');
  mkdirSync(receiptRoot);
  for (const role of roles) {
    detachedFixture(homes[role], checkouts[role]);
    const receipt = role === 'runtime'
      ? `exists: ${checkouts[role]} at ${pins[role].head}\n`
      : `created ${checkouts[role]} (detached at ${pins[role].head}, KEEP)\n`;
    writeFileSync(path.join(receiptRoot, `checkout-${role}-${pins[role].head}`), receipt);
  }
  const target = path.basename(checkouts.app);
  mkdirSync(path.join(workerRoot, target), { recursive: true });
  writeFileSync(path.join(workerRoot, target, 'meta'), `name=${target}\nrepo=app\nworktree=${checkouts.app}\n`);
  // Match bin/test-run: commit-tree <target tree> -p HEAD, then a detached worktree.
  const snapshot = path.join(base, '.test-fixture');
  const snapshotHead = runGit(checkouts.app, 'commit-tree', pins.app.tree, '-p', 'HEAD', '-m', 'test snapshot fixture');
  runGit(checkouts.app, 'worktree', 'add', '-q', '--detach', snapshot, snapshotHead);
  const env = Object.fromEntries(roles.flatMap((role) => [
    [`D66_${role.toUpperCase()}_SHA`, pins[role].head], [`D66_${role.toUpperCase()}_TREE`, pins[role].tree],
    [`D66_${role.toUpperCase()}_CHECKOUT`, checkouts[role]],
  ]));
  return { base, roles, homes, pins, checkouts, env, snapshot, snapshotHead, target, receiptRoot, workerRoot };
}

test('D73 verifies a real service snapshot, receipts and target after mutable homes move', async () => {
  const f = serviceFixture();
  const plan = buildSubmitPlan({ name: 'p1', paths: f.homes });
  assert.deepEqual(plan.pins, f.pins);
  assert.equal(plan.target, undefined);
  for (const role of f.roles) {
    writeFileSync(path.join(f.homes[role], `${role}.txt`), 'normal home advanced\n');
    runGit(f.homes[role], 'add', '.');
    runGit(f.homes[role], 'commit', '-qm', 'advance normal home');
  }
  const result = preflightSources(f.env, f.homes, f.snapshot, f);
  assert.equal(result.target, f.target);
  assert.equal(result.sources.app.head, f.pins.app.head);
  assert.equal(result.service_source.head, f.snapshotHead);
  assert.equal(result.service_source.tree, f.pins.app.tree);
  assert.deepEqual(result.service_source.parents, [f.pins.app.head]);
  assert.equal(preflightSources(f.env, f.homes, f.checkouts.app, f).service_source.head, f.pins.app.head);
  const checkoutRequests = f.roles.map((role) => ({ role, head: f.pins[role].head, checkout: f.checkouts[role],
    receipt: path.join(f.receiptRoot, `checkout-${role}-${f.pins[role].head}`) }));
  assert.deepEqual(await waitForSubmitReceipts({ pins: f.pins, checkoutRequests }, { waitMs: 0 }), f.checkouts);
});

test('D73 refuses same-tree worker finalization parents, grandparents, multiple parents and changed snapshot trees', () => {
  const f = serviceFixture();
  const finalized = runGit(f.checkouts.app, 'commit-tree', f.pins.app.tree, '-p', f.pins.app.head, '-m', 'worker finalization');
  const wrongTree = runGit(f.checkouts.agent, 'rev-parse', 'HEAD^{tree}');
  // Import only this tiny fixture tree into the App fixture object store.
  runGit(f.checkouts.app, 'fetch', '-q', f.checkouts.agent, 'HEAD');
  const cases = [
    [f.pins.app.tree, '-p', finalized],
    [f.pins.app.tree, '-p', f.pins.app.head, '-p', finalized],
    [f.pins.app.tree],
    [wrongTree, '-p', f.pins.app.head],
  ];
  for (const args of cases) {
    const head = runGit(f.checkouts.app, 'commit-tree', ...args, '-m', 'bad service snapshot');
    // Only HEAD changes; every same-tree counterexample has identical tracked files.
    runGit(f.snapshot, 'update-ref', '--no-deref', 'HEAD', head);
    assert.throws(() => preflightSources(f.env, f.homes, f.snapshot, f), /App service source/);
  }
  runGit(f.snapshot, 'update-ref', '--no-deref', 'HEAD', f.snapshotHead);
  runGit(f.checkouts.app, 'update-ref', '--no-deref', 'HEAD', finalized);
  assert.throws(() => preflightSources(f.env, f.homes, f.snapshot, f), /app source does not match its submit-time pin/);
});

test('D73 refuses wrong App selection, attached or dirty selected checkouts, and dirty service roots', () => {
  const f = serviceFixture();
  assert.throws(() => preflightSources({ ...f.env, D66_APP_CHECKOUT: f.snapshot }, f.homes, f.snapshot, f), /does not match its submit-time pin/);
  for (const role of f.roles) {
    runGit(f.checkouts[role], 'update-ref', 'refs/heads/d73-attached', f.pins[role].head);
    runGit(f.checkouts[role], 'symbolic-ref', 'HEAD', 'refs/heads/d73-attached');
    assert.throws(() => preflightSources(f.env, f.homes, f.snapshot, f), /must be detached/);
    runGit(f.checkouts[role], 'update-ref', '--no-deref', 'HEAD', f.pins[role].head);
    writeFileSync(path.join(f.checkouts[role], `${role}.txt`), 'dirty\n');
    assert.throws(() => preflightSources(f.env, f.homes, f.snapshot, f), /dirty/);
    writeFileSync(path.join(f.checkouts[role], `${role}.txt`), `${role}\n`);
  }
  writeFileSync(path.join(f.snapshot, 'app.txt'), 'dirty service root\n');
  assert.throws(() => preflightSources(f.env, f.homes, f.snapshot, f), /App service source is dirty/);
});

test('D73 refuses missing pins before checkout access, missing/wrong receipts and target metadata mismatches', () => {
  const f = serviceFixture();
  for (const role of f.roles) {
    for (const kind of ['SHA', 'TREE']) {
      const env = { ...f.env, D66_APP_CHECKOUT: '/unavailable/should-not-be-read' };
      delete env[`D66_${role.toUpperCase()}_${kind}`];
      assert.throws(() => preflightSources(env, f.homes, f.snapshot, f), /must be a full 40-character SHA/);
    }
  }
  assert.throws(() => preflightSources(f.env, f.homes, f.snapshot, { ...f, receiptRoot: path.join(f.base, 'missing-receipts') }), /ENOENT/);
  const receipt = path.join(f.receiptRoot, `checkout-agent-${f.pins.agent.head}`);
  writeFileSync(receipt, `exists: ${f.checkouts.runtime} at ${f.pins.agent.head}\n`);
  assert.throws(() => preflightSources(f.env, f.homes, f.snapshot, f), /receipt selected the wrong checkout/);
  writeFileSync(receipt, `exists: ${f.checkouts.agent} at ${f.pins.runtime.head}\n`);
  assert.throws(() => preflightSources(f.env, f.homes, f.snapshot, f), /receipt is missing or tampered/);
  assert.throws(() => appCheckoutTarget(f.checkouts.app, f.pins.app.head, { ...f, target: 'app-proof-worker' }), /stable exact App checkout/);
  writeFileSync(path.join(f.workerRoot, f.target, 'meta'), `name=${f.target}\nrepo=app\nworktree=${f.snapshot}\n`);
  assert.throws(() => appCheckoutTarget(f.checkouts.app, f.pins.app.head, f), /target metadata does not match/);
});

test('D73 preflight entrypoint records actual snapshot separately and stops before imports, build or collection', () => {
  const f = serviceFixture();
  const script = path.join(f.snapshot, 'scripts/testing/d66-plain-stack.mjs');
  const output = path.join(f.base, 'output');
  const invoke = (pins, mode = '--preflight') => spawnSync(process.execPath, ['--input-type=module', '-e', [
    `import { main } from ${JSON.stringify(script)};`,
    `process.argv = [process.execPath, ${JSON.stringify(script)}, 'p1', ${JSON.stringify(mode)}];`,
    `await main(${JSON.stringify({ receiptRoot: f.receiptRoot, workerRoot: f.workerRoot })});`,
  ].join('\n')], {
    cwd: f.snapshot, encoding: 'utf8', env: { ...process.env, ...pins, D66_OUTPUT_DIR: output,
      D66_NORMAL_AGENT_HOME: f.homes.agent, D66_NORMAL_RUNTIME_HOME: f.homes.runtime,
      D66_NORMAL_COMPOSITION_HOME: f.homes.composition,
      ASTRID_PYTHON: '/missing/no-python-in-preflight', ASTRID_RUNTIME_PYTHON: '/missing/no-python-in-preflight' },
  });
  // The fixture has no node_modules, build config or specs. Python paths deliberately do not exist.
  const result = invoke(f.env);
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /source preflight PASS/);
  const manifest = JSON.parse(readFileSync(path.join(output, 'manifest.json'), 'utf8'));
  assert.equal(manifest.repo_heads.app, f.pins.app.head);
  assert.equal(manifest.service_source.head, f.snapshotHead);
  assert.deepEqual(manifest.service_source.parents, [f.pins.app.head]);
  assert.equal(manifest.service_target, f.target);
  assert.equal(manifest.service_versions, undefined);
  const poisoned = invoke({ ...f.env, D66_RUNTIME_SHA: '' });
  assert.equal(poisoned.status, 1);
  assert.match(poisoned.stderr, /runtime SHA must be a full 40-character SHA/);
  assert.doesNotMatch(poisoned.stdout, /PASS/);
  const poisonedRun = invoke({ ...f.env, D66_RUNTIME_SHA: '' }, 'run');
  assert.equal(poisonedRun.status, 1);
  assert.match(poisonedRun.stderr, /runtime SHA must be a full 40-character SHA/);
});

function submitIo(f, waitStatuses = ['pass']) {
  const calls = [];
  let requestNumber = 0;
  let waitNumber = 0;
  const runCommand = async (file, args) => {
    calls.push({ type: path.basename(file), args });
    if (file.endsWith('request-test')) {
      requestNumber += 1;
      const id = `${args[1]}-${requestNumber}`;
      return { status: 0, stdout: `${f.base}/tests/${id}/\n`, stderr: '' };
    }
    return { status: 0, stdout: '', stderr: '' };
  };
  const runWait = async (args) => {
    calls.push({ type: 'wait-test', args });
    const status = waitStatuses[Math.min(waitNumber++, waitStatuses.length - 1)];
    return { status: status === 'timeout' ? 124 : status === 'pass' ? 0 : 1, stdout: '', stderr: '' };
  };
  return { calls, runCommand, runWait, readStatus: () => waitStatuses.at(-1) };
}

test('D73 --submit queues one preflight, waits it, then one normal request with the same tuple', async () => {
  const f = serviceFixture();
  const registryPath = path.join(f.base, 'suites.conf');
  const artifactPath = path.join(f.base, 'submit-plan.json');
  const original = Buffer.from('app existing-suite existing-command\n# preserve this comment\n');
  writeFileSync(registryPath, original);
  const io = submitIo(f);
  const order = [];
  const env = { ...f.env, D66_SUBMIT_SUITE: 'd73-submit-fixture', D66_OUTPUT_DIR: f.base };
  const options = { env, homes: f.homes, appRoot: f.snapshot, receiptRoot: f.receiptRoot,
    workerRoot: f.workerRoot, checkoutRoot: f.base, registryPath, runCommand: async (file, args) => {
      order.push(['command', path.basename(file), ...args]);
      return io.runCommand(file, args);
    }, runWait: async (args) => { order.push(['wait', ...args]); return io.runWait(args); }, readStatus: io.readStatus };
  const result = await submit('p1', options);
  assert.equal(result.preflight.id, 'd73-submit-fixture-preflight-1');
  assert.equal(result.normal.id, 'd73-submit-fixture-2');
  assert.deepEqual(order.slice(0, 6).map((entry) => entry[0]), ['command', 'command', 'command', 'command', 'command', 'wait']);
  assert.deepEqual(order.slice(-2).map((entry) => entry[0]), ['wait', 'command']);
  assert.deepEqual(order.at(-1).slice(2), [f.target, 'd73-submit-fixture', '--no-cache']);
  const registered = readFileSync(registryPath);
  assert.ok(registered.subarray(0, original.length).equals(original));
  assert.match(registered.toString(), /app d73-submit-fixture-preflight .* --preflight\napp d73-submit-fixture /s);
  assert.doesNotMatch(registered.toString(), /\$\{node\}/);

  const beforeRetry = order.length;
  await submit('p1', options);
  assert.equal(order.length, beforeRetry, 'a completed plan must not queue another original');
});

test('D73 --submit stops after a refused preflight and never queues the normal body', async () => {
  const f = serviceFixture();
  const registryPath = path.join(f.base, 'suites.conf');
  writeFileSync(registryPath, 'app existing-suite existing-command\n');
  const io = submitIo(f, ['fail']);
  const env = { ...f.env, D66_SUBMIT_SUITE: 'd73-submit-refused', D66_OUTPUT_DIR: f.base };
  await assert.rejects(() => submit('p1', { env, homes: f.homes, appRoot: f.snapshot, receiptRoot: f.receiptRoot,
    workerRoot: f.workerRoot, checkoutRoot: f.base, registryPath, runCommand: io.runCommand, runWait: io.runWait, readStatus: io.readStatus }), /preflight refused/);
  assert.equal(io.calls.filter((call) => call.type === 'request-test').length, 1);
  assert.equal(io.calls.filter((call) => call.type === 'request-test' && call.args[1] === 'd73-submit-refused').length, 0);
});

test('D73 timeout resumes the same preflight ID without duplicating either request', async () => {
  const f = serviceFixture();
  const registryPath = path.join(f.base, 'suites.conf');
  writeFileSync(registryPath, 'app existing-suite existing-command\n');
  const io = submitIo(f, ['timeout', 'pass']);
  const env = { ...f.env, D66_SUBMIT_SUITE: 'd73-submit-timeout', D66_OUTPUT_DIR: f.base };
  const result = await submit('p1', { env, homes: f.homes, appRoot: f.snapshot, receiptRoot: f.receiptRoot,
    workerRoot: f.workerRoot, checkoutRoot: f.base, registryPath, runCommand: io.runCommand, runWait: io.runWait, readStatus: io.readStatus });
  const waits = io.calls.filter((call) => call.type === 'wait-test');
  assert.deepEqual(waits.map((call) => call.args), [['d73-submit-timeout-preflight-1'], ['d73-submit-timeout-preflight-1']]);
  assert.equal(io.calls.filter((call) => call.type === 'request-test').length, 2);
  assert.equal(result.normal.id, 'd73-submit-timeout-2');
});

test('D79 serializes concurrent same-plan callers and preserves one normal ID across a 124 resume', async () => {
  const f = serviceFixture();
  const registryPath = path.join(f.base, 'suites.conf');
  writeFileSync(registryPath, 'app existing-suite existing-command\n');
  const io = submitIo(f);
  let releaseWait;
  let enteredWait;
  const waitEntered = new Promise((resolve) => { enteredWait = resolve; });
  const blocked = new Promise((resolve) => { releaseWait = resolve; });
  let waits = 0;
  const env = { ...f.env, D66_SUBMIT_SUITE: 'd79-submit-race', D66_OUTPUT_DIR: f.base };
  const options = {
    env, homes: f.homes, appRoot: f.snapshot, receiptRoot: f.receiptRoot,
    workerRoot: f.workerRoot, checkoutRoot: f.base, registryPath,
    runCommand: io.runCommand,
    runWait: async (args) => {
      waits += 1;
      if (waits === 1) {
        enteredWait();
        await blocked;
        io.calls.push({ type: 'wait-test', args });
        return { status: 124, stdout: '', stderr: '' };
      }
      return io.runWait(args);
    },
    readStatus: io.readStatus,
  };

  const first = submit('p1', options);
  await waitEntered;
  const second = submit('p1', options);
  await new Promise((resolve) => setImmediate(resolve));
  assert.equal(io.calls.filter((call) => call.type === 'request-test').length, 1,
    'the queued caller must not submit while the first caller owns the plan');
  releaseWait();
  const [firstResult, secondResult] = await Promise.all([first, second]);
  assert.equal(firstResult.normal.id, 'd79-submit-race-2');
  assert.equal(secondResult.normal.id, firstResult.normal.id);
  assert.deepEqual(io.calls.filter((call) => call.type === 'request-test').map((call) => call.args[1]), [
    'd79-submit-race-preflight', 'd79-submit-race',
  ]);
  assert.deepEqual(io.calls.filter((call) => call.type === 'wait-test').map((call) => call.args), [
    ['d79-submit-race-preflight-1'], ['d79-submit-race-preflight-1'],
  ]);
});

test('D73 registry registration refuses a concurrent outside-byte change', () => {
  const base = Buffer.from('app old old-command\n');
  let reads = 0;
  assert.throws(() => registerSubmitRecipes({ registryPath: '/tmp/d73-registry-fixture', rows: [
    'app d73-preflight preflight-command', 'app d73-normal normal-command'],
  readRegistry: () => (reads++ === 0 ? base : Buffer.from(`${base}app concurrent changed\n`)), writeRegistry: () => assert.fail('must not write after a concurrent change') }), /changed concurrently/);
});
