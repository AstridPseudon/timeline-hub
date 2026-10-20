import { defineConfig } from 'vitest/config';
import path from 'node:path';

const root = process.env.AUDIT_APP_ROOT ?? process.cwd();
export default defineConfig({
  root,
  cacheDir: path.join(process.env.AUDIT_NOTES!, 'cache', path.basename(root)),
  server: { fs: { allow: [root, process.cwd(), '/home/user/work/app'] } },
  resolve: {
    alias: {
      '@': path.join(root, 'src'),
      '@astrid/editor-sdk': path.join(root, 'src/sdk/index.ts'),
      '@workspace-effects': path.join(root, 'vendor/banodoco-effects'),
      '@workspace-animations': path.join(root, 'vendor/banodoco-animations'),
      '@workspace-transitions': path.join(root, 'vendor/banodoco-transitions'),
      '@test-react-refresh': path.join(root, 'node_modules/@vitejs/plugin-react-swc/refresh-runtime.js'),
      'fake-indexeddb': path.join(root, 'vendor/fake-indexeddb/index.js'),
      '@banodoco/timeline-schema': path.join(root, 'src/test/shims/banodoco/timeline-schema.ts'),
    },
  },
  test: {
    globals: true,
    environment: 'jsdom',
    cache: false,
    include: ['src/**/*.test.{ts,tsx}', 'notes/bootstrap-current-contract-audit/*.test.ts'],
    setupFiles: [path.join(root, 'src/test/reactRefreshSetup.ts'), path.join(root, 'src/test/setup.ts')],
  },
});
