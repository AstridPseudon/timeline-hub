# App2 native bootstrap fixed-pair suite proposal

Status: harness prepared; central registration and execution are pending. This
is native prerequisite evidence only. It does not activate App consumers,
adopt a private pin, qualify a browser journey, or retire a writer.

## Exact sources

- Agent initializer source: commit
  `4296a7091d30543d3839fe703c0f0626f9882ebe`, tree
  `855e2fe057e5b4b14257a6b8179201c3601dc94f`.
- Agent test-only real-provider patch: child commit
  `2585e01cd2a198d3a091066848bd72152955bb0a`, whose only changed path from
  `4296a...` is `tests/sdk/test_timeline_pristine_initialize_runtime.py`.
  The patch SHA256 is
  `c733c4eca7aba5c5252892857ed5113a2f974fde4fbe25dbb36d18536755583f`.
- Runtime source: commit
  `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`, tree
  `4b7dd0fe44be973c344bab3de568eaf0bdd28476`.
- Private immutable roots:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-fixed-pair-gate/sources/agent-4296`
  and
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-fixed-pair-gate/sources/runtime-a0dca`.
- Read-only interpreter: `/home/user/work/venv-app2-native/bin/python`.

The Agent schema SHA256 is
`6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`; the
pristine fixture SHA256 is
`6a13d80d9cbe9af015ff5c8b71cf8ce4901ff8248e00c26bf6215a7ce97cbff7`.
The Agent `runtime.lock.json` names exactly Runtime `a0dca...`.

## Harness and collection

Runner:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-fixed-pair-gate/harness/run-exact-bootstrap-pair.sh`

It runs three pytest processes because the existing provider unit fixture
temporarily installs a fake `runtime_protocol` module; separating that lane
from real-provider tests preserves the existing test bodies and expectations.

The runner selects:

- 31 Agent direct initializer/provider tests, including the original
  `null`, `false`, `[]`, and `{}` reload/inverse/redo positives plus strict
  pristine, order/intervening-write, ABA/equal-bytes, and history negatives.
- 4 Agent real-provider tests: initializer retry/restart/reload/undo/redo,
  the disjoint opaque-row regression, and image/video first-birth negatives.
- 12 unchanged Runtime neighbors from
  `tests/test_timeline_fresh_bootstrap_scope.py` and
  `tests/test_timeline_absent_head_repair_integration.py`, including the
  same-ID corrupt-scope refusal and absent/null-head repair cases.

Collection-only result: `31`, `4`, and `12` tests in the three processes.

## Manager registration and request

Register one new allow-list line through the manager-owned path; do not replace
the old 12-pass suite:

```text
app bootstrap-fixed-pair-native-integration /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-fixed-pair-gate/harness/run-exact-bootstrap-pair.sh
```

Then request exactly:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test integration:app bootstrap-fixed-pair-native-integration)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Expected exact-pair result after registration is `31 + 4 + 12 = 47 passed`.
No central service request was submitted by this worker because the allow-list
is manager-owned and the existing old suite points at different 310e/7f6
sources.
