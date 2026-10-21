import { isAbsolute, join } from 'node:path';
import { pathToFileURL } from 'node:url';

const appCheckout = process.env.APP_CHECKOUT;
const importRoot = process.env.APP_IMPORT_ROOT ?? appCheckout;
if (!appCheckout || !isAbsolute(appCheckout) || !importRoot || !isAbsolute(importRoot)) {
  throw new Error('APP_CHECKOUT and APP_IMPORT_ROOT must be absolute frozen paths');
}

const importFromApp = (relativePath) => import(pathToFileURL(join(importRoot, relativePath)).href);
const [local, bootstrap] = await Promise.all([
  importFromApp('tests/e2e/local/support/harness.ts'),
  importFromApp('tests/e2e/timeline/viewing-parity/bootstrap.ts'),
]);

for (const [name, value] of Object.entries({
  DirectHarness: local.DirectHarness,
  harnessUnavailableReason: local.harnessUnavailableReason,
  startRealPackHost: bootstrap.startRealPackHost,
})) {
  if (typeof value !== 'function') throw new Error(`required App driver export missing: ${name}`);
}

if (process.argv.includes('--imports-only')) {
  console.log(JSON.stringify({
    check: 'current-pack-host-readiness-imports',
    exports: ['DirectHarness', 'harnessUnavailableReason', 'startRealPackHost'],
    readyRenderCapability: 'not-imported',
  }));
  process.exit(0);
}

const unavailable = local.harnessUnavailableReason();
if (unavailable) throw new Error(unavailable);

const harness = new local.DirectHarness();
let host;
let failure;
try {
  await harness.start({ seed: false });
  // startRealPackHost already verifies host_ready_capabilities and the Runtime
  // rendering.render catalog. Do not add a public catalog helper or fabricate
  // a capability result when readyRenderCapability is unavailable.
  host = await bootstrap.startRealPackHost(harness, async () => undefined);
  console.log(JSON.stringify({
    check: 'current-pack-host-readiness',
    readiness: 'startRealPackHost-returned',
    realm_id: harness.realmId,
    runtime_instance_id: harness.runtimeInstanceId,
  }));
} catch (error) {
  failure = error;
} finally {
  try { await host?.stop(); } catch (error) { failure ??= error; }
  try { await harness.stop(); } catch (error) { failure ??= error; }
}
if (failure) throw failure;
