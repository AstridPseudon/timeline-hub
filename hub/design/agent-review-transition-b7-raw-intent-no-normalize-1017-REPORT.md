# Transition raw-params safety review

Date: 2026-10-21 UTC

## Verdict

**Corrected and approved for the bounded source review.** The prior
`params:null` test encoded silent data retention: after an accepted selected
transition with `params: {"seed": 8}`, the next SET submitted literal
`params:null` and committed `{"seed": 8}`. That was not an intentional raw
merge; `_transition_set` explicitly copied the existing object in its
`params is None` branch.

The handler now keeps the raw intent boundary:

- existing absent or literal-null `params` plus an incoming literal null
  succeeds and stores literal null;
- an existing non-empty parameter object plus incoming literal null refuses
  before any write, preserving the draft/document unchanged;
- object updates still merge only named supplied keys, preserving opaque and
  other parameter values;
- existing reference presence/absence, exact selected identity, adjacency,
  shortest-clip fit, inverse, and selected-authority guards are unchanged.

The safety refusal covers non-empty raw objects (including opaque-only data),
not just schema-known keys, so no raw parameter payload can be silently
discarded. Empty object to null has no parameter value to discard and remains a
literal raw replacement.

## Changes

- `astrid/sdk/timeline/_clip_scalar_commands.py`: refuse destructive
  object-to-null transition updates; preserve null explicitly.
- `tests/sdk/test_timeline_transition_schema.py`: replace the misleading
  selected `{seed: 8} -> null` preservation expectation with an atomic refusal
  assertion, and add the positive already-null duration-update case.

No schema, generated artifact, Runtime/App source, pin, release, registry
activation, generation, native, HTTP, or full-suite path was changed.

## Evidence

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_transition_schema.py` — **5 passed**. The selected-pack fixture exercises the existing retained authority; no pin operation or publication was performed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_clip_scalar_fields.py -k 'private_transition_set_update_remove_pairs_element_ref_and_roundtrips or existing_unreferenced_transition_set_preserves_params_presence or existing_unreferenced_transition_params_merge_and_opaque_fields_survive or unreferenced_transition_set_refuses_present_reference_spelling or unreferenced_transition_set_refuses_changed_type_or_revision_presence or transition_set_enforces_main_adjacency_and_shortest_clip_fit'` — **13 passed, 109 deselected**.
- `/home/user/work/venv-agent/bin/ruff check astrid/sdk/timeline/_clip_scalar_commands.py` — **passed**.
- `git diff --check` — **passed**.

The focused conformance lane retains the exact built-in descriptor ID
`cross-fade`; its existing `.75` authored-seconds update path remains covered,
and the transition handler's authored-seconds/frame-fit admission was not
changed. No full, repeated-178, generation, native, HTTP, or browser suite
was run.

## Blockers / next steps

None for this bounded review. The orchestrator should merge this correction
with the existing b7 source, then continue the separately held source/schema
and Runtime/App consumer qualification process.
