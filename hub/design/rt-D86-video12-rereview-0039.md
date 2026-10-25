## FAIL_SOURCE — F-D86 video12

Reviewed `9f884cdf518843d9ae4c3f0316e79f642f8642ce`.

The shared-topology defect is repaired: `occ-a` and `occ-b` use the genuine registered `capture_occurrence_place_shared` path and retain the same physical shot identity.

Blocking finding: the semantic bootstrap drops original setup data that the pre-migration fixture preserved, including parent/shot/occurrence/internal opaque fields, parent clips/config structure, shot metadata, and the new registry binding’s opaque value. Existing assertions compare against this reduced baseline and cannot detect the loss.

Checks:

- Baseline/candidate in-memory compile and AST conservation: PASS.
- All 12 selectors preserved; recipe byte-identical.
- Candidate/baseline Ruff: PASS.
- Candidate/baseline mypy: PASS.
- `git diff --check`: PASS.
- Prohibited-path scan: clean.

No pytest, collection, fixture/helper execution, service, build, browser, profile, or full suite was run. No source changes were made.

Author merge is not recommended until the original opaque/source topology is preserved through an existing supported path. `DONE` and commit message were recorded.