Implemented the private `occurrence.resize@1` source proposal.

- Writes only `occurrence.duration_ms`; preserves identity, placement, shot pin, maps, and opaque fields.
- Added schema/registry wiring and conformance tests for 3000→4150 ms, inverse/redo, ABA, disjoint rebase, invalid values, and missing identity.
- Candidate schema hash: `79c54f0ba6ddb1028a90f8e5545ece68a34fa156a3642b14fea550a8f02da0c2`.
- Tests: targeted lanes passed (`29 passed`, `53 passed`); Ruff, JSON validation, and `git diff --check` passed.
- Broader neighboring lane: `199 passed, 3 pre-existing unrelated failures`.
- No full/native HTTP/generation/pin/release run. Peer ACK remains required.
- Parent `config.duration`/ripple extent remains a separate authored gap; no root writer added.

Files: [resize command](</home/user/work/wt/agt-m2-occurrence-duration-carrier/astrid/sdk/timeline/native_occurrence_resize.py>), [tests](</home/user/work/wt/agt-m2-occurrence-duration-carrier/tests/editing_conformance/test_recipe_occurrence_resize.py>), [handoff](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-occurrence-duration-source.md), [report](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-occurrence-duration-carrier/report.md>).