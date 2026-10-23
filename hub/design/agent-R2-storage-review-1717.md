# Agent R2 storage review — agt-R2-storage-review-1717

## Verdict

**PASS for the assigned offline two-file R2/C0 review.** Candidate `ccbb528dc19ddf67367bbfec08d9110a02adafc3` is limited to `astrid/sdk/timeline/inverse.py` and `tests/editing_conformance/test_captured_registry_redo.py` relative to reviewed fold `64e7c59e1`. `git log tl/integration..ccbb528dc` contains only the candidate commit; the fold is already in `tl/integration`.

No product repair, test weakening, merge, pin, generated-file, dependency, environment, or Git write was made.

## Review findings

No blocking or non-blocking findings.

The implementation consistently projects authenticated `parent/occurrences` to the existing physical `bundle.placements` rows for landing guards, historical guards, scratch restoration, original-read validation, and recorded reads/writes. It reuses `State`/`Recording`; it adds no State subclass, public API, root-address broadening, stored parent mirror, or manufactured storage. `_recording_storage` restores both state/input references in `finally`, and only copies validated rows back to physical placements.

The strict path preserves canonical row identity, existing shot ownership, order, membership, and revision pins. Contradictory parent mirrors, absent/null/object aggregates, missing/duplicate/foreign identities, forged revisions/ranges, source-callback changes, and ABA intervening changes refuse. No sorting, ID rebuilding, forced pinning, source/native/effect/history loss, or equal-bytes retargeting was found.

## Independent evidence

- Exact requested focused command on runtime pin `rt-pin-d9e2a71e`: **130 passed in 13.30s**.
- Author `audit.py`, rerun from the current review source with d9: **PASS**; canonical exact, native/effects exact, guard lengths `[1, 3, 3]`, 47 tamper cases, strict input unchanged, and original refusal document/head/history/SQL unchanged.
- Candidate canonical SHA-256 and expected SHA-256: `9c0d1b08599c0c0f8fb895c65a18bca29ca3dab4fff8c21307032fadb882b312`.
- Causal old-RED/new-GREEN: loading reviewed `64e7c59e1`'s `inverse.py` over the new test gives the expected one failure at the historical aggregate guard (`original authored guard changed`); the candidate gives the passing regression above.
- Scoped Ruff: **all checks passed**.
- Scoped mypy: **success, no issues in 2 source files**.
- Ruff baseline: **2149/2149**.
- Mypy baseline: **1912/1912**.
- Vendor lock: **ok** (`34eac0041b0891e9011966b39bcbd26053fde5bc`).
- Artifact manifest: **current**.
- `git diff --check`: **clean**.

## Custody

- Packet `7ab92b619cbe6466b782852afd63c46309722d6d65d88f8fbb8c1e93111a6c15` unchanged.
- Capture `b55cca41df4ee9490c537e01e77742310fc198729f9c4c7acb595da8d833a266` unchanged.
- Source-history supplement `40ea0dda05c20e01bf38eabac35688fbf71d774657a0f9557efe02714fd4e683` unchanged.
- Current imports resolve to this review worktree for Agent and `/home/user/work/wt/rt-pin-d9e2a71e` for Runtime protocol.

## Exact commands

```sh
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-d9e2a71e PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e /home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -pno:cacheprovider tests/editing_conformance/test_captured_registry_redo.py tests/editing_conformance/test_captured_nested_redo.py tests/editing_conformance/test_inverse_stage_images.py tests/editing_conformance/test_step_undo_v2.py
```

```sh
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-d9e2a71e PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e /home/user/work/venv-agent/bin/python /tmp/agt-R2-storage-review-1717-audit/run/audit.py
```

```sh
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/agt-R2-storage-review-1717-ruff /home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline/inverse.py tests/editing_conformance/test_captured_registry_redo.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid/sdk/timeline/inverse.py tests/editing_conformance/test_captured_registry_redo.py --cache-dir /tmp/agt-R2-storage-review-1717-mypy-scoped --hide-error-context --no-pretty
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/agt-R2-storage-review-1717-ruff-baseline /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e MYPY_CACHE_DIR=/tmp/agt-R2-storage-review-1717-mypy-baseline-2 /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
```

## Limits and next step

Public/live Runtime redo was not run, as required by the brief. The review supports manager-owned continuation to the single joint public redo body after the separate validation result; it does not qualify public redo, C271, full/P suites, browser, or integration-worktree behavior.
