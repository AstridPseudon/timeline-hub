#!/usr/bin/env node
// Re-seal the Astrid Plan A contracts after their source files moved.
//
//   node scripts/quality/refresh-astrid-contracts.mjs [--astrid-root <dir>] [--runtime-root <dir>] [--check]
//
// C1 (config/contracts/astrid-plan-a-c1.json): recompute every sourceEvidence sha256 whose repository
//   root is known (astrid-app always; astrid-agent and astrid-runtime via the flags), then the canonical digest.
// C2 (config/contracts/astrid-plan-a-c2.json): recompute predecessor.rawFileSha256 and canonicalDigest from
//   the C1 file, diagnostic.schemaSha256, applicable source hashes and generated-client hashes, then the canonical digest.
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
const RUNTIME_METADATA_PATH = 'runtime_protocol/contract_metadata.py';
const APP_METADATA_PATH = path.join(REPO_ROOT, 'src/integrations/runtime/contract-metadata.ts');

// Source files that moved upstream after the contract was issued: old path -> new path, per repository.
// A moved path is rewritten only when the old one is gone and the new one exists.
const PATH_MOVES = {
  'astrid-agent': {
    'astrid/packs/vibecomfy/executors/run/run.py': 'astrid/packs/vibecomfy/actions/run/run.py',
    'astrid/packs/vibecomfy/executors/run/requirements.txt': 'astrid/packs/vibecomfy/actions/run/requirements.txt',
  },
};

const sha256 = (bytes) => createHash('sha256').update(bytes).digest('hex');
const serialize = (value) => `${JSON.stringify(value, null, 2)}\n`;

function parseArgs(argv) {
  const options = { roots: { 'astrid-app': REPO_ROOT }, check: false };
  for (let index = 0; index < argv.length; index += 1) {
    const flag = argv[index];
    if (flag === '--check') { options.check = true; continue; }
    const name = { '--astrid-root': 'astrid-agent', '--runtime-root': 'astrid-runtime' }[flag];
    if (!name) throw new Error(`unknown argument: ${flag}`);
    const value = argv[++index];
    if (!value || value.startsWith('--')) throw new Error(`${flag} requires a path`);
    options.roots[name] = path.resolve(value);
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
  const syncSource = (label, source, root) => {
    try { sync(label, source, 'sha256', hashSource(root, source.path)); }
    catch (error) { problems.push(`${label} (${source.repository}:${source.path}): ${error.message}`); }
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
    const root = roots[source.repository];
    if (!root) continue;
    if (source.repository === 'astrid-app' && source.path === 'config/contracts/astrid-plan-a-c1.json') {
      sync(`C2 ${source.path}`, source, 'sha256', sha256(c1Text));
    } else {
      syncSource(`C2 sourceApplicability ${source.path}`, source, root);
    }
  }

  for (const client of c2.generatedClientCompatibility?.clients ?? []) {
    const root = roots[client.repository];
    if (!root) continue;
    try { sync(`C2 generated client ${client.repository}:${client.generatedPath}`, client, 'generatedSha256', hashSource(root, client.generatedPath)); }
    catch (error) { problems.push(`C2 generatedClientCompatibility.${client.repository}.generatedPath (${client.generatedPath}): ${error.message}`); }
    try { sync(`C2 generated client ${client.repository}:${client.metadataPath}`, client, 'metadataSha256', hashSource(root, client.metadataPath)); }
    catch (error) { problems.push(`C2 generatedClientCompatibility.${client.repository}.metadataPath (${client.metadataPath}): ${error.message}`); }
  }

  const runtimeRoot = roots['astrid-runtime'];
  if (runtimeRoot) {
    try {
      const metadata = readFileSync(path.resolve(realpathSync(runtimeRoot), RUNTIME_METADATA_PATH), 'utf8');
      const match = metadata.match(/^\s*SCHEMA_DIGEST\s*=\s*['"](sha256:[0-9a-f]{64})['"]\s*$/m);
      if (!match) throw new Error(`SCHEMA_DIGEST not found in ${RUNTIME_METADATA_PATH}`);
      sync('C2 generatedClientCompatibility.runtimeSchemaDigest', c2.generatedClientCompatibility, 'runtimeSchemaDigest', match[1]);
    } catch (error) {
      problems.push(`C2 generatedClientCompatibility.runtimeSchemaDigest (${RUNTIME_METADATA_PATH}): ${error.message}`);
    }
  }
  sync('C2 digest', c2, 'digest', computeC2Digest(c2));

  const appMetadata = readFileSync(APP_METADATA_PATH, 'utf8');
  let nextAppMetadata = appMetadata;
  for (const [name, digest] of [['ASTRID_C1_CANONICAL_DIGEST', c1.digest], ['ASTRID_C2_CANONICAL_DIGEST', c2.digest]]) {
    const pattern = new RegExp(`(export const ${name} = ')[^']*(' as const;)`);
    if (!pattern.test(nextAppMetadata)) {
      problems.push(`src/integrations/runtime/contract-metadata.ts: missing ${name} constant`);
      continue;
    }
    nextAppMetadata = nextAppMetadata.replace(pattern, `$1${digest}$2`);
  }
  if (nextAppMetadata !== appMetadata) changes.push('src/integrations/runtime/contract-metadata.ts: C1/C2 digest constants updated');

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

  return { c1Text, c2Text: serialize(c2), appMetadataText: nextAppMetadata, fixtures, changes, problems };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const options = parseArgs(process.argv.slice(2));
    const { c1Text, c2Text, appMetadataText, fixtures, changes, problems } = refresh(options);
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
    writeFileSync(APP_METADATA_PATH, appMetadataText);
    for (const fixture of fixtures) writeFileSync(fixture.file, fixture.text);
    console.log(changes.length === 0 ? 'Nothing to refresh.' : `Refreshed ${changes.length} value(s).`);
  } catch (error) {
    console.error(error.message);
    process.exit(1);
  }
}
