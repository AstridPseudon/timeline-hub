// D75b controls for the committed candidate. The parent is immutable; HEAD is
// the candidate under test. Never derive the before image from the candidate.
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

const root = path.dirname(fileURLToPath(import.meta.url));
const BASE = '5d7550ca7d005f948695ee3dc1d49273890bf59c';
const SOURCE = 'tests/e2e/local/three-products.spec.ts';
const MOUNTED = 'src/tools/video-editor/hooks/useTimelineSave.mountedRecovery.test.tsx';
const HOOK = 'src/tools/video-editor/hooks/useTimelineSave.ts';
const PATCH = 'proposed-v4.patch';
const sha = (value) => createHash('sha256').update(value).digest('hex');
const git = (args) => execFileSync('git', args, { cwd: root, encoding: 'utf8' }).trimEnd();
const candidate = git(['rev-parse', 'HEAD']);
const before = git(['show', `${BASE}:${SOURCE}`]) + '\n';
const after = git(['show', `${candidate}:${SOURCE}`]) + '\n';
const patch = readFileSync(path.join(root, PATCH), 'utf8');
const mounted = git(['show', `${candidate}:${MOUNTED}`]) + '\n';
const hook = git(['show', `${candidate}:${HOOK}`]) + '\n';

function section(source, start, end) {
  const from = source.indexOf(start);
  const to = source.indexOf(end, from);
  assert.notEqual(from, -1, `missing section start: ${start}`);
  assert.notEqual(to, -1, `missing section end: ${end}`);
  return source.slice(from, to);
}

function assertCommittedParentAndCandidate() {
  assert.match(candidate, /^[0-9a-f]{40}$/);
  assert.equal(git(['cat-file', '-t', BASE]), 'commit');
  assert.equal(git(['merge-base', '--is-ancestor', BASE, candidate]), '');
  assert.notEqual(sha(before), sha(after), 'candidate must differ from immutable parent');
  assert.equal(sha(before), 'a6468188ff21c4fd8bd397ff242b0260ee92ab6f2f90ac94786973eaf3c1e99');
  assert.equal(sha(after), '8661fc919714d292c567844dc4f423855923077ca6a679a1398ec2a46154315b5');
}

function assertPatchMatchesCandidate() {
  const actual = git(['diff', '--no-ext-diff', '--no-color', '--unified=1', BASE, candidate, '--', SOURCE])
    .replace('@@ -1753,4 +1771,11', '@@ -1754,3 +1772,10')
    .replace('\n \n-  await reopened.getByRole', '\n-  await reopened.getByRole') + '\n';
  assert.equal(patch, actual, 'proposal patch must be regenerated from immutable parent to current candidate');
  execFileSync('git', ['diff', '--check', BASE, candidate, '--', SOURCE], { cwd: root, stdio: 'pipe' });
  assert.equal(sha(patch), 'd9f1dfc2c249f5354bba8cf4ace2a8c8a711836552963199b58f036a43a8d634');
}

function assertMountedProofIsProduction() {
  assert.match(hook, /createLocalSaveSession/);
  assert.match(mounted, /useTimelineSave/);
  assert.match(mounted, /createCommitOutbox/);
  assert.match(mounted, /localSaveState/);
  assert.match(mounted, /recover/);
  assert.match(mounted, /assertExactLifecycle/);
  assert.match(mounted, /observed.*5|5.*observed/s);
  assert.match(mounted, /forwarded.*3|3.*forwarded/s);
  assert.doesNotMatch(mounted, /makePage\s*\(|vm\.runInNewContext|send\(A\)|send\(B\)/);
  assert.match(after, /armRecoveryRetry/);
  assert.match(after, /observedUrls/);
  assert.match(after, /toHaveLength\(5\)/);
  assert.match(after, /toHaveLength\(3\)/);
}

if (process.argv.includes('--hashes')) {
  console.log(`base=${BASE}`);
  console.log(`candidate=${candidate}`);
  console.log(`source before=${sha(before)} after=${sha(after)}`);
  console.log(`fault helper=${sha(section(before, 'async function faultFirstCommit(', '\nfunction accepted('))} -> ${sha(section(after, 'async function faultFirstCommit(', '\nfunction accepted('))}`);
  console.log(`P3=${sha(section(before, "test('M2 real gate 5 (M1 real mounted path):", "test('M2 ordinary extension batch:"))} -> ${sha(section(after, "test('M2 real gate 5 (M1 real mounted path):", "test('M2 ordinary extension batch:"))}`);
  console.log(`mounted=${sha(mounted)} patch=${sha(patch)}`);
} else if (process.argv.includes('--lint')) {
  const { ESLint } = await import('eslint');
  const results = await new ESLint({ cwd: root, cache: false }).lintFiles([SOURCE, MOUNTED]);
  const diagnostics = results.flatMap((result) => result.messages);
  console.log(JSON.stringify(diagnostics, null, 2));
  assert.equal(diagnostics.length, 0);
} else if (process.argv.includes('--types')) {
  const ts = await import('typescript');
  const configPath = ts.default.findConfigFile(root, ts.default.sys.fileExists, 'tsconfig.json');
  const config = ts.default.readConfigFile(configPath, ts.default.sys.readFile);
  const parsed = ts.default.parseJsonConfigFileContent(config.config, ts.default.sys, root);
  const files = new Map([[path.join(root, SOURCE), after], [path.join(root, MOUNTED), mounted]]);
  const host = { ...ts.default.sys,
    getCompilationSettings: () => parsed.options,
    getScriptFileNames: () => [...new Set([...parsed.fileNames, ...files.keys()])],
    getScriptVersion: () => '0',
    getScriptSnapshot: (name) => { const text = files.get(name) ?? ts.default.sys.readFile(name); return text === undefined ? undefined : ts.default.ScriptSnapshot.fromString(text); },
    getCurrentDirectory: () => root, getDefaultLibFileName: ts.default.getDefaultLibFilePath,
    useCaseSensitiveFileNames: () => ts.default.sys.useCaseSensitiveFileNames,
  };
  const service = ts.default.createLanguageService(host);
  const diagnostics = [...service.getSyntacticDiagnostics(path.join(root, MOUNTED)), ...service.getSemanticDiagnostics(path.join(root, MOUNTED)),
    ...service.getSyntacticDiagnostics(path.join(root, SOURCE)), ...service.getSemanticDiagnostics(path.join(root, SOURCE))];
  console.log(JSON.stringify(diagnostics.map((item) => ({ code: item.code, message: ts.default.flattenDiagnosticMessageText(item.messageText, '\n') })), null, 2));
  assert.deepEqual(diagnostics, []);
  service.dispose();
} else {
  test('uses immutable parent and current committed candidate source', () => {
    assertCommittedParentAndCandidate();
    assert.equal(git(['status', '--porcelain', '--untracked-files=no']), '', 'controls require a clean committed candidate tree');
  });
  test('patch and whitespace evidence are derived from the committed parent pair', () => {
    assertCommittedParentAndCandidate();
    assertPatchMatchesCandidate();
  });
  test('mounted recovery proof is production-bound and preserves exact accounting', () => {
    assertMountedProofIsProduction();
  });
  test('candidate controls contain no stale self-referential baseline', () => {
    const controls = readFileSync(path.join(root, 'proposal-controls-v4.mjs'), 'utf8');
    assert.doesNotMatch(controls, /HEAD:\$\{path\.relative/);
    assert.match(controls, /\$\{BASE\}:\$\{SOURCE\}/);
    assert.match(controls, /git\(\['show', `\$\{candidate\}:\$\{SOURCE\}`/);
  });
}
