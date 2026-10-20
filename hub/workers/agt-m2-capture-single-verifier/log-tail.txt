`project_capture` no longer re-verifies the preview, and the two prior-revision loops are now one pass. The new Runtime-authority test and the capture goldens did not run, because the integration fixtures fail at setup on current Runtime.

**Size**: 3 files changed, +36 / −114 lines. `commit.py` is +6 / −49 (the re-verify block was about 43 lines; the fold saves about 6).

**What changed**
- **`astrid/sdk/timeline/commit.py`, `project_capture`**: the field-by-field comparison of the preview against the saved base and the `preview_authoring_candidate` recompute are gone. It now reads `preview["publication"]`, the candidate base parent, and the two digests directly. Runtime's `_candidate_document` is the single verifier. The `bundle_from_document(document)` call stays, so an inconsistent saved closure is still refused, and I removed the now-unused import.
- **`astrid/sdk/timeline/commit.py`, `document_from_bundle`**: the "reuse prior revision" logic was the opened-source check followed by a separate loop over the historical bundles. It is now one `next(...)` over `[historical docs..., source]`, so a historical match still wins, as before.
- **Tests**: I deleted three tests in `tests/sdk/test_timeline_capture_projection.py` that exercised the removed re-verify:
  - `test_inconsistent_candidate_refuses_even_with_recomputed_preview` (17 cases)
  - `test_json_distinct_base_values_are_not_equal`
  - `test_reused_candidate_pin_is_compared_with_verified_image`

  Their replacement is `test_forged_candidate_is_refused_by_runtime_authority` in `tests/sdk/test_capture_source_runtime.py`. It forges the forwarded preview and expects Runtime to refuse it at `create_task`. The cases are `kind`, `head`, `candidate_digest`, `publication_digest`, `publication`, `candidate_after_freeze`, `base_parent`, `project_id` and `timeline_id`.
- **Goldens**: `test_real_saved_projection_config_registry_and_full_pins_golden` and `test_real_saved_entire_expansion_golden` are untouched, so the golden that `project_capture` equals `_project_exact_parent_head` stays.

**Tests**
- The targeted request returned `1703 passed, 4 skipped, 176 deselected, 5 xfailed` (exit 0, 129s):
  `request-test agt-m2-capture-single-verifier targeted --files "tests/editing_conformance tests/timeline tests/sdk/test_timeline_capture_projection.py tests/sdk/test_capture_source_runtime.py"`
- The 176 deselected are the `integration`-marked tests, which includes the capture goldens, the new test and the existing candidate-vs-opener test.
- I ran those by hand with `-m integration` and `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime`. Every fixture fails at setup with `RetiredRouteError: legacy timeline writes are retired` from `publish_parent_composition`. The fixture is unchanged by this work and fails before reaching any code I touched.
- The test service rejects `-m` in `--files`, so there was no way to run these there.

**Gaps and risks**
- The new Runtime-authority test and the goldens did not run, so they are unverified. The new test shares the broken fixture. It needs a fixture that publishes through `commitTimeline`, or a Runtime commit that still allows legacy publish.
- The fold is covered by the existing `tests/timeline` and `tests/editing_conformance` reuse tests, which pass unchanged.
- **Weaker coverage:** Runtime's `_candidate_document` checks the preview kind, both digests, scope, base binding and closure. It does not check that the candidate's base payloads, placements, `source_mapping` and child bases match the saved base, or that the publication was derived from the candidate. Those Agent-side checks are gone, with no equivalent in the new test. Runtime should add them if they matter.

The commit message is in `commit-msg` and `DONE` is created.
