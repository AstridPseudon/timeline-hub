import base from '/home/user/work/wt/vw-m3-audio-compile-vector-reconcile/config/testing/vitest.config.ts';
import fs from 'node:fs';
import path from 'node:path';
const worker = '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-audio-compile-vector-reconcile';
const artifact = path.join(worker, '../vw-m3-envelope-public-clock-join/artifact/package');
const pkg = JSON.parse(fs.readFileSync(path.join(artifact, 'package.json'), 'utf8'));
const aliases = Object.entries(pkg.exports).map(([key, value]) => ({
  find: '@banodoco/timeline-composition' + (key === '.' ? '' : key.slice(1)),
  replacement: path.join(artifact, typeof value === 'string' ? value : value.import),
}));
export default {
  ...base, cacheDir: path.join(worker, 'vite-cache'),
  resolve: { ...base.resolve, alias: [
    ...aliases.sort((a, b) => b.find.length - a.find.length),
    ...Object.entries(base.resolve.alias).map(([find, replacement]) => ({ find, replacement })),
  ] },
  test: { ...base.test, maxWorkers: 1, pool: 'threads' },
};
