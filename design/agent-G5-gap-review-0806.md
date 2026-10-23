# G5 independent Luna review: HARD Sol draft 68a987d6b

## Disposition

**FAIL.** This review covers draft 68a987d6b, based on tl/agt-G5-sol-complete-0741 at 1d74f90bf. The two preserved positive behavioral cases remain red, so the draft cannot be called PASS:

1. test_duplicate_of_a_chapter_film_keeps_one_distinct_shot_per_chapter: **FAIL**, stopped by the Runtime-verified-media boundary.
2. test_duplicate_commit_keeps_a_repeated_shot_shared: **FAIL**, stopped by identity_collision.

The positive assertions were preserved. I made no product or test implementation changes, did not weaken/skip/xfail/delete tests, and did not request merge.

## Exact behavioral evidence

Final targeted command:

~~~sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTEST_ADDOPTS= /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_sync.py tests/sdk/test_p4_commit_v2.py tests/sdk/test_p4_ten_note_provider.py tests/sdk/test_p4_note_rerun.py tests/sdk/test_p4_cli_sheet_v2.py tests/editing_conformance/test_document_patch_emitter_engine.py tests/editing_conformance/test_document_patch_emitter_v2.py tests/sdk/test_authoring_diff_cli.py tests/timeline/test_authoring_diff_format.py tests/sdk/test_timeline_restructure.py tests/sdk/test_scene_save_core.py tests/sdk/test_timeline_checkout.py::test_three_way_merges_disjoint_edits_and_refuses_overlapping_ones tests/sdk/test_timeline_checkout.py::test_two_writers_on_one_working_copy_merge_and_never_drop_each_others_edits
~~~

Result: 2 failed, 215 passed in 36.52s.

Additional command from the completion report:

~~~sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/packs/timeline/test_verbs_working_copy.py -k 'duplicate or copy_content or id_map or parses_to_its_handler'
~~~

Result: 10 passed, 26 deselected in 1.55s. This covers archive cleanup and working-copy scaffolding, but not the two required positive restructure cases.

### Positive 1: empty-destination chapter-film duplication

Failing test: tests/sdk/test_timeline_restructure.py::test_duplicate_of_a_chapter_film_keeps_one_distinct_shot_per_chapter.

The test creates an authenticated canonical empty destination with generated.verified_media=[] and requires three chapter occurrences, one distinct shot per chapter, preserved names, and distinct IDs. It does not invent media bytes, a pin, a schema field, or a client-side Runtime fact.

Exact production fail path:

1. astrid/sdk/timeline_duplicate.py:393, _commit_bundle.
2. astrid/sdk/timeline_duplicate.py:56, _stage_bundle(session, desired).
3. astrid/sdk/timeline/commit_session.py:188, _capture_free_edits.
4. astrid/sdk/timeline/_doc_patch.py:416, patch application.
5. astrid/sdk/timeline/_doc_patch.py:311, CommandError("patch references media outside Runtime-verified inputs", kind="dependency_changed", ref="parent").
6. The duplicate wrapper catches the failure, archives the partial destination again, and raises TimelineEditError reporting that nothing was created.

The source closure is not available to _doc_patch.py as an accepted Runtime-verified input for this destination. The current destination dependency manifest carries immutable media ID/content digest, while the accepted MediaSelection requires the five Runtime-authenticated fields asset, generation_id, variant_id, object_id, and catalog_digest. The fixture does not and must not fabricate them.

Source-backed classification: I found no existing authenticated Agent input, stage, or semantic command in the current v2 wire that can carry this original source closure into an empty destination without adding facts. The current registry in astrid/sdk/timeline/commands.py:63-96 includes doc.patch, occurrence.create, occurrence.duplicate, occurrence.fork, and media operations, but no timeline.duplicate.

The current Runtime contract requires root/closure creation and managed-edge changes to use authenticated semantic commands; new media must already be Runtime-verified; callers cannot forge manifest pins or CAS identities; occurrence shot/revision links are provider-managed closure edges; and doc.patch cannot impersonate effect-root or managed-edge creation. Existing media commands can carry the exact five-field selection only after Runtime verifies it. This is a capability gap, not a missing test argument.

