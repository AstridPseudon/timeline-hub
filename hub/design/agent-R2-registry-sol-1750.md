# R2 guarded registry inverse — agt-R2-registry-sol-1750

Base: `079580ca46af77e0292d49dc34386b25c8391f99`.

Completed the assigned registry correction in `astrid/sdk/timeline/inverse.py` plus one new focused test file. No other product files, original test bodies, schema, client, locks, pins, storage helpers or validation changed. No git writes, installs, daemon/browser/socket/full-suite runs or guard waivers.

## Cause and correction

`State.set(parent/asset:...)` writes every declared parent registry mirror. Coalescing deliberately keeps direct `parent.registry` addresses physical, whereas the native asset address normalizes to `parent.config.registry.assets`. Consequently the authored empty container remained empty in its landing guard after its asset child had been installed and reloaded.

Coalescing now projects the native asset's direct physical storage alias, including its exact before/after states, into the landing calculation. It derives initial presence from the first source registry write and follows explicit registry creation/removal in native order. An asset written before a direct registry is created gets no invented earlier direct alias. The existing folding algorithm computes both ancestor images. Native source records remain unchanged: sequential execution, previous-value guards, later-write/ABA scans, physical identity checks, collection order and guarded emptiness still run through the existing engine. No value-equality-only authorization or ancestor guard removal.

The production `execute`/semantic provider/commit and whole/selected undo callers continue using this same coalescer. No alternate product executor or new helper/public interface. `_recording.py`, `_step_undo.py`, `_commit_patch.py`, and `commit.py` are unchanged. C0 request/reply shapes, preview and structured failures are untouched. Frozen 34e Runtime vendor bytes and all other tracked pins/artifacts are unchanged; tests imported qualified Runtime checkout `d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b` using the existing dependencies.

## Results

- Causal new tests on original source: **3 failed** at exactly the direct-container landing mismatch (`causal-old-red.log`). The same tests pass after the correction.
- Original selector collection: **6/85**, exactly absent/direct/mirrored × image/video, 79 deselected (`collect-original-six.log`).
- Original six unchanged, run once after the meaningful initial source candidate: **6 passed, 79 deselected** (`original-six-candidate.log`). This exercised reload/undo/redo and the original empty-container negative assertions. The subsequent source-order refinement was verified through new focused tests; the original six were not repeated per brief.
- Final new focused file: **41 passed** (`final-new-tests.log`). Includes all six storage/kind round trips, exact native write reversal, ancestor/asset/clip changes, foreign asset, occupied clip IDs, collection order, asset/ancestor ABA, corrupt source order/previous value, immutability/no-write assertions, preservation of a disjoint registry sibling, and an asset write preceding direct-registry creation.
- Bounded existing neighbors: **10 passed, 6 failed, 99 deselected** (`bounded-neighbors.log`). The 8 physical-registry mirror-presence tests and 2 selected provider tests pass. Six split/native-leaf redo nodes fail in unchanged `_step_undo.py:169`, `nested inverse ranges differ from accepted history`.
- Read-only baseline comparison restores only HEAD's original coalescer in process, then calls unchanged production provider/tests: **the same six failures**, 29 deselected (`baseline-neighbor-comparison.log`, retained `baseline_neighbors.py`). This is a baseline comparison, not a production bypass or Runtime qualification.
- Final Ruff baseline: **2149 = 2149**; focused lint passes (`ruff-final-source.log`, `final-integrity.log`).
- Final mypy baseline using existing private typecheck venv and private cache: **1912 = 1912** (`mypy-final-source.log`).
- Vendor lock, artifact manifest, whitespace/diff, original recipe and protected source/pin byte checks: **PASS** (`final-integrity.log`).

Development results retained honestly: an initial new negative test wrongly expected an unrelated registry sibling to be guarded in direct-assets-only history (35 pass/1 fail). It was corrected to mutate the actual authored container, and a separate positive now checks sibling preservation. A further new ordering control exposed candidate overprojection into a not-yet-created direct registry (1 fail); the final presence-tracking refinement fixes it (38 pass, then 41 pass after adding video coverage). No existing test assertion or body was changed.

## Remaining boundary and recommendation

The registry target is complete. The separate nested inverse-stage/effect-range blocker remains with the assigned `_step_undo.py` / `_commit_patch.py` owners. Complete that work and then integrate this narrow change through the manager's merge queue. The original six result belongs to the initial source candidate; final focused tests cover its full storage/kind matrix after the ordering refinement. A reviewer may qualify the original selector on the final integrated tree as their next independent check.

