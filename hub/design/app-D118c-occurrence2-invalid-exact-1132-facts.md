# D118c occurrence2 exact invalid-timing facts

- Base: `36e44e1c0ed9b454faaf973715a2be7119552d0a`.
- Changed path: `tests/editing_conformance/test_commit_runtime_occurrence_create.py` only.
- The original file SHA-256 is `26ecb3e8da202dc9a1113f942cf9c1a7384600d8662cb9c1e8d983caf17afe6f`; the new file is `f1d86c7a95140a3f69a60e3ac348511eedf2eca52d75da135eb04450f9935ca1`.
- AST assertion conservation: 29 → 31 assertions; the only delta is status `422`, details status `invalid`, and details code `unsupported_timing`. Every other assertion source segment is byte-exact. The authored `invalid_birth['args']['on'] = 1e308` input and existing `details['reason'] == 'unsupported_timing'` assertion remain unchanged.
- The target file is absent from frozen `origin/codex/handover-timeline-r4-20261019-candidate-sdk`, proving this file is owned by this integration line.

## Contract/source basis

- C0 §1, `/home/user/work/runtime/contract/commit-v2.md:60-80`, defines the exact base pair and request semantics.
- C0 §4, `/home/user/work/runtime/contract/commit-v2.md:1299-1310`, defines invalid-at-claimed-base final timing validation as HTTP 422 with `details.status: "invalid"`, while later-head guard failures are not invalid-base diagnoses.
- Current Agent source `/home/user/work/wt/app-D118c-occurrence2-invalid-exact-1132/astrid/sdk/timeline/_commit_errors.py:65-71,90-110` maps unchanged-base `unsupported_*` to invalid and emits 422/details code equal to the reason. Fresh SHA-256: `c0e11dcdd2e6f511f18ce08afd60eff5d54554bcfb93855ab667c7e047a476e3`.
- Approved D16 is `/home/user/timeline-hub/hub/design/app-P1-D16-caller-sol-2325.md:1-14,26-33`.

## Pinned Runtime run

The clean immutable checkout was `/home/user/work/wt/rt-pin-42aad0e9`, HEAD `42aad0e92f6da8ea83dd0a382a87e3acd12651b0`, tree and fresh `git write-tree` both `085a5be70b56353deb41ae7d743336a4ccb7f29c`.

Fresh raw SHA-256 values: `runtime_protocol/errors.py` `f10518c992c28d5836fdd7916337679f0ba92b9722dacc1dd94fe408a22a49f4`; `runtime_protocol/service.py` `5a051f014e01698746dfe48b39ecadc9042b228a7a26df1bb439a79aa77b2666`; `contract/commit-v2.md` `4581ea85aada0af405b1b1b9284e9938a6dba3ca4f6980b7c3c0be8f135f9bb7`.

Both exact nodes passed the new invalid-timing assertions, preserved the no-write/history checks up to that point, and then stopped at unrelated Runtime guards:

- `[False]`: Runtime `invalid_records` at `timeline_commit_auth.py:1645`, `inverse stage materialization differs from its recorded source image` during `media_undo`.
- `[True]`: Runtime `invalid_records` at `timeline_commit_auth.py:2267`, `provider intermediate image lacks an authenticated physical promotion` during grouped birth.

These are Runtime-owned seams. No Runtime source, production source, later test assertion, or broad tolerance was changed or investigated further. The original full tail is therefore not claimed green.

Static checks all passed: Ruff, mypy with `--follow-imports=skip`, `PYTHONPYCACHEPREFIX=... python -m py_compile`, and `git diff --check`.
