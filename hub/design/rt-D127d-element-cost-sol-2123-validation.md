# D127d validation — offline evidence only

Exact Runtime base cf0b82dd47452a7a34fc63eb233e9b1dc0532806 / tree 8d5683702f36034f27ee7f49737665d66dbc2b75; tracked production,
original tests, fixtures, schemas and generated artifacts are unchanged. Two additive files only.

Final targeted command:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --basetemp=/tmp/w-4fa5bdeb1b/pytest-d127d-final tests/test_timeline_offline_cost.py tests/test_timeline_validation_cost.py tests/test_timeline_validation_walk.py tests/test_timeline_schema_resolution.py
```

Result: **54 passed in 3.17s** (8 additive probe guard tests, 46 existing tests). Earlier same
selection before the final benchmark-only API/field changes: 54 passed in 3.31s.
The guards cover finite JSON, cycles/shared children/subclasses, concurrent mutation checks,
nested schema dialects, dynamic scope, registry/checker identity, cache eviction, unknown refs,
exact validation counts and repeated whole-document validation, schema/digest/owner/capture
corruption, and detachment. No test was edited, skipped, weakened or disabled.

```sh
/home/user/work/venv-agent/bin/ruff check --no-cache tools/benchmark_timeline_commit_cost.py tests/test_timeline_offline_cost.py
PYTHONDONTWRITEBYTECODE=1 pyright --pythonpath /home/user/work/venv-runtime/bin/python --project /tmp/w-4fa5bdeb1b/pyright-d127d.json tools/benchmark_timeline_commit_cost.py tests/test_timeline_offline_cost.py
git diff --check
```

Results: Ruff **All checks passed**; Pyright **0 errors, 0 warnings, 0 informations**;
git diff --check PASS. Pyright private config explicitly includes only the two new files,
extraPaths=[worktree, /home/user/work/venv-runtime/lib/python3.13/site-packages], pythonVersion=3.13.
The explicit command filenames ensure this is not an empty include run. Initial Pyright found
pytest resolution and undocumented pstats.Stats attribute access; no ignores were added:
Runtime site-packages was supplied and public cProfile.getstats() replaced undocumented access.
An intermediate absolute-include configuration checked no files and is NOT counted as evidence.

Private compile command (no pyc/cache writes):

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python - <<'COMPILE'
from pathlib import Path
for relative in ('tools/benchmark_timeline_commit_cost.py', 'tests/test_timeline_offline_cost.py'):
    path = Path(relative)
    compile(path.read_bytes(), str(path), 'exec')
    assert all(line.rstrip() == line for line in path.read_text().splitlines())
COMPILE
```

Result PASS. New-file git diff --no-index --check produced no whitespace diagnostics (exit 1
indicates these are new files); private whitespace assertions also cover both untracked additions.
Benchmark command and all final timing samples are in benchmark.md / measurements.json.
All execution used the existing Runtime interpreter; Ruff/Pyright were already-installed read-only tools.

Independent review: /root/independent_review performed read-only pipeline and final benchmark/test
review. Verdict **UNAPPLIED supported; no new blocking findings**. Review caught two evidence-label
issues (validated document images vs full closure; canonical vs file bytes); both were corrected.
Reviewer confirmed public cProfile.getstats() mapping, custody restoration and profiling limits.
Review did not run additional tests or qualify the production join.

Real-provider native smoke: **NOTRUN**. Source-manifest disk available:
4801744896 bytes (<5,000,000,000). No production optimization candidate exists.
Next supported venue/handoff: Runtime lane's central test service, outside this sandbox, at >=5 GB,
on the independently reviewed eventual Runtime candidate with the exact registered Agent provider.
A fresh scoped native commit/preview/invalid/retry smoke must be arranged there before RELEASE;
this report does not authorize a body or assert that one was queued. App owns its sole later element
VERIFY body only after an independently reviewed fix. No further live profiling round is requested.
Original element/P1-P5/full/core/child/fixture whole-make/HTTP/Store/browser/collector and D130 bodies:
**NOTRUN**. No release, full-suite, production security qualification or timing-budget claim.
