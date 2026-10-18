#!/usr/bin/env node
// Re-seal the Astrid Plan A contracts after their source files moved.
//
//   node scripts/quality/refresh-astrid-contracts.mjs [--astrid-root <dir>] [--runtime-root <dir>] [--check]
//
// C1 (config/contracts/astrid-plan-a-c1.json): recompute every sourceEvidence sha256 whose repository
//   root is known (reigh-app always; Astrid and workspace-runtime via the flags), then the canonical digest.
// C2 (config/contracts/astrid-plan-a-c2.json): recompute predecessor.rawFileSha256 and canonicalDigest from
//   the C1 file, diagnostic.schemaSha256, the reigh-app sourceApplicability hashes, then the canonical digest.
//   Entries pinned to other repositories are historical producer evidence and are left as issued.
// Every hash comes from the checkers' own functions or a plain SHA-256 of the file; nothing is typed by hand.
// --check writes nothing and exits 1 if a refresh would change a file. Missing source files are reported
// and make the command fail, so a half-refreshed contract is never presented as sealed.
import { createHash } from 'node:crypto';
import { existsSync, readFileSync, realpathSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { computeContractDigest as computeC1Digest } from './check-astrid-contract-freeze.mjs';
import { computeContractDigest as computeC2Digest } from './check-astrid-contract-c2.mjs';

const REPO_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const C1_PATH = path.join(REPO_ROOT, 'config/contracts/astrid-plan-a-c1.json');
const C2_PATH = path.join(REPO_ROOT, 'config/contracts/astrid-plan-a-c2.json');
const SCHEMA_PATH = path.join(REPO_ROOT, 'config/contracts/astrid-plan-a-diagnostic-c2.schema.json');

// Source files that moved upstream after the contract was issued: old path -> new path, per repository.
// A moved path is rewritten only when the old one is gone and the new one exists.
const PATH_MOVES = {
  Astrid: {
    'astrid/packs/vibecomfy/executors/run/run.py': 'astrid/packs/vibecomfy/actions/run/run.py',
    'astrid/packs/vibecomfy/executors/run/requirements.txt': 'astrid/packs/vibecomfy/actions/run/requirements.txt',
  },
};

const sha256 = (bytes) => createHash('sha256').update(bytes).digest('hex');
const serialize = (value) => `${JSON.stringify(value, null, 2)}\n`;

function parseArgs(argv) {
  const options = { roots: { 'reigh-app': REPO_ROOT }, check: false };
  for (let index = 0; index < argv.length; index += 1) {
    const flag = argv[index];
    if (flag === '--check') { options.check = true; continue; }
    const names = { '--astrid-root': ['Astrid'], '--runtime-root': ['workspace-runtime', 'banodoco-workspace-runtime'] }[flag];
    if (!names) throw new Error(`unknown argument: ${flag}`);
    const value = argv[++index];
    if (!value || value.startsWith('--')) throw new Error(`${flag} requires a path`);
    for (const name of names) options.roots[name] = path.resolve(value);
  }
  return options;
}

function hashSource(root, relativePath) {
  const realRoot = realpathSync(root);
  const file = realpathSync(path.resolve(realRoot, relativePath));
  if (!file.startsWith(`${realRoot}${path.sep}`)) throw new Error('source escapes repository root');
  return sha256(readFileSync(file));
}

export function refresh({ roots, check = false }) {
  const problems = [];
  const changes = [];
  const sync = (label, entry, key, next) => {
    if (entry[key] !== next) { changes.push(`${label}: ${String(entry[key]).slice(0, 19)}... -> ${next.slice(0, 19)}...`); entry[key] = next; }
  };

  const c1 = JSON.parse(readFileSync(C1_PATH, 'utf8'));
  for (const evidence of c1.sourceEvidence) {
    const root = roots[evidence.repository];
    if (!root) continue;
    try {
      const moved = PATH_MOVES[evidence.repository]?.[evidence.path];
      if (moved && !existsSync(path.resolve(root, evidence.path)) && existsSync(path.resolve(root, moved))) {
        changes.push(`C1 ${evidence.id}: path ${evidence.path} -> ${moved}`);
        evidence.path = moved;
      }
      sync(`C1 ${evidence.id}`, evidence, 'sha256', hashSource(root, evidence.path));
    }
    catch (error) { problems.push(`C1 sourceEvidence.${evidence.id} (${evidence.repository}:${evidence.path}): ${error.message}`); }
  }
  sync('C1 digest', c1, 'digest', computeC1Digest(c1));
  const c1Text = serialize(c1);

  const c2 = JSON.parse(readFileSync(C2_PATH, 'utf8'));
  sync('C2 predecessor.rawFileSha256', c2.predecessor, 'rawFileSha256', sha256(c1Text));
  sync('C2 predecessor.canonicalDigest', c2.predecessor, 'canonicalDigest', c1.digest);
  sync('C2 diagnostic.schemaSha256', c2.diagnostic, 'schemaSha256', sha256(readFileSync(SCHEMA_PATH)));
  for (const source of c2.sourceApplicability) {
    if (source.repository !== 'reigh-app') continue;
    try {
      // The C1 file's own entry hashes the bytes about to be written, not the ones on disk.
      const next = source.path === 'config/contracts/astrid-plan-a-c1.json' ? sha256(c1Text) : hashSource(REPO_ROOT, source.path);
      sync(`C2 ${source.path}`, source, 'sha256', next);
    }
    catch (error) { problems.push(`C2 sourceApplicability ${source.path}: ${error.message}`); }
  }
  sync('C2 digest', c2, 'digest', computeC2Digest(c2));

  // Fixtures pin the C2 digest they were issued against; carry them to the new one (text replace keeps their formatting).
  const fixtures = [];
  for (const relative of [...c2.fixtures.positive, ...c2.fixtures.negative]) {
    const file = path.join(REPO_ROOT, relative);
    const text = readFileSync(file, 'utf8');
    const fixtureDigests = new Set(text.match(/"contractDigest":\s*"(sha256:[0-9a-f]{64})"/g)?.map((m) => m.match(/sha256:[0-9a-f]{64}/)[0]));
    if (fixtureDigests.size === 0 || (fixtureDigests.size === 1 && fixtureDigests.has(c2.digest))) continue;
    const next = [...fixtureDigests].reduce((acc, old) => acc.split(old).join(c2.digest), text);
    changes.push(`fixture ${relative}: contractDigest -> ${c2.digest.slice(0, 19)}...`);
    fixtures.push({ file, text: next });
  }

  return { c1Text, c2Text: serialize(c2), fixtures, changes, problems };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const options = parseArgs(process.argv.slice(2));
    const { c1Text, c2Text, fixtures, changes, problems } = refresh(options);
    for (const line of changes) console.log(line);
    for (const line of problems) console.error(`UNRESOLVED ${line}`);
    if (problems.length > 0) process.exit(1);
    if (options.check) {
      const stale = changes.length > 0;
      console.log(stale ? 'STALE: run without --check to refresh' : 'Contracts are sealed and current.');
      process.exit(stale ? 1 : 0);
    }
    writeFileSync(C1_PATH, c1Text);
    writeFileSync(C2_PATH, c2Text);
    for (const fixture of fixtures) writeFileSync(fixture.file, fixture.text);
    console.log(changes.length === 0 ? 'Nothing to refresh.' : `Refreshed ${changes.length} value(s).`);
  } catch (error) {
    console.error(error.message);
    process.exit(1);
  }
}
