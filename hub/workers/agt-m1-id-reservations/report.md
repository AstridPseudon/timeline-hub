Implemented provider-only reservations from trusted Runtime history. Retired IDs now conflict on ordinary creation; guarded redo restores the original identity. Previews remain read-only, and moves without creates avoid reservation scans. Corrupt required history fails closed; the verified legacy boundary remains explicit.

Changes: **3 files, +290/−3 lines**; product code **+38/−1**.

Validation:

- Focused provider/recipe neighbors: **186 passed, 1 deselected**.
- Central `commit-integration --files tests/sdk/test_timeline_commit_provider_runtime.py`: **1 passed, 2 failed**. The new real-store test passed restart, retired-ID refusal, exact redo, and receipt retry without execution or reservation checks.
- Both existing CLI journeys failed the schema handshake: Runtime `4e52f7df…` versus client `a32cc6e5…`.
- Scoped ruff, mypy and whitespace checks passed. No full suite or local listener run.

Exact commands and results are recorded in [m1-agent-coordination.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/m1-agent-coordination.md).

Next: review/merge, synchronize the generated client pin, then rerun the central CLI journeys. [Harness commit message written](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m1-id-reservations/commit-msg); no manual git mutation.