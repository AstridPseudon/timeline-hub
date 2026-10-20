# Runtime original-audio CLI pair

Date: 2026-10-20

## Result

Blocked on the exact Agent CLI capture prerequisite. The unchanged public S2
journey was run with `--runxfail` against Agent `9bf503f98deb3051cb9caceeae3ea6a5ebd5f185`
(`/home/user/work/wt/agt-pin-9bf503f9`) and Runtime `7d1cfa6b1da0c50bb8a9d3430dcaa6272b20b55e`.
The normal door/auth/lost-ack control passed, but both original-audio and
literal-media journey parametrizations failed before the timeline POST.

First failure in both parametrizations:

```text
timeline_edit_error: registry source duration requires exact Runtime-verified media metadata
```

The trace is Agent-only: `astrid/packs/timeline/cli_native.py:61-81`
`commit_trim` calls `capture_clip_trim(bundle, select, ...)` without
`verified_media`; `astrid/sdk/timeline/_trim_commands.py:35-50` rejects the
missing descriptor before `ctx.read_media`. The 9bf `TimelineSession.trim`
preflight is not used by this native CLI route. Runtime raw-media acceptance,
stale rebase, lost acknowledgement, restart retry, inverse, and revision-view
assertions were therefore not reached. No Runtime/provider/schema workaround
was added.

## Exact evidence

Central named suite:

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
R=$("$ORCH/bin/request-test" rt-m2-original-audio9bf-cli-pair original-audio9bf-cli-pair-integration)
"$ORCH/bin/wait-test" "$R"
```

Result: **2 failed, 1 passed in 9.67s**, exit 1. The two failures are the
journey's `historical-audio` and `literal-media` cases; the passing case is
`test_real_door_lost_ack_restart_exact_retry_never_executes_provider`.
The suite command guards the exact Agent HEAD and clean status and uses the
Runtime worktree at the requested pin.

Runtime targeted neighbours:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-runtime/bin/python \
  -m pytest -q -p no:cacheprovider \
  tests/test_timeline_raw_audio_port.py tests/test_timeline_commit_film_fixture.py
```

Result: **14 passed in 2.99s**. `git diff --check` passed. No full, browser,
renderer, or comprehensive Agent-pair suite was run.

## Required next step

Agent must make the supported native CLI capture path obtain exact Runtime-
verified raw-audio metadata, or provide an approved provenance-preserving
source fixture. Then rerun the unchanged strict-positive journey with the
same source guards. Do not add authored duration to the fixture, adopt raw
bytes, alter health/door authority, or weaken/delete the original assertions.
