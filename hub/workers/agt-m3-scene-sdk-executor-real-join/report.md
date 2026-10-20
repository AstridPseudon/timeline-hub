Implemented D09 SDK/executor join alignment.

- Updated SDK and fixture to consume the actual executor field `entrypoints.scene`.
- Preserved strict ZIP, digest, provenance, map, label, and advisory-`UNAVAILABLE` validation.
- Appended exact contract/boundary to the shared D09 handoff.
- Added flat Viewing peer note requesting existing receipt provenance population.
- No `run.py`, Root-prep, projector, validator, authority, save, or DTO changes.

Tests:

```text
89 passed
1 transport candidate source test passed
2 saved/candidate preparation tests passed
```

Native renderer test remains blocked by missing Remotion/React peer dependencies. Ruff reports 10 pre-existing module findings; `git diff --check` passes. No full suite requested.

Current managed positive join and ordinary activation remain unverified until Viewing adds receipt provenance. `DONE` and commit message files were created.