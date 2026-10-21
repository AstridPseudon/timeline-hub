# APPROVE SOURCE FOR PEER ACK — Agent free-multi corrected codefix

Reviewed only commit `a19192ea789a209260da46bfbdd5b616fc7cc4ac`
(`fix(timeline): preserve forward move-set guards and rational fps`) against
its parent `922317bd58aa4db8f7cced85b37dd96038ae17df`, using the settled plan,
`agent-free-multi-aba-fps-code-fix.md`, and the prior 922 source review. This
is an independent source/test-conversion review. No product or test files were
changed by this review.

## Findings

- `astrid/sdk/timeline/rebase.py` uses the existing forward identity-only
  history path, then performs a second move-set-specific history check for
  membership/order, source/structure/activity, and identity reads. Ordinary
  clip values remain validated against the final head by the original captured
  command claims. The original plan, reads, selections, bindings, created IDs,
  dependencies, records, and commands are not refreshed or mutated.
- The ordinary forward equal-final-value cases accept both a single later
  same-value write and `2 -> 3 -> 2` ABA, including the staged create-track
  plan. The returned bundle, records, and commands are exact-equal to the
  original plan. Inverse/later-intent checks remain strict and refuse with
  `intervening_write`.
- Membership, lane/root membership ABA, authored order, source, source
  registry, activity, rate, clip/track identity, and occupied-created-ID
  guards remain refusal/atomicity cases. The old incorrect forward `read-aba`
  refusal was converted one-to-one to the positive equal-state case; the new
  changed-membership blocker supplies the independent negative. No old
  passing assertion was deleted, skipped, weakened, or rewritten to expect
  refusal.
- `_rational_fps` accepts Main's mapping and two-item list spellings, while
  preserving the positive-integer policy. `capture.rate()` and the timing
  evaluator share it; scalar/default behavior remains unchanged. The move-set
  still records the canonical numerator/denominator and uses the existing
  common quantized delta/half-open overlap logic. Mapping and list forms
  produce identical rows, writes, dependencies, bindings, selections, and
  created IDs.
- The prior review's literal `head = deepcopy(plan.bundle)` probe is an
  already-applied result containing the newly created V3. Refusal with
  `identity_collision` is correct and distinct from the required equal-state
  forward probe, which must use `head = deepcopy(original)`.
- Schema and floors are unchanged: raw schema SHA-256
  `f44b00983b2d5e8c3f137985baabb8b226fe00e821fed74e66444fa3fbdd3a69`,
  canonical formatted SHA-256
  `ba0c42d6a9359c32d89d8088416f7bc9092481dbd05f236e4d7e6e019c9246e7`,
  60 definitions / 34 operation clauses / 12 explicit v2 clauses. Removing
  only move-set reconstructs the `84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5`
  floor (59 definitions / 33 clauses / 12 v2 clauses).

## Evidence

Focused guard, conversion, rational, inverse, and timing tests:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_free_move_set.py::test_forward_equal_value_aba_accepts_original_guards tests/editing_conformance/test_recipe_free_move_set.py::test_forward_changed_membership_refuses_atomically tests/editing_conformance/test_recipe_free_move_set.py::test_forward_source_and_identity_aba_remain_guarded tests/editing_conformance/test_recipe_free_move_set.py::test_membership_predicates_sources_and_aba_refuse_atomically tests/editing_conformance/test_recipe_free_move_set.py::test_inactive_lane_members_do_not_block_but_their_activity_is_guarded tests/editing_conformance/test_recipe_free_move_set.py::test_groups_intents_and_occupied_created_ids_refuse_whole_batch tests/editing_conformance/test_recipe_free_move_set.py::test_source_registry_reads_and_same_value_assignments_remain_guarded tests/sdk/test_timing_compiler.py::test_fixed_source_window_and_rational_half_frame_ties tests/sdk/test_timing_compiler.py::test_main_and_capture_share_positive_integer_rational_policy tests/sdk/test_timing_compiler.py::test_rational_rate_in_base_parent_canvas_uses_main_policy
38 passed in 4.58s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python - <<'PY'
... bounded direct probe ...
equal-state+identity ABA: ACCEPTED; bundle/records/commands exact
already-applied plan.bundle: REFUSED identity_collision
PY

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python - <<'PY'
... schema/hash/count/floor probe ...
schema file sha256 f44b00983b2d5e8c3f137985baabb8b226fe00e821fed74e66444fa3fbdd3a69
formatted runtime sha256 ba0c42d6a9359c32d89d8088416f7bc9092481dbd05f236e4d7e6e019c9246e7
defs/clauses/v2 60 34 12
stripped84fc 84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5 59 33
PY

git diff --quiet a19192ea789a209260da46bfbdd5b616fc7cc4ac^ a19192ea789a209260da46bfbdd5b616fc7cc4ac -- astrid/core/timeline/schema/edit-command.schema.json
schema diff vs parent: none

git diff --check && /home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/rebase.py astrid/sdk/timeline/capture.py astrid/sdk/timeline/units.py astrid/sdk/timeline/_timing_evaluators.py tests/editing_conformance/test_recipe_free_move_set.py tests/sdk/test_timing_compiler.py
All checks passed
```

No full, Runtime, App, browser, live-socket, generation, pin/freeze, render,
or integration suite was run. No blocker remains. The manager may send the
source-ACK request to Runtime/App from this report; no automatic adoption,
pinning, freeze, or public activation was performed.

