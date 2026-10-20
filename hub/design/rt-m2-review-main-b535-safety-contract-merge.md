# Runtime b535 merge-forward review

**Decision: APPROVE the Runtime merge; hold downstream adoption.**

`8bd92de` is a genuine two-parent merge of Timeline `7a956c0` and upstream `b535646`, with common ancestor `240d5bb` and merged tree `d964d713`. Main Windows realm admission, SQLite URI/read-write/WAL safeguards, IPv6/identity restrictions, worker handoff, and Timeline commit authority remain intact. No first-parent deletions or conflict artifacts were found.

The target's 76-artifact regeneration is expected: first parent had 75, upstream had 69, and the only artifact-set addition is `contract/schemas/services.json` with the corresponding generated health/service projections. Runtime metadata is internally exact at contract `0.2.13`, schema digest `sha256:14a8757db22ca98cd6fd2ce4f41ff3ac71aa3e4d616c1e15856c88a325e7fa90`, artifact version `sha256:e7d0390075eeef189516bb710dac01bf307be651c819992cc6905b59958990db`, and 133 operations.

Agent/App still advertise the old schema digest `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`; App fails closed on that mismatch and its Health DTO lacks the new fields. This is a required coordinated tuple, not a reason to rewrite the Runtime merge or silently accept the old digest. No release/pin decision is implied.
