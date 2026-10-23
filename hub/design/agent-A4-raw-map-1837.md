# A4 exact raw-provider case map

Date: 2026-10-23 UTC  
Worker: `agt-A4-raw-map-1837`  
Scope: read-only continuation of the existing A4 provider map at Agent
`78738040d72ce74c42ddf7731221aecb06f9246d`.

## Verdict

This is a case map, not a parity or suite verdict. The current Agent provider
has three relevant bounded evidence families:

1. registered `clip.add-media` parent-media provider evidence;
2. registered generic `doc.patch` / `list.move` evidence using the App-shaped
   track fixture; and
3. registered generic `doc.patch` evidence using an App-shaped nested transcript
   bundle plus the existing exact transcript source-input boundary.

The second and third families are deliberately generic-provider witnesses.
They do not prove `track.reorder`, `transcript.associate`, mounted App execution,
Runtime/HTTP execution, or the old capture envelopes. All old App capture files
and tests remain KEEP. The old App preview/editor acceptance and normalization
are not raw-provider evidence.

The current production App save boundary is `localSaveSession` (A2), which
serializes persisted document intent as generic `doc.patch`; the dormant
`commitSession` path is type-only/detached at the reviewed source snapshot.
The production raw-provider boundary is the Agent provider reached by the
normal commit service, not local App preview.

## Evidence heads and source identities

| evidence | exact head / blob | qualification |
|---|---|---|
| Agent current | `78738040d72ce74c42ddf7731221aecb06f9246d` | current source requested by the brief |
| Track witness | integrated in `1962a2413095a2f82bf927e7c42c532072b5c812`; blob `ca046a721d527a1f6bf383659b8b5bbaada4d13d` (SHA-1), SHA-256 `fa9aa1ce49e3acab4fda0be91f62ad6c3f98b704b3b063c4c7450d6febeff546` | nine collected cases; direct targeted run `9 passed in 2.43s`; current HEAD retains the blob |
| Transcript witness | integrated in `14fc0740f278e13c3075fa12d5ebf975cc7044af`; blob `c074858c073b0594985729f13bd26b633b7cd66d` (SHA-1), SHA-256 `5181e08490658dcc97e367b38c7a54f19687e539994c3535128d08f5d085d182` | seven cases; pinned integrated run `7 passed in 1.80s`; current HEAD retains the blob |
| Track review source | App donor `68594c668` / track fixture blob `b79b69f9a95b8df417c7b157f0db92eb803535e3`; fixture content SHA-256 `5aa9aed23a9764e4a9fb0d56fd5efc47368711933adbfaa224f2f725a766ed00` | reviewed byte-identical fixture; no mounted-App claim |
| App capture donor | App `7f7e2daffad39a6d9aa3917a9fc526ba91caf2e6` | exact old capture test bodies read read-only |
| App qualified frozen ref | `8f0c2484463e9b666d184a744d52e252984e551a` | current qualified App source; dormant capture files are absent there |
| Runtime pin used by retained witness runs | `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d` | used as PYTHONPATH authority in retained runs; no live Runtime claim |

The retained App handoff is `peer-app-to-agent-20261023T1823-A4-scoped-PASS-and-raw-map.md`; the corrected mounted-boundary source is `agent-A4-provider-map-mount-return-1758.md`; the integrated witness reports are `agent-A4-track-integrated-1813.md` and `agent-A4-transcript-integrated-1823.md`.

## Current registry and request/reply boundary

`astrid/sdk/timeline/commands.py:67-103` registers `doc.patch` and
`clip.add-media`; it has no `track.reorder` or `transcript.associate` entry.
The current generic provider therefore accepts the track/transcript-shaped
cases only as `doc.patch` changes, never as invented operation names.

The C0 request shape remains unchanged: `api_version`, project/timeline IDs,
exact base revision/publication pair, commands, label, steps with per-step
patch and reads, merge mode, declared reads, idempotency key, `dry_run`, source,
rationale, and group ID. The reply shape remains unchanged: accepted/merged
canonical document and full receipt, records, bindings, effects, dependencies,
history, undo steps; preview `would_status` with null receipt; and structured
errors with code, path, head, hint, and suggested command. Existing code and
contract evidence remain the authority for the full shape. The A4 witnesses
assert only the fields relevant to their bounded cases and do not upgrade
partial C0 assertions into whole-contract proof.

