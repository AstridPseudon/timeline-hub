# G3/P4 independent readonly final review — `a8132afba`

Verdict: **PASS**. Reviewed exact delta `6131704b3..a8132afba`; no source
edits were made by this reviewer.

## Scope

The range contains exactly the own first-return commit `a8132afba` and no
unreviewed ancestors. Its five paths are the two reader helpers, their focused
tests, and `report.md`; no pins, generated/schema files, executors, or shared
dependencies changed.

The prior review `agent-P4-shared-read-review-0553.md` correctly found two
defects in `47aa77266`: missing parent tuple validation and historical diff
reading shared internals under the parent timeline. Both are fixed. The repair
validates parent, shot, and internal `(project_id, owner/timeline_id,
revision_id)` tuples before projection and uses only exact authenticated
`dependency_manifest.internal_timelines` owner pins. Missing, malformed,
conflicting, foreign, and mismatched data refuse; no latest fallback or guessed
owner was found. Existing corrupt-closure and cross-owner refusals remain
asserted; fixture manifest additions are faithful transport metadata.

## Production trace

- `timeline.open` (`astrid/sdk/timeline/commit_session.py:237`) →
  `store.fetch_bundle` (`astrid/sdk/timeline/store.py:641`) →
  `RemoteTimelines.open_bundle` (`astrid/sdk/_remote_timeline.py:27`).
- `RemoteTimelines.diff` (`astrid/sdk/remote.py:1572`) →
  `read_authoring_revision` (`astrid/sdk/authoring_revision_diff.py:29`) →
  `_authenticated_internal_owners` (`:10`).

Import origins used by the tests: Agent modules from
`/home/user/work/wt/agt-P4-shared-read-final-review-0606`; `runtime_protocol`
from `/home/user/work/runtime/runtime_protocol/__init__.py`.

## Evidence

- Targeted pytest: **45 passed**.
- Scoped Ruff: **PASS**.
- Scoped persistent mypy: **PASS**.
- `make ruff`: **PASS**, 2149/2149; `make mypy`: **PASS**, 1914/1914.
- `vendor_lock.py check` against `/home/user/work/wt/rt-pin-34eac004`: **PASS**.
- `artifact_manifest.py --check`: **PASS**.
- `git diff --check` (working tree and reviewed range): **PASS**.

Exact commands are recorded in the worktree `report.md`. No full/browser/live
HTTP suite or Proof-owned P4 HTTP body was run. PASS permits Proof staging its
originaltenHTTP work on the exact callable source.
