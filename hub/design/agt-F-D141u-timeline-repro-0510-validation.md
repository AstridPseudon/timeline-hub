# Validation

- Queue prerequisites: `queue/done/agt-F-D141u-timeline-repro-0510` and `queue/done/checkout-agent-64197afa297f86f1e738238d5e80aff6d33e303a` were present before the pristine body; the latter records the normal checkout at `64197afa297f86f1e738238d5e80aff6d33e303a`.
- Both Agent and Runtime sources were clean before and after each body; exact readbacks are in `source-manifest.json` and `source-status.txt`.
- Disk trace: minimum observed free bytes is computed from `disk-trace.txt`; every sample stayed above the 4,000,000,000-byte stop.
- Private outputs have mode 0600.
- Read-only checks run after bodies: `git status --short --branch`, `git diff --check`, and exact commit/tree readbacks on cut Agent, pristine Agent, cut Runtime, and pristine Runtime.
- Typecheck/lint: NOTRUN because this reproduction made no source changes. Full suite/Farm: NOTRUN per brief.
- Test command for both bodies: `/home/user/work/venv-agent/bin/python -m pytest -q -n3 -o addopts= -p no:cacheprovider --timeout=45 --junitxml=<pair-private-xml> tests/timeline/test_authoring_feedback.py::test_document_publish_stdout_and_durable_receipt_contain_shared_feedback tests/timeline/test_authoring_media.py::test_document_publish_forwards_new_stale_head_to_runtime`.

## Exact read-only outputs

- Minimum traced free bytes: `4374601728`; final free bytes: `4374450176`.
- See `git-readonly.txt` for exact `git status --short --branch`, `git diff --check`, and `git diff --quiet` outputs for all four checkouts.

- Interpreter invocation was `/home/user/work/venv-agent/bin/python` (realpath `/usr/bin/python3.13`, version `3.13.16`) for both bodies.
- Exact first stdout frames were recorded in `result.json`: both began with `bringing up nodes...`; both stderr streams were empty.
