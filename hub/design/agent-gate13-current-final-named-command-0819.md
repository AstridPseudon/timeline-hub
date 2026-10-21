# Gate1/3 current named command handoff

Ready for one later central-service execution. No test body, Runtime daemon,
renderer, native process, socket, browser, HTTP, or full suite was run by this
worker.

## Named suite and exact service command

The single allow-list entry is `agent gate13-current-b92-integration` in
`ORCH/tests/suites.conf`. It uses the current service snapshot and verifies
imports from that snapshot for `astrid`, while requiring `runtime_protocol`
from `/home/user/work/runtime`. It also guards the clean Runtime b92/tree6abc
checkout, the normal95 producer and lock, the ordinary public6ba schema,
all76 artifacts, and the existing C13 environment.

Request it once, only after source adoption and the conditional preflight below:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test integration:agent gate13-current-b92-integration) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

The suite command has exactly these three selectors:

```text
tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_rational_move_is_lossless_across_native_frontends
tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_occurrence_move_preserves_shared_source_across_native_frontends
tests/editing_conformance/test_commit_runtime_native_checkout.py::test_authenticated_v1_commit_reload_undo_survives_stopped_renderer_and_preview_reports_unavailable
```

The first function expands to `python`, `cli`, and `sheet` (3 cases); the
second does the same (3 cases); the stopped-renderer function is one case.
Expected collection is therefore **7 tests**, not 3. The transcript selector
is intentionally not included.

## Required identities and result contract

- Runtime checkout: `/home/user/work/runtime`, commit
  `b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree
  `6abc2f117391de8e7e35c0283f575a002199894d`, clean.
- Normal95 producer: `/home/user/work/wt/rt-pin-95bd3c5f`, commit
  `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`, clean.
- Agent lock: `runtime.lock.json` SHA-256
  `920f4a3edf3d0e5ce9df5a0b2749f7b02bc2ea7db6fef2ec70db8d02b65be8e7`, with
  `source_commit=95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`.
- Public ordinary schema: Agent and Runtime edit-command schemas are both
  SHA-256 `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.
- Runtime artifact manifest: SHA-256
  `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`, with
  76 artifact entries.
- Existing C13 environment: `/home/user/work/runtimes/agent-remotion-0013`,
  Node `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`, C13
  child site `/home/user/work/venv-agent-child-c13-a8a40afd/lib/python3.13/site-packages`,
  and its existing `node_modules`.
- Import guards: `astrid.__file__` must resolve under the service snapshot
  root; `runtime_protocol.__file__` must resolve exactly to
  `/home/user/work/runtime/runtime_protocol/__init__.py`.

The selected tests retain the existing API assertions: accepted responses have
`data.commands`, `data.canonical_document`, `data.accepted_revision_id`, and
`receipt.receipt_id`; reload uses `open_bundle(...).ok` and
`data.bundle`; undo/redo preserves the canonical-document/revision shape; and
history exposes `items` with command records under `records.commands`. The
renderer-off case additionally requires the existing unavailable-preview
shape: `CapabilityRuntimeError`, runtime category, `not_found`, and
`rendering.timeline_visualize`.

## Source adoption and final preflight dependency

The final document-presence repair/current merge must first be adopted into
`/home/user/work/agent` on `tl/integration`. The named suite intentionally has
no guessed Agent source-tree literal: the test service snapshots the selected
current integration tree and records the exact `tree=` receipt in its result
directory. That receipt is the source identity for this generic current-
snapshot lane.

If a manager supplies a final exact Agent tree before enqueue, the worker
command record may use this explicit placeholder and replace it with that
literal value:

```sh
SOURCE_TREE=<manager-supplied-final-agent-tree>
test "$(git rev-parse HEAD^{tree})" = "$SOURCE_TREE"
```

This placeholder must not be put in `ORCH/tests/suites.conf`; the production
suite line remains syntactically runnable. Before the one request, perform the
document preflight and condition the remaining existing product checks on the
adopted final source. Do not relabel the predecessor's offline collection as a
live qualification, and do not claim the transcript or any other product gate
from this lane.
