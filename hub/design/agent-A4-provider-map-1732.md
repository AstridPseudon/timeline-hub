# A4 provider coverage map

Date: 2026-10-23  
Scope: read-only Agent/App provider-coverage audit for the three App capture modules named by A4.  
Agent source: 6531622c8f198c3efb509217e303fcad0126c47b  
App source: 4c4c9c77c96fab70c4efef09db9a3bc456b0d803

## Verdict

The current authoritative Agent registry exposes doc.patch and clip.add-media, but not track.reorder or transcript.associate. The App capture modules for the latter two operations are therefore not backed by a registered Python provider fixture/test witness. Existing Python tests provide bounded evidence for generic document patching, parent-media birth, exact transcript source pins, refusal atomicity, and retained source inputs. They do not prove the dormant App operation shapes, nested transcript reconciliation, or App capture-specific claims.

No source, test, TypeScript golden, or assertion was changed. The App checkout was read only with git show at the exact snapshot above.

## Authoritative provider and mounted-caller map

| App intent/module | Current mounted path | Authoritative Agent entrypoint and arguments | Coverage result |
|---|---|---|---|
| Parent media add, including the commit-session parent-media port | App src/tools/video-editor/commands/commitSession.ts:444-519; parentClipAddMediaPort calls captureParentClipAddMedia and submits a command whose op is checked at :508-518 | astrid/sdk/timeline/commands.py:67-103 registers clip.add-media at :102; astrid/sdk/timeline/native_parent_media_commands.py:87-94 calls execute with schema_version 1, op clip.add-media, version 1, select parent or parent/clip:*, and {row, media}. The handler at :25-52 reads parent/config/output/fps, parent/source/source_window, occurrence placement, registry, and selected/created clip state; it creates/binds the media and clip and applies submitted read guards. | Registered. Existing parent-media witnesses cover this path, subject to the failing existing reload/inverse cases noted below. |
| App after-anchor capture module | src/tools/video-editor/commands/parentAfterAnchorCapture.ts:137-177 is defined, but git grep at the App snapshot found no production import/caller. Mounted useTimelineCommandsService.addClip instead uses local rows at :520-548 for afterClipId, and prepared media at :471-503. | The registered Agent entrypoint is still clip.add-media above; there is no registered after-anchor-specific provider operation or current Agent _after_capture_row witness. | Partially covered by generic/parent-media semantics, not by the dormant after-anchor capture basis. |
| Track reorder capture module | src/tools/video-editor/commands/trackReorderCapture.ts:138-173 is defined and tested, but no production import/call was found. Mounted useTimelineCommandsService.moveTrack uses local config mutation at :918-963, not this capture. | astrid/sdk/timeline/commands.py:67-103 has no track.reorder; no Agent handler/schema/provider fixture or Python test witness for that op was found. | Unregistered. Generic doc.patch list/order evidence exists, but it is not an authoritative track.reorder witness. |
| Transcript association capture module | src/tools/video-editor/commands/transcriptAssociateCapture.ts:517-573 is defined and tested, but no production import/call was found at the App snapshot. No mounted App caller for this association operation was found. | No transcript.associate registration, handler, schema, or Python provider fixture/test witness was found in Agent. | Unregistered. Existing Python tests prove exact verified transcript-source input behavior, not this nested association operation. |
| Generic mounted App editing | src/tools/video-editor/commands/documentPatchIntent.ts:109-223 creates a local patch intent; src/tools/video-editor/commands/localSaveSession.ts:162-179 serializes it as doc.patch. The commit request builder is src/tools/video-editor/commands/commitSession.ts:204-223. | Agent astrid/sdk/timeline/commands.py:67-68 registers doc.patch. The runtime commit service is created in astrid/sdk/timeline/commit.py:1216-1220. | Registered generic path. The App after-anchor and track paths currently reach local row/config intent and are later represented through this generic path, not through the dormant capture operations. |

