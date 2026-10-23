# Agent R2 legal ABA partition repair — source quality only

Base: `65a2e5aec` (`tl/agt-R2-current-port-1831`, current-only candidate port). No merge, checkout, commit, push, ref mutation, daemon, socket/browser suite, full suite, shared dependency write, pin or environment change was performed.

## Result and exact cause

The original provider-produced two-native-command history emits inverse stage **b**, ordinal 1, native `[0,9]`, effects `[0,0]`; then **a**, ordinal 0, native `[9,19]`, effects `[0,2]`. The next inverse previously refused the legitimate empty effect range. All nine writes in b are retained no-op native writes; all four compiler mirrors belong to a. Three mirrors share the clip-position endpoint while their complete app objects differ. The original review is available with `git show tl/agt-R2-cumulative-review-1831:design/agent-R2-cumulative-review-1831.md` and was read.

`_step_undo.py` changes by **9 insertions / 4 deletions**. It accepts contiguous zero-length effect slices while retaining nonempty native ranges, strict integer types and full native/effect coverage. Property-only parent clip histories now use the existing native-range reconstruction, which checks cause/site and complete before/after observations on detached state. Live inverse execution is unchanged: accepted effects remain validation/attribution, never mutation instructions. All source identity, step, ordinal, physical binding, dependency, membership/order, later-write/ABA, stale/replay and surviving-consumer guards remain in the unchanged provider/inverse machinery.

The new `test_inverse_aba_partition.py` creates every positive accepted entry through the production Python provider and recorder using the existing detached port/ABI fixture. The second native command is captured from the first command's execution result. No positive history is copied and mutated. Whole and selected inverses traverse three further inverse publications with exact complete closure equality, preview immutability/null receipts and accepted receipt agreement. Seventeen detached attribution negatives and three public forged-authority negatives retain strict refusals and immutable durable state.

## Scope decision and independent review

An initial broader dispatch exposed real structural regressions: **95/110 passed, 15 failed**, **5/5 split passed**, **7/14 original passed, 7 failed**. Structural create/delete histories contain order-restoration mirrors between native writes, so they cannot use the property-only reconstruction. That attempt was corrected, and its logs remain under `first-*`. Final code preserves the structural effect-image partition path byte-exact; the new native path requires nonempty property paths. This follows the smallest causal repair and retains existing structural behavior.

**Limitation:** structural histories still contain the pre-existing effect-image/first-equal endpoint matching path. This task fixes the reported legal property ABA; it does not establish a general structural partition redesign. No new ABA boundary is inferred from equal endpoint bytes.

A separate read-only Luna reviewer examined the revised source and all new tests: **qualified source/test quality PASS**, with that structural caveat. Reviewer made no edits or test runs. This is **not merge approval**. Partial 887/fb97/0b/65a candidates remain HELD for the orchestrator. `_root_inverse.py` is byte-exact and the separately owned root repair/16-positive qualification was not run or claimed here.

## Exact validation commands and results

All direct test commands ran in this assigned worktree with:

```sh
export TMPDIR=/tmp/w-121fc62701
export PYTHONDONTWRITEBYTECODE=1
export ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f
export PYTHONPATH=.:/tmp/w-121fc62701:/home/user/work/wt/rt-pin-2a9e347f
export MYPY_CACHE_DIR=/tmp/w-121fc62701/mypy
export RUFF_CACHE_DIR=/tmp/w-121fc62701/ruff
```

Runtime import fixture pin: `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`. Python dependencies were reused read-only. `capture_aba` is an observational plugin in this worker's private scratch directory; its source is retained in evidence. It records inputs before provider/inverse/effect validation and full replies/refusals, including request base pair, commands, steps/patch/reads, merge, declared reads, key, API/project/timeline/source/rationale/group, native/derived writes, stage bindings, source closures/digests, effects/dependencies/history/undo_steps and receipts. The final full-capture run includes preview would_status and null receipt. Public error captures retain structured code/path/current/hint/suggested_command for provider-originated errors. Missing-history failures come from the detached port's legacy envelope and are explicitly distinguished. No Runtime HTTP, merged-wire or production authentication qualification is claimed.

