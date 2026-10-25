Restored the reference-apply fault’s exact released **503 status/body**, retaining the private static tag with empty stack/class metadata. Only nine production lines added; guards, C0 shapes, all 44 tags, and B010 fixes remain intact.

Validation:

- Candidate: **50 boundaries + 6 diagnostics passed**.
- Pre-tag comparison: identical public envelope; **49 expected diagnostic failures, 1 passed**.
- Regressions: **134 local + 1 central socket, 68 guards, 4 real-provider checks passed**, including seed/bootstrap smoke.
- Ruff/Pyright: **zero new diagnostics**. Compile and diff checks passed.

[Exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-P2-tags-envelope-sol-1156/evidence/validation-commands.txt).

No contract decision or blocker. Wrote `commit-msg` and `DONE`; evidence totals 708 KB. Per D30, this final message is the report; no report/design files written directly.

Held for independent review; no merge/release. Full/browser/P4/native App replay remains unverified.