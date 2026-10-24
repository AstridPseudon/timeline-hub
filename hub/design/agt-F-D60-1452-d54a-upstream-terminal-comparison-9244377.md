# D54a upstream terminal comparison: Agent 9244377

Evidence-only comparison of the exact 276-selector D54a set against the one retained terminal upstream run. No test rerun was performed; the original 267 census was not blended with this 276-selector set.

## Terminal custody

- Service: `agt-F-D60-baseline-amend-1336-full-upstream-final-9244377-1024135120-1621`
- Status/exit/bench lease: `fail` / `1` / `complete`
- Durable JUnit: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D60-snapshot-return-1342/evidence/upstream-full-9244377.xml`
- JUnit SHA-256: `2941565205663912985f766210bfead7db42264976fabee7dc899d03d4f4657f`
- Source: Agent `92443771676ef2bbb547d0a103d708fa8bec4c63`, tree `a81a8c7f262e4416dcdefc0720fd760e026d766b`
- Runtime: `becfe6db88b2cc034dba3fafa6c050117cdf2b06`, tree `7edc08e3fe94edcbc8ef695c479f4de301789b89`
- Environment facts are retained from service preflight: Node `v20.19.4`, `/home/user/work/venv-agent/bin/python`, runtime `/home/user/work/runtime`, and the pinned Remotion profile. Module-origin and clean-tree guards were asserted by the service.

The XML parses completely and ends with `</testsuites>`. XML testcase counts are 12,396 passed, 91 failed, 14 errors, 16 skipped; its root total is 13,083 after 566 subtests. The service summary independently reports 12,396 passed, 91 failed, 14 errors, 16 skipped, 566 subtests in 3,563.50 seconds. These counts agree.

## Exact 276 comparison

- Scope: 159 core + 117 non-core = 276.
- Exact selector matches: 75 (66 FAILED, 9 PASSED).
- Missing/renamed/uncollected upstream selectors: 201 UNKNOWN.
- No absent selector is treated as PASS.
- Current authoritative rollup remains 162 PASS, 112 OPEN, 2 DEFERRED; core is 152 PASS, 5 OPEN, 2 DEFERRED.

The complete row set is `d54a-comparison-rows.tsv`; the prepared comparator output is `upstream-comparison-9244377.json`.

## Current core-open assignments

All five current core-open selectors remain unproven as current regressions because their upstream selector is absent. Four retain current FAIL (the D61 fork cases); the D13 case retains current UNKNOWN. Exact worker-ready selectors:

- `tests/editing_conformance/test_provider_occurrence_fork.py::test_v2_registered_fork_reply_physical_effects_step_reads_and_undo[True]`
- `tests/editing_conformance/test_provider_occurrence_fork.py::test_disjoint_head_merge_and_preview_keep_other_edit`
- `tests/editing_conformance/test_recipe_occurrence_fork.py::test_reload_undo_redo_exact_and_replay[1]`
- `tests/editing_conformance/test_recipe_occurrence_fork.py::test_reload_undo_redo_exact_and_replay[2]`
- `tests/packs/video_editing/test_runtime_publication_chain.py::test_d13_installed_native_preflight`

These are evidence-bound assignments, not cause claims. The Agent 68e82 proposal-inverse fix is outside this exact 276 set; the newer two forward ABI1 cases are excluded.

## Historical contrasts and limits

Nine selectors are upstream PASS while the old checkpoint was FAIL. Eight are historical checkpoint contrasts without retained current FAIL evidence. One (`tests/sdk/test_timeline_persistence.py::test_publish_after_a_restart_merges_other_clips_onto_the_moved_head`) has retained current FAIL but is authoritative DEFERRED; it is recorded as a deferred checkpoint contrast, not relabeled as a regression. Therefore no current regression is proven.

The 66 matched upstream failures are preserved as status matches, but exact paired cause identity was not retained for both runs, so pre-existing is not asserted solely from status. Existing env and deferred categories and their evidence references are preserved unchanged; no known gap is guessed.

## Validation

- Prepared `compare_junit.py` ran against the retained XML: exit `2` because 201 exact selectors are UNKNOWN, as required by the lossless guard.
- XML parse/count/custody assertions: PASS.
- Exact 276 order/identity/scope/count assertions: PASS.
- No product, test, registry, generated, client, lock, source, or dependency edits; no rerun, install, browser, HTTP, or child acquisition.
