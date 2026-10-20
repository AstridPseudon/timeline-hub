# D13 / RT07 native assembler consumer replacement

## Source tuple

- Worktree: `/home/user/work/wt/agt-m2-d13-native-current-cut`
- Base: `tl/agt-m2-next-ordinary-current-core-gate`, source HEAD `310e5484`
- Reviewed hunks: `0536d246` (registered producer), `32d6de6a` (current requester), `ed39c027` (durable admission), `c6101360` (strict flight tag)
- Agent-only implementation; no Runtime/App/Composition worktree or public `013` pin was changed.

## Current native seam

The registered assembler now uses the existing path: capture the original target,
frozen child membership and verified media reads; build the reviewed immutable
admission; persist the exact admission body in the existing one-flight outbox;
execute through `GenericHost`; settle through `capture_assembled_media`; read the
managed settled proposal; and queue the existing requester commit. Reopen accepts
only the strict `assembly-admission` flight tag and retries the saved body, so a
lost admission ACK does not recapture or mutate the original intent.

`GenericHost` carries the captured target, producer identity, and exact Runtime
association rows into the native action. The action emits the existing
`SettledProducerProposal` shape. Ordinary schema/text/parent auto behavior,
GenericHost source-helper extraction, F1 staged inverse, stage guards, and the
normal rendering/stitch route remain intact.

## Deletions and refusal

- Deleted `GenericPackHost._publish_assembled_timeline` and its pre-settlement
  whole-candidate publication call/payload (104 lines removed in that method and
  call path).
- Legacy assembler admission without an immutable original target now visibly
  refuses while preserving its artifacts; it is not silently rewritten as a
  native admission or fallback writer.
- `runtime_stitch.py` and the existing `publish_timeline_render` route remain
  unchanged; this does not claim render restoration from artifact upload alone.
- The old host-positive tests are strict xfails naming the native-consumer
  requirement; no passing behavior test was rewritten to expect refusal.

## Net product change

Including the new untracked modules, product files add 445 lines and remove 116
(net +329); the old whole-publication hook accounts for 104 removed lines.
Tests add 146 lines, limited to the native admission/recovery cases, strict flight
validation, and the two bounded legacy expectations.

## Evidence

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_assembly.py tests/sdk/test_timeline_sync.py tests/packs/rendering/test_assemble_timeline.py tests/sdk/test_timeline_producer_guard.py tests/editing_conformance/test_producer_insertion.py`
  - `158 passed in 22.38s`
- Focused local publication/consumer run: `77 passed, 1 xfailed in 19.91s`.
- Central targeted snapshot for `test_timeline_assembly.py`, `test_timeline_sync.py`, `test_assemble_timeline.py`, and `test_runtime_publication_chain.py`:
  - `77 passed, 2 deselected integration tests, 1 xfailed in 24.64s` (exit 0).
- Ruff on changed contract/action/assembly/sync/test files: `All checks passed!`.
- `git diff --check`: passed.
- Broader producer/host check: `318 passed, 6 deselected, 6 failed`; every failure is the sandbox's `PermissionError: [Errno 1] Operation not permitted` while creating the GenericHost control socket, before the native seam.

## Remaining gates

The real registered producer/GenericHost/Runtime service path with a decodable tiny
generated-media fixture, duplicate-CAS positive, atomic changed-guard negative,
and cross-restart lost-ACK recovery was not runnable in this worker. No HTTP,
live-socket, or full-suite result is claimed; the registered-assembler named suite
is not available for this Agent repo. D13 remains HELD in the ledger until the
manager's merged qualification, then the manager may delete the ledger row.
