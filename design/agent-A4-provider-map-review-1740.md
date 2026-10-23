# A4 provider-coverage map — independent read-only review

Date: 2026-10-23  
Verdict: **FAIL for complete A4 coverage-map parity; PASS only for the bounded registered-path findings below.**  
Scope: Agent provider coverage for the three App capture modules, their current production mounts, C0 request/reply boundaries, and the retained targeted evidence. This is a coverage-map verdict, not a behavior-suite PASS.

## Source identity and limits

The source under review is fixed and was read without checkout or mutation:

| source | exact identity | role |
|---|---|---|
| Agent | commit `6531622c8f198c3efb509217e303fcad0126c47b`, tree `7c624ddd8ac897923ad85cf4520c905d64eb68a1` | provider source and Python witnesses |
| App | commit `4c4c9c77c96fab70c4efef09db9a3bc456b0d803`, tree `2652d85a0ab40bcf0e88443f721dc4b868eeb743` | exact App capture sources/tests and production caller source |
| Runtime authority used by retained Agent run | `/home/user/work/runtime`, commit `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`, tree `f79a2355cfb39d9ada7721978bd20d5702105778` | runtime source path named by the author run |

The retained Python run names `/home/user/work/runtime` on `PYTHONPATH`, but it did not record module origin for every case. Runtime authority is therefore reported as the used source path, not as per-test import provenance. Agent provider tests are detached realm/port tests, not live App, HTTP, browser, renderer, or daemon tests. No browser, HTTP, full, native-14, original-SDK-4, Runtime-20, renderer, benchmark, or build evidence was collected for this review.

Relevant exact blobs:

```text
Agent astrid/sdk/timeline/commands.py                         d349ebd4afc1764fa5db2f464ff234ce6c146b89
Agent astrid/sdk/timeline/native_parent_media_commands.py      433f94a1b3a4f1a5f9bd2aa5c4fa5d344231a557
Agent astrid/sdk/timeline/commit.py                            3f4a86567d053b4a5fa9ec3b44f35ef58e25ef23
Agent astrid/sdk/timeline/_commit_preview.py                   514ecfb5219b5d1e90b154936efae9544f82eee2
Agent astrid/sdk/timeline/_commit_errors.py                    084df70928383e915175456dc57775ad9750203a
App src/tools/video-editor/commands/commitSession.ts           830ec790a2a0cba98847061980852bd251af73d1
App src/tools/video-editor/hooks/useTimelineCommandsService.ts 3304899ec1d0301a67c587bc252f3de96b287f7f
App src/tools/video-editor/commands/documentPatchIntent.ts     5e1b1d1e2cd95ac7e402daf0ac9f4f4cf1ec606f
App src/tools/video-editor/commands/localSaveSession.ts        83d2166d57c05980d3bd8ebc9bbd79a37c3c5e44
App parentAfterAnchorCapture.test.ts                           346ae62eac5936e946266924f5e79e27df8dab54
App trackReorderCapture.test.ts                                61d123e0b63d3f3321afaa1218eda9ecef7e3292
App transcriptAssociateCapture.test.ts                         5c39a293009df59f796fe476e107a0a9900244d7
```

## Registered providers and actual production mounts

The Agent registry at `astrid/sdk/timeline/commands.py:29-103` registers `doc.patch` at `:67` and `clip.add-media` at `:102`. There is no `track.reorder` or `transcript.associate` entry in this registry, and no corresponding Agent schema, handler, provider fixture, or Python test witness was found at the exact Agent source.

The exact App production boundaries are different from the dormant capture modules:

