# App review: combined Agent project-data source contract

Date: 2026-10-20 UTC

## Decision

**APPROVE the exact combined Agent source floor for cross-area contract purposes.**
This is an ACK of the source/schema contract only. App native activation, Runtime
provider qualification, pinning, generation, adoption, and legacy-writer retirement
remain held until a fresh matched counterpart is proven.

## Reviewed identity

- Agent commit: `e010e6a3868e963471244491bb6672c3e4a5135e`
- Agent tree: `70414cf6875d2c97c45f33e0a5158c80bd7391d9`
- Parent/private pin: `a53703ce66de7119b6bef51376e274b8ad6296e7`
- Parent tree: `d0e6f57acb8d806cb0cf9065eb12c36e1ee28e94`
- Schema SHA-256: `39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d`
- `_project_data_commands.py` SHA-256: `aef03cf2bf36a3f18f72cbbb4e0b009f849c9693b40e598f6664a111110e73e0`
- `commands.py` SHA-256: `302f8ab7130dd618e93d4e8aaab6164f26f5e3d43c961d52ba9ddbc68be0f3cf`

The source diff is limited to the schema, project-data handler/registry, focused
conformance tests, and the two existing union tests. `git diff --check` passes.

## Contract ACK

The new closed operation is exactly `project-data.write` v1, selected at `parent`,
with args `target`, `key`, `value`, and `mode: "replace"`. It writes exactly one
leaf at `parent.config.app[target][key]`; it preserves sibling keys/namespaces and
finite JSON opaquely. Original leaf guards remain authoritative. Only missing,
null, or dictionary setup-container claims may merge through disjoint-key rebase;
malformed namespaces, same-key ABA, dependent later writes, and strict inverse
dependencies refuse visibly.

The combined schema has 56 definitions and 30 operation clauses, with the 12
pre-existing v2-capable clauses unchanged. Removing only `ProjectDataWriteArgs` and
the `project-data.write` conditional reconstructs private carrier
`613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3`; the ordinary
reconstruction remains `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.
The 0a/89ed project-data guard semantics are retained; the e010-vs-0a source diff
contains only the already-pinned materialization changes outside the project-data
handler/guard semantics.

No old 357/613 or 0a/89ed frozen ref was mutated, and there is no new group,
transition, generator, endpoint, DTO, store, public pin, client vendoring, or
source edit.

## App boundary and future hold

App’s strict preflight remains narrow: reject reserved outer keys and non-canonical
keys, do not broaden nested-value JSON acceptance, trim/adopt/rename keys, normalize
merge into replace, reorder operations, or adopt malformed namespace shapes. The
current App public patch vocabulary is not native EditCommand support.

Any future App producer must first emit a fresh v2 capture with the required
materialization/source prerequisites and exact original guards. It must not silently
adopt old sealed v1 captures or claim compatibility by relabeling/regenerating them.
The future App/Runtime pair must qualify this exact 56/30 source through the existing
`/v1` path, including accepted-record identity, retry/restart, mixed-batch atomic
refusal, dependent same-leaf refusal, disjoint rebase, and exact inverse behavior.

## Evidence

Ran against one private archive of the exact Agent commit, using the shared read-only
Python environment (no dependency changes):

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PRIVATE" \
  /home/user/work/venv-app2-native/bin/python -m pytest -q \
  -o addopts= -p no:cacheprovider \
  "$PRIVATE/tests/editing_conformance/test_recipe_m2_project_data.py" \
  "$PRIVATE/tests/sdk/test_timeline_materialization_schema_union.py" \
  "$PRIVATE/tests/sdk/test_timeline_current_union_schema.py"
=> 69 passed, 2 warnings in 160.30s
```

Reused unchanged-tree App evidence from the prior guard review: project-data
helper/timeline-patch focused lane `76 passed`, compiler-canary lane `6 passed,
53 skipped`, and source-map lane `3 passed, 28 skipped`. No full suite, browser,
localhost, live socket, Runtime HTTP, dependency install, pin, generation, or
integration adoption was run.

## Recommended next step

Hold the source as approved, then require one exact current App consumer + Runtime
provider qualification before any native activation or legacy-writer deletion.