The precise production caller for the currently registered parent-media provider is the App commit-session parentClipAddMediaPort, not the dormant after-anchor, track-reorder, or transcript-associate modules. The App request preserves the C0 envelope in commitSession.ts:204-223: api_version, project/timeline IDs, base pair, commands, label, full step metadata, merge mode, declared reads, dry_run false, and source via app. The current builder supplies the parent-media command and its patch/step metadata; the provider-side handler consumes the command arguments and read guards described above.

The Agent C0 response boundary is also present in the current provider: astrid/sdk/timeline/commit.py:1167-1188 prepares expected_head, canonical_document, document_digest, full records, id_map, semantic_events, provider/compiler versions, and accepts either preview or the authoritative port result. astrid/sdk/timeline/_commit_preview.py:7-22 and :83-105 preserve commands, bindings/effects/dependencies as generated records, steps, merge_mode, label, undo_steps, evaluated_head, base pins, and preview would_status with a null receipt. Accepted results come from port.accept(prepared) at commit.py:1187-1188, so the Runtime receipt/full-record/head contract remains authoritative rather than being projected locally. Failure envelopes preserve status, reason/code, path, base/current, conflicts, hint, and suggested_command at astrid/sdk/timeline/_commit_errors.py:74-110. This is the boundary for accepted/merged, canonical document, receipt, records, bindings/effects/dependencies/history/undo_steps, preview would_status, and structured failure details; no dormant App operation adds a parallel response shape.

## Exact behavior-to-witness mapping

### Parent after-anchor / clip.add-media

App parentAfterAnchorCapture.test.ts at the exact App commit:

- Fixture and media selection shape: src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts:14-50.
- Main raw-clone, rate-aware ripple, opaque-data, complete-read/selection/binding/created-claim assertion: :59-173. It expects a closed clip.add-media command, anchor-selected insertion, cloned row/media, same-track later-member shifts, unchanged other-track members, and exact reads/writes/bindings/created records.
- JSON basis reload, wrong ownership/identity, missing anchor, and catalog-digest refusal: :176-195.
- Source transition and missing/null source cases: :197-247; null effect/track/asset and timing boundary cases: :248-309.
- Parity note: :310-355 references an older Agent commit and _after_capture_row; no corresponding symbol exists in current Agent source.

Agent witnesses:

- tests/editing_conformance/test_recipe_m2_parent_media.py:test_exact_capture_replay_scoped_birth_and_inverse (:123) and test_portable_golden (:148) cover exact parent-media command capture/replay and a portable fixture. Fixture: tests/editing_conformance/fixtures/recipe_m2_parent_media.json:45, with parent inputs at :50-62 and command arguments at :65-74.
- test_existing_binding_is_required_exactly_without_birth (:156), test_missing_registry_containers_are_guarded_writes_with_exact_inverse_redo (:172), and test_explicit_malformed_asset_containers_refuse_untouched (:222) cover existing binding, registry-container, malformed-input, and atomic refusal boundaries.
- Refusal matrix: test_refusals_preserve_input (:239), including missing inputs, wrong object/catalog, intent, occurrence/lane, media kind, occupied IDs/aliases, invalid windows/speed/hold, registry state, and membership cases.
- Replacement/order/rebase/undo coverage: test_replace_removes... (:302), test_replace_first_middle_last_exact_reload_inverse_redo_and_replay (:330), test_replace_preserves_equal_z_order... (:352), test_replace_keeps_order_and_membership_guards (:365), test_replace_refuses_corrupt_insertion_proof (:388), test_replacement_composes... (:401), test_asset_alias_inverse_is_guarded... (:440), test_disjoint_edit_rebases... (:452), test_provider_exact_reload_inverse_redo... (:468), and test_ordered_provider_reload_inverse_redo... (:510).
- Registered implementation: astrid/sdk/timeline/native_parent_media_commands.py:25-52,87-94. It verifies media, refuses non-null source windows and occurrence-owned lanes, reads parent/config/output/occurrence/registry state, creates the media/clip binding, and applies exact submitted reads.

This is the strongest existing provider mapping. It covers raw clone, rate-aware timing, ripple/order, null/absent/opaque data, created claims, previous values, membership/order guards, refusals, and the detached provider boundary. It does not prove that the dormant after-anchor App capture module is production-mounted or that its exact capture basis is accepted by a distinct provider entrypoint.