| mounted App path | actual source evidence | provider reached | coverage classification |
|---|---|---|---|
| Parent media port | `src/tools/video-editor/commands/commitSession.ts:444-519`; `finish` calls `captureParentClipAddMedia` at `:487`, and `submit` requires `command.op === 'clip.add-media'` at `:508-517` | registered `clip.add-media`; Agent capture builder `native_parent_media_commands.py:87-94`, handler `:25-52` | **Mounted and registered** |
| Generic A2 local document save | `localSaveSession.ts:152-179` turns persisted `documentIntent` into `doc.patch`; `documentPatchIntent.ts:109-223` emits id-addressed changes and `created` claims; `timelineLocalSaveHandoff.ts:305-311` appends the intent | registered `doc.patch` through the normal provider commit path | **Mounted source path, with the exact full-v2 gate in `localSaveSession.ts:153-156`** |
| Add clip after an anchor | `useTimelineCommandsService.ts:520-548` uses local `buildDuplicateClipEdit` and `applyValidatedMutation`; the dormant `parentAfterAnchorCapture.ts:148-179` is not imported by the production hook at this commit | eventual generic local-save path if the mounted persistence handoff is active; no after-anchor-specific Agent op | **Mounted behavior is local-row/config based; dormant capture parity is unproven** |
| Track move | `useTimelineCommandsService.ts:918-963` computes `nextTracks` and applies a local `config` mutation | eventual generic local-save path if mounted; no `track.reorder` provider | **Mounted behavior is not the dormant capture operation** |
| Transcript association | `transcriptAssociateCapture.ts:517-573` defines capture/finish/execute, but the frozen App source has no production import/caller for it | none found | **Dormant/unmounted at this snapshot** |

The C0 request type at App `src/integrations/runtime/timeline-commit-types.ts:67-112` retains `api_version`, project/timeline IDs, the base revision/publication pair, commands, label, steps with per-step patch/read fields, merge mode, declared reads, dry-run, source, rationale, group ID, and the accepted/preview/failure response types. The mounted parent-media builder at `commitSession.ts:204-223` supplies the base pair, commands, label, step patch, merge, reads, `dry_run: false`, and `source: { via: 'app' }`; its idempotency key is the outbox/request key passed to `send`, not a body field, and this path does not populate optional `rationale` or `group_id`. The generic `localSaveSession.ts:162-179` carries persisted step/patch, merge, optional reads, label, source, and the same request key. The report does not alter or reinterpret these C0 fields.

On the Agent side, `commit.py:1167-1188` prepares the expected head, canonical document, digest, full records, bindings/effects/dependencies, semantic events, provider/compiler versions, and delegates preview/acceptance to the Runtime port. `_commit_preview.py:7-22,83-105` retains commands, steps, merge mode, label, undo steps, evaluated/base heads, and `would_status` with a null receipt for preview. `_commit_errors.py:74-110` preserves structured `status`, `reason`, `code`, `path`, `base/current` heads, conflicts, hint, and suggested command. These are boundary facts, not evidence that all three dormant App operations execute through the boundary.

## Complete three-module case map

### 1. `parentAfterAnchorCapture.test.ts` — parent after-anchor / media birth

App source/test citations are from the exact App commit:

