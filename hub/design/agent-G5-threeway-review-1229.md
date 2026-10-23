# G5 independent review: `tl/agt-G5-threeway-tests-1222`

Verdict: **PASS** for the bounded, test-only migration; **not** a whole-G5 or
P1 integration approval.

## Source and scope

- Review role: independent G5/Luna review; executing worker model: Codex/GPT-5.
- Candidate source: `4dac21c9bd13e54fedec2e4b42a5b00de50e2ce6` (abbreviated
  source is `4dac21c9b`).
- Production parent: `7f4edd327`.
- Mapping: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-G5-threeway-tests-1222.md`.
- Normative sources: PLAN §3 G5 and C0 §§1–5 (`design/commit-v2.md`).
- Changed paths: `tests/sdk/test_timeline_checkout.py` and
  `tests/sdk/test_timeline_store_fixes.py` only.

## Exact findings

- Candidate diff is 2 test files only (56 insertions, 38 deletions); no product,
  generated, schema, pin, contract, facade, Runtime, or dependency changes.
- Three mapped legacy functions/four direct calls were migrated from direct
  `three_way` use to real `Checkout.save()`/`Checkout.load()` local replay.
  The path exercises the file lock, local writer merge, existing emitter and
  patch application; no copied/renamed legacy merger or alternate executor is
  present.
- Original successes remain asserted: disjoint clip edits merge; parent
  chapters merge beside the head clip change; and local forced candidate theme
  config lands. Original refusals/no-write remain asserted: overlapping clip
  and parent-config conflicts refuse and leave the disk head intact.
- `force=True` is exercised only on `Checkout.save()` for temporary local
  working-copy files. No publication/runtime force route was introduced.
- The existing local guard cases remain unchanged and pass: concurrency,
  absence/null/opaque order, failed replacement/retry, unknown/free/step/mixed/
  order conservative refusal, and source-bound child/raw-parent mirror cases.
- AST comparison against parent: checkout 69 test functions present in both;
  store-fixes 5 present in both; no removals/additions; only the three mapped
  functions changed. The earlier 64-function baseline is therefore retained.
- Ruff comparison: parent 47 findings, current 46, current-only 0; the sole
  parent-only finding is the baseline unused `pytest` import in store-fixes.
- No skips, xfails, weakened assertions, invented reads, product edits, Git
  mutation, shared installation mutation, or safety/tool denial occurred.

## Commands and counts

Affected three:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_checkout.py::test_three_way_merges_disjoint_edits_and_refuses_overlapping_ones tests/sdk/test_timeline_store_fixes.py::test_publish_merge_keeps_candidate_parent_config_changes_next_to_head_changes tests/sdk/test_timeline_store_fixes.py::test_publish_merge_flags_a_parent_config_key_changed_differently_and_force_wins
3 passed in 1.18s
```

Local guard 13:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_checkout.py::test_save_load_round_trip_shows_both_clocks_and_honours_timeline_edits tests/sdk/test_timeline_checkout.py::test_three_way_merges_disjoint_edits_and_refuses_overlapping_ones tests/sdk/test_timeline_checkout.py::test_two_writers_on_one_working_copy_merge_and_never_drop_each_others_edits 'tests/sdk/test_timeline_checkout.py::test_local_patch_replay_preserves_the_whole_bundle_and_landing_history[a-rocket]' 'tests/sdk/test_timeline_checkout.py::test_local_patch_replay_preserves_the_whole_bundle_and_landing_history[b-plate]' tests/sdk/test_timeline_checkout.py::test_local_patch_replay_preserves_explicit_absence_null_and_opaque_array_order tests/sdk/test_timeline_checkout.py::test_local_patch_replay_failed_replacement_keeps_pending_intent_for_retry 'tests/sdk/test_timeline_checkout.py::test_local_patch_replay_keeps_unknown_reads_and_collection_order_conservative[free]' 'tests/sdk/test_timeline_checkout.py::test_local_patch_replay_keeps_unknown_reads_and_collection_order_conservative[step]' 'tests/sdk/test_timeline_checkout.py::test_local_patch_replay_keeps_unknown_reads_and_collection_order_conservative[mixed]' 'tests/sdk/test_timeline_checkout.py::test_local_patch_replay_keeps_unknown_reads_and_collection_order_conservative[order]' 'tests/sdk/test_timeline_checkout.py::test_local_patch_replay_keeps_source_bound_children_and_raw_parent_mirrors[parent]' 'tests/sdk/test_timeline_checkout.py::test_local_patch_replay_keeps_source_bound_children_and_raw_parent_mirrors[internal]'
13 passed in 1.53s
```

Private mypy:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy tests/sdk/test_timeline_checkout.py tests/sdk/test_timeline_store_fixes.py
Success: no issues found in 2 source files
```

Ruff command:

```text
RUFF_CACHE_DIR=/tmp/agt-G5-threeway-review-1229-ruff /home/user/work/venv-agent/bin/ruff check tests/sdk/test_timeline_checkout.py tests/sdk/test_timeline_store_fixes.py
```

It reports 46 existing findings. Parent comparison is 47; current-only is 0,
with one parent-only unused-`pytest` finding removed. `git diff --check`
passes. No full suite was requested or run.

The first guard command used malformed parametrized node IDs and collected no
tests; it was corrected from pytest's collector output. This does not affect
the passing evidence above.

## Disposition

PASS for this independent bounded review. No blocker remains. Retain as a
draft-only PASS until P1 GO and the orchestrator's integration/merge process;
do not infer whole-G5 completion or approve deletion work from this report.
