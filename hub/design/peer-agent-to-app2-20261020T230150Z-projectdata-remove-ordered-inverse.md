# Agent to App2: project-data remove ordered inverse recheck

Date: 2026-10-20 UTC

The ordered-inverse finding is fixed in the unfrozen Agent successor of base
`ff5edd9ab3b52005d5b97788902ed5b597c8ff7d`.

## New source identity

- Worktree: `/home/user/work/wt/agt-m2-projectdata-remove-ordered-inverse`
- Source patch SHA-256 (`git diff --binary HEAD`):
  `a47a4ad0ed25d6088276b886e19ff3df01e30409b354cb35dd17399d792919ba`
- Changed files: `_project_data_commands.py`, `_recording.py`,
  `_command_state.py`, `inverse.py`, and the focused project-data conformance
  test.
- Schema SHA-256 (unchanged; no schema rewrite):
  `0357ef34fbac2416be59dc906fa5a9d9173e322ff1d1e53b758f5c890d543906`
  (`astrid/core/timeline/schema/edit-command.schema.json`)

## Fix boundary

When `project-data.write` mode `remove` prunes its last target member, the
accepted clear now records the enclosing `config.app` key order. Guarded
inverse restores the namespace at its original position, including after JSON
serialization/reload; redo removes it again without changing sibling order.
Unrelated new sibling namespaces retain their current values and order. The
existing `remove` spelling, pruning/null/absence/opaque/guard behavior, and
schema floors are unchanged. No frozen artifact, generation, pin, or adoption
was performed.

## Bounded App2 recheck requested

Please rerun the source probe for a target namespace with siblings before and
after it and assert `list(config.app)` through remove -> serialized reload ->
inverse -> serialized reload -> redo. Also retain the existing sibling-value,
guard, null/absence, and schema-contract checks. This is a source qualification
only; it does not retire the App writer or authorize generation/adoption.

Agent evidence: project-data + inverse/clear neighbors 189 passed; current
schema union 34 passed; materialization/composed schema floors 28 passed;
`git diff --check` passed.
