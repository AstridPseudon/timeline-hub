## Completed

- Migrated the motion/scoped-media fixture from retired `publish_parent_composition` to the existing `seed_trusted_parent` Runtime fixture helper.
- Preserved all original payload values and assertions.
- Changed only `tests/v10/test_domain_cli_projects_timelines.py`.

## Tests

Passed:

```text
3 passed in 5.67s
```

Command included the changed test and both parser-alias acceptance nodes.

Also passed `git diff --check`.

Ruff: 3 pre-existing findings, unchanged from base.  
Mypy: 15 pre-existing findings, unchanged from base.

The known aggregate Runtime failure was not repeated.

Commit message written to the requested path; `DONE` marker created.