## PASS — retained caller migration

Migrated five allowed test files to current public `show`/`apply`/`edit` paths.

- `commands-file` and `apply --native` → `apply <timeline> <sheet> --json`
- `track-label` positives → `show --as sheet --native` → sheet edit → `apply`
- Retired flag cases remain parser-refusal/no-write tests.
- Preserved command, closure, label, opaque/null/absence, retry, history, undo, and output assertions.
- Restore expectations now retain the authenticated current `base_parent` pair (`r1`/`pub1`) explicitly.
- Added required `.path` to fake checkouts.

Targeted result:

```text
92 passed in 102.25s
```

Static checks:

- Ruff baseline: `2148 = 2148`
- Mypy baseline: `1911 = 1911`
- Scoped inherited findings unchanged: Ruff 2, mypy 2
- Vendor lock: PASS
- Artifact manifest: PASS
- `git diff --check`: PASS
- Parameterized/test collection count: unchanged, 92 collected
- No skip, deselect, or xfail markers
- Only the five permitted files changed

The prior qualified full snapshot had 36 failures across these files; the full suite was not rerun per the brief. Independent Luna review and merge remain external follow-ups.

Commit message written and `DONE` marker created.