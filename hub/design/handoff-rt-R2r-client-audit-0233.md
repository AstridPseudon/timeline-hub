## R2r client audit: FAIL

- Valid v2 `merged` replies are rejected by both public clients:
  - Python: `generated.py:940-950`
  - TypeScript: `generated.ts:187-191`
- Both accept malformed partial receipts and preview replies with missing/invalid `would_status`.
- Conflict/invalid envelopes preserve required structured details correctly.
- DTOs already declare `merged` and valid `would_status`; runtime guards are stale.
- No repository files changed; `DONE` marker created.

Evidence:

- TypeScript build passed using a temporary output directory.
- Direct Python/TypeScript public-client probes reproduced all findings.
- No full/native/browser suites run per task scope.

Full handoff: [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2r-client-audit-0233/report.md)