import assert from 'node:assert/strict';
import { existsSync, mkdirSync, mkdtempSync, rmSync, symlinkSync, writeFileSync, realpathSync } from 'node:fs';
import path from 'node:path';

export const DISCOVERY_SUMMARY = 'discovered exactly 5 current native-codec-chrome155 parity cases';

export function assertDiscoverySummary(discovery) {
  assert.equal(discovery, DISCOVERY_SUMMARY, 'frozen discover() return contract changed');
  return discovery;
}

function caseSource({ count = 5, renameLast = false } = {}) {
  const names = [
    'normal App Render action downloads',
    'fixture readiness seeks',
    'compares native-size actual Player frames',
    'captures the actual Player page as one native-PTS VP8/Opus tab stream',
    renameLast ? 'picture-only renamed case' : 'picture-only one-host patch',
  ];
  return [
    "import { test } from '@playwright/test';",
    ...names.slice(0, count).map(name => `test('${name}', () => {});`),
    '',
  ].join('\n');
}

function link(source, destination) {
  mkdirSync(path.dirname(destination), { recursive: true });
  symlinkSync(source, destination);
}

function makeDiscoveryFixture(appRoot, options) {
  const root = mkdtempSync(path.join(path.dirname(new URL(import.meta.url).pathname), 'discovery-controls-'));
  assert.equal(realpathSync(root), root, 'discovery control root must be canonical');
  link(path.join(appRoot, 'node_modules'), path.join(root, 'node_modules'));
  writeFileSync(path.join(root, 'playwright.viewing-parity.native-codec.config.ts'), [
    "import { defineConfig } from '@playwright/test';",
    "export default defineConfig({ testDir: './tests/e2e/timeline', testMatch: 'player-export-frame-parity.spec.ts', projects: [{ name: 'native-codec-chrome155' }] });",
    '',
  ].join('\n'), { mode: 0o600 });
  const spec = path.join(root, 'tests/e2e/timeline/player-export-frame-parity.spec.ts');
  mkdirSync(path.dirname(spec), { recursive: true });
  writeFileSync(spec, "import './viewing-parity/cases';\n", { mode: 0o600 });
  const cases = path.join(root, 'tests/e2e/timeline/viewing-parity/cases.ts');
  mkdirSync(path.dirname(cases), { recursive: true });
  writeFileSync(cases, caseSource(options), { mode: 0o600 });
  return root;
}

function refuses(label, operation, message) {
  assert.throws(operation, message, `${label} must refuse`);
}

export function assertDiscoveryRefusals(controller, appRoot) {
  const roots = [];
  try {
    const wrongCount = makeDiscoveryFixture(appRoot, { count: 4 });
    roots.push(wrongCount);
    refuses('wrong-count discovery', () => controller.discover(wrongCount), /exactly 5 parity cases/);

    const wrongName = makeDiscoveryFixture(appRoot, { renameLast: true });
    roots.push(wrongName);
    refuses('wrong-name discovery', () => controller.discover(wrongName), /missing a current parity case/);

    const noTests = makeDiscoveryFixture(appRoot, { count: 0 });
    roots.push(noTests);
    refuses('no-tests discovery', () => controller.discover(noTests), /No tests found/);

    const helperError = mkdtempSync(path.join(path.dirname(new URL(import.meta.url).pathname), 'discovery-controls-'));
    assert.equal(realpathSync(helperError), helperError, 'helper-error root must be canonical');
    roots.push(helperError);
    refuses('helper-error discovery', () => controller.discover(helperError), /offline Playwright discovery failed/);
  } finally {
    for (const root of roots) {
      assert.equal(realpathSync(root), root, 'only the recorded discovery control root may be removed');
      rmSync(root, { recursive: true, force: true });
    }
  }
  return { wrongCount: 'refused', wrongName: 'refused', noTests: 'refused', helperError: 'refused' };
}

export function assertDiscoveryReadiness(controller, appRoot) {
  const discovery = assertDiscoverySummary(controller.discover(appRoot));
  const refusals = assertDiscoveryRefusals(controller, appRoot);
  return { discovery, refusals };
}
