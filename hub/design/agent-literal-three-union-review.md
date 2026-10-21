# Agent literal-three current union review

**APPROVE** — source-only review of `f448c4b40c60d08f4092e232688b0de99bb07243`.

## Scope and identity

- Candidate: `f448c4b40c60d08f4092e232688b0de99bb07243`
- Parent: `30f3d20bf2788e62c1e157f1767d2156dca15131`
- Candidate tree: `d4508b9fa5db9b2a2774fc5acc811fc34814c53d`
- Schema SHA-256: `da144e6d1c0d3e2ad6ef8246a63a4d4c5fd379b7a0efbedc0f376987527ef068`

The actual diff is limited to the schema, two scalar-command docstrings, and
their conformance/union tests. There is no new caller, registry activation,
generation, freeze, pin, Runtime/App change, or live writer activation.

## Review result

The narrow composition preserves the reviewed individual sources and exact
floor reconstructions:

- ordered project-data remove: `c49a6058...` source floor;
- track mute: `0f0b7e93...` source floor;
- clip opacity: `9b4f16f8...` source floor;
- all three removed: exact `84fc0863...` floor;
- existing composed floors remain exact: `65bb68ac...`, `27f2e3ed...`,
  `39211e63...`, `613123b2...`, and `6ba7b51e...`.

The schema is appropriately narrow: `track.muted` is boolean and may be
explicitly cleared; clip `opacity` is a number in inclusive `0..1` and may be
explicitly cleared. `additionalProperties: false`, command JSON validation,
and the recorder preserve null versus absence, reject invalid booleans/numbers,
and keep opacity out of `params`. Existing per-property guards, authored
write records, strict ABA inverse refusal, disjoint rebase, occurrence
ownership, opaque sibling preservation, and ordered namespace inverse behavior
remain intact.

## Evidence

Existing evidence in `agent-literal-three-current-union.md` reports the full
bounded source matrix: **211 passed**, plus the four compact floor checks.
I did not repeat that matrix.

Independent bounded checks against this exact tree:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_track_scalar_fields.py tests/editing_conformance/test_recipe_clip_scalar_fields.py -k 'opacity or closed_bounded_fields_and_disjoint_set_clear'
28 passed, 103 deselected in 1.27s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_materialization_schema_union.py -k 'only_carrier_additions or removing_only_group_additions or removing_group_and_project_data or extent_proposal or private_remove or private_extent_floor or literal_three_union or voiceover_property or complete_reviewed_private_s2'
9 passed, 15 deselected in 1.12s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_current_union_schema.py -k 'full_current_candidate_preserves or next_successor_is_exactly_complete or all_published_floors_preserve'
9 passed, 25 deselected in 4.53s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_clip_scalar_fields.py -k 'original_basis_and_consumed_timing_refuse_changes_atomically or disjoint_rebase_unchanged_write_history_aba_and_inverse or original_app_journey_fields_exact_capture_roundtrip_and_portable_golden'
11 passed, 124 deselected in 1.69s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_m2_project_data.py -k 'remove_deletes_one_key_preserves_order_and_roundtrips_exactly or remove_last_key_prunes_only_empty_namespace_and_app or remove_distinguishes_absent_target_from_null_namespace or remove_pruned_namespace_restores_exact_order_after_reload_and_redo or remove_rebases_disjoint_key_and_refuses_same_key_aba'
5 passed, 17 deselected in 0.79s
```

`git diff HEAD^ HEAD --check` passed. No full, live-socket, Runtime/App,
generation, freeze, pin, or activation suite was run or inferred.

## Recommendation

Accept f448 as the Agent source composition only. Keep Runtime/App adoption,
schema generation/freeze/pin, and caller activation as separate later gates.
