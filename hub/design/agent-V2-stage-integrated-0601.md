# V2/R2 integrated-head readonly source proof

Result: PASS for the requested readonly review on Agent head `6131704b36807e165575fa944ba984cc847059c8`.

## Exact source and composition

- Agent HEAD: `6131704b36807e165575fa944ba984cc847059c8`
- Agent tree: `b4a194abe8601470ea7fa9b38ea54e258dc673c3`
- Worktree: clean; no product/source/test edits made.
- Composition: `6131704b3` merges `f94a3a032` (parents `12b40af01` and `9e6e9cbb5`) with `bfa799284` (D12 validation on fork base `900ba8f09`).
- Protected lineage is present and the merged source controls coexist:
  - authenticated occurrence fork: `900ba8f09`;
  - ordinary-show parent: `12b40af01`;
  - independent guarded-stage source: `9e6e9cbb5`;
  - composed D12 source: `bfa799284`;
  - final merge: `6131704b3`.

## Protected deltas

- `5292b388a` (`test_native_word_anchor.py`) is an ancestor and its current blob is unchanged.
- `38e806316` (`native_word_anchor_fixture.py`) is an ancestor and its current blob is unchanged.
- Protected schema digest `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d` matches the current `astrid/core/timeline/schema/edit-command.schema.json` SHA-256 exactly.
- Runtime lock remains pinned to `34eac0041b0891e9011966b39bcbd26053fde5bc`, tree `9853574865f25e08284e82ffb26c0bdecaa16a30`; `vendor_lock.py check` passed.
- `076630e4e` is not an identity ancestor of this merge composition, but its inverse-binding test blob is byte-identical and its guard hunk is present in `inverse.py`: physical bindings bypass entity alias dispatch only for authenticated `AcceptedRecords`, while unauthenticated/raw records still fail with `history_unavailable`. The current source also contains the later fork-required `recover_rebound_sources` call; this is additive and does not weaken the protected guard.

## Production caller and contract preservation

The mounted path is live: `commands.operations()` registers `occurrence.fork`; `RuntimeCommitService.commit` validates/executes the request, performs final validation, and calls Runtime `preview` or `accept`; `create_runtime_commit_service()` is the service factory consumed by Runtime's `load_timeline_commit_provider('astrid')`. The public `Timeline.commit`/outbox path builds the request with base pair, commands, source, dry-run, label, steps, merge, reads, rationale, and stable flight/idempotency key. Runtime acknowledgements preserve and validate the full `{data, receipt}` shape, including accepted/merged/rebased compatibility, canonical closure/digests, receipt identity, and preview status. Assembly publication additionally carries `group_id`.

D12 exact-rate/reference guards, legacy declaration/source identity retention, authenticated fork-root ownership, and first-stage restoration identity are covered by the passing targeted files below. No metadata, guard, test expectation, skip, or xfail was changed.

## Tests and checks

- `/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_commit_legacy_text_reference.py tests/editing_conformance/test_commit_fps_d12.py tests/editing_conformance/test_commit_anchor_d12.py tests/editing_conformance/test_commit_v2_validation.py tests/editing_conformance/test_commit_timing_validation.py tests/editing_conformance/test_provider_occurrence_fork.py tests/editing_conformance/test_recipe_occurrence_fork.py tests/editing_conformance/test_inverse_stage_images.py tests/editing_conformance/test_step_undo_v2.py tests/editing_conformance/test_provider_step_undo_v2.py tests/sdk/test_timeline_inverse_binding.py tests/sdk/test_timeline_pristine_initialize_provider.py tests/sdk/test_timeline_clip_add_provider.py tests/sdk/test_timeline_semantic_reservations.py`: **227 passed in 14.32s**.
- Targeted Ruff over V2/R2 source/tests: **PASS**.
- V2/R2-only private mypy with `/home/user/work/venv-agent-typecheck-v2/bin/python`: **PASS**, 9 source files.
- `PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/agt-V2-stage-integrated-0601/ruff-normal make ruff PY=/home/user/work/venv-agent/bin/python`: **PASS**, current 2149 / baseline 2149.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/tmp/agt-V2-stage-integrated-0601 MYPY_CACHE_DIR=/tmp/agt-V2-stage-integrated-0601/mypy-normal /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline`: **PASS**, current 1914 / baseline 1914.
- `/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004`: **PASS**.
- `/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check`: **PASS**.
- `git diff --check`: **PASS**.

A deliberately broader exploratory scoped-mypy command that also included unrelated `astrid/core/timeline/cuts.py` failed only on the existing G3 annotation at `cuts.py:187`; the V2/R2-only command passes. No full/browser/live-socket suite was run or requested.

## Import origins

With `PYTHONPATH=.:/tmp/agt-V2-stage-integrated-0601`:

- Agent `commit.py`, `commands.py`, `validation.py`, `native_occurrence_fork.py`, `inverse.py`: current worktree.
- Runtime `runtime_protocol`, `contract_metadata`, `timeline_commit`, `timeline_commit_port`: private archive of Runtime `495769531de8d79d27a2d8022851d75b92f04ebe`, tree `0651fbfe829b4cebb0cfb0fa7540d44e9d999344`.
- `load_timeline_commit_provider('astrid')`: `RuntimeCommitService`, provider id `astrid-v1`, module `astrid/sdk/timeline/commit.py`.

No blockers remain for this readonly proof. Recommended next step: orchestrator may accept this integrated source proof, while tracking the unrelated pre-existing G3 mypy finding separately.

