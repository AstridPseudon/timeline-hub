Implemented native P2 SWAP replay diagnostics and one registry row.

- D112 control: SWAP 200, Undo 200.
- App-shaped request: fork generated; combined fork+swap returned 409 `dependency_changed`, no receipt, stderr empty.
- Recorded App reason remains `history_unavailable`; fresh reconstruction does not claim the same lower predicate due unavailable original retained history/auth inputs.
- No product files changed.

Tests:

- Python compile, Node syntax check, `git diff --check`: pass.
- Central `full-p2-swap-native-1055`: 1 passed in 37.09s.

Evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-P2-SWAP-replay-return-1055/evidence/native-replay-summary.json`

Commit message and `DONE` marker created.