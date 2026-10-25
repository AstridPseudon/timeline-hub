# D134 D100 applicability validation

## Read-only source checks

- `python3` JSON parse/shape check for `evidence/{verdict.json,source-manifest.json,predicate-map.json}` — PASS.
- Source hash/AST script over the six cohort files and the original
  `_create_fixture` authority — PASS. Exact SHA-256, byte counts, assertion
  counts, selector function AST hashes, and shared input/create AST hashes all
  match `source-manifest.json`.
- Predicate-map conservation script — PASS: six cohort counts sum to exactly
  30 and the selector list contains exactly 30 entries.
- `PYTHONPYCACHEPREFIX=/tmp/w-a5c352dc68/d134-applicability-2056/pycache
  python3 -m py_compile` over the six cohort files plus
  `test_commit_runtime_occurrence_media.py` — PASS.
- `ruff check --no-cache` over the six cohort files — PASS (`All checks
  passed!`).
- `mypy --cache-dir=/tmp/w-a5c352dc68/d134-applicability-2056/mypy-cache` over
  `test_recipe_m2_shared_auto_placement.py`,
  `test_recipe_m2_shot_pool.py`, and `test_recipe_occurrence_media.py` — PASS
  (`Success: no issues found in 3 source files`). These are the managed16
  source-authority files carrying the shared input and caller paths.
- `git diff --check a30e74e901a28b39c28facba3deb00d76f186e23 --` — PASS.
- `git diff --quiet a30e74e901a28b39c28facba3deb00d76f186e23 --` on all six
  cohort files — PASS; no source/test delta.
- `git status --short --branch` — PASS; clean branch
  `tl/app-D134-D100-applicability-2056`.

## Reused prior qualification evidence

- Held D100 product/source state `9486cbb…` / `42040a9…` and product SHA-256
  `018f174004bf9b9c275aa23ef6ceb432ce9d7294d71e3024f96353c25fa808a3` were
  read from the existing security and product27 evidence manifests.
- Existing D100 source-security review is recorded as
  `PASS_SOURCE_SECURITY_BEHAVIOR_NOTRUN`; existing product27 review is recorded
  as source custody PASS with the 27-test candidate pass.
- Current joined original9 remains pending after its recorded setup boundary;
  no current original9 run or D134 behavior run was performed here.

## Explicitly not run

No pytest, Runtime provider/service, socket, browser, native, acquisition,
fixture rewrite, unchanged original body, P2/P4, family, core, profile,
collector, or full suite was run. No skipped, filtered, wrapper-only, or
historical event was counted as a pass. No behavior or setup credit is claimed.

At validation time `/tmp` reported 5,503,811,584 available bytes. The brief
prohibited behavior execution for this task, so that capacity was not used to
start a service or test run.
