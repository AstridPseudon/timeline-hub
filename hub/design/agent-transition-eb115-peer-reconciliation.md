# Agent transition peer reconciliation

## Disposition

Both peer findings against Agent candidate `eb115db81ac2c24b182fe6873fbd883da851571e` are confirmed and corrected in this worktree. The correction is writer-side only; the `clip.set` carrier, canonical incoming policy, explicit paired clear, transition-only clear, and existing inverse/P1/P2 proof remain in place.

## Controls and correction

- `_transition_set` now requires exactly one same-track predecessor from the existing recorded `transition.predecessor` selection, applies Main’s literal adjacency tolerance (`abs(predecessor_end - destination_start) < 0.001`), and applies Main’s shortest-neighbor fit (`duration_frames <= min(predecessor_duration, destination_duration) * fps + 0.0001`). No duration clamping or field stripping was added.
- The selected-pack `clip.set` resolver now participates in the existing retained selected-authority chain. For a stable `(packId, id, kind)` reference, a revision-only update must use the accepted P1 source/snapshot proof; a later P2 pin is refused atomically. `clip.set-element` remains the explicit reselection operation. Existing inverse/replay machinery was not changed.
- `clear: ['transition', 'elementRef']` still performs the guarded paired removal, including legacy `element_ref`; `clear: ['transition']` still preserves unrelated references. No DTO, schema, generated artifact, public pin, normal-generation path, freeze, or new API was added.

The new writer checks govern newly authored SETs. No playback/compiler rule was widened or changed, so old data remains readable through the existing playback path; the legacy transition-only clear remains independently executable.

## Executable evidence

Added counterexamples for a gap, cross-track destination, and oversized transition, plus a provider-level first-P1 then same-reference P2 substitution. The P2 attempt leaves the Runtime-shaped realm head, entries, and documents unchanged. Existing selected-authority forward/inverse tests remain unchanged in meaning and pass.

Exact targeted command:

```text
PYTHONPATH=. /home/user/work/venv-agent/bin/pytest -q tests/sdk/test_timeline_transition_schema.py tests/sdk/test_timeline_selected_param_authority.py tests/editing_conformance/test_recipe_clip_scalar_fields.py tests/sdk/test_timeline_clip_scalar_provider.py tests/sdk/test_timeline_current_union_schema.py
```

Result: **183 passed in 205.49s**. No full suite, browser, socket, or live Runtime run was requested.

## Source/schema identity

- Base/source candidate: `eb115db81ac2c24b182fe6873fbd883da851571e`.
- Source files changed: `_clip_scalar_commands.py`, `_selected_param_authority.py`, `commit.py`; their post-change SHA-256 values are `db72c5dbaed2eac46b9a5132dcbbc5533bcca904fdc725e9a5e821b9d6dbf8d6`, `2747d3c64a5eebe9ee11c5c8fca5f23afaa13f6c9ef406a98eeaec572924bed8`, and `d5faef1698d183017eb6a39710ca012e83d26469f88e1621f0214ab164c6ce88` respectively.
- Schema unchanged: `astrid/core/timeline/schema/edit-command.schema.json` SHA-256 `a70f0e8898c6acccb34062e73733c93dd4e7bc22c34ef012431e1791907e1f4a`.

The Runtime/App peer contracts remain unpublished and were not modified here.
