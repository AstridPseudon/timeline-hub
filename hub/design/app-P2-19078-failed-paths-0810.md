# Report

Completed read-only actual19078 failed-path investigation.

- Corrected arithmetic: 4 PASS / 2 FAIL / 1 ERROR / 1 NOTRUN; readiness separate at 1 PASS.
- Attributed failures:
  - SWAP: observed POST 409 `history_unavailable` at `p2-popup.spec.ts:495`.
  - Element: missing `applied` status after 5s; request outcome UNKNOWN.
  - Placement: 90s commit-response wait timeout; downstream outcome UNKNOWN.
- Runtime namespace-to-gesture correlations remain UNKNOWN; no Runtime repair or waiver made.
- Preserved erroneous producer terminal note unchanged.

Outputs:

- [19078-failed-paths.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P2-19078-failed-paths-0810/notes/19078-failed-paths.json)
- [19078-failed-paths.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P2-19078-failed-paths-0810/notes/19078-failed-paths.md)
- [corrected-terminal.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P2-19078-failed-paths-0810/corrected-terminal.md)

Verification:

- Artifact JSON/XML and four trace archives parsed successfully.
- Source hashes matched retained manifest.
- `git diff --check` passed; worktree clean.
- No tests, browser, TypeScript, lint, backend, or full suite rerun, as instructed.

Requested R4 control-doc path was absent. `DONE` and commit message were created.