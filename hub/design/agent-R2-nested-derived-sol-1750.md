# R2 nested derived stages — partial candidate, owner coordination required

**BLOCKED / not ready to merge as the complete R2 fix.** Agent base `079580ca46af77e0292d49dc34386b25c8391f99`; Runtime import checkout `/home/user/work/wt/rt-pin-d9e2a71e`, exact head `d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b`.

Changed only `astrid/sdk/timeline/_step_undo.py` and new `tests/editing_conformance/test_nested_parent_mirror_ranges.py`. The stage selector now retains and partitions the parent/config/clips derived mirror sequence by contiguous accepted effect slices. It checks the actual command cause ordinal, exact compiler site, canonical before values, sequential mirror chain, complete coverage and final effect image. Aggregate and leaf canonical effects are both supported. Effects are evaluated only against a detached scratch mirror for attribution validation; timeline mutation remains the existing native inverse executor. No history records, native writes, source bindings or outward identities are rewritten. Other derived sites remain refused.

The new focused regression gives **34 passed**, including normal semantic provider whole and selected undo/redo with multiple inherited mirror partitions under one immediate publication/step/command identity; two exact source chains (add/replacement); and strict native/effect ranges, publication, step, ordinals, derived cause/site/images, missing source and foreign source negatives. Original behavior assertions were never edited, skipped or xfailed.

## Exact original eight and retained RED

Collect-only verified exactly eight unchanged nodes: two `test_provider_exact_reload_inverse_redo_and_retired_ids` and six `test_ordered_provider_reload_inverse_redo_and_retired_ids` (77 deselected; registry six never executed).

- Original source: **8 failed**, all `nested inverse ranges differ from accepted history` (16.01s).
- First aggregate candidate: **3 passed, 5 failed** (20.53s).
- Final candidate: **3 passed, 5 failed** (20.33s), with the five now correctly refused by `nested inverse effects differ from execution`.
- Pass: exact `[False]`, ordered `[C-image]`, `[C-video]`.
- Still fail: exact `[True]`, ordered `[A-image]`, `[A-video]`, `[target-image]`, `[target-video]`.

This source is not fixture-invalid. Complete actual accepted entries and source boundaries were saved before inverse validation. The add inverse has two native writes and one derived mirror; ordered/replacement has three native writes and three contiguous mirror writes, with their exact canonical aggregate endpoint effect. Existing source history, effect and ordinal authority remain intact. No compact accepted history was invented.

## Reserved-file boundary and exact next step

`inverse.py:819` calls `restoration_orders(records, only=record)` using the copied stage record returned by `inverse_stages`. `_collections.restoration_orders` matches `record is only`, so no source collection order is selected for this view. The resurrected replacement clip is appended. The captured A-image stage expects `[born, target, C]`, but actual execution produces `[target, C, born]`. C works because appending happens to place it correctly. The strict `_commit_patch.py:530` comparison remains active and refuses the five bad executions.

Published early interface: `design/agent-R2-nested-derived-sol-1750-interface.md`. Manager must coordinate the unique `registrySol1750` inverse.py owner. That executor must consume stage-local authenticated collection order while preserving membership, source and effect checks; a full source-record identity lookup alone is insufficient for partial stages. Do not turn accepted effect patches into timeline mutation instructions, change effect comparisons, flatten history, drop mirrors or fabricate partitions. No change to the reserved inverse.py, _recording.py, commit.py or _commit_patch.py was attempted.

## Bounded neighbors and quality

Final existing nested/history/provider neighbor command: **82 passed, 1 failed, 3 deselected** (7.81s). The failure is `test_create_edit_whole_undo_redo_retains_transient_roots`, `restored root differs from accepted source` in `_root_inverse.py:190`. A private source overlay loaded the exact HEAD `_step_undo.py` and reran this unchanged node: **1 failed with the identical error** (1.79s), establishing it predates this candidate. It was not skipped or rewritten. The three deselections are the existing integration lane exclusion and two media-removal nodes outside this bounded neighbor selection. ABI stub/provider cases are offline, not sockets.

Final scoped Ruff/mypy pass; Ruff baseline **2149/2149**; mypy baseline **1912/1912** using the existing private typecheck venv. Vendor lock, artifact manifest and diff checks pass. Source audit proves inverse.py, _recording.py, commit.py, _commit_patch.py, original parent-media recipe, runtime.lock.json and artifacts.json are unchanged. Frozen producer/pins were retained. No shared environment, dependency, cache, schema/client, ref or Git metadata was modified.

## Evidence and limits

