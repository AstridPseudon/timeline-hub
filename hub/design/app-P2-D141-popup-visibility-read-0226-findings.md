# P2 popup visibility gate — finite investigation

Verdict: **PROVED_PRODUCT_GAP**, scoped to the accepted setup head not becoming the mounted canonical occurrence/shot-group projection required by the original popup test. This is an integration-boundary verdict; it does not assign cause to App, Agent, or Runtime individually.

## Actual retained run

The pinned run is App867 / Agent28e / Runtime6a / Composition635f. D66 normal launch, native seed, Agent identity, authoritative history, and mounted-readiness all passed. The original test blob is unchanged and fails at `three-products.p2-popup.spec.ts:356`:

```text
locator('[data-shot-group-key^="f2-occurrence-copy:"]').first()
```

The retained DOM is connected and mounted but says `No shots yet`; there is no matching `data-shot-group-key`. The failure precedes the double-click, dialog, popup ADD gesture, canonical save, reload, undo, and every later original predicate.

## Fixture and boundary proof

`commitFixtureCommand` asserts `200`, `data.status === accepted`, exact base revision/publication, and `rebased_onto === null` for both setup commits: `occurrence.place-shared` followed by `doc.patch`. The Agent implementation at `native_occurrence_shared.py:295-326` validates the explicit occurrence owner and creates the requested parent occurrence entity. This is setup acceptance evidence, not a reconstructed payload.

The exact missing record is a structural canonical-read/projection record at the accepted setup head showing the requested shared occurrence in the mounted `runtime.shots.canonicalOccurrences` / `useShotGroups` input. The private phase stream records completed HTTP commit lifecycles and 200 responses but does not retain the response body needed to publish that occurrence-presence record. The DOM absence is therefore used together with accepted setup semantics and source identity, not as a timeout-only causal claim.

## Authentic pre-cut comparison

Run `app-pin-04beedcd-d73-p2-04beedcd-submit-1025075440-19078` is an authentic pre-cut PASS for the same original test SHA and the same Composition635f head/tree. Its same original ADD case passed, though the retained overall run had unrelated failures. The five production caller/renderer source object hashes (`useAstridShotsHost`, `AstridTimelineEditor`, `useShotGroups`, `TimelineCanvas`, `ShotGroupOverlay`) are identical between pre-cut App04be and App867. The selector and fixture assertions are consequently not a newly introduced locator relaxation opportunity.

## App5fe relevance

App5fe is a later merge than the actual App867 run. Its changed paths are Runtime data-provider loading, placement-service mutation preparation, and shot-group pack commands/tests. It does not change the canonical occurrence host, `useShotGroups`, canvas, overlay, or the original test. It is not evidence for the actual failure and is not credited as a fix or cause.

## Contract and scope

No product, test, fixture, pin, schema, kit, registry, queue, hub, or Git metadata was changed. The original request/response contract assertions remain untouched, including command/step fields, atomic merge, reads, idempotency, dry-run/source/rationale/group fields, accepted/merged receipt data, conflict/invalid/preview branches, and full original tails. No test was rerun under the read-only investigation hold.
