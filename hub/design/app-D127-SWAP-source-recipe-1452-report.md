# D127 report

Completed the finite read-only SWAP source handoff. No product files changed; worktree remains clean.

Artifacts:

- `evidence/source-recipe.md`
- `evidence/source-recipe.json`
- `evidence/facts.json`
- `evidence/missing-components.md`
- Commit message: `docs: D127 finite SWAP source recipe`
- `DONE` marker created

Key handoff: `seedThreeProducts(15, 'native-none', 12)` → shared occurrence placement at `12s` → old-media registration → mounted SWAP → authenticated selections → `occurrence.fork` followed by `occurrence.swap-media` → persisted outbox → registered `commitTimeline` Runtime caller.

Original popup source SHA verified:

`09f5e2c2ea2a207575534a88adf2847d68cdd389caa5d145580100f21302b2b9`

Checks passed:

- JSON validation with `python -m json.tool`
- SHA-256 custody comparison against committed blob
- `git status --short` clean
- `git diff --check` clean

Tests/types/lint were not run, as instructed for this read-only task. The original3250 private SWAP body, concrete historical IDs, provider output, closure bindings, and lower `history_unavailable` cause remain explicitly missing; no inference or replay claim was made.