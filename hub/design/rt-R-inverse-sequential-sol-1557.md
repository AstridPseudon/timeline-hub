Implemented **R-inverse-sequential** in `timeline_commit_auth.py`, with one new focused test file.

Runtime incorrectly treated native `timeline` captures as absent payload roots. It now validates their exact revision/digest pins, reversed source captures, and complete ordered source-effect reversal. Existing guards and D62 classification remain intact.

Validation — [exact commands and retained evidence](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R-inverse-sequential-sol-1557/evidence/commands.txt):

- Qualified oldRED: native comparator passed; restore inverse reproduced the retained sequential-input rejection.
- Final focused controls: **28 passed**, including transient-root tampering refusal.
- Existing inverse/shared/source-copy/history/strict controls: **333 passed**.
- Unchanged `test_restore_inverse_redo_and_exact_retry_survive_runtime_restart`: **1 passed**, run exactly once after correction. Its body matches Agent `57779274a0`.
- Ruff, Pyright, compilation, and `git diff --check`: passed; Pyright reported zero errors.

Independent security review **passed** after adding exact source-effect reversal.

No blockers for this correction. A separate exploratory third native V2 inversion failed inside Agent; provenance is retained and that behavior was not changed. No full suite or browser journey ran.

Commit message and `DONE` are ready. Recommended next step: harness commit and merge through the Runtime queue.