# agt-P4-shared-read-return-0601

Readonly repair report: **PASS for the requested local repair; independent review pending**.

Base: `6131704b3`. Imported only the `47aa77266` two-file reader delta, then repaired the reviewed parent-tuple and historical shared-owner defects.

Production source is wired through `RemoteTimelines` (`astrid/sdk/remote.py:458`): public open calls `_RemoteTimelineRevisionMixin.open_bundle` (`astrid/sdk/_remote_timeline.py:27`), and historical diff calls `read_authoring_revision` (`astrid/sdk/authoring_revision_diff.py:29`). Both use exact authenticated `dependency_manifest.internal_timelines` owner pins. Parent, shot, and internal returned tuples are checked before projection; malformed/missing/ambiguous/foreign pins refuse without fallback.

Evidence: focused readonly selection **45 passed**; scoped Ruff and persistent mypy **PASS**; normal Ruff baseline **2149/2149 PASS**; mypy baseline **1914/1914 PASS**; vendor lock, artifact manifest, and diff check **PASS**. Exact commands and the initial missing-`runtime_protocol` collection issue are recorded in the worktree `report.md`.

Independent-review need: run a fresh readonly review of the final tree, specifically checking the parent/shot/internal tuple guards and both public-open/historical-diff owner-call arguments. No full/live HTTP suite was run, per brief.
