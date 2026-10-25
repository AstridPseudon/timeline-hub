## F-D86 report

Created the metadata-only packet under:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-next-inputs-0314/evidence/`

Eligible set: 32 unique selectors:

- Parent media: 20
- Auto track-label selectors: 2
- Reviewed inverse7: 7
- Reviewed D92 compound: 3

Included:

- `flat-ready-source-selector-manifest.tsv`
- `per-id-eligibility.tsv`
- `set-accounting.tsv`
- `packet-metadata.json`
- Private source/receipt copies with `SHA256SUMS`

Accounting preserves Runtime-owned 161, later102, D91’s separate ten, original dispositions, and held auto/D92 cases. No duplicate scheduling or source/product changes were made.

Validation:

- Manifest and eligibility tables: 32 rows each; canonical sets match.
- Duplicate canonical nodes: 0.
- JSON validation: passed.
- Private-copy SHA256 verification: passed.
- AST parse and in-memory compile: passed for both copied parent sources.
- `git diff --check`: passed.
- Worktree remains clean at HEAD `7e23790248f17b8a4492fc9aee88d2c4e1df328d`.
- No pytest/full suite/Ruff/mypy run; this was source-only metadata work and behavior remains unverified.

Commit message written to the requested path, and `DONE` created. Receiving owner: Agent MAIN affected-node batch.