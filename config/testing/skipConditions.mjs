// The conditions behind the skips declared in skipRegistry.mjs. Each returns `false` when the test must run, or
// `true` / a string (the reason) when the skip applies. Callers never pass their own boolean: they pass the registry
// name, and the helper (src/test/declaredSkip.ts, tests/e2e/support/declaredSkip.ts, scripts/quality/declared-skip.mjs)
// evaluates the condition here. A condition checks the one thing it names and rethrows anything else, so an
// unrelated error is a failing test and never a declared skip.
import { execFileSync } from 'node:child_process';
import { accessSync, constants as fsConstants, existsSync, mkdtempSync, rmSync, statSync, symlinkSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const REPO_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');

/** Where the direct journey finds the sibling Runtime checkout and the production build. */
export const RUNTIME_CHECKOUT = path.resolve(process.env.ASTRID_RUNTIME_CHECKOUT ?? path.join(REPO_ROOT, '..', 'astrid-runtime'));
export const DIST_DIR = path.resolve(process.env.ASTRID_APP_DIRECT_DIST ?? path.join(REPO_ROOT, 'dist'));

export function runtimePython() {
  const explicit = process.env.ASTRID_RUNTIME_PYTHON;
  if (explicit) {
    const candidate = path.resolve(explicit);
    try {
      accessSync(candidate, fsConstants.X_OK);
      if (statSync(candidate).isFile()) return candidate;
    } catch { /* the caller receives the normal unavailable reason below */ }
    return null;
  }
  const python = path.join(RUNTIME_CHECKOUT, '.venv', 'bin', 'python');
  return existsSync(python) ? python : null;
}

/** Why the direct-journey harness cannot run here, or null when it can. */
export function harnessUnavailableReason() {
  if (process.env.ASTRID_RUNTIME_PYTHON && !runtimePython()) return `ASTRID_RUNTIME_PYTHON is not an executable file: ${path.resolve(process.env.ASTRID_RUNTIME_PYTHON)}`;
  if (!runtimePython()) return `Runtime venv not found at ${RUNTIME_CHECKOUT}/.venv (set ASTRID_RUNTIME_CHECKOUT)`;
  if (!existsSync(path.join(DIST_DIR, 'index.html'))) return `no production build at ${DIST_DIR} (run npm run build, or use npm run test:e2e:direct)`;
  try {
    execFileSync('openssl', ['version'], { stdio: 'ignore' });
  } catch (error) {
    if (error?.code === 'ENOENT') return 'openssl is required to make the test certificate';
    throw error;
  }
  return null;
}

/**
 * Why stock Chromium cannot decode the harness's generated clip (no ffmpeg with a VP8 encoder), or null.
 * The harness (tests/e2e/local/support/harness.ts) makes the clip only when this is null, and a failure to make it
 * then is an error, not a fallback.
 */
export function ffmpegUnavailableReason() {
  let encoders;
  try {
    encoders = execFileSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-encoders'], { encoding: 'utf8' });
  } catch (error) {
    if (error?.code === 'ENOENT') return 'ffmpeg is not installed; the fallback MP4 cannot be decoded by stock Chromium';
    throw error;
  }
  return /\blibvpx\b/.test(encoders) ? null : 'ffmpeg has no libvpx encoder; the fallback MP4 cannot be decoded by stock Chromium';
}

/** True for exactly the error a symlink attempt raises when the process lacks the privilege to make one. */
export function isSymlinkPermissionError(error) {
  return (error?.code === 'EPERM' || error?.code === 'EACCES') && error?.syscall === 'symlink';
}

/** True when this process may not create symlinks: it tries one in a temp dir. Any other failure is thrown. */
export function symlinkCreationRefused() {
  const dir = mkdtempSync(path.join(tmpdir(), 'symlink-probe-'));
  try {
    symlinkSync(path.join(dir, 'target'), path.join(dir, 'link'));
    return false;
  } catch (error) {
    if (isSymlinkPermissionError(error)) return true;
    throw error;
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}

export const isWindows = () => process.platform === 'win32';
export const macosLockfMissing = () => process.platform !== 'darwin' || !existsSync('/usr/bin/lockf');
