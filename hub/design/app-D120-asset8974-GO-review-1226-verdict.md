# D120 current isolated registerAsset 8974: GO

Verdict: **GO for this one protected originalasset case.** The preserved service `app-pin-34d46445-d73-p2-register-asset-34d46445-submit-1025122001-8974` exited 0 in 204 seconds. Its normal preflight `5383` passed. Readiness is 1/1 PASS and the original registerAsset XML is 1/1 PASS, with zero failures, skips, and errors.

## Source custody

The service manifest, immutable checkout receipts, and live read-only checks agree on:

| repo | commit | tree | checkout |
| --- | --- | --- | --- |
| App | `34d4644589970274a5252c0f7c68b6288eb0b0b4` | `48d71e1a0c18a13668e1d1e086def9dd6210affe` | `/home/user/work/wt/app-pin-34d46445` |
| Agent | `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2` | `6056414359ae9fce08d999d54cbecf719fda33c3` | `/home/user/work/wt/agt-pin-070dfc5e` |
| Runtime | `7070f1378d1917fcce69857ebd33cd2b3015568b` | `cd68015cb9fe85a6ecd2d15dd7e2eac69f67e2b1` | `/home/user/work/wt/rt-pin-7070f137` |
| Composition | `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` | `5ab5191a296980a0a6bcd1178ab6902d6478a148` | `/home/user/work/wt/vw-pin-635f4de0` |

All four immutable checkouts are clean. The service source is clean and has App tree `48d71e…`. The manifest records pinned Agent/Runtime import roots, provider `astrid-v1`, compiler `authoring-bundle-1`, Node `v20.19.4`, Runtime `AstridRuntime/0.1 Python/3.13.16`, protocol `workspace.v1`, and schema digest `sha256:867f3553…`.

The tested source hashes are unchanged before/after: readiness `2b9723…`, registerAsset source `7cca78…`, and D66 launcher `81d273…`. Preflight manifest hash is `b5d8de…`; normal manifest hash is `babaaa…`; readiness XML hash is `06739d…`; registerAsset XML hash is `48d8e8…`.

## Predicate qualification

The original test source at `tests/e2e/local/three-products.p2-elements-assets.spec.ts:1133-1203` reaches the full tail:

- real mounted file import and authenticated media selection identity;
- semantic `clip.add-media` request with exact row/media and v2 base/scope/step/merge/source/Idempotency-Key checks;
- accepted canonical reply and independent canonical reread/digest;
- exact parent registry update, absent `config.registry` mirror, unchanged existing assets, and media manifest identity;
- authoritative history entry and scoped reload showing the added clip;
- guarded native `timeline.inverse` targeting the accepted publication;
- independently derived canonical restoration, exact Undo history, and scoped reload with the added clip gone;
- `assertNoLegacy(wire)` after forward and Undo tails.

The D115/C0/D101 asset read union is exact: the physical parent `registry` field is a `present` field dependency with its value, and the absent `parent.config.registry` mirror is a second `absent` field dependency. The source does not optionalize or replace that envelope. The native response oracle deep-compares independently derived result, canonical document/digest, command/step metadata, receipt, authenticated history, recorder metadata, and Undo history; its mutation controls reject wrong/missing/extra path, ref, state, or value fields.

## Limits and overall status

This is only the 8974 proof. I did not use 27438 or 15712 as case evidence, and I did not run tests, typecheck, lint, backend, HTTP, browser, a new body, or source edits. The mutable `/home/user/work/agent` and `/home/user/work/runtime` have since advanced beyond the pinned Agent/Runtime sources; therefore this GO is strictly for the preserved service run against the immutable tuple and is not a claim for those later heads.

Overall P2 remains **NO-GO** for SWAP and element. This case would make 6/8 on the named tuple runs, not a full-tour GO.
