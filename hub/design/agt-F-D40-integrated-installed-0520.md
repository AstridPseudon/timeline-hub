## PASS — installed D40 original positive

- Executed exactly once:
  `tests/stage1/test_zero_shim_execution_pack_deletion.py::test_generic_host_runs_external_python_orchestrator_from_admitted_pack`
- Result: `1 passed in 3.32s`
- Actual production imports resolved from the installed child’s `site-packages`; relevant worktree/installed Agent source hashes matched.
- Child: Agent `ba8f0bc…`, Runtime `f3208b2…`, provision status passed.
- Profile: Node `v20.19.4`, Remotion archive SHA `819acf6b…`.
- Worktree remained clean; `git diff --check` passed.

Durable evidence:

[d40-installed-original-positive.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D40-integrated-installed-0520/evidence/d40-installed-original-positive.json)  
SHA256: `77bddf5b34c107a53a518823e4faf42a6d373646636a1931596454d069af495f`

Recorded candidate SHA/tree, child/package/client identities, direct URLs, markers, five Runtime fixture hashes, origin maps, source equality, body/three-assertion hashes, subprocess `imported_from`, and profile custody.

Decisions/notes:

- Installed Agent is `ba8f…`, not current full source; relevant production files were explicitly proven equal before qualification.
- Current helper blob is `5e2d2f…`; the reviewed 0446 helper blob was `ada16e…`, changed by merged `014dbfe6b9`. The original test blob remains `d106a9…`.
- The requested frozen contract path was absent; the Runtime contract at `/home/user/work/runtime/contract/commit-v2.md` was used.
- Prior 0511 Ruff/mypy/compile checks were reused as instructed; no broad mypy or full suite was run.

Commit message written and `DONE` marker created.