### Track reorder / track.reorder

App trackReorderCapture.ts:

- Claims, collection address, and authored track-reference validation: :14-72.
- Command envelope assertion: :74-83; requires op track.reorder, select parent, and an empty intent.
- Collection membership/order read: :85-100; mutation of parent.track_order and track rows: :102-136; capture/finish/execute: :138-173.
- trackReorderCapture.test.ts:28-60 asserts raw rows, null/opaque lane data, exact command/read/selection/expect/authorship claims, permutation/order, and input immutability. Same-order explicit-write case: :63-72. Malformed/foreign/duplicate/stale-order refusals: :75-114.

Existing Agent generic witnesses include tests/editing_conformance/test_doc_patch_v2.py:test_ordered_read_detects_shape_aba_and_membership_read_ignores_reorder (:425-436), test_list_move_merges_unread_sibling_item_field (:439-448), test_list_move_conflict_precedence (:451-486), test_field_edit_merges_intervening_sibling_order_change (:489-496), and broader ordered insert/move/remove and list guard tests (:102-144). These verify generic doc.patch list membership/order guards and merge behavior. They do not assert the App track fixture, track.reorder op envelope, track-specific writes, or track-specific refusal claims. No Python test may honestly be labelled the authoritative witness for dormant track.reorder because the operation is absent from the Agent registry.

### Transcript association / transcript.associate

App transcriptAssociateCapture.ts:

- Operation/schema constants and exact pin helper: :30-40,78-91.
- Verified transcript validation: :103-133; checks project/document/version/digest, media.transcript/v1, media/source identity, canonical transcript document ID, and word membership.
- Source item selection and membership/order guards: :136-184; canonical nested carrier validation: :186-200.
- Canonical transcript item projection: :210-228; reference/review reconciliation begins at :267; exact command argument shape: :387-395.
- Provider-like apply/claim behavior for parent config, nested transcriptReferences, itemsBySchemaRef, source items, caption mirrors, and extension review data: :406-515; capture/finish/execute: :517-573.
- transcriptAssociateCapture.test.ts:162-222 is the primary nested-plane/opaque/reconciliation assertion; prior-pin replacement: :225-252; new-pin mismatch atomic refusal: :254-267; primary-mirror-empty behavior: :269-367; caption/review collision and shared-ownership refusals: :370-382; malformed pinned source refusal: :384-396.

Existing Agent source-input witnesses:

- Exact transcript pin verification: astrid/sdk/timeline/native_source_inputs.py:82-106 through get_project_verified_document, exact returned pin/document scope/version/digest checks, and _validate_transcript_v1.
- tests/sdk/test_timeline_commit_provider.py:test_retained_input_closure_survives_document_overwrite_and_new_provider (:620-651) covers retained transcript/config source inputs through a detached provider move, live-source overwrite, second move, and inverse. test_missing_or_malformed_transcript_source_is_refused (:654-683) covers missing, version, digest, project, source-identity, kind, and pin damage with atomic refusal.
- Native word-anchor tests provide additional exact source-input witnesses, including test_provider_resolves_exact_first_use_pin_and_refuses_unavailable_source (tests/editing_conformance/test_native_word_anchor.py:722), test_source_read_revocation_is_atomic_before_first_use_retention (:741), and exact source/timing/word-binding cases at :115-711. Portable capture/refusal boundaries are in tests/editing_conformance/test_native_word_anchor_vectors.py:68-86.
- tests/sdk/test_media_transcript.py:24 and subsequent write/update/sync tests cover existing media-transcript document behavior, not association reconciliation.

These witnesses prove exact verified source pins, retained input closure, source overwrite handling, refusal atomicity, and word-anchor source semantics. They do not prove the App nested transcriptReferences/itemsBySchemaRef planes, canonical segment projection, caption mirror, review extension reconciliation, prior-pin replacement, or a transcript.associate provider command. The existing source fixture uses lines (tests/sdk/test_timeline_commit_provider.py:601-617), whereas the App capture fixture uses canonical segments; that is a real fixture/schema boundary.

