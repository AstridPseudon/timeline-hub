## Result: FAIL — V1 copy audit

- Candidate: `25991306f3e432a694766ab7fb795a93485fad12`, tree `b731cddae1fbb204fff5f5c9897785e80b522b56`.
- Runtime source: `691a9436ce3dbf2dcbfeaf959c85143c165fe4e2`.
- All 15 mapped files match producer bytes and hashes.
- Normal refresh, lock check, manifest check, artifact tests, clean-install schema parity, production compiled-schema probe, and caller import passed.
- Full v2 DTO shape is unchanged; `WorkspaceClient` still calls the generated client.

Blocking finding:

- Candidate 36-test lane: **35 passed, 1 failed**.
- Failure: `tests/timeline/test_timeline_roundtrip_fixture.py::test_allowlist_parity_with_runtime_vendored_schema`
- Agent `_TIMELINE_TOP_ALLOWED` omits the newly canonical top-level `meta`; current integration baseline passes all 36.
- Clip and track `meta` are likewise rejected by Agent allowlists.

Other checks:

- Ruff: 53 inherited generated-file diagnostics; no product changes made.
- Mypy: 60 inherited diagnostics.
- `git diff --check`: passed.
- No full/browser/farm suites run.

No product files were changed. `DONE` and commit message were written. Recommend a follow-up allowlist/meta seam fix, then rerun the 36-test lane; do not queue this as a PASS yet.