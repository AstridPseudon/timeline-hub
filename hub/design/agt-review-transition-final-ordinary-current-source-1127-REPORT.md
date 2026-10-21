# Final ordinary transition source review

## Verdict

**APPROVE — exact Agent source/tree/schema/floor.** The ordinary transition
carrier and its selected project-pack P1 safety repair are complete on the
current-preserving source. This is source/contract approval only: obtain the
reciprocal Runtime ACK, then hand the exact source to the normal generation
owner. No pin, publication, activation, native, HTTP, generation, or full
suite claim is made here.

## Exact identity

- Agent source commit: `0cfa4ad14664cec9df430637d8f68f2d1f2b487f`
- Parent/current source: `1a50cf3f30398500e9f1ccf0b94d59fe7a8bdb3f`
- Agent tree: `01561fcefb61db6ad70b3cf2f31a778701f8db5e`
- Raw schema SHA-256: `9397d5faf66776c0a27d3611def6af42d9526dd965ad60eef11dc52bd3dd3e3a`
- Schema inventory: 55 `$defs`, 29 `EditCommand` clauses
- Transition-stripped ordinary floor SHA-256: `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`

The diff from `1a50cf3f3` is exactly the nine expected feature/test paths:

```text
astrid/core/timeline/schema/edit-command.schema.json
astrid/sdk/timeline/_clip_scalar_commands.py
astrid/sdk/timeline/_collections.py
astrid/sdk/timeline/_recording.py
astrid/sdk/timeline/_selected_param_authority.py
astrid/sdk/timeline/commit.py
tests/sdk/test_timeline_current_union_schema.py
tests/sdk/test_timeline_selected_param_authority.py
tests/sdk/test_timeline_transition_schema.py
```

All paths outside that set are byte-identical to `1a50cf3f3`, including the
current label/beat/transcript/outbox/presence/docs/public-pin surfaces. There
are no private017, generated, lock, registration, or new live-caller changes.

## Contract and safety findings

- `_selected_reference` and `_selected_reference_from_reads` independently
  preserve presence for `elementRef` and `element_ref`, accept tagged ABSENT
  canonical plus matching legacy P1, and reject present null/empty/malformed
  or disagreeing claims. The same strict helper is used by the transition
  schema resolver and the new selected-authority carrier/history path.
- The old `clip.set-params` lookup remains on its existing non-strict path.
  Strict reference validation is scoped to the new transition `clip.set`
  carrier. A selected-pack same-stable-ID newer P2 refuses atomically; the
  legacy P1 success remains accepted.
- The carrier stores the literal incoming transition on the selected TO clip,
  retains the exact descriptor ID (`cross-fade`) and authored seconds, and
  guards same-track predecessor adjacency and shortest-neighbor fit. Raw
  opaque envelope/parameter data remains lossless. Absent, null, and object
  params remain distinct; destructive non-empty-object-to-null is refused.
  Transition-only clear preserves unrelated references; paired transition plus
  `elementRef` clear validates identity and removes both spellings.
- The current 55/29 schema remains complete, and stripping only the additive
  transition carrier reconstructs the exact ordinary floor above.

## Evidence

Fresh compact checks in this worktree, using read-only shared dependencies:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_selected_param_authority.py -k 'transition_refuses_new_pin_after_legacy_authority_and_preserves_document or transition_refuses_canonical_null_over_legacy_authority_and_preserves_document or transition_accepts_matching_legacy_authority'
3 passed, 27 deselected in 6.25s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_transition_schema.py -k 'transition_set_preserves_raw_values_and_paired_clear_inverse or transition_only_clear_preserves_unrelated_reference or transition_set_enforces_main_adjacency_and_shortest_fit or transition_params_presence_and_destructive_null_refusal or unreferenced_transition_update_preserves_params_presence or unreferenced_transition_update_refuses_present_reference or paired_transition_clear_refuses_mismatched_identity or ordinary_schema_floor_is_exact_after_stripping_transition_additions'
18 passed in 6.01s

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -B - <<'PY'
from astrid.sdk.timeline._command_state import ABSENT
from astrid.sdk.timeline._selected_param_authority import _INVALID, _selected_reference, _selected_reference_from_reads
p1 = {'packId': 'pack', 'id': 'fade', 'kind': 'transition', 'revision': 'p1'}
p2 = {**p1, 'revision': 'p2'}
assert _selected_reference({}) is ABSENT
assert _selected_reference({'element_ref': p1}) == p1
assert _selected_reference({'elementRef': None}) is None
assert _selected_reference({'elementRef': {}}) == {}
assert _selected_reference({'elementRef': p1, 'element_ref': p2}) is _INVALID
assert _selected_reference_from_reads({'elementRef': {'state': 'absent'}, 'element_ref': {'state': 'present', 'value': p1}}) == p1
for reads in ({'elementRef': {'state': 'present', 'value': None}, 'element_ref': {'state': 'present', 'value': p1}}, {'elementRef': {'state': 'present', 'value': {}}, 'element_ref': {'state': 'present', 'value': p1}}, {'elementRef': {'state': 'present', 'value': p1}, 'element_ref': {'state': 'present', 'value': p2}}):
    assert _selected_reference_from_reads(reads) is _INVALID
print('strict selected-reference counterexamples passed: absent+legacy success; null/empty/disagreeing refusal')
PY
strict selected-reference counterexamples passed: absent+legacy success; null/empty/disagreeing refusal
```

```text
/home/user/work/venv-agent/bin/ruff check astrid/sdk/timeline/_clip_scalar_commands.py astrid/sdk/timeline/_collections.py astrid/sdk/timeline/_recording.py astrid/sdk/timeline/_selected_param_authority.py astrid/sdk/timeline/commit.py tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_selected_param_authority.py tests/sdk/test_timeline_transition_schema.py
All checks passed
```

git diff --check
passed

python3 -m json.tool astrid/core/timeline/schema/edit-command.schema.json
passed
```

Reused, without broad reruns, the 1102/1113 evidence: repaired focused
authority/transition/provider lane **85 passed**, current-union lane **34
passed**, and the earlier ordinary transition/provider/direct checks. No full,
native, HTTP, browser, live socket, generation, pin, or activation suite was
run.

The worktree is clean. Recommended next step: Runtime records its reciprocal
ACK against this exact source/tree/schema, then normal generation proceeds from
this tuple.