Every test/quality argv, environment, exit outcome and complete output is retained in absolute worker `evidence/*.command.json` / `*.log`; `run.py` is the exact runner. `red-captures/` preserves all eight baseline packets. Final `capture-*.json` includes complete actual requests/contexts, prepared records, native/derived writes, step patches, bindings, source/history documents and before-validation stage/effect images, plus replies/refusals; observational capture hooks never alter return values. `ordered-effect-diagnosis.json` summarizes the exact failing order. Source audit and baseline/candidate source files are retained. Full data remains in the worker directory (not design/); the flat design report and manifest point there. Earlier read-only exploration is also in the harness worker log; inputs.json durably retains the required plan/control/report contents.

The production path is the existing semantic provider/commit and whole/selected inverse executor, used by these offline tests. C0 request/reply routing remains unchanged: exact base pair, step metadata/reads, merge, source/rationale/group, idempotency, canonical result, records/effects/bindings/dependencies/history/undo_steps, required preview would_status/null receipt and structured errors were not removed or reshaped. Actual public Runtime accepted/merged replies, preview, sockets and API behavior were not qualified here. Current Runtime d9e authority is already qualified; no missing approval is alleged. The independently audited G5SDK original failure is not assigned this same cause.

No full suite, other registry six, original SDK four, publicredo, original nine, 40/281/58/P1/P4, browser, provisioning, daemon or merge tools ran. No test was weakened. The all-eight GREEN acceptance remains unmet. Keep P1/no-go decisions unchanged and coordinate the executor owner before rerunning the eight on a combined candidate.

## Exact retained commands

All commands below ran in `/home/user/work/wt/agt-R2-nested-derived-sol-1750`. Their command JSON retains these environment settings: `PYTHONDONTWRITEBYTECODE=1`, `ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-d9e2a71e`, `PYTHONPATH=.:/tmp/w-8d269f08be:/home/user/work/wt/rt-pin-d9e2a71e`, `TMPDIR=/tmp/w-8d269f08be`, and private Ruff/mypy cache paths. Scratch helper scripts are copied into durable evidence; replace their old scratch path with that copy to inspect/replay them after scratch cleanup.

### collect

```sh
/home/user/work/venv-agent/bin/python -m pytest --collect-only -q -p no:cacheprovider tests/editing_conformance/test_recipe_m2_parent_media.py -k 'provider_exact_reload_inverse_redo_and_retired_ids or ordered_provider_reload_inverse_redo_and_retired_ids'
```

Result: `8/85 tests collected (77 deselected) in 1.29s`. Complete output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-nested-derived-sol-1750/evidence/collect.log`.

### final-artifact

```sh
/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
```

Result: `artifacts.json is current`. Complete output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-nested-derived-sol-1750/evidence/final-artifact.log`.

### final-diff

```sh
git diff --check
```

Result: `(empty output / success; see final checks)`. Complete output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-nested-derived-sol-1750/evidence/final-diff.log`.

### final-eight

```sh
/home/user/work/venv-agent/bin/python -m pytest -q --tb=short -p no:cacheprovider -p capture1750 tests/editing_conformance/test_recipe_m2_parent_media.py -k 'provider_exact_reload_inverse_redo_and_retired_ids or ordered_provider_reload_inverse_redo_and_retired_ids'
```

Result: `5 failed, 3 passed, 77 deselected in 20.33s`. Complete output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-nested-derived-sol-1750/evidence/final-eight.log`.

### final-focused

```sh
/home/user/work/venv-agent/bin/python -m pytest -q --tb=short -p no:cacheprovider -p capture1750 tests/editing_conformance/test_nested_parent_mirror_ranges.py
```

Result: `34 passed in 41.50s`. Complete output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-nested-derived-sol-1750/evidence/final-focused.log`.

### final-mypy-baseline

```sh
/home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
```

Result: `Mypy findings: current=1912 baseline=1912`. Complete output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-nested-derived-sol-1750/evidence/final-mypy-baseline.log`.

### final-neighbors

```sh
/home/user/work/venv-agent/bin/python -m pytest -q --tb=short -p no:cacheprovider tests/editing_conformance/test_captured_nested_redo.py tests/editing_conformance/test_inverse_stage_images.py tests/editing_conformance/test_step_undo_v2.py tests/editing_conformance/test_provider_step_undo_v2.py -k 'not selected_media_removal'
```

Result: `1 failed, 82 passed, 3 deselected in 7.81s`. Complete output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-nested-derived-sol-1750/evidence/final-neighbors.log`.

### final-ruff-baseline

```sh
/home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline
```

Result: `Ruff findings: current=2149 baseline=2149`. Complete output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-nested-derived-sol-1750/evidence/final-ruff-baseline.log`.

### final-scoped-mypy

```sh
/home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid/sdk/timeline/_step_undo.py tests/editing_conformance/test_nested_parent_mirror_ranges.py --cache-dir /tmp/w-8d269f08be/mypy-scoped --hide-error-context --no-pretty
```

Result: `Success: no issues found in 2 source files`. Complete output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-nested-derived-sol-1750/evidence/final-scoped-mypy.log`.

### final-scoped-ruff

```sh
/home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline/_step_undo.py tests/editing_conformance/test_nested_parent_mirror_ranges.py
```

Result: `All checks passed!`. Complete output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-nested-derived-sol-1750/evidence/final-scoped-ruff.log`.

