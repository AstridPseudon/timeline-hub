# D108/P2 independent partial-GO review

Verdict: the four authentic original PASS cases are case-level GO. The early tuple remains overall NO-GO: the service exited 1 with 4 PASS, 2 FAIL, 1 ERROR, and 1 NOTRUN. Failed/errored/not-run cases receive zero gate credit. This is early-tuple evidence only, not D111 final-tour/final-cut credit.

Evidence was read-only. The normal service record is `app-pin-04beedcd-d73-p2-04beedcd-submit-1025075440-19078` (exit 1, 716 seconds); readiness is PASS 1/1 from `app-pin-04beedcd-d73-p2-04beedcd-submit-preflight-1025075410-15434` (exit 0). The original XML is 8 tests: four PASS, two failure nodes, one error node, one skipped node. XML SHA-256: `5b0f6377b0ca81d77962e8cd750cd9e1472090f0c40d52cb982a7f1d94d3f1da`; readiness XML SHA-256: `c81c0c66189c855dded26685cf8a723c2526e16720dc0f880b326b1a8486005c`.

## Four GO cases

- ADD (`three-products.p2-popup.spec.ts:941-947`): the original predicate covers the real mounted popup gesture, occurrence fork plus A2 media-add command, completed media import and authenticated media selection, exact canonical closure/effects, authoritative receipt/history/head, reload, native inverse restoring the original closure, and zero legacy writes. Shared predicates are at lines 423-444, 494-570, and 854-918.
- Parent move (`three-products.p2-tour.spec.ts:745-775`): exact `doc.patch` set of the selected clip's `at` to 5, complete provider/read guards, only-intended-field delta, authoritative canonical/history/receipt checks, reload, guarded `timeline.inverse`, full restoration, and zero legacy writes. Shared predicates are at lines 257-313, 337-474, 532-620, and 679-743.
- Transition single (`three-products.p2-tour.spec.ts:777-795`): exact present-before transition removal, field/pinned-group guards, opaque-field/order preservation, authoritative history/reload, guarded inverse restoration, and zero legacy writes. Shared predicates are at lines 476-530, 584-620, and 679-743.
- Transition bulk (`three-products.p2-tour.spec.ts:797-817`): exact two-clip selection and transition removals, per-clip guards, opaque-field/order preservation, authoritative history/reload, guarded inverse restoration of both clips, and zero legacy writes. Shared predicates are the same as the single case.

The common tour proof checks the accepted/merged reply envelope, canonical closure against the Runtime readback, exact changed fields, receipt-linked history and dependencies, reload persistence, `timeline.inverse` targeting the accepted publication, complete restoration, preserved prior history, and no legacy route traffic. The popup proof additionally checks occurrence-qualified rendering, exact child counts/tracks/assets after reload, and authenticated media bindings.

## Custody and contract cross-check

The normal and preflight manifests agree on the pinned tuple: App `04beedcd18b8abb49502f65cd3facaafbe93db4e` / tree `300d186a45d3d0b96ef2ae39582f1e9b4a760e7d`; Agent `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2` / tree `6056414359ae9fce08d999d54cbecf719fda33c3`; Runtime `1daca2a33f6d7b10053e07c539a54843e3984e19` / tree `a522511414947e48e317a5e5c2103483b121a750`; Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` / tree `5ab5191a296980a0a6bcd1178ab6902d6478a148`. All four actual pinned checkouts were clean. The service source tree is the App tree, and the manifest's import roots point to the pinned Agent/Runtime checkouts, not ambient newer prose.

The four source test hashes are unchanged before/after: popup `09f5e2c2ea2a207575534a88adf2847d68cdd389caa5d145580100f21302b2b9`; tour `54ea18f3f3fa8fef2eb31cc0a05809ede76099f3bee9bf0511824e652a85f7`; elements/assets `9b8791e6e3b71155daab01440466987de406b23e2b6269dcc67872cc75c807c7`; readiness `2b9723db262978ebbb410d5925163fe61c4a83f05f3b44fbbd524bc9df301593`.

C0 §§1–7 were checked against `/home/user/work/wt/rt-pin-1daca2a3/contract/commit-v2.md` (SHA-256 `4581ea85aada0af405b1b1b9284e9938a6dba3ca4f6980b7c3c0be8f135f9bb7`): request/base/idempotency (60–92), closure and previous-value patch semantics (276–320), conflicts (595–612), replies (703–715), guarded inverse/history scan (1563–1635), meta preservation (4544–4581), and history/attribution (4609–4637). The requested Astrid control-doc directory was not present; the pinned Runtime contract is byte-identical to the available read-only hub design copy, so no alternate product source was used.

Artifact hashes and safe source/import identities are in `partial-GO.json`. No raw logs, auth material, request bodies, keys, URLs, or private identifiers were exported.

## Not run

Per the brief, no tests, tsc, lint, full/browser/backend/HTTP/provision/body/package reruns were performed. Only parsing, hashing, source/tree/import-root verification, XML membership/status checks, and local `git diff --check` were performed. The worktree remains clean and no product/source/test/generated/pin/manifest files were edited.