```sh
/home/user/work/venv-agent/bin/python -m pytest -q --tb=short -p no:cacheprovider tests/editing_conformance/test_nested_parent_mirror_ranges.py tests/editing_conformance/test_inverse_registry_containers.py tests/editing_conformance/test_nested_inverse_order.py tests/editing_conformance/test_nested_native_aggregate_partition.py
# 110 passed in 53.52s
/home/user/work/venv-agent/bin/python -m pytest -q --tb=short -p no:cacheprovider -p capture_aba tests/editing_conformance/test_inverse_clip_mirrors.py -k 'split_leaf_output_undo_redo_exact_document_and_causal_records or (split_then_native_leaf_command_restores_each_command_boundary and whole)'
# 5 passed, 30 deselected in 5.05s
/home/user/work/venv-agent/bin/python -m pytest -q --tb=short -p no:cacheprovider -p capture_aba tests/editing_conformance/test_recipe_m2_parent_media.py -k 'provider_exact_reload_inverse_redo_and_retired_ids or ordered_provider_reload_inverse_redo_and_retired_ids or (missing_registry_containers_are_guarded_writes_with_exact_inverse_redo and not config)'
# 14 passed, 71 deselected in 37.73s
/home/user/work/venv-agent/bin/python -m pytest -q --tb=short -p no:cacheprovider -p capture_aba tests/editing_conformance/test_inverse_aba_partition.py
# 19 ABA/attribution tests passed on final source; before adding public negatives, 19 passed in 35.50s.
# Later full 22-case capture: the same 19 plus one public case passed, two new diagnostic-shape assertions failed.
/home/user/work/venv-agent/bin/python -m pytest -q --tb=short -p no:cacheprovider -p capture_aba tests/editing_conformance/test_inverse_aba_partition.py -k public_inverse
# After correcting those new test assumptions: 3 passed, 19 deselected in 5.52s.
```

Final existing cumulative evidence is **129 passed** across the three exact selections, run once on the revised source. Earlier failed implementation results remain visible; they are not included in the passing count. The final 22 new cases are qualified by the unchanged passing 19 plus final targeted three, not by claiming one green combined 22-case invocation. Initial new-test mistakes (an unused `value` on remove, guessed invalid reason, and detached-port error shape/current assumptions) and their corrected evidence are retained. No pre-existing test was changed, skipped, deleted, disabled or xfailed.

Final scoped commands:

```sh
/home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline/_step_undo.py astrid/sdk/timeline/inverse.py tests/editing_conformance/test_nested_parent_mirror_ranges.py tests/editing_conformance/test_nested_inverse_order.py tests/editing_conformance/test_nested_native_aggregate_partition.py tests/editing_conformance/test_inverse_aba_partition.py
# All checks passed.
/home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid/sdk/timeline/_step_undo.py astrid/sdk/timeline/inverse.py tests/editing_conformance/test_nested_parent_mirror_ranges.py tests/editing_conformance/test_nested_inverse_order.py tests/editing_conformance/test_nested_native_aggregate_partition.py tests/editing_conformance/test_inverse_aba_partition.py --hide-error-context --no-pretty
# Success: no issues found in 6 source files.
/home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline
# 2149 current / 2149 baseline
/home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
# 1912 current / 1912 baseline
/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
# ok runtime.lock.json
/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
# artifacts.json is current
git diff --check
# exit 0
```

Ratchets ran on final product source; only the new public test diagnostics changed afterward and final scoped checks cover those. Preliminary checks from the superseded attempt are retained as `first-*`, not presented as final-source evidence. No full test-service request was made.

## Integrity, evidence and next action

All **1068 pre-existing Python test files are byte-exact** against pre-edit SHA256, hence their ASTs are unchanged. All existing Python files except `_step_undo.py` are byte-exact. Registry `22f1cb169`'s `coalesce` function is byte-exact. Current R1/reader/A4/legacy paths, Runtime/App/schema/commit/validation/locks/artifacts are untouched; only `_step_undo.py` and the new focused test are product-tree changes.

Actual loaded `_step_undo.py` SHA256:

- before: `003fc372b66221a1faeacd360fcaad9d780b7ecb152c9ef5bc5dcbafecb7d202`
- after: `459151d59444197628e0ebd3a74f1b4efdce33a97597e3e1e04878f022fcf21c`

Evidence directory:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-ABA-partition-sol-1833/evidence/`

It contains bounded full captures, baseline/final source and actual module hashes, exact command/environment JSON, raw passing and failing logs, independent review summary, source/test integrity checks, credential-pattern scan and SHA256SUMS. Credential scan found no matching private-key/token patterns. Large captures stay in the worker directory, never design/.

No implementation blocker remains for this scoped source repair. Recommended next action: orchestrator reviews the source-quality report and independent review, keeps unrelated partial candidates HELD, and runs any further separately authorized qualification/merge step. Root work remains separately owned.

Initial red regression command, before source edits (not repeated unchanged):

```sh
/home/user/work/venv-agent/bin/python -m pytest -q --tb=short -p no:cacheprovider -p capture_aba tests/editing_conformance/test_inverse_aba_partition.py -k 'zero_effect and whole'
# 1 failed, 18 deselected; nested inverse ranges differ from accepted history.
```
