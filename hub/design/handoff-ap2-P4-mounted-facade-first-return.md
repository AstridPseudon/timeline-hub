# Handoff: ap2-P4 mounted facade first return

Source parent is Agent `131561e2ba99eab41ce3588cfdee59e193aeeff3`; the corrected candidate starts from reviewed candidate `d143e3029afc176f91159c79eaf720b5ffb1f0d5`. The harness will create the final commit after exit, so no final SHA is claimed here.

The test-only correction fixes the single fixture to mirrored `at: 0 -> 5` and routes every ten-note mutation through the existing `emit_document_commands` using detached per-note before/after bundles, then stages each emitted command via public `tl.command` and commits once. It asserts ten unique step boundaries, labels, intent/tags/reads, note readback, and preservation of timing, asset, and track. Only `tests/sdk/test_p4_commit_v2.py` is new relative to the original base; the two accidental authored report files from the reviewed candidate were deleted.

Verification passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p4_commit_cases.py tests/sdk/test_p4_commit_v2.py  # 4 passed, 1 unknown-timeout warning
/root/.local/bin/ruff check tests/sdk/test_p4_commit_v2.py                         # All checks passed
/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p4_commit_v2.py       # Success: no issues found
git diff --check                                                               # pass
```

This remains bounded fake-transport/API/real-Python-engine evidence, not Runtime service acceptance or a full P4/H3 claim. CLI/sheet execution, show/history, conflict/rerun, R2 undo, complete v2 reply fields, official Runtime wire acceptance, and the remaining contract matrix are unverified and require later integrated coverage.

