**HOLD WC4 writer deletion.** Reviewed `a6098b5d` read-only and reproduced one compatibility regression: the original helper succeeds with a digest-only admission and verified local artifacts; the candidate refuses it with “pack snapshot unavailable; re-admit pack.”

Existing targeted suites passed: **442 tests**. Additional probes confirmed rebased acceptance, lost-ACK/restart recovery, pagination, bool/number-safe intent matching, and explicit-pin refusal. Supplementary result: **3 passed, 1 failed**—the failure preserves the original legacy-success expectation.

Exact test commands, results, source references, and reproduction steps are recorded in the [detailed report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-wc4-helper-native/notes/report.md) and [flat review](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-review-wc4-helper-native.md).

Keep same-element PARAM source selection held for the separate owner rule. No manifest-order inference was found. No repository changes, fixes, ledger edits, HTTP/browser tests, or full suites were performed.

Next: resolve the compatibility gap, then review the corrected migration against the settled pin rule. Review complete; `commit-msg` and empty `DONE` written.