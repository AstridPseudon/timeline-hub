# F-D86 / D95 source disposition

Disposition: `legacy-only` for actual9211 IDs 99 and 101; no worktree files
changed.

## Decisive distinction

The supported CURRENT word-reference form is `clip.anchor`, stored as a parent
clip's `app.astrid.word_anchors` choice. Its binding is the exact
`choice.document` pin (`document_id`, version, content digest), plus the
occurrence/clip source and stable `word_ids`. `_hydrate()` authenticates that
pin through `transcript_source`; the timing validator resolves the same pin and
source clip; accepted materialization retains the pin in the dependency
manifest. The current examples are `test_gate1_fresh_word_transcript_frontends.py`
and `test_timing_retained_inputs.py`, including the captured transcript
document v1 path. This is not a binding to a `text_bindings` row or to its MIME.

`text-binding.set` is a separate registered operation. It reads the
occurrence-owned row, and on set replaces the media/hash/size/MIME values while
dropping derived `binding_id` (and other derived fields); clear removes the row.
The registered production path is `RuntimeService.commit_timeline` -> registered
Agent provider -> `text_binding_set` -> final validation -> Runtime acceptance.

The two originals retain the historical clip reference shape
`elementRef = {kind: "text", binding_id, anchor}`. `_validate_element_reference`
explicitly treats that shape as historical, and `_text_reference_basis` includes
the matching binding row and the pinned transcript document. It requires the
declaration, clip type, and source basis to be unchanged. Rebinding changes the
row (including removal of `binding_id` by the native setter); clearing removes
the row. Both therefore invalidate the historical reference and are rejected
without a write under C0 §4/D12. The six-field current descriptor/MIME transition
is only one part of that mismatch, not the sole possible current-binding model.

## Exact compatibility conclusion

A CURRENT `word_anchors` choice can coexist with an unrelated legacy descriptor
row because its dependency is the immutable transcript document pin. That does
not make the originals current: their live clip reference remains the legacy
`elementRef.binding_id`, and validation still checks it independently. Replacing
that elementRef with a `word_anchors` choice would remove/change the original
bound target and its source semantics; adding a current choice while retaining
the legacy elementRef still leaves the historical basis check active. No
faithful setup-only migration preserves the original bound descriptor, MIME and
bytes, exact inverse assertions, and no-write purpose.

## Replacement coverage / gap

- Unbound current set/rebind and clear inverse coverage exists in
  `test_rebind_retains_v1_after_v2_restart_exact_inverse_and_redo` and
  `test_clear_removes_row_and_undo_restores_empty_exactly` (voiceover rows).
- The exact bound-main rebind/clear originals must be ledgered as legacy-only.
  Current C0 replacement coverage should name the unbound inverse cases above
  and the bound invalidating set/clear refusal with no-write. The latter refusal
  is established by the validator predicate/source path but is not a dedicated
  current test in this allowed file; add one targeted NEW-OURS case only in the
  later approved test/ledger migration step. This source-only task adds none.

No validator, guard, Runtime, schema, pin, generated, or original-test change
was made.
