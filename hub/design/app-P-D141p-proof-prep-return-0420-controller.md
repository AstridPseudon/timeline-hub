# D141p corrected execution controller

Status: `NOT_READY`. This controller is documentary. No source checkout,
builder import, service submission, registration, preflight, browser, provider
import, collection, or proof body ran.

## Admission and serial order

1. Placement is first. Admit each D141g-a pair once at `>= 4.6 GB` available
   bytes with one heavy unit at a time.
2. Keep one continuous 5-second `KEEP` trace across preflight and body. Enforce
   the `4 GB` stop before, during, and after the pair. There is no second floor
   gate between preflight and body.
3. The first placement trace measures `X`. Before any later pair, use
   `max(4.6 GB, 4 GB + X + 0.2 GB)`. If the computed minimum is `<= 4.3 GB`,
   notify the lead before queueing the next pair.
4. Run the remaining five named P2 selectors, then P1, then P3, serially. The
   six P2 selectors are exactly the six entries in `source-manifest.json`.
5. If the installed paired kit is missing, use the ordinary `5 GB` rule and
   `WAIT`; do not invent flags or use direct `--run`, queue edits, reissue,
   re-targeting, or cancellation of old rows `18617` and `19479`.

Runtime and Composition are fixed qualified tuple members as recorded in the
manifest. Exact detached checkout custody and receipts, the installed kit,
and the new App/Agent source receipts remain gates. Existing D141p/D141l
authority is sufficient; this controller adds no new MAIN authorization wait.

## Existing D66 route only

When the genuine tuple and receipts exist, the source owner runs the existing
production `buildSubmitPlan`/`serviceRecipe` path from the authenticated final
App `scripts/testing/d66-plain-stack.mjs`, then the normal D66 `--submit` route.
The pair is atomically registered by that existing route; compare its actual
registered bytes to the builder output before either paired part runs. Then use
the existing central service, preflight first and normal second:

```text
request-test <app-pin-target> d141g-<selector>-<APP_HEAD8>-submit-preflight --no-cache
wait-test <preflight-result-id>
request-test <app-pin-target> d141g-<selector>-<APP_HEAD8>-submit --no-cache
wait-test <normal-result-id>
```

No hand-written row, generic receiver, new receipt schema, direct `--run`, or
arbitrary module path is permitted. The exact output root for any prospective
evidence is the absolute packet root recorded in `readiness.json`; actual
registered bytes are not written by this preparation.

## D141j and scope dispositions

Popup ADD is unchanged. A PASS is reported exactly as `NOT REPRODUCED`, with
cause undetermined; it is not called fixed. A FAIL is preserved and stops the
popup line. A later diagnostic body may start only after a retained pre-body
artifact proves these four fields visible: read-head continuity, occurrence
presence in that read, `activeCanonicalOccurrences` before `useShotGroups`, and
shot-group output before `ShotGroupOverlay`. No collector is added now.

P4 requires checking the actual freeze-2 source path against the existing
`app-P4-D141-path-independent-0226` map. No duplicate P4/P5 body is created.
D130 and all other existing stops remain unchanged.

