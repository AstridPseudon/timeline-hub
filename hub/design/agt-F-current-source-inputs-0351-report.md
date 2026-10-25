# F-D86 report

Prepared lossless source-delta evidence against Agent normal:

- Commit: `68404b8484749d1d8ec2bdaef34faa004ad87dbe`
- Tree: `bc0eaa245fe5ec6f16b17b3b64c2b499f85e82f2`

Results:

- 27 unique ready selectors.
- 20 exact MAIN overlaps retained but not duplicated.
- 10 explicit held IDs.
- 49 pending IDs: word-bootstrap46 and D92×3 lack normal-home receipts in the fixed base.
- No repository files changed.

Evidence:

- [selectors.txt](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-current-source-inputs-0351/evidence/selectors.txt>)
- [per-id-source-map.tsv](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-current-source-inputs-0351/evidence/per-id-source-map.tsv>)
- [source-manifest.json](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-current-source-inputs-0351/evidence/source-manifest.json>)
- [receiving-handback.md](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-current-source-inputs-0351/evidence/receiving-handback.md>)

Checks:

- In-memory AST compilation: PASS.
- Scoped Ruff: PASS.
- Scoped mypy: PASS, 9 files.
- `git diff --check`: PASS.
- Worktree: clean.
- No pytest, collection, fixture/helper execution, services, probes, installs, or full suites run.

Completion marker and commit message were written; `DONE` created.