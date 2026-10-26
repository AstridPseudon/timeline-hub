#!/usr/bin/env node
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { existsSync } from 'node:fs';
import { writeFile } from 'node:fs/promises';

const evidence = new URL('.', import.meta.url).pathname;
const appRepo = '/home/user/banodoco/reigh-app';
const appCommit = '04545a1e52c58a5fa938cb4aa0a060328e8d3efc';
const appTree = '0429c1f57f5d4244d722a59285140451dcf571cb';
const candidateCheckout = '/home/user/work/wt/app-pin-04545a1e';
const runtimeCheckout = '/home/user/work/wt/rt-pin-95d98f03';
const helperPath = `${runtimeCheckout}/tests/helpers/p2_commit_phase_capture.py`;
const helperSha256 = '095c252b111a6d43cb5b4b9ed284b5a445b8b6fe69ca0ad4ee6950f1383c352d';
const expectedOccurrenceId = 'f2-occurrence-copy';
const observationEnv = `TIMELINE_D141J_VISIBILITY_CAPTURE='${JSON.stringify({ expectedOccurrenceId })}'`;

const tuple = {
  app: { repo: appRepo, sha: appCommit, tree: appTree, checkout: candidateCheckout, materialized: false },
  agent: {
    repo: '/home/user/peteromallet/astrid-agent',
    sha: 'ecdc242ed9b673f641759ecf029f95e89a2c6f92',
    tree: 'd362fe9dfdbd0c1fc8e0739c193ed2b74a7d2735',
    checkout: '/home/user/work/wt/agt-pin-ecdc242e',
  },
  runtime: {
    repo: '/home/user/banodoco/banodoco-workspace-runtime',
    sha: '95d98f038320d5d46bd679ac000ab3e15825c935',
    tree: '78df31d62c5b9ba4c84dee4ea346e43a767718c1',
    checkout: runtimeCheckout,
  },
  composition: {
    repo: '/home/user/work/wt/app-P-D141j-final-route-source-1326',
    sha: '635f4de06fda22a85fc2e4cfc764d0153a4c9f40',
    tree: '5ab5191a296980a0a6bcd1178ab6902d6478a148',
    checkout: '/home/user/work/wt/vw-pin-635f4de0',
  },
};

const blobs = [
  ['builder', 'scripts/testing/d66-plain-stack.mjs', 49914, '2032f3087faab5bc1037b54faa593cb32536de15b748809601731ad5f6a7602f'],
  ['popup_spec', 'tests/e2e/local/three-products.p2-popup.spec.ts', 54668, '09f5e2c2ea2a207575534a88adf2847d68cdd389caa5d145580100f21302b2b9'],
  ['fixture_app', 'tests/e2e/local/support/app.ts', 26369, '6e9cd5a23c0b25f60de16bad266b75e9d2b5c2ee6f3cab39ae324fb1873ffbbc'],
  ['fixture_capture', 'tests/e2e/local/support/d141j-visibility.ts', 5689, '97cb782069904555f66ce389edc344076a533497a388c6117c03b4463e1d5dce'],
  ['capture_controls', 'tests/e2e/local/support/d141j-visibility.test.ts', 10279, '1bc23a1797a42a66481aeeb10246674575c7aeeb3d5b8662cfbe53e8c3881777'],
  ['collector', 'src/tools/video-editor/diagnostics/d141jVisibilityObservation.ts', 6308, '504088ca11b9522f39e38328cfcd636f621768387c4dc2b5c461a76ab9856e56'],
  ['checker', 'scripts/testing/check-d141j-visibility.mjs', 5985, 'bd5feadba07f6cdec3afa4d12baa3008cfd9bd012fdb9db6895d34e3db5baa27'],
  ['accepted_read_emitter', 'src/tools/video-editor/adapters/app/useAstridShotsHost.ts', 16733, '59c1982900d564564487fb871527ac92e7b80e61350793ac36491ccaf3e8ffdf'],
  ['active_occurrences_emitter', 'src/tools/video-editor/hooks/useShotGroups.ts', 15272, 'f8545d3e1decc55a5d84a35ba2ef68fc63dd221789be18a1cd2537a8f334207e'],
  ['overlay_emitter', 'src/tools/video-editor/components/TimelineEditor/TimelineEditorCore.tsx', 39334, '555526c695eafb2d6436344e31ce6a824b10932e1c48f40a40ec97d334adda44'],
  ['control_test', 'src/tools/video-editor/components/TimelineEditor/TimelineEditorCore.test.tsx', 28085, '4f9ed3c617ecbd4619b233960053e0e571ad00e6dea7a108226d9aab584e4a07'],
  ['install_manifest', 'public/install-manifest.json', 4765, '47e89fbe576a1c118b074a9fb5ef7d8b5eb788405d5537a9808d1b8279f28e41'],
  ['build_inputs_manifest', 'vendor/astrid-build-inputs/manifest.json', 18726, '5cedfb8b544b73dc0db769e45ba19740de61b5296aca107fbb550185f58ee2df'],
];

