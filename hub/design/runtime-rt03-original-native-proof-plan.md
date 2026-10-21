# RT03 original-reference native proof plan

Status: **PREREQUISITE HANDOFF — source and final pair held** (2026-10-21).

This is a bounded proof plan, not a Runtime or Agent change. It uses the
approved existing raw carrier and keeps the original reference positive strict
until a real Agent command/provider and its private Runtime counterpart are
qualified by independent reviews.

## Source identities and current disposition

- Main witness: `80973d34` (private archive used by
  `runtime-rt03-film-scope-witness-correction.md`). The exact original
  positive is
  `tests/test_runtime_exact_idempotency.py::test_timeline_shot_and_reference_creation_are_keyed_durable_and_non_overwriting`.
  Its reference payload is exactly
  `{"reference_id":"exact-reference","object_id":"object-digest","role":"source"}`
  on timeline `exact-timeline`.
- Current Runtime base: commit/tree `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`.
  Approved private carrier source: Runtime commit
  `f53bf588bf70b090ce8e0bed5ccb7d91157771b6`, tree
  `d82f37052847949e77c12e1704c3f27c6dd56a46`, changed paths only
  `runtime_protocol/timeline_commit.py`,
  `runtime_protocol/timeline_commit_port.py`, and
  `tests/test_timeline_raw_capture.py`.
- Carrier: existing `dto.MediaManifestEntry`, exactly
  `{"media_id":"sha256:<64 lowercase hex>","content_digest":"sha256:<same digest>"}`,
  read only through private request-scoped
  `raw_media_info(pin: dto.MediaManifestEntry) -> MediaInfo`. `MediaInfo` is
  the existing internal descriptor (`object_id`, `media_type`, `size`, with
  only existing optional intrinsic fields). It is not a new DTO, endpoint,
  schema, generated client, pin, activation, or release.
- Agent ACK: `peer-agent-to-runtime-20261021T010309Z-raw-pin-exact-ack.md`
  ACKs that exact carrier and requires declared-command membership, managed
  project scope, one CAS descriptor, and acceptance-time recheck. Current
  Agent is `57d6635616f2982b814cfcc059b670ea1a7c9f2c`; its command registry
  (`astrid/sdk/timeline/commands.py`) and edit-command schema contain no
  committed `timeline.reference`, `ReferenceArgs`, `MediaManifestEntry`, or
  `raw_media_info` recipe. Therefore there is no Agent source/schema identity
  to qualify yet.

The historical `object-digest` is the original opaque identity assertion. The
native positive must replace only that unsafe opaque value with the actual
ingested `media_id`/`content_digest` pin and prove that the same digest is
project-managed. It must preserve the original `reference_id` and `role`.
That is the custody correction, not a new success or a placement substitute.

## One-to-one proof nodes

The eventual private proof should use the real Agent semantic provider through
the normal Runtime commit path. It should be one small command/fixture case,
not a new harness or a `PreparedProvider` claim of parity:

1. **Seed/ownership.** Create `Exact Timeline` / `exact-timeline`, ingest one
   raw object into that project, and retain its exact
   `MediaManifestEntry`. Start from an empty accepted parent. Assert the
   `project_objects` relation is `managed` for the pin; do not create a
   catalog reference, managed generation/variant, shot, occurrence, clip, or
   project placement.
2. **Command declaration.** The Agent command (not yet present) must carry
   the exact pin in its declared command object. The provider must call
   `port.raw_media_info(pin)`, require returned `object_id == pin.media_id`,
   record the exact media dependency, and place the pin in the candidate
   dependency manifest. The command must create exactly the reference leaf
   with `reference_id=exact-reference` and `role=source`; it must not require
   or invent an occurrence/shot/clip or generation tuple.
3. **Accepted result.** Submit through the real provider and Runtime commit
   acceptance. Assert the accepted reference has the exact ID, raw object
   identity, and `source` role; the parent remains unplaced (zero
   `timeline_shots`, occurrences, clips, and placement/catalog writes), while
   the existing `timeline_references` projection has exactly the one expected
   row.
4. **Unsafe input refusal.** Repeat with a missing digest, the same object
   whose project relation is no longer `managed`, and an object managed only
   by a foreign project. Each must visibly refuse before writes, preserve the
   head and database/CAS snapshot, and never become an accepted reference.
   Do not turn any of these into a success by falling back to
   `media_info`, `selected_media`, catalog lookup, caller metadata, or public
   object reads.
5. **Restart/idempotency.** Close and reopen Runtime, submit the exact same
   command and idempotency key, and require the byte-equivalent accepted
   result/receipt. The ledger-first retry must not call the provider or reread
   `raw_media_info`; this is the direct counterpart of
   `f53bf588:tests/test_timeline_raw_capture.py::test_exact_retry_after_restart_replays_ledger_before_raw_capture`.
6. **Changed payload.** After restart, reuse the original key with the same
   reference ID but changed `role=target` (the original assertion) and require
   visible `409` idempotency mismatch with no writes.
7. **Occupied identity.** Submit a changed role under a different key and
   require visible `409` occupied-identity refusal; the original `source`
   row and all heads remain unchanged. This must exercise the native command
   identity guard, not the retired writer.
8. **Retired-route control.** Keep the existing direct timeline reference
   refusal tests unchanged: service and HTTP legacy writers remain `410`
   `timeline_commit_required` with no lookup/replay or writes. The original
   strict-xfail positive remains in place until nodes 1–7 pass with the real
   Agent provider and matching private Runtime source.

## Precise Agent prerequisite handoff

Agent must first provide a committed source/tree for the smallest native
`timeline.reference` command/provider recipe, including its current
edit-command schema identity and direct tests for the declaration, exact
recorded dependency, reference ID/role, identity collision, and empty-parent
no-placement result. Runtime can then pair that source with the approved
`f53bf588` carrier and review the resulting native proof. Until that handoff,
no Runtime source merge, schema generation, client pin/activation, public
adoption, or final pair claim is authorized.

## Existing evidence used

- `f53bf588` raw-capture focused evidence: 6 raw-capture tests; 48 port/media
  selection tests; 59 acceptance tests with 1 deselected; independent archive
  run 113 passed, 1 deselected. The restart case proves ledger replay before
  raw capture, not Agent native semantics.
- Original controls remain in
  `tests/test_runtime_exact_idempotency.py:81-124` and
  `tests/test_timeline_reference_authority.py:151-213`.
- No full, browser, renderer, live-socket, schema-generation, pin, release,
  or public-adoption run was made for this handoff.
