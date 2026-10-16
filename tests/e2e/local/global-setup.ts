/** Builds the production bundle once unless an existing dist is newer than every input. */
import { execFileSync } from 'node:child_process';
import { existsSync, readdirSync, statSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const INPUTS = ['src', 'config', 'public', 'vendor', 'index.html', 'package.json', 'package-lock.json', 'tsconfig.json'];

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

export function distIsCurrent(dist = path.join(root, 'dist')): boolean {
  const built = path.join(dist, 'index.html');
  if (!existsSync(built)) return false;
  const builtAt = statSync(built).mtimeMs;
  return INPUTS.every((input) => newestMtime(path.join(root, input)) <= builtAt);
}

export default function globalSetup() {
  if (process.env.REIGH_DIRECT_DIST) return; // a caller-supplied build is used as is
  if (distIsCurrent()) {
    console.log('[direct] dist is current; skipping the build');
    return;
  }
  console.log('[direct] building the production bundle (npm run build)');
  execFileSync('npm', ['run', 'build'], { cwd: root, stdio: 'inherit', env: { ...process.env, NODE_OPTIONS: process.env.NODE_OPTIONS ?? '--max-old-space-size=4096' } });
}
