# P4 HTTP seed first return

## Change

`tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py` now builds the
trusted isolated baseline from the existing `initial_bundle()` via
`compile_authoring_candidate(source).publication["parent_composition"]`.
That normal constructor preserves the complete authored parent payload and
derives the empty `occurrences` collection. Setup adds only
`parent.setdefault("registry", {})`, the required Runtime-managed canonical
envelope field; it does not register media or alter the shared seed helper.

The post-seed assertion explicitly compares the complete source parent plus
the empty Runtime registry wrapper, preserving the original command/edit/raw,
sibling, CLI, show, history, and guard assertions.

## Evidence

- Exact integration node collection: **PASS**, 1 collected.
- Offline Agent canonical-document verification: **PASS**.
- Offline Runtime `PreparedCommit` schema verification: **PASS**.
- Ruff: **PASS**.
- private mypy: **PASS**.
- `git diff --check`: **PASS**.

The live HTTP/socket test was not run by this worker per the brief. Manager
owns the one existing failed-node retry after independent review.