function git(repo, args) {
  return execFileSync('git', ['-C', repo, ...args], { encoding: 'utf8' }).trim();
}

function show(repo, rev, path) {
  return execFileSync('git', ['-C', repo, 'show', `${rev}:${path}`]);
}

function sha(bytes) {
  return createHash('sha256').update(bytes).digest('hex');
}

function shellQuote(value) {
  return `'${String(value).replaceAll("'", "'\\''")}'`;
}

function builderModule(source) {
  // The source is loaded from the immutable git blob. Only the module's root
  // locator is replaced so a data URL can call its pure exports; no recipe
  // logic or source bytes are rewritten.
  const rootLine = "const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');";
  const replacement = "const root = '/home/user/banodoco/reigh-app';";
  if (!source.toString().includes(rootLine)) throw new Error('builder root locator changed');
  const runnable = source.toString().replace(rootLine, replacement)
    .replaceAll('fileURLToPath(import.meta.url)', "'/never-run/d66-plain-stack.mjs'");
  return import(`data:text/javascript;charset=utf-8,${encodeURIComponent(runnable)}`);
}

function checkTuple() {
  return Object.fromEntries(Object.entries(tuple).map(([role, source]) => {
    const actualTree = git(source.repo, ['show', '-s', '--format=%T', source.sha]);
    if (actualTree !== source.tree) throw new Error(`${role} tree mismatch: ${actualTree}`);
    return [role, { ...source, verified: true }];
  }));
}

function checkBlobs() {
  return Object.fromEntries(blobs.map(([name, path, bytes, expectedSha]) => {
    const data = show(appRepo, appCommit, path);
    const actual = sha(data);
    if (data.length !== bytes || actual !== expectedSha) throw new Error(`${name} blob mismatch`);
    return [name, { path, bytes, sha256: actual, git_blob: git(appRepo, ['rev-parse', `${appCommit}:${path}`]) }];
  }));
}

function checkRuntimeHelper() {
  const data = show(tuple.runtime.repo, tuple.runtime.sha, 'tests/helpers/p2_commit_phase_capture.py');
  if (data.length !== 67914 || sha(data) !== helperSha256) throw new Error('runtime helper blob mismatch');
  return { path: helperPath, bytes: data.length, sha256: sha(data), git_blob: git(tuple.runtime.repo, ['rev-parse', `${tuple.runtime.sha}:tests/helpers/p2_commit_phase_capture.py`]) };
}

function parseAssignments(recipe) {
  const assignments = {};
  for (const match of recipe.matchAll(/(?:^| )([A-Z][A-Z0-9_]*)='((?:[^']|'\\'')*)'/g)) {
    assignments[match[1]] = match[2].replaceAll("'\\''", "'");
  }
  return assignments;
}

function commandParts(recipe, withObservation) {
  const full = withObservation ? `${observationEnv} ${recipe}` : recipe;
  const marker = "'/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node'";
  const index = full.indexOf(marker);
  if (index < 0) throw new Error('node command missing from recipe');
  const envText = full.slice(0, index).trim();
  const commandText = full.slice(index).replaceAll("'", '');
  const parts = commandText.split(/\s+/);
  return { full, env: { ...parseAssignments(envText), TIMELINE_D141J_VISIBILITY_CAPTURE: JSON.stringify({ expectedOccurrenceId }) }, argv: parts, envText };
}

