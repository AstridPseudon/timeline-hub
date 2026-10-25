# D118d commands and results

- `git diff --check` — PASS.
- `/home/user/work/venv-agent/bin/ruff check tests/sdk/test_timeline_capture_projection.py` — PASS (`All checks passed!`).
- `PYTHONPYCACHEPREFIX=/tmp/w-8124954af4/app-D118d-projection-first-return-1551/pycache /home/user/work/venv-agent/bin/python -m py_compile tests/sdk/test_timeline_capture_projection.py` — PASS.
- `/home/user/work/venv-agent/bin/mypy --cache-dir /tmp/w-8124954af4/app-D118d-projection-first-return-1551/mypy --follow-imports=skip tests/sdk/test_timeline_capture_projection.py` — PASS (`Success: no issues found in 1 source file`).
- `df -B1 /tmp` — 4,953,280,512 bytes available; exact own-node command was not run because it is below the 5,000,000,000-byte admission floor.
- Runtime custody check — PASS: `/home/user/work/wt/rt-pin-5e9ad1c6` at `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`, tree `de2954a0ceadb4455903d9abdfec3b773318a50f`, clean.
- `git cat-file -e d11417a59:tests/sdk/test_timeline_capture_projection.py` — absent (status 128).
- `git cat-file -e 92443771676ef2bbb547d0a103d708fa8bec4c63:tests/sdk/test_timeline_capture_projection.py` — absent (status 128); this is the verified D120 upstream target.
- Protected prior own9 — FAIL: all nine nodes errored at `bundle_from_document(document)` with `AuthoringBundleError: project scope belongs on the canonical document`, before the registered `doc.patch` call.
