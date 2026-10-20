# Agent M2 canonical-group full-carrier source candidate

Status: private source candidate only. No public freeze, generated artifact,
pin, activation, Runtime source change, native qualification, or App adoption.

## Exact basis and composition

- Base: `e010e6a3868e963471244491bb6672c3e4a5135e`.
- Reviewed group source: `80ddba79fa458e7e74e5bdb046424c4e2d979917`, applied as
  the exact reviewed semantic/schema/capture delta.
- Runtime shape ACK: `scratchpad/orch/design/runtime-group80-contract-delta.md`.
- Candidate schema SHA-256: `27f2e3edaffdfc49665a858c5c1d6989dd89ef200932679b77367bc459329cfb`.
- Candidate schema inventory: 58 definitions, 32 operation clauses.
  The two added operation clauses are exactly `timeline.migrate-groups` and
  `occurrence.move`; `project-data.write` remains present.
- Working-tree content digest (sorted tracked and non-ignored candidate files,
  path and bytes):
  `1964d2fca33c65cb66f829bda824916e4b0b67b29d32d0f6e09ead1212615f3e`.
  A commit/tree SHA is pending the harness commit because this worker cannot
  write the repository index or create commits.

Schema-floor checks reconstruct the prior floors by removing only the intended
additions:

- ordinary: 55 definitions / 29 operations, SHA-256
  `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`;
- full carrier: 55 / 29, SHA-256
  `613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3`;
- full carrier plus project-data: 56 / 30, SHA-256
  `39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d`;
- composed candidate: 58 / 32, with only the two group clauses added to the
  56 / 30 source.

## Source behavior

The candidate registers the reviewed migration and occurrence-move commands,
records canonical ownership/capture data, uses chapters-as-shots, preserves
source-bound allocations and authoring guards, and keeps the read-side
`pinnedShotGroups` projection migration-only. Legacy groups require the sole
recorded migration command; unsupported timing/maps, interleaving, duplicate
IDs, shared sources, occupied lanes, and malformed shapes refuse without
mutating the draft. Existing inverse, order, concurrency, materialization,
and version behavior remains in place.

## Evidence

Command run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_composed_schema.py tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_materialization_schema_union.py tests/editing_conformance/test_pristine_initialize.py tests/editing_conformance/test_current_group_slice.py tests/editing_conformance/test_group_read_view.py tests/editing_conformance/test_recipe_m2_group_migration.py tests/editing_conformance/test_recipe_m2_group_move.py
```

Result: **170 passed in 178.07s**. `git diff --check` is clean.

No full suite, localhost/browser/live-socket suite, HTTP/native-pair test,
schema regeneration, artifact write, release, or frozen branch mutation was
performed. Native remains unqualified pending a separately generated and
agreed counterpart. No new cross-area semantic decision was needed.
