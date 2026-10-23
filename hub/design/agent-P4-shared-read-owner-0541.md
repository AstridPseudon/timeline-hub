# Agent G3/P4 shared-read owner seam

Verdict: genuine source bug confirmed and minimally fixed in Agent SDK.

The production path is `RemoteTimelines.open_bundle`, called by
`astrid/sdk/timeline/store.py:fetch_bundle`. The old reader fetched every
internal revision with the parent scope. For the authentic closure, parent
timeline `film` contains a shot pin to `internal-1`, while the canonical
internal image and dependency manifest identify owner timeline `chapter-1`.
Runtime's `get_project_timeline_revision` performs an exact
`WHERE project_id=? AND timeline_id=? AND id=?` lookup, making the old
`(film, internal-1)` request a concrete wrong-scope counterexample.

The fix in `astrid/sdk/_remote_timeline.py` reads the exact parent revision's
authenticated `dependency_manifest.internal_timelines` owner pins, rejects
malformed/missing/conflicting owner data, calls Runtime with the exact owner,
and checks the returned project/timeline/revision tuple. It preserves the
existing project auth, foreign-scope, digest, exact pin, revision, and closure
guards. It does not infer latest, rewrite authorship, or alter intentionally
distinct working shot-placement identities.

Regression: `tests/sdk/test_remote_timeline_owner_scope.py` invokes the public
reader through a mock transport, asserts the exact call
`(project-1, chapter-1, internal-1)`, and asserts the old film-scoped call is
absent.

Evidence:

- Focused SDK/document/show tests: `22 passed in 12.51s`.
- Scoped Ruff: passed.
- Scoped private mypy: `Success: no issues found in 2 source files`.
- Normal `make ruff`: current 2149 equals baseline 2149.
- `runtime.lock.json`: matches `/home/user/work/wt/rt-pin-34eac004` producer.
- `artifacts.json`: current.
- `git diff --check`: passed.
- Normal `make mypy` is blocked by the pre-existing shared environment: missing
  `types-PyYAML` stubs and NumPy stubs incompatible with the interpreter; no
  changed-file diagnostic was emitted.
- Import origins: Agent source is this worker worktree; Runtime protocol is
  `/home/user/work/runtime/runtime_protocol`; pytest is from `venv-agent`.

No full/live HTTP/browser/P4 duplicate was run by instruction, so live Runtime
acceptance remains unverified. Independent read-only review is needed. The
harness commit SHA is pending; base reviewed was `31a5e8d3`.
