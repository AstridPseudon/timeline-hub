## Report

Submitted one authorized normal run:

`request-test integration:agent p4-current-becfe-http-3legs --no-cache`

Tuple:

- Agent `c2a63bbee9369b84bec7f4bfec06f447df02c27b`
- Runtime `732c48c6f5a9441a65c61b24595d454a1cd3e180`
- App `5fcb9ad5cf8af93709d682ab994bcdb1af207f07`
- Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`

Preflight passed: parsed command `bash -n=0`; positive stub exit 17/one call; poison exit 1/zero calls. Disk remained above the 6 GB floor. `P4_LIVE_PROFILE_DIR` was unset.

Service ID: `agent-p4-current-becfe-http-3legs-1024221732-29429`

Results:

- Ten-note: 45.314s — FAIL/timeout
- `[False-None]`: 10.486s — PASS
- `[False-public-element]`: 11.308s — PASS
- `[True-None]`: 7.360s — PASS
- `[True-public-element]`: 7.470s — PASS

Board timing: **4/5 passed; 1 timeout; JUnit 84.318s, service wall 88s against 45s per-original.**

Automatic result: NO-GO, exit 1. No rerun or diagnosis was performed. Worktree remains clean; no product edits. Evidence is under the assigned `evidence/` directory, and `DONE` plus the required commit message were created.