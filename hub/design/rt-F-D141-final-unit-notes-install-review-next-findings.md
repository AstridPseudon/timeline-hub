# F D141 final unit-notes installation review

Verdict: **FAIL_CUSTODY_LIMIT**.

## Passed checks

- README target: regular non-symlink `0644`, 38,282 bytes, exact accepted candidate `48013c7fbcb8f72a7d4371540b50a4abcc43dd8c6274d90726beec82b8f9fc02`.
- gate-results target: regular non-symlink `0644`, 35,582 bytes, exact accepted candidate `506e4461b63e81af490e4b43c5eb7fe2717ebb07825c77d216a59967d863a55d`.
- Backups are regular non-symlink `0644` files and hash to preimages `13f2b3409d42313dd2ed02d1d479bc5e27cb74f7ec29151e30199428fe0bc776` and `b29945990c34adc8d8ae0b25f8c6621c4c509f43c84b22adb7dedca141815b47`.
- Candidate bytes equal installed bytes and preserve each complete backup prefix.
- The production caller was inspected before execution. Only `render_readme` from `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build` was invoked with controlled `agent`, `runtime`, `app`, and `composition` dictionaries; `main`/CLI was not called. Placeholders resolved, fences balanced, disclosure count was 2, the complete table heading count was 1, the numbered ID count was 32, and the missing-gate fallback retained `Not recorded yet.` without the gate placeholder.
- A fresh read-only traversal found exactly 568 outside regular non-symlink files at genuine paths under `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/delivery`, excluding only the two canonical target paths. The current inventory matches both retained maps byte-for-byte and mode-for-mode.

## Finding

The installer method took an in-memory outside inventory before replacement and compared it after replacement, but the first process exited after the CAS when its fallback assertion was too strict. It therefore did not serialize the pre/post inventory. The follow-up was read-only, but initialized both `outside_files_before` and `outside_files_after` from the already-installed current tree. The retained maps are consequently equal and match the current 568 paths, but they are not an independently observed genuine pre-install map. Genuine all-568 pre/post conservation is **UNOBSERVABLE** from the durable artifacts.

The installer log supports that the first process reached and passed its in-memory outside comparison before the fallback assertion, and supports that no second mutation occurred. That is historical process evidence, not an independent retained preimage inventory. The installer disk trace has no retained PID, exit code, wait, or reap facts; those lifecycle facts are unobservable for the installer. The review sampler lifecycle in `sampler-lifecycle.json` is a separate read-only monitor and must not be attributed to the installer.

## Scope and limits

The protected `0909` candidate checks and the `0914` controlling publication remain inherited documentary scope; this review performs no new content classification. Historical counts, applicability boundaries, and the existing finite App-unit scope remain unchanged. This review makes no product, full-suite, REG0, gate, build, ZIP, or final-delivery claim.
