## Report: agt-m3-mouth-product-and-xfail-drop

**Status:** Unit 1 is done. Unit 2 is blocked. I did not create `DONE`; I wrote `BLOCKED` with the reason.

### Unit 1: drop clamp-off xfail rows (done)
- `tests/editing_conformance/fixtures/visual_compile_contract.json`: removed `overhang-clamp-off-end-frame` and `overhang-clamp-off-duration-frames`. The clamp-on rows are kept.
- `tests/editing_conformance/test_compile_contracts.py`: no edit needed. Its visual test reads the rows from the fixture, so dropping them there is enough.
- `design/visual-compile-contract.md`: added the 06:18 decision note, removed the two clamp-off table rows, and updated the stale references and measured counts.
- Deletion ledger: no clamp row exists there, so no note was added.
- Test run: `targeted` request `agt-m3-mouth-product-and-xfail-drop-targeted-1020062459-10614`, command `python -m pytest -q tests/editing_conformance/test_compile_contracts.py`. Result: **27 passed, 2 xfailed**, exit 0. The two xfails are the audio vectors 10-11, which are unchanged.
- Commit message: `commit-msg` in the worker dir.

### Unit 2: mouth product patch (blocked, nothing applied)
`git apply --check` fails on all three files, so I did not hand-port anything:
- `am-presenter/element.yaml`: the scene-diagnostics comment block the patch edits is absent from HEAD.
- `am-presenter/motion.ts`: HEAD has no `mouthEraseRect`, `mouthAnchor`, `anchorOr`, `PixelRect` or `pixelGeometry`. The patch context comes from base `751dd75e2`.
- `am-presenter/scene.ts`: does not exist in HEAD.

The patch's base is a different lineage from `tl/integration` (HEAD `470e4001`). Commit `8c46d913`, which adds the presenter scene and mouth inspection footprint, is not an ancestor of HEAD, and neither is `751dd75e2`. Applying the patch would mean re-porting the whole presenter scene capability, which the brief rules out.

**Decision needed from the orchestrator:** either bring the presenter scene lineage into `tl/integration` first and then re-apply the patch, or issue a new handoff against HEAD. I did not apply the review conditions (trim the `element.yaml` comment, update SSR/scene geometry expectations) because they only apply once the patch lands.

### Not run
No full suite was requested, per the brief. Nothing was pushed or committed by me. No build output or temp files were left in the worktree; `git status` shows only the two Unit 1 files.
