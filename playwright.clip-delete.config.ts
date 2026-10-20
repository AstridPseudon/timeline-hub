import { defineConfig } from '@playwright/test';
import threeProducts from './playwright.three-products.config.ts';

const APPROVED_AGENT_CHECKOUT = '/home/user/work/wt/app-m2-bundle2-agent-source';
const APPROVED_RUNTIME_CHECKOUT = '/home/user/work/wt/app-m2-bundle2-runtime-source';
const APPROVED_AGENT_HEAD = '027bd16d96010544331c953c0e1014e161786e71';
const APPROVED_RUNTIME_HEAD = '4c145dc62192f0e942e3ee3922a11488aefe9b41';

/**
 * The real-delete lane is deliberately source-pinned by its caller.  A list or
 * run without the approved paired checkouts and heads is not qualification
 * evidence, so fail at config load rather than silently selecting sibling
 * defaults.
 */
for (const name of [
  'ASTRID_CHECKOUT',
  'ASTRID_RUNTIME_CHECKOUT',
  'TIMELINE_BUNDLE_AGENT_HEAD',
  'TIMELINE_BUNDLE_RUNTIME_HEAD',
]) {
  if (!process.env[name]) throw new Error(`clip-delete qualification requires ${name}`);
}
for (const [name, actual, expected] of [
  ['ASTRID_CHECKOUT', process.env.ASTRID_CHECKOUT, APPROVED_AGENT_CHECKOUT],
  ['ASTRID_RUNTIME_CHECKOUT', process.env.ASTRID_RUNTIME_CHECKOUT, APPROVED_RUNTIME_CHECKOUT],
  ['TIMELINE_BUNDLE_AGENT_HEAD', process.env.TIMELINE_BUNDLE_AGENT_HEAD, APPROVED_AGENT_HEAD],
  ['TIMELINE_BUNDLE_RUNTIME_HEAD', process.env.TIMELINE_BUNDLE_RUNTIME_HEAD, APPROVED_RUNTIME_HEAD],
] as const) {
  if (actual !== expected) throw new Error(`clip-delete qualification requires frozen Bundle2 ${name}=${expected}; got ${actual}`);
}

export default defineConfig({
  ...threeProducts,
  testMatch: 'clip-delete-command.spec.ts',
  outputDir: process.env.PLAYWRIGHT_OUTPUT_DIR ?? 'test-results/clip-delete',
});
