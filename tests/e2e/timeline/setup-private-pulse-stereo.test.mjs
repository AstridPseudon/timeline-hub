import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {
  chmodSync,
  existsSync,
  mkdirSync,
  mkdtempSync,
  readFileSync,
  rmSync,
  writeFileSync,
} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {test} from 'node:test';
import {
  NODE_EXECUTABLE,
  NODE_EXECUTABLE_SHA256,
  WORKER_STATE_ROOT,
} from './tab-audio-capture.controller.mjs';

const setupSource = join(import.meta.dirname, 'setup-private-pulse-stereo.sh');
const PINNED_NODE_RUNTIME = {version: 'v20.19.4', execPath: NODE_EXECUTABLE};
const LIVE_FLAGS = [
  'TAB_AUDIO_RUN',
  'TAB_AUDIO_PREFLIGHT_PATH',
  'TAB_AUDIO_RUN_MARKER',
  'TAB_AUDIO_GRANT_PATH',
  'PLAYWRIGHT_OUTPUT_DIR',
  'TAB_AUDIO_LOCK_PATH',
  'PRIVATE_PULSE_STATE_ROOT',
];

function assertPinnedNode() {
  assert.equal(createHash('sha256').update(readFileSync(NODE_EXECUTABLE)).digest('hex'), NODE_EXECUTABLE_SHA256);
}

function writeExecutable(path, source) {
  writeFileSync(path, source, {mode: 0o700});
  chmodSync(path, 0o700);
}

function createFixture() {
  const root = mkdtempSync(join(tmpdir(), 'setup-private-pulse-behavior-'));
  const timeline = join(root, 'tests/e2e/timeline');
  const nodeModules = join(root, 'node_modules');
  const guardBin = join(root, 'guard-bin');
  const recordPath = join(root, 'controller-record.ndjson');
  const daemonMarker = join(root, 'daemon-started');
  const browserMarker = join(root, 'browser-started');
  const lockPath = join(root, 'unit-browser.lock');
  mkdirSync(timeline, {recursive: true});
  mkdirSync(join(nodeModules, 'playwright'), {recursive: true});
  mkdirSync(guardBin);

  writeExecutable(join(timeline, 'setup-private-pulse-stereo.sh'), readFileSync(setupSource));
  const controllerStub = `
import {appendFileSync} from 'node:fs';

const kind = process.argv[1].endsWith('private-pulse-stereo.controller.mjs') ? 'private' : 'base';
const args = process.argv.slice(2);
const keys = [
  'TAB_AUDIO_RUN',
  'TAB_AUDIO_GRANT_PATH',
  'TAB_AUDIO_PREFLIGHT_PATH',
  'TAB_AUDIO_RUN_MARKER',
  'PLAYWRIGHT_OUTPUT_DIR',
];
const environment = Object.fromEntries(keys.map((key) => [key, process.env[key] ?? null]));
appendFileSync(process.env.SETUP_STUB_RECORD, JSON.stringify({kind, args, environment,
  runtime: {version: process.version, execPath: process.execPath}}) + '\\n');
if (kind === 'base' && args[0] === '--preflight') process.exit(23);
`;
  writeFileSync(join(timeline, 'private-pulse-stereo.controller.mjs'), controllerStub);
  writeFileSync(join(timeline, 'tab-audio-capture.controller.mjs'), controllerStub);
  writeFileSync(join(nodeModules, 'playwright', 'cli.js'), `
import {writeFileSync} from 'node:fs';
writeFileSync(process.env.SETUP_BROWSER_MARKER, 'browser invoked');
`);
  writeExecutable(join(guardBin, 'pulseaudio'), `#!/usr/bin/env bash
set -eu
printf 'daemon invoked' > "$SETUP_DAEMON_MARKER"
`);
  writeExecutable(join(guardBin, 'chown'), `#!/usr/bin/env bash
exit 0
`);

  return {
    root,
    setup: join(timeline, 'setup-private-pulse-stereo.sh'),
    recordPath,
    daemonMarker,
    browserMarker,
    lockPath,
    guardBin,
  };
}

function withFixture(callback) {
  const fixture = createFixture();
  try {
    return callback(fixture);
  } finally {
    rmSync(fixture.root, {recursive: true, force: true});
  }
}

function runSetup(fixture, overrides = {}) {
  const environment = {...process.env};
  for (const key of LIVE_FLAGS) delete environment[key];
  Object.assign(environment, {
    PATH: `${fixture.guardBin}:${process.env.PATH}`,
    TAB_AUDIO_NODE_EXECUTABLE: NODE_EXECUTABLE,
    SETUP_STUB_RECORD: fixture.recordPath,
    SETUP_DAEMON_MARKER: fixture.daemonMarker,
    SETUP_BROWSER_MARKER: fixture.browserMarker,
    ...overrides,
  });
  return spawnSync('bash', [fixture.setup], {
    env: environment,
    encoding: 'utf8',
    timeout: 10_000,
    maxBuffer: 1024 * 1024,
  });
}

function records(fixture) {
  if (!existsSync(fixture.recordPath)) return [];
  return readFileSync(fixture.recordPath, 'utf8').trim().split('\n').filter(Boolean).map(JSON.parse);
}

