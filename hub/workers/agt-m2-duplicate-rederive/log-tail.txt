`occurrence.duplicate` now re-derives only the copy's root `stable_deep_link` and `output_identity` against the compiled destination, and the strict xfail test now passes. I did not run ruff, mypy or `make check`.

**Change**
- **Code:** I added `_rederive_root_identity` in `astrid/core/timeline/authoring_bundle.py`. It runs in the compile step that sets `placement["shot_revision_id"]`.
- **Scope:** it runs only for placements with no base placement, so existing occurrences are never rewritten. It rewrites a field only if the row already carries it. Everything else on the copied row is untouched.
- **Factories:** it calls the existing `stable_occurrence_deep_link` and `stable_output_identity`. There is no suffix remapper and no change to the closed call.
- **Test:** I renamed the xfail test to `test_copy_rederives_only_root_identity_against_compiled_destination` and removed the marker. It now reads the compiled parent row and closure from `document_from_bundle`. It checks:
  - the two new values match the factories, using the compiled destination revision;
  - that revision is in the closure;
  - the source's own two fields are unchanged;
  - historical `output_records` and the other row fields are identical to the source.

**Where `parent_document_id` comes from.** No new input is invented. The occurrence rows already carry `parent_document_id`, and the contract validator requires it to equal the project `document_id`. The test fixture rows don't carry it, so the fallback is `timeline_id`. That is the existing default in `shot_composition_migration.py:377` and `invocation.py:1388`. I did not add a field to the authoring bundle, so there is no schema change. If you want `parent_document_id` carried explicitly in the bundle anyway, say so.

**Behaviour to be aware of.** Any brand-new occurrence whose row carries those two fields gets them re-derived, not just duplicates. A `placement.create` row would be affected the same way, but those rows normally don't carry them.

**Tests** (central test service, targeted only):
- `test_recipe_occurrence_duplicate.py` and `test_recipe_m2_placement_create_unplace.py`: 70 passed, no xfail left.
- `tests/editing_conformance tests/timeline`: 1680 passed, 4 skipped, 137 deselected.

I also updated `design/m2-occurrence-duplicate.md` in the orch directory, and wrote the commit message and `DONE` marker.