The Agent boundary is `commit.py:1167-1188`, `_commit_preview.py:7-22,83-105`,
and `_commit_errors.py:74-110`. The parent-media boundary is
`native_parent_media_commands.py:25-52,87-94`; exact transcript source input is
`native_source_inputs.py:82-106`.

## Exact old App case → current Python-provider map

Status terms:

- **Covered, generic** means an executed current Agent provider witness exists,
  but only for the registered generic operation and its exact fixture/input.
- **Covered, registered** means the current `clip.add-media` provider and its
  existing fixture/tests exercise the property.
- **Raw boundary only** means the current provider/source-input guard is proven,
  while the old capture operation or full old case is not.
- **UNCOVERED** means no exact current Python-provider acceptance/refusal
  witness was found. A similarly named App/editor test is not substituted.
- **Retained run** means the cited command/result is reused from the prior
  report at an identical blob; it is not a new run in this continuation.

### A. `parentAfterAnchorCapture.test.ts`

Old source: App donor `7f7e2da...`,
`src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts`.
Fixture/input: `media` is `reserved-new` with object pin
`sha256:` + 64 `2`s and catalog pin `sha256:` + 64 `b`s; verified media is
`video/fixture`, size 123, duration 10; parent has `before`, `anchor`, `later`,
and `other` rows, 24/1 FPS, and opaque values (old lines 14-50).

