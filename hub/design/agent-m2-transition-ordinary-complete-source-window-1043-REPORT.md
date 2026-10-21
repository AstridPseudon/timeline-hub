# Agent ordinary-only transition source report

Status: source preparation complete on base `b3c96a758`; no version, publication, pin, generation, activation, native execution, DTO/store, or authority-system addition was made.

## Exact identity

- Base commit: `b3c96a758`
- Base tree: `3467b7bffb0fe6edf9178c9a9de4d446c8ab8857`
- Provisional worktree content tree (includes the new test, computed without writing Git objects): `a65ef9208d265cc2567692fa582246f9b761b882`
- Complete schema raw SHA-256: `9397d5faf66776c0a27d3611def6af42d9526dd965ad60eef11dc52bd3dd3e3a`
- Complete schema canonical SHA-256: `9397d5faf66776c0a27d3611def6af42d9526dd965ad60eef11dc52bd3dd3e3a`
- Complete schema inventory: 55 `$defs`, 29 `EditCommand` clauses
- Ordinary-only floor after stripping only transition additions (`transition`, `elementRef`, `schema_source`, and their description/enum entries): `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`, 55 `$defs`, 29 clauses. This is the exact ordinary6ba55 floor.

Changed source paths:

```
astrid/core/timeline/schema/edit-command.schema.json
astrid/sdk/timeline/_clip_scalar_commands.py
astrid/sdk/timeline/_collections.py
astrid/sdk/timeline/_recording.py
astrid/sdk/timeline/_selected_param_authority.py
astrid/sdk/timeline/commit.py
tests/sdk/test_timeline_current_union_schema.py
tests/sdk/test_timeline_transition_schema.py
```

Source SHA-256:

```
astrid/core/timeline/schema/edit-command.schema.json  9397d5faf66776c0a27d3611def6af42d9526dd965ad60eef11dc52bd3dd3e3a
astrid/sdk/timeline/_clip_scalar_commands.py           29c46a5796780e1db74efa12729b20533f933ca84acaa51527567f83ea87eb51
astrid/sdk/timeline/_collections.py                    6b7fbb13065e694bc5b3e16f9bdb61c38144f1a3265fd4be1abc4138f677e7f6
astrid/sdk/timeline/_recording.py                      68b67e0956dfd258f234eee81942937aa19d433134b595c018cfb574112c6f77
astrid/sdk/timeline/_selected_param_authority.py      8b19d56d2c28f1dc9e003f1a578e361397e0f73845319ee76cd60456ba211fdf
astrid/sdk/timeline/commit.py                          abf15c4d3705ff0a60504d7154977a6a35cd10467d8f75221178f1b318f8086d
tests/sdk/test_timeline_current_union_schema.py       29550ce35044e0a40a2e494acae1b4e2741f42815a52fedaa3be44823a75f59d
tests/sdk/test_timeline_transition_schema.py           9bc837e57dcc3379dd009d9dc27b3324216f8db0c936d87af8b6db1e7191442e
```

## Scope and callers

The reviewed transition carrier is additive to the existing `clip.set` union. It preserves ordinary descriptor IDs, authored seconds, incoming predecessor/adjacency/shortest-fit checks, selected P1 authority, raw reference-key presence/revision tuple, absent/null/object parameter states, and visible destructive-null refusal. Paired `transition` + `elementRef` clear requires exact identity; transition-only clear remains compatible. No private materialization, group, transcript, rawOLD, generated/client/lock, or frozen017 content was copied.

Existing live paths observed (no new activation path added):

```
astrid/sdk/timeline/commands.py:82              existing clip.set registration
astrid/sdk/timeline/_clip_scalar_commands.py    clip.set handler/capture
astrid/sdk/timeline/native_checkout.py          existing clip.set checkout branches
astrid/sdk/timeline_sheet.py                    existing clip.set capture/allowed keys
astrid/sdk/timeline_elements.py                existing clip.set construction/recognition
```

The transition implementation is therefore carried by the existing `clip.set` path and remains dormant until a caller supplies the additive fields.

## Evidence

All commands used the shared runtime only through `PYTHONPATH` and did not modify shared dependencies. No full suite was requested.

```
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_transition_schema.py
18 passed in 6.59s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_transition_schema.py tests/sdk/test_timeline_current_union_schema.py -k 'transition or only_reviewed_producer or s2_only_adds or next_successor or each_added_definition' tests/editing_conformance/test_recipe_clip_scalar_fields.py -k 'transition'
26 passed, 121 deselected in 5.80s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_current_union_schema.py -k 'only_reviewed_producer or s2_only_adds or next_successor or each_added_definition' tests/sdk/test_timeline_transition_schema.py
4 passed, 48 deselected in 0.65s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_current_union_schema.py -k 'each_added_definition'
1 passed, 33 deselected in 0.12s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_clip_scalar_provider.py tests/sdk/test_timeline_commit_provider_scalar.py
37 passed in 7.85s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_selected_param_authority.py -k 'disjoint_peer_and_paginated_reload or inverse_consumed_pin or param_cannot_reselect_pin_after_relevant_peer_selection or batch_reselection_changes_stage_authority or param_after_inverse or equal_selection_aba'
7 passed, 20 deselected in 3.59s

git diff --check
passed

python3 -m json.tool astrid/core/timeline/schema/edit-command.schema.json >/dev/null
passed
```

The reciprocal Runtime/App ACK, generated artifacts, live activation/native execution, and any full/browser/live-socket suites remain unverified by design and are next-step integration work.
