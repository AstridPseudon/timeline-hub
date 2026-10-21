# Agent source-only reference/track current-floor union

Status: source-only implementation and focused qualification. No public schema
freeze, generated artifact/client, Runtime/App pin, API/store change, or
acceptance claim is made.

## Exact source and floor

- Current worktree base: `d1f5f7824a5ede5587088735fad6e6870f0b95db`
  (`d1f5` tree `ca825c4bf900400487f9a1ca6b8c1651d63d5a68`), the reviewed
  `timeline.reference` source.
- Track source: `3684b8458389d70ee0713d669c44cdd67a9ddcf8`, tree
  `ce34c03784dfb28ab7d25af325304a45afa8c5d2`. That handoff commit removes
  only its repository process document; the implementation and proof are the
  preceding `a8604a8ca` + `c1ae9e93d` source, carried onto the same current
  floor.
- Shared current floor: `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree
  `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`.

The union is narrow: the current `timeline.reference` additions remain intact,
and `track.reorder` adds only its command definition/registry entry, virtual
order address/read/write, and focused conformance proof. The resulting schema
has 61 definitions and 35 closed operation clauses; both operations are
registered (`timeline.reference`, `track.reorder`).

Changed source/test paths:

- `astrid/core/timeline/schema/edit-command.schema.json`
- `astrid/sdk/timeline/_command_state.py`
- `astrid/sdk/timeline/_track_commands.py`
- `astrid/sdk/timeline/commands.py`
- `tests/editing_conformance/test_recipe_m2_parent_reference.py`
- `tests/editing_conformance/test_recipe_track_order.py`
- `tests/sdk/test_timeline_composed_schema.py`
- `tests/sdk/test_timeline_current_union_schema.py`
- `tests/sdk/test_timeline_materialization_schema_union.py`

## Semantics proven

`timeline.reference@1` remains parent-scoped, `role: source`, and carries
exactly the existing two-field `MediaManifestEntry` (`media_id` and equal
`content_digest`). Verified raw media metadata stays an optional private
boundary result; it is not command/schema state. The recipe writes the
namespaced unplaced reference and the existing parent asset registry carrier,
with exact dependency/identity guards. It creates no placement, shot,
occurrence, clip, track, managed tuple, generation, freeze, pin, or public
artifact.

The reference positive now also runs `compile_authoring_candidate`, then the
real `document_from_bundle` -> JSON copy -> `bundle_from_document` -> document
roundtrip. It proves the raw media manifest survives compilation and reload,
not only State execution. The added namespace probe puts an ordinary asset at
the same user-visible ID and proves the command refuses atomically without
aliasing or overwriting it.

`track.reorder@1` accepts only a complete unique same-owner parent track
permutation plus captured `expected_order`. `track_order` is virtual and
recorder-only; the existing raw track rows remain the carrier, so labels,
null/false/zero/opaque values, clips, config siblings, and lane-placement data
are preserved. The proof covers serialized replay, inverse/redo, equal-state
forward replay, disjoint label rebase, stale order/identity refusal, duplicate
or incomplete membership refusal, and strict recorded A->B->A inverse refusal.
The unsupported `lanes` argument is rejected atomically.

## Namespace disposition

The existing parent asset registry is one ordinary asset namespace (including
its direct/config mirror rule), and the existing `Recording.create_asset`
factory takes the user identity directly. The only deterministic scoped asset
projection found in current code is occurrence projection, not a parent
reference factory; reusing it here would invent an authority/identity contract.
Therefore the precise current source contract is: a new reference ID that is
already occupied by an ordinary parent asset is refused as an identity
collision. The regression test makes this refusal visible and verifies no
silent alias. Separate reference/asset IDs would require an explicitly
approved new-kind or existing deterministic scoped parent factory; neither is
introduced by this source-only task.

## Floor evidence

The schema tests strip only `TimelineReferenceArgs`/`timeline.reference` and
`TrackReorderArgs`/`track.reorder` before reconstructing the prior floors. The
full current-union/materialization/composed schema checks passed, including
the existing exact 84fc reconstruction assertions. No old whole schema was
copied or replaced.

## Tests

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_m2_parent_reference.py
7 passed in 0.98s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_track_order.py
3 passed in 0.85s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_composed_schema.py tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_materialization_schema_union.py
61 passed in 176.04s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider tests/editing_conformance/test_parent_track_label.py tests/sdk/test_timeline_commit_provider_parent_track_label.py
27 passed in 1.77s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_m2_parent_media.py
85 passed in 18.54s

/home/user/work/venv-agent/bin/ruff check --no-cache astrid/sdk/timeline/_command_state.py astrid/sdk/timeline/_track_commands.py astrid/sdk/timeline/commands.py tests/editing_conformance/test_recipe_track_order.py tests/editing_conformance/test_recipe_m2_parent_reference.py tests/sdk/test_timeline_composed_schema.py tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_materialization_schema_union.py
All checks passed

git diff --check
passed
```

No full suite, Runtime/App paired qualification, live socket/browser test,
generation, pin, freeze, publication, or acceptance suite was run.