| exact old case | current Python test / full fixture input | current request and guard | outcome / evidence head |
|---|---|---|---|
| Positive raw clone, rate-aware ripple, opaque preservation, complete reads/selections/bindings/created/writes: old `it('matches Agent raw clone...')`, lines 58-173 | `tests/editing_conformance/test_recipe_m2_parent_media.py::test_exact_capture_replay_scoped_birth_and_inverse(kind)` and `::test_portable_golden`; `fixtures/recipe_m2_parent_media.json`; `parent_inputs(kind)` adds free parent `overlay` lane with `ov-a`/`ov-b`; `args()` sends complete row/media | `capture_clip_add_media` → registered `clip.add-media`, `select=parent`; `add_media` verifies media, parent FPS, absent `source_window`, occurrence-owned lanes, registry/clip collections, and birth claims; output is parent-owned `reserved-new`/`born` | **Covered, registered but not all-green.** Retained parent-media command: `71 passed, 14 failed in 26.64s`; the 14 existing reload/inverse failures remain unmodified. Exact per-case pass was not separately reported; do not call whole suite PASS. Head `78738040...`; source map `mount-return-1758`. |
| JSON reload, selected tuple/IDs, wrong ownership/identity, missing anchor, duplicate source rows, catalog mismatch: old `it('keeps the selected tuple...')`, lines 176-196 | `test_existing_binding_is_required_exactly_without_birth`; `test_refusals_preserve_input(damage)` for `missing-input`, `wrong-object`, `wrong-catalog`, `occurrence`, `membership`, `occupied-id`; same parent-media fixture and verified list | `clip.add-media` plain command/selection and `_verified` media pin; `ctx.create`/registry and collection membership guards; malformed/occupied identity refuses before mutation | **Partial covered registered.** Exact wrong-object/catalog and atomic no-write are in the retained refusal matrix; duplicate source-clip-identity is **UNCOVERED** (see below). Existing run is retained, not a new body rerun. |
| Incoming source transition survives capture/replay: old `it('preserves an incoming source transition...')`, lines 197-207 | No exact named current test for the after-anchor transition row. Closest retained provider cases are `test_exact_capture_replay_scoped_birth_and_inverse`, `test_provider_exact_reload_inverse_redo_and_retired_ids`, and replacement/replay tests, all on `recipe_m2_parent_media.json` | Existing `clip.add-media` receives complete authored row and exact media; provider preserves opaque row fields it accepts, but no current after-anchor operation exists | **UNCOVERED exact old after-anchor transition case.** Generic/registered parent-media resemblance is not inflated to parity. |
| Missing/null source hold is preserved for raw video: old parametrized `it.each(['missing','null'])`, lines 209-231 | No exact current Python test for missing `hold` or explicit `hold=None` on the source row. Current `test_refusals_preserve_input('zero-hold')` covers only explicit zero; `test_literal_completion...` uses positive holds | Current provider birth row is complete and `_clip` requires a finite positive hold; no retained test proves old missing/null source normalization/preservation | **UNCOVERED**: missing/null hold raw-provider behavior. |
| Missing/null hold on non-video refuses atomically: old parametrized case, lines 233-246 | No exact current Python case combining non-video source, missing/null hold, and provider refusal | Existing generic/parent media refusal matrix has media-kind and zero-hold cases, but not this exact raw input | **UNCOVERED**. |
| Missing/null ordinary parent birth remains strict: old parametrized case, lines 248-259 | No exact current Python case for ordinary `clip.add-media` with omitted/null hold. `test_refusals_preserve_input('zero-hold')` is not equivalent | `clip.add-media` validation is present; exact missing/null input is not in the retained fixture/test body | **UNCOVERED**. |
| Explicit null effect survives; explicit null `track`/`asset` refuses: old case, lines 261-274 | `test_refusals_preserve_input('no-track')` and `test_explicit_malformed_asset_containers_refuse_untouched` cover missing/invalid track and malformed registry containers; no row-level explicit-null track/asset case | `add_media`/state collection and media/registry guards reject invalid lane/asset shape; generic `doc.patch` null test is not a parent-media row witness | **Partial only; exact null track/asset override is UNCOVERED.** Explicit null effect preservation is also not separately asserted in current parent-media provider tests. |
| Positive sub-0.05 hold floors, zero hold refuses: old case, lines 276-295 | `test_refusals_preserve_input('zero-hold')` and timing cases in `test_completion_builder_places_a_parent_clip_after_the_anchor_or_at_the_track_end`; fixture uses ordinary positive holds | `clip.add-media` / completion provider validates positive hold; no exact `.01` raw source case and no old after-anchor duration helper | **Zero refusal covered boundedly; positive subminimum normalization is UNCOVERED.** Do not claim old floor parity. |
| Source `at_ms` must refuse rather than normalize/drop: old case, lines 297-306 | No exact retained current Python test mutating source `at_ms=1003` on an after-anchor source row. Completion tests preserve source units but do not assert this refusal | `clip.add-media` accepts complete row input; current source map has no exact `at_ms` raw rejection witness | **UNCOVERED exact raw-vs-normalized `at_ms` behavior.** |
| Exact media/object and catalog pins | `test_refusals_preserve_input('wrong-object')`, `('wrong-catalog')`, `test_exact_capture_replay_scoped_birth_and_inverse`, `test_existing_binding_is_required_exactly_without_birth`; `parent_inputs`/`args` create verified media and registry pin | `_verified(ctx,pin)` plus registry alias/object/catalog checks; `add_media` binds exact media before create | **Covered, registered** for current `clip.add-media` provider input. This is not a claim about the old after-anchor envelope. |
| Duplicate source clip identity | No exact current test found for duplicate `anchor`/source clip identity in both authored mirrors. Existing `test_refusals_preserve_input('membership')` is a collection/selection mismatch, not duplicate identity | `State` collection guards detect some duplicate collection identity, but no exact retained parent-media witness maps this source duplication | **UNCOVERED.** Smallest next witness is a test-only duplicate source row in both parent clip mirrors, before any inverse-dependent work. |

The current registered parent-media guard source is concrete: verify media and
kind, read output FPS, reject non-null parent `source_window`, reject
occurrence-owned lane conflicts, bind media owner, validate/create registry
asset and parent clip, then observe supported submitted placement reads. The
old after-anchor helper's `at`/`at_ms` normalization and ripple envelope are
not this provider guard.

### B. `trackReorderCapture.test.ts`

Old source: App donor `7f7e2da...`,
`src/tools/video-editor/commands/trackReorderCapture.test.ts`.
Fixture: `recipe_m2_app_track_label.json`; rows are `picture`, `audio` with
explicit null/false/zero opaque values, and `overlay` with opaque array data;
App config carries `timelineDataLanePlacement` and parent opaque data (old
lines 10-23).