export async function compose() {
  const builder = show(appRepo, appCommit, 'scripts/testing/d66-plain-stack.mjs');
  if (sha(builder) !== '2032f3087faab5bc1037b54faa593cb32536de15b748809601731ad5f6a7602f') throw new Error('builder source hash mismatch');
  const mod = await builderModule(builder);
  const pins = Object.fromEntries(Object.entries(tuple).map(([role, source]) => [role, { head: source.sha, tree: source.tree }]));
  const checkouts = Object.fromEntries(Object.entries(tuple).map(([role, source]) => [role, source.checkout]));
  const plan = mod.buildSubmitPlan({
    name: 'p2-popup-add', target: 'app-pin-04545a1e', pins, checkouts,
    checkoutRoot: '/home/user/work/wt', receiptRoot: '/tmp/route-receipts',
  });
  const diagnosticHelper = { path: helperPath, sha256: helperSha256 };
  const normal = mod.serviceRecipe({ name: 'p2-popup-add', pins: plan.pins, checkouts: plan.checkouts, diagnosticHelper });
  const preflight = mod.serviceRecipe({ name: 'p2-popup-add', pins: plan.pins, checkouts: plan.checkouts, diagnosticHelper, preflight: true });
  if (Buffer.byteLength(normal) !== 1172) throw new Error('normal recipe byte count changed');
  if (sha(Buffer.from(normal)) !== 'dbfb3788c869f5f1e2a1e6e6f967305c5aa714c94185f021ec1861db43314f78') throw new Error('normal recipe hash changed');
  if (Buffer.byteLength(preflight) !== 1184) throw new Error('preflight recipe byte count changed');
  if (sha(Buffer.from(preflight)) !== '5532be8f9ce5df340fa60813fe3a31794da8cd0948909832aacfde1752c0dd6b') throw new Error('preflight recipe hash changed');
  if (normal.includes('TIMELINE_D141J_VISIBILITY_CAPTURE')) throw new Error('normal builder recipe was edited');
  const sourceManifest = {
    schema: 'timeline.app.d141j.final-route-source-manifest.v1',
    status: 'PROSPECTIVE_NATIVE_ROUTE_NOTRUN',
    registration: false,
    candidate: { commit: appCommit, tree: appTree, checkout: candidateCheckout, materialized: false, source_qualification: 'reviewed-private-pending-manager-checkout' },
    tuple: checkTuple(),
    source_blobs: checkBlobs(),
    runtime_helper: checkRuntimeHelper(),
    protected_unchanged: [
      'tests/e2e/local/three-products.p2-popup.spec.ts',
      'src/tools/video-editor/diagnostics/d141jVisibilityObservation.ts',
      'src/tools/video-editor/adapters/app/useAstridShotsHost.ts',
      'src/tools/video-editor/hooks/useShotGroups.ts',
      'src/tools/video-editor/components/TimelineEditor/TimelineEditorCore.tsx',
      'scripts/testing/check-d141j-visibility.mjs',
    ],
    original_proof_tuple: {
      app: { sha: '82e9e13ddf1d7ec6c736521b2eb091dca9877598', tree: '6a6e49eb4461b5ca1a7fa1247653bc794f26d710' },
      agent: { sha: 'ecdc242ed9b673f641759ecf029f95e89a2c6f92', tree: 'd362fe9dfdbd0c1fc8e0739c193ed2b74a7d2735' },
      runtime: { sha: '95d98f038320d5d46bd679ac000ab3e15825c935', tree: '78df31d62c5b9ba4c84dee4ea346e43a767718c1' },
      composition: { sha: '635f4de06fda22a85fc2e4cfc764d0153a4c9f40', tree: '5ab5191a296980a0a6bcd1178ab6902d6478a148' },
    },
  };
  const route = {
    schema: 'timeline.app.d141j.final-route.v1',
    route_status: 'NOTRUN_FINITE_NATIVE_PENDING_CHECKOUT',
    cause: 'UNKNOWN',
    registration: false,
    candidate: sourceManifest.candidate,
    expected_occurrence_id: expectedOccurrenceId,
    observation_env: observationEnv,
    normal_recipe: { bytes: Buffer.byteLength(normal), sha256: sha(Buffer.from(normal)), text: normal },
    preflight_recipe: { bytes: Buffer.byteLength(preflight), sha256: sha(Buffer.from(preflight)), text: preflight },
    future_native_invocation: {
      cwd: candidateCheckout,
      argv: ['/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node', '--max-old-space-size=6144', '--import', 'tsx', 'scripts/testing/d66-plain-stack.mjs', 'p2-popup-add'],
      env_prefix: observationEnv,
      command: `${observationEnv} ${normal}`,
      target: 'app-pin-04545a1e',
    },
    future_preflight_invocation: { cwd: candidateCheckout, argv: ['/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node', '--max-old-space-size=6144', '--import', 'tsx', 'scripts/testing/d66-plain-stack.mjs', 'p2-popup-add', '--preflight'], env_prefix: observationEnv, command: `${observationEnv} ${preflight}`, target: 'app-pin-04545a1e' },
    output: {
      d66_output_root: '/tmp/d66-p2-popup-add',
      d66_manifest: '/tmp/d66-p2-popup-add/manifest.json',
      artifact_relative_path: 'testInfo.outputPath(\'d141j-visibility.json\')',
      attachment_name: 'd141j-visibility.json',
      checker: '/home/user/work/wt/app-pin-04545a1e/scripts/testing/check-d141j-visibility.mjs',
      keep_on: ['PASS', 'FAIL', 'timeout', 'interrupted'],
    },
    gates: { disk_admission_bytes: 5.2 * 1024 ** 3, disk_stop_bytes: 4 * 1024 ** 3, heavy_jobs: 1, native_seconds: 5, test_keep_before_queues: true, floor_scope: 'ordinary-own-source-only' },
    side_effects: { request_test: false, wait_test: false, row_cas: false, registration: false, checkout: false, install: false, browser: false, request: false, collection: false, body: false, native: false },
  };
  const sourceMap = {
    schema: 'timeline.app.d141j.final-route-source-map.v1',
    candidate: { commit: appCommit, tree: appTree },
    occurrence_derivation: 'tests/e2e/local/three-products.p2-popup.spec.ts:273-283 assigns sharedOccurrenceId=f2-occurrence-copy; :943 selects the unchanged data-clip-id selector.',
    popup_case: 'tests/e2e/local/three-products.p2-popup.spec.ts:941-946',
    selector: '.clip-action[data-clip-id="f2-occurrence-copy:f2-agent-clip"]',
    fixture_config: 'tests/e2e/local/support/app.ts:34-50',
    fixture_wrapper: 'tests/e2e/local/support/app.ts:62-72',
    page_fixture_assignment: 'tests/e2e/local/support/app.ts:207-215',
    collector_install: 'tests/e2e/local/support/d141j-visibility.ts:35-59,104-112',
    retention: 'tests/e2e/local/support/d141j-visibility.ts:121-146',
    output_path: 'testInfo.outputPath(\'d141j-visibility.json\') then testInfo.attach(\'d141j-visibility.json\', ...)',
    source_events: {
      accepted_read: 'useAstridShotsHost.ts:210-216',
      active_occurrences: 'useShotGroups.ts:188',
      useShotGroups_input_result: 'useShotGroups.ts:273,336',
      overlay: 'TimelineEditorCore.tsx:931',
    },
    checker: 'scripts/testing/check-d141j-visibility.mjs:20-109',
    d66_builder: 'scripts/testing/d66-plain-stack.mjs:361-395,638-695',
    d66_env_propagation: 'scripts/testing/d66-plain-stack.mjs:748-765,781-795; playwrightLaunchEnv spreads baseEnv and does not delete TIMELINE_D141J_VISIBILITY_CAPTURE',
  };
  await writeFile(`${evidence}/route.json`, `${JSON.stringify(route, null, 2)}\n`);
  await writeFile(`${evidence}/source-manifest.json`, `${JSON.stringify(sourceManifest, null, 2)}\n`);
  await writeFile(`${evidence}/source-map.json`, `${JSON.stringify(sourceMap, null, 2)}\n`);
  return { route, sourceManifest, sourceMap, normal, preflight, plan };
}

if (process.argv[1] && process.argv[1].endsWith('pure-route-control.mjs')) {
  const result = await compose();
  console.log(JSON.stringify({ status: 'PASS_PURE_PROSPECTIVE_ONLY', normal_bytes: result.route.normal_recipe.bytes, normal_sha256: result.route.normal_recipe.sha256, candidate_checkout_materialized: existsSync(candidateCheckout) }, null, 2));
}
