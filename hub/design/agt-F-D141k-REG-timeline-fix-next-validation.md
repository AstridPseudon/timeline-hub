# Validation

## Targeted nodes

Command (with the reproduction’s pinned Runtime source origin on `PYTHONPATH`):

```text
PYTHONPATH=/home/user/work/wt/agt-F-D141k-REG-timeline-fix-next:/home/user/work/wt/rt-pin-6a011d58 /home/user/work/venv-agent/bin/python -m pytest -q -n3 -o addopts= -p no:cacheprovider --timeout=45 --junitxml=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141k-REG-timeline-fix-next/evidence/private/targeted.xml tests/timeline/test_authoring_feedback.py::test_document_publish_stdout_and_durable_receipt_contain_shared_feedback tests/timeline/test_authoring_media.py::test_document_publish_forwards_new_stale_head_to_runtime
```

Result: `2 passed in 3.54s`, exit `0`; both requested IDs passed, with zero errors/failures/skips. Private XML/stdout/stderr are retained mode `0600` under `private/`.

A preliminary invocation without the pinned Runtime `PYTHONPATH` failed during collection with `ModuleNotFoundError: runtime_protocol`; it did not execute a test body and is not counted as qualification. The corrected invocation used the exact Runtime `6a011d58` origin from reproduction0510.

## Static checks

- `git diff --check`: PASS.
- `/home/user/work/venv-agent/bin/python -m ruff check tests/timeline/test_authoring_feedback.py tests/timeline/test_authoring_media.py`: PASS (`All checks passed!`).
- Input/assertion conservation AST audit: PASS for both functions; only `_bundle` → `_capture_bundle` setup naming differs, and assertion/raise counts are unchanged.
- Product-path mypy: N/A; no product file changed.
- Full suite and pristine duplicate: NOTRUN per brief.

## Disk/source

`disk-trace.txt` is the retained continuous reproduction trace from 0510: minimum observed free bytes `4374601728`, above the `4000000000` stop. No full suite or heavy body was run here.

Agent base: commit `8585ed9c0404d0187b2ce70242d25114a32747c2`, tree `92a3ffdb5a8bf476e10bfa1bbda3e2856fb9938c`.

Runtime source: commit `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d`, tree `ac5b862744bece65b2e30565db1777bacd60da28`, clean.

Exact working diff SHA-256: `7cdf3f1bd17fe2fdb76687ed4da6f95af95a3317083423939e2b7868f21e4c76`.
