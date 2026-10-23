import base from '/Users/hannahomalley/Developer/astrid-video/astrid-local/labs/app-shots/config/testing/vitest.config';
const appModules = '/Users/hannahomalley/Developer/astrid-video/astrid-local/labs/app-extensions/node_modules';
const T = '/Users/hannahomalley/Developer/astrid-video/astrid-local/labs/astrid-r2-04/tests/packs/rendering/';
export default {
  ...base,
  resolve: {
    ...base.resolve,
    alias: [
      ...(Array.isArray(base.resolve?.alias) ? base.resolve.alias : Object.entries(base.resolve?.alias ?? {}).map(([find, replacement]) => ({ find, replacement }))),
      { find: /^@testing-library\/react$/, replacement: `${appModules}/@testing-library/react/dist/index.js` },
      { find: /^@testing-library\/dom$/, replacement: `${appModules}/@testing-library/dom/dist/index.js` },
    ],
  },
  test: {
    ...base.test,
    include: ['world_explorer_panel.test.tsx','world_explorer_model.test.ts','world_explorer_authoring.test.ts','world_explorer_extension.test.tsx','world_explorer_roam.test.tsx','world_explorer_camera.test.ts','world_explorer_timebar.test.tsx','world_explorer_library.test.ts','scene_protocol.test.ts','scene_surface_lifecycle.test.tsx','live_scene_authoring.test.ts','shot_stills.test.tsx','shot_still_renderer.test.tsx','shot_gallery.test.tsx'].map(n => `${T}test_${n}`),
    exclude: [],
  },
};
