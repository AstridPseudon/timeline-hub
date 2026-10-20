import assert from 'node:assert/strict';
import {test} from 'node:test';
import {readFileSync} from 'node:fs';
import {dirname, join} from 'node:path';
import {createRequire} from 'node:module';
import {BROWSER_EXECUTABLE, EXPECTED_PACKAGE_VERSIONS, FROZEN_PRIVATE_GRAPH, REPO_ROOT, TASK_TEMP_PREFIX, TASK_TEMP_ROOT, hashTree, packageGraphFingerprint, renderGraphFingerprint} from './tab-audio-capture.controller.mjs';

test('package graph fingerprint collects every package with an expected version', () => {
  const {packages} = packageGraphFingerprint();

  for (const [name, version] of Object.entries(EXPECTED_PACKAGE_VERSIONS)) {
    assert.equal(packages[name]?.version, version, `${name} must be collected at its expected version`);
  }
});

test('render graph fingerprint resolves the package root and all frozen files', () => {
  assert.deepEqual(renderGraphFingerprint(), {
    '@remotion/player/dist/cjs/PlayerUI.js': '5dc9b4b89310609f57a718c641334d530b72ecf284fc1682610afcec208a4fbb',
    '@remotion/player/dist/cjs/use-player-methods.js': 'ff50ab8b4ae86423fab18aa1ecf6c48c41501c4f7b527f05a55c2c36598def46',
    '@remotion/player/dist/cjs/use-playback.js': '6c8369a19d7a29eab5dab4642799172d4f2a7e11dad39125edcb673ec5729fb0',
    '@remotion/player/dist/esm/index.mjs': 'd3ef9728584c78e0e01cdb71ad72e3c6ddb36f96bfef90a4231d8b795e906b12',
    'remotion/dist/esm/index.mjs': '5a1584f7660fa8fffa7eb8fe016b82a4d719e67d4b7904d4fa4f299eb1355f28',
    'remotion/dist/cjs/audio/shared-audio-tags.js': '949ccec3419398183e8e22f63820a4a57cb8379befb184fbac9a3acde040c5b8',
  });
});

test('browser and Playwright trees retain their exact frozen hashes', () => {
  if (!FROZEN_PRIVATE_GRAPH) throw new Error('Private graph is not READY');
  assert.deepEqual(hashTree(dirname(BROWSER_EXECUTABLE)), {
    sha256: '5b9b48fad617dc414d4a18ccfe9c7933c7bc4a8efd78c70d4f7a9e853808de0e',
    fileCount: 255,
  });
  const require = createRequire(join(FROZEN_PRIVATE_GRAPH.root, '../package.json'));
  const playwrightRoot = dirname(require.resolve('playwright-core/package.json'));
  assert.deepEqual(hashTree(playwrightRoot), {
    sha256: '6a78060c81886b7ba6f631d5b1193d50f0362c779f5b2dff2d784a31a6acc46d',
    fileCount: 106,
  });
});

test('launcher binds one fresh short task temp and cleans it after every attempt', () => {
  const setup = readFileSync(join(REPO_ROOT, 'tests/e2e/timeline/setup-tab-audio-capture.sh'), 'utf8');

  assert.match(setup, new RegExp(`mktemp -d ${TASK_TEMP_ROOT}/${TASK_TEMP_PREFIX}XXXXXX`));
  assert.match(setup, /unset TAB_AUDIO_TASK_TMPDIR/);
  assert.match(setup, /TASK_TMPDIR_ID=''/);
  assert.match(setup, /TASK_TMPDIR_ID=\$\(stat -c/);
  assert.match(setup, /trap cleanup EXIT/);
  assert.match(setup, /cleanup_task_tmpdir \"\$TASK_TMPDIR\"/);
  assert.match(setup, /TAB_AUDIO_TASK_TMPDIR=\"\$TASK_TMPDIR\"/);
  assert.match(setup, /TMPDIR=\"\$TASK_TMPDIR\" TMP=\"\$TASK_TMPDIR\" TEMP=\"\$TASK_TMPDIR\"/);
  assert.doesNotMatch(setup, /export HOME=|PULSE_SERVER=|PULSE_RUNTIME_PATH=/);
});
