# Runtime group80 contract delta

Date: 2026-10-20 UTC

## Verdict

**Bounded Runtime ACK of the operation shape; adoption remains held on the
private schema composition and native Agent proof.** No Runtime source change,
new DTO, endpoint, provider method, materialization carrier, or authority was
needed for this slice.

The reviewed Runtime base is commit `95202c2b09e83aaae028287d6c59b773410141f3`,
tree `d438d3e28a29ad80fa6b7c19c55e1b7a4485eae2`, with the private 613 schema
(`613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3`). The
Agent group candidate is `80ddba79fa458e7e74e5bdb046424c4e2d979917`; its
private group schema is additive, with 57 definitions / 31 operation clauses
(`c51d71e687e9962fd5309528d6d69d266e319ebffe9a1dc46af20be7add8afc3`) versus
the Runtime base's 55 / 29.

## Exact operation shape

| Operation | Selection | Args | Created facts |
| --- | --- | --- | --- |
| `timeline.migrate-groups` v1 | exactly `parent`; `resolved: []` | closed `groups[]`, each exactly `{legacy_shot_id, shot_id, occurrence_id}` | Agent records the new shot and occurrence roots; v1 creates no items (`items: []`) |
| `occurrence.move` v1 | exact occurrence root, no `::` path | closed `{on, track, child_track}`; absolute seconds, explicit parent output lane and raw child lane | none for the move; an optional same-batch ordinary `track.create` carries any new child-lane birth |

The command envelope already has the required generic carriers: typed root
references, `reads`, selections, bindings, and `CommandRecord.created` facts
with `{ref, kind, owner}`. The Agent remains the semantic owner of group
membership, migration provenance, lane occupancy, source capture, and inverse
meaning. `pinnedShotGroups` remains a read-side compatibility view, not a
second Runtime-owned store.

## What Runtime already covers

- The normal `/v1` commit path can carry both commands. Runtime validates the
  existing request/head/digest/closure/record envelope and preserves atomic
  refusal; it does not need to interpret either operation's arguments.
- The migration's fresh semantic shot root is covered by the existing global
  shot-root identity, created-fact, durable-reservation, and destination
  occupancy checks. The operation's empty item list means no new item map,
  item allocation, or physical item authority is introduced.
- Existing closure validation rejects duplicate occurrence IDs within a
  parent revision and verifies the persisted occurrence rows, while Agent's
  singleton owner and explicit parent/raw-child lane guards own the current
  occurrence slot decision. Occurrence IDs are parent-revision-owned here;
  there is no evidence for a new project-wide occurrence reservation guard.
- Existing materialization owner/source/item/edge checks and
  `_same_materialization_slot` remain intact. They are not a carrier for this
  slice: `occurrence.move` explicitly refuses shared/derived sources until a
  separately qualified carrier exists. No group-specific materialization API
  is warranted.
- Existing CAS/catalog-head and C4 historical-reuse protections are outside
  these args and remain untouched. Neither operation adds media selection,
  catalog writes, or a new dependency authority.

Accordingly, I found no concrete Runtime/Agent guard mismatch requiring a
Runtime implementation change. The one real boundary is artifact state: the
current generated Runtime schema/DTOs are still ordinary 55/29 and therefore
must not be described as carrying group80 yet.

## Exact composition prerequisite

The ordinary 55/29 source is **not** a replacement for the full 613 carrier.
The next private composition must:

1. Start from the complete 357/613 source unchanged: all 55 definitions, all
   29 operation clauses, and all 12 explicit v2 branches.
2. Add exactly `MigrateGroupsArgs` and `OccurrenceMoveArgs` and exactly the two
   group operation clauses above. For the group-only successor this is 57/31.
3. Keep `project-data.write` separate in meaning and review. Its independent
   shape remains v1, `select: "parent"`, args exactly
   `{target, key, value, mode: "replace"}`, writing only the existing
   `parent.config.app[extension_id][key]` path. If one later produces a single
   combined private schema, it must retain all 613 content and add that one
   `ProjectDataWriteArgs` definition/clause as well (expected 58/32), rather
   than replacing 613 with the 56/30 project-data candidate or an ordinary
   partial floor.
4. Only after the combined Agent source is frozen, run the normal generator
   for the Python/TypeScript projections and compare the exact schema/digest.
   Generated DTOs are projections; they do not authorize a Runtime project-data
   writer or group authority.

## Next small task and limits

Compose and normally generate one reviewed private successor from full 613 plus
the separately reviewed project-data member and these two group clauses. Then
run one exact private native migration-plus-move acceptance/readback/retry/
inverse proof against that matched source. The existing Agent report still has
an unqualified trusted-bootstrap issue (`record.created` and command `created`
do not yet align in the failing path), so no accepted migration, public freeze,
release, pin, or App adoption is claimed here. Do not duplicate the Agent
85/401/5 lanes or introduce a native group case in this Runtime review.

## Evidence

Read-only schema inventory probe:

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python - <<'PY' ...
current 55 29 613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3
candidate 57 31 c51d71e687e9962fd5309528d6d69d266e319ebffe9a1dc46af20be7add8afc3
group_ops [('timeline.migrate-groups', '#/$defs/MigrateGroupsArgs'),
           ('occurrence.move', '#/$defs/OccurrenceMoveArgs')]
candidate_additional_defs ['MigrateGroupsArgs', 'OccurrenceMoveArgs']
PY
```

Targeted Runtime guard/generator suite:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python \
  -m pytest -q -p no:cacheprovider \
  tests/test_timeline_commit_type_generator.py \
  tests/test_timeline_commit_contract.py \
  tests/test_timeline_materialization_join.py \
  tests/test_timeline_materialization_authority_review.py \
  tests/test_timeline_projection_ownership.py \
  tests/test_timeline_fresh_bootstrap_scope.py
```

Result: **243 passed, 4 deselected in 157.34s**. No full, live, socket,
regeneration, artifact write, wire commit, or native group acceptance was run.
