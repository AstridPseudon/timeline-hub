# P4 rerun record-boundary correction — ap2-P4-rerun-records-return-0833

Disposition: complete within the assigned test-only boundary. Only
`tests/editing_conformance/test_p4_note_rerun_v2_runtime.py` was changed. The
approved canonical physical diagnostic path and every original `NOTE_PATH`
request operand remain unchanged.

## Exact source identity

- Base: `tl/ap2-P4-rerun-path-resume-sol-0824` at
  `501297fb34cbce80aa97fa5aba97e09144b7b773`.
- Current source SHA: `501297fb34cbce80aa97fa5aba97e09144b7b773` (harness commit
  not created yet).
- Current source tree: `f35ff9cbebb6b0e00543ee56d7cf052e8d74f4c9`.
- Edited target blob: `53a8ad9143e7464c0dc606c61f1e3339205bee32`.
- Cumulative owned tracked files: one target test file; 34 insertions and 4
  deletions in this record delta. The preceding approved path delta is already
  in the base and remains intact.
- Runtime control: `/home/user/work/wt/rt-pin-a5d42583` at
  `a5d4258312c979024865ee704da2d632ca5b2730`, tree
  `f74b016ea837f8148db4a602c972073a226ed177`, clean.

## Change

`_expected_plan` obtains the authenticated canonical document at the exact
peer retry head and independently executes the submitted retry command with the
captured request and evaluated head. Accepted reply commands are compared to
that plan's authoritative `records[*]["command"]`, while every submitted
command field (including nested `args.changes` path, before, and value) is
checked for exact equality against the enriched command. The accepted canonical
document, steps, stored records, full command captures, effects, bindings and
dependencies are compared to the same independent plan. Existing conflict,
rerun, key freshness, canonical physical path, closure, opaque/null/absence,
show/history/restart assertions remain present.

This applies the already approved raw-request versus enriched-authoritative-
record boundary principle. It does not loosen to a projection, suffix/path
set, or response-derived expected value, and does not alter production code,
fixtures, transport, or contract scope.

## Controls

Passed:

- Named-node collect-only: one target test collected.
- Ruff on the target: `All checks passed!`.
- Private-cache Mypy on the target: `Success: no issues found in 1 source file`.
- `py_compile` and `git diff --check`.
- Offline independent-plan and negative controls: authoritative enrichment,
  nested submitted-field equality, record/effect/binding/dependency presence,
  and canonical/raw path controls passed.
- Pinned Runtime module-origin and clean-tree preflight.
- `scripts/vendor_lock.py check runtime.lock.json`: `ok runtime.lock.json`.

No live HTTP/body/socket/browser/service/full suite was run, as explicitly
forbidden by this bounded task. The original `[200, 409, 200]` node is therefore
not re-credited here. The orchestrator should obtain the final independent Luna
review covering both the preceding Sol path delta and this record delta, then
run exactly one changed-evidence original node before qualification.
