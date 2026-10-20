# Private temp guarded cleanup — compact design log

- Scope: immediate `/tmp` directories matching `ap2-*`, `app-ap2-*`, `ordinary-*`, or `timeline-normal014-app.*` only.
- Preconditions: predecessor stopped/recycled; no `ORCH/tests/*/running/status` lease; no live cwd/command-line references.
- Cutoff: 20 minutes before the initial inventory at `2026-10-20T17:58:52Z`.
- Action: 38 exact root-owned generated copies/per-run temp roots removed with per-directory age/path/ownership/process guards. No broad-prefix deletion; no source graph/report/archive target was selected.
- Result: 8,192,053,248 apparent bytes removed; 15 newer/uncertain candidates retained for a later sweep.
- No product, Git, worktree, shared dependency, global cache, or test changes.
