**PASS: bounded R2 fix ready for independent Luna review.**

The capture confirmed unsafe acceptance: the first clear creates a fork while a sibling retains the original physical root. A later absent→absent clear writes the fork, but the inverse scan guarded only the original root.

Changed only `inverse.py` and one new regression file. The guard now includes the authenticated fork output and its surviving consumers. Equal-value writes remain recorded; historical aliases are unchanged. The original assertion is untouched.

Validation:

- Valid RED: **4 failed, 1 passed**, exposing equal-clear and declared-consumer gaps.
- Original exact test plus new regressions: **6 passed**.
- Scalar-provider lane plus regressions: **20 passed**.
- Selected R2 negatives: **16 passed**.
- Config-history, ABA, compiler and transcript controls: **8 passed**.
- Real Runtime caller: **PASS** for accepted/merged replies, stale base pair, preview/null receipt, canonical history, and refusal without writes.
- Scoped Ruff, private mypy, pinned vendor check, artifact check and diff check: **PASS**.

[Exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-R2-equal-write-sol-2306/evidence/validation-commands.txt) accompany complete before/after captures in the same evidence directory, totaling under 1 MB.

No blockers. No full-suite retry, integration-head move, commit or merge. The retained full-suite failure remains available. `commit-msg` and `DONE` are written; independent Luna review is next.