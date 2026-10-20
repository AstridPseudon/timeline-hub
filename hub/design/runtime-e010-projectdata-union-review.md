# Runtime review: e010 full carrier plus project-data source

Date: 2026-10-20

Result: bounded source ACK for future private counterpart preparation. This is
not a generation, freeze, version, pin, release, adoption, or native-pair ACK.

## Reviewed identities

- Agent source commit: `e010e6a3868e963471244491bb6672c3e4a5135e`
- Agent source tree: `70414cf6875d2c97c45f33e0a5158c80bd7391d9`
- Parent/private952 source: `a53703ce66de7119b6bef51376e274b8ad6296e7`
- New schema: `39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d`
- Frozen private carrier: `613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3`
- Ordinary floor: `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`

The six changed paths are limited to the Agent schema, the project-data
handler, the current command engine's project-data claim path, the focused
project-data tests, and the two carrier inventory tests. No Runtime ABI, DTO,
root/context, or Runtime guard file changes are present. Group80 is not in the
patch.

## Exact source checks

Removing only `ProjectDataWriteArgs` and the `project-data.write` conditional
from e010 reconstructs exactly 55 definitions / 29 clauses and the frozen
613 schema hash. Removing the carrier-only branches from that result then
reconstructs the ordinary 6ba schema hash. Existing definitions and operation
clauses are retained; the candidate is 56 definitions / 30 clauses.

The operation clause and `ProjectDataWriteArgs` definition compare byte-for-
byte at the parsed-definition level with the reviewed standalone `0a/89ed`
feature. `_project_data_commands.py` is also the exact reviewed file
(`aef03cf2bf36a3f18f72cbbb4e0b009f849c9693b40e598f6664a111110e73e0`). The
combined source is therefore distinguished from, and not relabeled as, the
old standalone 89ed schema.

The semantic additions are bounded to one replace-only parent operation:
closed target/key/mode/value validation; opaque finite JSON; absent/null/
empty namespace preservation; disjoint-key rebase; same-key ABA and malformed
namespace refusal; exact inverse and dependent-write refusal. The reviewed
source-map and compiler-canary cases remain one ordered native batch. No group
operation or project-catalog operation is added.

## Runtime generator probe

An in-memory probe fed the 392 candidate schema to the existing
`generators.timeline_commit_types.render()` without writing Runtime files.
It produced a closed `ProjectDataWriteArgs` TypedDict:

```text
{'target': str, 'key': str, 'value': JSON, 'mode': Literal['replace']}
```

The generated command union contained the new closed operation branch, and
`value` resolved to the recursive JSON alias. No `Any` occurs in the new Args;
the existing `Any` uses remain only in pre-existing open canonical payloads.

There is one executable normal-generation prerequisite: the existing Python
root export template (`generators/python_client_init_template.py`) is a static
list and does not export `ProjectDataWriteArgs`. Before generation, Runtime
must add that root import/export and update the 29-operation/41-variant
inventory expectations to 30/42. The generator pin must then advance from
613 to the exact e010 commit/tree/schema; only after that should the normal
generator refresh the checked-in contract bundle and clients.

## Evidence and limits

- Source reconstruction probe: PASS (`613...aaad3`, then `6ba...768f2d`).
- In-memory Runtime generator probe: PASS for closed Args, operation branch,
  recursive JSON typing; root export prerequisite found as above.
- The Agent's previously reported 69 focused tests were not rerun here, per
  the brief. The Runtime 243 broad lane was not rerun. No generation, freeze,
  pin, release, adoption, or native pair was performed.

Normal private generation prerequisites, in order: Agent source review ACK;
Runtime root-export/test-template update; exact source pin update; generated
bundle/client regeneration and checks; then one coordinated native pair after
both source reviews. Public artifacts and ordinary014/public013 remain
unchanged.