function livePaths() {
  const runRoot = mkdtempSync(join(WORKER_STATE_ROOT, 'setup-private-pulse-test-'));
  const pulseStateRoot = mkdtempSync(join(tmpdir(), 'setup-private-pulse-state-'));
  const path = (name) => join(runRoot, name);
  return {
    runRoot,
    pulseStateRoot,
    preflight: path('preflight.json'),
    marker: path('run.marker'),
    grant: path('strictgrant.json'),
    output: path('playwright-output'),
  };
}

function removeLivePaths(paths) {
  rmSync(paths.runRoot, {recursive: true, force: true});
  rmSync(paths.pulseStateRoot, {recursive: true, force: true});
}

test('pure prepare receives neither live-run nor grant state', () => {
  assertPinnedNode();
  withFixture((fixture) => {
    const paths = livePaths();
    try {
      const result = runSetup(fixture, {
        TAB_AUDIO_RUN: '0',
        TAB_AUDIO_PREFLIGHT_PATH: paths.preflight,
        TAB_AUDIO_RUN_MARKER: paths.marker,
        TAB_AUDIO_GRANT_PATH: paths.grant,
        PLAYWRIGHT_OUTPUT_DIR: paths.output,
        TAB_AUDIO_LOCK_PATH: fixture.lockPath,
        PRIVATE_PULSE_STATE_ROOT: paths.pulseStateRoot,
      });

      assert.equal(result.status, 0, result.stderr);
      assert.match(result.stdout, /Offline preflight only/);
      assert.deepEqual(records(fixture), [{
        kind: 'private',
        args: ['--prepare'],
        runtime: PINNED_NODE_RUNTIME,
        environment: {
          TAB_AUDIO_RUN: null,
          TAB_AUDIO_GRANT_PATH: null,
          TAB_AUDIO_PREFLIGHT_PATH: paths.preflight,
          TAB_AUDIO_RUN_MARKER: paths.marker,
          PLAYWRIGHT_OUTPUT_DIR: paths.output,
        },
      }]);
    } finally {
      removeLivePaths(paths);
    }
  });
});

test('live preflight keeps the original strict grant after private preparation', () => {
  assertPinnedNode();
  withFixture((fixture) => {
    const paths = livePaths();
    try {
      const result = runSetup(fixture, {
        TAB_AUDIO_RUN: '1',
        TAB_AUDIO_PREFLIGHT_PATH: paths.preflight,
        TAB_AUDIO_RUN_MARKER: paths.marker,
        TAB_AUDIO_GRANT_PATH: paths.grant,
        PLAYWRIGHT_OUTPUT_DIR: paths.output,
        TAB_AUDIO_LOCK_PATH: fixture.lockPath,
        PRIVATE_PULSE_STATE_ROOT: paths.pulseStateRoot,
      });

      assert.equal(result.status, 23, result.stderr);
      assert.deepEqual(records(fixture), [
        {
          kind: 'private',
          args: ['--prepare'],
          runtime: PINNED_NODE_RUNTIME,
          environment: {
            TAB_AUDIO_RUN: null,
            TAB_AUDIO_GRANT_PATH: null,
            TAB_AUDIO_PREFLIGHT_PATH: paths.preflight,
            TAB_AUDIO_RUN_MARKER: paths.marker,
            PLAYWRIGHT_OUTPUT_DIR: paths.output,
          },
        },
        {
          kind: 'base',
          args: ['--preflight'],
          runtime: PINNED_NODE_RUNTIME,
          environment: {
            TAB_AUDIO_RUN: '1',
            TAB_AUDIO_GRANT_PATH: paths.grant,
            TAB_AUDIO_PREFLIGHT_PATH: paths.preflight,
            TAB_AUDIO_RUN_MARKER: paths.marker,
            PLAYWRIGHT_OUTPUT_DIR: paths.output,
          },
        },
      ]);
      assert.equal(existsSync(fixture.daemonMarker), false);
      assert.equal(existsSync(fixture.browserMarker), false);
    } finally {
      removeLivePaths(paths);
    }
  });
});

for (const invalidName of ['TAB_AUDIO_PREFLIGHT_PATH', 'TAB_AUDIO_RUN_MARKER', 'TAB_AUDIO_GRANT_PATH', 'PLAYWRIGHT_OUTPUT_DIR']) {
  test(`out-of-scope ${invalidName} refuses before controllers, daemon, or browser`, () => {
    assertPinnedNode();
    withFixture((fixture) => {
      const paths = livePaths();
      try {
        const values = {
          TAB_AUDIO_RUN: '1',
          TAB_AUDIO_PREFLIGHT_PATH: join(paths.runRoot, 'preflight.json'),
          TAB_AUDIO_RUN_MARKER: join(paths.runRoot, 'run.marker'),
          TAB_AUDIO_GRANT_PATH: join(paths.runRoot, 'strictgrant.json'),
          PLAYWRIGHT_OUTPUT_DIR: join(paths.runRoot, 'playwright-output'),
          TAB_AUDIO_LOCK_PATH: fixture.lockPath,
          PRIVATE_PULSE_STATE_ROOT: paths.pulseStateRoot,
        };
        values[invalidName] = join(tmpdir(), `outside-${invalidName.toLowerCase()}`);

        const result = runSetup(fixture, values);

        assert.equal(result.status, 2, result.stderr);
        assert.deepEqual(records(fixture), []);
        assert.equal(existsSync(fixture.daemonMarker), false);
        assert.equal(existsSync(fixture.browserMarker), false);
      } finally {
        removeLivePaths(paths);
      }
    });
  });
}