## Boundary and fixture assessment

- Agent provider tests use detached realms/ports (tests/sdk/test_timeline_commit_provider.py:68-163) and fake document/source providers. They are provider-boundary witnesses, not live HTTP, browser, renderer, or production App-runtime tests.
- The Agent transcript fixture includes schema media.transcript/v1, media/source IDs, lines, and a pin. It is not the App nested bundle with transcriptReferences, itemsBySchemaRef, caption ownership, and review extension data.
- The parent-media fixture is a concrete JSON recipe with parent clips, registry/media data, source timing, and authored inputs. It is the closest authoritative registered-provider fixture for the App parent-media behavior.
- Generic doc.patch tests cover null/absent values, opaque data, previous values, created claims, list membership/order, refusals, and merge/history behavior. They should not be relabelled as witnesses for absent operations.
- No evidence was collected from browser, HTTP, full, native-14, original SDK-4, Runtime-20, renderer, benchmark, or build suites, per the A4 boundary.

## Targeted collection and test evidence

Commands were run from the Agent worktree with shared Runtime source on PYTHONPATH:

    PYTHONPATH=/home/user/work/wt/agt-A4-provider-map-1732:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest --collect-only -q tests/editing_conformance/test_doc_patch_v2.py tests/editing_conformance/test_recipe_m2_parent_media.py

Result: 187 tests collected in 1.55s.

    PYTHONPATH=/home/user/work/wt/agt-A4-provider-map-1732:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_doc_patch_v2.py

Result: 102 passed in 11.81s.

    PYTHONPATH=/home/user/work/wt/agt-A4-provider-map-1732:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_m2_parent_media.py --maxfail=20

Result: 71 passed, 14 failed in 26.64s. Six missing-registry-container guard cases fail after reload with CommandError: original authored guard changed; eight exact/ordered provider reload/inverse cases fail with CommitRejected: nested inverse ranges differ from accepted history. This is evidence that the current snapshot is not fully green; it was not repaired or masked.

    PYTHONPATH=/home/user/work/wt/agt-A4-provider-map-1732:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_timeline_commit_provider.py -k 'retained_input_closure_survives_document_overwrite_and_new_provider or missing_or_malformed_transcript_source_is_refused'

Result: 9 passed, 105 deselected in 2.17s.

The first combined bounded run was attempted, but its 30-second execution window expired while parent-media failures were still being reported; the separate runs above are authoritative. No App Vitest/browser/full/HTTP suite was run.

## Smallest continuation proposal — coordinate before authoring

No continuation tests were authored because the missing operations have no Agent schema, registration, or provider entrypoint to exercise. Adding a Python test that pretends otherwise would overclaim coverage.

If the orchestrator approves a test-only continuation after coordination with the App worker:

1. For currently mounted track behavior, add only a Python witness for the existing generic doc.patch list-move representation, using a track-shaped fixture and asserting actual previous values, membership/order reads, and refusal atomicity. Label it doc.patch, not track.reorder; add no operation or schema.
2. For currently mounted transcript/source behavior, adapt the existing document-patch fixture only enough to model existing nested parent.config.bundle data and exact verified source pin. Assert actual doc.patch changes, previous values, no unjustified created claims, declared reads, and exact source-input refusal boundary. Add no transcript.associate, API, schema, or reconciliation semantics.
3. If intended retirement requires preserving dormant App capture claims themselves, that is not test-only work: it requires an explicit provider/API decision and App-worker coordination before authoring. Current evidence supports retirement of unregistered operation claims, not certification of them.

## Handoff

Safe conclusion for A4: clip.add-media and generic doc.patch have registered Agent witnesses; track.reorder and transcript.associate do not. Parent-media behavior has a substantial fixture/test map but the selected parent-media suite currently has 14 failures in existing reload/inverse checks. Transcript source pinning is covered under existing doc.patch/source-context and native word-anchor paths, while App nested association/review reconciliation remains uncovered. The App track and after-anchor workers should use this map to avoid duplicating implementation or inventing provider operations.

