# F-D89 protected review — Projection9

Verdict: `PASS_SOURCE` for `4a8ecdf7d747969244dd0a277da1dfe0498f6544` only.
This is an independent source/static verdict, not behavioral closure and not pooled with M2.

## Identity and scope

- Candidate: `4a8ecdf7d747969244dd0a277da1dfe0498f6544`, `test(timeline): F-D86 restore projection opaque fixture baseline`.
- Own parent/authorbase: `6386c700ee56264aebe12da4558ac74dda0d60ca`.
- Candidate diff: only `tests/sdk/test_timeline_capture_projection.py`, 52 insertions and 0 deletions.
- Candidate blob: `91047638576673c9cbb65780d7364b9a4d5245ec40b19cbd52af5c3381a41105`.
- No production/generated/schema/pin/ledger/credential or neighboring test file changed.

The independent shared fixture dependency is tracked separately: occurrence48 birth/reload is `095177db7903075eaa9cae35308b28492a74a008`, adopted by normal home `25c1e182614145c54decb07afc384180cc8e7e34`. Its corrected helper blob is `b42079e3b350212109b63aa86bd0eb145444843b`; this Projection9 candidate itself does not import that helper. The occurrence48 review independently reported PASS; it is not used as Projection9 behavioral proof.

## Before/after input and topology map

Before, `saved_closure` reads the parent, shot revisions, internal timeline revisions, and dependency manifest through the current Runtime source reader, opens an authoring bundle, duplicates the source shot into `shot-z`/`occ-z` and `shot-a`/`occ-a`, removes the source, adds authored metadata, and publishes through `_RuntimeAuthoringWriter.commit_timeline` and the registered current provider. The fixture failed during duplication when the real internal source lacked the required opaque timeline carrier.

After, the same real Runtime document and provider path is used, but the candidate explicitly restores the complete authored-extension shape before duplication: parent/config/registry fields; occurrence placement, transform, muted, provenance, and future fields; shot metadata, opaque shot, pools, selected variants, provenance, generation inputs, text bindings, and item metadata; internal effects/audio/layout/assets, opaque timeline/registry, track, and clip fields. The strict source identity reads remain direct (`source_internal['registry']['assets']` and `source_internal['clips'][0]`). The publication still creates the same topology—parent → `occ-z`/`occ-a` → `shot-z`/`shot-a` → internal timelines—then removes the original source and verifies the current provider’s canonical projection against the managed current projector.

The added `setdefault`/empty-items conditional are fixture augmentation statements, not replacements of existing assertion or source-reader indexing. They are the bounded point to recheck if the gate is interpreted as forbidding any defaulting in added fixture setup; no existing dropped-input path was hidden or weakened in the diff.

## Predicate/AST preservation

All 11 top-level `test_` definitions compare exactly between parent and candidate ASTs. Their original names, decorators, parameter values, assertion bodies, raises contexts, and branches are unchanged:

`test_capture_candidate_inputs_exact_pure_detached_golden`, `test_projection_is_detached_json_deterministic_without_io`, `test_inconsistent_saved_closure_refuses`, `test_inconsistent_candidate_refuses_even_with_recomputed_preview`, `test_json_distinct_base_values_are_not_equal`, `test_reused_candidate_pin_is_compared_with_verified_image`, `test_capture_method_imports_and_runs_without_renderer_or_runtime`, `test_real_saved_projection_config_registry_and_full_pins_golden`, `test_real_saved_entire_expansion_golden`, `test_saved_canonical_images_preserve_authored_fields_pins_order_and_read_rows`, `test_real_candidate_matches_sdk_opener_exactly`.

The AST census is 43 assertions, 4 `pytest.raises` contexts, and 27 branch nodes in both parent and candidate. The 9 original Projection9 predicates/selector cases are retained; no direct lookup was replaced and no `.get()`/default was substituted into an existing predicate.

## Checks

Passed:

- in-memory `compile()` for exact baseline and candidate sources;
- scoped Ruff, baseline from `git show` and candidate;
- scoped mypy, baseline via `--shadow-file` and candidate;
- `git diff --check`.

No pytest, collection, test/function/fixture execution, Runtime service, build, browser, render, or probe was run. The source/static PASS does not establish the real Runtime/provider publication or projection behavior. Functional MAIN proof remains mandatory.

## Handoff

Request the normal original-author fixture merge and verify the exact home/integration blob before behavioral qualification. Never merge a review branch. Keep this verdict separate from M2 and do not pool their PASS states.
