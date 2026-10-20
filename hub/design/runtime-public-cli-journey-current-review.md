# Runtime public S2 CLI journey review

Decision: **APPROVE**.

## Exact source under review

- Runtime worktree/base: `388eff42a644aeafa5d4605d0bb235e1ca849741`, tree `708df14c75ef739a2c6130ca39f9e67b2758a571`; clean at setup and at handoff.
- Agent integration checkout: `8e3107853d17453758a933d1f47215cc1c002660`, tree `7b395a0165b00808b9b554213ff015838e813e51`; unchanged and clean.
- Added file: `tests/test_timeline_public_s2_mixed_cli_journey.py`, exactly 411 lines, SHA-256 `727d77e12e79eff40c686cc11ef267d46578b6f92cb82b71d5e521811cc5f843`.
- The added file is byte-for-byte identical to the reviewed source-branch file on `tl/rt-m2-public-s2-literal-journey-control`.
- Runtime repository diff is tests-only: the target test module is the only worktree change. No schema, generation, pin, product, or fixture-archive change was made.

## Evidence checked

The port retains the complete historical mixed-journey success body and its native CLI capture assertions. The historical `music-documents` audio case still requires capture before POST, stale rebase, lost ACK, restart, exact retry, undo, closure, and public views. It is only marked `xfail(strict=True, raises=HistoricalAudioCaptureGap)` for the one exact pre-POST result `clip.trim applies to media clips`; any other error or a success remains a failure/strict XPASS.

The independent `literal-film` setup creates a real mono PCM WAV (8 kHz, 16-bit, 48,000 samples), derives its six-second duration with `wave`, imports and verifies the retained CAS bytes/location, and publishes separate shot/internal-timeline identities. The renderer tripwires are installed after setup. The journey asserts native CLI capture of source/base/guards and the exact disk flight, an independently authenticated disjoint track label, stale rebase, durable lost-ACK acceptance, restart recovery, byte-identical retry, unchanged store/history under a provider tripwire, guarded undo, disjoint label preservation, and exact `show`, `--layers`, and `visualize --mode inputs` views. No all-Main-trim parity claim is made.

## Tests

Central named current-integration lane, exact requested files:

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
"$ORCH/bin/request-test" rt-m2-public-cli-journey-current-review public-s2-literal-current-integration --files 'tests/test_timeline_public_s2_mixed_cli_journey.py tests/test_timeline_commit_integration.py::test_real_door_lost_ack_restart_exact_retry_never_executes_provider'
"$ORCH/bin/wait-test" rt-m2-public-cli-journey-current-review-public-s2-literal-current-integration-1020135405-6131
```

Result: **2 passed, 1 xfailed in 9.70s**, exit 0. The lane verified `runtime_protocol.__file__ == /home/user/work/runtime/runtime_protocol/__init__.py`, guarded current Runtime HEAD `388eff42…`, and used current Agent `8e310785…`. The full log is at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/rt-m2-public-cli-journey-current-review-public-s2-literal-current-integration-1020135405-6131/log.txt`

Direct targeted fixture-neighbor check:

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_timeline_commit_film_fixture.py
```

Result: **6 passed in 2.15s**.

Additional checks: `python -m py_compile tests/test_timeline_public_s2_mixed_cli_journey.py`, AST parsing, source byte comparison, and `git diff --check` all passed. No full or broad suite was run.

## Decision and remaining work

The bounded test port is justified and approved for the current `388eff42…` source pair. The existing named suite's source guard was updated from the stale prior `b748ae7…` candidate to exact current `388eff42…`; this is test-service configuration only and was necessary to qualify the requested current integration lane.

The historical audio path remains unresolved in Agent: trustworthy source-duration capture/authoring must be restored, after which this strict xfail must be removed and the original positive must pass. This review does not qualify renderer parity, browser/App journeys, all writers, or delivery gates.
