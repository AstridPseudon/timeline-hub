# F-D86 R2/V2 exact source-only combined join

Task: `agt-R2-word-choice-restore-join-0622`.

This candidate is based on exact reviewed `word-mirror-source0617` at
`5e9acf59d266d45d74e5ae844bf62fddb64267f3` (parent `8c88ea8f06b65f9b79fb7810af04720845c5cc6f`).
Only the reviewed source blobs below were imported:

- R2 `7e7753564f127eb0242f53704ad33ba63d9e2e63`: `astrid/sdk/timeline/_step_undo.py` and
  `tests/sdk/test_timeline_restore_effect_order_runtime.py`.
- V2 `11d8a231ee503b409337eda563f865f0443e572e`: `astrid/sdk/timeline/native_word_anchor.py` and
  `astrid/sdk/timeline/_commit_timing_validation.py`.

All four product/test blobs are byte-exact to those reviewed commits. No semantic edits,
schema/client/runtime/pin/generated-file changes, or other tracked bytes were made.

## Canonical proof selection

Exactly three original selectors are carried forward:

1. Restore ID5 from the existing 0525/0558 selection:
   `tests/editing_conformance/test_word_binding_recipe.py::test_last_write_clear_undo_restore_and_restore_inverse`.
2. Word-choice ID3 from `handoff-agt-F-held13-0301-selectors.tsv`:
   `tests/editing_conformance/test_word_binding_recipe.py::test_follow_rebases_original_choice_after_source_move_and_reorder[True]`.
3. Word-choice ID9 from the same handoff:
   `tests/editing_conformance/test_word_binding_recipe.py::test_stale_anchor_refuses_when_intervening_window_excludes_selected_word`.

The original TEN, P4, parent-6, four-already-PASS controls, new-regression
repeat, and unchanged-60 controls are excluded. This source join reduces venue
setup only; it makes no coverage claim.

## Retained historical checkpoints

- Old RED `31475`: reviewed new regression RED; strict three controls PASS; the
  unchanged word-binding control remained an ERROR.
- Candidate `30269`: reviewed new regression plus strict three controls PASS;
  the unchanged word-binding setup remained an ERROR.
- Restore ID5 actual `1023`: ERROR at the unchanged contradictory-parent-mirrors
  setup.
- The stale-clip setup's two existing errors remain retained and are not
  converted to PASS.
- All other prior non-PASS dispositions remain non-PASS.

## Static validation

- AST parse and in-memory compile: PASS for all four imported Python files.
- Scoped Ruff candidate: PASS; parent Ruff diagnostics for the three existing
  product files: PASS.
- Scoped mypy candidate: PASS with zero diagnostics for the three product files;
  reviewed parent reports also record PASS with zero diagnostics.
- `git diff --check`: PASS.
- Static caller trace confirms `inverse.py` consumes `inverse_stages`, while
  `validation.py` calls `validate_candidate_timing` and the registered
  `commitTimeline/provider` path reaches the changed helpers.

No imports, pytest, collection, helper/fixture/function execution, probes,
services, browsers, rendering, builds, installs, or full suites were run.
