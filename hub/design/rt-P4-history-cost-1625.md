## Report

- Profiled the genuine retained sequential capture:
  - 54 `CanonicalDocument` validations plus 2 `Recorder` validations.
  - Schema validation dominated (~0.23–0.26s); finite-JSON traversal was ~0.009–0.013s.
  - Immutable registry/validator caching already exists.
  - Registry-crawl/direct-definition experiments showed no reliable end-to-end improvement.
- No production change was justified without violating D47’s no validated-result caching rule.
- Added focused deterministic tests in [tests/test_timeline_validation_cost.py](/home/user/work/wt/rt-P4-history-cost-1625/tests/test_timeline_validation_cost.py).

Tests:

- Focused: `3 passed`
- Required suite with integration Agent checkout: `147 passed in 107.92s`
- Ruff: passed
- Pyright new test: passed
- Compile and diff checks: passed

The frozen R4 Agent branch lacked `astrid.sdk.timeline.commit`; required tests passed using read-only `/home/user/work/agent`.

Commit message written; `DONE` marker created. Recommended next seam, if needed, is the repeated `_capture_document_images` caller in `timeline_commit_auth.py`, requiring separate D47 review.