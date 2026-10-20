**Review complete: request changes for one P2 defect.**

`native_occurrence_create.py:35` lets finite `on: 1e308` overflow frame quantization. Runtime returns retryable **503 runtime_unavailable** instead of a permanent command refusal. History remains unchanged. Recommend translating the quantizer error to `CommandError(unsupported_timing)` and adding a regression.

Fresh validation on `206f40fe`:

- Targeted birth/inverse/source neighbors: **574 passed**.
- Normal Runtime lifecycle: **2 passed**.
- Reservation/delete neighbors: **52 passed**.
- Independent probes confirmed main-compatible empty-shot behavior, cross-project collisions, ABA refusal and exact retry.

The 53-definition cohort needs an additive **54-definition / 27-operation** join; exact conflict resolutions are documented. No joined-source or public qualification is claimed.

[Flat review](../design/agent-review-occurrence-birth-current.md) · [Detailed report with exact commands, results and repro](notes/report.md)

No product changes, full suites, HTTP/browser runs or git mutations. Worktree clean; temporary archives removed; `commit-msg` and `DONE` written.