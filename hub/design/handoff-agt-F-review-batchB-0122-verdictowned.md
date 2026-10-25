# FAIL — owned-move protected review

## Scope

- Candidate: `tl/agt-F-owned-move-return-0115`, revision `75a656dafac44f71a01576256338f3121b9fc451`
- Compared with the candidate's true original baseline: `43bc0b71922e1791b12590e2132ddde1063d25b2`
- Reviewed file only: `tests/editing_conformance/test_owned_move_publish_runtime.py`
- Candidate file SHA-256: `15d144444a39f5d1a7f93ae47155dc470ae3f89b921ecd75bc23a43387667f12`
- Baseline file SHA-256: `2f83ea67363832a8f260c818ecdb79c92ab4298594d1df98f2c3d407f0a8223b`

## Verdict and bounded finding

**FAIL.** The candidate's intended semantic `occurrence.delete` repair is unreachable because `_commit_parent_variant` reads occurrences from the wrong bundle location.

`bundle_from_document()` calls `open_authoring_bundle()`. In `astrid/core/timeline/authoring_bundle.py`, that routine removes `occurrences` from the copied parent payload and materializes them under `placements` (the relevant source is lines 400–402). The candidate nevertheless indexes `before['parent']['occurrences']` at its original-order and requested-order reads. A real call therefore reaches a missing key before the loop can invoke the registered `capture_occurrence_delete` helper. The candidate cannot establish the required physical-source-preserving semantic delete baseline, regardless of the helper's otherwise appropriate registration.

This is a source-trace failure, not a weakened expectation or a pooled result. No merge is authorized. The bounded repair is to read the actual occurrence representation returned by `bundle_from_document()` and then re-review the cumulative delta; I did not modify the candidate.

## Structural evidence

- All 15 test function ASTs are retained with no added or removed test definitions; only `_commit_parent_variant` changes.
- The prior Batch A generic-emitter membership failure is not being treated as repaired merely because a semantic helper was added: the new bundle-location failure prevents that path from running.
- No test, collection, helper, fixture, service, or browser execution was performed.

## Checks

- In-memory compile of baseline and candidate: passed.
- Scoped Ruff on baseline and candidate: passed.
- Scoped mypy under Python 3.13 with `--follow-imports=silent` and private cache: passed for baseline and candidate.
- `git diff --check`: passed.

Static PASS is not closure; later functional proof remains owed after a bounded source repair.
