Registered the isolated suite atomically, preserving the predecessor and all outside bytes, including the existing observer-suite row. No tracked files or original probe code changed.

- Ran `bin/request-test rt-D83-seed-service-sol-2040 d83-native-local-integration --no-cache`, then waited on result `rt-D83-seed-service-sol-2040-d83-native-local-integration-1024204027-15384`.
- **Result: exit 1; 7 passed, 1 failed, 1 deselected in 145.18s.** All eight seed commits accepted. N=4/observer-on timed out during the subsequent history read.
- Ruff, scoped Pyright, compile and `git diff --check` passed. [Exact commands and results](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D83-seed-service-sol-2040/evidence/commands.md>).

Seed targets took **1.56–8.48s**. N=4/on provider time was **7.42s wall / 7.32s thread CPU**. Maximum real acquisition elapsed across all variants was **2.09ms**. These controls support compute cost; they establish no seconds-long lock wait. Acquisition rows lack caller stacks, so the maximum cannot be assigned to a unique source line.

The optional comparison was submitted despite a failed source check: integration had advanced beyond exact `4351`. I cancelled it and excluded all partial results; no retry followed.

Hand back to Runtime owner2031. The original 33s interval remains unattributed: generated-media commands, the final document patch and App2026’s request/dump correlation remain missing. D80/P4/R2 common cause remains a hypothesis.

[Detailed handoff and evidence](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D83-seed-service-sol-2040/evidence/handoff.md>). Raw artifacts are retained at `0600`; commit message and `DONE` are written.