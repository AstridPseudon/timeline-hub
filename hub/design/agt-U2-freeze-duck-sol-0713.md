Source repairs are complete; **136-test acceptance remains blocked by the central test-service environment**.

Changed only the five permitted files:

- Added heterogeneous line-record and boolean-mask types; separated scalar and array bed variables.
- Selected `real_runtime(authoring_profile="astrid")`.
- Removed both trailing blank lines and regenerated `artifacts.json` with the prescribed tool.
- Preserved the complete managed duck test, including all 17 assertions.

Direct tests used:

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH="$PWD:/home/user/work/runtime" \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
/home/user/work/venv-agent/bin/python -m pytest -q \
-oaddopts= -pno:cacheprovider \
tests/packs/music/test_duck.py tests/packs/music/test_duck_overlap.py
```

**9 passed.** The same command with these files produced **126 passed**:

```text
tests/core/rendering/test_remotion_registry_corpus_churn.py
tests/sdk/test_host_bootstrap_source_identity.py
tests/test_lane_registry.py
tests/test_lanes.py
tests/test_skip_guard.py
```

Other checks:

| Command | Result |
|---|---|
| `make ruff PY=/home/user/work/venv-agent/bin/python` | PASS, 2145/2145 |
| `MYPY_CACHE_DIR="$TMPDIR/mypy-head-cache" make mypy PY=/home/user/work/venv-agent-typecheck-v2/bin/python` | PASS, 1902/1902 |
| Raw mypy comparison against archived `1f15f27482`, using separate private caches | Zero new or removed normalized diagnostic identities |
| `/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-45c3a7f4` | PASS |
| `/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check` | PASS |
| `git diff --check 1f15f27482` | PASS, including pending fixes |
| `git merge-base --is-ancestor 25359ed6877b9e13e07799bb2c9600fd143fde88 HEAD` | PASS |

`git diff --check 1f15f27482 HEAD` still reports the frozen commit’s two EOF errors until the harness commits these fixes.

Central qualification attempts:

- Generic named suite: failed before collection because Runtime was missing from `PYTHONPATH`.
- Default targeted suite: **111 passed, 15 failed, 10 deselected**. Registry-child stderr confirms `ModuleNotFoundError: runtime_protocol`. Its lane policy also excludes required cases.
- The initial request containing pytest options in `--files` was rejected before execution.

Production source still connects `pack.yaml → duck.run` to managed media, with adoption through `Checkout.publish → TimelineSession.submit → timelines.commit`. **The managed seed/invocation/adoption/rerun workflow was not executed.** Timeline transport, provider, schema, client and lock files remain unchanged; no broader v2 qualification is claimed.

Wrote `commit-msg` and `BLOCKED`; no `DONE`. Next: register the exact minimal 136-test service command, qualify joined coverage, then review. No home merge, full suite, browser run or installed qualification was performed.