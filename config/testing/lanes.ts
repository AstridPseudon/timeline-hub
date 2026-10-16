// Test lanes (testing plan UP.3, R-5). Tests listed here need files outside this
// repository: another repo's checkout or a local evidence directory. The default
// run excludes them; `npm run test:checkout` runs exactly them, so the two lanes
// together are the whole suite.
export const CHECKOUT_LANE = [
  // Reads Runtime's conformance vectors from a sibling Runtime worktree.
  'src/tools/video-editor/data/portableVisualSeamIntent.test.ts',
  // Re-runs Astrid's own scene-authoring test through @astrid (ASTRID_CHECKOUT).
  'src/tools/video-editor/runtime/astridSceneAuthoring.test.ts',
  // Checks the extension catalog against the selected Astrid checkout.
  'src/tools/video-editor/dev/localExtensions.catalog.test.ts',
  // Reads a scripted example from ../../runs (local evidence, not in git).
  'src/pages/Home/replay/scriptedReplay.test.ts',
];
