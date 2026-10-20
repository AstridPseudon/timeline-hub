import { defineConfig } from '@playwright/test';
import threeProducts from './playwright.three-products.config.ts';
import { CONTRACT_VERSION } from './src/integrations/runtime/generated-contract-metadata.ts';

const APPROVED_AGENT_CHECKOUT = '/home/user/work/wt/app-m2-bundle2-agent-source';
const APPROVED_RUNTIME_CHECKOUT = '/home/user/work/wt/app-m2-bundle2-runtime-source';
const APPROVED_AGENT_HEAD = '027bd16d96010544331c953c0e1014e161786e71';
const APPROVED_RUNTIME_HEAD = '4c145dc62192f0e942e3ee3922a11488aefe9b41';
const APPROVED_CONTRACT_VERSION = '0.2.3';

/**
 * The scalar lane is source-pinned by its caller. A run without the protected
 * Bundle2 leases, heads and client selection is not QA evidence.
 */
for (const name of [
  'ASTRID_CHECKOUT',
  'ASTRID_RUNTIME_CHECKOUT',
  'ASTRID_PYTHON',
  'ASTRID_RUNTIME_PYTHON',
  'TIMELINE_BUNDLE_AGENT_HEAD',
  'TIMELINE_BUNDLE_RUNTIME_HEAD',
]) {
  if (!process.env[name]) throw new Error(`clip-scalar qualification requires ${name}`);
}
for (const [name, actual, expected] of [
  ['ASTRID_CHECKOUT', process.env.ASTRID_CHECKOUT, APPROVED_AGENT_CHECKOUT],
  ['ASTRID_RUNTIME_CHECKOUT', process.env.ASTRID_RUNTIME_CHECKOUT, APPROVED_RUNTIME_CHECKOUT],
  ['TIMELINE_BUNDLE_AGENT_HEAD', process.env.TIMELINE_BUNDLE_AGENT_HEAD, APPROVED_AGENT_HEAD],
  ['TIMELINE_BUNDLE_RUNTIME_HEAD', process.env.TIMELINE_BUNDLE_RUNTIME_HEAD, APPROVED_RUNTIME_HEAD],
] as const) {
  if (actual !== expected) throw new Error(`clip-scalar qualification requires frozen Bundle2 ${name}=${expected}; got ${actual}`);
}
if (CONTRACT_VERSION !== APPROVED_CONTRACT_VERSION) {
  throw new Error(`clip-scalar qualification requires client ${APPROVED_CONTRACT_VERSION}; got ${CONTRACT_VERSION}`);
}

export default defineConfig({
  ...threeProducts,
  testMatch: 'clip-scalar-command.spec.ts',
  outputDir: process.env.PLAYWRIGHT_OUTPUT_DIR ?? 'test-results/clip-scalar',
});
