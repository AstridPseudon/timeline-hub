# F-D86 SHEET13 — UNAPPLIED

No worktree source change was made. The protected failure is reproduced by static
source tracing on `f29bc274f5`.

## Exact media contradiction

- `tests/editing_conformance/test_native_sheet_current_runtime.py:98-142`
  selects the B internal timeline from `tests/fixtures/timeline_editing/tiny.json`.
- In that original closure, `P` is consumed by `b-vo` on the `vo` audio track,
  while the same source identity is retained in the registry; replacing it with
  `idea-1.png` / `image/png` is therefore not faithful.
- `tests/editing_conformance/test_recipe_clip_scalar_fields.py:35-63` constructs
  the App-shaped closure with one `OLD` media identity for both `f2-app` typed
  `image/png` and `f2-video` typed `video/mp4`, and for the child image registry;
  `AUDIO` is independently carried by `items` and `audio_bindings`.
- `astrid/sdk/timeline/native_media_admission.py:70-86` authenticates each
  admitted concrete `media_id` against Runtime raw media and selected catalog
  facts; `astrid/sdk/timeline/native_parent_media_commands.py:168-183` binds a
  selected media kind into the authored registry. One concrete `OLD` object
  cannot simultaneously be the original image/png and video/mp4 roles. Splitting
  the identity, choosing one MIME, or inferring a role from a filename changes
  the original sharing/topology. This is the exact contradiction required to be
  reported UNAPPLIED.

## Exact emitter seam

- `seed_shared_occurrence_parent` at lines 433-435 calls
  `emit_document_commands(before_bundle, authored_bundle)` after foreign shared
  occurrence creation.
- The authored overlay changes managed parent collections (clips/registry) while
  the destination skeleton contains only tracks and occurrence edges. The
  emitter consequently reaches its existing managed-edge / closure-membership
  refusal in `astrid/sdk/timeline/emitter.py:266-267`.
- `_publish_current_candidate`'s added reload equality assertion is only a
  post-publication check; it cannot alter that before/after relationship.
- Correcting this requires a genuine semantic managed-creation setup (and the
  same authenticated canonical baseline), but that setup is blocked by the
  exact `OLD` MIME/share contradiction above. No emitter guard or product caller
  was changed.

## Static checks

- `/home/user/work/venv-agent/bin/python -m ruff check tests/editing_conformance/test_native_sheet_current_runtime.py` — PASS
- `/home/user/work/venv-agent/bin/python -m mypy tests/editing_conformance/test_native_sheet_current_runtime.py` — PASS
- in-memory `compile(...)` of the allowed file — PASS
- `git diff --check` — PASS (clean tree)

No pytest, collection, helper/fixture/function execution, service, browser,
render, build, or full suite was run.
