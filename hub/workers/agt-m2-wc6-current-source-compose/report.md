Implemented the reviewed WC6 slice on current Agent source:

- Native bounded document-script publication and same-alias media rebinding.
- Authenticated media selection/verification plumbing.
- Strict accepted-payload inverse guard and scalar media manifest fix.
- Correct dropped-HTTP-ack retry proof.
- Preserved current P1/F1 authority and held legacy/narration paths.

Tests:

- Targeted WC6 tests: **12 passed**.
- Central `targeted --files "tests/timeline/test_authoring_media.py"`: **71 passed, 1 deselected**.
- Ruff: **passed**.
- `git diff --check`: **passed**.
- No full suite run.

Required [design note](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-wc6-current-source-compose.md>), commit message, and `DONE` marker were written.