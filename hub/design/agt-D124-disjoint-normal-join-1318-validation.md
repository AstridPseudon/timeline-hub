# D124 validation
## Join and ownership
- Normal base: `0b586e4b56cffbcd066ea8792adf46b660f5395a`.
- Donor: `07ff6c71d301d6cdc230664c4ed2cc4b4bf2e6e5`, independently reviewed PASS.
- Product join contains only the six paths listed in `source-manifest.json`.
- Runtime-owned `commit.py`, `_commit_preview.py`, and `_commit_patch.py` are byte-identical to normal before and after the join.
- `held-producer.patch` is the exact donor `_commit_patch.py` delta; SHA-256:
  `07fb7ff4201acd1e8fdaa25b82a9f0278fd6aebde24c08801370da5e09bc3596`.
- Worktree diff paths are Agent-owned only; no whole-branch merge or Git write was performed.
- `git diff --check`: PASS.
- Free space at admission: 4.7 GB (required >=4.6 GB; no floor wait).
## Targeted offline tests
Command environment for both commands:
```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-369ffa7c /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider
```
D124 disjoint numeric/mirror nodes:
```text
tests/sdk/test_d124_shared_custody.py::test_patch_materialization_preserves_numeric_encoding
tests/sdk/test_d124_shared_custody.py::test_compile_inputs_exposes_recorded_parent_mirrors_to_recipe_consumer
```
Result: **2 passed in 0.74s**.
Unchanged strict controls from the author recipe:
```text
tests/sdk/test_timeline_commit_provider.py::test_restore_inverse_proof_representations_allow_preview_and_redo
tests/editing_conformance/test_doc_patch_mirrors.py::test_initial_contradictory_mirrors_still_refuse
tests/editing_conformance/test_doc_patch_mirrors.py::test_sequential_clip_mirrors_execute_provider_history_and_inverse
tests/editing_conformance/test_step_undo_v2.py::test_aba_tail_refuses_even_when_the_current_guard_matches
tests/editing_conformance/test_step_undo_v2.py::test_missing_or_corrupt_authority_never_authorizes_partial_inverse
tests/sdk/test_timeline_inverse_fork_guard.py::test_fork_materializations_require_complete_unique_authenticated_edges
tests/sdk/test_timeline_inverse_fork_guard.py::test_equal_payload_sibling_cannot_supply_fork_source_authority
tests/sdk/test_timeline_commit_provider_document.py::test_malformed_complete_closure_fails_closed
```
Result: **45 passed in 10.33s**.
The following four new D124 custody nodes were exercised only to classify the partition and remain unqualified because the Runtime-owned producer delta was intentionally held out:
```text
tests/sdk/test_d124_shared_custody.py::test_legacy_materialization_has_source_effect_pins_for_inverse
tests/sdk/test_d124_shared_custody.py::test_single_inverse_keeps_endpoint_materializations_for_redo[2-2.0]
tests/sdk/test_d124_shared_custody.py::test_single_inverse_keeps_endpoint_materializations_for_redo[1-True]
tests/sdk/test_d124_shared_custody.py::test_single_inverse_keeps_endpoint_materializations_for_redo[True-1]
```
Observed result: **4 failed**, all asserting producer-owned materialization/effect records absent from the intentionally normal producer. No test was changed, skipped, weakened, or marked xfail. The donor's full 53-pass result is not inherited by this partial join.
No Runtime body/socket, full/family/P4, collector/profile/install/acquisition, or known RED suite was run.
## Static checks
All cache and compile output used private `$TMPDIR=/tmp/w-e65adfdb96` paths.
```bash
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=$TMPDIR/d124-ruff-cache /home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline/_doc_patch_materialize.py astrid/sdk/timeline/_recording.py tests/sdk/test_d124_shared_custody.py tests/editing_conformance/native_word_anchor_fixture.py tests/editing_conformance/test_native_word_anchor.py tests/editing_conformance/test_word_binding_recipe.py
```
Result: **All checks passed!**
```bash
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=$TMPDIR/d124-ruff-cache /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline
```
Result: **Ruff findings current=2143 baseline=2143**.
```bash
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=$TMPDIR/d124-mypy-cache /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
```
Result: **Mypy findings current=1902 baseline=1902**.
Python 3.11 compile: **6 changed/imported Python files passed**, output under `$TMPDIR/d124-compile`.
```bash
git diff --check
```
Result: **PASS**.
