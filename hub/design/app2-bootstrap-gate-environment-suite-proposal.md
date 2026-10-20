# App2 frozen bootstrap gate — central suite proposal

Status: harness ready; central run awaits manager registration. No App,
Runtime, Agent, dependency, pin, generated-file, or test-source changes were
made.

## Exact frozen inputs

- Agent commit `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3`, tree
  `c5a8a3ec7e9e01c61c5ae31834da53bed4be406a`
- Runtime commit `7f6dd8920e1ceec41b137358df5e7fecc304888d`, tree
  `4cccb2d643194df7df95d624e89a6cd9f6f268fc`
- Private extracted roots:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-gate-environment/sources/agent-310e`
  and
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-gate-environment/sources/runtime-7f6`
- Read-only interpreter: `/home/user/work/venv-app2-native/bin/python`

## Proposed one-line suite registration

Append this line to the central allow-list only through the manager-owned
registration path:

```text
app bootstrap-frozen-pair-integration /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-gate-environment/harness/run-frozen-bootstrap-gate.sh
```

Then request exactly:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test integration:app bootstrap-frozen-pair-integration)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "${R}"
```

The runner command is also directly inspectable at
`.../workers/ap2-m2-bootstrap-gate-environment/harness/run-frozen-bootstrap-gate.sh`.
It uses `-c /dev/null -p no:cacheprovider`, the read-only native venv, and
`PYTHONPATH=runtime/tests:runtime:agent`; it does not use the shared Runtime or
Agent worktrees.

## Expected collection

The two unchanged Runtime files collect 12 tests. The run selects all 12
(7 local-safe guards and 5 provider-backed integration/null-head cases) and
excludes only `darwin_native` and `live` markers. Expected result on the exact
pair: `12 passed`.

Local collection and import checks found no missing runtime/package imports.
The only initial collection failure was the expected flat helper lookup until
`runtime/tests` was added to `PYTHONPATH`.

## Current hold

This gate does not prove or claim the separate Agent opaque-inverse undo hold
is fixed. The four original unrelated-parent opaque inverse positives remain
the current strict failing hold from the frozen Agent 310e reproduction, with
`inverse_dependency_changed` at `parent`; no expectation was changed or
weakened here.

This worker did not register the suite or request the central run because the
service/suite environment is read-only in the brief and the manager owns suite
registration. Until that one line is registered, no central qualification
claim is made.
