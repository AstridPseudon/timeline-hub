import { chromium, test as base, type Browser } from '@playwright/test';
import { execFileSync } from 'node:child_process';
import { readFile, realpath } from 'node:fs/promises';
import { resolve } from 'node:path';
import { DirectHarness, harnessUnavailableReason, REPO_ROOT } from '../../local/support/harness';
import { startRealPackHost } from './bootstrap';
import { prepareFrameParityFixture, type FrameParityFixture, readRuntimeJson } from './fixture';
import { mediaHash } from './media';
import type { Capability } from '../../../../src/integrations/runtime/generated';

export const INSTALLED_BROWSER = '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell';
const COMPOSITION_HASH = 'sha256:93bc66b5c63d2d20597c66a2458dcab1c9cd65838b2ff493486c1e84dbec6caa';

function requiredEnv(name: string): string {
  const value = process.env[name];
  if (!value) throw new Error(`${name} must name the manager-frozen source tuple`);
  return resolve(value);
}

export async function sourceVersions() {
  const roots = {
    app: REPO_ROOT, agent: requiredEnv('ASTRID_CHECKOUT'), runtime: requiredEnv('ASTRID_RUNTIME_CHECKOUT'),
    composition: requiredEnv('TIMELINE_COMPOSITION_CHECKOUT'),
  };
  const artifacts = [resolve(roots.app, 'vendor/artifacts/banodoco-timeline-composition-0.0.8.tgz'),
    resolve(roots.agent, 'remotion/artifacts/banodoco-timeline-composition-0.0.8.tgz')];
  const hashes = await Promise.all(artifacts.map(async path => mediaHash(await readFile(path))));
  if (hashes.some(hash => hash !== COMPOSITION_HASH)) throw new Error(`both consumers require exact public 0.0.8 artifact ${COMPOSITION_HASH}: ${hashes}`);
  const remotionProject = await realpath(requiredEnv('ASTRID_REMOTION_PROJECT_DIR'));
  const packages: Record<string, string> = {};
  const installedCompositionHashes: Record<string, string> = {};
  for (const [index, [consumer, root]] of [['app', roots.app], ['agent', remotionProject]].entries()) {
    const artifact = artifacts[index];
    const entries = execFileSync('tar', ['-tzf', artifact], { encoding: 'utf8' }).trim().split('\n').filter(name => !name.endsWith('/'));
    const installed = Buffer.concat(await Promise.all(entries.map(name => {
      if (!name.startsWith('package/') || name.split('/').includes('..')) throw new Error('unexpected public package member');
      return readFile(resolve(root, 'node_modules/@banodoco/timeline-composition', name.slice('package/'.length)));
    })));
    const published = execFileSync('tar', ['-xOf', artifact], { maxBuffer: 8 * 1024 * 1024 });
    if (!installed.equals(published)) throw new Error(`${consumer} installed Composition bytes differ from exact public artifact`);
    installedCompositionHashes[consumer] = mediaHash(installed);
    for (const [name, expected] of [['react', '18.3.1'], ['react-dom', '18.3.1'], ['remotion', '4.0.509'], ['@banodoco/timeline-composition', '0.0.8']]) {
      const pkg = JSON.parse(await readFile(resolve(root, 'node_modules', name, 'package.json'), 'utf8'));
      if (pkg.version !== expected) throw new Error(`${consumer} ${name}: ${pkg.version} != ${expected}`);
      packages[`${consumer}:${name}`] = pkg.version;
    }
  }
  if (process.env.ASTRID_REMOTION_BROWSER_EXECUTABLE !== INSTALLED_BROWSER) {
    throw new Error('Agent parent must select the installed headless_shell 1194 through ASTRID_REMOTION_BROWSER_EXECUTABLE');
  }
  return {
    revisions: Object.fromEntries(Object.entries(roots).map(([name, root]) => [name,
      execFileSync('git', ['rev-parse', 'HEAD'], { cwd: root, encoding: 'utf8' }).trim()])),
    roots, remotionProject, artifacts, hashes, installedCompositionHashes, packages, browserExecutable: INSTALLED_BROWSER, node: process.version,
  };
}

export async function readyRenderCapability(harness: DirectHarness): Promise<Capability> {
  let cursor: string | null = null;
  do {
    const page: { items: Capability[]; next_cursor: string | null } = await readRuntimeJson(harness,
      `/v1/capabilities?limit=50${cursor ? `&cursor=${encodeURIComponent(cursor)}` : ''}`);
    const capability = page.items.find(item => item.capability_id === 'rendering.render');
    if (capability) {
      if (capability.status !== 'ready' || !/^sha256:[0-9a-f]{64}$/.test(capability.definition_digest)) {
        throw new Error(`production rendering.render is unavailable: ${JSON.stringify(capability)}`);
      }
      return capability;
    }
    cursor = page.next_cursor;
  } while (cursor);
  throw new Error('production rendering.render is absent from the real Runtime catalog');
}

export const test = base.extend<object, {
  harness: DirectHarness; fixture: FrameParityFixture; browser: Browser;
}>({
  // eslint-disable-next-line no-empty-pattern
  harness: [async ({}, provide) => {
    const reason = harnessUnavailableReason();
    if (reason) throw new Error(reason);
    await sourceVersions();
    const harness = await new DirectHarness().start();
    try { await provide(harness); } finally { await harness.stop(); }
  }, { scope: 'worker', timeout: 240_000 }],
  fixture: [async ({ harness }, provide) => {
    const fixture = await prepareFrameParityFixture(harness);
    await harness.enableTimelineAuthoring(requiredEnv('ASTRID_PYTHON'));
    // startRealPackHost is intentionally fail-closed until Agent provides its
    // launcher-owned setup helper. No browser/export lane is currently qualified.
    const host = await startRealPackHost(harness);
    try {
      await readyRenderCapability(harness);
      await provide(fixture);
    } finally { await host.stop(); }
  }, { scope: 'worker', timeout: 240_000 }],
  browser: [async ({ harness, fixture }, provide) => {
    void fixture;
    const browser = await chromium.launch({ args: harness.chromiumArgs, executablePath: INSTALLED_BROWSER });
    try { await provide(browser); } finally { await browser.close(); }
  }, { scope: 'worker' }],
  context: async ({ browser, harness }, provide) => {
    const context = await browser.newContext({ ...harness.contextOptions,
      viewport: { width: 1600, height: 1000 }, deviceScaleFactor: 1, acceptDownloads: true });
    try { await provide(context); } finally { await context.close(); }
  },
});
