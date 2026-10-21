# RT03 accepted unplaced-reference projection

Status: implementation pending harness commit and independent custody/data-safety review.

This Runtime change is based exactly on `f53bf588bf70b090ce8e0bed5ccb7d91157771b6`.
It consumes the reciprocal Agent source contract at
`d1f5f7824a5ede5587088735fad6e6870f0b95db` and does not alter the Agent
carrier, the existing placed-occurrence projector, the catalog, or any DTO,
table, endpoint, or artifact manifest.

The acceptance transaction derives `config.app.astrid.timeline_references` only
after normal closure and raw-media custody validation. Each closed v1 leaf must
have role `source`, an exact matching media pin in the accepted manifest, and a
lowercase equal SHA-256 identity. Runtime projects the resulting map into the
existing `timeline_references` rows and `timeline_revisions.references_json`.
Unrelated live rows are retained. A global occupied ID is refused unless the
immediately previous accepted parent carrier and exact live row prove ownership;
removal uses the same proof and guards state deletion by the exact live row.

The source tests use the approved ephemeral trusted acceptance setup and the
existing `raw_media_info` commit-port capture. They demonstrate Runtime
projection behavior, not qualification of the normal Agent provider's source
generation path. The original strict positive remains open until that paired
normal-provider path is available.

Evidence from this worktree:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:$PWD/tests" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider --timeout=60 tests/test_timeline_unplaced_reference_projection.py
4 passed in 1.34s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:$PWD/tests" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider --timeout=60 tests/test_timeline_commit_closure_invariants.py tests/test_timeline_history_boundaries.py -k 'not http' tests/test_timeline_raw_capture.py tests/test_timeline_unplaced_reference_projection.py
21 passed, 4 deselected in 4.46s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:$PWD/tests" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider --timeout=60 tests/test_timeline_catalog_history_integration.py tests/test_timeline_projection_occupancy.py tests/test_timeline_commit_restore_integration.py
17 passed, 12 deselected in 2.81s
```

An initial combined closure/history invocation also collected four HTTP
history cases; the sandbox refused localhost socket creation with
`PermissionError: [Errno 1] Operation not permitted`. Those cases are not
counted as product evidence; the non-HTTP closure/history neighbors above are
the direct local result. No full, render, browser, or normal-provider source
generation suite was run.
