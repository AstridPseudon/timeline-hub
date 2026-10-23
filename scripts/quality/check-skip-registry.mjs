#!/usr/bin/env node
// Every skip and lane in config/testing/skipRegistry.mjs must be real and visible:
//  - each `ci` job id exists in .github/workflows/*.yml, and that job really runs the entry: `runs[job]` is the
//    command the entry needs, and the job's `run:` steps must contain it. Both sides are resolved through
//    package.json (`npm test`, `npm run X` become their script's commands, recursively), flags the registry does
//    not name are ignored, and a path the command names must exist. For a skip, a command that lists test files
//    explicitly must list every file that uses the skip. Not evaluated: which files a vitest or Playwright config
//    includes, and whether the job's `if:` or matrix lets it run;
//  - every skip carries its `applies` predicate (callers pass only the name);
//  - an entry with no CI job says why in `manual`, and an entry with CI jobs does not claim `manual`;
//  - every name passed to skipWhen / skipUnlessLane / declaredSkip / declaredSkipIf in a test is declared,
//    and every declared skip is used by at least one test (a stale entry is an invisible hole).
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { LANES, SKIP_REGISTRY } from '../../config/testing/skipRegistry.mjs';

const DEFAULT_REPO_ROOT = path.resolve(import.meta.dirname, '../..');
const SCAN_DIRS = ['src', 'tests', 'scripts'];
const USE = /\b(?:skipWhen|declaredSkip|declaredSkipIf)\(\s*(?:t\s*,\s*)?'([a-z0-9-]+)'/g;

function listFiles(dir, out = []) {
  if (!fs.existsSync(dir)) return out;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === 'node_modules' || entry.name === '__fixtures__') continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) listFiles(full, out);
    else if (/\.[cm]?[jt]sx?$/.test(entry.name)) out.push(full);
  }
  return out;
}

/** job id -> the text of its `run:` steps (single-line and block scalars), read without a YAML parser. */
function ciJobs(repoRoot) {
  const dir = path.join(repoRoot, '.github/workflows');
  const jobs = new Map();
  for (const file of fs.readdirSync(dir).filter((name) => name.endsWith('.yml'))) {
    const lines = (fs.readFileSync(path.join(dir, file), 'utf8').split(/^jobs:\s*$/m)[1] ?? '').split('\n');
    let job = null;
    for (let i = 0; i < lines.length; i++) {
      const jobMatch = /^  ([a-z][a-z0-9-]*):\s*$/.exec(lines[i]);
      if (jobMatch) {
        job = jobMatch[1];
        if (!jobs.has(job)) jobs.set(job, []);
        continue;
      }
      const run = job && /^(\s*)(?:- )?run:\s*(.*)$/.exec(lines[i]);
      if (!run) continue;
      if (/^[|>][+-]?$/.test(run[2])) {
        const indent = (lines[i + 1] ?? '').match(/^\s*/)[0].length;
        while (i + 1 < lines.length && (lines[i + 1].trim() === '' || lines[i + 1].match(/^\s*/)[0].length >= indent)) jobs.get(job).push(lines[++i].trim());
      } else {
        jobs.get(job).push(run[2].trim());
      }
    }
  }
  return jobs;
}

