# D141cc independent whole-path findings

## Verdict

Complete, read-only, source-faithful mapping. No product fix, no production-body claim, and no native-route qualification. The current private 1032 candidate remains a procedure model only. The unchanged native builder is retained.

## Exact passing-versus-cancelled comparison

The retained exact tuple is App `82e9e13ddf1d7ec6c736521b2eb091dca9877598` / tree `6a6e49eb4461b5ca1a7fa1247653bc794f26d710`, Agent `ecdc242ed9b673f641759ecf029f95e89a2c6f92` / tree `d362fe9dfdbd0c1fc8e0739c193ed2b74a7d2735`, Runtime `95d98f038320d5d46bd679ac000ab3e15825c935` / tree `78df31d62c5b9ba4c84dee4ea346e43a767718c1`, and Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` / tree `5ab5191a296980a0a6bcd1178ab6902d6478a148`.

- Placement preflight `...1026101609-6758` passed; normal `...1026101639-9168` passed, exit 0 in 259 s. This is a bounded placement PASS only.
- Popup preflight `...1026102125-437` passed. Normal `...1026102149-13234` was running, then cancelled with exit 130; normal `...1026102155-20413` was queued, identified itself as identical while `13234` was in flight, then cancelled without a body exit. Neither has a functional popup verdict.
- The six other selectors (parent move, transition single, transition bulk, register asset, P1, P3) remain NOTRUN. No D141j diagnostic was triggered.

The 1026 original whole-path report attributes the popup outcome to overlapping worker/controller invocations, not an internal native retry and not an independent service caller. The unchanged builder has one normal `request-test` call per actual `--submit` invocation. The native artifact lock at lines 704–710 remains unchanged and is part of the production mechanism.

## Review-next findings, all intrinsic to the private candidate

1. **D141cc-R1 — synthetic popup retry.** The candidate's authorized retry is not generated from the unchanged `serviceRecipe`. Builder command SHA is `27fcd174df3f214502bbca1e67b0eb366c361c11e1f5ae5c0c48d7a987582501`; candidate records `809c1a5ed1be729808d335c8c18dbfdee3ccd73d9454e4739b91e256572def37`. Builder retry row SHA is `c89f8ac7430f4e5342fbffb23cd5ce4aa54f2151e38b3e46af7035aea13fc6c3`; candidate records `17e8a4acc32f21825eb0642d7e7a832889ec10b9591c0a05795e2dfa8cf6a018`. Six original rows match, but the authorized retry does not. This is a candidate/source-binding failure, not evidence against the builder.
2. **D141cc-R2 — preflight/normal interleaving.** The FakeService adversarial control creates another normal request immediately after preflight creation and before normal creation; observed `normal_calls=2`. The candidate does not re-inspect same-target/suite candidates or acquire the unchanged builder lock at that boundary. The model therefore does not prove adoption of a real request created in that window.
3. **D141cc-R3 — mismatched tuple is not fail-closed.** A same-target/suite candidate with matching source digest but wrong command bytes is silently excluded by `exact_candidates`; the candidate then creates a normal request. The command/row digest-to-byte relationship is not checked. A real future route must stop on this mismatch rather than create.

All three findings are intrinsic private-candidate findings. They do not authorize a source repair here and do not convert the native builder or product into a defect.

## FakeService-to-native gap

The private controls prove only in-memory procedure properties: adoption, selector isolation, terminal-status honesty, and disk-stop attribution. They do not execute the unchanged builder; do not exercise `serviceRecipe` lines 375–395; do not call `registerSubmitRecipes` lines 407–425; do not persist/inspect the actual submit artifact; do not acquire the real `.lock`; do not enqueue a genuine `request-test`; do not observe daemon snapshot/receipt timing; and do not call `wait-test`. Consequently, `PASS_PRIVATE_CONTROLS` is not native readiness or live service qualification.

## Safe finite procedure

For a future caller, use one existing owner/tool session and the unchanged builder with the exact tuple and exact unique suite/output/plan paths. Before any create or relaunch, inspect authoritative same-target/same-suite/source request records and the durable artifact. Under the existing artifact lock, adopt an exact preflight/normal ID if present; a missing normal ID is not permission to call `request-test` from a second independent process. A live or unknown owner is a finite custody stop. A mismatched source/argv/command/row tuple, multiple candidates, missing receipt, or safety refusal is also a finite stop for that selector. Only after a real normal terminal receipt may the original body be credited.

The same native artifact lock cannot justify a second independent manual normal request: it serializes the unchanged builder's own submit path for one artifact path; it is not an external lease or authorization for a worker to repeat the normal request. The original overlap is evidence for preserving this ownership rule, not for adding a new interface, guard, lease, kit, or authorization mechanism.

Do not resume cancelled popup IDs `13234` or `20413`, do not backfill their body verdict, do not reopen popup ADD in this pass, and do not investigate safety-refused paths. The remaining selectors may only be considered later under the single-owner finite procedure, one at a time, with the 4 GB stop.
