# Served PCM guard-fix handoff

Prepared, execution HELD. This handoff fixes only the two defects in
`handoff-vw-m3-served-pcm-controller-review-REPORT.md`:

- the controller rejects tracked **and untracked** source drift and repeats the
  complete source/helper/archive-package/dependency/environment preflight in a
  `finally` after pytest; a postflight failure is reported and changes a
  successful pytest result to failure while preserving a nonzero pytest result;
- the fixture binds every original and prepared HTTP read to the live
  `InvocationAssetServer.port` in addition to the existing loopback-host check.

The predecessor flat fixture/controller remains untouched. No product tree,
protocol, source authority, HOME, browser, listener, or central test service
was changed or run.

## Frozen flat files

All paths are absolute and live under the ORCH design directory:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-served-pcm-guard-fix-controller.py
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-served-pcm-guard-fix-test_normal_audio_served_sources.py
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-served-pcm-guard-fix-guard-regressions.py
```

SHA256 (freeze these exact bytes before any manager registration):

```text
CONTROLLER_SHA256=72f5c85e73082e068b2898e62ce33ce3bb6733129f929eb9333e8de734f63c3e
FIXTURE_SHA256=2298b10a512fe5b32a6ba20ed5b806a189ed4e6a065f125833bc91709b734ba8
REGRESSIONS_SHA256=d7aa4ee955aca24bc72f48ff2a0cb805e4df41f97c88fd853a3575135c9f17d5
```

## Exact local pure checks

```sh
D=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/ruff check \
  "$D/handoff-vw-m3-served-pcm-guard-fix-controller.py" \
  "$D/handoff-vw-m3-served-pcm-guard-fix-test_normal_audio_served_sources.py" \
  "$D/handoff-vw-m3-served-pcm-guard-fix-guard-regressions.py"
T=$(mktemp -d /tmp/vw-m3-served-pcm-guard-fix-tests.XXXXXX)
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/vw-m3-served-pcm-guard-fix \
  /home/user/work/venv-agent/bin/python -B -m pytest -q \
  -c /home/user/work/wt/vw-m3-served-pcm-guard-fix/pyproject.toml \
  -p no:cacheprovider --basetemp "$T" \
  "$D/handoff-vw-m3-served-pcm-guard-fix-guard-regressions.py"
```

Expected pure result: `4 passed`; this uses no HTTP listener or socket. The
fixture's existing positive/nativebytes/forgery/doubleapply/cleanup tests and
its two ordinary RED phase tests are preserved verbatim except for the
required `expected_port=server.port` arguments.

## Manager-only frozen central preparation

After the producer manager supplies a final committed SHA and an already
approved installed public12 project, substitute only `FINAL_PRODUCER_SHA` and
`APPROVED_INSTALLED_PROJECT` below. Do not use the current producer scratch
project as the approved project.

Named suite registration:

```text
agent integration-viewing-pcm-served-pcm-guard-fix /home/user/work/venv-agent/bin/python -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-served-pcm-guard-fix-controller.py --source-sha FINAL_PRODUCER_SHA --project APPROVED_INSTALLED_PROJECT --node /tmp/vw-m3-agent-gate-node20.19.4/bin/node --scope whole
```

One central request, not run by this worker:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test vw-m3-served-pcm-guard-fix integration-viewing-pcm-served-pcm-guard-fix) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

The `whole` scope is the existing seven passing module cases only and keeps
`window`/`layer` ordinary RED. Do not grant `with-phase` until the source-owner
join prerequisites in the review report are proven.
