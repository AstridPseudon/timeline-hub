Completed on base `6e21b74ff99029929e76cc39ab9e178e8f01396e`. Only the four owned files changed. Production harness/launcher and bootstrap-test bytes match donor `f09c357`; D110 manifest and all unowned files remain unchanged.

Removed D102/D105’s mandatory historical-object lookups. All 27 D66 cases remain: 25 test bodies are donor-identical; the two restructured controls retain every current-behavior assertion. Added seed-phase byte preservation across two later starts. Historical old-RED controls remain separate evidence.

Validation with `/opt/node20/bin/node`:

- `--test scripts/testing/d66-plain-stack.test.mjs`: **27 passed**.
- Same exact test bytes in a source snapshot without `.git` or pre-squash objects: **27 passed**.
- `--import tsx --test tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts`: **1 passed, 2 failed**. Parent bodies reproduce both failures: unavailable helper and missing Runtime Python executable.
- Both App/Node `tsc --noEmit`, scoped four-file ESLint with zero warnings, both MJS syntax checks, and `git diff --check`: **passed**.
- Separate historical controls: **2 passed**. Current D105 against immutable old harness: **expected assertion failure**.

The real production caller control preserves one seed plus two valid stage-2 starts, distinct `0700` namespaces, `0600` evidence, and existing cleanup. Concurrent allocation was source-audited; cross-process concurrency and browser gestures were not executed.

Full commands, logs, hashes and predicate accounting are in [evidence]( /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P2-phase-sink-portable-sol-0726/evidence/checks.md).

`commit-msg` and `DONE` written. No implementation blocker; the two parent bootstrap failures remain unchanged. Next step: manager-owned independent review.