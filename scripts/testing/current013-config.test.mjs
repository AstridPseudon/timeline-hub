import assert from 'node:assert/strict';
import { existsSync } from 'node:fs';
import test from 'node:test';

const root = new URL('../..', import.meta.url);
const spec = new URL('tests/e2e/local/bootstrap013-real-http.spec.ts', root);
const { default: config } = await import(new URL('playwright.bootstrap013.config.ts', root));

test('current013 dedicated config selects exactly the bootstrap journey', () => {
  assert.equal(config.testDir, './tests/e2e/local');
  assert.equal(config.testMatch, 'bootstrap013-real-http.spec.ts');
  assert.equal(config.globalSetup, './tests/e2e/local/global-setup.ts');
  assert.equal(config.webServer, undefined);
  assert.ok(existsSync(new URL(config.testDir, root)));
  assert.ok(existsSync(new URL(config.globalSetup, root)));
  assert.ok(existsSync(spec));
});
