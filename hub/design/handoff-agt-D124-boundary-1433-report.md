Blocked on a proved Runtime boundary mismatch. Runtime checks step-wide materialization edges against the final command’s intermediate input. Agent product code remains unchanged.

Added a minimal genuine-provider regression:

- Endpoint custody: **PASS**.
- Grouped acceptance: **FAIL** at the physical-edge guard.
- Selected tamper, alias, shared-owner and ABA controls: **20 PASS**.
- Ruff: **2143/2143**; mypy: **1902/1902**; targeted Ruff, Python 3.11 compile and diff check: **PASS**.

Exact commands/results are in [validation.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-D124-shared-four-return-sol-1417/evidence/validation.md). [Source findings and unapplied owner action](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-D124-shared-four-return-sol-1417/evidence/root-cause.md) identify Runtime’s correction point.

Original four were not replayed: no semantic correction was applied, and disk remained below 5 GB. Their acceptance remains unverified. Created `commit-msg` and `BLOCKED`.

Next: authorized Runtime correction, independent core/security review, bounded original-four validation, then Farm core.