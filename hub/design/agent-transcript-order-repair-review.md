# Transcript source-order repair review

## Disposition

**APPROVE the source-only repair at Agent commit `85e3bef7103680fdf96a8f123717bccbd95df7f3`, tree `c8e1d998a5c51b26a5dca525a9b20355290e93c2`.** No data-safety defect was found in the reviewed diff. This approves the source change for adoption; it does not qualify the normal Runtime-Door node below.

## Review findings

- The repair uses the existing `parent.config.bundle.itemsBySchemaRef` carrier and the existing `transcript.source-items` selection. It does not add a schema, DTO, history writer, record field, or second source authority.
- Existing owned rows are keyed by the existing owner/source/item identity. A row is retained in its original position only when the projected fields match. New projected rows are appended after the retained original array, so the old `[old-V1, unrelated-one, unrelated-two]` order is restored by the existing inverse write rather than guessed or appended.
- `_known_projection_matches` checks every projected field recursively, including list length and order, while allowing extra authored keys on the existing row. Therefore unknown fields and `null`/`false`/other opaque values survive. The copied source map also preserves sibling schema collections and map-level fields.
- The final word-ID adjustment is bounded: `_source_item_matches_projection` relaxes only `payload.words[*].id`, and only when the old/new word mappings have identical key sets and all other values match positionally. It does not accept changed text, timing, word order, word shape, segment fields, owner, provenance, or item identity. The retained row supplies its original stable word IDs and opaque data.
- Existing source-map read/write guards, the ordered source selection, exact new/previous transcript dependencies, and the unchanged generic inverse/intervening-write/ABA machinery remain in force. No whole-array authority or weakened inverse/pin guard was introduced.

## Evidence run in this review

Runtime imports used the approved compatible checkout `/home/user/work/wt/rt-pin-3dcae183`; no shared dependency was changed.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-3dcae183" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/editing_conformance/test_recipe_film_transcript_association.py::test_serialized_replacement_inverse_restores_source_item_order \
  tests/editing_conformance/test_recipe_film_transcript_association.py::test_association_uses_guarded_inverse_and_replay \
  tests/editing_conformance/test_recipe_film_transcript_association.py::test_normal_serialization_reload_preserves_nested_carrier_through_inverse_and_redo \
  tests/editing_conformance/test_recipe_film_transcript_association.py::test_replacement_requires_and_retains_exact_prior_pin \
  tests/editing_conformance/test_inverse_clear_batches.py::test_noop_batch_allows_equal_state_rebase_and_keeps_inverse_publication_guards \
  tests/editing_conformance/test_inverse_clear_batches.py::test_leaf_batch_preserves_disjoint_concurrent_edits_and_refuses_guarded_changes \
  tests/editing_conformance/test_recipe_scalar_commands.py::test_inverse_refuses_same_batch_unchanged_or_aba_scalar_write \
  tests/editing_conformance/test_recipe_scalar_commands.py::test_inverse_allows_later_explicit_write_and_disjoint_prior_stages
=> 16 passed in 1.73s

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/ruff check \
  astrid/sdk/timeline/native_transcript_association.py \
  tests/editing_conformance/test_recipe_film_transcript_association.py
=> All checks passed

git diff --check
=> passed
```

The selected tests covered the new serialized source-order inverse regression, nested serialization reload/inverse/redo, exact prior-pin retention, and nearest inverse/ABA controls. No product or test assertion was changed by this review.

An initial identical local invocation without the Runtime checkout on
`PYTHONPATH` collected no tests and failed with
`ModuleNotFoundError: runtime_protocol`; the successful command above used the
approved checkout. No old52/59/110, full, HTTP, browser, or normal-Door repeat
was run.

## Remaining qualification boundary

The exact bounded normal-Door node remains **unqualified**:

```text
retained-transcript3dca-integration-nodes
  --files tests/editing_conformance/test_gate1_transcript_normal_door.py
  ::test_transcript_association_normal_door_reload_restart_inverse_redo
```

Its prior run failed before this final word-ID predicate adjustment, at inverse source ordering, and therefore never reached redo. This review did not repeat the normal Door/HTTP/browser run per the task boundary. The source approval should be paired with one later rerun of that exact node before claiming native Door qualification.

