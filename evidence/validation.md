# Validation

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/w-d134-review-mnQwjG/pycache311 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-ab1e4f61" /usr/bin/python3.11 -m py_compile tests/editing_conformance/test_occurrence_fork_source_baseline.py tests/editing_conformance/test_native_sheet_ordinary_runtime.py` — PASS.
- `RUFF_CACHE_DIR=/tmp/w-d134-review-mnQwjG/ruff /home/user/work/venv-agent/bin/python -m ruff check --no-cache tests/editing_conformance/test_occurrence_fork_source_baseline.py tests/editing_conformance/test_native_sheet_ordinary_runtime.py` — PASS.
- `MYPY_CACHE_DIR=/tmp/w-d134-review-mnQwjG/mypy PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-ab1e4f61" /home/user/work/venv-agent/bin/python -m mypy --config-file pyproject.toml tests/editing_conformance/test_occurrence_fork_source_baseline.py tests/editing_conformance/test_native_sheet_ordinary_runtime.py` — PASS.
- `git diff --check a30e74e901a28b39c28facba3deb00d76f186e23 HEAD` — PASS.
- Agent source tree before/after review — commit `8c41696560fd278705751febdcd32527bc2cdf07`, tree `b3638fbf9edb2b2104a89a7e7e4400cac707e471`.
- Runtime source — commit `ab1e4f6141987706132916e2da16477f5a019464`, tree `7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`, clean checkout.
- Central prior targeted run — exit 5; all five integration nodes deselected; not functional evidence.
- Permitted one live integration — NOT RUN: no admissible central exact-selector suite for the required pinned checkout; no local or alternate-runtime fallback.
