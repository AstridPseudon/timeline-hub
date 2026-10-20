**HOLD** on committed port `f511038d`. A real live child’s closed or reused pidfd descriptor falsely produces exit proof, bypassing reuse refusal in a synthetic census. No production close race or external exploit was demonstrated.

- Central `root-prep-current-integration --files "tests/core/execution/test_process_group.py tests/core/execution/test_custody_broker.py"`: **627 passed, 16 Darwin-only skipped, 0 deselected**.
- Local refusal/regression selection: **5 passed**.
- Descriptor probe reproduced the failure.
- Product code and original tests remain unchanged.

[Full review, exact commands and recommended correction](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-main-custody-security-final.md).

Report, commit messages and `DONE` written. No operational blocker; approval requires a corrected committed successor.