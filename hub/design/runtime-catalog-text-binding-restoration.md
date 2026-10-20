# RT02 unplaced project-shot text binding restoration

Status: complete on worker branch `tl/rt-m2-catalog-text-binding-restore`.

## Original Main -> current proof

- Exact source precedent: Main `29d0954b6d78a7d7937d81bc36567b6dee7ca976` contains
  the existing `RuntimeService` implementations of `set_project_shot_text_binding`
  and `rebind_project_shot_text_binding` (the original methods begin at source
  lines 3932 and 3977).
- Current base before this change: `16acbb6`. Its service aliases at
  `runtime_protocol/service.py:3144-3145` sent both operations to the direct-shot
  retirement gate, while the routes and generated client methods already existed.
- Restored service methods are at `runtime_protocol/service.py:3441-3570`.
  The restoration reuses Main's project-scoped UUID identity, UTF-8/1 MiB
  validation, managed CAS ownership and integrity checks, durable mutation
  wrapper, command receipt/idempotency records, and event sequence/rebind shape.
  Events use the current presence projection payload (`state: "present"` plus
  project/shot/key/media/hash/size/MIME provenance), so this operation does not
  create a second direct-writer event format. Existing retained legacy payloads
  remain readable through the current default-present compatibility path.
- The original four positive assertions in `tests/test_shot_text_bindings.py`
  now run as positives. Their retired shot-create setup was replaced by a
  private row seed in the ephemeral test realm only; the binding operation under
  test remains the normal authenticated client/HTTP operation.

## Exact scope predicate

`RuntimeService._require_unplaced_project_shot` at
`runtime_protocol/service.py:3199-3218` requires:

1. `project_shots.id = shot_id AND project_shots.project_id = project_id`;
2. no row exists in `composition_revision_occurrences` for that same project
   and shot, joined through `parent_composition_revisions` with the same
   project.

The second condition is history-wide, not merely current-head-wide. It rejects
shots that have ever been accepted into film history, including a shot detached
from the current film later. It runs before CAS materialization or binding/event
writes for first use, and is rechecked for every existing-binding set/rebind.
The rejection is a 409 conflict with `details.reason=shot_in_film_history`;
missing project shots remain 404. Film-visible binding changes therefore remain
EditCommand operations.

## Change size and boundaries

- Product delta: `runtime_protocol/service.py`, +272/-2 lines; the two retired
  aliases were removed and only the existing two text-binding operations were
  restored.
- Test delta: `tests/test_shot_text_bindings.py` +18/-8 and
  `tests/test_timeline_shot_authority.py` +18/-8.
- No endpoint, DTO, table, public command, or new persistence journal was
  added. Existing CAS publication journaling is used for the existing managed
  object custody path.
- Project-shot create/update/item/reorder/promotion and other direct CRUD remain
  retired. Native `MediaReads` text selection and its strict new-selection MIME
  behavior remain unchanged; authenticated retained legacy `text/plain` reads
  remain covered.
- The parallel project-catalog promotion worker owns related unplaced-catalog
  scope/revision helpers. This worker kept the small local text-only guard above
  to avoid waiting or editing another worktree; final composition should
  deduplicate equivalent predicates when that helper is committed. No other
  worktree was edited.
- RKKEEP remains proposed until merge. No pin, publication, merge, or full suite
  was performed.

## Evidence

- `python -m pytest -q tests/test_timeline_text_selection.py tests/test_timeline_text_binding_clear.py tests/test_timeline_text_legacy_custody.py`
  -> **69 passed**, 1 existing pytest-config warning, 62.26s.
- Central daemon lane:
  `request-test rt-m2-catalog-text-binding-restore targeted --files "tests/test_shot_text_bindings.py tests/test_timeline_shot_authority.py"`
  -> **115 passed**, exit 0, 99.21s. This includes all four original positives,
  actual HTTP auth/scope checks, film-history refusal and shot-authority
  neighbors.
- Central native MIME/auth neighbor:
  `request-test rt-m2-catalog-text-binding-restore targeted --files "tests/test_timeline_verified_media_http.py"`
  -> **5 passed**, exit 0, 8.04s.
- `python -m compileall -q runtime_protocol packages/python/astrid_runtime_client`
  -> passed; generated caches were removed afterward.
- `git diff --check` -> passed.

No full suite, browser/live integration matrix, publication, merge, or pin was
run or claimed.
