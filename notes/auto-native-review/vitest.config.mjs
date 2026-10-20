import path from 'node:path';

const candidate = process.env.AUTO_NATIVE_CANDIDATE;
if (!candidate) throw new Error('AUTO_NATIVE_CANDIDATE must name the frozen candidate archive');
export default {
  cacheDir: process.env.AUTO_NATIVE_CACHE,
  resolve: { alias: {
    '@': path.join(candidate, 'src'),
    'vitest': '/tmp/app-coherent-deps12/node_modules/vitest/dist/index.js',
  } },
  test: { environment: 'node', include: ['notes/auto-native-review/review.test.ts'] },
};
