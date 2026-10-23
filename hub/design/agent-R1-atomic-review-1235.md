# R1 atomic scope review: PASS

Review target: `tl/agt-R1-atomic-scope-1216/dcb4cee322` against `d1fa6c1332011e4c4f6e075ca458c7dff6bf130c`.

## Verdict

PASS. No findings. The target changes exactly the requested two files:

- `astrid/sdk/timeline/_commit_patch.py`
- `tests/editing_conformance/test_doc_patch_atomic_scope_runtime.py`

There is no Runtime diff or product/schema/pin/contract change. Runtime remained clean at `3b926efab2eed122d374540baee297d4cdcec62a` before and after review. The current Runtime authentication/service source hashes match the retained evidence exactly.

## Review basis

`CommitPatch.finish()` now records effect and materialization bindings before constructing the atomic batch union. The union includes canonical authored writes/reads/derived writes plus every physical binding, and preserves the parent-to-timeline aggregate rule. If that union is not present in every step's input closure, it conservatively uses the timeline scope for every step. Each resulting capture is built from `Closure(self.inputs[step['id']])` using the step's original input boundary, so sequential steps retain their actual input digest and command/step provenance.

The retained d1fa RED evidence is causal and authentic: complete JSON was refused because three materialized physical scopes were omitted, and the independent removed-root case was refused because later-step surviving roots were not represented by the earlier step. The GREEN evidence records zero missing atomic scopes for the complete-JSON acceptance, removed-root acceptance, sequential preview, and sequential acceptance. The new tests exercise canonical readback, idempotent retries, full physical captures, fallback on all steps, sequential input digests/boundaries, source/rationale/group ID, and dry-run no-write behavior.

The impacted suite retains coverage for native captures, physical aliases, sequential step reads, ABA/history guards, collection membership/order, forged captures, no-write refusal, unknown/free atomic fields, previous values, and undo. The existing strict Runtime controls were reused only after source-origin and hash verification; no Runtime guard was changed. No empty-reads workaround or synthetic authority was accepted.

## Commands and results

From `/home/user/work/wt/agt-R1-atomic-review-1235`:

```sh
PY=/home/user/work/venv-agent/bin/python
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTEST_ADDOPTS= "$PY" -m pytest -q \
  -o addopts= -p no:cacheprovider \
  --basetemp=/tmp/agt-R1-atomic-review-1235.SgUyi3/new3 \
  tests/editing_conformance/test_doc_patch_atomic_scope_runtime.py
# 3 passed in 3.64s
```

```sh
PY=/home/user/work/venv-agent/bin/python
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTEST_ADDOPTS= "$PY" -m pytest -q \
  -o addopts= -p no:cacheprovider \
  --basetemp=/tmp/agt-R1-atomic-review-1235.SgUyi3/impacted2 \
  tests/editing_conformance/test_doc_patch_v2.py \
  tests/editing_conformance/test_doc_patch_mirrors.py \
  tests/editing_conformance/test_provider_step_undo_v2.py \
  tests/editing_conformance/test_step_undo_v2.py \
  tests/editing_conformance/test_document_patch_emitter_engine.py \
  tests/sdk/test_timeline_commit_v2_errors.py
# 211 passed in 43.00s
```

Retained strict Runtime evidence, after verifying unchanged Runtime source hashes and origins:

```sh
PY=/home/user/work/venv-agent/bin/python
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/runtime:/home/user/work/runtime/tests \
  PYTEST_ADDOPTS= "$PY" -m pytest -q -o addopts= -p no:cacheprovider \
  --basetemp=/tmp/w-c6d28215e6/strict-auth-agent \
  tests/test_timeline_commit_authentication.py \
  -k 'forged_provider_records_are_rejected_without_writes or read_claims_are_checked_at_input_and_in_dependency_union'
# 32 passed, 41 deselected

PYTHONDONTWRITEBYTECODE=1 "$PY" -m pytest -q -o addopts= -p no:cacheprovider \
  --basetemp=/tmp/w-c6d28215e6/atomic-omission \
  'tests/test_timeline_commit_authentication.py::test_atomic_mode_requires_authoritative_scope_dependencies[True]'
# 1 passed
```

```sh
PY=/home/user/work/venv-agent/bin/python
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. RUFF_CACHE_DIR=/tmp/agt-R1-atomic-review-1235.SgUyi3/ruff \
  make ruff PY="$PY"
# Ruff findings: current=2149 baseline=2149

PY=/home/user/work/venv-agent-typecheck-v2/bin/python
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. MYPY_CACHE_DIR=/tmp/agt-R1-atomic-review-1235.SgUyi3/mypy \
  make mypy PY="$PY"
# Mypy findings: current=1912 baseline=1912

PY=/home/user/work/venv-agent/bin/python
PYTHONDONTWRITEBYTECODE=1 "$PY" scripts/artifact_manifest.py --check
PYTHONDONTWRITEBYTECODE=1 "$PY" scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004
git diff --check
# all passed
```

The prescribed worker `tmpdir` path was a regular file rather than a directory, so pytest could not create its basetemp there. Tests were rerun with the private `/tmp/agt-R1-atomic-review-1235.SgUyi3` directory; this was harness/environment diagnosis only and did not modify the worktree or shared dependencies.

No full suite, browser/HTTP/native14/original58/D17 duplicate suite, or P1/P4 journey was run. No test was weakened, skipped, deleted, or xfailed. No blocker remains. This source fix is independent of the G5 deletion gate; recommended next step is the orchestrator's normal own-merge path.
