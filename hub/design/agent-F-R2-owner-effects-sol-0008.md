Fixed all three original R2 failures.

- Nested restoration now recovers occurrence order from authenticated stage partitions. Exact effect comparison remains enforced.
- Successor resolution preserves owner and read-site provenance. Explicit physical reads remain strict.
- Changed two source files and added one focused regression file; original assertions remain unchanged.

Validation on final source:

- **56 passed**, including all three originals and 35 focused regressions.
- **186 controls passed**.
- Before-fix proof: three originals and eight focused positives failed.
- Ruff, private Mypy, vendor-lock, artifact-manifest, and diff checks passed.
- Frozen `34e`/`d106`/`819acf` identities preserved.

Fourteen legacy fixture failures reproduced unchanged on parent source, all missing `_runtime_document`. No full-suite rerun; the retained full result remains **262 failures + 5 errors**.

[Exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-R2-owner-effects-sol-0008/evidence/commands.json) and [source-cause classification](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-R2-owner-effects-sol-0008/evidence/classification.json) accompany 12.8 MB of retained inputs, effects, diffs, and hashes; zero credential fields found.

No scoped blocker. Commit message and `DONE` written. Recommended next step: independent review and normal harness merge.