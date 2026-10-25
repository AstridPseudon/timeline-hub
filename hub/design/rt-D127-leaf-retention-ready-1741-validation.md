# D127 Runtime leaf-retention validation

## Source and scope

- Current base: `ab1e4f6141987706132916e2da16477f5a019464`.
- Imported reviewed source commit: `231ddb5a6605b535d26172d34439ebe7b90804de`, parent `b81c0ab26df66c7e6f4656104a02e001224b3ffd`.
- The two authorized files are byte-identical to the reviewed commit. No other worktree file or mode changed.
- The App combined review remains **FAIL**; its lifecycle-matrix validator gap was not promoted or edited.

## Commands and results

- `/home/user/work/venv-agent/bin/ruff check --no-cache tests/helpers/p2_commit_phase_capture.py tests/test_p2_commit_phase_capture.py` — **FAIL (baseline-only)**: three existing E402 errors at the intentional `pytest_plugins`-before-import seam in `tests/test_p2_commit_phase_capture.py`. The same three errors reproduce against the current-base file via Ruff stdin. The helper alone passes.
- `/home/user/work/venv-agent/bin/ruff check --no-cache tests/helpers/p2_commit_phase_capture.py` — **PASS**.
- `TMPDIR=/tmp/w-8eb5222f06 /root/.local/bin/mypy --cache-dir /tmp/w-8eb5222f06/mypy-cache --follow-imports=skip tests/helpers/p2_commit_phase_capture.py` — **PASS**, no new helper-only type errors.
- `PYTHONPYCACHEPREFIX=/tmp/w-8eb5222f06/pyc /home/user/work/venv-runtime/bin/python -m py_compile tests/helpers/p2_commit_phase_capture.py tests/test_p2_commit_phase_capture.py` — **PASS**.
- `python -m pytest -q tests/test_p2_commit_phase_capture.py -k 'not mounted_http_commit_route_and_provider_are_observed and not live_watchdog_uses_real_handler_and_private_faulthandler_output' --disable-warnings` — **PASS: 21 passed, 2 deselected** in 1.89s.
- `git diff --check` — **PASS**.
- Reused central evidence: `app-D127-leaf-retention-author-1606-targeted-1025160952-28551` — **PASS: 23 passed in 3.46s**, not rerun here.
- No full, socket-backed, browser, activation, profile, SWAP, WAL, or App validator suite was run.

## Static/source checks

- AST parsing of both authorized Python files — PASS.
- Defaults preserved: max requests `8`, max events `128`, max bytes `65536`, sampling interval `0.02` seconds (`20ms`), top-frame output bound `10`.
- Safe leaf projection is separate from inclusive routing frames; lost-sample and dispatch-wall denominators remain present.
- Lifecycle outcomes are `completed`, `raised`, `returned_without_response`, and `pending_at_stop`; `buffer_complete` remains distinct from lifecycle outcome and legacy `complete` is retained.
- Existing safe-frame allowlist, hashed idempotency key, 0600 sink creation, no raw request payload/headers/credentials/private URLs, and watchdog cancellation paths are preserved by source identity and focused tests.
- No production, wire, store, auth, schema, generated, pin, profile, tour, native, collector, SWAP, WAL, or App files were changed.

## Decision/blockers

The source-only import is complete. The exact requested Ruff command is not green because its test-file E402 baseline is already present on the current base; fixing it would violate exact reviewed-byte identity and the two-file source-only scope. Manager should retain this precise baseline finding and decide normal-queue admission.