All execution here was pure Agent or detached-provider testing. No mounted/public Runtime acceptance, API receipt, whole end-to-end proof, preview qualification or complete C0 wire packet was generated or claimed. The full original 85/14/provider eight/SDK four/c271/publicredo/9/40/281/58/P1-P4/browser suites were not run. The existing 85 recipe tests remain byte-identical (verified by git diff and retained hash).

No plan or contract decision was changed. Decisions were limited to keeping physical mirror projection private to coalescing, tracking source presence sequentially, and preserving disjoint sibling edits.

## Exact commands and complete outputs

All paths below are absolute. Every captured command log starts with the exact shell command and ends with its exit code. `session-capture.log` retains the worker transcript including early reconnaissance, source reads, edits and command outputs. `initial-reads.txt` retains complete plan/control/contract/diagnosis documents. `inverse.patch`, final source/test copies and the original source are retained alongside logs. Nothing necessary depends on disposable TMPDIR.

### causal-old-red

Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-registry-sol-1750/evidence/causal-old-red.log`

```bash
TMPDIR=/tmp/w-dc8fb21486 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_inverse_registry_containers.py -k direct_container_landing_guard
```

```text
FAILED tests/editing_conformance/test_inverse_registry_containers.py::test_direct_container_landing_guard_contains_sequential_asset[absent]
FAILED tests/editing_conformance/test_inverse_registry_containers.py::test_direct_container_landing_guard_contains_sequential_asset[direct]
FAILED tests/editing_conformance/test_inverse_registry_containers.py::test_direct_container_landing_guard_contains_sequential_asset[mirrored]
3 failed, 33 deselected in 1.42s

EXIT 1
```

### collect-original-six

Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-registry-sol-1750/evidence/collect-original-six.log`

```bash
TMPDIR=/tmp/w-dc8fb21486 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e /home/user/work/venv-agent/bin/python -m pytest --collect-only -q -p no:cacheprovider tests/editing_conformance/test_recipe_m2_parent_media.py -k "missing_registry_containers_are_guarded_writes_with_exact_inverse_redo and not config"
```

```text
tests/editing_conformance/test_recipe_m2_parent_media.py::test_missing_registry_containers_are_guarded_writes_with_exact_inverse_redo[mirrored-video]

79 tests left out by --splits/-k/--deselect (run by other shards or excluded by name)
6/85 tests collected (79 deselected) in 1.02s

EXIT 0
```

### original-six-candidate

Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-registry-sol-1750/evidence/original-six-candidate.log`

```bash
TMPDIR=/tmp/w-dc8fb21486 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_m2_parent_media.py -k "missing_registry_containers_are_guarded_writes_with_exact_inverse_redo and not config"
```

```text
$ TMPDIR=/tmp/w-dc8fb21486 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_m2_parent_media.py -k "missing_registry_containers_are_guarded_writes_with_exact_inverse_redo and not config"
......                                                                   [100%]
79 tests left out by --splits/-k/--deselect (run by other shards or excluded by name)
6 passed, 79 deselected in 1.93s

EXIT 0
```

### new-controls

Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-registry-sol-1750/evidence/new-controls.log`

```bash
TMPDIR=/tmp/w-dc8fb21486 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_inverse_registry_containers.py
```

```text
tests/editing_conformance/test_inverse_registry_containers.py:96: Failed
=========================== short test summary info ============================
FAILED tests/editing_conformance/test_inverse_registry_containers.py::test_registry_inverse_refuses_changed_guards_without_writes[ancestor-direct]
1 failed, 35 passed in 3.49s

EXIT 1
```

### new-controls-final

Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-registry-sol-1750/evidence/new-controls-final.log`

```bash
TMPDIR=/tmp/w-dc8fb21486 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_inverse_registry_containers.py
```

```text
$ TMPDIR=/tmp/w-dc8fb21486 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_inverse_registry_containers.py
.....................................                                    [100%]
37 passed in 2.85s

EXIT 0
```

### alias-order-candidate-red

Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-registry-sol-1750/evidence/alias-order-candidate-red.log`

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e TMPDIR=/tmp/w-dc8fb21486 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_inverse_registry_containers.py -k asset_before_direct_registry_creation
```

```text
37 tests left out by --splits/-k/--deselect (run by other shards or excluded by name)
=========================== short test summary info ============================
FAILED tests/editing_conformance/test_inverse_registry_containers.py::test_asset_before_direct_registry_creation_does_not_invent_earlier_alias
1 failed, 37 deselected in 1.24s

EXIT 1
```

### new-controls-final-source

Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-registry-sol-1750/evidence/new-controls-final-source.log`

```bash
TMPDIR=/tmp/w-dc8fb21486 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_inverse_registry_containers.py
```

