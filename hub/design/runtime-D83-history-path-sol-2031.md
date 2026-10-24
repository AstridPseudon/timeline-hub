Implemented one D83 correction: `_capture_projection_equal` now uses temporary shallow projections instead of copying complete payloads. Recursive comparison and fresh schema/authentication checks remain intact.

- **Source support:** authentic profile14690 attributes 4.135s to copies from this helper. Raw summary/events/profile hashes and 54 handler pairs verified.
- **Measured result:** retained-capture median CPU fell **4.28%**, 0.330514s → 0.316378s per three verifications. All 40 validation/keyword/type/equality count frames match. Individual rounds were noisy.
- **Tests:** **289 passed in 86.48s**, plus **96 passed in 20.40s**; zero failures/errors/skips. Includes 31 new projection tests and strict schema, authentication, history, event, ABI, reservation and inverse-range controls.
- **Static:** Ruff, baseline/candidate Pyright, compilation and `git diff --check` passed; zero new diagnostics.

Changed Git blobs:

- `timeline_commit_auth.py`: `dddabb1a11e7c9b010d294f9db3765f771cd8cd8`
- `test_timeline_capture_projection.py`: `7486b460b999a3ee4d44d412e625434ef1152059`

[Exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D83-history-path-sol-2031/evidence/commands.txt). Adjacent artifacts contain XML, logs, exits, origins and measurements.

No blocker. Commit message and `DONE` written. **One independent security review remains before merge**, followed by the orchestrator’s batched original run. No further source change proposed. Original 45s acceptance and shared lock-wait causality remain unverified.