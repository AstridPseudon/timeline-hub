/** Builds the hosted production bundle once unless an existing dist is newer than every input and was built for the Runtime door. */
import { execFileSync } from 'node:child_process';
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const INPUTS = ['src', 'config', 'public', 'vendor', 'index.html', 'package.json', 'package-lock.json', 'tsconfig.json'];
/** The default Runtime door origin `npm run build:hosted` compiles in (package.json). */
const DEFAULT_HOSTED_ORIGIN = 'http://127.0.0.1:17340';

/** A central browser lane may give the hosted build an owned per-run door port. */
function hostedOrigin(): string {
  return process.env.VITE_RUNTIME_ORIGIN?.trim() || DEFAULT_HOSTED_ORIGIN;
}

function newestMtime(entry: string): number {
  let stat;
  try { stat = statSync(entry); } catch { return 0; }
  if (!stat.isDirectory()) return stat.mtimeMs;
  let newest = stat.mtimeMs;
  for (const child of readdirSync(entry, { withFileTypes: true })) {
    if (child.name === 'node_modules' || child.name === 'dist') continue;
    newest = Math.max(newest, newestMtime(path.join(entry, child.name)));
  }
  return newest;
}

/** True when the built bundle points at the door origin (the hosted build, not a plain `npm run build`). */
export function distIsHosted(dist = path.join(root, 'dist')): boolean {
  const assets = path.join(dist, 'assets');
  if (!existsSync(assets)) return false;
  return readdirSync(assets).some((name) => name.endsWith('.js')
    && readFileSync(path.join(assets, name), 'utf8').includes(hostedOrigin()));
}

export function distIsCurrent(dist = path.join(root, 'dist')): boolean {
  const built = path.join(dist, 'index.html');
  if (!existsSync(built)) return false;
  const builtAt = statSync(built).mtimeMs;
  return INPUTS.every((input) => newestMtime(path.join(root, input)) <= builtAt) && distIsHosted(dist);
}

export default function globalSetup() {
  if (process.env.ASTRID_APP_DIRECT_DIST) return; // a caller-supplied build is used as is
  if (distIsCurrent()) {
    console.log('[direct] hosted dist is current; skipping the build');
    return;
  }
  const script = process.env.VITE_RUNTIME_ORIGIN?.trim() ? 'build' : 'build:hosted';
  console.log(`[direct] building the hosted production bundle (npm run ${script})`);
  execFileSync('npm', ['run', script], { cwd: root, stdio: 'inherit', env: { ...process.env, NODE_OPTIONS: process.env.NODE_OPTIONS ?? '--max-old-space-size=4096' } });
  if (!distIsHosted()) throw new Error(`npm run ${script} did not compile ${hostedOrigin()} into dist/assets`);
}
