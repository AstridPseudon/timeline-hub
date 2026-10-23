**PASS for the assigned R2 fix**, based on `d7db17a60`.

Changed only `inverse.py` and `tests/sdk/test_timeline_inverse_fork_guard.py`:

- Validate complete, unique materialization provenance against authenticated execution boundaries before inverse application.
- Preserve owner and field scope for retained siblings and existing physical read dependencies.
- Classify the four child-scope graph cases as `intervening_write`, preserving their original assertions.

The actual before/after probe confirmed the defect: identical accepted calls and inverse inputs produced **accepted undo with state changes before**, versus **`history_unavailable` with no writes after**. The missing-binding regression was RED for whole and selected-step undo, then GREEN.

Ran the exact bounded commands from [2306’s validation commands](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-R2-equal-write-sol-2306/evidence/validation-commands.txt), using the specified Runtime, venv, environment and pytest flags:

| Final run | Result |
|---|---:|
| Original regression + expanded fork tests | 31 passed |
| Scalar provider + fork tests | 45 passed |
| Immediate negatives | 16 passed |
| History controls | 8 passed |
| Four graph child variants | 4 passed |

Ruff, mypy, vendor lock, artifact manifest and `git diff --check` passed. Final acceptance runs had no skips or xfails. Original fork-test bodies and the original scalar-test file hash remain unchanged; prior evidence artifacts were untouched.

Limits: a genuinely changed retained sibling exposed an existing `binding_changed` ambiguity in untouched `_commit_patch.py`; recommend separate owner follow-up. Reused 2306’s production Runtime caller proof; no fresh full suite was requested, and run 25691 was untouched.

Final `inverse.py` SHA256: `2491a97d9c9cf262834d12524eb7935312ae24ff6afa5f258883f18633d570b1`.

R2 commit message and empty `DONE` marker written. Worker evidence remains under 1 MB.