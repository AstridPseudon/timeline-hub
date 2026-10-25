# D118d independent protected review

Verdict: **FAIL — exact unapplied setup seam**

The exact pinned own9 run was executed with 5,089,345,536 bytes free. All 9 nodes failed during setup at `tests/sdk/test_timeline_capture_projection.py:284`:

`bundle_from_document(document)` → `AuthoringBundleError: project scope belongs on the canonical document`

`_saved_document()` retains `project_id` on revision rows, while `bundle_from_document()` correctly rejects scoped rows. Therefore the new registered `doc.patch` is never reached, so canonical source-item provenance is unproven.

Static/source review passed:

- Only the assigned test file changed: +52/-0.
- Original assertions: 43 preserved; one new setup-status assertion.
- Original fixture tail, decorators, parameters, inputs, and golden values unchanged.
- Historical commit `28081580dc95f02470d82ad81b826335d8e4bd09` matches exactly.
- Runtime pin clean: `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`, tree `de2954…`.
- D120 upstream target absent at `92443771676ef2bbb547d0a103d708fa8bec4c63`.

Checks:

- Ruff: PASS
- Mypy: PASS
- Py_compile: PASS
- `git diff --check`: PASS
- Own9: FAIL, 9 setup errors, exit 1

Evidence:

- [verdict.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D118d-projection-protected-review-1545/evidence/verdict.json)
- [verdict.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D118d-projection-protected-review-1545/evidence/verdict.md)
- [commands-results.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D118d-projection-protected-review-1545/evidence/commands-results.md)

No source or product files were modified.