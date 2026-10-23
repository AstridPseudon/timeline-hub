# R2 native and derived partition — candidate complete

Base `fb97d24bf` in `/home/user/work/wt/agt-R2-native-partition-sol-1818`. Changed only `_step_undo.py`, the exact endpoint interface in `inverse.py`, and new focused `test_nested_native_aggregate_partition.py` (20 cases). No commits, refs, shared dependencies, environment provisioning, pins, runtime, schema or public request/reply shapes changed.

## Cause and implementation

The retained accepted split has four compiler mirrors leaving `clip-right` present, followed by authenticated native `config/clips` and `clips` aggregates removing it. Mirror-only endpoint partitioning cannot complete this canonical image. A detached state now follows native leaf and aggregate writes in their accepted native ranges, checks exact previous values, consumes exact causal compiler observations in order, and compares each completed image with its accepted effect slice. The partition returns actual derived slices separately from complete native-plus-derived endpoint images. The order helper consumes those endpoints while retaining its original source/step/boundary identity, slice, command, selection and inverse-effect guards. Native inverse execution, membership/order guards, arrange, and `_commit_patch` strict effect comparison remain unchanged; accepted effect patches only validate detached attribution.

The new path is selected only for accepted records containing the relevant native aggregate sites. Existing mirror-only behavior is retained. Registry coalesce and all existing test bodies including the 41 registry tests are byte-exact. The `inverse.py` adjustment is necessary because the last compiler mirror is not the completed native aggregate endpoint; changing only the partition would give the order helper the wrong final membership.

## Permanent evidence and scope

Permanent own evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-native-partition-sol-1818/evidence`. `split-before-validation.json`, original `split-classification.json`, and full `retained-actual-A-image.json` were copied before validation. Before/candidate/final module files, actual module paths/hashes captured before test validation, complete split and provider realm/request/history/record/effect captures, and the original six full native boundary captures are retained. `split-candidate-classification.json` verifies the exact retained split entry now partitions correctly without changing its input. The original fourteen were run once on the meaningful final candidate; native full-input packets reuse the already complete fb97 capture rather than repeating bodies for instrumentation. The 110-case focused run uses checked-in fixture/test inputs, with the permanent split input retained; it did not use per-node capture instrumentation. No fabricated inputs or receipts.

The previous partial review worker `agt-R2-nested-partial-review-1801` ended STOPPED without a completed report. Its available adversarial script/log were inspected. Its copied-trusted-history mutation probes do not establish submitted-caller control over authenticated store history. The new guard tests explicitly retain that distinction. Final cumulative independent read-only review passed (`evidence/independent-review.md`); it reran no tests. Keep previous 887/fb97 source partials held as standalone candidates; this continuation is for the serialized merge/review queue.

The previously reported `test_create_edit_whole_undo_redo_retains_transient_roots` failure remains visible and UNQUALIFIED, with unchanged `_root_inverse.py:190` refusal `restored root differs from accepted source`. It was not rerun, waived, skipped, or modified. Next causal owner: the root-baseline restoration owner for `_root_inverse.py`, separately assigned by the orchestrator. No full suites, browser/socket runs, original 85, SDK four, c271, publicredo, original9, cohorts or P1/P4 were run.

## Exact commands and results

All commands below ran from the assigned worktree. The runner's command JSON records exact environment (`PYTHONDONTWRITEBYTECODE=1`, private TMPDIR/Ruff/mypy caches, worktree-first PYTHONPATH, Runtime checkout `/home/user/work/wt/rt-pin-2a9e347f`). No shared cache/dependency writes. Source audit confirms the resolved modules. Each log and command JSON is retained under the evidence path.

**five-split: 5 passed, 30 deselected; exact five previously failing nodes, run once**

```sh
/home/user/work/venv-agent/bin/python -m pytest -q --tb=short -p no:cacheprovider -p capture1750 tests/editing_conformance/test_inverse_clip_mirrors.py -k 'split_leaf_output_undo_redo_exact_document_and_causal_records or (split_then_native_leaf_command_restores_each_command_boundary and whole)'
```

**focused: 110 passed: existing 90 + 20 new cases**

```sh
/home/user/work/venv-agent/bin/python -m pytest -q --tb=short -p no:cacheprovider tests/editing_conformance/test_nested_parent_mirror_ranges.py tests/editing_conformance/test_inverse_registry_containers.py tests/editing_conformance/test_nested_inverse_order.py tests/editing_conformance/test_nested_native_aggregate_partition.py
```

**original-fourteen: 14 passed, 71 deselected; one run on final candidate**

```sh
/home/user/work/venv-agent/bin/python -m pytest -q --tb=short -p no:cacheprovider -p capture1750 tests/editing_conformance/test_recipe_m2_parent_media.py -k 'provider_exact_reload_inverse_redo_and_retired_ids or ordered_provider_reload_inverse_redo_and_retired_ids or (missing_registry_containers_are_guarded_writes_with_exact_inverse_redo and not config)'
```

**actual-replay: PASS: baseline capture_mismatch; candidate accepted exact [born, target, C]**

```sh
/home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-native-partition-sol-1818/evidence/replay_actual.py
```

**scoped-ruff: All checks passed**

```sh
/home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline/_step_undo.py astrid/sdk/timeline/inverse.py tests/editing_conformance/test_nested_native_aggregate_partition.py
```

**scoped-mypy: No issues in 3 source files**

```sh
/home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid/sdk/timeline/_step_undo.py astrid/sdk/timeline/inverse.py tests/editing_conformance/test_nested_native_aggregate_partition.py --hide-error-context --no-pretty
```

**ruff-baseline: 2149 / 2149**

```sh
/home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline
```

**mypy-baseline: 1912 / 1912**

```sh
/home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
```

**vendor: ok runtime.lock.json**

```sh
/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
```

**artifact: artifacts.json is current**

```sh
/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
```

**source-audit: PASS: protected files, original test bodies, exact coalesce, pins, actual split endpoints and retained full inputs**

```sh
/home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-native-partition-sol-1818/evidence/audit.py
```

**final-diff: PASS**

```sh
git diff --check
```

## Decisions, remaining work

No contract or approval decision was needed. The only interface adjustment uses complete authenticated native-plus-derived stage endpoints while retaining the exact normal native execution path. Evidence scan found no credential patterns; SHA256SUMS covers permanent evidence. Merge queue may review/apply this candidate; separately assign the transient-root baseline defect. No product blocker remains for this narrow split partition repair, and no wider qualification is claimed.