| exact old case | current Python test / full fixture input | current request and guard | outcome / evidence head |
|---|---|---|---|
| Raw rows/opaque siblings/order/immutability/JSON replay: old `it('matches the Agent source shape...')`, lines 27-61 | `tests/editing_conformance/test_a4_track_doc_patch_witness.py::test_detached_track_doc_patch_preserves_rows_and_json_replays_without_source_write`; `track_document()` loads the App fixture, adds `audio`/`overlay`, preserves parent/config opaque values | `doc.patch` with `list.move`, `ref=parent`, `path=['config','tracks']`, `id=overlay`, exact `before` row, `order_before`, `after_id`; generic collection read has members/order | **Covered, generic.** The integrated nine-case witness passed `9 passed in 2.43s`; evidence head `1962a...` retained by `787...`. It is not `track.reorder`. |
| Same-order explicit write and op record: old `it('round-trips... keeps same-order writes explicit')`, lines 63-73 | No exact current A4 Python witness. Generic list tests (`test_ordered_insert_move_remove_and_created_claim`, `test_list_guards_and_anchors`) are not proof of this App case; the A4 witness's `move_overlay` changes order | A current generic `doc.patch` no-op/explicit `list.move` request and record would be needed; no current test maps the old `track_order` write to an op record | **UNCOVERED**, specifically as requested. Do not infer from a generic no-op or from the absent `track.reorder` registry entry. |
| Missing/duplicate/foreign/malformed desired identity refusal: old parametrized case, lines 75-85 | `test_detached_track_doc_patch_refuses_duplicate_identity_before_mutation`; public witness also has bad previous/order/anchor and forged-created cases | Generic `doc.patch` list identity/previous/order/anchor validation; no `track.reorder` desired-order envelope | **Covered generic for duplicate collection identity and generic refusal; track-specific desired identity is UNCOVERED.** |
| Lane-bearing input and invalid current collection refusal: old case, lines 87-100 | No exact current Python lane-bearing or malformed track projection case. Generic `doc.patch` operand/collection cases are not equivalent | No current `track.reorder` parser/provider; generic provider only sees the `doc.patch` change shape | **UNCOVERED exact track capture refusal.** |
| Stale captured identity/order before row write: old case, lines 102-115 | `test_public_track_doc_patch_refuses_bad_previous_order_or_anchor_without_write` (three parametrized cases), `test_public_track_doc_patch_rejects_membership_change_and_forged_created_claim`, `test_public_track_doc_patch_detects_order_aba_even_when_final_order_returns_to_base` | Generic list move checks exact previous row, `order_before`, `after_id`, collection membership and order ABA; no track-specific capture basis | **Covered, generic** for the provider guard properties and no-write outcome; old track envelope remains uncovered. |
| Current mounted track persistence shape | `test_public_provider_accepts_current_doc_patch_and_persists_c0_step_and_read_records`, same `track_document` and `list.move` input | C0 controls: label `Move tracks`, `merge=fields`, request/step reads, preview then accepted; record stores patch/read and empty created | **Covered, generic detached provider boundary.** The source caller is A2 `localSaveSession`, not dormant `createTimelineCommandSession`. |
| Membership/order conflict versus disjoint sibling field merge | `test_public_track_doc_patch_rejects_membership_change...`, `test_public_track_doc_patch_detects_order_aba...`, `test_public_track_doc_patch_merges_disjoint_neighbor_field_change` | `track_read` records sorted members and exact order; generic provider returns invalid `selection_changed` for stale structural reads and `rebased` for disjoint field edit | **Covered, generic.** `rebased` is the current detached spelling; it is not relabelled as the C0 `merged` reply. |

The track witness proves only the current generic provider boundary. It does
not prove App hook execution, outbox/restart/lost-ack behavior, HTTP, or
Runtime. Existing App track implementation and tests remain retained.

### C. `transcriptAssociateCapture.test.ts`

Old source: App donor `7f7e2da...`,
`src/tools/video-editor/commands/transcriptAssociateCapture.test.ts`.
Old fixture input uses `asset-a`, source `source-1`, media digest
`sha256:` + 64 `a`s, legacy/canonical segment IDs, nested
`transcriptReferences`/`itemsBySchemaRef`, a caption, and a review extension
(old lines 14-158).

