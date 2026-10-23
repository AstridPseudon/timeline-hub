# P1 mounted-chain source handoff

Status: **source repaired for independent re-review**. This handoff records the
test-only correction on top of `1372d5fe7`; it is not H3 acceptance evidence.

The source now drives the real mounted App split through the existing UI ruler
seek seam to `SPLIT_AT = 2`, holds the authentic split commit before Runtime
acceptance, authors the new-ID trim locally, and verifies that the dependent
outbox intent remains behind its predecessor. It then forwards the unchanged
split, holds the actual trim request before Runtime acceptance, lands a
disjoint Agent track-label edit, and forwards the unchanged trim. The trim must
return modern `merged` with `rebased_onto` equal to the Agent head. The ACK is
then lost after Runtime has accepted the trim; restart/recovery must replay the
exact original body and idempotency key and receive the byte-equivalent
`{data, receipt}` envelope without a second history entry.

The refusal branch now checks the structured conflict reason/current head and
conflict list, the retained-save message, the rejected outbox state, and the
canonical split plus Agent move without the stale trim. Modern successes require
`accepted` or `merged`; `rebased` is not accepted for these calls.

The request/reply checks cover the exercised v2 fields: scope and both base
IDs, command envelope, label, step identity/intent/tags/ordinals/patch,
`merge`, `dry_run`, idempotency key, canonical document/digest, id map,
provider/compiler versions, receipt identity/result, and authoritative
`steps[].dependencies` (not a fictitious top-level `dependencies` field).
Opaque/null/foreign app data, absent split-side intent data, list membership and
order, canonical mirror closure, registry, and Agent label preservation are
asserted.

The original corpus remains a descriptor corpus, explicitly
`authored-not-go`, rather than a runnable browser blob. The exercised edit is
the original `app-native-trim-real-document` intent from
`tests/fixtures/p1-feasibility/cases.json`, backed by
`src/tools/video-editor/commands/fixtures/recipe_m2_clip_trim.json`; the
split-created-ID and Agent-label descriptors are retained as the intended
cross-product semantics. The browser seed uses the harness's real media object
through the existing direct genesis seam, because the fixture descriptors do
not contain a runnable mounted closure. This is bounded coverage of the
mounted parent chain; unrelated invalid/preview shapes remain unexecuted.

Later selector: `tests/e2e/local/three-products.p1-chain.spec.ts`, after the
official Runtime 780 producer/client join, normal A2 outbox caller, and current
trim consumer are integrated. The source was not run in a browser or against
live sockets in this worker.
