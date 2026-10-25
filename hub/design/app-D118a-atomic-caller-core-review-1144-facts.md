# D118a protected review facts

Result: PASS for the exact D118a source revision `8a4103dd16bb32306ca6c782dcd9a7a4a908de6d`.

The reviewed diff is one authorized production line in `astrid/packs/rendering/docs/scripts/timeline_document.py`: detached publication now calls `TimelineSession._capture_bundle(session_state)`. The existing private seam fetches the exact `(revision_id, publication_id)` pair and retains `_runtime_document` for the source-bound emitter. Public `TimelineSession._bundle` remains unchanged and still removes `_runtime_document`.

Protected evidence on clean Runtime `42aad0e92f6da8ea83dd0a382a87e3acd12651b0`, tree `085a5be70b56353deb41ae7d743336a4ccb7f29c`:

- Original atomic node: `1 passed in 2.57s`; XML SHA256 `f2a61f549070808035c8d4487bdab2d140a33551abd51e465288ae65277db8f2`.
- Existing private-pair source/wrong-pair/no-write controls: `4 passed in 18.19s`; XML SHA256 `32335c1595a84e29acb5f69e86597b905f9d1688c9ce5dfb985a041a94c56daf`.
- Ruff, mypy (`--follow-imports=skip`), external-cache `py_compile`, and `git diff --check`: pass.
- Original test SHA256 and AST are unchanged/equal to base; all non-target blob objects are equal across base and review head.

No source or test files were changed by this review. No full, browser, P2, P4, profile, acquisition, or adoption/gate claim is made.
