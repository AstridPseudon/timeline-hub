# D141 App journey handoff

Status: prepared, not dispatchable. No journey body was run.

## App cut

The App packet is bounded to the existing D66/D73 routes:

- P1: `p1` — original chain only.
- P2: `p2-automatic-child-placement`, `p2-popup-add`, `p2-parent-move`, `p2-transition-none-single`, `p2-transition-none-bulk`, and `p2-register-asset`.
- P3: `p3` — Gate5 original.

The exact source files, source hashes, original grep selectors, historical qualified tuple pointers, C0 v2 field guards, pure-preflight command, normal command, disk admission, and serialized heavy-run rule are in `recipe.json`.

P2 `SWAP` and `Element` are explicit owner-morning-cut exclusions. They are not skipped predicates for the six included routes, and the broad P2 result must not be represented as qualified.

## Hard gate

Do not run a body until the D141 control record supplies all four final commit/tree pins and a recorded MAIN GO. The final tuple is absent from the available control documents; the historical qualified tuples in `recipe.json` are evidence pointers only and must not be substituted.

After the tuple and GO arrive, use the existing D66 `--submit`/D73 plan path. It must create the exact normal and preflight suite rows through the central service, run pure preflight first, and queue the normal row only after preflight passes. Use `request-test`/`wait-test` through the service, with `--no-cache`, one heavy body at a time, and the documented reserve/stop thresholds.

## Peer handoff

Agent owns P4. Runtime owns P5. They should consume the same final four-way tuple and MAIN GO, then use their existing normal routes for P4 publish/transport and P5 renderer-off save/authorization/crash-retry behavior. App does not add a P4/P5 controller. Preserve C0 v2 envelopes, exact history/undo predicates, and zero legacy traffic across the handoff.

## Missing inputs

The cut record still needs the final four-way pins and trees, receipt/checkout identities, service-generated suite row names or plan, and AST hashes if AST hashes are mandatory for admission. No AST hash was present in the retained qualified evidence, so none is inferred here.
