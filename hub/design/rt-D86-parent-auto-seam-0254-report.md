## F-D86 investigation report

No product or test files changed. Worktree is clean; commit message and `DONE` marker were written.

### Canonical six

From actual10077 outcomes:

1. `test_disjoint_head_accept_reload_exact_retry_undo_redo_and_reserved_id[image-anchor]` — outcome row 175
2. `...[image-fallback]` — row 176
3. `...[image-lane-end]` — row 177
4. `...[video-anchor]` — row 178
5. `...[video-fallback]` — row 179
6. `...[video-lane-end]` — row 180

Tuple: Agent `0ae146e1`, Runtime `a3cd1a32`, App `91368644`, Composition `635f4de0`.

### Exception and trace

All six captured the same outer exception:

`runtime_protocol.errors.RuntimeErrorBase: intervening publication changed a guarded address`

Static traceback source:

- Agent `astrid/sdk/timeline/commit.py:1370` calls `rebase_patch(...)`.
- Agent `astrid/sdk/timeline/_commit_patch.py:951` raises the underlying `CommandError`.
- Agent wraps it at `commit.py:1456–1467` as `CommitRejected`.
- Runtime propagates it through `runtime_protocol/service.py`’s commit coordinator/public-failure boundary.

The failure occurs before `RequestCommitPort.preview()`/`accept()` and before Runtime’s strict prepared-candidate validation. Therefore no Runtime guard defect is established; exact guard `kind/ref/path` is UNKNOWN from the captured XML.

### Source ownership

The D86 author report confirms only the assigned test file changed. The actual current Agent `_commit_patch.py` is byte-equivalent to the integration source and its guard block was introduced by R1 commit `8a66b1ac88b`, not by the D86 fixture migration.

The nearest previously reviewed passing parent-auto source was based on Agent `537c2ecd` / candidate `0937d6fd`, not the actual current `0ae146e1` tuple. It therefore does not close this seam.

Smallest genuine repair owner: Agent, `astrid/sdk/timeline/_commit_patch.py`, specifically `rebase_patch()` guard projection. No Runtime file is implicated by the captured path.

### Validation

No pytest, collection, service, browser, body execution, profiling, or product-code execution was run, per task constraints. Static XML/report/source comparison and git identity checks completed successfully.

Recommended next step: Agent owner reproduces the exact tuple and inspects the specific projected guard path; Runtime should remain unchanged unless a candidate reaches `RequestCommitPort.preview()` and fails there.