## Report

Reviewed [g4-managed-duck-0856.row](/home/user/work/wt/agt-G4-duck-row-review-0857/evidence/g4-managed-duck-0856.row).

- PASS: exact Agent source/tree/blob and 17 AST assertions.
- PASS: Runtime `becfe6db…`, tree, auth blob/SHA-256, clean state, and origin.
- PASS: `HEAD^` snapshot semantics against `bin/test-run`’s `commit-tree -p HEAD`.
- PASS: `bash -n`, stdlib `shlex`/AST checks, benign selector forwarding and failure propagation, `git diff --check`.
- Compared with 0832: preserved the tuple while adding explicit HOLD inputs, snapshot-parent guard, `--noprofile --norc`, full cleanliness, and selector forwarding.

The row remains explicitly blocked pending:

1. One genuine installed child for Agent `0ff3d103…` / tree `1d613f…` and Runtime `becfe6db…` / tree `7edc08e…`.
2. Its immutable host/profile path and bytes.
3. A matching managed-Store receipt proving that exact tuple.

Existing `ba8f0bc8…`/`f3208b26…` and failed `0c2c28da…` candidates do not qualify. Future binding must use one supported managed-child installation and receipt, then verify the row’s guards before service execution.

No imports, preflight, pytest, service, provisioning, registry, product edits, or full suites were run. Commit message written and `DONE` created.