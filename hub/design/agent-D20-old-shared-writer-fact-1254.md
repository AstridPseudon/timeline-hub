# D20 old shared-writer fact

**YES — an old ordinary publication writer could create a second same-timeline placement while retaining the same physical shot and internal revision.**

## Minimal source proof

- Frozen R4 Runtime source blob `1a73b22dfdd6f11234b684d98b982974bec9a25c`, `runtime_protocol/service.py:3296`, defines `RuntimeService.publish_parent_composition(self, project_id, timeline_id, body, *, idempotency_key=None)`. It reads `body["parent_composition"]["occurrences"]`, resolves the closure once by `(shot_id, shot_revision_id)`, and rejects only duplicate `occurrence_id` values (`:3411-3473`); there is no uniqueness guard on the shot/revision pair. The accepted write inserts each occurrence row with its own ordinal while the closure/shot/internal rows remain set-like.
- Frozen R4 Runtime test blob `bdad1d3420b35e58afaea8bd0604f3ae422b5680`, `tests/test_shot_composition_runtime.py:94-127`, builds an ordinary publication candidate with two unique occurrence IDs (`occurrence-1`, `occurrence-2`) pointing at the same `shot_id` and `shot_revision_id`, with placements at 0 and 1000 ms. `:159-165` calls the real `_publication_route`/`publish_parent_composition`, asserts HTTP status 200, reads the committed parent, asserts two occurrences, and asserts the sole shared `shot_revision_id`.
- The same frozen test's `:378-386` independently copies an occurrence, changes only its ID/placement, appends it to an ordinary publication, and calls `service.publish_parent_composition` successfully before integrity checks. This is not direct SQLite fixture injection.
- Current App source `tests/e2e/local/three-products.p2-popup.spec.ts:209-272` shows the exact retired caller shape: `preparePopupSeed(harness)` clones `sourceOccurrence`, creates `f2-occurrence-copy`, preserves the source `shot_id`/`shot_revision_id`/internal closure, changes only `placement.start_ms` to `12000`, then posts the full publication to `POST /v1/projects/{project}/timelines/{timeline}/composition-revisions` (`:266-270`). This is the private P2 fixture injection and is separate from the ordinary publication witness above.

## Agent carrier trace

The frozen R4 Agent old writer is also a carrier, though the decisive acceptance proof is Runtime-owned:

- Frozen R4 Agent `astrid/sdk/timeline/store.py` blob `3748991fe3cab508162da45ba029b7a4f8a4300a`, `publish_bundle(candidate, idempotency_key, *, client=None, force=False)` (`:311`), calls `publish_authoring_candidate` through `_Writer.publish_parent_composition(project_id, timeline_id, publication, *, idempotency_key)` (`:358-364`).
- Frozen R4 Agent authoring compiler blob `884232783b360bf69a2bdae464ad3e2df5a2d845`, `compile_authoring_candidate` placement loop (`:1385-1464`), enforces unique occurrence IDs but permits multiple placements to resolve to the same compiled shot; it emits each `shot_revision_id` and computes `referenced_shot_ids` as a set. `publish_authoring_candidate(candidate, writer, *, idempotency_key, media_imports=None)` (`:2020-2045`) passes the complete publication to that existing Runtime port.
- AST checks confirmed the exact signatures: Runtime `(self, project_id, timeline_id, body, *, idempotency_key)`; Agent `(candidate, writer, *, idempotency_key, media_imports)`.

## Boundary and next action

The existing G4 shared-seed audit and independent 1222 seam proof remain correct for the *current v2 replacement* paths: `doc.patch`, `occurrence.create`, `occurrence.duplicate`, `occurrence.fork`, and `timeline.duplicate` do not provide this exact authenticated same-timeline shared placement. They do not overturn the historical fact that the old publication writer accepted it.

**Ready board line:** `D20 YES — frozen R4 publish_parent_composition accepted two unique occurrences with identical shot_id/shot_revision_id (same physical/internal closure); old writer is an in-scope migration, with App popup caller separately traced at three-products.p2-popup.spec.ts:233-270.`

No product/test/dependency/schema/contract/generated files were changed. No full, HTTP, browser, native14/58, P1/P2/P3/P4, or D17 run was performed.
