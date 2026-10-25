**READY_SOURCE — independent recipe review pending.** Created a new source-based `p2-element --submit` recipe and exact committed helper copy at the required persistent paths. All four real detached receipts and App target metadata are retained.

Final STAT/SHA256 checks passed; all four files are regular nonsymlinks, mode `0600`, inside a `0700` evidence directory:

| Output at exact absolute path | Bytes | SHA256 |
|---|---:|---|
| [recipe.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D127-element-durable-recipe-sol-1824/evidence/recipe.md) | 13360 | `3432c22a9c6838b9cda8ef18d71a37591fa8a53a1579664ec67cdfd4efb24254` |
| [source-custody.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D127-element-durable-recipe-sol-1824/evidence/source-custody.json) | 18710 | `4184c934ea6196d364af913494cb83f3c503019dcef32cf9685d2954ecebf132` |
| [readiness.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D127-element-durable-recipe-sol-1824/evidence/readiness.json) | 3674 | `f7e9867935fd469c734a05ed636467a1538f34bdb12dc408cb5f611fd9a900fa` |
| [p2_commit_phase_capture.py](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D127-element-durable-recipe-sol-1824/evidence/p2_commit_phase_capture.py) | 46496 | `4ee0424b63f1f9847995a605dc1050ad7cb8ca75f4d64b8c36d851cfe723f41e` |

Verification:

- `python /tmp/w-3ba02ff44b/d127_prepare.py` — PASS: committed blob equality, source hashes, receipts, detached tuples, metadata, AST parsing, Node20 syntax/resolution and shell syntax.
- `bash -n` on the extracted final recipe shell — PASS.
- Both JSON files parsed successfully; `git diff --check` passed; worktree remains unchanged.
- No tests, preflight, submission, browser/backend, collector, sampler or build ran.

Evidence contradicts the inherited branch’s claimed product-tree equivalence: `d8c0ce8…` contains three tracked evidence additions. The recipe therefore uses the verified clean normal App `d5a1` controller root with exact commit/tree checks; the detached service target and guards remain unchanged.

Historical 1731 raw capture remains absent. The 1630 overall FAIL, corrected 1723 SOURCE PASS, and retained 1738 bootstrap/origin PASS are cited with their limits.

`DONE` and the D127 commit message are present; no source commit is expected. Next: independent recipe review, then a separately dispatched controller with genuine 5.2 GB admission. D130 holds remain unchanged.