```text
$ TMPDIR=/tmp/w-dc8fb21486 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_inverse_registry_containers.py
......................................                                   [100%]
38 passed in 2.69s

EXIT 0
```

### final-new-tests

Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-registry-sol-1750/evidence/final-new-tests.log`

```bash
TMPDIR=/tmp/w-dc8fb21486 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_inverse_registry_containers.py
```

```text
$ TMPDIR=/tmp/w-dc8fb21486 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_inverse_registry_containers.py
.........................................                                [100%]
41 passed in 3.01s

EXIT 0
```

### bounded-neighbors

Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-registry-sol-1750/evidence/bounded-neighbors.log`

```bash
TMPDIR=/tmp/w-dc8fb21486 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_captured_registry_redo.py tests/editing_conformance/test_inverse_clip_mirrors.py tests/editing_conformance/test_provider_step_undo_v2.py -k "physical_registry_folding_keeps_authored_mirror_presence or split_leaf_output_undo_redo_exact_document_and_causal_records or split_then_native_leaf_command_restores_each_command_boundary or two_patch_sequential_reads_select_last_step_and_redo or whole_inverse_projects_each_stage_even_when_final_bytes_equal"
```

```text
FAILED tests/editing_conformance/test_inverse_clip_mirrors.py::test_split_leaf_output_undo_redo_exact_document_and_causal_records[True-path1]
FAILED tests/editing_conformance/test_inverse_clip_mirrors.py::test_split_then_native_leaf_command_restores_each_command_boundary[whole]
FAILED tests/editing_conformance/test_inverse_clip_mirrors.py::test_split_then_native_leaf_command_restores_each_command_boundary[move]
6 failed, 10 passed, 99 deselected in 5.20s

EXIT 1
```

### baseline-neighbor-comparison

Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-registry-sol-1750/evidence/baseline-neighbor-comparison.log`

```bash
TMPDIR=/tmp/w-dc8fb21486 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-registry-sol-1750/evidence/baseline_neighbors.py
```

```text
FAILED tests/editing_conformance/test_inverse_clip_mirrors.py::test_split_leaf_output_undo_redo_exact_document_and_causal_records[True-path1]
FAILED tests/editing_conformance/test_inverse_clip_mirrors.py::test_split_then_native_leaf_command_restores_each_command_boundary[whole]
FAILED tests/editing_conformance/test_inverse_clip_mirrors.py::test_split_then_native_leaf_command_restores_each_command_boundary[move]
6 failed, 29 deselected in 3.55s

EXIT 1
```

### ruff-final-source

Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-registry-sol-1750/evidence/ruff-final-source.log`

```bash
TMPDIR=/tmp/w-dc8fb21486 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e RUFF_CACHE_DIR=/tmp/w-dc8fb21486/ruff-cache /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline && /home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/inverse.py tests/editing_conformance/test_inverse_registry_containers.py --output-format concise
```

```text
$ TMPDIR=/tmp/w-dc8fb21486 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e RUFF_CACHE_DIR=/tmp/w-dc8fb21486/ruff-cache /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline && /home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/inverse.py tests/editing_conformance/test_inverse_registry_containers.py --output-format concise
Ruff findings: current=2149 baseline=2149
All checks passed!

EXIT 0
```

### mypy-final-source

Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-registry-sol-1750/evidence/mypy-final-source.log`

```bash
TMPDIR=/tmp/w-dc8fb21486 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e MYPY_CACHE_DIR=/tmp/w-dc8fb21486/mypy-cache /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
```

```text
$ TMPDIR=/tmp/w-dc8fb21486 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e MYPY_CACHE_DIR=/tmp/w-dc8fb21486/mypy-cache /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
Mypy findings: current=1912 baseline=1912

EXIT 0
```

### final-integrity

Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-registry-sol-1750/evidence/final-integrity.log`

```bash
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json && PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check && PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/inverse.py tests/editing_conformance/test_inverse_registry_containers.py --output-format concise && git diff --check && git diff --exit-code HEAD -- tests/editing_conformance/test_recipe_m2_parent_media.py astrid/sdk/timeline/_recording.py astrid/sdk/timeline/_step_undo.py astrid/sdk/timeline/_commit_patch.py astrid/sdk/timeline/commit.py runtime.lock.json artifacts.json astrid_runtime_client astrid/core/timeline/schema && git status --short
```

```text
artifacts.json is current
All checks passed!
 M astrid/sdk/timeline/inverse.py
?? tests/editing_conformance/test_inverse_registry_containers.py

EXIT 0
```

Tracked production diff size:

```text
16	0	astrid/sdk/timeline/inverse.py
```
