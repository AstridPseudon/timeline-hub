// One chrome-headless-shell for every Astrid Remotion stack.
//
// Remotion downloads its browser into `<project>/node_modules/.remotion` (the
// nearest package.json above the cwd), so each stack carried its own 193 MB
// copy. This module points Remotion at one copy per Remotion version under
// ~/Library/Caches/astrid-remotion-browser/<version>/, which
// scripts/fetch-shared-browser.mjs fills once. When that copy is absent the
// functions return null and Remotion keeps its per-project default, so nothing
// here downloads during a render.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

// Overrides the shared location (an explicit path must exist; it is never ignored).
export const BROWSER_ENV = 'ASTRID_REMOTION_BROWSER_EXECUTABLE';

// Remotion evaluates remotion.config.ts (and what it imports) as bundled CommonJS, where import.meta is empty:
// an unconditional fileURLToPath(import.meta.url) here threw while the config loaded, so no render could start.
// Native ESM (the frame worker, the scripts) keeps the module-relative default; the config loader runs from
// the selected Remotion root, so its working directory is the project.
const here = typeof import.meta.url === 'string' ? path.dirname(fileURLToPath(import.meta.url)) : null;
const defaultProjectRoot = () => (here === null ? process.cwd() : path.resolve(here, '..'));

export const sharedBrowserRoot = () =>
  path.join(os.homedir(), 'Library', 'Caches', 'astrid-remotion-browser');

// Remotion's own layout inside a download: chrome-headless-shell/<platform>/<dir>/chrome-headless-shell.
export function browserPlatformDir(platform = process.platform, arch = process.arch) {
  if (platform === 'darwin') return arch === 'arm64' ? 'mac-arm64' : 'mac-x64';
  if (platform === 'linux' && arch === 'x64') return 'linux64';
  if (platform === 'win32' && arch === 'x64') return 'win64';
  throw new Error(`no chrome-headless-shell layout for ${platform}/${arch}`);
}

export function browserRelativePath(platform = process.platform, arch = process.arch) {
  const dir = browserPlatformDir(platform, arch);
  const exe = platform === 'win32' ? 'chrome-headless-shell.exe' : 'chrome-headless-shell';
  return path.join('chrome-headless-shell', dir, `chrome-headless-shell-${dir}`, exe);
}

// The Remotion version this project renders with, read from its installed package
// (not via require.resolve: @remotion/renderer's exports map may hide package.json).
// Returns null when the package is not installed: the config must still load (tests, typecheck).
export function remotionRendererVersion(projectRoot = defaultProjectRoot()) {
  const pkg = path.join(projectRoot, 'node_modules', '@remotion', 'renderer', 'package.json');
  try {
    return JSON.parse(fs.readFileSync(pkg, 'utf8')).version ?? null;
  } catch {
    return null;
  }
}

export function sharedBrowserExecutable({
  env = process.env,
  projectRoot = defaultProjectRoot(),
  root = sharedBrowserRoot(),
  platform = process.platform,
  arch = process.arch,
} = {}) {
  const explicit = env[BROWSER_ENV];
  if (explicit) {
    if (!fs.existsSync(explicit)) throw new Error(`${BROWSER_ENV} points at a missing browser: ${explicit}`);
    return explicit;
  }
  const version = remotionRendererVersion(projectRoot);
  if (!version) return null;
  const candidate = path.join(root, version, browserRelativePath(platform, arch));
  return fs.existsSync(candidate) ? candidate : null;
}