Smallest source-backed repair: add one Runtime-owned authenticated source-closure import/duplicate semantic operation to the current v2 contract, with an exact source timeline/revision/publication reference and Runtime-produced closure/media selections. Agent should collect the exact source reference and invoke that provider command. Runtime must load the exact source revision, verify source/destination identity separation, authenticate imported media, allocate fresh destination occurrence/shot identities, and return canonical document/effects. Negative controls must reject an unverified source revision, mismatched source pair, caller-forged media fields, source/destination aliasing, and ordinary doc.patch attempts to write managed closure edges.

This is not covered by the current C0 v2 wire. The frozen R4 SDK candidate has useful source-backed evidence: timeline_duplicate.py, commands.py, and commit.py:_load_duplicate_source loaded an exact source parent revision/closure, reserved fresh identities, and sent source, bootstrap_revision_id, and identities to a Runtime command. That old detached-writer design cannot be restored silently: current v2 registry/schema and C0 do not contain it. A concrete Agent/Runtime contract decision is required.

Owner: Runtime owns authenticated source closure import and media/managed-edge verification. Agent owns the bounded caller adapter and public behavior preservation. No existing contract authority covers the operation.

### Positive 2: repeated-shot copy

Failing test: tests/sdk/test_timeline_restructure.py::test_duplicate_commit_keeps_a_repeated_shot_shared.

The desired canonical bundle has two distinct occurrence IDs sharing one copied shot ID, preserving sharing, count, order, and identity.

Exact production fail path:

1. astrid/sdk/timeline_duplicate.py:_commit_bundle.
2. astrid/sdk/timeline_duplicate.py:_stage_bundle, at the second capture_occurrence_create.
3. astrid/sdk/timeline/native_occurrence_create.py:41, calling ctx.create_entity("shot:" + shot_id, ...).
4. astrid/sdk/timeline/_recording.py:196, raising CommandError("created identity is occupied", kind="identity_collision").

The current occurrence.create schema is occurrence_id, shot_id, name, track, on, duration, and its implementation always creates both a fresh shot and a fresh occurrence. It has no source-shot reference or existing-shot attachment mode. Runtime contract/schemas/edit-command.json:2016-2032 defines OccurrenceDuplicateArgs with only occurrence_id and shot_id.

Exact existing-command trace:

- occurrence.duplicate in astrid/sdk/timeline/native_occurrence_duplicate.py reads one selected occurrence; copy_child creates a fresh shot and fresh occurrence. It cannot place an existing copied shot or import across timelines.
- occurrence.fork copies a child and changes one existing occurrence's shot link; it does not create a second occurrence.
- placement.create in astrid/sdk/timeline/native_placement_commands.py:81-99 adds image media inside an existing occurrence; it is not parent occurrence placement.
- occurrence.create is the failing caller and necessarily collides when asked to create a second occurrence around an occupied shot identity.

No existing registered command places an existing copied shot while preserving the required semantics. Guessing an argument to occurrence.create, occurrence.duplicate, or occurrence.fork would be an invalid weaker oracle.

Smallest source-backed repair: add or expose a Runtime-owned semantic operation to create an occurrence referencing an existing copied shot, or extend an existing command only after the v2 contract explicitly defines that distinction. It must accept only a Runtime-authenticated shot from the same duplication transaction, allocate/check only a fresh occurrence identity, preserve order and metadata, and reject arbitrary cross-document or caller-forged references. Negative controls must reject an occupied occurrence ID, a shot not allocated by the authenticated source-closure operation, a source/destination mismatch, and ordinary root patch mutation of the managed shot edge.

Owner: Runtime owns the managed closure edge, identity authorization, and negative controls. Agent maps canonical repeated rows to the command and consumes canonical state. C0/current frozen v2 wire does not cover this; a concrete Agent/Runtime contract decision is needed.

### Exact caller/import map

