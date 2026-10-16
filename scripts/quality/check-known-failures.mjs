#!/usr/bin/env node
// Known-failure gate (testing plan R-6). A red test may stay in the suite only
// as an inverse test (it.fails / test.fails, or a `? it.fails : it` ternary)
// with this comment on the line directly above it:
//   // known-failure: <owner> | <expires YYYY-MM-DD> | <reason>
// Exits 1 when an entry is missing its comment, malformed, or expired, or when
// there are more than MAX_ENTRIES entries in total.
import fs from 'node:fs';
import path from 'node:path';

const REPO_ROOT = path.resolve(import.meta.dirname, '../..');
const SRC_DIR = path.join(REPO_ROOT, 'src');
const MAX_ENTRIES = 10;
const MARKER_RE = /\b(?:it|test)\.fails\b/;
const COMMENT_RE = /^\s*\/\/\s*known-failure:\s*([^|]+?)\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*(\S.*?)\s*$/;

const today = (() => {
  const d = new Date();
  const pad = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
})();

function listTestFiles(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) return listTestFiles(full);
    return /\.test\.tsx?$/.test(entry.name) ? [full] : [];
  });
}

const isRealDate = (value) => {
  const time = Date.parse(`${value}T00:00:00Z`);
  return !Number.isNaN(time) && new Date(time).toISOString().slice(0, 10) === value;
};

const entries = [];
const problems = [];

for (const file of listTestFiles(SRC_DIR)) {
  const lines = fs.readFileSync(file, 'utf8').split('\n');
  lines.forEach((line, index) => {
    if (!MARKER_RE.test(line)) return;
    const where = `${path.relative(REPO_ROOT, file)}:${index + 1}`;
    const match = index > 0 ? COMMENT_RE.exec(lines[index - 1]) : null;
    if (!match) {
      entries.push({ where, status: 'MALFORMED', detail: 'no well-formed known-failure comment directly above' });
      problems.push(`${where}: missing or malformed known-failure comment`);
      return;
    }
    const [, owner, expires, reason] = match;
    let status = 'ok';
    if (!isRealDate(expires)) status = 'MALFORMED';
    else if (expires < today) status = 'EXPIRED';
    entries.push({ where, status, detail: `owner=${owner} | expires=${expires} | ${reason}` });
    if (status !== 'ok') problems.push(`${where}: ${status === 'EXPIRED' ? `expired on ${expires}` : `invalid date ${expires}`}`);
  });
}

for (const entry of entries) {
  console.log(`${entry.status.padEnd(9)} ${entry.where} | ${entry.detail}`);
}
console.log(`known-failure entries: ${entries.length} (max ${MAX_ENTRIES}), checked against ${today}`);
if (entries.length > MAX_ENTRIES) {
  problems.push(`${entries.length} entries exceed the limit of ${MAX_ENTRIES}`);
}
for (const problem of problems) console.error(`FAIL ${problem}`);
process.exit(problems.length > 0 ? 1 : 0);
