# Served PCM current-entry phase fixture handoff

Prepared, execution HELD. This handoff preserves the guard-fix baseline and
updates only the two served-WAV phase cases to use the current inactive
producer's real `window`/`tracks` entry:

- the controller rejects tracked **and untracked** source drift and repeats the
  complete source/helper/archive-package/dependency/environment preflight in a
  `finally` after pytest; a postflight failure is reported and changes a
  successful pytest result to failure while preserving a nonzero pytest result;
- the fixture binds every original and prepared HTTP read to the live
  `InvocationAssetServer.port` in addition to the existing loopback-host check.

The seven whole-source cases, source postflight, actual server-port checks,
and cleanup/forgery/double-apply assertions remain frozen. No product tree,
protocol, source authority, HOME, browser, listener, or central test service
was changed or run.

## Frozen flat files

All paths are absolute and live under the ORCH design directory:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-served-phase-current-fixture-controller.py
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-served-phase-current-fixture-test_normal_audio_served_sources.py
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-served-phase-current-fixture-guard-regressions.py
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-served-phase-current-fixture-UNAPPLIED-tests.patch
```

SHA256 (freeze these exact bytes before any manager registration):

```text
CONTROLLER_SHA256=557a7f0cbc0a7c3136253576cf773c131efdb9073a99e93a4f4bc76576f99abd
FIXTURE_SHA256=f2a659a9a1fa0068ba4d105fd345c3729643b50705566a0d030b339b4a110736
REGRESSIONS_SHA256=2bed196e0930eccddb6824221fba56ece4ef97be3652844fcb48e076b98357bf
PATCH_SHA256=77f8974abda095480d3ca460fbd2e5fffa18d6315522d85739c6c90710f1c404
```

## Exact local pure checks

```sh
D=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/ruff check \
  "$D/handoff-vw-m3-served-phase-current-fixture-controller.py" \
  "$D/handoff-vw-m3-served-phase-current-fixture-test_normal_audio_served_sources.py" \
  "$D/handoff-vw-m3-served-phase-current-fixture-guard-regressions.py"
T=$(mktemp -d /tmp/vw-m3-served-phase-current-fixture-tests.XXXXXX)
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/vw-m3-served-phase-current-fixture \
  /home/user/work/venv-agent/bin/python -B -m pytest -q \
  -c /home/user/work/wt/vw-m3-served-phase-current-fixture/pyproject.toml \
  -p no:cacheprovider --basetemp "$T" \
  "$D/handoff-vw-m3-served-phase-current-fixture-guard-regressions.py"
```

Expected pure result: `4 passed`; this uses no HTTP listener or socket. The
fixture's existing seven whole-source positive/nativebytes/forgery/doubleapply/
cleanup tests are preserved, while the two phase cases now call the current
inactive entry with the unsliced compiled props and retain their full-source
PCM, clock, gain, source-binding, and strict float assertions.

## Manager-only frozen central preparation

After the producer manager supplies a final committed SHA and an already
approved installed public12 project, substitute only `FINAL_PRODUCER_SHA` and
`APPROVED_INSTALLED_PROJECT` below. Do not use the current producer scratch
project as the approved project.

Named suite registration:

```text
agent integration-viewing-pcm-served-phase-current-fixture /home/user/work/venv-agent/bin/python -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-served-phase-current-fixture-controller.py --source-sha FINAL_PRODUCER_SHA --project APPROVED_INSTALLED_PROJECT --node /tmp/vw-m3-agent-gate-node20.19.4/bin/node --scope with-phase
```

One central request, not run by this worker:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test vw-m3-served-phase-current-fixture integration-viewing-pcm-served-phase-current-fixture) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

The `whole` scope is the existing seven passing module cases only. The
`with-phase` scope adds the two current inactive-entry phase cases; a pass
proves only the inactive helper transform, not Agent normal-service
provenance/activation or Player/export parity.
