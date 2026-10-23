# G5 inverse test fidelity — draft return

## Scope

This draft changes only:

`tests/sdk/test_timeline_restructure_guarded_runtime.py`

The requested production behavior remains pending. No product/provider/store,
Runtime, sync, pin, client, schema, generated, or contract changes were made.

## Decisions applied

The old `restructure_runtime` fixture in
`tests/sdk/test_timeline_restructure.py` is shared by legacy restructure tests,
so it was not rewritten. The new guarded-inverse test now uses a local
`restructure_inverse_runtime` fixture layered over that same one-service setup.
The local fixture binds the actual `RemoteTimelines.open_bundle` implementation
and adds only the existing public revision-read methods to the lightweight
generated transport seam. Its document read supplies both the current revision
and publication IDs to `open_bundle`; the reader then verifies the exact
history receipt pair and complete canonical closure as production does.

The new fixture contains no private `revision_closure` call. It does not invent
authority, cache, acceptance, or `reads: []`; it leaves the full v2 request,
metadata, command, receipt, canonical, dependency, and inverse assertions in
the original test intact.

The later overlap refusal now snapshots the current head, full history page,
and authenticated canonical document before attempting inverse. After the
expected `CommitConflict`, it asserts all three are byte/equality unchanged.
The accepted overlapping write and original refusal property remain present.

No wrong-pair/scope negative was added because this return is deliberately
limited to the two identified seams and makes no additional behavior claim.

## Evidence

- Collection: **49 tests collected** for the target and its legacy neighbor.
- Pure target behavior: **35 passed, 13 deselected** with
  `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime`.
- Legacy duplicate neighbors: **2 passed, 46 deselected** with the same
  supported Runtime checkout.
- Scoped Ruff: **passed**.
- Scoped private mypy: **passed**.
- `git diff --check`: **passed**.
- Source/AST mapping: **passed** for exact production reader usage, exact
  revision/publication pair, no private closure in the new fixture, and explicit
  head/history/canonical no-write assertions.

The known failing real Runtime whole-undo body was not rerun. The prior causal
review's `503 not_ready / runtime_unavailable` remains open, so inverse behavior
is **PENDING** the owner source fix and this is G5 draft-only evidence. No full
suite, browser/live journey, shared dependency mutation, daemon, or Git mutation
was performed.
