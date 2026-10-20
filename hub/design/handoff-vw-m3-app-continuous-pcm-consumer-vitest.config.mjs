import { defineConfig } from "vitest/config";
import { createElementAdmissionsPlugin } from "/home/user/work/wt/vw-m3-app-continuous-pcm-consumer/config/vite/astridElementAdmissions.ts";
export default defineConfig({...{
  "root": "/home/user/work/wt/vw-m3-app-continuous-pcm-consumer",
  "cacheDir": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-continuous-pcm-consumer/vite-cache",
  "resolve": {
    "alias": {
      "@banodoco/timeline-composition/evaluation": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/clean-project/node_modules/@banodoco/timeline-composition/dist/evaluation.js",
      "@banodoco/timeline-composition/theme-api": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/clean-project/node_modules/@banodoco/timeline-composition/dist/theme-api.js",
      "@banodoco/timeline-composition/registry.generated": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/clean-project/node_modules/@banodoco/timeline-composition/dist/registry.generated.js",
      "@banodoco/timeline-composition/effects.generated": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/clean-project/node_modules/@banodoco/timeline-composition/dist/effects.generated.js",
      "@banodoco/timeline-composition/animations.generated": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/clean-project/node_modules/@banodoco/timeline-composition/dist/animations.generated.js",
      "@banodoco/timeline-composition/transitions.generated": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/clean-project/node_modules/@banodoco/timeline-composition/dist/transitions.generated.js",
      "@banodoco/timeline-composition/registries": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/clean-project/node_modules/@banodoco/timeline-composition/dist/registries.js",
      "@astrid/editor-sdk": "/home/user/work/wt/vw-m3-app-continuous-pcm-consumer/src/sdk/index.ts",
      "@": "/home/user/work/wt/vw-m3-app-continuous-pcm-consumer/src",
      "@test-react-refresh": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/clean-project/node_modules/@vitejs/plugin-react-swc/refresh-runtime.js",
      "@banodoco/timeline-schema": "/home/user/work/wt/vw-m3-app-continuous-pcm-consumer/src/test/shims/banodoco/timeline-schema.ts",
      "@banodoco/timeline-composition": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/clean-project/node_modules/@banodoco/timeline-composition/dist/index.js",
      "react": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/clean-project/node_modules/react",
      "react-dom": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/clean-project/node_modules/react-dom",
      "remotion": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/clean-project/node_modules/remotion",
      "@remotion/media": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/clean-project/node_modules/@remotion/media",
      "@remotion/layout-utils": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/clean-project/node_modules/@remotion/layout-utils",
      "@testing-library/react": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/clean-project/node_modules/@testing-library/react",
      "@testing-library/jest-dom": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/clean-project/node_modules/@testing-library/jest-dom",
      "vitest": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/clean-project/node_modules/vitest",
      "zod": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/clean-project/node_modules/zod",
      "zustand": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/clean-project/node_modules/zustand",
      "@astrid": "/home/user/work/wt/vw-m3-app-continuous-pcm-consumer/vendor/astrid-browser/astrid"
    }
  },
  "test": {
    "globals": true,
    "environment": "jsdom",
    "include": [
      "src/**/*.test.{ts,tsx}",
      "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-continuous-pcm-consumer/*.test.tsx",
      "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-continuous-pcm-consumer/*.test.ts"
    ],
    "setupFiles": [
      "/home/user/work/wt/vw-m3-app-continuous-pcm-consumer/src/test/reactRefreshSetup.ts",
      "/home/user/work/wt/vw-m3-app-continuous-pcm-consumer/src/test/setup.ts"
    ],
    "server": {
      "deps": {
        "inline": [
          "remotion",
          "@banodoco/timeline-composition"
        ]
      }
    }
  }
}, plugins: [createElementAdmissionsPlugin()]});
