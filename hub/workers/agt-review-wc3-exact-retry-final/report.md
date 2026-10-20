## WC3 review complete

- Verdict: **Concrete bug; do not approve exact-retry guard or whole WC3.**
- Bug: non-mapping `old_media` and `media` values bypass `_pending_matches` validation and reach `flush`; typed mismatches must refuse with zero POST and unchanged outbox.
- Key/body/head/publication protections are present in `TimelineSession._flight_body`.
- Whole WC3 remains held pending the real private Runtime parent-provider qualification and retained six positive assertions.

Evidence:

- Focused review probes: **10 passed**.
- Broader targeted command: **165 passed** (run once; not repeated).
- `git diff --check HEAD^ HEAD`: passed.
- No product/test changes made; no full or integration suite run.

Published report: [agent-review-wc3-exact-retry-final.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-review-wc3-exact-retry-final.md)

Commit message and `DONE` marker created.