| exact old case | current Python test / full fixture input | current request and guard | outcome / evidence head |
|---|---|---|---|
| Nested source planes, opaque preservation, no-asset caption/review reconciliation: old `it('matches the Agent record...')`, lines 161-223 | `tests/editing_conformance/test_a4_transcript_doc_patch_witness.py::test_nested_transcript_planes_preserve_app_shape_and_exact_source_pin`; `transcript_document_fixture()` uses existing private `source_fixture('transcript')`, puts App-shaped bundle under `parent.config.bundle`, and records the exact source pin in `dependency_manifest` | Generic `doc.patch` set changes nested `transcriptReferences` and item payload; provider request is generic, with exact source pin retained as a dependency input. No association command | **Covered, generic for nested raw JSON and exact source-input use. Old reconciliation/caption/review semantics are UNCOVERED.** Integrated witness head `14fc...`/current `787...`; retained pinned run `7 passed in 1.80s`. |
| Exact capture pin and source identity: old source helper and primary case, lines 35-53, 175-190 | `test_exact_source_and_prior_pin_bytes_are_provider_inputs_not_nested_metadata_authority` and `test_nested_transcript_planes_preserve_app_shape_and_exact_source_pin`; `source_fixture('transcript')` gives exact `document_id`, version, digest, project and `media.transcript/v1` content | Existing `read_verified_transcript`/source hydration validates exact pin, document scope/version, canonical digest, and transcript shape. Generic patch does not derive authority from opaque nested metadata | **Raw boundary covered; exact old `transcript.associate` capture-pin case remains UNCOVERED.** Do not claim App fixture identity parity. |
| Prior-pin replacement and source order: old `it('retains the exact prior pin...')`, lines 225-252 | Current source-input tests `test_retained_input_closure_survives_document_overwrite_and_new_provider(kind)` and malformed-source matrix; A4 witness has prior-pin bytes but no association replacement | Existing retained-input closure keeps exact source documents/pins across overwrite/provider/inverse; no nested association projection or prior-document command | **Raw source retention covered; exact association replacement/order is UNCOVERED.** |
| New pin differs from supplied source: old atomic refusal, lines 254-267 | `test_malformed_exact_source_refuses_before_nested_patch_and_no_open_metadata_integrity_is_claimed`; source-input matrix `test_missing_or_malformed_transcript_source_is_refused(damage)` for missing/version/digest/project/source identity/kind/pin | Exact source pin mismatch/malformed source is rejected before generic nested patch; document and accepted count remain unchanged | **Raw boundary covered; old association-shaped refusal record is UNCOVERED.** |
| Populated config clip mirror when primary parent collection is empty: old case, lines 269-368 | No current exact Python witness. A4 generic witness patches `parent.config.bundle`; it does not model `config.clips`/primary `parent.clips` mirror selection | No current transcript association provider; generic patch has no mirror/reconciliation semantics | **UNCOVERED.** |
| Caption destination collision and shared review ownership: old parametrized refusal, lines 370-382 | Generic A4 `test_previous_value_mismatch_and_collision_refuse_atomically_with_structured_details` covers generic identity collision; it does not use caption fingerprint/review ownership rows | Generic previous-value/identity guards are provider-enforced; no transcript-specific collision/reconciliation guard exists | **UNCOVERED exact refusal-record and atomic collision/shared-row cases.** |
| Malformed pinned source before either nested plane changes: old case, lines 384-396 | `test_malformed_exact_source_refuses_before_nested_patch_and_no_open_metadata_integrity_is_claimed`; `test_missing_or_malformed_transcript_source_is_refused` matrix | Existing exact pin/content/schema/source validation rejects before generic nested writes; no metadata referential-integrity inference | **Raw boundary covered; exact old nested-plane case remains UNCOVERED.** |
| Config mirror/shared rows and caption/review ownership | No current Python provider test maps the old `config.clips` fallback, shared source item ownership, caption identity, or review movement | No `transcript.associate` registration/handler/schema/provider fixture | **UNCOVERED.** |

Current A4 transcript witness test IDs and what they actually prove:

- `test_nested_transcript_planes_preserve_app_shape_and_exact_source_pin`:
  generic nested preservation and exact pin as an input;
- `test_explicit_null_and_absence_are_distinct_in_nested_bundle`: generic
  absent versus explicit-null semantics;
