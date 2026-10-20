Implemented and handed off.

- Routed native CLI trim through existing `TimelineSession.trim` verified preflight.
- Added CLI forwarding regression.
- Tests:
  - `test_cli_commit_trim.py` + trim recipe: **138 passed**
  - CLI/native neighbors: **79 passed**
  - `git diff --check`: passed
- Runtime rerun request published for only the two original failed nodes.
- Runtime journey remains unverified downstream.
- Commit message written; `DONE` marker created.