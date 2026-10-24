Implemented the D56 security correction.

- Retained redo roots now require accepted inverse-stage provenance, exact ordered source ownership, and digest-verified identity. Equal-byte successor fallback is removed.
- Added two strict custody negatives.
- Production path remains mounted through `create_runtime_commit_service().commit()`.

Tests/checks:

- Author cohort: `336 passed`
- Non-managed neighbors: `199 passed`
- Ruff, mypy, vendor lock, artifact manifest, `git diff --check`: passed
- Prior durable comparison: `327 passed/7 failed` → `334 passed/0 failed`, zero lost passes, 17 strict negatives.
- Four managed-realm cases were unavailable due missing external dependencies; no managed/full/HTTP/gate runs.

Changed: [_commit_patch.py](/home/user/work/wt/agt-R2-redo-security-review-1234/astrid/sdk/timeline/_commit_patch.py), [test_redo_retained_boundaries.py](/home/user/work/wt/agt-R2-redo-security-review-1234/tests/editing_conformance/test_redo_retained_boundaries.py).

Commit message and `DONE` marker written.