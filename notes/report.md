# Worker report: M2 opacity SET/CLEAR

## What changed

- Extended the existing closed `clip.set@1` args schema with `values.opacity`
  as a raw finite JSON number in the inclusive `0..1` fraction range.
- Added `opacity` to the existing explicit `clear` enum. Clear removes the
  leaf; it does not write null, an empty string, a default, or a percentage
  conversion.
- Kept the existing parent/occurrence target and recorder path. Opacity uses
  the ordinary exact leaf before-state/read guard, generic inverse/redo, ABA
  protection, and disjoint rebase. No new operation, DTO, endpoint, renderer,
  or legacy fallback was added.
- Added conformance for the UI-shaped capture, closed-schema refusal,
  ABSENT/null/zero distinctions, same-value SET, clear, exact undo/redo,
  opaque namespace preservation, shared-occurrence isolation, ABA refusal,
  and disjoint parameter rebase.
- Published the absolute contract at
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/m2-opacity-contract.md`.

## Tests and checks

- `PYTHONPATH=. python3 -m pytest -q tests/editing_conformance/test_recipe_clip_scalar_fields.py tests/editing_conformance/test_parent_track_label.py tests/editing_conformance/test_commit_runtime_clip_scalar_fields.py tests/sdk/test_timeline_clip_scalar_provider.py`
  — **158 passed, 3 deselected**.
- `PYTHONPATH=. python3 -m pytest -q tests/editing_conformance/test_recipe_scalar_commands.py tests/editing_conformance/test_inverse_clear_batches.py tests/editing_conformance/test_native_batch_ingress.py`
  — **170 passed, 40 deselected**.
- `ruff check astrid/sdk/timeline/_clip_scalar_commands.py tests/editing_conformance/test_recipe_clip_scalar_fields.py`
  — **passed**.
- `python3 -m json.tool astrid/core/timeline/schema/edit-command.schema.json`
  — **passed**.
- Direct closed-schema smoke check for valid `0.4` and refusal of unknown,
  boolean, null, empty-string, and out-of-range opacity values — **passed**.
- `git diff --check` — **passed**.
- Existing golden
  `tests/editing_conformance/fixtures/recipe_m2_app_clip_scalar_fields.json`
  SHA-256 before/after — **identical**:
  `8bb75e23c10c9677635d85f33f219b7f1b2d89baf481e3b7ed21f425b76f0c06`.

No full suite, browser, socket, install, network, merge, pin, or push was run.

## Decisions / limits

The canonical opacity unit is the existing raw visual fraction `0..1`; no
percent conversion, clamp, or default normalization was introduced. The raw
canonical timeline schema already admits numeric opacity, so only the existing
`clip.set` closed command schema needed extension. App wiring remains a
separate handoff; this worker did not modify the App worktree.

## Recommended next step

App should adapt its reviewed `updateClip` opacity producer to emit this exact
`clip.set` capture shape and then prove accepted reload/retry/undo and zero
legacy snapshot traffic before deleting its old writer path.
