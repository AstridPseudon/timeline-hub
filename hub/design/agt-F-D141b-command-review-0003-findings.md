# F/D141b independent command review

**Verdict: FAIL.** The candidate commit is resolved as
`6274c362f902632a99ab0f676ad458ace08f550b` on
`tl/agt-F-D141b-plain-command-2358`, based on
`c585cb2aa73c5298d474e614cb2144f58f27e605`.

The source packet is otherwise conservative and within scope. `bash -n`, JSON
parsing, `git diff --check`, the four frozen SHA/tree/clean-status receipts,
and the exact 17-root inventory all pass. The command uses the exact Agent and
Runtime pinned paths, changes to the pristine Agent checkout, and sets
`PYTHONPATH` to the pristine Agent plus Runtime checkout. It has no D73
launcher, positive/poison controls, source overlay, package acquisition,
pytest collection, or body execution.

Blocking findings:

1. `command.sh:158` sends stdout and stderr to one `pytest.log`; it does not
   retain distinct durable raw stdout and raw stderr. The EXIT trap at line 33
   records `exit=` only on failure, so a successful run has no durable exit
   witness. This fails the required XML/rawstdout/rawstderr/exit/disk/output
   ownership evidence contract.
2. `monitor_disk` returns 97 on an unreadable disk measurement, but the caller
   only treats monitor status 124 as terminal. A successful body can therefore
   yield wrapper `state=PASS` after a monitor failure. This is not fail-closed
   and does not honestly record safety status.
3. The packet records only the 4.7 GB start and 4.0 GB stop thresholds. It
   omits the separately required 4.6 GB source floor, conflating source
   admission with the one-time heavy-body start gate.
4. The interpreter path and version are recorded but not asserted. The body
   can be admitted with a changed existing venv target or version.
5. The service row's command hash guard names
   `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141b-plain-command-2358/evidence/command.sh`.
   That path is absent after the author worktree was recycled, so the exact
   documented `/bin/bash` invocation currently fails at its hash guard. The
   manager must publish the exact bytes to a durable path and verify the path
   before controller submission; this review does not edit or substitute it.

No product tests, imports, collection, service request, or body were run. No
source/code or other worker worktree was modified.

Historical D73 controls and the prior recipe are not revived. Farm retains all
project tests, and no REG or ship credit is inferred.
