# Agent ordinary-only transition source review

Date: 2026-10-21 UTC

## Verdict

**REPAIR LIST — do not issue reciprocal Runtime/App ACK yet.**

The ordinary-only source is otherwise the requested public successor: the
incoming transition is stored on the selected TO clip, the authored duration
stays in seconds, predecessor/track adjacency and shortest-neighbor fit are
guarded, raw presence/null/opaque values are retained, paired clear is
guarded, and the existing transition-only clear remains unchanged. The
ordinary schema floor is exact. One P1/reference-presence hole remains in the
newly enabled `clip.set` selected-authority path.

## Exact source identity

| Item | Identity |
| --- | --- |
| Review base/current public source | `b3c96a758c1cfa2a609d1498e0e9ee401b32cc40`; tree `3467b7bffb0fe6edf9178c9a9de4d446c8ab8857` |
| Candidate source | `47b716d001b45d38805e03b1a254c3353b5968e9`; tree `bbb5ffa28eaadcc521ebc85e115f56e7edf3b1ca` |
| Corrected-1acc reference | `1acc64610019cd13e344a4a4d75e84280b8b7f16`; tree `b51829d29f5eb22e6cae524b1df66bf0febd1de9` |
| Candidate schema raw SHA-256 | `9397d5faf66776c0a27d3611def6af42d9526dd965ad60eef11dc52bd3dd3e3a` |
| Candidate schema inventory | 55 `$defs`, 29 `EditCommand` clauses |
| Transition-stripped ordinary floor SHA-256 | `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d` |

The candidate differs from `b3c96a758` in exactly these eight paths:

```text
astrid/core/timeline/schema/edit-command.schema.json
astrid/sdk/timeline/_clip_scalar_commands.py
astrid/sdk/timeline/_collections.py
astrid/sdk/timeline/_recording.py
astrid/sdk/timeline/_selected_param_authority.py
astrid/sdk/timeline/commit.py
tests/sdk/test_timeline_current_union_schema.py
tests/sdk/test_timeline_transition_schema.py
```

The current candidate SHA-256 matrix for those paths is:

```text
astrid/core/timeline/schema/edit-command.schema.json  9397d5faf66776c0a27d3611def6af42d9526dd965ad60eef11dc52bd3dd3e3a
astrid/sdk/timeline/_clip_scalar_commands.py           29c46a5796780e1db74efa12729b20533f933ca84acaa51527567f83ea87eb51
astrid/sdk/timeline/_collections.py                    6b7fbb13065e694bc5b3e16f9bdb61c38144f1a3265fd4be1abc4138f677e7f6
astrid/sdk/timeline/_recording.py                      68b67e0956dfd258f234eee81942937aa19d433134b595c018cfb574112c6f77
astrid/sdk/timeline/_selected_param_authority.py      8b19d56d2c28f1dc9e003f1a578e361397e0f73845319ee76cd60456ba211fdf
astrid/sdk/timeline/commit.py                          abf15c4d3705ff0a60504d7154977a6a35cd10467d8f75221178f1b318f8086d
tests/sdk/test_timeline_current_union_schema.py        29550ce35044e0a40a2e494acae1b4e2741f42815a52fedaa3be44823a75f59d
tests/sdk/test_timeline_transition_schema.py           9bc837e57dcc3379dd009d9dc27b3324216f8db0c936d87af8b6db1e7191442e
```

No other current blob differs from `b3c96a758`. The delta contains no private
materialization/group/rawOLD/projectdata/AgentWrite insertion-order feature,
generation/native/HTTP activation, or opacity widening. `DocumentPin` is only
the existing selected-pack source carrier.

## Verified contract

- `_transition_set` writes the raw transition to the selected target clip;
  `transition.predecessor` records the same-track predecessor and order.
- `clip_timeline_duration` and authored `at`/`at_ms` values are used; no
  outgoing rewrite, alias normalization, literal-ID rewrite, or saved
  `durationFrames` field is introduced.
- Positive finite frame product, explicit starts, same-track adjacency, and
  shortest adjacent-clip fit are enforced.