/** The leaf commands a command line runs: `a && b; c` split, `npm test` / `npm run X` replaced by script X's commands. */
function leafCommands(commandText, scripts, seen = new Set()) {
  const leaves = [];
  for (const raw of commandText.split(/\n|&&|\|\||;/)) {
    const command = raw.trim().replace(/^npx\s+/, '').replace(/^\.venv\/bin\//, '').replace(/\s-c\s/, ' --config ');
    if (!command) continue;
    const npm = /^npm\s+(?:run\s+)?([\w:.-]+)(?:\s+--\s.*)?$/.exec(command);
    const script = npm && Object.hasOwn(scripts, npm[1]) && !seen.has(npm[1]) ? npm[1] : null;
    if (script) leaves.push(...leafCommands(scripts[script], scripts, new Set([...seen, script])));
    else leaves.push(command);
  }
  return leaves;
}

const words = (command) => command.split(/\s+/).filter(Boolean);
const isFlag = (word) => word.startsWith('-');
const isTestFile = (word) => /\.(?:test|spec)\.[cm]?[jt]sx?$/.test(word);
/** `needle` runs inside `leaf`: same words in the same order, extra words and flags allowed in between. */
function runsWithin(needle, leaf) {
  const have = words(leaf);
  let at = 0;
  for (const word of words(needle)) {
    const found = have.indexOf(word, at);
    if (found < 0) return false;
    at = found + 1;
  }
  return true;
}

function checkRuns({ kind, name, entry, jobs, scripts, repoRoot, usedBy }) {
  const problems = [];
  for (const job of entry.ci) {
    if (!jobs.has(job)) { problems.push(`${kind} ${name}: no CI job "${job}"`); continue; }
    const needleText = entry.runs?.[job];
    if (!needleText) { problems.push(`${kind} ${name}: no \`runs\` command for CI job "${job}"; say which command in that job runs it`); continue; }
    const needles = leafCommands(needleText, scripts);
    for (const word of needles.flatMap(words)) {
      if (/^[\w./-]+\.(?:[cm]?[jt]s|json|ya?ml|py)$/.test(word) && !word.startsWith('-') && !fs.existsSync(path.join(repoRoot, word))) problems.push(`${kind} ${name}: \`runs\` for job "${job}" names ${word}, which does not exist`);
    }
    const leaves = leafCommands(jobs.get(job).join('\n'), scripts);
    for (const needle of needles) {
      const matches = leaves.filter((leaf) => runsWithin(needle, leaf));
      if (matches.length === 0) { problems.push(`${kind} ${name}: CI job "${job}" has no step that runs \`${needle}\` (its steps run: ${leaves.filter((leaf) => !/^(?:npm ci|playwright install|sudo|curl|echo|chmod|printf|magick|mkdir|cp|find|jq|python -m venv|pwsh)/.test(leaf)).join(' ; ') || 'nothing relevant'})`); continue; }
      for (const file of usedBy ?? []) {
        const explicit = matches.every((leaf) => words(leaf).some(isTestFile));
        if (explicit && !matches.some((leaf) => words(leaf).includes(file))) problems.push(`${kind} ${name}: CI job "${job}" runs \`${needle}\` on an explicit list of test files, and ${file} (which uses this skip) is not in it`);
      }
    }
  }
  return problems;
}

export function checkSkipRegistry({ repoRoot = DEFAULT_REPO_ROOT, skips = SKIP_REGISTRY, lanes = LANES } = {}) {
  const problems = [];
  const jobs = ciJobs(repoRoot);
  const scripts = JSON.parse(fs.readFileSync(path.join(repoRoot, 'package.json'), 'utf8')).scripts ?? {};
  const usedIn = new Map();
  const used = new Set();
  for (const dir of SCAN_DIRS) {
    for (const file of listFiles(path.join(repoRoot, dir))) {
      const rel = path.relative(repoRoot, file);
      if (/declared-?[sS]kip\.[cm]?[jt]s$/.test(rel) || /check-skip-registry|skipGuard\.test/.test(rel)) continue;
      for (const match of fs.readFileSync(file, 'utf8').matchAll(USE)) {
        used.add(match[1]);
        usedIn.set(match[1], [...new Set([...(usedIn.get(match[1]) ?? []), rel])]);
        if (!Object.hasOwn(skips, match[1])) problems.push(`${rel}: skip "${match[1]}" is not declared in config/testing/skipRegistry.mjs`);
      }
    }
  }
  for (const [kind, table] of [['skip', skips], ['lane', lanes]]) {
    for (const [name, entry] of Object.entries(table)) {
      if (kind === 'skip' && typeof entry.applies !== 'function') problems.push(`skip ${name}: no \`applies\` predicate; the registry, not the caller, decides when it skips`);
      problems.push(...checkRuns({ kind, name, entry, jobs: jobs, scripts, repoRoot, usedBy: kind === 'skip' ? usedIn.get(name) : undefined }));
      if (entry.ci.length === 0 && !entry.manual) problems.push(`${kind} ${name}: no CI job runs it; say why in "manual"`);
      if (entry.ci.length > 0 && entry.manual) problems.push(`${kind} ${name}: has CI jobs and a "manual" note; drop one`);
    }
  }
  for (const name of Object.keys(skips)) if (!used.has(name)) problems.push(`skip ${name}: declared but no test uses it`);
  return problems;
}

if (import.meta.url === pathToFileURL(process.argv[1] ?? '').href) {
  const problems = checkSkipRegistry();
  if (problems.length) {
    console.error('Skip registry problems:');
    for (const problem of problems) console.error(`  ${problem}`);
    process.exit(1);
  }
  const manual = [...Object.entries(SKIP_REGISTRY), ...Object.entries(LANES)].filter(([, entry]) => entry.manual);
  console.log(`check-skip-registry: ${Object.keys(SKIP_REGISTRY).length} declared skips, ${Object.keys(LANES).length} lanes; ${manual.length} with no CI job:`);
  for (const [name, entry] of manual) console.log(`  MANUAL ${name}: ${entry.manual}`);
}
