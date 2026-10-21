# Current public batch-full profile preflight

Date: 2026-10-21 UTC

## Verdict

**NOT READY; storage correctly refused profile build/install.** No current
Agent wheel, private profile, pytest collection/body, central suite request,
or full run was made.

Exact clean inputs:

- Agent: commit `c4b964f6a050edf63a4278d35717e46a88a80386`, tree
  `d7796be264c341adbcb9765aae374b832dede144`, `/home/user/work/agent`.
- Runtime: commit `b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree
  `6abc2f117391de8e7e35c0283f575a002199894d`, `/home/user/work/runtime`.
- Client/artifacts: commit `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`,
  `/home/user/work/wt/rt-pin-95bd3c5f`.
- C13 source marker: `30da0a5e05d4529a2b97b3c1818cf9e15842d628`.
- C13 artifact SHA-256:
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.

The C13 marker is `/home/user/work/runtimes/agent-remotion-0013/.source-commit`;
the artifact is under its `artifacts/` directory. Node is
`/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node` `v20.19.4`.
C13 `node_modules`, ffmpeg, ffprobe, and VibeComfy are present. The current
`runtime.lock.json` names client source `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3`.

## Read-only closure and tooling inventory

The independent 0908 profile remains read-only and was not used as current
product input:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-d13-private-entrypoint-custody-profile-repair-0908/private-profile-f4edcb4b`

Its retained closure is 164 constraints / 166 distributions, constraint
SHA-256 `478af081b0f27c1e90dac1ab4b0b645583f34787ecfe7b8079d1bb88ca034761`.
Its Agent is f4edcb4b (wheel SHA-256
`7455220aa1d3f8c67c7c9cee0f7a6571fb4f51882eca2543ead25943eebd185a`), so it
cannot be this current c4b product and was not copied or mutated.

Existing tooling: `scripts/smoke_wheel_install.sh`,
`scripts/reshape/installed_artifact.py`,
`scripts/reshape/authority_lint.py`, the settled recipe at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-m4-coherent-installed-profile-recipe.md`,
and the 0908 profile's `preflight.txt`, `metadata/provenance.txt`,
`metadata/wheels.sha256`, and `audit.txt`.

## Named suite

Added `/home/user/work/wt/agt-m4-current-public-batch-full-profile-preflight-0927/scripts/full_coherent_public_current_integration.sh`.
The named suite is `full-coherent-public-current-integration`. It preserves
the default-full body `pytest -q -n 3`, has no integration marker, and adds no
`--basetemp`, cache-provider, or cleanup override; normal pytest temporary
behavior is retained. It checks all setup inputs and reports all failures
before pytest.

Planned central command after profile readiness:

```text
agent full-coherent-public-current-integration env -i HOME=/root LANG=C.UTF-8 PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/nix/var/nix/profiles/default/bin:/root/.local/bin:/usr/local/go/bin:/opt/node22/bin:/opt/maven/bin:/opt/gradle/bin:/opt/rbenv/bin:/root/.bun/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/bin FULL_COHERENT_PUBLIC_PROFILE_ROOT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-current-public-batch-full-profile-preflight-0927/private-profile-c4b964f6 FULL_COHERENT_PUBLIC_AGENT_WHEEL=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-current-public-batch-full-profile-preflight-0927/private-profile-c4b964f6/wheelhouse/astrid-0.1.0-py3-none-any.whl bash scripts/full_coherent_public_current_integration.sh
```

These private paths are planned only; they do not exist. No central
`suites.conf` edit or service request was made; the manager registers the
named command when ready.

## Setup-only evidence and all failures

Command (did not reach pytest):

```bash
SOURCE_ROOT=/home/user/work/agent bash /home/user/work/wt/agt-m4-current-public-batch-full-profile-preflight-0927/scripts/full_coherent_public_current_integration.sh
```

Positive nodes: Agent, Runtime, client, runtime-lock client pin, Node C13,
C13 marker/artifact/hash, C13 `node_modules`, ffmpeg, ffprobe, and VibeComfy.
All failures from the one invocation:

1. `FULL_COHERENT_PUBLIC_PROFILE_ROOT` unset: no current public profile.
2. `FULL_COHERENT_PUBLIC_AGENT_WHEEL` unset: c4b wheel not built.
3. `STORAGE NEED 2.733592987060547 GiB for full-coherent-public-current-integration`:
   free `11023470592` bytes (`10.272 GiB`), below the manager admission
   threshold of more than 13 GiB for profile plus full scratch reserve.

The mandatory current-profile eight-origin, 166-RECORD, and source-byte
checks were not claimed because their profile/wheel prerequisites are absent.
The 0908 audit is the only closure evidence and remains read-only.

## Not run / next step

No build, install, venv creation, profile activation, shared-dependency
mutation, pytest collection/body, Runtime launch/HTTP/socket, native, render,
browser, or full run. Old 21969 remains historical.

After central storage release raises free space above 13 GiB, build exactly one
private c4b Agent wheel/profile, run the complete preflight (all eight origins,
166 RECORD files, source-byte checks, and 164/166 closure), register the named
suite, then let the manager decide whether to spend the one full run.
