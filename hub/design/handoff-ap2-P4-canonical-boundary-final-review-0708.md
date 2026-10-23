# P4 canonical-boundary final review

## Disposition

**SOURCE PASS. OPS target-row PASS. RERUN READINESS FAIL/not ready.**

### Source

Reviewed candidate `dd0bd73e2cef92cdca8213d26e175e350b484af6`
(tree `e762ea942c4139b97f782a1882e7de3453b42cb8`) against
`a809764ae56f9fc13845464138c9ad4cd56e2575`
(tree `15b155b7872b24e640b82fb93382970eb6e837c4`).

Exactly one tracked path changed:
`tests/editing_conformance/test_p4_ten_note_v2_runtime.py`.

Ten-note blob:
`cdb186d001fe8bd7476c2a059ee65e9a312dbec5` →
`b8876628d100897a9dcda6750fc5395a3b5b41f3`.
Rerun blob stayed exactly
`cbd332db227ecb9c6254e8ced0af72c3de91821e`.

The 22407 cause is confirmed in the actual SDK: ordinary
`timeline.open()` calls `fetch_bundle` without a publication pin
(`commit_session.py:252-254`); `_remote_timeline.py:180-207` only restores
provider-only `_runtime_document` after an authenticated exact
revision/publication receipt and canonical-closure equality check. The
correction uses that existing exact read, asserts private-cache absence on
ordinary initial and restarted opens, and preserves the original request,
reply, physical/shared-closure, ten-note, per-step undo/redo, show/history,
restart, opaque/null, absence, and source-mapping assertions. No source,
helper, fixture, rerun, synthetic cache/document, guard waiver, or product
change was made.

Checks passed: 2-test collection (unknown pytest `timeout` warning), scoped
Ruff, private-cache Mypy, `git diff --check`, and offline canonical
round-trip for shared/non-shared fixtures. No live execution.

### Rerun readiness

The untouched rerun is not ready: `_assert_full_closure()` at
`test_p4_note_rerun_v2_runtime.py:142-163` reads
`source_mapping["_runtime_document"]`, and it is called on the ordinary
post-restart `timeline.open()` bundle at lines 285-293. That bundle
deliberately lacks the private cache, so the rerun has the same deterministic
KeyError boundary issue. It remains unmodified.

### OPS

Verified clean Runtime checkout:
`/home/user/work/wt/rt-pin-a5d42583`,
HEAD `a5d4258312c979024865ee704da2d632ca5b2730`,
tree `f74b016ea837f8148db4a602c972073a226ed177`.

The sole `agent p4-v2-http-nodes` row is 1,379 bytes,
SHA-256 `fafc5fa04275856881cb8188f782f00b73caf9492640a34369799738bd0af948`;
it is a literal-only substitution of the reviewed 1cf path/SHA, retaining the
tree, parser, import-origin guards, selector, and pytest suffix. Runtime and
Agent import origins passed. Current outside-row snapshot is 89,481 bytes,
SHA-256 `5458eda3b592be14dc93de9e2d0ebeaae55b1760f2f90e40601266d135d29981`;
the immediate 0701 operation evidence recorded 89,481 bytes and
`6c092f5ca15f838165820b58de7c518d5ea9dbd5fb5a7231839cf06986f1a145`, with
later unrelated shared-config row activity accounting for the current snapshot
difference. Retained Runtime independent/integrated 49-pass evidence was not
rerun.

No HTTP/body/service/socket/browser/build/full/request was run. Manager next:
one original ten-note live run, then separately repair and run the rerun.

