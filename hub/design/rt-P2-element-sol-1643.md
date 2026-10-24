**R-P2-element-docpatch-hang: blocked on actual request evidence; no Runtime cause established.**

- Retained App reports describe one element POST pending through teardown. **Runtime arrival count, handler entry, lock wait, provider execution, and receipt remain UNKNOWN**, not zero.
- Same-run service artifacts for `app-d66-plain-p2-three-products-1024161326-25943` are absent locally. Need App-owned `log.txt`, `d66/manifest.json`, element diagnostic, and any retained `<harness.tmp>/door-audit.jsonl` or daemon output. The audit records responses; Runtime suppresses ordinary access logs.
- Passing P1 and popup’s captured `422 invalid_records` remain separate observations. Neither establishes the element cause.

Worktree unchanged at `6bba471a0`; inherited P4 tests preserved. No authentication, validation, budget, timeout, or original-test changes. The single authorized meaningful reproduction was **not submitted** because its actual request/baseline inputs are unavailable.

Verification: **25 passed in 3.12s**; scoped Ruff passed; Pyright reported zero errors/warnings; five files compiled; `git diff --check` passed. Exact commands and results: [commands.txt](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-P2-element-sol-1643/evidence/commands.txt). These are invariant controls, not reproduction or RED/GREEN proof.

Commit message and `BLOCKED` written. Next: App supplies existing safe request-phase evidence or makes the retained request/baseline available in place for the supported targeted service route. Any resulting fix still needs independent core/security review before merge; App owns the meaningful P2 rerun.