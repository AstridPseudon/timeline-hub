# G5 independent review: local-save test migration

Verdict: **PASS** for the bounded, test-only migration. This is not a whole-G5
or P1 integration approval.

## Scope and sources

- Review role: independent G5/Luna review; executing worker model: Codex/GPT-5.
- Candidate: `4dac21c9bd13e54fedec2e4b42a5b00de50e2ce6` (`tl/agt-G5-threeway-tests-1222`).
- Production parent: `7f4edd327` (`tl/agt-G5-local-save-1137`).
- Files under review: `tests/sdk/test_timeline_checkout.py` and
  `tests/sdk/test_timeline_store_fixes.py` only.
- Decision sources read: `PLAN.md` §3 G5 and
  `design/agent-G5-threeway-tests-1222.md`; C0 §§1–5 in
  `design/commit-v2.md`.

## Findings

1. The candidate diff is test-only: exactly the two assigned files, 56 insertions
   and 38 deletions. No production, Runtime, generated, schema, pin, contract,
   facade, or dependency file changed. `git diff --check` passes.
2. The mapping is faithful. Three legacy test functions contained four direct
   `three_way` calls: checkout disjoint/overlap (two calls), parent-config
   success (one), and parent-config conflict/force (two). All now use real
   `Checkout.save()`/`Checkout.load()` local replay through the file-lock and
   local merge path; no copied or renamed legacy merger was added.
3. Original success behavior remains asserted: disjoint `R` nudge plus
   `b-type` text survives together; parent-config chapters survive alongside
   the head clip edit; and the candidate parent theme value lands after local
   force. Original overlap/conflict behavior remains asserted: ordinary save
   refuses, the disk head remains unchanged, and the exact local conflict
   wording is checked.
4. Force remains local-only. The new force calls are only
   `Checkout.save(force=True)` against temporary checkout JSON files. The diff
   adds no publication/runtime force route and no alternate executor.
5. Existing strict local-save controls remain present and pass: two-writer
   concurrency/no-loss behavior; explicit absence, null, and opaque array
   order; failed replacement/retry; unknown/free/step/mixed/order conservative
   refusal; and source-bound child/raw-parent mirror preservation. The selected
   guard set is 13 collected cases, with no skip, xfail, weakened expectation,
   or copied test merger.
6. AST comparison against the production parent found no removed or added test
   functions: checkout has 69 parent/current test functions and store-fixes has
   5 parent/current test functions. Only the three mapped functions changed.
   This preserves the earlier 64-function baseline set and the local-save guard
   additions.

## Commands and evidence

All commands ran from `/home/user/work/wt/agt-G5-threeway-review-1229` with the
requested private Agent/runtime environments.

Affected migrated cases:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/sdk/test_timeline_checkout.py::test_three_way_merges_disjoint_edits_and_refuses_overlapping_ones \
  tests/sdk/test_timeline_store_fixes.py::test_publish_merge_keeps_candidate_parent_config_changes_next_to_head_changes \
  tests/sdk/test_timeline_store_fixes.py::test_publish_merge_flags_a_parent_config_key_changed_differently_and_force_wins
3 passed in 1.18s
```

Local-save guard selection (13 collected cases):

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/sdk/test_timeline_checkout.py::test_save_load_round_trip_shows_both_clocks_and_honours_timeline_edits \
  tests/sdk/test_timeline_checkout.py::test_three_way_merges_disjoint_edits_and_refuses_overlapping_ones \
  tests/sdk/test_timeline_checkout.py::test_two_writers_on_one_working_copy_merge_and_never_drop_each_others_edits \
  'tests/sdk/test_timeline_checkout.py::test_local_patch_replay_preserves_the_whole_bundle_and_landing_history[a-rocket]' \
  'tests/sdk/test_timeline_checkout.py::test_local_patch_replay_preserves_the_whole_bundle_and_landing_history[b-plate]' \
  tests/sdk/test_timeline_checkout.py::test_local_patch_replay_preserves_explicit_absence_null_and_opaque_array_order \
  tests/sdk/test_timeline_checkout.py::test_local_patch_replay_failed_replacement_keeps_pending_intent_for_retry \
  'tests/sdk/test_timeline_checkout.py::test_local_patch_replay_keeps_unknown_reads_and_collection_order_conservative[free]' \
  'tests/sdk/test_timeline_checkout.py::test_local_patch_replay_keeps_unknown_reads_and_collection_order_conservative[step]' \
  'tests/sdk/test_timeline_checkout.py::test_local_patch_replay_keeps_unknown_reads_and_collection_order_conservative[mixed]' \
  'tests/sdk/test_timeline_checkout.py::test_local_patch_replay_keeps_unknown_reads_and_collection_order_conservative[order]' \
  'tests/sdk/test_timeline_checkout.py::test_local_patch_replay_keeps_source_bound_children_and_raw_parent_mirrors[parent]' \
  'tests/sdk/test_timeline_checkout.py::test_local_patch_replay_keeps_source_bound_children_and_raw_parent_mirrors[internal]'
13 passed in 1.53s
```

Private typecheck:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy \
  tests/sdk/test_timeline_checkout.py tests/sdk/test_timeline_store_fixes.py
Success: no issues found in 2 source files
```

Ruff comparison used a private cache and compared both changed files against
their parent blobs by `(file, rule, message)`:

```text
RUFF_CACHE_DIR=/tmp/agt-G5-threeway-review-1229-ruff \
  /home/user/work/venv-agent/bin/ruff check \
  tests/sdk/test_timeline_checkout.py tests/sdk/test_timeline_store_fixes.py
Current diagnostics: 46 (pre-existing checkout-test diagnostics).
Parent diagnostics: 47. Current-only diagnostics: none. The one parent-only
diagnostic is the baseline unused `pytest` import in test_timeline_store_fixes.py.
```

Other read-only checks:

```text
git diff --no-ext-diff --check 7f4edd327..4dac21c9b
passed

git diff --no-ext-diff --name-status 7f4edd327..4dac21c9b
M tests/sdk/test_timeline_checkout.py
M tests/sdk/test_timeline_store_fixes.py
```

An initial guard invocation used malformed parametrized node IDs and yielded
pytest's `no tests ran` collection error. It was immediately corrected using
the collector's exact IDs; the corrected 13-case command above is the evidence.

No full suite, browser/live-socket suite, Runtime integration, dependency
installation, shared-install/cache mutation, or Git mutation was performed.

## Decisions, blockers, next step

The only review judgment was to retain the local boundary's conservative
`parent.` conflict wording rather than the retired publication-unit wording,
as prescribed by the mapping report. No blocker remains for this bounded
review. Keep this PASS as draft-only until the orchestrator's P1 GO and normal
integration/merge process; this review does not approve G5 deletions or whole
project completion.
