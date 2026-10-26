# Validation

Command: `python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-fullpair-source-accounting-return-1051/evidence/check_source_accounting.py`

Results generated fresh by this read-only checker:

- XML parse/hash: cut 6710f7fe1b4b1a0b4d43614f0fe58d437b0b6fff76990e4a717022cef773fcd5, pristine 9d36fcecf662cc9138cd30cb6ad674a57db30209b18593f29da08ed961792bba; declared/concrete equations pass: `9561 = 9388 + 173`, `3255 = 3082 + 173`.
- XML status conservation: cut 201 FAIL + 196 ERROR = 397 bad outcomes; pristine 20 FAIL + 15 ERROR = 35.
- Source identity AST checks: 5 named checks; 5 pristine exact functions absent; decorator/parameter records retained; no fuzzy name substitution.
- Pristine-only source map: 64 exact IDs emitted; behavior-preservation proofs: 0; unresolved rows: 64.
- Frozen source refs: Agent ecdc242ed9b673f641759ecf029f95e89a2c6f92 vs 64197afa297f86f1e738238d5e80aff6d33e303a; Runtime 95d98f038320d5d46bd679ac000ab3e15825c935 vs fa9cd5464a8b37b02f971de375e56be846cd69e2; runtime symbol summaries emitted in `source-map.json`.
- Product worktree status: `clean`.
- No pytest, collection, provider, browser, install, test-service request, body, full suite, or product mutation.
