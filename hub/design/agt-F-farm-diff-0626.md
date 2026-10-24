## Report

Completed read-only farm diff evidence under:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-farm-diff-0626/evidence/`

Results:

- Historical basis: 172 closed / 95 open.
- Current package: 202 closed / 65 open; newer proof was not backdated.
- Historical closed farm failures: 88 possible regressions; 0 confirmed non-environment regressions.
- Open nodes proven PASS on farm: 0. No JUnit/pass enumeration exists.
- Environment-only nodes: 0 promoted. The retained raw log is unavailable, so aggregate setup messages were not treated as per-node causal proof.
- Unresolved: 185 failed lines and 187 errored lines.
- Farm arithmetic preserved: 281 failed lines + 7 missing summary failures = 288; 187 setup errors.

Farm subject was Agent `9cd3dbe865a941c052bda04ae0d61306d18f8f26`, tree `57f0231da0d7904ecd8778169973d6384e0ae141`, Runtime `45c3a7f476e1c5f74fafc15956a58b9871eee21f`. The selected `8657e836` subject did not run.

Validation command: stdlib-only JSON/list membership, duplicate, partition, and hash checks — PASS. Product tests/static checks were not run.

Manifest SHA-256: `aabae0ea21377884d3f452032747c54cc2ad71d5975c0833a940b6549ef6c81b`

No product/shared-census edits. Commit message written and `DONE` created.