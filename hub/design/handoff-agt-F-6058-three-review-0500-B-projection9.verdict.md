# B — capture projection NOCANDIDATE review

Verdict: `NOCANDIDATE / BLOCKED` is source-supported for the requested current route. No safe test patch exists in this scope.

Refs and exact file blobs:

- Captured base/parent: `tl/integration` at `6cd767b6afd157b3f12e14dde5e9ef50dcb1f70a`.
- Candidate branch: `tl/agt-F-6058-projection9-0451` at `6cd767b6afd157b3f12e14dde5e9ef50dcb1f70a` (parent `786385631b8096e50e66b8ecff1e7034c5bc1da9`; merge parent includes the captured base); the assigned file has no diff from the captured base.
- Assigned file blob on both sides: `337379f6d9cc9732664b8423dfe537b6cd71fa09`.
- `tests/sdk/test_timeline_capture_projection.py` AST: 11 test functions, 43 assertions, 2 raises; decorators/parameters and the complete graph/opaque-field assertions are unchanged.

PASS_FACTS

- The current production bootstrap is source-backed: `native_occurrence_create.py:41-44` creates each new shot with `payload.items: []`, while `native_occurrence_media_commands.py:207-221` creates the physical child clip and registry binding only. There is no current native command in this route that materializes the legacy shot `items` row or its published item identity/map.
- The current genuine capture fixture route is `tests/sdk/test_capture_source_runtime.py:262-293`: Runtime commits initialize, parent track, occurrence, child track, and occurrence media through the registered provider. It does not create `shot.payload.items`.
- `test_timeline_capture_projection.py:274-367` then uses that genuine saved closure, and line 316 requires `source_payload["items"][0]` to preserve `item-1`; the current bootstrap cannot supply that item.
- The exact 9/complete-opaque projection surface remains live in the unchanged file: pure capture/no-IO checks, saved/candidate refusal guards, exact JSON identity checks, the real saved config/registry/full-pins golden, entire expansion golden, canonical image/read-envelope checks, and all six `change` variants of the SDK-opener comparison. No assertions were removed, weakened, xfailed, or replaced.
- An authentic retained legacy baseline exists in `tests/fixtures/timeline_redo_media_closure_1338.json` with accepted closure data containing `item-1` and an `item_id_map`; `tests/sdk/test_timeline_commit_provider_document.py:22-60` also supplies a genuine-shaped `document_fixture` with `item-1`, but that is an in-memory fixture API, not a current Runtime publication route.

FAIL_FACTS / BOUNDED HANDBACK

- The missing seam is one of: (1) an authenticated retained legacy Runtime closure whose shot payload already contains `items` plus its source provenance/item map, or (2) an approved current Runtime/Agent API that materializes those shot items and publishes the exact source mapping. `occurrence.create` plus `occurrence.add-media` is insufficient.
- Reusing `document_fixture`, injecting `items` into the current saved document, or adding a collector/body/helper would fabricate the unavailable source and violate the brief. Retiring the legacy behavior cannot be inferred from this absence; it is an orchestrator decision.
- No pytest, collection, import, service, or functional execution was run.

Static evidence:

- In-memory AST parse/compile: PASS.
- `/home/user/work/venv-agent/bin/python -m ruff check tests/sdk/test_timeline_capture_projection.py`: PASS.
- `/home/user/work/venv-agent/bin/python -m mypy tests/sdk/test_timeline_capture_projection.py`: PASS.
- `git diff --check 6cd767b6..6cd767b6 -- tests/sdk/test_timeline_capture_projection.py`: PASS (no candidate delta).
