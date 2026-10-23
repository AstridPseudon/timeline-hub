# Runtime OPS-bench-store D27 independent Luna review

**PASS — source and combined private caller qualification.** Private qualification only; no installation or production eviction claim.

- Author artifact: `ca580d0ca39b2405a4743a51d5b10a05d8cd2432`
- Product Runtime: clean `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`
- Source SHA256: `6d9368207947aa316e1ed6486c5fa7ef843a84f50163114bb958011b538712a8`
- Manifest SHA256: `ea3df6c290430ad1d7a2696c4abf914133461999e9bcef224cf91215f7f91cec`

The source guard found exactly the intended `ensure`, `recover`, and `_delete_owned` changes. Final-seal ordering, same-final-path custody verification, no reseal on reuse, child and Runtime `seal=seal` callers, owned rollback/recovery/eviction identity checks, and foreign/symlink refusal controls all passed.

Results: core **18/18**, projection **15/15**, leases **24/24**, lifecycle **11/11**, and private queued callers **34/34 actual outcomes**, exit 0. The adapter emitted 57 PASS lines. Validator passed 83/83 manifest files, 148/148 source-before/after inputs, 14 embedded Python blocks, six zero-fuzz patch replay/cmp checks, and clean Runtime2a9/diff checks. Fixture was 1,241,088 bytes; review TMPDIR allocation was 13,475,840 bytes.

Finding: the projection test has an unmanifested dependency on the immutable 1858 baseline source. The unchanged test passed 15/15 when run from a private copy with that exact prior source supplied read-only from ORCH evidence; this is packet self-containment only, not a source/behavior failure. The initial `$PWD` validator target was the artifact commit and was rejected as expected; `/home/user/work/runtime` passed.

No product/source/test/generated/schema/pin/Git/integration worktree was modified. No full suite, browser, install, network, real bench, or production eviction ran. Next is the separate reviewed kit-install/idle-backup smoke worker.