### final-vendor

```sh
/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
```

Result: `ok runtime.lock.json`. Complete output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-nested-derived-sol-1750/evidence/final-vendor.log`.

### focused-provider-final

```sh
/home/user/work/venv-agent/bin/python -m pytest -q --tb=short -p no:cacheprovider tests/editing_conformance/test_nested_parent_mirror_ranges.py -k provider_nested
```

Result: `2 passed, 32 deselected in 2.86s`. Complete output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-nested-derived-sol-1750/evidence/focused-provider-final.log`.

### focused-provider

```sh
/home/user/work/venv-agent/bin/python -m pytest -q --tb=short -p no:cacheprovider tests/editing_conformance/test_nested_parent_mirror_ranges.py -k provider_nested
```

Result: `2 failed, 32 deselected in 2.44s`. Complete output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-nested-derived-sol-1750/evidence/focused-provider.log`.

### focused

```sh
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_nested_parent_mirror_ranges.py
```

Result: `32 passed in 33.43s`. Complete output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-nested-derived-sol-1750/evidence/focused.log`.

### green-eight

```sh
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -p capture1750 tests/editing_conformance/test_recipe_m2_parent_media.py -k 'provider_exact_reload_inverse_redo_and_retired_ids or ordered_provider_reload_inverse_redo_and_retired_ids'
```

Result: `5 failed, 3 passed, 77 deselected in 20.53s`. Complete output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-nested-derived-sol-1750/evidence/green-eight.log`.

### neighbor-baseline

```sh
/home/user/work/venv-agent/bin/python /tmp/w-8d269f08be/baseline_neighbor.py
```

Result: `1 failed in 1.79s`. Complete output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-nested-derived-sol-1750/evidence/neighbor-baseline.log`.

### neighbors

```sh
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_captured_nested_redo.py tests/editing_conformance/test_inverse_stage_images.py tests/editing_conformance/test_step_undo_v2.py tests/editing_conformance/test_provider_step_undo_v2.py -k 'not selected_media_removal'
```

Result: `1 failed, 82 passed, 3 deselected in 14.77s`. Complete output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-nested-derived-sol-1750/evidence/neighbors.log`.

### ordered-effect-boundary

```sh
/home/user/work/venv-agent/bin/python -m pytest -q --tb=short -p no:cacheprovider -p capture1750 'tests/editing_conformance/test_recipe_m2_parent_media.py::test_ordered_provider_reload_inverse_redo_and_retired_ids[A-image]'
```

Result: `1 failed in 3.43s`. Complete output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-nested-derived-sol-1750/evidence/ordered-effect-boundary.log`.

### quality-artifact

```sh
/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
```

Result: `artifacts.json is current`. Complete output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-nested-derived-sol-1750/evidence/quality-artifact.log`.

### quality-diff

```sh
git diff --check
```

Result: `(empty output / success; see final checks)`. Complete output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-nested-derived-sol-1750/evidence/quality-diff.log`.

### quality-mypy

```sh
/home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
```

Result: `Mypy findings: current=1912 baseline=1912`. Complete output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-nested-derived-sol-1750/evidence/quality-mypy.log`.

### quality-ruff

```sh
/home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline
```

Result: `Ruff findings: current=2149 baseline=2149`. Complete output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-nested-derived-sol-1750/evidence/quality-ruff.log`.

### quality-vendor

```sh
/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
```

Result: `ok runtime.lock.json`. Complete output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-nested-derived-sol-1750/evidence/quality-vendor.log`.

### red

```sh
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -p capture1750 tests/editing_conformance/test_recipe_m2_parent_media.py -k 'provider_exact_reload_inverse_redo_and_retired_ids or ordered_provider_reload_inverse_redo_and_retired_ids'
```

Result: `8 failed, 77 deselected in 16.01s`. Complete output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-nested-derived-sol-1750/evidence/red.log`.

### scoped-mypy

```sh
/home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid/sdk/timeline/_step_undo.py tests/editing_conformance/test_nested_parent_mirror_ranges.py --cache-dir /tmp/w-8d269f08be/mypy-scoped --hide-error-context --no-pretty
```

Result: `Success: no issues found in 2 source files`. Complete output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-nested-derived-sol-1750/evidence/scoped-mypy.log`.

### scoped-ruff

```sh
/home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline/_step_undo.py tests/editing_conformance/test_nested_parent_mirror_ranges.py
```

Result: `All checks passed!`. Complete output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-nested-derived-sol-1750/evidence/scoped-ruff.log`.

### source-audit

```sh
python3 /tmp/w-8d269f08be/audit.py
```

Result: `d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b`. Complete output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-nested-derived-sol-1750/evidence/source-audit.log`.

