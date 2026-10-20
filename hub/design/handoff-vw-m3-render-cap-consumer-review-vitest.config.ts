// Offline frozen-source review: original config aliases/setup/plugin; no external Astrid checkout discovery.
import { defineConfig } from 'vitest/config';
import path from 'path';
import { createElementAdmissionsPlugin } from '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-render-cap-consumer-review/app-source-e6c4aae/config/vite/astridElementAdmissions';
import { resolveAstridSource, validateAstridToolCatalog } from '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-render-cap-consumer-review/app-source-e6c4aae/config/vite/astridSource';
import { CHECKOUT_LANE } from '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-render-cap-consumer-review/app-source-e6c4aae/config/testing/lanes';

const projectRoot = '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-render-cap-consumer-review/app-source-e6c4aae';
const checkoutLane = process.env.VITEST_LANE === 'checkout';
const astridSource = { checkout: '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-render-cap-consumer-review/agent-source-d874', sourceRoot: '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-render-cap-consumer-review/agent-source-d874/astrid' };
const astridPublicSource = undefined;
export default defineConfig({
  root: projectRoot,
  cacheDir: '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-render-cap-consumer-review/vite-cache',
  plugins: [createElementAdmissionsPlugin()],
  resolve: {
    alias: {
      '@': path.resolve(projectRoot, 'src'),
      '@test-react-refresh': path.resolve(projectRoot, 'node_modules/@vitejs/plugin-react-swc/refresh-runtime.js'),
      '@astrid/editor-sdk': path.resolve(projectRoot, 'src/sdk/index.ts'),
      ...(astridSource ? { '@astrid': astridSource.sourceRoot } : {}),
      ...(astridPublicSource ? { '@astrid-public': astridPublicSource.sourceRoot } : {}),
      'fake-indexeddb': path.resolve(projectRoot, 'vendor/fake-indexeddb/index.js'),
      // Share one React/Remotion runtime with Composition and linked host elements.
      'react': path.resolve(projectRoot, 'node_modules/react'),
      'react-dom': path.resolve(projectRoot, 'node_modules/react-dom'),
      'remotion': path.resolve(projectRoot, 'node_modules/remotion'),
      '@remotion/layout-utils': path.resolve(projectRoot, 'node_modules/@remotion/layout-utils'),
      '@remotion/media': path.resolve(projectRoot, 'node_modules/@remotion/media'),
      '@banodoco/timeline-schema': path.resolve(projectRoot, 'src/test/shims/banodoco/timeline-schema.ts'),
    },
    dedupe: [
      'three',
      '@remotion/three',
      'react',
      'react-dom',
      'remotion',
      '@remotion/layout-utils',
      '@banodoco/timeline-composition',
    ],
  },
  server: {
    fs: {
      // Allow Vite to read from sibling banodoco-workspace.
      allow: [
        path.resolve(projectRoot, '..', '..'),
        ...(astridSource ? [astridSource.checkout] : []),
        ...(astridPublicSource ? [astridPublicSource.checkout] : []),
      ],
    },
  },
  test: {
    globals: true,
    // Hang guard only (testing plan R-10): durations never fail a run, so the
    // per-test and per-hook ceilings are generous; only a genuine hang trips them.
    testTimeout: 120_000,
    hookTimeout: 120_000,
    environment: 'jsdom',
    include: checkoutLane
      ? CHECKOUT_LANE
      : ['src/**/*.test.{ts,tsx}', '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-render-cap-consumer-review/carrier-proof.test.ts'],
    exclude: [
      ...(checkoutLane ? [] : CHECKOUT_LANE),
      'supabase/functions/**',
      // This suite imports Astrid's selected Remotion composition and has its
      // own config so its linked workspace aliases resolve to Astrid's pack.
      'src/tools/video-editor/runtime/astridSceneComposition.test.tsx',
    ],
    // Keep Composition and the test providers on one Remotion context instance.
    server: {
      deps: {
        inline: ['remotion', '@banodoco/timeline-composition'],
      },
    },
    setupFiles: [
      path.resolve(projectRoot, 'src/test/reactRefreshSetup.ts'),
      path.resolve(projectRoot, 'src/test/setup.ts'),
    ],
  },
});
