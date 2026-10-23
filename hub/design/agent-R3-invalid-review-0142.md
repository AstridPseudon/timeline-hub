# PASS — Agent R3 invalid-source check

The exact base is `73df0a99bec2264777cce15b0de7277b98e575d` (`tl/agt-R3-current-forward-0049`). The existing R3 repair is correct; no production code change was made.

At `astrid/sdk/timeline/_doc_patch.py:363-366`, a wrong patch `before` raises `previous_value_mismatch`. The existing classifier in `astrid/sdk/timeline/_commit_errors.py:65-71,90-110` treats that as invalid only at the original base and produces HTTP 422 / `validation_error` with `status=invalid`, code/reason, path, current head, hint, and suggested command. The outer production path in `astrid/sdk/timeline/commit.py:1114-1127` preserves those fields. During rebase, `commit.py:1058-1073` maps a changed replay guard to a dependency/selection conflict; a prior history write can also be rejected as `value_conflict` by the existing rebase guard.

The added direct tests in `tests/sdk/test_timeline_commit_v2_errors.py` prove both boundaries: original-base wrong `before` is 422 and leaves head/accepted/prepared state untouched; a real changed-head replay is 409 conflict and does not accept a second write.

Evidence:

- Targeted pytest with `ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-27f0306b` and matching `PYTHONPATH`: `93 passed` (`tests/sdk/test_timeline_commit_v2_errors.py` and `tests/editing_conformance/test_doc_patch_v2.py`).
- Scoped Ruff: passed.
- Private mypy on `_commit_errors.py` and `commit.py`: passed, 2 files, no issues.
- `git diff --check`: passed.

This is not a live Runtime wire claim. The tests use the Agent provider and `DetachedPort`; they do not qualify Runtime HTTP/schema replies or the complete v2 accepted/merged/preview envelope. No Runtime files, schema, generated files, or shared dependencies were changed. The Runtime lane should repeat its bounded native run against this exact Agent source once its independent Runtime repairs are available.