The failing Agent call chain imports and crosses these concrete boundaries: timeline_duplicate._commit_bundle -> timeline_duplicate._stage_bundle -> CommitSession._capture_free_edits -> _doc_patch patch application for the media failure; and timeline_duplicate._stage_bundle -> native_occurrence_create -> recording.create_entity for the identity failure. The command surface is assembled by astrid/sdk/timeline/commands.py, while the Runtime-side wire authority is /home/user/work/runtime/contract/schemas/edit-command.json and contract/commit-v2.md. The relevant registered operations are doc.patch, occurrence.create, occurrence.duplicate, occurrence.fork, and placement.create; no registered timeline.duplicate or existing-shot occurrence placement operation was found. These are the exact imports/callers audited, not a guessed alternate executor.

## Cumulative retirement and integration audit

The cumulative retirement range 4edc4b321..68a987d6b is 17 files, 531 insertions, and 1116 deletions. The draft own delta 1d74f90b..68a987d6b is 7 files, 451 insertions, and 185 deletions.

Production retired-name search:

~~~sh
rg -n 'publish_bundle|three_way|document_diff|_cmd_publish|_configure_publish|commands-file|--publication' astrid/sdk/timeline astrid/sdk/timeline_duplicate.py astrid/sdk/timeline_checkout.py astrid/packs/timeline
~~~

Result: no matches. Generic publish remaining in astrid/sdk/timeline/publish.py:82-84 and attached native_checkout.py:257 is intentional fail-fast/attached behavior, not retired publish_bundle. Old names still occur in unrelated existing tests, including transaction/publish-connection and old editing-conformance fixtures; I did not delete them. Their full-suite status is unverified.

The migrated scaffolds use real production callers: test_timeline_sync.py invokes Agent commands.execute and canonical document conversion with Runtime verified_media; test_p4_cli_sheet_v2.py retains sheet/body/provenance/full-bundle assertions; test_scene_save_core.py exercises _commit_bundle and real bundle connection; test_timeline_checkout.py uses timeline.open commit sessions for disjoint merge/conflict/reapply; and test_timeline_restructure.py exercises the real CLI restructure path while retaining lost-ACK, narration, cleanup, and both positives.

Separate cumulative integration gap: current /home/user/work/agent on tl/integration at e49a6e76b contains G2 commit 68d54e15a, absent from this draft. G2 adds canonical _runtime_document hydration in astrid/sdk/timeline/commit_session.py via _adopt, _execution_bundle, _capture_free_edits, and _append, plus tests/sdk/test_timeline_public_command.py (194 lines). That public suite covers batching/history/restart, child free-edit hydration, contradictory shared-alias refusal, function-conflict rehydration/re-run, preview would_status, and source/patch guards for pair, foreign, digest, outside, and previous references. The draft deletes that test and lacks the hydration changes, so it is not cumulative with current integration qualification. This is independent of the two restructure failures.

## Quality checks

~~~sh
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/agt-G5-gap-review-0806-ruff-cache make ruff PY=/home/user/work/venv-agent/bin/python
~~~

Result: Ruff findings current=2148 baseline=2148; ruff baseline passed.

~~~sh
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/agt-G5-gap-review-0806-mypy-cache /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
~~~

Result: Mypy findings current=1904 baseline=1904.

~~~sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
~~~

Results: runtime.lock.json OK; artifacts.json current; git diff --check clean.

No full suite, browser suite, original P4 HTTP, native14, crash24, or duplicate full suite was run. No localhost/live-socket test was run. The targeted command above is the final behavioral evidence.

## Next steps

1. Keep FAIL; do not merge.
2. Dispatch the bounded Agent/Runtime v2 contract decision for authenticated source-closure duplication and existing-shot occurrence placement, with the negative controls above.
3. Reconcile the draft with G2 hydration and retain tests/sdk/test_timeline_public_command.py.
4. After owner repair, rerun the exact 217-case targeted command and normal lint/type/vendor/artifact/diff checks before broader test-service suites.

No safety refusal, guard waiver, alternate executor, hand-generated bytes, M5, or upstream push was used.
