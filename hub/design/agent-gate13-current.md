# Agent Gate1/Gate3 current proof — published014/Main497

Date: 2026-10-21 UTC

## Verdict

**PASS for the requested bounded Gate1/Gate3 qualification.** The exact
current merged Agent source is `091aa23ec83ea05ffd3b0115a640230d51c8c429`,
tree `e3ae90fe482ba6cad6c3f94069127faf76ebceb6`. It is the current
`tl/integration` snapshot and is descended from Main497
`497714c73531f164082555ec81b61ca5bc8b6554`. The worktree was clean before
and after the run.

This is a bounded qualification result, not a claim that every transcript,
rational-timing, occurrence/source, browser, render, cross-product, or full
suite gate is green.

## Exact source, Runtime, lock, and C13 identities

- Agent source: `091aa23ec83ea05ffd3b0115a640230d51c8c429`, tree
  `e3ae90fe482ba6cad6c3f94069127faf76ebceb6`.
- Runtime checkout: `/home/user/work/wt/rt-pin-95bd3c5f`, commit
  `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`; checkout clean.
- Agent `runtime.lock.json` SHA-256:
  `920f4a3edf3d0e5ce9df5a0b2749f7b02bc2ea7db6fef2ec70db8d02b65be8e7`.
  Its `source_commit` is the exact Runtime95bd commit above and its
  `producer_version` is
  `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`.
  The producer `contract/artifacts.json` SHA-256 is
  `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`.
- The C13/public Composition origin used by the pinned Remotion profile is
  `/home/user/work/runtimes/agent-remotion-main95bd`, with Composition 0.0.13
  archive SHA-256
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738` and
  Node `v20.19.4`.
- Ordinary edit-command schema SHA-256 is
  `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.
  No schema override, assertion rewrite, pin change, generation change, or
  activation change was made. The current timeline-config schema is byte
  identical to Runtime95bd's contract schema.

Read-only checks passed:

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-95bd3c5f
ok runtime.lock.json (matches producer manifest)

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
artifacts.json is current

git diff --check
```

## The one requested named run

Existing suite: `main95bd-real-fixture-qualification`.

Central result ID:
`agt-m2-gate13-published014-current-proof-main95bd-real-fixture-qualification-1021031102-23927`

Snapshot tree: `e3ae90fe482ba6cad6c3f94069127faf76ebceb6`.

Exact command:

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
  tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_omitted_native_clip_row_delete_retries_rebases_and_refuses_changed_selection \
  tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_cut_owned_native_sheet_hold_reloads_and_undoes \
  tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_label_clear_is_lossless_across_native_frontends \
  tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_semantic_batch_original_pins_reload_inverse_redo \
  tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_sheet_lost_ack_restart_exact_retry_original_guards_and_aba \
  tests/editing_conformance/test_commit_runtime_native_checkout.py::test_authenticated_v1_commit_reload_undo_survives_stopped_renderer_and_preview_reports_unavailable
```

Result: **11 passed in 49.56s**, service wall time 52s, exit 0.

The run preserved the existing assertions and covered native sheet/CLI/Python
clears, opaque data and membership guards, reload/inverse/redo, lost-ACK
restart and exact retry/ABA guards, plus authenticated `/v1` commit/reload/
undo with the renderer stopped and honest unavailable preview reporting. No
test source or failure evidence was changed.

No other suite was requested or run: no old51/130, browser, render, full, or
passing-neighbor rerun.

## Remaining holes

- **Transcript:** this named lane has no fresh transcript/source-binding
  scenario. The retained-transcript handoff records that Runtime95bd's public
  verified-document route rejects `media.transcript`; therefore no current
  Runtime-door transcript proof is claimed here.
- **Rational timing:** this named lane does not select the rational-fps,
  half-open-boundary, or rational explicit-occurrence three-frontend cases.
  Their earlier staged evidence is not relabeled as proof for this exact
  published014 snapshot.
- **Occurrence/source:** this lane exercises native-row membership/guards but
  does not freshly qualify connected occurrence/shared-source isolation across
  all three frontends on this exact snapshot. The earlier occurrence-source
  handoff remains separate evidence.

These are transcript/rational/occurrence qualification holes, not failures
observed in the requested run. No bounded core regression was found, so no
product or generation change was justified.

## Recommended next step

The manager can decide whether to schedule separate exact-current-source
transcript, rational, and connected-occurrence proofs. Do not treat this
bounded PASS as a full Gate1 corpus or complete foundation qualification.
