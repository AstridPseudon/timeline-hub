## Report

Implemented D124 in the existing Runtime phase helper and focused tests only.

- Added UTC/monotonic witnesses, PID/birth binding, capture namespaces, sanitized routes, SHA-256 Idempotency-Key correlation, explicit unsupported boundaries, and bounded 20 ms passive sampling.
- Preserved redaction, fail-closed loading, watchdog behavior, and Runtime product code.
- Verified normal App `sitecustomize.py` loader offline against the exact helper path.
- Reused reviewed D111a donor: `a0b3eac1a2126c6bf2e77f06ab5d0a9312ef4328`, SHA-256 `4efa1e6e7934cd6ada72e83660ed54f3db7b9e60c28905614b070e1194cebe41`.

Tests:

```text
pytest tests/test_p2_commit_phase_capture.py: 18 passed
ruff: All checks passed
py_compile: passed
mypy --follow-imports=skip --ignore-missing-imports: passed
git diff --check: passed
```

Only changed:

- `tests/helpers/p2_commit_phase_capture.py`
- `tests/test_p2_commit_phase_capture.py`

No full/P2 browser tour was run per task restrictions. Recommended next step: independent protected review, then normal central P2 execution.