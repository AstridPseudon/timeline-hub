## Result

Blocked at a genuine C0 contract seam; no product or test files changed.

Runtime currently normalizes `parent/collection:asset` to:

```json
{"kind":"scope","ref":"parent","path":[]}
```

Evidence:

- Runtime `timeline_commit_auth.py:123-129, 387-403`
- Agent `_command_state.py:410-420`
- Agent `_collections.py:50-55`
- Native producer `native_occurrence_media_commands.py:114-125`

The Agent held source instead projects the same read to `parent/config/registry/assets` (`_commit_patch.py:104-109, 524-537`). This loses the fact that the captured shape spans both raw and config registry mirrors. Replacing it with the Runtime root scope satisfies `covers()` but causes Agent `rebase_patch()` (`_commit_patch.py:921-952`) to conflict with unrelated parent edits.

C0 supports only single-path `field`, `collection`, or `scope` dependencies (`contract/schemas/timeline-commit.json:128-175`). It has no representation for a multi-location logical collection shape preserving both mirror presence/null/value states while remaining narrowly mergeable.

Precise contract question: should C0 add an authenticated multi-location logical-shape dependency, or explicitly authorize separate Runtime authentication and Agent rebase/undo guard representations for this native read? No safe producer-only mapping exists under the current contract.

Later single-author ownership:

- Runtime: `runtime_protocol/timeline_commit_auth.py`, only if the contract decision changes auth encoding.
- Agent: `astrid/sdk/timeline/_commit_patch.py`, sole producer pairing after that decision.
- Proof selector: the existing six-case `tests/editing_conformance/test_commit_runtime_parent_auto_completion.py::test_disjoint_head_accept_reload_exact_retry_undo_redo_and_reserved_id`.
- Existing auth controls: `tests/test_timeline_commit_authentication.py::test_native_assembly_aliases_authenticate_at_the_sealed_boundary`.

Checks:

- In-memory Runtime and held Agent compile: PASS.
- Scoped Ruff on Runtime auth and Agent `_commit_patch.py`: PASS.
- `git diff --check` and source equality checks: PASS.
- Mypy baseline: 268 pre-existing errors across 23 imported files; no changed source implicated.
- No pytest, collection, fixtures, services, browsers, or full suites run.

`DONE` and the required commit message were created.