| App case and assertions | registered Agent witness | exact coverage | boundary / uncovered claim |
|---|---|---|---|
| Positive raw clone, rate-aware ripple, opaque values, complete claims, selected anchor, created row/media: `parentAfterAnchorCapture.test.ts:59-173` | `clip.add-media`; `test_recipe_m2_parent_media.py:test_exact_capture_replay_scoped_birth_and_inverse` (`:123`), `test_portable_golden` (`:148`); fixture `fixtures/recipe_m2_parent_media.json:45-74` | **Raw/canonical:** complete row/media birth and replay. **Reads/created/previous:** provider records submitted reads and created binding; generic patch tests cover previous values/created IDs. **Opaque/null/absent:** parent-media refusal and literal preservation are exercised by the recipe/refusal matrix. **Order/ripple:** `test_completion_builder_places_a_parent_clip_after_the_anchor_or_at_the_track_end` (`:484`) and replacement/order tests (`:330-401,468-566`). | This is the strongest registered mapping, but it is not proof that the dormant App capture basis and its exact claims are accepted by a distinct provider operation. The selected parent-media suite has retained failures below. |
| JSON reload, selected tuple/ID preservation, wrong ownership/identity, missing anchor, catalog digest refusal: `:176-195` | `test_existing_binding_is_required_exactly_without_birth` (`:156`), `test_refusals_preserve_input` (`:239`), malformed/container refusal tests (`:172-222`) | **Refusal atomicity:** no partial birth on invalid ownership, identity, registry, or source. **Membership/order:** parent collection and registry guards are checked. | App-specific capture claims are not independently mapped to the registered provider record. |
| Incoming source transition and replay: `:197-247` | `test_exact_capture_replay_scoped_birth_and_inverse` (`:123`), `test_provider_exact_reload_inverse_redo_and_retired_ids` (`:468`), `test_ordered_provider_reload_inverse_redo_and_retired_ids` (`:510`) | **Source/media selection and inverse:** covered at provider boundary, with reload/redo assertions. | The eight nested-inverse failures mean this existing evidence is not an all-green behavior claim. |
| Explicit null effect preserved; null track/asset rejected: `:261-275` | `test_explicit_malformed_asset_containers_refuse_untouched` (`:222`), `test_refusals_preserve_input` (`:239`); generic `test_tagged_null_explicit_clear...` (`test_doc_patch_v2.py:69`) | **Null vs absence and refusal:** bounded evidence exists for generic patch semantics and parent-media input refusal. | No claim that every App null/absence branch has a provider-equivalent fixture. |
| Positive sub-0.05 duration floor and zero-hold refusal: `:276-295` | parent-media `test_refusals_preserve_input` (`:239`), completion/provider timing cases (`:484-555`) | **Timing boundary:** bounded provider evidence. | No distinct after-anchor operation witness. |
| Source `at_ms` refusal rather than stripping: `:297-309` | parent-media refusal matrix (`:239`) and native media input verification in `native_parent_media_commands.py:25-38` | **Refusal before mutation:** covered at provider input boundary. | The exact App raw-capture assertion remains an App-only claim. |

Registered implementation details: `native_parent_media_commands.py:25-52` reads parent output/fps, source-window state, occurrence placement, registry and selection/binding state; refuses unsupported source windows and occurrence-owned lanes; creates/binds the media and clip at `:31-40`; and checks submitted placement reads at `:41-52`. The capture helper at `:87-94` emits `schema_version: 1`, `op: clip.add-media`, version `1`, a parent/clip selector, and `{row, media}`.

**Parent conclusion:** `clip.add-media` is registered and has substantial Python coverage for raw birth, timing, ripple/order, null/absent/opaque input, reads, created IDs, prior values, and refusals. The dormant App after-anchor capture test is not a production-mounted provider witness. The existing 14 failures prevent an all-green claim.

### 2. `trackReorderCapture.test.ts` — track order

| App case and assertions | registered Agent witness | exact coverage | boundary / uncovered claim |
|---|---|---|---|
| Raw rows, opaque lane values, lane siblings, exact command/read/selection/expect/authorship claims, permutation and input immutability: `trackReorderCapture.test.ts:28-60` | No `track.reorder` provider. Generic `test_doc_patch_v2.py:test_ordered_read_detects_shape_aba_and_membership_read_ignores_reorder` (`:425-436`), `test_list_move_merges_unread_sibling_item_field` (`:439-448`), and list move conflict tests (`:451-496`) | **Generic only:** ordered list membership/order guards, list moves, previous values, and merge precedence. | Not an authoritative witness for the App `track.reorder` envelope, `parent/collection:track` selection, track-specific rows, or its claims. |
| Explicit same-order write: `:63-72` | Generic list-move/previous-value semantics in `test_doc_patch_v2.py:112-144,425-496` | **Generic no-op/order boundary:** partially analogous. | No `track.reorder` registration or exact same-order capture witness. |
| Lane-bearing input, malformed/foreign/duplicate/stale collection refusals without mutation: `:75-114` | `test_bad_operands_refuse_atomically` (`test_doc_patch_v2.py:95`), `test_list_guards_and_anchors` (`:130`), ordered read/conflict tests (`:425-496`) | **Generic refusal and membership/order:** covered for `doc.patch`. | Track-specific refusal reasons, selection, authorship, raw opaque lane shape, and operation claims remain uncovered. |

