# Runtime source-boundary review: Agent c064 group composition

Date: 2026-10-20 UTC  
Review: `rt-m2-review-group-c064-source-boundary`  
Plan: M2 groups, option A

## Verdict

**BOUNDED ACK.** Runtime has no source-boundary mismatch for the exact Agent
candidate `c0644cf1a7b63c9bcff7f70502b953a07879c9f3`, tree
`0699f877a4c809005536a80f5956b8051a814ef7`, and schema
`27f2e3edaffdfc49665a858c5c1d6989dd89ef200932679b77367bc459329cfb`.

The existing `/v1` request, provider port, recorder, and commit store already
carry the candidate's generic facts. They do not need a group-specific
authority carrier, DTO, endpoint, materialization API, or Runtime source
change. This is a source ACK only: the current Runtime generated schema is
not being changed or described as carrying the group operations, and this
review does not authorize generation, freeze, pin, adoption, native
qualification, or a public release.

## Exact candidate boundary

The candidate schema independently hashes to the stated `27f2e3ed...` digest
and contains 58 definitions / 32 operation clauses. The only group additions
are:

| Operation | Runtime-visible shape |
| --- | --- |
| `timeline.migrate-groups` v1 | `select: "parent"`, `resolved: []`; closed `groups[]`, each exactly `{legacy_shot_id, shot_id, occurrence_id}` |
| `occurrence.move` v1 | exact occurrence-root selection; closed `{on, track, child_track}`; absolute seconds, explicit parent output lane and raw child lane |

The candidate's stripping evidence remains accepted: removing the two group
definitions/clauses recovers the `392` floor, then the project-data member
removal recovers `613`, and carrier-only removal recovers `6ba`, with the
digests recorded in `design/agent-group-full-union-review.md`. No existing
operation, explicit source-bound v2 branch, or version refusal is replaced.

## Generic Runtime carrier check

The existing Runtime ABI is sufficient at the boundary:

| Candidate fact | Existing carrier / owner | Result |
| --- | --- | --- |
| typed births for migration roots and optional child lane | `CommandRecord.created[]` uses `AgentCreatedID {ref, kind, owner}`; the optional lane birth is an ordinary same-batch `track.create` | carried; Runtime need not interpret group kinds |
| source mapping and exact source/dependency pins | `AgentDependency {key, kind: source/media/transcript/..., pin, policy}` plus the canonical document dependency manifest | carried and checked by the existing request port; Agent owns group source mapping semantics |
| membership/order and collection boundaries | `AgentSelection {key, query_version, owner, members, order, boundaries, policy}` | carried as recorded selection facts; `uniqueItems` and closed shape are schema-validated |
| parent/raw-child lane bindings | `AgentBinding {key, ref, policy, dependencies}` and the command's typed `select`/args | carried; Agent owns singleton/ownership/lane semantics |
| guarded inverse | `AgentWrite` before/after facts, `AgentRead`, `AgentDerivedWrite.cause`, recorder `undo_of`, and existing `timeline.inverse` publication guards | carried and checked generically; no group-specific inverse authority is needed |

The relevant current Runtime contract is visible in
`contract/schemas/edit-command.json` (selection, binding, created, dependency,
write, and derived-write definitions) and
`contract/schemas/timeline-commit.json` (`CommandRecord`). The request port
retains exact captured revision/shot/media/document inputs and refuses changed
captures before acceptance. The commit store validates whole-document digest,
record ordinals, derived-write causes, undo order, restored-source digests,
semantic events, and dependency captures before publication.

## Required semantic boundary

The following remains the Agent/provider responsibility and is covered by the
existing 170-test pure evidence cited by the Agent review:

- migration is lossless, preserves opaque legacy data and provenance, and is
  the sole explicit admission for legacy `pinnedShotGroups`;
- unsupported shared, duplicate, reordered/interleaved, item-bearing,
  mapped, aliased, or otherwise ambiguous legacy shapes refuse atomically;
- `occurrence.move` is fixed, translation-only, single-output-lane movement;
  shared/derived ownership and unsupported source geometry refuse;
- child retrack is atomic, with any new child lane represented only by an
  ordinary typed `track.create` in the same batch;
- the display `pinnedShotGroups` view is derived from current canonical
  membership/order and source geometry; legacy provenance is display metadata,
  not a second authority;
- migration creates shot/occurrence roots only and does not silently refresh a
  sealed capture or manufacture item births (`items: []`).

Runtime preserves this boundary. It accepts and durably records the generic
canonical document/recorder facts atomically, but does not inspect or recreate
group semantics, project a second group store, refresh a sealed capture, or
allocate an item for either operation. Existing closure checks still refuse
duplicate occurrence identity, malformed occurrence order/dependency graphs,
foreign or unavailable captured inputs, and occupied destinations unless the
existing guarded inverse rules authorize the reuse.

## Evidence

Agent pure evidence, reused rather than rerun here:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_composed_schema.py tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_materialization_schema_union.py tests/editing_conformance/test_pristine_initialize.py tests/editing_conformance/test_current_group_slice.py tests/editing_conformance/test_group_read_view.py tests/editing_conformance/test_recipe_m2_group_migration.py tests/editing_conformance/test_recipe_m2_group_move.py
```

Result: **170 passed**, exit 0 (151.88s), as recorded in the Agent source
review. This review did not run a native Agent/Runtime pair, HTTP/live-socket
qualification, generator, artifact write, public freeze, pin, or broad/full
suite.

Runtime bounded checks run on this current integration worktree:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_timeline_commit_validation.py tests/test_timeline_commit_contract.py tests/test_timeline_commit_closure_invariants.py
```

Result: **89 passed in 25.63s**, exit 0.

## Handoff

Runtime ACKs the exact source shape only. Keep the candidate private until
the separately required normal generation, matched native migration-plus-move
proof, and the Agent trusted-bootstrap `record.created` / command `created`
issue are resolved. No Runtime edits were required for this review.