- Transition envelope keys and nested opaque values survive updates;
  absent, literal-null, and object `params` states are distinguished.
  Destructive non-empty-object-to-null is refused atomically.
- `clear: ["transition"]` preserves unrelated `elementRef`/`element_ref`;
  paired `clear: ["transition", "elementRef"]` validates the stored
  transition identity before clearing both spellings.
- Current public schema/code/capture agreement is through the existing
  `clip.set` registration (`astrid/sdk/timeline/commands.py:82`), capture
  (`_clip_scalar_commands.py:308-312`), and commit resolver
  (`commit.py:493-518`). Existing callers remain the sheet preview
  (`timeline_sheet.py:720-845`), element/session producer
  (`timeline_elements.py:28-46`), CLI/native checkout, and the current
  `clip.set`/`clip.set-params` APIs. No new transition caller or activation
  path was added.
- Unchanged current paths retain whole-track labels, transcript status/pin
  metadata, Scene/document guards, and the existing ordinary source/client
  identities.

## Required repairs

1. Make the selected-authority read in
   `astrid/sdk/timeline/_selected_param_authority.py:43-52` presence-aware
   for both reference spellings. The current code chooses
   `reads['elementRef']` whenever that key was read, even when its tagged
   state is `ABSENT`, and consequently ignores a present legacy
   `element_ref`. It can accept a requested newer P1 for a clip whose
   retained legacy reference is an older P1. Check both independently:
   absent canonical + matching legacy is valid; any present null/empty/
   malformed/mismatched spelling must not be treated as absence; both
   present must agree with the retained authority.

2. Replace the truthiness-based selected-reference lookup newly exposed by
   `clip.set` in `astrid/sdk/timeline/commit.py:495` and `:516` with the same
   presence-aware helper. A present canonical `null` or empty value must not
   fall through to a legacy value, and a legacy value must not be ignored
   merely because the canonical key was read as absent. Preserve the existing
   `clip.set-params` behavior outside this feature while applying the strict
   rule to the new transition carrier.

3. Add a provider-level regression for a selected project-pack transition:
   first accepted P1 through legacy `element_ref`, then a same-stable-ID
   newer revision/P2 transition `clip.set` must refuse without mutation;
   also cover canonical-present-null plus legacy-valid. The current 18
   transition tests cover built-in and raw cases but do not exercise this
   selected-pack `clip.set` authority transition.

## Evidence

Passed directly in this worktree, with shared dependencies read-only:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_transition_schema.py
18 passed in 5.76s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_current_union_schema.py
34 passed in 161.04s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_clip_scalar_provider.py tests/sdk/test_timeline_commit_provider_scalar.py
37 passed in 9.47s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_selected_param_authority.py -k 'disjoint_peer_and_paginated_reload or inverse_consumed_pin or param_cannot_reselect_pin_after_relevant_peer_selection or batch_reselection_changes_stage_authority or param_after_inverse or equal_selection_aba'
7 passed, 20 deselected in 4.17s

/home/user/work/venv-agent/bin/ruff check astrid/sdk/timeline/_clip_scalar_commands.py astrid/sdk/timeline/_collections.py astrid/sdk/timeline/_recording.py astrid/sdk/timeline/_selected_param_authority.py astrid/sdk/timeline/commit.py tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_transition_schema.py
All checks passed

git diff --check
passed

python3 -m json.tool astrid/core/timeline/schema/edit-command.schema.json >/dev/null
passed
```

The independent counterexample probe against `_association` returned the
requested P2 when the captured reads were canonical `ABSENT` plus legacy
present P1 (`association returned requested P2: True`), demonstrating the
repair above. No full, generation, native/HTTP, pin, browser, renderer, or
live-activation suite was run.

## Recommended next step

Repair the two presence lookups, add the selected-pack transition P1
regression, rerun this same focused matrix, then request reciprocal
Runtime/App ACK against the repaired source. No Runtime/App product change,
generation, pinning, or activation is authorized by this review.
