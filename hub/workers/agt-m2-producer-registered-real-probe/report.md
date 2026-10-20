Blocked on the actual producer seam. The registered assembler writes its artifact, then `publishTimelineRender` fails **before upload/settlement** because it requires a legacy document whose creation route is retired. The route itself remains reachable.

Added two narrow strict xfails preserving completion expectations, covering distinct and duplicate CAS inputs. Existing positives and product code remain unchanged.

Validation:

- Targeted assembler/stitch/hook tests: **14 passed**.
- Existing Runtime publication/cancellation/restart controls: **3 passed**; these SQL-seed the legacy document.
- Central command `request-test agt-m2-producer-registered-real-probe commit-integration --files tests/packs/rendering/test_registered_assembler_producer.py`: **2 xfailed, 2 failed** against Runtime `2c4ac18`. The failures are accompanying M1 schema mismatches.
- Ruff and `git diff --check`: passed.

Native proposal settlement and authorized requester queueing remain unverified. Child outputs are fixtures, not generation qualification.

[Detailed report with exact commands, trace, limits, and smallest next unit](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-producer-registered-real-probe/notes/report.md). Cross-owner handoff, `commit-msg`, and precise `BLOCKED` file written; no `DONE`.