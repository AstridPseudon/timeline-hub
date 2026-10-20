Implemented native proposal production and normal host settlement. Stitch aliases remain `rendering.render`; native proposals never commit with worker authority.

Validation:

- Focused pytest: **92 passed** across assembly, sync, stitch, and assembler tests.
- Central `identity-pin94114269-integration --files tests/packs/rendering/test_registered_native_pair.py`: **4 outer passes**; private suite **4 passed, 2 unchanged strict xfails**.
- Ruff and `git diff --check` passed. Cycle check retains the verified baseline failure.

The private pair qualifies actual registered-host artifacts and settled associations. Published schemas/pins remain untouched. Requester commit/restart, lost-ACK admission durability, and registered render remain unqualified.

[Detailed report with exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-registered-native-proposal-output/notes/report.md)

Commit message and `DONE` written. No blocker.