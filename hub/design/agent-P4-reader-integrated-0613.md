# G3/P4 integrated reader readonly review — PASS

Readonly integrated-source review: **PASS**.

Exact integrated SHA/tree: `168a5c9b32e31c7f8db14a96153a3d1955054734` /
`123a5832553dc43093dbbb3fc8d73ce01d59e49f`. It merges first parent
`6131704b36807e165575fa944ba984cc847059c8` with `bd23946157d863b39a8c0e3c41ea489455e08b1b`; the integrated tree is identical to
`bd239`, with no later or unrelated ancestry. The merge delta is exactly four
paths: `_remote_timeline.py`, `authoring_revision_diff.py`,
`test_authoring_revision_diff.py`, and `test_remote_timeline_owner_scope.py`.
Their blobs exactly match reviewed `a8132afba38ca66b1c815ed2c99404a66a02337f`
(`bc8b9fce`, `db106a74`, `8f59a4b1`, `7fffe374`). Root `report.md` is absent.

Qualified readonly owner scope: authenticated parent
`(project_id,timeline_id,revision_id)` validation; shot
`(project_id,shot_id,revision_id)` validation; internal
`(project_id,authenticated owner timeline_id,revision_id)` validation; and
missing/foreign/wrong/mismatched tuple refusals. Historical open/diff reads use
the authenticated manifest owner and exact pins, with no mutable-head fallback.
Production trace is `timeline.open → store.fetch_bundle →
RemoteTimelines.open_bundle` and `RemoteTimelines.diff →
read_authoring_revision`.

Evidence: exact requested pytest command **45 passed in 13.07s**; scoped Ruff
**PASS**; configured private mypy with persistent
`/home/user/work/venv-agent-typecheck-v2/bin/python` **PASS**; `make ruff`
**2149/2149 PASS**; `make mypy` **1914/1914 PASS**; vendor lock, artifact
manifest, and `git diff --check` **PASS**. Agent imports came from the
integrated worktree; `runtime_protocol` came from `/home/user/work/runtime`.

**P4 is not DONE**: the original single/ten-note HTTP-body proof was not run,
as explicitly prohibited. No source or dependency edits were made. The worker
`tmpdir` was a sentinel file, so private caches used `/tmp/agt-P4-reader-integrated-0613-*`.
