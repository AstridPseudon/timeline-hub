import assert from 'node:assert/strict';
import { test as originalTest, readyRenderCapability } from './harness';
import { startRealPackHost } from './bootstrap';
import { prepareFrameParityFixture, type FrameParityFixture } from './normal-profile-native1920.fixture';

export { readyRenderCapability, sourceVersions } from './harness';

// Proposal only: retain original source/package/browser guards and ordinary host.
// The manifest records the pending manager decision; this is not a run grant.
export const test = originalTest.extend<object, { fixture: FrameParityFixture }>({
  fixture: [async ({ harness }, provide) => {
    const fixture = await prepareFrameParityFixture(harness);
    assert.ok(process.env.ASTRID_PYTHON, 'ASTRID_PYTHON must name the manager-frozen Python');
    await harness.enableTimelineAuthoring(process.env.ASTRID_PYTHON);
    const host = await startRealPackHost(harness, () => readyRenderCapability(harness));
    try { await provide(fixture); } finally { await host.stop(); }
  }, { scope: 'worker', timeout: 240_000 }],
  context: async ({ browser, harness }, provide) => {
    const context = await browser.newContext({ ...harness.contextOptions,
      viewport: { width: 2000, height: 1200 }, deviceScaleFactor: 1, acceptDownloads: true });
    try { await provide(context); } finally { await context.close(); }
  },
});
