import { execFileSync } from 'node:child_process';
import { cpSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { describe, expect, it } from 'vitest';

const ROOT = path.resolve(__dirname, '../../..');
const SCRIPT = 'scripts/vendor-lock.mjs';
const LOCKS = execFileSync('git', ['ls-files', '--cached', '--others', '--exclude-standard', '*vendor.lock.json'], { cwd: ROOT, encoding: 'utf8' })
  .split('\n').filter(Boolean);

function check(root: string, lock: string): { status: number; output: string } {
  try {
    return { status: 0, output: execFileSync('node', [path.join(root, SCRIPT), 'check', path.join(root, lock)], { encoding: 'utf8', stdio: 'pipe' }) };
  } catch (error) {
    const failed = error as { status: number; stderr: string };
    return { status: failed.status, output: failed.stderr };
  }
}

describe('vendor.lock.json', () => {
  it('finds the Runtime locks', () => {
    expect(LOCKS).toEqual(expect.arrayContaining(['src/integrations/runtime/vendor.lock.json', 'vendor/timeline-schema/vendor.lock.json']));
  });

  it.each(LOCKS)('%s matches the vendored bytes', (lock) => {
    expect(check(ROOT, lock)).toMatchObject({ status: 0 });
  });

  it('names a file with a one-byte local change', () => {
    // The script resolves consumer paths against its own repo root, so plant the change in a temp copy of that tree.
    const copy = mkdtempSync(path.join(tmpdir(), 'vendor-lock-'));
    try {
      const [lockRelative] = LOCKS;
      const lock = JSON.parse(readFileSync(path.join(ROOT, lockRelative), 'utf8')) as { files: Record<string, unknown> };
      const [victim] = Object.keys(lock.files);
      for (const file of [...Object.keys(lock.files), lockRelative, SCRIPT]) cpSync(path.join(ROOT, file), path.join(copy, file), { recursive: true });
      writeFileSync(path.join(copy, victim), `${readFileSync(path.join(copy, victim), 'utf8')} `);
      const result = check(copy, lockRelative);
      expect(result.status).toBe(1);
      expect(result.output).toContain(`${victim}: edited locally`);
    } finally {
      rmSync(copy, { recursive: true, force: true });
    }
  });
});
