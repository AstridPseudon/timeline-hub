## Result

Oracle is wrong; no product defect found. App submits the six-field raw `doc.patch`, while Agent/Runtime authentically add recorder fields (`expect`, `authorship`, `reads`, `bindings`, `intent`, `resolved`, `selections`) before receipt-bound history persistence.

Prepared one strict review-only proposal:

[proposal.patch](/tmp/timeline-p3-recorded-command.r4Gx4F/proposal.patch)  
[proposal.md](/tmp/timeline-p3-recorded-command.r4Gx4F/proposal.md)

- Exact-key and deep-equality checks preserve all raw fields and reject missing/unexpected authority fields.
- Virtual source hash: `736fd381…` → `ef05a482…`
- `git apply --check` — PASS
- Node 20 fault-order controls — PASS
- Strict envelope controls — PASS, 3/3
- Worktree remains clean.
- Actual pinned P3 remains original FAIL at line 1820; no GO or downstream credit granted.
- Commit message and empty `DONE` marker created.