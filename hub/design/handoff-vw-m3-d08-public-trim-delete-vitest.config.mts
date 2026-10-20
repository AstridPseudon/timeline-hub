import base from '/home/user/work/wt/vw-m3-d08-public-trim-delete/config/testing/vitest.config.ts';
export default {
  ...base,
  cacheDir: '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d08-public-trim-delete/vite-cache',
  test: { ...base.test, maxWorkers: 1 },
};
