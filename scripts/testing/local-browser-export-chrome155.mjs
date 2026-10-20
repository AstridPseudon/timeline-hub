import { execFileSync, spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { mkdtempSync, readFileSync, readdirSync, realpathSync, rmSync } from 'node:fs';
import { join, relative } from 'node:path';

const root = process.cwd();
const archive = join(root, 'vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz');
const composition = join(root, 'node_modules/@banodoco/timeline-composition');
const evidence = process.env.LOCAL_BROWSER_EXPORT_EVIDENCE_ROOT;
if (!evidence || !evidence.startsWith('/tmp/')) {
  throw new Error('LOCAL_BROWSER_EXPORT_EVIDENCE_ROOT must be an explicit /tmp path');
}
execFileSync('mkdir', ['-p', evidence]);
if (realpathSync(evidence) !== evidence) throw new Error('evidence root is not a real private path');

const sha256 = (bytes) => createHash('sha256').update(bytes).digest('hex');
const fileSha256 = (path) => sha256(readFileSync(path));
const packageVersion = (name) => JSON.parse(readFileSync(join(root, 'node_modules', name, 'package.json'), 'utf8')).version;
const fail = (message) => { throw new Error(message); };
const run = (file, args, options = {}) => execFileSync(file, args, { encoding: 'utf8', ...options }).trim();

if (process.version !== 'v20.19.4') fail(`unexpected Node: ${process.version}`);
const chrome = '/opt/google/chrome/chrome';
if (run(chrome, ['--product-version'], { stdio: ['ignore', 'pipe', 'ignore'] }) !== '155.0.8059.84') fail('unexpected Chrome155 version');
if (fileSha256(chrome) !== 'cb19b59995072b86cc7f887b3b1c7ab1f63518a7f2ed9f0d33249e1a040e2c76') fail('unexpected Chrome155 executable bytes');
if (fileSha256(archive) !== '9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738') fail('unexpected Composition archive bytes');
if (JSON.parse(readFileSync(join(composition, 'package.json'), 'utf8')).version !== '0.0.13') fail('unexpected Composition package version');

const archiveMembers = run('tar', ['-tzf', archive]).split('\n')
  .filter((member) => member.startsWith('package/') && !member.endsWith('/'))
  .map((member) => member.slice('package/'.length)).sort();
const walk = (directory) => readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
  const path = join(directory, entry.name);
  return entry.isDirectory() ? walk(path) : entry.isFile() ? [relative(composition, path)] : [];
}).sort();
const installedMembers = walk(composition);
if (archiveMembers.length !== 77 || installedMembers.length !== 77) fail(`Composition all77 count failed: ${archiveMembers.length}/${installedMembers.length}`);
if (archiveMembers.join('\n') !== installedMembers.join('\n')) fail('Composition all77 member list failed');
for (const member of archiveMembers) {
  const archiveHash = sha256(execFileSync('tar', ['-xOf', archive, `package/${member}`]));
  if (archiveHash !== fileSha256(join(composition, member))) fail(`Composition all77 byte mismatch: ${member}`);
}

for (const [name, expected] of [
  ['react', '18.3.1'],
  ['react-dom', '18.3.1'],
  ['remotion', '4.0.509'],
  ['@remotion/player', '4.0.509'],
  ['@remotion/web-renderer', '4.0.509'],
]) {
  if (packageVersion(name) !== expected) fail(`unexpected ${name} version`);
}
for (const [path, expected] of [
  ['node_modules/@remotion/player/dist/cjs/PlayerUI.js', '5dc9b4b89310609f57a718c641334d530b72ecf284fc1682610afcec208a4fbb'],
  ['node_modules/@remotion/player/dist/cjs/use-player-methods.js', 'ff50ab8b4ae86423fab18aa1ecf6c48c41501c4f7b527f05a55c2c36598def46'],
  ['node_modules/@remotion/player/dist/cjs/use-playback.js', '6c8369a19d7a29eab5dab4642799172d4f2a7e11dad39125edcb673ec5729fb0'],
  ['node_modules/@remotion/player/dist/esm/index.mjs', 'd3ef9728584c78e0e01cdb71ad72e3c6ddb36f96bfef90a4231d8b795e906b12'],
  ['node_modules/remotion/dist/esm/index.mjs', '5a1584f7660fa8fffa7eb8fe016b82a4d719e67d4b7904d4fa4f299eb1355f28'],
  ['node_modules/remotion/dist/cjs/audio/shared-audio-tags.js', '949ccec3419398183e8e22f63820a4a57cb8379befb184fbac9a3acde040c5b8'],
]) {
  if (fileSha256(join(root, path)) !== expected) fail(`render graph hash mismatch: ${path}`);
}

const privateRoot = mkdtempSync('/tmp/timeline-local-browser-export-');
const privateEnv = {
  ...process.env,
  PLAYWRIGHT_TIMELINE_DEVICES: '1',
  PLAYWRIGHT_CHROMIUM_EXECUTABLE: chrome,
  PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD: '1',
  PLAYWRIGHT_OUTPUT_DIR: evidence,
  PWTEST_CACHE_DIR: join(privateRoot, 'playwright-cache'),
  PRIVATE_VITE_CACHE_DIR: join(privateRoot, 'vite-cache'),
  TMPDIR: join(privateRoot, 'tmp'),
  XDG_RUNTIME_DIR: join(privateRoot, 'runtime'),
};
for (const path of [privateEnv.PWTEST_CACHE_DIR, privateEnv.PRIVATE_VITE_CACHE_DIR, privateEnv.TMPDIR, privateEnv.XDG_RUNTIME_DIR]) {
  execFileSync('mkdir', ['-p', path]);
}
console.log(JSON.stringify({
  preflight: 'PASS',
  node: process.version,
  chrome: run(chrome, ['--product-version'], { stdio: ['ignore', 'pipe', 'ignore'] }),
  composition: { version: '0.0.13', regularFiles: 77, archiveSha256: fileSha256(archive) },
  remotion: '4.0.509',
  player: '4.0.509',
  renderCase: 'audio-reactive-colour-export.spec.ts :: renders the pinned Astrid marker fixture with exact decoded frame boundaries',
  evidence,
}, null, 2));

try {
  const result = spawnSync(process.execPath, [
    'node_modules/@playwright/test/cli.js', 'test',
    '--config', 'playwright.local-browser-export.config.ts',
    '--project=timeline-devices',
    'tests/e2e/timeline/audio-reactive-colour-export.spec.ts',
    '--grep', 'renders the pinned Astrid marker fixture',
    '--workers=1',
  ], { env: privateEnv, stdio: 'inherit' });
  if (result.error) throw result.error;
  process.exitCode = result.status ?? 1;
} finally {
  rmSync(privateRoot, { recursive: true, force: true });
}