- `test_exact_source_and_prior_pin_bytes_are_provider_inputs_not_nested_metadata_authority`:
  exact current/prior source bytes and dependency retention;
- `test_declared_nested_read_and_full_c0_metadata_survive_accepted_preview_and_receipt`:
  relevant request/preview/accepted metadata, not complete C0 proof;
- `test_previous_value_mismatch_and_collision_refuse_atomically_with_structured_details`:
  generic structured refusal and no-write collision;
- `test_intervening_unrelated_edit_merges_but_atomic_scope_refuses`: generic
  fields rebase versus atomic-scope refusal;
- `test_malformed_exact_source_refuses_before_nested_patch_and_no_open_metadata_integrity_is_claimed`:
  exact source refusal before nested generic patch.

## Explicit uncovered-case ledger

These are the requested cases for which this map does **not** claim an exact
current Python-provider acceptance/refusal witness:

| requested uncovered case | nearest evidence (not equivalent) | exact gap |
|---|---|---|
| duplicate source clip identity | generic track duplicate collection identity and parent selection/membership refusals | no duplicate source clip in old after-anchor parent mirrors mapped to current provider |
| `at_ms` raw versus normalized | current completion/source-unit tests; old App raw refusal | no current raw-provider `at_ms` input case with explicit refusal/normalization outcome |
| source zero / positive subminimum | current explicit zero-hold refusal | no positive subminimum floor and no old after-anchor duration helper witness |
| exact media/catalog pin | **Covered for registered `clip.add-media`** by wrong-object/wrong-catalog refusal and verified media fixture; old after-anchor envelope remains unproven | preserve this distinction; do not mark the registered provider input guard uncovered, and do not inflate it into old capture parity |
| missing/null hold, non-video and ordinary parent birth | current zero-hold/media-kind/refusal matrix | no exact omitted/null hold source cases for either raw non-video or ordinary parent birth |
| null track / null asset override | current no-track and malformed registry-container cases | no explicit null row override case; explicit-null effect also not independently mapped |
| track same-order explicit write/op record | generic list semantics and current move witness | no exact same-order explicit write in the A4 current witness; no `track.reorder` record |
| transcript exact capture pin | current exact source pin and retention boundary | no old `transcript.associate` capture envelope or App fixture identity parity |
| transcript config mirror | none exact | no primary-empty/config-clips fallback or mirror write witness |
| transcript malformed pinned content | **Raw boundary covered** by exact source refusal before generic nested write | no old transcript association-shaped record/reconciliation case |
| transcript refusal record | generic structured previous-value/collision refusal | no transcript-specific collision/refusal record with old nested fields |
| transcript atomic collision | generic identity collision is atomic | no caption fingerprint/review ownership collision |
| transcript shared rows | none exact | no shared source-item/review ownership or caption mirror case |

No “metadata referential integrity,” invented operation/API, `transcript.associate`,
or `removed_after_capture_row` row is inferred. No arithmetic PASS or whole-A4
parity claim is made.

## Smallest test-only next witnesses

These are recommendations for manager coordination only; this worker authored
no product or test code.

1. **Parent raw guards (no inverse dependency):** one test-only extension of
   the existing parent-media fixture can cover duplicate source clip identity,
   omitted/null hold for video/non-video and ordinary birth, explicit null
   track/asset, source `at_ms`, zero, and positive subminimum. Keep the current
   `clip.add-media` operation and provider; assert input immutability and exact
   refusal/accepted row. Do not rerun the retained 14-failure body as a gate.
2. **Parent reload/inverse rows:** only after current inverse source `1833` and
   `_root` source `1831` are independently qualified should the existing
   retained reload/inverse cases be revisited. This map does not relabel their
   current 14 failures.
3. **Track same-order:** if App A2 confirms the mounted persisted intent is an
   explicit generic `doc.patch` write, add one generic `list.move`/ordered-field
   witness asserting an explicit write and record. It must be labelled
   `doc.patch`, not `track.reorder`, and must not infer operation-specific
   authorship claims.
4. **Transcript source boundary:** retain the existing exact-pin/malformed
   source tests as the smallest raw-provider witness. A config-mirror or
   caption/review collision witness is not honest without an approved existing
   provider/API semantics; manager must coordinate that dependency with the
   App owner before any test-only authoring. Do not manufacture a generic test
   that claims reconciliation.

