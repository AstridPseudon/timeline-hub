Implemented a bounded causal fix for **F-render-timeout** on `bc38aa3eb3`.

Rendering and element registry loads admitted the same source/project pack root twice. They now reuse admission within that load. Canonical checks, distinct-root scans, provenance and cache invalidation remain intact. Added eight focused controls in `tests/core/rendering/test_catalog_scan_once.py`.

Two small unsupported-support probes used the production SDK/CommandTransport route:

| Profiled measurement | Installed baseline | Changed source |
|---|---:|---:|
| Imports | 0.334s | 0.526s |
| Dispatch reached | 11.788s | 6.200s |
| Child catalog loading | 13.079s | 6.647s |
| Total | 25.644s | 13.964s |
| Canonical admissions, parent/child | 56 / 56 | 28 / 28 |

Both returned the same `mystery` rejection. Profile resolution and binary checks were each below 1ms. Baseline modules came from installed child `d12c6f…`; changed modules came from this worktree, using that child’s interpreter and Runtime. The relevant installed baseline files matched parent HEAD.

**Timing limitation:** probes omitted the external-schema search variable and used vendored shape validation. These profiled timings establish redundant work, not qualification of the original case.

Tests used the prescribed qualified environment:

```bash
PYTHONDONTWRITEBYTECODE=1
PYTHONPATH=.:/home/user/work/wt/rt-pin-8ea0766f
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8ea0766f
ASTRID_RUNTIME_SOURCE_ROOT=/home/user/work/wt/rt-pin-8ea0766f
```

Exact pytest commands, with that environment:

```bash
/home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -p no:cacheprovider tests/core/rendering/test_catalog_scan_once.py tests/core/timeline/test_transition_catalog_lazy.py tests/timeline/test_type_resolve.py tests/timeline/test_timeline_elements_catalog.py tests/core/rendering/test_registry.py tests/packs/test_pack_discovery_metadata.py
# 65 passed in 7.09s

/home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -p no:cacheprovider tests/core/test_elements_registry.py tests/core/test_element_kind_registry.py tests/core/rendering/test_registry_matrix.py
# 76 passed, 7 subtests passed in 5.75s
```

Other checks:

- `python -m ruff check . --no-cache --output-format json`: parent/current **2,147 identical diagnostics**, zero new identities.
- Private `python -m mypy astrid scripts/reshape --hide-error-context --no-color-output --no-pretty --show-error-codes`, separate `$TMPDIR/mypy-parent` and `$TMPDIR/mypy-fixed` caches: **1,911 identical diagnostics**, zero new identities.
- `scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004`: PASS.
- `scripts/artifact_manifest.py --check`: PASS.
- `git diff --check`: PASS.

Original test/body, validator, clients, pins and artifacts remain unchanged. No original-body, render, browser or full-suite run occurred.

Commit message and `DONE` written. No blocker to review. Next: Manager review, then normal installed-child qualification of the original 45-second case.