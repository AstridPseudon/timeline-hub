**UNAPPLIED.** Production remains unchanged. The offline probes did not reproduce the 21.7-second delay or prove a safe optimization. Independent review agrees.

Added a durable benchmark and eight guard tests. The retained capture measured **123 ms warm**; synthetic document checks reached **267 ms**. These are helper measurements, not controlled lifecycle comparisons.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --basetemp=/tmp/w-4fa5bdeb1b/pytest-d127d-final tests/test_timeline_offline_cost.py tests/test_timeline_validation_cost.py tests/test_timeline_validation_walk.py tests/test_timeline_schema_resolution.py
```

**54 passed in 3.17s.** Scoped Ruff, Pyright, private compilation and whitespace checks passed.

All six evidence files, review findings and exact commands are preserved in [validation.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D127d-element-cost-sol-2123/evidence/validation.md). Commit message and `DONE` written.

Native smoke: **NOTRUN below 5 GB**. Next step is matched, already-retained lifecycle dimensions for offline reproduction. Any eventual fix still requires independent review and real-provider smoke before release.