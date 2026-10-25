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

## F1 correction and custody

The sole F1 defect is resolved in `evidence/source-recipe.md`: the HTTP 409/static `history_unavailable` observation is now attributed to retained terminal3250 evidence (`app-D127-full-P2-3250-terminal-1421-facts.json`, normal ID `app-pin-fe3309db-d73-p2-fe3309db-submit-1025140943-3250`), while `three-products.p2-popup.spec.ts:495` is explicitly identified only as the failed HTTP 200 assertion. The lower private binding/cause remains `UNKNOWN`.

The source-recipe file changed only one line. Exact SHA-256 custody: old `62503a6fa96b7ebe15410ff72017b7c14994132bd40b3fd671945e8a7e391e0c`; new `9fa32d440a428bdbe05cf3a543ccf78853790b4f8b5a998fdb4e270c82c8e401`. The minimal diff is the final Safe retained result sentence only; source construction, caller facts, JSON, and missing-components evidence were preserved. Copied artifact hashes: source-recipe.json `00f43ce5b3b7640b62b327198f424c01f59c0868eed949e9d10b74d30e579307`, facts.json `e44a5d36a32ddcc5d58b06a5cc176ab9bdab1001195d0e6a51de8d53f7906b1c`, missing-components.md `4572f87ebf38d3ff189019c0969cf06c3c28f0136b847060b50fd3b21ef2b1f8`.