Dependencies are the existing Agent provider/fixtures and, for reload/inverse,
the pending current inverse qualification. App owns App files and old tests;
the manager coordinates any test-only continuation to avoid competing core
authors. No new approval gate or scope escalation is proposed.

## Retained command evidence

The following are reused only because the cited witness blobs are identical to
the integrated/current source:

```text
# Track witness, direct integrated run
timeout 300s env PYTHONDONTWRITEBYTECODE=1 \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f \
  PYTHONPATH=.:/home/user/work/wt/rt-pin-2a9e347f \
  /home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= \
  -pno:cacheprovider --timeout=15 \
  tests/editing_conformance/test_a4_track_doc_patch_witness.py
=> 9 passed in 2.43s

# Transcript witness, direct integrated run
timeout 15s env PYTHONDONTWRITEBYTECODE=1 \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f \
  PYTHONPATH=.:/home/user/work/wt/rt-pin-2a9e347f \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= \
  -p no:cacheprovider tests/editing_conformance/test_a4_transcript_doc_patch_witness.py
=> 7 passed in 1.80s

# Existing generic/parent evidence retained from prior map; not rerun here
PYTHONPATH=/home/user/work/wt/agt-A4-provider-map-1732:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q \
  tests/editing_conformance/test_doc_patch_v2.py
=> 102 passed in 11.81s

PYTHONPATH=/home/user/work/wt/agt-A4-provider-map-1732:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q \
  tests/editing_conformance/test_recipe_m2_parent_media.py --maxfail=20
=> 71 passed, 14 failed in 26.64s

PYTHONPATH=/home/user/work/wt/agt-A4-provider-map-1732:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q \
  tests/sdk/test_timeline_commit_provider.py -k \
  'retained_input_closure_survives_document_overwrite_and_new_provider or missing_or_malformed_transcript_source_is_refused'
=> 9 passed, 105 deselected in 2.17s
```

The 14 parent-media failures are retained known failures: six missing-registry
container reload guard cases and eight exact/ordered provider reload/inverse
cases with nested inverse ranges. No old known-failed body was rerun in this
continuation. No original-14, SDK-four, c271, nine-body, full, browser, HTTP,
P1/P4, native, farm, daemon, benchmark, schema, pin, Git, or environment run
was performed.

## Safety and unchanged decisions

- Frozen references `34e`, `d106`, and `819acf` remain unchanged.
- No source, schema, client, operation, API, metadata-integrity rule, guard,
  pin, test weakening, skip, xfail, deletion, environment, daemon, merge,
  benchmark, or App file changed.
- No new approval gate or scope escalation is proposed.
- The old App behavior/tests remain KEEP and the original A4/P1 gate remains.
- The current inverse source 1833 / `_root` 1831 work is pending and is not
  silently treated as evidence here.

## Source citations

- Plan: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/PLAN.md`.
- Latest App handoff: `peer-app-to-agent-20261023T1823-A4-scoped-PASS-and-raw-map.md`.
- Corrected mounted map: `agent-A4-provider-map-mount-return-1758.md`.
- Track witness/review/integration: `agent-A4-track-witness-1758.md`,
  `agent-A4-track-review-1805.md`, `agent-A4-track-integrated-1813.md`.
- Transcript witness/review/integration: `agent-A4-transcript-witness-1758.md`,
  `agent-A4-transcript-eof-review-1815.md`,
  `agent-A4-transcript-integrated-1823.md`.
- Current Agent files: `tests/editing_conformance/test_a4_track_doc_patch_witness.py`,
  `tests/editing_conformance/test_a4_transcript_doc_patch_witness.py`,
  `tests/editing_conformance/test_recipe_m2_parent_media.py`,
  `tests/editing_conformance/test_doc_patch_v2.py`,
  `tests/sdk/test_timeline_commit_provider.py`,
  `astrid/sdk/timeline/commands.py`,
  `astrid/sdk/timeline/native_parent_media_commands.py`,
  `astrid/sdk/timeline/native_source_inputs.py`.
- Frozen App donor: `git show 7f7e2daffad39a6d9aa3917a9fc526ba91caf2e6:<old capture file>`.

