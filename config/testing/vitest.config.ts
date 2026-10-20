import { defineConfig } from 'vitest/config';
import path from 'path';
import { createElementAdmissionsPlugin } from '../vite/astridElementAdmissions';
import { resolveAstridSource, validateAstridToolCatalog } from '../vite/astridSource';
import { CHECKOUT_LANE } from './lanes';

const projectRoot = path.resolve(__dirname, '../..');
const checkoutLane = process.env.VITEST_LANE === 'checkout';
const astridSource = resolveAstridSource();
if (astridSource) validateAstridToolCatalog(astridSource.sourceRoot);
const astridPublicSource = resolveAstridSource(
  process.env.ASTRID_PUBLIC_CHECKOUT ?? '',
  'ASTRID_PUBLIC_CHECKOUT',
);
export default defineConfig({
  root: projectRoot,
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
      : ['src/**/*.test.{ts,tsx}'],
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
