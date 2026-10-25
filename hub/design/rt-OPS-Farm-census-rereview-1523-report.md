## Report

Result: **FAIL diagnostic fitness**. Actual Farm census remains **EXACTMISSING**; no Farm root/build/install/reissue was performed.

Findings:

- Static counts (46/121/143) do not prove dynamic coverage. Store and dependency layers only check small subsets.
- License ownership, exact distribution metadata, dependency lock/wheel/hash checks, Store locks/registrations/projections, and several retained-path bindings are not independently covered.
- Farm schema source handling is misaligned: the production caller uses `commit:packages/timeline-schema/python`, while the diagnostic archives the whole commit.
- Deadline is 20 minutes, exceeding the required 15-minute bound.
- Several globs/reads are unbudgeted; output can overwrite an input path.
- Unexpected `SyntaxError`/`AssertionError`/`RuntimeError` can escape structured boundary reporting.
- Installed source hashes are only compared before/after, not pinned to the required exact hashes; call-graph validation is regex-based.

Tests:

- `python3 -m py_compile <diagnostic>` — PASS.
- Exact absent-root invocation — PASS execution; result `EXACTMISSING`, no PASS/COMPLETE claim.
- `python3 -m json.tool <result>` — PASS.
- Installed hashes before/after unchanged: maker `e62f…dc3`, Store `7d58…495`, dependency verifier `116b…bfe2`.
- Worktree clean; no product changes.

Required corrections: implement independent bounded checks for all three production layers and license/source-carrier/Store/dependency guards; correct Farm schema subtree binding; enforce a 15-minute deadline and budget every filesystem operation; reject output/input overlap; catch and report all unexpected exceptions; pin and verify exact installed source identities.