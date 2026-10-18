// Test lanes (testing plan UP.3, R-5). Tests listed here need files outside this
// repository: another repo's checkout. The default run excludes them;
// `npm run test:checkout` runs exactly them, so the two lanes together are the
// whole suite.
export const CHECKOUT_LANE = [
  // Reads Runtime's conformance vectors from a sibling Runtime worktree.
  'src/tools/video-editor/data/portableVisualSeamIntent.test.ts',
  // Runs Astrid's pack-owned scene-authoring test through @astrid (ASTRID_CHECKOUT).
  // Astrid has no JS runner, so this wrapper is the only place that test executes.
  'src/tools/video-editor/runtime/astridSceneAuthoring.test.ts',
  // Checks the extension catalog against the selected Astrid checkout.
  'src/tools/video-editor/dev/localExtensions.catalog.test.ts',
];
