# Agent group full-carrier union review

Date: 2026-10-20 UTC

## Verdict

**APPROVE the private Agent source candidate only.** Public freeze, normal
generation, artifact/pin, Runtime native qualification, App adoption, and
integration remain held.

## Exact candidate identity

- Branch: `tl/agt-m2-group-full-carrier-source-compose`
- Commit: `c0644cf1a7b63c9bcff7f70502b953a07879c9f3`
- Tree: `0699f877a4c809005536a80f5956b8051a814ef7`
- Exact parent: `e010e6a3868e963471244491bb6672c3e4a5135e`
- Candidate schema SHA-256: `27f2e3edaffdfc49665a858c5c1d6989dd89ef200932679b77367bc459329cfb`
- Candidate schema inventory: 58 definitions / 32 operation clauses
- Added operations: `timeline.migrate-groups` and `occurrence.move` only

The group-specific implementation and conformance files are unchanged from
reviewed `80ddba79fa458e7e74e5bdb046424c4e2d979917`. The shared registry,
schema, and union-test files also carry the separately reviewed full-carrier
project-data member already present in exact parent `e010`. The complete
`80ddba79 → c0644cf1` delta is that project-data composition; this is not a
re-review or replacement of the group source.

## Independent checks

Removing only the two group definitions and their two operation clauses from
the candidate reconstructs the exact project-data floor:

| Source | Definitions / clauses | SHA-256 |
| --- | ---: | --- |
| Candidate | 58 / 32 | `27f2e3edaffdfc49665a858c5c1d6989dd89ef200932679b77367bc459329cfb` |
| Remove group delta only | 56 / 30 | `39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d` |
| Then remove project-data member | 55 / 29 | `613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3` |
| Then remove carrier-only additions | 55 / 29 | `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d` |

Existing definitions, operation clauses, the 12 explicit source-bound v2
branches, and version refusals remain covered by the union/floor tests. No
copied frozen schema, new framework/DTO/source field, generation, freeze, or
public pin was added. `git diff --check` is clean.

The exact targeted command was:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_composed_schema.py tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_materialization_schema_union.py tests/editing_conformance/test_pristine_initialize.py tests/editing_conformance/test_current_group_slice.py tests/editing_conformance/test_group_read_view.py tests/editing_conformance/test_recipe_m2_group_migration.py tests/editing_conformance/test_recipe_m2_group_move.py
```

Result: **170 passed in 151.88s**, exit 0.

## Semantic boundary

The reviewed migration remains the sole explicit admission for legacy
`pinnedShotGroups`; ordinary edits still refuse an unmigrated legacy group.
Migration records canonical shot/occurrence ownership, complete legacy
provenance, source/dependency bindings, and lossless inverse data. It refuses
unsupported maps, interleaving, duplicate/shared members, occupied or
ambiguous shapes, and item-bearing births without an explicit mapping. It does
not silently refresh a sealed capture or manufacture physical item births.

`occurrence.move` remains the bounded fixed, translation-only,
single-output-lane operation. It uses explicit parent and raw child lane
bindings, preserves authored child geometry and opaque state, refuses shared
or derived ownership, and allows an optional caller-allocated child track only
as an ordinary typed `track.create` in the same batch. The pure group view
derives current canonical membership/order and source geometry; legacy
provenance supplies display metadata only.

These behaviors are unchanged from reviewed `80dd`; the candidate adds them
to the complete `e010`/392 floor rather than changing chapters-as-shots,
lossless migration, or existing v2/source-bound semantics.

## Cross-area handoff requests

**Runtime:** please provide a bounded source ACK for this exact
`c0644cf1`/tree/schema composition, confirming that the existing group80
operation shape and full 392 carrier remain the accepted source boundary.
This requests no Runtime source change, generated DTO, artifact, generation,
freeze, pin, or native acceptance. The existing Runtime group80 contract
remains the limit: no group-specific materialization carrier or authority is
introduced.

**App2:** please provide a bounded consumer/source ACK against the exact
candidate identity. The read-side bindings and derived `pinnedShotGroups`
view are available for adapter review, but App adoption is not implied. The
three original App visible assertions remain a consumer gate, not a result of
these pure Agent tests: free multi-clip drag, pinned-group cross-track drag,
and pinned-group drag onto a new track/retrack. They must be restored and
qualified by App against accepted readback before adoption or writer
retirement.

No full suite, HTTP/live socket, native qualification, artifact generation,
sealed-capture refresh, or App browser run was performed or inferred.
