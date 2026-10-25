# D120/P2 independent five-case partial-GO review

Verdict: **PARTIAL-GO for five authentic original PASS cases; overall tuple remains NO-GO.**

The review used the actual normal D66 run `app-pin-34d46445-d73-p2-34d46445-submit-1025114516-11251`, with preflight `...-1025114446-12718`. Preflight passed (exit 0). The normal run ended `FAIL`, exit 1, after 643 seconds. Readiness was 1 PASS. The original XML was 8 tests: 5 PASS, 2 FAIL, 1 NOTRUN, 0 errors. No second body or diagnostic investigation was run.

## Custody and source

The explicit tuple was consistent across the persistent plan, D66 manifest, source-preflight manifest, terminal packet, and genuine checkout receipts:

| source | commit | tree |
| --- | --- | --- |
| App | `34d4644589970274a5252c0f7c68b6288eb0b0b4` | `48d71e1a0c18a13668e1d1e086def9dd6210affe` |
| Agent | `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2` | `6056414359ae9fce08d999d54cbecf719fda33c3` |
| Runtime | `7070f1378d1917fcce69857ebd33cd2b3015568b` | `cd68015cb9fe85a6ecd2d15dd7e2eac69f67e2b1` |
| Composition | `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` | `5ab5191a296980a0a6bcd1178ab6902d6478a148` |

The normal manifest is SHA-256 `892c089c4a03c04c7ca12f487766116e39595be7970bd1a733418e65356588ca`; preflight manifest is `c120f04e621d4cd0624e2588dc0b6e8180debc490f849ad78a158364c43058c8`. All four original test source hashes were equal before/after and match the pinned App checkout. The service manifest records pinned import roots from `agt-pin-070dfc5e` and `rt-pin-7070f137`, provider `astrid-v1`, compiler `authoring-bundle-1`, Node `v20.19.4`, npm `10.8.2`, Python `3.13.16`, protocol `workspace.v1`, and schema digest `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`.

The tested source files were unchanged:

- `three-products.mounted-readiness.spec.ts`: `2b9723db262978ebbb410d5925163fe61c4a83f05f3b44fbbd524bc9df301593`
- `three-products.p2-popup.spec.ts`: `09f5e2c2ea2a207575534a88adf2847d68cdd389caa5d145580100f21302b2b9`
- `three-products.p2-tour.spec.ts`: `83948c53c7990824fce81be7f0db2b4f947837c66a827abf2ffb08492f09bee4`
- `three-products.p2-elements-assets.spec.ts`: `7cca78274f96c9466d82bea3108f6f8a447462c9cd722c078ab958bc3578d637`

Support harness/oracle/fixture hashes, checkout receipt hashes, the generated plan hash, recipe hash, D66 launcher hash, XML hashes, and import-root hashes are recorded in the JSON packet beside this report.

## Per-case verdicts

All five cases below are GO because their complete original tails reached terminal PASS in `d66/p2.xml` and the source predicates were reviewed in full.

1. **ADD — GO.** XML `p2.xml:74-76`; source `three-products.p2-popup.spec.ts:920-947`, with request/semantic guards at `423-578` and the full reload/Undo tail at `854-918`. The test verifies the v2 envelope, occurrence fork plus occurrence add-media, authenticated imported selection, exact whole canonical document, provider history/records/dependencies, reload projection, close/dialog-gone, guarded native Undo, restored history/document, and zero old-route writes.

2. **Parent move — GO.** XML `p2.xml:119-121`; source `three-products.p2-tour.spec.ts:746-776`, with the shared complete tail at `680-744`. It verifies the exact parent `at` patch and before guard, complete declared timing/asset/track/collection reads, exact field isolation, closure/digest and authoritative reread, history recorder/dependency metadata, reload, guarded inverse, full restoration, repeated history, and no legacy writes.

3. **Single transition clear — GO.** XML `p2.xml:119-123`; source `three-products.p2-tour.spec.ts:778-796`. It verifies one exact raw `remove` with a present before value, strict absent-after semantics, opaque/non-target preservation and list order, declared guards, complete canonical/history/reload tail, and guarded Undo restoring the original transition.

4. **Bulk transition clear — GO.** XML `p2.xml:119-125`; source `three-products.p2-tour.spec.ts:798-817`. It verifies the two exact ordered raw removes, both before guards, strict two-target absence and list/order/opaque preservation, full canonical/history/reload tail, guarded Undo restoring both transitions, and zero legacy writes.

5. **Automatic child placement — GO.** XML `p2.xml:71-72`; source `three-products.p2-elements-assets.spec.ts:1214-1295`, with reload helper at `1018-1036`. It verifies real import/selection identity, occurrence add-media request, closure/digest, exact child row/registry/manifest effects, history and no legacy writes, reload projection, the merged D113 real Close followed by dialog-gone before native Undo, guarded inverse restoration of parent/shot/internal closure, and final scoped placement residue absence.

## Excluded outcomes and credit

- SWAP remains FAIL at `three-products.p2-popup.spec.ts:495`, with the public 409 refusal reason `history_unavailable`; zero credit.
- Element remains FAIL at `three-products.p2-elements-assets.spec.ts:1052`; backend outcome is UNKNOWN; zero credit.
- registerAsset remains NOTRUN at `three-products.p2-elements-assets.spec.ts:1133`; zero credit.

These were kept visible and were not re-investigated. This packet is not element credit, final-cut credit, or an overall GO.

## Verification limits

Per the readonly brief, I ran no tests, typecheck, lint, full suite, browser/backend/HTTP rerun, provisioning, package rerun, second body, or diagnostic investigation. I ran read-only manifest/XML/source/hash checks and `git diff --check`; the assigned worktree remained clean.

Exact safe artifacts are in `partial-GO.json`. The producer’s safe packets consumed were `notes/submission.json`, `notes/terminal.json`, and `submission/full-p2/p2-submit-plan.json`; no raw logs, authentication, request/response bodies, opaque payloads, URLs, private stacks, or message identifiers were exported.
