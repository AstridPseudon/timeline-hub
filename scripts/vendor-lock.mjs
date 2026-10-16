#!/usr/bin/env node
// Consumer side of the producer-manifest / vendor.lock.json design (testing plan C1).
//   node scripts/vendor-lock.mjs check <lock>                       local bytes vs lock (default lane, no producer)
//   node scripts/vendor-lock.mjs check <lock> --producer <checkout> lock vs the producer's manifest (boundary job)
//   node scripts/vendor-lock.mjs update <lock> --producer <checkout> copy from the producer and rewrite the lock
// Lock paths are relative to this repo's root. Never hand-edit a lock; run `update`.
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { copyFileSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const digest = (file) => `sha256:${createHash('sha256').update(readFileSync(file)).digest('hex')}`;
const readJson = (file) => JSON.parse(readFileSync(file, 'utf8'));
const fail = (message) => { console.error(message); process.exit(1); };

const [command, lockArg, ...rest] = process.argv.slice(2);
const producerAt = rest.indexOf('--producer');
const producer = producerAt >= 0 ? path.resolve(rest[producerAt + 1] ?? '') : null;
if (!['check', 'update'].includes(command) || !lockArg || (command === 'update' && !producer)) {
  fail('usage: vendor-lock.mjs check <lock> [--producer <checkout>] | update <lock> --producer <checkout>');
}

const lockPath = path.resolve(lockArg);
const lock = readJson(lockPath);
const producerManifest = () => readJson(path.join(producer, lock.manifest));
const reVendor = `re-vendor with: node scripts/vendor-lock.mjs update ${path.relative(ROOT, lockPath)} --producer <${lock.producer} checkout>`;

if (command === 'update') {
  const manifest = producerManifest();
  for (const [consumerPath, entry] of Object.entries(lock.files)) {
    const target = path.join(ROOT, consumerPath);
    mkdirSync(path.dirname(target), { recursive: true });
    copyFileSync(path.join(producer, entry.from), target);
    entry.sha256 = digest(target);
    if (manifest.artifacts[entry.from] !== entry.sha256) fail(`${entry.from}: producer manifest is stale (run its artifact_manifest.py)`);
  }
  lock.producer_version = manifest.version;
  lock.source_commit = execFileSync('git', ['-C', producer, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim();
  writeFileSync(lockPath, `${JSON.stringify(lock, (k, v) => (v && typeof v === 'object' && !Array.isArray(v) ? Object.fromEntries(Object.entries(v).sort(([a], [b]) => (a < b ? -1 : 1))) : v), 2)}\n`);
  console.log(`updated ${path.relative(ROOT, lockPath)} from ${lock.producer} ${lock.source_commit.slice(0, 12)}`);
  process.exit(0);
}

const problems = [];
for (const [consumerPath, entry] of Object.entries(lock.files)) {
  let actual;
  try { actual = digest(path.join(ROOT, consumerPath)); } catch { problems.push(`${consumerPath}: missing`); continue; }
  if (actual !== entry.sha256) problems.push(`${consumerPath}: edited locally`);
}
if (problems.length) fail(`${problems.join('\n')}\n${reVendor}`);

if (producer) {
  const manifest = producerManifest();
  const changed = Object.values(lock.files).filter((entry) => manifest.artifacts[entry.from] !== entry.sha256).map((entry) => entry.from);
  if (changed.length || manifest.version !== lock.producer_version) {
    fail(`producer changed: ${changed.join(', ') || '(manifest version only)'}\n${reVendor}`);
  }
}
console.log(`ok ${path.relative(ROOT, lockPath)}${producer ? ' (matches producer manifest)' : ''}`);
