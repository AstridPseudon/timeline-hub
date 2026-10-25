# D127d independent validation

Source: Runtime `684b3d7b6ac5381ed92a363fa7c941031622e1f3`, tree `7051fd435bc4b328954800bf171f5823ae00b2dd`. No product files were edited.

## Required targeted test

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --basetemp=/tmp/w-47e0772443/d127d-tests tests/test_timeline_offline_cost.py
```

Result: **8 passed in 0.41s**.

## Required bounded benchmark

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-runtime/bin/python tools/benchmark_timeline_commit_cost.py --repeats 1 --output /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D127d-offline-path-review-2135/evidence/benchmark-smallwarm.json
```

Result: exited 0; output status `UNAPPLIED`. Retained capture: 200,611 file bytes / 200,610 canonical bytes / 2 commands / 54 canonical-document checks; warm median **123.629 ms**. Synthetic maximum: 54,643 canonical bytes / 54 checks; validation+digests **205.264 ms** warm and detached copies **87.888 ms** warm. The raw JSON is preserved in `benchmark-smallwarm.json`.

## Scoped static/source checks

```sh
/root/.local/bin/ruff check --no-cache tools/benchmark_timeline_commit_cost.py tests/test_timeline_offline_cost.py
```

Result: **FAIL**, five findings in the inherited additive artifact: one import-order I001 and four B023 closure-loop warnings. No fix was applied because this task is a read-only review and the retained benchmark/tests are the author's artifact; the findings do not alter the path verdict.

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python - <<'PY'
import ast
from pathlib import Path
paths = ["runtime_protocol/server.py", "runtime_protocol/service.py", "runtime_protocol/timeline_commit_execution.py", "runtime_protocol/timeline_commit_provider.py", "runtime_protocol/timeline_commit_port.py", "runtime_protocol/timeline_commit_store.py", "runtime_protocol/timeline_commit_auth.py"]
required = {"runtime_protocol/server.py": {"_timeline_commit"}, "runtime_protocol/service.py": {"register_timeline_commit_provider", "commit_timeline", "_execute_timeline_commit"}, "runtime_protocol/timeline_commit_execution.py": {"execute", "_execute"}, "runtime_protocol/timeline_commit_provider.py": {"load_timeline_commit_provider"}, "runtime_protocol/timeline_commit_port.py": {"capture_sequential_execution", "preview", "accept"}, "runtime_protocol/timeline_commit_store.py": {"preview", "accept"}, "runtime_protocol/timeline_commit_auth.py": {"_capture_document_images", "validate_sequential_capture", "validate"}}
for name, expected in required.items():
    found = {node.name for node in ast.walk(ast.parse(Path(name).read_text(), filename=name)) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
    assert expected <= found, (name, expected - found)
print("AST call-seam symbol census PASS: 15 symbols")
PY
```

Result: **PASS**.

```sh
git diff --check
```

Result: **PASS**; worktree remained clean.

No full suite, HTTP/socket/daemon/browser run, native smoke, provider/store benchmark, or D130 WAL/SWAP test was run. Those remain unverified by this review.
