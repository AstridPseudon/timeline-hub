**REQUEST CHANGES — one P2 remains.** If reverse-step promotion fails after draft replacement, reopening exposes no inverse operation. Both undo and redo reproduce this gap; recovery states remain hidden in temporary files.

Publication boundary fencing and lost-ACK retry pass review. Existing evidence verified: **386 targeted passes** and **4 renderer-blocked provider passes** on the exact reviewed tree.

Fresh command, from the assigned worktree:

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_checkout_history_boundaries.py tests/sdk/test_timeline_checkout_publication_retry.py "$ORCH/workers/agt-review-history-boundary-final/test_review_restore_interruption.py"
```

Result: **11 passed, 2 failed**; both failures demonstrate the recovery gap.

The combined ten-path patch applies cleanly to current integration `e2ad5958`. The successor alone requires `88dd38f1`. No source edits or full suite.

[Review, reproduction, safe port paths, and exact validation](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-review-history-boundary-final.md>). `notes/report.md`, commit message, and `DONE` written.