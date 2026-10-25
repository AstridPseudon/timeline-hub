# D127 report

- Imported donor test byte-exactly into [p2-runtime-phase-bootstrap.test.ts](/home/user/work/wt/app-D127-reviewed-clean-bootstrap-1731/tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts).
- Baseline: `d4e5284…`; donor: `54c91d77…`, tree `7be73e2c…`.
- Target SHA256 matches donor: `92586e7f…`; only the assigned file differs.
- Branch: `tl/app-D127-reviewed-clean-bootstrap-1731`; HEAD/tree: `d4e5284…` / `5efca939…` (uncommitted; commit message prepared).
- Source review reference: independent D127 lifecycle review `app-D127-lifecycle-final-review-1723`, Source PASS.

Tests:

- Scoped ESLint: PASS.
- D127 offline validators: 2 passed, 3 skipped.
- Real `P2 Runtime observer bootstrap`: PASS, exit 0; 1 passed, 4 skipped, 0 failed.
- Helper `4ee0424b…`, Agent `070dfc…`, Runtime `ab1e4f…`, supported Agent Python supplied via `ASTRID_PYTHON`.
- Capture: 102 events, expected phases, two completed summaries, `0600`, no checked private markers.
- No retries, full suites, D78 rerun, or integration/browser/native suites.

Evidence and custody files were written to the assigned worker directory. `DONE` created.