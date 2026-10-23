# CommitV2-D12-anchor — agt-V2-anchor-D12-repair-0524

Source repair: PASS in focused validation and the production provider with a detached Runtime port. Original unchanged native neighbor: FAIL at the next, unrelated Runtime acceptance guard. No native acceptance/setup PASS is claimed.

## Scope and decision

Base `e50beb3063df13b5faa86896eb5161ba1df8cb54`, source tree `4edd6dddebbe04decc2d74e0e399510d086b1044`. Read PLAN §3, BOARD-HEADER D12/D14, design/commit-v2.md §§1–5 and the merged Runtime C0d text at contract/commit-v2.md:1307–1315. Read the prior FPS worker's final trace/report. Decisions remain in force.

Only `astrid/sdk/timeline/_commit_timing_validation.py` and new `tests/editing_conformance/test_commit_anchor_d12.py` change. The existing D12 compiler input/attribution mechanism is reused. The parent-word adapter now consults the same proven exemptions before invoking `legacy_binding`. Exemption still requires an identical declaration, identical reference basis, and proof that the declaration was already unresolvable in the baseline. The existing timing compiler receives the unchanged declaration in its existing legacy-declarations input, with no fabricated WordBinding and no authored removal or rewrite.

The old parent reference basis omitted child word sources. For a word declaration only, comparison now includes the full legacy-search target set (all occurrences and their shot clips, source timing declarations, tracks/registry/timing inputs, captured documents) and exact physical source/parent owners. An unresolved word has no authorized selected source, so narrowing that search basis would guess a binding. Changed source geometry, newly introduced/modified declarations, and equal-byte replacement physical images cannot inherit the exemption. Beat/cut handling and the 89c shared-beat causal guard remain unchanged.

The mounted production path remains `create_runtime_commit_service().commit` → `validate_final_candidate(plan.bundle, baseline=base-or-landing-head)` (`commit.py:1121`) → this timing adapter. No request/reply, idempotency, merge, history, inverse, replay, G4, fork, client, schema, pins, Runtime or FPS policy code changes. Full v2 metadata is not transformed by this repair. Detached-port tests assert accepted/preview, preview would_status, receipt shape, byte-exact parent clip retention, unchanged internal revisions, and authoritative label/step patch records. The detached acceptance port does not echo all production wire fields; this is production-provider proof, not new HTTP/full-envelope qualification.

## Identities and import origins

All commands below run in `/home/user/work/wt/agt-V2-anchor-D12-repair-0524`. The assigned `tmpdir` is a pointer file containing `/tmp/w-4b4ee1b374`; scratch, private archives and caches are under that actual path.

```sh
mkdir -p /tmp/w-4b4ee1b374/runtime-be584 /tmp/w-4b4ee1b374/runtime-seed-80973
git -C /home/user/work/runtime archive be5848e17fbf68100286114883f5820fe4755911 | tar -x -C /tmp/w-4b4ee1b374/runtime-be584
git -C /home/user/work/runtime archive 80973d34ae10e498d7213c30287012c9876f4b1a | tar -x -C /tmp/w-4b4ee1b374/runtime-seed-80973
```

Runtime current test tree: `d6f20f841098811ad1351926139f515807e9c5ed` (exact be584); historical seed tree: `858797c721b2d002d7919e1be6afd45e7ec3dffc`. Shared Runtime was read-only at `6a6e97506409719b9d3c54984268e7c93c026efa`, and was not used as the mutable test dependency.

Verified in a separate clean interpreter before importing any detached-port test ABI doubles:

- Python `/home/user/work/venv-agent/bin/python`, 3.13.16.
- `astrid`, `astrid.sdk.timeline.commit`, `_commit_timing_validation`, and `astrid_runtime_client` resolve inside this assigned worktree.
- `runtime_protocol` and `runtime_protocol.timeline_commit` resolve in `/tmp/w-4b4ee1b374/runtime-be584/runtime_protocol/`.
- Native fixture's historical subprocess uses the private exact 80973 archive via `ASTRID_WORD_ANCHOR_SEED_RUNTIME` and its original fixture PYTHONPATH construction. Fixture/selection code is unchanged.

