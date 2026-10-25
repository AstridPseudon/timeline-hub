## Report

- Ran the sole D97 original selector through central service:
  - Request: `agent-p4-d97-original-0445-1025044719-22560`
  - Result: **PASS**, 1 passed in 28.11s; JUnit time 28.101s, under 45s.
  - Preflight/body exits: `0/0`.
- Controls passed:
  - `bash -n`: `0`
  - Positive stub: exit `17`, exactly one body
  - Poisoned manifest: exit `1`, zero body
- Verified Runtime/Agent lock and schema identities; registry SHA and suite configuration restored byte-identically.
- No product changes; worktree remains clean. Evidence: [receipt.txt](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-P4-D97-original-0445/evidence/receipt.txt)

Caveat for independent GO review: the App integration pointer advanced after the run from captured `1e34f8e…` to `3199118d…`; no recapture or rerun was performed. The launcher had verified the captured tuple before execution. Evidence is 148 KB; `DONE` created.