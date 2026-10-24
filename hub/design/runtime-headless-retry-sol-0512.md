**FAIL — clean qualification remains blocked.**

Changed only the assigned fixture:

- Expected allocations now follow proven `track, asset, clip` order.
- Both same-key retries retain the original `declare_track=True`.
- Offline interception proves identical serialized requests and metadata. All 84 assertions and function topology remain intact.

The single family run used:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python:/tmp/w-9973ff71a4 ASTRID_CHECKOUT=/tmp/w-9973ff71a4/agent-9cd3dbe PYTEST_PLUGINS=r5_capture /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_headless_overwrite_refused.py
```

All 13 nodes displayed passes; command exited **1**, wall **3.858s**. My supplementary capture finalizer incorrectly rejected Agent’s vendored client origin. Individual durations and accumulated actual packets were not persisted. No rerun performed.

Checks passed:

- In-memory compile and AST preservation.
- `/root/.local/bin/ruff check --no-cache tests/test_timeline_headless_overwrite_refused.py`
- Configured Pyright: **0 errors, 0 warnings**.
- `git diff --check`; three permitted hunks only.

Exact Agent SHA/tree verified. [Evidence and provenance](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R5-headless-retry-sol-0512/provenance.json>) retained; credential scan passed. Commit message and `BLOCKED` written.

Next: independent review, then a separately authorized uninstrumented qualification before merge.