The App capture module itself declares `COLLECTION_REF = 'parent/collection:track'` and `ORDER_ADDRESS = 'parent::track_order'` at `trackReorderCapture.ts:14-16`, with capture at `:138-173`. The mounted hook instead mutates `resolvedConfig.tracks` through a local `config` mutation at `useTimelineCommandsService.ts:918-963`. That current path may be serialized by generic A2 document diffing, but the exact operation-specific promises must be preserved by the App owner and verified against the actual mount; they cannot be inferred from the absence of a Python operation.

**Track conclusion:** generic list/order `doc.patch` semantics are registered and witnessed; `track.reorder` is not registered or witnessed. This is an uncovered operation seam, not permission to drop the existing App implementation or tests.

### 3. `transcriptAssociateCapture.test.ts` — transcript association

| App case and assertions | registered Agent witness | exact coverage | boundary / uncovered claim |
|---|---|---|---|
| Nested source planes, opaque data, no-asset caption/review reconciliation: `transcriptAssociateCapture.test.ts:162-222` | `test_timeline_commit_provider.py:test_retained_input_closure_survives_document_overwrite_and_new_provider` (`:620-651`); native source-input and word-anchor tests (`test_native_word_anchor.py:115-711`) | **Source pin/retention:** exact verified inputs, retained closure, overwrite and inverse boundaries. | Does not cover nested `transcriptReferences`, `itemsBySchemaRef`, canonical segment projection, caption mirror, or review extension reconciliation. |
| Prior-pin replacement and source order: `:225-252` | `test_missing_or_malformed_transcript_source_is_refused` (`test_timeline_commit_provider.py:654-683`); exact source/word binding tests | **Source identity/refusal:** verified pin, project/document/version/digest/source identity, and atomic malformed-source refusal. | No prior-pin association command or nested reconciliation witness. |
| New pin differs from supplied source: atomic refusal `:254-267` | same missing/malformed source test (`:654-683`), `test_provider_resolves_exact_first_use_pin_and_refuses_unavailable_source` (`test_native_word_anchor.py:722`), source-read revocation (`:741`) | **Source-pin mismatch and atomic refusal:** covered at source-input boundary. | App command shape and association-specific writes remain uncovered. |
| Populated config clip mirror when primary parent collection is empty: `:269-367` | None exact. `test_media_transcript.py` write/update/sync tests are document behavior, not association reconciliation. | **No exact Python witness.** | Primary/config mirror selection, caption ownership, and review movement are uncovered. |
| Malformed pinned source before either nested plane changes: `:384-396` | `test_missing_or_malformed_transcript_source_is_refused` (`:654-683`) | **Atomic source refusal:** covered for the existing source-input fixture. | App nested-plane atomicity is not proven. |

The App module validates exact project/document/version/digest and canonical `media.transcript/v1` source identity at `transcriptAssociateCapture.ts:103-133`; builds source-item membership/order guards at `:168-183`; projects canonical segments at `:210-228`; reconciles references/reviews at `:267-371`; and writes nested planes at `:406-515`. It emits `op: transcript.associate` at `:517-550`. None of those operation-specific semantics has a registered Agent counterpart at the exact Agent source.

**Transcript conclusion:** exact source pinning, retained input closure, source overwrite handling, word-anchor source semantics, and atomic malformed-source refusal are covered. Nested association/reconciliation and `transcript.associate` execution are uncovered.

## Generic patch semantics that can be reused honestly

Existing `doc.patch` evidence covers explicit null versus absent, opaque JSON, previous-value checks, created IDs, ordered insert/move/remove, collection membership/order reads, ABA/conflict behavior, atomic refusal, and merge precedence (`test_doc_patch_v2.py:69-144,221-273,384-496,652-700`). This is valid coverage for the generic operation only.

