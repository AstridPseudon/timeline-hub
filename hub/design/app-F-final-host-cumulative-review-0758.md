## Result

PASS with limits. Corrected return-0754 is valid and retains the initial 0748 FAIL. No final Agent/App tuple is claimed.

- App uses `scripts/vendor-lock.mjs`; both lock paths and selector constraints are correct. Current Runtime lock remains pinned to `34eac004…`.
- Runtime `becfe6db…` independently matches tree, 79 artifacts, manifest/version hashes, and all four listed producer file hashes.
- App matches final Runtime for `generated.ts`, `timeline-commit-types.ts`, and schema; metadata remains stale, with old `35c2d9…` schema references. No compatibility credit.
- Child/runtime maker argv, template names, and bare 64-hex lock digest requirements are correct.
- Registry confirms P1/P2/P3 and `commit-integration`; P4, `first-capture-integration`, and `marked-integration` are absent and correctly described as unavailable. Scope is 2 + 8 + 1 + 3 + 14 + 24 = 52 cases, plus the P3 reset precondition.
- C0 caller/reply fields remain present, including scoped bases, commands, `created`, steps, merge, reads, `Idempotency-Key`, canonical document/digest, id map, receipts, and accepted/merged/conflict/invalid handling.
- D50 row PASS: eight columns, owner `app`, exact producer/file/body/tail provenance, full hashes verified, exactly one `created: []` addition, all other bytes unchanged, and home merge explicitly pending.

## Verification

- `node scripts/vendor-lock.mjs check config/astrid-cli-surface/vendor.lock.json` — PASS
- `node scripts/vendor-lock.mjs check runtime.lock.json` — PASS
- `git diff --check HEAD` — PASS
- `git status --short --branch` — clean
- D50 full/body/tail hashes — all matched independently
- Runtime producer result `409 passed` — reused prior producer evidence; not rerun here
- No tests, browser/HTTP/service runs, installs, registrations, checkouts, or source/ledger/design changes performed.

Limit: the recipe’s direct `cmp` block names four artifacts but explicitly compares only two; this review independently hash-checked all four. Final Agent SHA, adopted App SHA, and receipts remain unavailable. Required commit message and `DONE` marker were created.