## Report

Implemented candidate provenance fix in [provenance.py](/home/user/work/wt/vw-m1-agent-label-review/astrid/packs/rendering/actions/timeline_visualize/provenance.py) and tests.

- Candidate labels now use only admitted marker `base_parent`.
- Managed and composed candidates no longer treat candidate revision `C1` as committed.
- Missing bases remain explicitly unsaved candidates.
- Conflicting bases fail closed.
- Added tests for real managed/composed marker shapes and `authoring_preview` detection.

Tests:

```text
97 passed, 1 warning
git diff --check: passed
```

Used the shared venv at `/home/user/work/venv-agent/bin/python`; the relative `venv-agent/bin/python` was absent.

No full suite run. Commit message written; no commit created.