The smallest report-only continuation proposal is therefore:

1. Coordinate the App source owner and the App worker currently porting track/after-anchor behavior.
2. Add, if they identify a currently mounted generic path that needs a witness, a test-only track-shaped `doc.patch` fixture asserting the actual previous values, collection membership/order reads, list moves, and refusal atomicity. Label it `doc.patch`; add no `track.reorder` operation, schema, provider, pin, or new contract.
3. Add, if the mounted transcript/source path needs a witness, a test-only generic patch fixture for existing `parent.config.bundle` data plus exact verified source-pin inputs. Assert only actual nested changes, previous values, declared reads, and source refusal. Add no `transcript.associate` operation or invented reconciliation semantics.
4. Preserve the dormant App implementations and all their tests until the App worker has a faithful mounted replacement with executable coverage. An absent/unregistered old operation is never permission to delete promised behavior or tests.

This continuation is within the PLAN’s test-only path and needs no orchestrator approval. It requires coordination with the App source owner/worker so the test names the actual mounted semantics and does not duplicate or fictionalize them.

For after-anchor behavior specifically, the registered `clip.add-media` selector can represent insertion after a stable parent clip (`native_parent_media_commands.py:39-40,87-94`), but that fact alone does not prove the dormant App rate-aware/ripple/claim promises. Do not invent a new operation or infer that generic doc.patch preserves those promises until the App owner maps the actual local row/config mutation and its save handoff.

## Retained targeted evidence

These are the prior author-worker results, not new runs by this review:

```text
PYTHONPATH=/home/user/work/wt/agt-A4-provider-map-1732:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest --collect-only -q \
  tests/editing_conformance/test_doc_patch_v2.py \
  tests/editing_conformance/test_recipe_m2_parent_media.py
=> 187 tests collected in 1.55s

PYTHONPATH=/home/user/work/wt/agt-A4-provider-map-1732:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q \
  tests/editing_conformance/test_doc_patch_v2.py
=> 102 passed in 11.81s

PYTHONPATH=/home/user/work/wt/agt-A4-provider-map-1732:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q \
  tests/editing_conformance/test_recipe_m2_parent_media.py --maxfail=20
=> 71 passed, 14 failed in 26.64s
```

The 14 parent-media failures are actual targeted failures: six registry-reload authored-guard failures and eight exact/ordered provider reload/inverse failures involving nested inverse ranges. They are not “all parent-media green,” were not repaired, hidden, skipped, or weakened. The first combined bounded run timed out at its 30-second window while failures were still printing; the separate runs above are authoritative.

```text
PYTHONPATH=/home/user/work/wt/agt-A4-provider-map-1732:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q \
  tests/sdk/test_timeline_commit_provider.py \
  -k 'retained_input_closure_survives_document_overwrite_and_new_provider or missing_or_malformed_transcript_source_is_refused'
=> 9 passed, 105 deselected in 2.17s
```

No new quality run is required for this report-only review. The result is a bounded evidence map, not a claim that the full parent-media behavior or the App/Runtime mounted path is green.

## Final handoff

- **PASS (bounded):** registered `doc.patch` generic semantics; registered `clip.add-media` provider boundary and substantial parent-media fixture coverage; exact transcript source-pin/retention/refusal boundaries.
- **FAIL (complete A4 map):** no registered or executable Agent witness for `track.reorder` or `transcript.associate`; no exact proof for dormant after-anchor capture parity; 14 retained parent-media targeted failures.
- **Never infer retirement:** missing/unregistered old operations do not authorize dropping the App implementations or behavioral tests. Preserve them until faithfully mounted and executable coverage exists.
- **Next owner:** hand this map to the App source owner and the two App A4 workers. They own the actual cuts/mounts; this review adds no product operation, schema, provider, pin, guard, daemon, or environment change.
