# Validation

- Accepted source recipe: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P-D141cc-submit-owner-sol-1047/evidence/dispatch-recipes.json`; `dispatches[4]` only.
- Independent review publication: PASS_SOURCE_ONLY, 43 controls.
- Programmatic preflight: exact all-four source pins/checkouts, builder SHA/blob, loaded Agent SHA, D66 environment, argv/cwd/unset/operational environment; final native custody action `FIRST_NATIVE_INVOCATION_ONLY`.
- Native submit: one exact `--submit` invocation, exit 0; preflight `app-pin-82e9e13d-full-d141-p2-register-asset-82e9e13d-submit-preflight-1026115730-3534` pass/0; normal `app-pin-82e9e13d-full-d141-p2-register-asset-82e9e13d-submit-1026115800-10328` pass/0.
- Normal observation: `wait-test app-pin-82e9e13d-full-d141-p2-register-asset-82e9e13d-submit-1026115800-10328` — pass, exit 0, 260s.
- Journey result: 1 readiness passed and 1 registerAsset test passed; no failures.
- Raw custody: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-pin-82e9e13d-full-d141-p2-register-asset-82e9e13d-submit-1026115800-10328/KEEP` exists; marker recorded at `2026-10-26T11:58:01Z`.
- Disk trace: 81 direct 5-second samples; min available `4861698048` bytes; 4 GB stop not reached; sampler explicitly signalled, waited and reaped.
- Product/source/pin changes: none.

Boundary: this evidence covers only the admitted original `p2-register-asset` selector; it makes no broader P2/platform or packaging claim.
