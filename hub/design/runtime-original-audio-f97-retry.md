# Runtime original-audio f97 retry

Date: 2026-10-20

## Result

Blocked on the first remaining Agent capture-preflight failure. Runtime stayed
at the required `7d1cfa6b1da0c50bb8a9d3430dcaa6272b20b55e`; Agent was the exact
clean `f97b2b87688abb20280572a5fc23e4f69ec9e3f8` checkout
`/home/user/work/wt/agt-pin-f97b2b87`.

The unchanged `tests/test_timeline_public_s2_mixed_cli_journey.py` was run in
one central named Runtime integration lane with `--runxfail`. Both required
parameters failed before the Runtime POST:

```text
timeline_edit_error: registry source duration requires exact Runtime-verified media metadata
```

The historical case still returns this error before the pause seam. The
literal-media case also returns it, and then the unchanged test reaches
`StopIteration` while looking for the absent observed trim wire row. The
previous native `clip.trim` type refusal is gone under f97, but exact metadata
capture is still unavailable. No stale rebase, lost acknowledgement, restart
retry, inverse, receipt, or public revision-view assertion was reached.

## Exact central evidence

The worker registered one bounded allow-list entry,
`original-audio-f97-cli-retry-integration`, guarded by both exact HEADs and
clean Agent status. It ran only:

```text
tests/test_timeline_public_s2_mixed_cli_journey.py
```

Command:

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
R=$($ORCH/bin/request-test rt-m2-original-audio-f97-retry original-audio-f97-cli-retry-integration)
$ORCH/bin/wait-test rt-m2-original-audio-f97-retry-original-audio-f97-cli-retry-integration-1020172927-30246
```

Result: **2 failed in 7.22s**, exit 1. Log:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/rt-m2-original-audio-f97-retry-original-audio-f97-cli-retry-integration-1020172927-30246/log.txt`

Relevant source path in the exact Agent checkout:

- `astrid/packs/timeline/cli_native.py:commit_trim` now calls
  `TimelineSession.trim`.
- `astrid/sdk/timeline/sync.py:282-313` performs the local raw-audio
  preflight and attempts `client.media.read_bytes`.
- `astrid/sdk/timeline/commit.py:407-434` resolves the retained raw-audio
  manifest pin.
- `astrid/sdk/timeline/_trim_commands.py:34-40` refuses when no exact
  `verified_media` descriptor is present.

The exact trace was sent to the Agent manager inbox. No Runtime provider,
schema, health, door, authority, adoption, fixture, or test change was made;
the Runtime worktree remains clean. No full, comprehensive, control, browser,
or local socket suite was run. This result proves only the in-process CLI
preflight boundary and the failure before POST; it makes no OSC/CLI transport
or EOF claim.

## Required next step

Agent must resolve or explicitly source the exact Runtime-verified media
descriptor for this supported native trim path, preserving the historical
fixture and all downstream assertions. After an approved Agent source update,
rerun this same two-case central lane. Do not weaken the positive journey,
invent authored duration, bypass Runtime verification, or repair Agent tests
from this Runtime worker.
