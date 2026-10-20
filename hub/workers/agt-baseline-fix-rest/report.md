## agt-baseline-fix-rest report

**Result:** I fixed groups B, C, F, I, K and L, all test-side. Group J is left for a decision. No product code changed. The worktree has six modified files, uncommitted, and the commit message is at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-baseline-fix-rest/commit-msg`. I did not commit, push, or request any `full*` suite.

### Per-group counts

"Before" comes from the cutlist's original 109-node log (`1020031037-28578`). I did not re-run the pre-fix tree, so those numbers are cited, not re-measured. "After" comes from the remotion-env run on the final tree and from the default-env targeted run.

| Group | Nodes (before) | Root cause (confirmed) | Fix | After |
|---|---:|---|---|---|
| B | 4 | Ambient `ASTRID_REMOTION_PROJECT_DIR` forces launch validation on a fake host that lacks it | Test: `monkeypatch.delenv("ASTRID_REMOTION_PROJECT_DIR", raising=False)`, same pattern as existing tests | 4 pass (remotion env and default env) |
| C | 3 in cutlist, **2 confirmed** | Fake inventory passes bare `Path` in `sources`; `discovery.py:296` reads `source.pack_root` | Test: `sources=(SimpleNamespace(pack_root=managed),)` | 2 pass in default env. In remotion env they still fail, but only on group A's `RemotionValidationError`, which masks them |
| F | 3 | Missing `import signal` | Test: add import | 3 pass |
| I | 1 | `Path` objects in `subTest` params can't be serialised by xdist | Test: `subTest(inventory=[str(path) for path in inventory])` | 1 pass |
| K | 1 | Doc counts stale: `generic_host.py` 13,598→13,798, `remotion/run.py` 2,158→1,851, `host_bootstrap.py` 1,601→1,717 | Doc: refresh the 3 rows, delete the "intentionally red" paragraph. Tolerance unchanged | 1 pass |
| L | 1 (collection error) | Generated client loaded as bare module, breaking its relative import | Test: load `astrid_runtime_client` as a package, import `.generated` | Collects and passes (module has no skip marks) |
| **J** | 1 | See "Needs decision" | None | **Still fails** (unchanged) |

### Test runs

- Remotion env, run `1020070432-479` (tree `88eee73c`, before C/K edits): 18 failed, 83 passed, 2 skipped. B, F, I, L passed here; the C, J and K failures remained.
- Remotion env, run `1020071349-12965` (tree `2e558eec`): 17 failed, 84 passed, 2 skipped. K now passes. The 2 C nodes fail only on group A (`RemotionValidationError`). J fails. All 14 remaining failures are group A's, which is not mine.
- Default env, targeted `1020071350-11030` (tree `2e558eec`): `167 passed, 3 skipped, 2 subtests passed`. This covers the C file, B file, F file, I file, L file and K.
- Final tree, targeted `1020072111-4757` (tree `22081c07`, after the doc newline fix): `167 passed, 3 skipped, 2 subtests passed`.

Exact request command for the remotion env: `bin/request-test agt-baseline-fix-rest remotion-env-nodes --files "<ids>"`. Exact targeted command: `bin/request-test agt-baseline-fix-rest targeted --files "tests/test_structure_contracts.py tests/sdk/test_host_bootstrap_source_identity.py tests/stage1/test_pack_host_interpreter_identity.py tests/packs/test_vibecomfy_metadata.py tests/sdk/test_admission_recovery.py tests/packs/runpod/test_worker_process.py"`.

I did not run `make structure`, `ruff` or `mypy`. Those commands need approval in this sandbox, so the lint and structure gates are unverified.

### Needs decision: group J (`test_failed_worker_release_retains_original`)

- The test expects `CleanupUncertainError` from `host.invoke_capability`. The product wraps it as `CommandCleanupUnresolved(HostError)` with the original as `__cause__` (`generic_host.py:8387-8393`).
- Evidence for the wrapper being the intended contract:
  - `tests/test_generic_host.py:4238` (`test_failed_command_finalizer_retains_original_and_attempt`) pins the same wrapping on the command path, expecting `HostError` with "owned command cleanup uncertain".
  - `tests/core/execution/test_render_scope_launch.py:105` expects `CommandCleanupUnresolved`.
  - Only this capability-path test expects the raw exception.
- My recommended fix is test-side: expect `CommandCleanupUnresolved` and assert `__cause__` is the `CleanupUncertainError` with the same message. I did not apply it because the brief says to leave wrapper semantics to a decision.
- Second assertion to verify: the test also checks `host._unresolved_task_scopes`, which the latch branch never appends to. Under the wrapper fix, that assertion may need to change too. I have not checked this.

### Notes and corrections

- Cutlist correction: C is **2** nodes, not 3. The correlated-terminal test fails on group A's `RemotionValidationError` here, not on `pack_root`.
- I did not change `test_host_bootstrap_source_identity.py` beyond the one fake. Once group A's conftest fix lands, the C nodes should go green under the remotion env too. That is expected from the default-env pass, not a remotion-env run.
- I omitted the `Co-Authored-By` model line from the commit message because the brief says "no model names". I kept the `Claude-Session` trailer.
- The doc edit initially dropped the trailing newline. I restored it, and the final targeted run covers that tree.

### Recommended next steps

1. Decide J: I recommend the test-side wrapper expectation above.
2. Land group A, then re-run the remotion-env nodes to confirm C is green there.
3. K's counts were measured on this tree. Any other worker that changes `generic_host.py`, `remotion/run.py` or `host_bootstrap.py` will move them again, so re-check K after merging.
