export default {
  root: '/home/user/work/wt/vw-m3-tab-clean-install-source-compose',
  resolve: {alias: {'@astrid/editor-sdk': '/home/user/work/wt/vw-m3-tab-clean-install-source-compose/src/sdk/index.ts', '@': '/home/user/work/wt/vw-m3-tab-clean-install-source-compose/src'}},
  cacheDir: '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-source-compose/vite-cache',
  test: {
    environment: 'node',
    include: ['src/tools/video-editor/compositions/playerEvaluation.test.ts'],
    watch: false,
    maxWorkers: 1,
  },
};
