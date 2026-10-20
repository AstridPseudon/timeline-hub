**HOLD** `e6e69814` / tree `b62e2173`.

Private diagnostics prove that an injected identity-read denial can cause pruning to forget a live child and falsely certify cleanup. The original tree refuses the same scenario.

- Central unchanged tests: **650 passed, 2 failed, 16 skipped**.
- Private diagnostics: **6 passed, 3 counterexamples failed**; all three pass against the original.
- Product unchanged. No ordinary exploit claim; macOS unverified.

[Report with exact commands, reproduction, and limits](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-d13-unowned-census-successor/report.md).

Review complete; commit-message files and `DONE` written. Source-owner correction and requalification recommended.