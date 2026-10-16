#!/usr/bin/env node
// Known-failure gate (testing plan R-6). A red test may stay in the suite only
// as an inverse test (it.fails / test.fails / test.fail(, or a `? it.fails : it`
// ternary) with this comment on the line directly above it:
//   // known-failure: <owner> | <expires YYYY-MM-DD> | <reason>
// Source tests (src/**/*.test.ts[x]) share one cap, MAX_SRC_ENTRIES.
// Journey specs (tests/**/*.spec.ts) each have an exact budget in FILE_BUDGETS:
// a count above or below its budget fails, so a marker that comes off must lower
// its budget in the same commit. A spec with markers and no budget entry has budget 0.
// Lines that are comments do not count as markers.
// Exits 1 when an entry is missing its comment, malformed, or expired, when the
// src cap is exceeded, or when a spec's marker count differs from its budget.
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const DEFAULT_REPO_ROOT = path.resolve(import.meta.dirname, '../..');
export const MAX_SRC_ENTRIES = 10;
export const FILE_BUDGETS = {
  // Exception note (CLAUDE.md "allowlists shrink"): 13 -> 17 is new behaviour, not debt. Plan A revision 3 adds four journey
  // cases (N1-N4) that fail until their cards land (A2.S/A2.P, A1.G2, A3.M); each marker comes off, and this number falls, in the commit that makes its case pass. Target: 0.
  'tests/e2e/local/direct-journey.spec.ts': 17,
};
const MARKER_RE = /\b(?:it|test)\.fails?\b/;
const COMMENT_LINE_RE = /^\s*(?:\/\/|\/\*|\*)/;
const COMMENT_RE = /^\s*\/\/\s*known-failure:\s*([^|]+?)\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*(\S.*?)\s*$/;

const localToday = () => {
  const d = new Date();
  const pad = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
};

function listFiles(dir, namePattern) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) return listFiles(full, namePattern);
    return namePattern.test(entry.name) ? [full] : [];
  });
}

const isRealDate = (value) => {
  const time = Date.parse(`${value}T00:00:00Z`);
  return !Number.isNaN(time) && new Date(time).toISOString().slice(0, 10) === value;
};

function scanFile(file, repoRoot, today) {
  const lines = fs.readFileSync(file, 'utf8').split('\n');
  const rel = path.relative(repoRoot, file).split(path.sep).join('/');
  return lines.flatMap((line, index) => {
    if (COMMENT_LINE_RE.test(line) || !MARKER_RE.test(line)) return [];
    const where = `${rel}:${index + 1}`;
    const match = index > 0 ? COMMENT_RE.exec(lines[index - 1]) : null;
    if (!match) {
      return [{
        where,
        status: 'MALFORMED',
        detail: 'no well-formed known-failure comment directly above',
        problem: `${where}: missing or malformed known-failure comment`,
      }];
    }
    const [, owner, expires, reason] = match;
    let status = 'ok';
    if (!isRealDate(expires)) status = 'MALFORMED';
    else if (expires < today) status = 'EXPIRED';
    const problem = status === 'ok'
      ? null
      : `${where}: ${status === 'EXPIRED' ? `expired on ${expires}` : `invalid date ${expires}`}`;
    return [{ where, status, detail: `owner=${owner} | expires=${expires} | ${reason}`, problem }];
  });
}

/**
 * Runs the gate over one repo tree. Returns the entries, the problems (each one fails the gate),
 * and the per-spec counts, so callers can print or assert on them.
 */
export function checkKnownFailures({
  repoRoot = DEFAULT_REPO_ROOT,
  today = localToday(),
  fileBudgets = FILE_BUDGETS,
  maxSrcEntries = MAX_SRC_ENTRIES,
} = {}) {
  const entries = [];
  const problems = [];

  const srcEntries = listFiles(path.join(repoRoot, 'src'), /\.test\.tsx?$/)
    .flatMap((file) => scanFile(file, repoRoot, today));
  entries.push(...srcEntries);

  const specCounts = new Map();
  for (const file of listFiles(path.join(repoRoot, 'tests'), /\.spec\.ts$/)) {
    const found = scanFile(file, repoRoot, today);
    const rel = path.relative(repoRoot, file).split(path.sep).join('/');
    specCounts.set(rel, found.length);
    entries.push(...found);
  }

  for (const entry of entries) {
    if (entry.problem) problems.push(entry.problem);
  }

  if (srcEntries.length > maxSrcEntries) {
    problems.push(`${srcEntries.length} src entries exceed the limit of ${maxSrcEntries}`);
  }

  const specFiles = new Set([...Object.keys(fileBudgets), ...specCounts.keys()]);
  const specReport = [];
  for (const rel of [...specFiles].sort()) {
    const count = specCounts.get(rel) ?? 0;
    const budget = fileBudgets[rel] ?? 0;
    specReport.push({ rel, count, budget });
    if (count !== budget) {
      problems.push(`${rel}: ${count} known-failure markers, budget is ${budget} (lower or raise the budget with the marker change)`);
    }
  }

  return { entries, problems, srcCount: srcEntries.length, specReport, today };
}

function main() {
  const result = checkKnownFailures();
  for (const entry of result.entries) {
    console.log(`${entry.status.padEnd(9)} ${entry.where} | ${entry.detail}`);
  }
  console.log(`known-failure entries: ${result.srcCount} in src (max ${MAX_SRC_ENTRIES})`);
  for (const spec of result.specReport.filter((s) => s.count > 0 || s.budget > 0)) {
    console.log(`known-failure markers: ${spec.count} in ${spec.rel} (budget ${spec.budget})`);
  }
  console.log(`checked against ${result.today}`);
  for (const problem of result.problems) console.error(`FAIL ${problem}`);
  process.exit(result.problems.length > 0 ? 1 : 0);
}

if (process.argv[1] && pathToFileURL(process.argv[1]).href === import.meta.url) {
  main();
}
