## F-D86 review: PASS

Reviewed `095177db79` against baseline `27c68177c1`.

- Only five lines changed in `_create_fixture`: genuine `occurrence.create` is accepted as `popup-birth`, then the bundle reloads from Runtime’s canonical document.
- Original 48-case matrix, inputs, opaque fields, media identities, mirrors, assertions, raises, retry/undo/redo/history, and single-batch popup operation are unchanged.
- Both transitive callers were checked: M2 shot pool and M2 auto-placement.
- No synthetic history, SQL writes, pins, local authority, skipped/xfail tests, or out-of-scope changes found.
- Worktree is clean; no review commit was needed.

Static results:

- AST/compile baseline and candidate: PASS
- Ruff baseline and candidate: PASS
- Mypy baseline and candidate: PASS
- `git diff --check`: PASS

No pytest, collection, fixture/helper execution, Runtime service, browser, build, or probe was run per task restrictions. Behavioral Runtime proof remains intentionally unverified.

Evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-occurrence48-review-0145/evidence/`