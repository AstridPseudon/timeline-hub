## P1 independent verdict

**Whole P1: NO-GO.**

- Actual run `24510`: **1 passed / 1 failed**, exit 1, 440s.
- Case 1 passed in 29.7s.
- Case 2 observed one POST instead of two and timed out. Agent move, Runtime 409, lost ACK/restart, and rollback assertions were not reached.

### Evidence checks

- **Safe export custody: PASS (direct file).**  
  `design/app-P1-24510-safe-diagnostic-2201.json` is 144,118 bytes; SHA-256:
  `faa0df373a0ae84dfd3ba56aab81988a65435c31b339ec91864be1bb299e4b0f`.

- **Safe projection/schema/security: PASS.**  
  Strict validation passed for schema, run metadata, tuple, case counts, bounded 32-record projection, finite phase/code/class values, overflow/loss markers, and forbidden-field scan. No credentials, raw request/reply, or private trace were exported.

- **Observed actual boundary:** project `e1c63027229f49adb37ef2e80552d3f9`, timeline `7329bb69-4aee-4eb8-bf2d-605485b890a1`, selected clip `p1-chain-source-1792792571203`; Source In changed `0 → 3`. One commit POST returned 200. Mounted sequence 23 recorded `capture-rejected`, `source-parent-mismatch`, `TimelineVersionConflictError`, before transport.

- The safe file exposes only request body length (3669 bytes) and key length (36 bytes); no request-body hash was reconstructed.

- **Source/body/no-weakening: PASS.**  
  App HEAD/tree are exactly `e6d72d3d07d2df485e4f3e86c56d1eb2dd5cd91a` / `6513960eb0b2704d02c3b3298ba594b546af7565`; worktree is clean. Reviewed `6ecc`, `def457`, and `f890` ancestry is present. Protected hashes match:

  - First P1 body: `4b04ad7e…a72ea8b7f`
  - Second P1 body: `2f750118…10a2f7`
  - Gate-5 body blob: `37caf285…e74b1`

  Prior independent 2118 evidence is reused: Node 20 safety test, three typechecks, lint, exact two-test listing, diff checks, and no-weakening review all passed.

### Causal conclusion

The observed failure proves a bounded local App capture refusal, but not whether the config or registry comparison arm differed, nor which field/operand caused it. Therefore classification remains **INSUFFICIENT EVIDENCE** between product defect and valid refusal/harness state.

The prior `21216` trivialboot and `4526` parser pre-body failures remain **NOTRUN**, not chain evidence.

No tests or live/browser/service runs were performed in this report-only task. Required `commit-msg` and `DONE` markers were created.