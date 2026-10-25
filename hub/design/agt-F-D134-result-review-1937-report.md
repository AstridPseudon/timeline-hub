## Report

- Produced the safe review packet under `evidence/`, including per-ID TSV for all 370 bad IDs.
- Accepted service: 18455; 8926 passed, 190 failed, 180 errors, 173 subtests passed.
- Classification: 344 `OURS_NEW_FILE`, 14 approved REG14 (all still FAIL), 12 UNKNOWN. `core_open_n`/`reg_open_n` remain UNKNOWN; retirement 0.
- Baseline and upstream status pairs independently reconciled.
- Final verdict: FAIL. Actual XML, raw runner receipt, and disk witness were unavailable; final custody and XML-level checks cannot PASS. No ship/C0 behavior credit granted.

Validation:

- JSON/TSV consistency: PASS
- `bash -n evidence/measurement-command.sh evidence/preflight-command.sh`: PASS
- `git diff --check`: PASS
- No product tests or reruns performed.

Commit message and `DONE` marker are present; harness may commit the worktree.