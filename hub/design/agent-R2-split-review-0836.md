# R2 split inverse review

Review result: **PASS (bounded Agent repair)**.

Reviewed exact HEAD `f7fcb72827405ea938555db92827a5095f02a3a5`, tree
`1f160774f677b1be16a1089e9034a0a3a7125143`, parent
`b8e5076250cc37cadf88c1ce699f2a05511fb909`. The diff is exactly five
production lines in `astrid/sdk/timeline/inverse.py` plus the focused
`tests/editing_conformance/test_inverse_clip_mirrors.py` regression file
(35 collected cases). No source/test/dependency/generated/pin changes were
made by this reviewer.

The production caller is unchanged: `create_runtime_commit_service().commit`
loads authenticated inverse records, calls `commands.execute`, and dispatches
`apply_inverse`; the repair is exercised through that provider path. The fix
calls the existing `Recording.compile_mirrors()` immediately after each
restored `parent/clip:<id>` leaf in both the scratch guard replay and the
installation replay. This makes the next authored aggregate `config.clips`
guard observe the restored raw clip mirror without dropping the aggregate
authored guard or derived history.

The positive matrix preserves the original request intent for both `clips` and
`config.clips` spellings and both output-change orders. Whole and selected-step
undo/redo, split followed by native leaf movement, exact canonical documents,
derived-write reversal, physical closure/sibling data, and opaque payload data
are asserted. Negative coverage preserves initial contradictory-mirror and
wrong-before/order/read/stale refusals, later field/order/equal/ABA writes,
surviving consumers, and missing history/commands/steps; refusal snapshots
prove no head, entry, document, prepared candidate, or acceptance-state writes.

The detached provider harness is not live Runtime HTTP/authentication proof.
The reviewed Runtime validator still authenticates every `commit.effect`
binding against one enclosing step input/output (`runtime_protocol/
timeline_commit_auth.py:343-391`), so the author’s separately reported
whole-multi-step inverse limitation remains an explicit Runtime-owned blocker.
No auth bypass, provenance weakening, effect coalescing, command reordering,
or success-to-refusal test adaptation was introduced.

See the exact command results in the external reviewer report.
