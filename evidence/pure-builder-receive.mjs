#!/usr/bin/env node
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const selectors = [
  'p2-automatic-child-placement',
  'p2-popup-add',
  'p2-parent-move',
  'p2-transition-none-single',
  'p2-transition-none-bulk',
  'p2-register-asset',
  'p1',
  'p3',
];

const rejected = new Set([
  '8f278b91accec5852e39bb84822e99124fccb81d',
  '520d7e4fc12a03392afaed3f486aba34a2b5c319',
]);
const rejectedAgent = new Set(['28e56cacb42d3da85b02e5b3543895b44f3d0f70']);

function fail(message) {
  throw new Error(`D141p pure receiver refused input: ${message}`);
}

function fullId(value, label) {
  if (!/^[0-9a-f]{40}$/.test(value ?? '')) fail(`${label} must be a full 40-character SHA`);
  return value;
}

function source(value, role) {
  if (!value || typeof value !== 'object') fail(`${role} source receipt is required`);
  const head = fullId(value.head, `${role} head`);
  const tree = fullId(value.tree, `${role} tree`);
  if (!path.isAbsolute(value.checkout ?? '')) fail(`${role} checkout must be absolute`);
  if (!value.receipt || typeof value.receipt !== 'string') fail(`${role} immutable receipt is required`);
  if (value.clean !== true) fail(`${role} clean receipt is required`);
  if (role === 'app' && rejected.has(head)) fail(`historical/draft App head ${head} is not final freeze-2 input`);
  if (role === 'agent' && rejectedAgent.has(head)) fail(`historical Agent head ${head} is not final freeze-2 input`);
  return { head, tree, checkout: value.checkout };
}

function sha256(bytes) {
  return createHash('sha256').update(bytes).digest('hex');
}

if (process.argv.length !== 4) fail('usage is <genuine-receipts.json> <absolute-output.json>');
const [receiptsPath, outputPath] = process.argv.slice(2);
if (!path.isAbsolute(outputPath)) fail('output path must be absolute and evidence-owned');
const input = JSON.parse(readFileSync(receiptsPath, 'utf8'));
const sources = Object.fromEntries(['app', 'agent', 'runtime', 'composition']
  .map((role) => [role, source(input.sources?.[role], role)]));
if (input.runtime_kit_receipt?.installed !== true || input.runtime_kit_receipt?.qualified !== true
  || typeof input.runtime_kit_receipt.receipt !== 'string') {
  fail('installed qualified Runtime paired-kit receipt is required');
}
const builderPath = input.builder?.path;
if (!path.isAbsolute(builderPath ?? '')) fail('genuine final builder path must be absolute');
const { buildSubmitPlan, serviceRecipe } = await import(pathToFileURL(builderPath));
if (typeof buildSubmitPlan !== 'function' || typeof serviceRecipe !== 'function') {
  fail('builder must export buildSubmitPlan and serviceRecipe');
}

const pins = Object.fromEntries(Object.entries(sources).map(([role, value]) => [role, {
  head: value.head,
  tree: value.tree,
}]));
const checkouts = Object.fromEntries(Object.entries(sources).map(([role, value]) => [role, value.checkout]));
const app8 = sources.app.head.slice(0, 8);
const target = `app-pin-${app8}`;
const bindings = selectors.map((name) => {
  const normalSuite = `d141g-${name}-${app8}-submit`;
  const preflightSuite = `${normalSuite}-preflight`;
  const plan = buildSubmitPlan({ name, target, pins, checkouts });
  const normal = serviceRecipe({ name, pins, checkouts });
  const preflight = serviceRecipe({ name, pins, checkouts, preflight: true });
  const normalRow = `app ${normalSuite} ${normal}\n`;
  const preflightRow = `app ${preflightSuite} ${preflight}\n`;
  return {
    selector: name,
    target,
    suites: { normal: normalSuite, preflight: preflightSuite },
    plan,
    commands: {
      normal: { command: normal, bytes: Buffer.byteLength(normal), sha256_utf8_without_newline: sha256(normal) },
      preflight: { command: preflight, bytes: Buffer.byteLength(preflight), sha256_utf8_without_newline: sha256(preflight) },
    },
    rows: {
      normal: { row: normalRow, bytes: Buffer.byteLength(normalRow), sha256_utf8_with_one_terminal_lf: sha256(normalRow) },
      preflight: { row: preflightRow, bytes: Buffer.byteLength(preflightRow), sha256_utf8_with_one_terminal_lf: sha256(preflightRow) },
    },
  };
});

writeFileSync(outputPath, `${JSON.stringify({
  schema_version: 1,
  task: 'D141p',
  status: 'PROSPECTIVE_PRODUCTION_BUILDER',
  registration: false,
  execution: 'none',
  source_receipts: sources,
  runtime_kit_receipt: input.runtime_kit_receipt,
  builder: { path: builderPath, declared_sha256: input.builder?.sha256 ?? null },
  bindings,
}, null, 2)}\n`);
