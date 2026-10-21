# Agent Main014 current Main95bd qualification

## Verdict

**PASS for the requested current Main014 Agent qualification.** The exact
staged source is candidate commit
`6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree
`2ed2b8a12b5b3391ca221ba6ff05390f71a73556`. The assigned worktree and the
central test snapshot both resolve to that commit/tree and were clean.

This result does not claim publication, adoption, activation, integration
branch mutation, private-leak evidence, or a public release.

## Requested central run

The one requested run was monitored by its existing ID; it was not
resubmitted or duplicated:

`agt-m2-main95bd-forward-latest-gates-main95bd-added-gates-integration-1021001525-26586`

Snapshot/source evidence:

- suite: `main95bd-added-gates-integration`
- result status: `pass`
- exit: `0`
- central snapshot tree: `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`
- requested: `2026-10-21T00:15:25Z`
- pytest result: `4 passed in 22.23s` (service summary: 28s)

Exact command run by the central service:

```sh
env -i HOME=/root LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-95bd3c5f" \
  PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/nix/var/nix/profiles/default/bin:/root/.local/bin:/root/.cargo/bin:/usr/local/go/bin:/opt/node22/bin:/opt/maven/bin:/opt/gradle/bin:/opt/rbenv/bin:/root/.bun/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/bin \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-95bd3c5f \
  ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-main95bd \
  ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
  ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-main95bd/node_modules \
  ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration \
  tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_rational_move_is_lossless_across_native_frontends \
  tests/sdk/test_timeline_selected_schema_runtime.py::test_http_attached_selected_param_retains_original_pin_after_v2_removal_restart
```

The first test supplied the three rational frontend cases; the second supplied
the one original-P1/after-V2-removal/restart case. All four passed against
Runtime checkout `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
`d3a290b407fa61e6ab2d476f50c068073f70df00`, using Node 20 and the private
test profile shown above.

## Carried pin evidence and boundaries

The prior independent normal consumer-pin review in
`agent-main95bd-owned-pin-review.md` is carried as-is; it approved the exact
Main95bd normal pin for staging and reciprocal pairing. The independent
Runtime producer review in `agent-runtime95bd-producer-review.md` is likewise
carried as-is. This handoff does not perform a review of either review.

The carried identity checks include the normal generated-client lock and
schema evidence: raw edit schema SHA-256
`6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d` and
`runtime.lock.json` SHA-256
`920f4a3edf3d0e5ce9df5a0b2749f7b02bc2ea7db6fef2ec70db8d02b65be8e7`.

Main497, current 5c changes, 6ba55/29 semantics, and the exact normal pin
remain preserved. No private-leak, adoption, or publication claim is made.

## Exceptions

No real failure occurred, so no test-setup fix or product-gap classification
is needed. No repository process documentation was changed. The service
runner log contains a post-run cache-file lookup warning, but the authoritative
status, exit code, snapshot, and pytest log are all successful.

