# D118d independent protected review commands and results

## Admission and exact behavioral proof

- `df -B1 /tmp` at dispatch: `5055291392` bytes available; this cleared the required `5000000000`-byte fresh-review floor.
- Exact mandated nine-node command against final source `e02180cedafa581bc8105d77341456b8b1c50b5b` and Runtime pin `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`: **FAIL**, exit 1.
- JUnit summary: `tests=9`, `errors=9`, `failures=0`, `skipped=0`.
- Safe first failure: `tests/sdk/test_timeline_capture_projection.py:303`, `source_shot["revision_id"]`, `KeyError: 'revision_id'`.
- The registered `doc.patch` call was not reached. Private raw outputs: `evidence/own9.xml` and `evidence/own9.log`.
- Post-run free space: `5023059968` bytes, above the ongoing `4000000000`-byte stop floor.

## Source custody and conservation

- `git diff --name-status 20177e66564f9f91735ed1a11bac821682d60edf e02180ced -- tests/sdk/test_timeline_capture_projection.py` — one modified assigned test file.
- `git diff --check` — PASS.
- `git diff --quiet 28081580dc95f02470d82ad81b826335d8e4bd09 a92c6afe0ccd2359e952fc534788d1fce2169049 -- tests/sdk/test_timeline_capture_projection.py` — PASS; candidate exactly matches historical 2808 setup.
- Commit lineage — PASS: candidate parent is base; final parent is candidate; both commits have author `Claude <noreply@anthropic.com>`.
- Final file SHA-256: `8747fa62ef628a9c25455fe30876a008ebf54b3b22d575c697c2f6893ca276da`.
- Final tree: `b83fcf6cbb2b9bd8620a8b203ba8d0419fa8c354`; base tree: `68433c5f77be90063b1f43d3e8f1407346a50675`; candidate tree: `4902fa8b7cb96d379a2feb276ac76896f59c1967`.
- Independent AST guard — PASS: all test-function ASTs equal across base/candidate/final; original test assertion count remains 43; candidate/final `saved_closure` AST and original fixture tail are equal.
- Final-vs-candidate diff — PASS: only `_saved_document()` field projection changed (+9/-3).
- Worktree status — clean after review; no source or product edits.

## Canonical/provider source review

- `_verify_document()` keeps `project_id` and `timeline_id` at top-level canonical scope and rejects scoped child rows; `bundle_from_document()` adds scope only when opening the authoring bundle.
- The genuine current Runtime reader and final `_saved_document()` use the same shot fields (`shot_id`, `revision_id`, `internal_timeline_revision_id`, `content_digest`, `payload`) and internal fields (`timeline_id`, `revision_id`, `content_digest`, `payload`).
- The current occurrence-create path initializes `payload.items` to `[]`; the added registered `doc.patch` is therefore the intended original physical item admission. Source review confirms the route is the registered Runtime provider, but execution did not reach it.
- Runtime pin `/home/user/work/wt/rt-pin-5e9ad1c6`: clean at commit `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`, tree `de2954a0ceadb4455903d9abdfec3b773318a50f`.
- `git cat-file -e 92443771676ef2bbb547d0a103d708fa8bec4c63:tests/sdk/test_timeline_capture_projection.py` — expected absence, status 128.

## Static checks

- `/home/user/work/venv-agent/bin/ruff check tests/sdk/test_timeline_capture_projection.py` — PASS (`All checks passed!`).
- `/home/user/work/venv-agent/bin/mypy --cache-dir /tmp/d118d-final-review-1558/mypy --follow-imports=skip tests/sdk/test_timeline_capture_projection.py` — PASS (`Success: no issues found in 1 source file`).
- `PYTHONPYCACHEPREFIX=/tmp/d118d-final-review-1558/pycache /home/user/work/venv-agent/bin/python -m py_compile tests/sdk/test_timeline_capture_projection.py` — PASS.
- `git diff --check` — PASS.

## Environment note

- The first static-check wrapper could not use the prescribed worker `tmpdir` because that path is an existing 18-byte file, not a directory. No source was changed; the exact checks were rerun with private `/tmp/d118d-final-review-1558` caches and passed.

## Verdict

**FAIL — exact-unapplied setup seam.** This is the second FAIL in the protected sequence; escalate to **HARDSol**, with no further Luna author and no speculative approval.
