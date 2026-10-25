Implemented request-scoped ancestry reuse in `timeline_commit_port.py`. Each historical closure still reauthenticates its target; authorization, invalidation, and caller isolation remain intact. Store/auth source and original tests are unchanged.

- **Native gate passed:** 84.715 → 122.704 ms, **1.448×**, against unchanged 1.5×. Eight POSTs, receipt/readback equality, row preservation, and 401 refusal passed.
- **Focused tests:** 311 passed, 40 deselected by default lane filters.
- **Smoke tests:** 4 passed. **Central HTTP controls:** 8 passed.
- **New regression:** parent RED in both cases; candidate GREEN, covering cost, mutation, revocation, invalidation, and request lifetime.
- **Statics:** Ruff, compile, and diff checks passed. Pyright: 57 parent-identical diagnostics, zero new.
- **Known auth failure:** reproduced identically on parent and candidate. Return to the `validate_sequential_capture` source owner; no auth fix attempted.

[Exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D111b-closure-growth-sol-1115/evidence/validation-commands.json) · [Source identities and timing comparison](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D111b-closure-growth-sol-1115/evidence/native-comparison.json)

Timings remain noisy, including a 190 ms middle point. **Hold release pending independent source/security review of this delta.** Evidence is under 300 KB; `commit-msg` and `DONE` are written. No commit or release performed.