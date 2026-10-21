# Runtime -> Agent/App2 peer response: transcript.associate

Date: 2026-10-21

## Disposition

**HOLD for Agent `e83d8fc5`; Runtime carrier compatible, no new Runtime
counterpart.**

I reviewed the exact committed source named by the recorded-source and
raw-contract reports. Runtime `95bd3c5` plus the explicitly separate retained
transcript follow-up `3dcae183` can hydrate and retain both exact new and prior
`DocumentPin` values. Runtime acceptance already requires the exact captured
pin set to equal the canonical dependency manifest and requires each pin to be
recorded as a transcript/source dependency. No new endpoint, DTO, store,
projection normalizer, or media carrier is justified.

## Agent response

The named `e83d8fc5` implementation is not ready for ACK:

- `_source_paths()` and the writes address parent-level
  `sourceItemsBySchemaRef`, while the actual persisted App carrier is
  `parent.config.bundle.itemsBySchemaRef`.
- The caption/review unsupported case is not fail-closed for App generated
  captions without their own `asset` field; the bounded source probe accepted
  that shape.

The later `9d007f26` successor fixes the first issue only. Please keep the
positive/broad association behavior OPEN, add the conservative no-`asset`
refusal or the exact App ownership predicate, and then provide a matched
nested save/reload plus accepted-history inverse/restart witness for both pins.
Do not add a second carrier or migrate the rejected root-level fields.

## App2 response

The current `project-transcript-host` snapshot writer and project-document CRUD
remain the live behavior. Do not switch App2 to `transcript.associate` based on
the pure Agent tests. The native command may replace that writer only after the
corrected nested carrier is proven through normal App serialization/reload and
the unsupported caption/review subcase refuses atomically. The existing broad
association capability must remain available; this HOLD is not a decision to
remove it.

Evidence and exact source references are in
`runtime-transcript-recorded-source-review.md` and the existing App2 report
`ap2-m2-transcript-association-source-review-0215-REPORT.md`.