## Exact tests and results

Common test environment:

```sh
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=.:/tmp/w-4b4ee1b374/runtime-be584
export ASTRID_RUNTIME_CHECKOUT=/tmp/w-4b4ee1b374/runtime-be584
P=/home/user/work/venv-agent/bin/python
```

```sh
$P -m pytest -q -o addopts= -p no:cacheprovider \
 --basetemp=/tmp/w-4b4ee1b374/pytest-anchor-final \
 tests/editing_conformance/test_commit_anchor_d12.py
```

PASS: **11 passed in 1.08s** (`/tmp/w-4b4ee1b374/anchor.log`). Covers byte-exact untouched legacy positive through the real compiler; create/modify/target-invalidate negatives; parent/shot/internal/occurrence physical replacement negatives; previously resolvable word invalidated by source trim; production provider acceptance and preview. Initial new-test development had 8 passed/2 failed because two physical replacement probes broke their canonical closure before reaching timing. The new probes were repaired to construct complete replacement documents with correct edges/manifests/digests, keeping the intended missing-anchor refusal assertion. No existing behavior test changed.

```sh
$P -m pytest -q -o addopts= -p no:cacheprovider \
 --basetemp=/tmp/w-4b4ee1b374/pytest-validation \
 tests/editing_conformance/test_commit_fps_d12.py \
 tests/editing_conformance/test_commit_timing_validation.py \
 tests/editing_conformance/test_commit_v2_validation.py \
 tests/editing_conformance/test_commit_anchor_d12.py \
 tests/sdk/test_p1_doc_patch_provider.py tests/sdk/test_timing_compiler.py \
 tests/sdk/test_timing_cycles.py tests/sdk/test_timeline_commit_v2_errors.py \
 tests/timeline/test_meta_validator.py
```

PASS: **188 passed in 26.38s** (`/tmp/w-4b4ee1b374/validation.log`). This includes all required three files, new regressions, unchanged exact-FPS arithmetic controls, P1 provider controls and the 89c shared physical beat/downbeat cases. No tests were skipped, xfailed, disabled or weakened.

### Original neighbor, exactly once after meaningful repair

```sh
ASTRID_WORD_ANCHOR_SEED_RUNTIME=/tmp/w-4b4ee1b374/runtime-seed-80973 \
 ASTRID_RUNTIME_CHECKOUT=/tmp/w-4b4ee1b374/runtime-be584 \
 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/tmp/w-4b4ee1b374/runtime-be584 \
 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= \
 -p no:cacheprovider --basetemp=/tmp/w-4b4ee1b374/pytest-neighbor -m integration \
 tests/editing_conformance/test_native_word_anchor.py::test_native_move_refuses_anchor_basis_until_explicit_clear
```

FAIL: **1 setup error in 3.97s**, log `/tmp/w-4b4ee1b374/neighbor.log`. It now passes the final FPS/timing/legacy-word validation and reaches `commit.py:1149 port.accept(prepared)`. The next refusal is exact be584 Runtime `timeline_commit_auth.validate_claims` at lines 250–257, reached through `timeline_commit_store._validate`: `invalid_records`, `provider executed a different command` (422). This compares submitted versus provider-recorded command identity/args/created fields. No more precise mismatching field was captured, so none is asserted here. This is a separate command-record authentication/producer compatibility issue, not another D12 timing refusal. Per brief, stopped broadening and did not rerun or alter the original test.

