# P3 integrated callers / operations handoff

## Verdict

**BLOCKED: no P3 operational-row update.** Integrated source and all bounded
caller checks passed except the required App project typecheck. It fails at
`src/tools/travel-between-images/components/shotTimelineDataProvider.ts:771`
with TS2322 because the shared-popup ADD command's `args.row` is
`Record<string, unknown>` where generated `EditCommand` requires JSON.

The source remains untouched. This is the reviewed A3 four-file delta; the
source-only fix is outside this task. The current P3 row remains unchanged at
line SHA-256
`100915e1363fe582a6581300a0dd209d233de207f7a8bcf2a81b0d3fddcf5dc5`.

## Evidence

- App: `2d3d14d998be2b59fb017b4c0f2458c3a7340423`, tree
  `7cd3b112b824711cebb87a6e25ce249461d574cc`.
- Reviewed receipts retained: Move `f2d6d62c7b2ed241c2eed9295969ab44479a667e`,
  Undo/Redo `2980bbe06db85ecc3531e493e4390e3576cfbf88`, shared popup
  `7fd2a6d0cca6afa172a582a185fb0bd3df441d7a`; exact non-overlap blobs match. The combined
  `timelineLocalSaveHandoff.ts` blob is `1c6176d2…` and equals the integrated
  first parent, preserving both move-intent reads and guarded Undo/Redo.
- Current diff from `890b9561666c3619f69335dd747b15e042b3a9a3` is exactly the
  17 authorized files; no P3 spec, generated, lock, package, or suite body
  changed. Original P3 source is the merged `18354adfa…` blob.
- Targeted union: 12 files / 255 tests passed.
- Root and Node typechecks, scoped lint, diff check, normal `34eac004` lock,
  private `819acf` graph (80 files), and exact one-test selector all passed.
- Runtime pinned `.venv/bin/python` was restored and exists; row-PYTHONPATH
  imports resolve from Agent b8 and Runtime a5d. No body/service/browser/build
  or central test run occurred.

The row must not be promoted until the App TS2322 is dispositioned and the
App typecheck passes. Then use only the existing row, with Agent
`b8e5076250…`/tree `eee66dc…` and Runtime `a5d4258312…`/tree `f74b016e…`,
and preserve its selector, private graph, normal client, and original body.
