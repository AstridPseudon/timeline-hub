# Handoff — ap2-P1-ancestry-ops-return-0740

## OPS PASS

The current `app ap2-P1-chain-h6` row is independently qualified against the intended candidate.

- Candidate source SHA-256: `d72798b2301973bfdabcf3b07c2746896e9ec5cd6188bebeda53733c070647a8`.
- Candidate commit/tree: `2b26c20a99fd14a9076fd0cbd6aa5548de14e35b` / `45f4b3ca9e204d3cc0223bb9929301ab5e40cf25`.
- Integrated `890` commit/tree: `890b9561666c3619f69335dd747b15e042b3a9a3` / `20c8c1ed5e9ca48bc1f56f66f0404c83f8d97473`.
- `git merge-base 8770aa1625198826778828173ef6e2c55a3c07f3 HEAD` returns exactly `8770aa1625198826778828173ef6e2c55a3c07f3` on both candidate and integrated `890`.
- OPS row: `37`; row SHA-256 `4d9c9db6a04646bd25d9eaf828a62897209a2c92980cf0b6bff265643a41ea81`.
- OPS file SHA-256: `c4e4e6f03a3cf79258de2393ce0017009f702238d0a57a4688bbf5a0e5ca1cf8`.
- Outside-row SHA-256: `228aa796658c29ac27d4071c7c2aef98f81e788d97fc614ffd6f41ab326af341`.
- All 11 row source/archive hashes match the candidate; the final source literal occurs once and the prior literal zero times.

The 0734 review’s “extra guard substitution” finding was accurate for that brief. The current manager brief explicitly authorizes and requires this exact `merge-base 8770… HEAD` guard, because `HEAD^ == 8770…` would reject the intended startup/paired-head/oracle/diagnostics descendant candidate. The current guard therefore passes source qualification and must not be reverted.

Private Composition graph (80 files, `0.0.14`, three public exports), normal Agent `f894c3c9…` / Runtime `34eac004…` execution identities, provider hash `46fbdca6…`, selectors, launch/list/type/lint/body checks, and outside bytes all pass. No product or test-body files were changed by this worker.

No browser, body, socket, service, build, full-suite, or original two-case run was performed. Proceed only with the manager-owned single changed-evidence original two-case run; do not merge a red test or retry an unchanged error.