The original node's body does not run. No setup/native acceptance, replay/rebase, original-source behavior or 52/54 result is claimed. Original `test_native_word_anchor.py` SHA-256 matches HEAD: `d1ca4b79922d78d7c39a0e64fd8e479dfe725df0de5d348550b54f1f8399a717`. Both D14 undo positives (`test_undo_recovers_before_binding_even_when_text_writes_are_equal`, same_text=False/True) remain unchanged, unskipped and deferred failing controls; they were not rerun in this task and no pass is claimed.

## Quality and integrity

```sh
RUFF_CACHE_DIR=/tmp/w-4b4ee1b374/ruff $P -m ruff check \
 astrid/sdk/timeline/_commit_timing_validation.py \
 tests/editing_conformance/test_commit_anchor_d12.py
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-4b4ee1b374/ruff \
 make ruff PY=/home/user/work/venv-agent/bin/python
```

PASS: scoped Ruff; normal Ruff **2149/2149**, log `ruff-ratchet.log`.

The author-log checker `/tmp/astrid-u2-typecheck/bin/python` no longer exists (initial invocation exited 127). Shared 3.13 scoped mypy succeeds, but normal mypy cannot run because shared NumPy 2.5.2 stubs use syntax incompatible with the repo's Python 3.11 target and types-PyYAML is missing. That attempt exits 2 with environment errors (`mypy-ratchet.log`), not a source result. Recreated the documented U2 checker entirely privately, with no target/config/budget changes:

```sh
UV_CACHE_DIR=/tmp/w-4b4ee1b374/uv-cache uv venv \
 --python /usr/bin/python3.11 /tmp/w-4b4ee1b374/typecheck
UV_CACHE_DIR=/tmp/w-4b4ee1b374/uv-cache uv pip install \
 --python /tmp/w-4b4ee1b374/typecheck/bin/python \
 mypy==1.17.0 numpy==2.4.6 types-PyYAML==6.0.12.20260906 PyYAML==6.0.3
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-4b4ee1b374/mypy-scoped \
 /tmp/w-4b4ee1b374/typecheck/bin/python -m mypy \
 astrid/sdk/timeline/_commit_timing_validation.py --follow-imports=skip
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/tmp/w-4b4ee1b374/runtime-be584 \
 MYPY_CACHE_DIR=/tmp/w-4b4ee1b374/mypy-normal \
 /tmp/w-4b4ee1b374/typecheck/bin/python -m scripts.reshape.compare_mypy_baseline
```

Private scoped mypy: **PASS, no issues in 1 source file**. Normal mypy: **PASS, current=1914 baseline=1914** (exit 0). Logs `mypy-scoped.log`, `mypy-normal.log`. Private environment Python 3.11.17, mypy 1.17.0; all shared installs stayed read-only.

```sh
PYTHONDONTWRITEBYTECODE=1 $P scripts/vendor_lock.py check runtime.lock.json
PYTHONDONTWRITEBYTECODE=1 $P scripts/artifact_manifest.py --check
git diff --check
git diff --exit-code -- tests/editing_conformance/test_native_word_anchor.py \
 tests/sdk/test_p1_doc_patch_provider.py tests/editing_conformance/test_commit_fps_d12.py \
 astrid/sdk/timeline/validation.py
git diff --quiet 89c700aded947a4c498043e0f1a46b4ab3e0a873 -- tests/sdk/test_p1_doc_patch_provider.py
```

PASS: `ok runtime.lock.json`; `artifacts.json is current`; diff whitespace; protected original tests/FPS code unchanged; 89c guard tests unchanged. No generated artifacts, pins or baselines changed. No deletion, git mutation, push, full/native14/browser/heavy/farm/P4 HTTP body run.

## Handoff

Review/merge only this bounded D12 timing fix and its focused tests. Route the newly exposed `provider executed a different command` refusal to the command-record/Runtime authentication owner, with the exact be584 trace above. Do not weaken that authentication guard, change fixtures, invent legacy bindings or widen this timing exemption. D14 relational undo and the larger native tour remain unqualified by this task.
