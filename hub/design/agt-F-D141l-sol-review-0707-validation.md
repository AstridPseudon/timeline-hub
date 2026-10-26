# F D141l Sol0638 validation

## Commands run

- `/home/user/work/venv-agent/bin/python -P /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-command-sol-0638/evidence/check-source.py check` — exit `0`; `control_status=PASS`, `pair_status=BLOCKED_EXISTING_CONTROLLER_BINDING_MISSING`, 10 admission cases and 36 lifecycle cases. New checker log: `control-logs/check-1792998822405145402.json`, SHA-256 `23daf2d2db5d924a2e09e5a4cd4ac96b15ffa94a7418a49cde7f2475d8a942af`.
- `bash -n` on `command-cut.sh`, `command-pristine.sh`, `positive-stub.sh`, and `tiny-controls.sh` — all exit `0`.
- `bash .../tiny-controls.sh` — positive `exit=17 calls=1`; poison `exit=1 calls=0`; both expected values matched.
- Read-only `git rev-parse HEAD HEAD^{tree}` and clean-status checks on the four current paths and two pristine paths — exact expected tuples, all clean.
- Checker-backed source existence check — all 22 cut and 17 pristine selectors exist; the five absent pristine own-ID roots are separately source-backed N/A.
- Read-only current caller trace — `request-test` validates suite registration and queues a request; `test-run` resolves the exact registered row, snapshots the target, invokes its production measured-floor validator when attached, and runs the registered command. The current rows do not point to Sol0638: `agent-core-full` remains 0309 + 0249, and the pristine row remains the old 0030-era command.
- Read-only production caller trace — Runtime `service.py:2469` `commit_timeline` validates the v2 request and calls `_execute_timeline_commit`; the normal provider path reaches Agent `commit.py` through the existing runtime execution module. No second writer or alternate executor was introduced.
- D89d arithmetic — `X=514564096`; dispatch floor `4714564096`; source preparation only enforces continuous stop `4000000000`. The controller dispatch floor is not re-gated by preparation.
- `git diff --check`/status on this review worktree — clean before artifacts; no product files were changed.

## Control observations

The checker independently exercised the actual shell functions with isolated
fixtures, not copied PASS declarations. It rejected malformed, missing,
self-authorized, wrong-service, wrong-controller, wrong-schema, mutated-receipt,
and mutated-brief admission inputs. It exercised success/body-17, missing and
bad JUnit, JUnit-failure-with-zero-body-exit, empty raw streams, KEEP/source
tampering, below/equal/above stop floor, disk read/write failures, monitor
stop/read/write failures, real five-second cadence, and TERM for both command
modes. It checked parseable nonempty XML, raw-to-runner dataflow, exact content
hashes, inode/owner/mode custody, source before/after equality, final status
ordering, and post-seal mutation rejection.

The unchanged launcher was invoked only with the approved tiny stub and current
manifest. Positive materialized the stub and returned 17 with one call; the
agent-SHA-only poison refused before the stub with exit 1 and zero calls. These
controls do not run pytest, collection, product imports, sockets, or a body.

The historical 26496/27388/10086 inputs and the F009 pre-05:00:57 trace gap
remain retained disclosures. No current source-work trace is used to backfill
that historical gap. No full suite, P4 body, request-test submission, row
installation, acceptance admission, typecheck, lint, or product test was run.
Product test/type/lint evidence is N/A because this review and the author packet
made no product edits.
