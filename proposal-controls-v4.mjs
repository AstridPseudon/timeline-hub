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
const gitText = (args) => execFileSync('git', args, { cwd: root, encoding: 'utf8' });
const git = (args) => gitText(args).trimEnd();
const candidate = git(['rev-parse', 'HEAD']);
const before = gitText(['show', `${BASE}:${SOURCE}`]);
const after = gitText(['show', `${candidate}:${SOURCE}`]);
const patch = readFileSync(path.join(root, PATCH), 'utf8');
const mounted = gitText(['show', `${candidate}:${MOUNTED}`]);
const hook = gitText(['show', `${candidate}:${HOOK}`]);

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
  assert.equal(sha(before), 'a6468188ff21c4fd8bd397ff242b0260ee92ab6f2f90ac94786973eaf3c1e99a');
  assert.equal(sha(after), '8661fc919714d292c567844dc4f423855923077ca6a679a1398ec2a46154315b');
  assert.equal(sha(mounted), '10e58e89c0626363c3d99ae40515f09aaabdfade67f5a6d1c2426602304f901b');
  // Control metadata can be repaired before its harness commit; the source
  // consumed by lint/types must still match the existing committed candidate.
  assert.equal(git(['status', '--porcelain', '--untracked-files=normal', '--', '.',
    ':(exclude)proposal-controls-v4.mjs', ':(exclude)proposal-evidence-v4.txt', ':(exclude)proposed-v4.patch']), '',
    'only the three control artifacts may differ from the committed candidate');
  for (const [name, content] of [[SOURCE, after], [MOUNTED, mounted], [HOOK, hook]]) {
    assert.equal(readFileSync(path.join(root, name), 'utf8'), content, `${name} must match committed HEAD`);
  }
}

function assertPatchMatchesCandidate() {
  const actual = gitText(['diff', '--no-ext-diff', '--no-color', '--full-index', '--unified=0', BASE, candidate, '--', SOURCE]);
  assert.equal(patch, actual, 'proposal patch must be regenerated from immutable parent to current candidate');
  const evidence = readFileSync(path.join(root, 'proposal-evidence-v4.txt'), 'utf8');
  for (const [label, content] of [['source before', before], ['source after', after], ['mounted', mounted], ['patch', patch]]) {
    assert.ok(evidence.includes(`${label} SHA-256: ${sha(content)}\n`), `${label} evidence must contain the full actual hash`);
  }
  execFileSync('git', ['diff', '--check', BASE, candidate, '--', SOURCE], { cwd: root, stdio: 'pipe' });
  execFileSync('git', ['apply', '--reverse', '--check', '--unidiff-zero', PATCH], { cwd: root, stdio: 'pipe' });
}

function assertMountedProofIsProduction() {
  assert.match(hook, /sessionCreation = createLocalSaveSession\(/);
  assert.match(hook, /send: \(request, key\) => provider\.commitTimeline!\(request, key\)/);
  assert.match(hook, /await session\.recover\(owners\[0\]\)/);
  const lifecycle = section(mounted, 'async function mountedLifecycle(', '\ndescribe(');
  const accounting = section(mounted, 'function assertExactLifecycle(', '\nfunction makeBoundary(');
  assert.match(lifecycle, /renderHook\(\(\) => useTimelineSave\(/);
  assert.match(lifecycle, /commitTimeline: boundary\.post/);
  for (const mount of ['first', 'intermediate', 'restarted']) {
    assert.ok(lifecycle.includes(`const ${mount} = mount();`));
    assert.ok(lifecycle.includes(`${mount}.hook.unmount();`));
  }
  assert.match(lifecycle, /localSaveState\?\.status\)\.toBe\('saved'\)/);
  assert.match(lifecycle, /assertExactLifecycle\(boundary\.attempts, boundary\.forwarded,/);
  assert.match(lifecycle, /expect\(\(await createCommitOutbox\(\)\.list\(scope\)\)\[0\]\?\.intents\)\.toEqual\(\[\]\)/);
  assert.match(accounting, /expect\(attempts\)\.toHaveLength\(5\)/);
  assert.match(accounting, /attempts\.slice\(0, 4\).*\.toEqual\(\[a, a, a, a\]\)/);
  assert.match(accounting, /expect\(attempts\[4\]\)\.toMatchObject\(\{ body: b\.body, key: b\.key \}\)/);
  assert.match(accounting, /attempt\.url === url/);
  assert.match(accounting, /new URL\(attempt\.url\)\.origin === origin/);
  assert.match(accounting, /expect\(forwarded\.map\(.*\.toEqual\(\[a, a, b\]\)/);
  assert.match(accounting, /expect\(forwarded\)\.toHaveLength\(3\)/);
  assert.doesNotMatch(mounted, /makePage\s*\(|vm\.runInNewContext|send\(A\)|send\(B\)/);
  assert.match(after, /armRecoveryRetry/);
  assert.match(after, /observedUrls/);
  assert.match(after, /toHaveLength\(5\)/);
  assert.match(after, /toHaveLength\(3\)/);
}

if (['--hashes', '--lint', '--types'].some((mode) => process.argv.includes(mode))) {
  assertCommittedParentAndCandidate();
  assertPatchMatchesCandidate();
  assertMountedProofIsProduction();
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
  execFileSync(process.execPath, [path.join(root, 'node_modules/typescript/bin/tsc'),
    '--noEmit', '--pretty', 'false', '--incremental', 'false'], { cwd: root, stdio: 'inherit' });
  console.log('PASS: repository tsc --noEmit --pretty false --incremental false');
} else {
  test('uses immutable parent and current committed candidate source', () => {
    assertCommittedParentAndCandidate();
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
    assert.match(controls, /gitText\(\['show', `\$\{candidate\}:\$\{SOURCE\}`/);
  });
}
