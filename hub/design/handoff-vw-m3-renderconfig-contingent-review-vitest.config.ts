import { createElementAdmissionsPlugin } from "/home/user/work/wt/vw-m3-renderconfig-contingent-review/config/vite/astridElementAdmissions.ts";
export default {
  plugins: [createElementAdmissionsPlugin()],
  "root": "/home/user/work/wt/vw-m3-renderconfig-contingent-review",
  "cacheDir": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-renderconfig-contingent-review/vite-cache",
  "resolve": {
    "alias": {
      "@": "/home/user/work/wt/vw-m3-renderconfig-contingent-review/src",
      "@test-react-refresh": "/home/user/work/wt/vw-m3-renderconfig-contingent-review/node_modules/@vitejs/plugin-react-swc/refresh-runtime.js",
      "@astrid/editor-sdk": "/home/user/work/wt/vw-m3-renderconfig-contingent-review/src/sdk/index.ts",
      "@astrid": "/home/user/work/wt/vw-m3-renderconfig-contingent-review/vendor/astrid-browser/astrid",
      "@banodoco/timeline-schema": "/home/user/work/wt/vw-m3-renderconfig-contingent-review/src/test/shims/banodoco/timeline-schema.ts",
      "fake-indexeddb": "/home/user/work/wt/vw-m3-renderconfig-contingent-review/vendor/fake-indexeddb/index.js",
      "react": "/home/user/work/wt/vw-m3-renderconfig-contingent-review/node_modules/react",
      "react-dom": "/home/user/work/wt/vw-m3-renderconfig-contingent-review/node_modules/react-dom",
      "remotion": "/home/user/work/wt/vw-m3-renderconfig-contingent-review/node_modules/remotion",
      "@remotion/layout-utils": "/home/user/work/wt/vw-m3-renderconfig-contingent-review/node_modules/@remotion/layout-utils",
      "@remotion/media": "/home/user/work/wt/vw-m3-renderconfig-contingent-review/node_modules/@remotion/media",
      "@workspace-effects": "/home/user/work/wt/vw-m3-renderconfig-contingent-review/vendor/banodoco-effects",
      "@workspace-animations": "/home/user/work/wt/vw-m3-renderconfig-contingent-review/vendor/banodoco-animations",
      "@workspace-transitions": "/home/user/work/wt/vw-m3-renderconfig-contingent-review/vendor/banodoco-transitions"
    },
    "dedupe": [
      "react",
      "react-dom",
      "remotion"
    ]
  },
  "test": {
    "globals": true,
    "environment": "jsdom",
    "testTimeout": 120000,
    "setupFiles": [
      "/home/user/work/wt/vw-m3-renderconfig-contingent-review/src/test/reactRefreshSetup.ts",
      "/home/user/work/wt/vw-m3-renderconfig-contingent-review/src/test/setup.ts"
    ],
    "include": [
      "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-renderconfig-contingent-review/donor.lifecycle.test.tsx",
      "/home/user/work/wt/vw-m3-renderconfig-contingent-review/src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx",
      "/home/user/work/wt/vw-m3-renderconfig-contingent-review/src/tools/video-editor/lib/canonicalRenderBounds.test.ts"
    ],
    "watch": false
  }
};
