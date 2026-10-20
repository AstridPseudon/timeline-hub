const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {test} = require('node:test');

// Pure module: no renderer, Chromium or network. The Remotion version comes from a
// fake installed package under a temp project root.
const {sharedBrowserExecutable, browserRelativePath, BROWSER_ENV} = require('../shared-browser.mjs');

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'shared-browser-'));
const project = path.join(tmp, 'project');
const root = path.join(tmp, 'cache');
fs.mkdirSync(path.join(project, 'node_modules', '@remotion', 'renderer'), {recursive: true});
fs.writeFileSync(path.join(project, 'node_modules', '@remotion', 'renderer', 'package.json'), '{"version":"9.9.9"}');
test.after(() => fs.rmSync(tmp, {recursive: true, force: true}));

test('no shared copy yet: resolves to null so Remotion keeps its per-project default', () => {
  assert.equal(sharedBrowserExecutable({env: {}, projectRoot: project, root, platform: 'darwin', arch: 'arm64'}), null);
});

test('a copy for the installed Remotion version is used, other versions are not', () => {
  const rel = browserRelativePath('darwin', 'arm64');
  const exe = path.join(root, '9.9.9', rel);
  fs.mkdirSync(path.dirname(exe), {recursive: true});
  fs.writeFileSync(exe, '');
  assert.equal(sharedBrowserExecutable({env: {}, projectRoot: project, root, platform: 'darwin', arch: 'arm64'}), exe);
  assert.equal(sharedBrowserExecutable({env: {}, projectRoot: project, root: path.join(tmp, 'other'), platform: 'darwin', arch: 'arm64'}), null);
});

test('an explicit override wins and must exist', () => {
  const exe = path.join(tmp, 'explicit-browser');
  fs.writeFileSync(exe, '');
  assert.equal(sharedBrowserExecutable({env: {[BROWSER_ENV]: exe}, projectRoot: project, root}), exe);
  assert.throws(() => sharedBrowserExecutable({env: {[BROWSER_ENV]: path.join(tmp, 'missing')}, projectRoot: project, root}), /missing browser/);
});

test('layout matches Remotion download paths per platform', () => {
  assert.equal(browserRelativePath('darwin', 'arm64'), path.join('chrome-headless-shell', 'mac-arm64', 'chrome-headless-shell-mac-arm64', 'chrome-headless-shell'));
  assert.equal(browserRelativePath('linux', 'x64'), path.join('chrome-headless-shell', 'linux64', 'chrome-headless-shell-linux64', 'chrome-headless-shell'));
  assert.throws(() => browserRelativePath('freebsd', 'x64'));
});

test('a project without Remotion installed resolves to null instead of throwing', () => {
  assert.equal(sharedBrowserExecutable({env: {}, projectRoot: path.join(tmp, 'empty'), root, platform: 'darwin', arch: 'arm64'}), null);
});
