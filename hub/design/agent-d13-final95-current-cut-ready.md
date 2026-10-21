# Agent D13 current-source deletion unit — proposed handoff

## Proposed ledger status

**HOLD / OPEN; not DELETED.** This is one staged Agent unit on qualified
current Main `6efc81500a0e0688c2bb41e736503f0fc3e04abb`. It must remain held
until the coordinated Agent/Runtime/App adoption and the exact normal014
native render tuple are merged and requalified. The manager edits the ledger;
this report does not claim a D13 deletion or release.

## Source change

The current source was first checked against the reviewed native requester
source `7b3e1205a374443c46bad6b18753ef146e1e42c6` and its approved requester
series. Current Main still had the legacy GenericPackHost
`_publish_assembled_timeline` hook and no `assembly-admission` requester
flight. The staged unit ports only the missing D13 seam:

- `runtime_orchestration.py`: immutable native-assembler admission identity,
  original target/child selection/order capture, and bounded storage estimate;
- `sdk/timeline/assembly.py`: exact requester capture, durable admission-flight
  retry, and managed settled-proposal/provenance/digest validation;
- `sdk/timeline/sync.py`: admission and settled-proposal requester methods,
  strict flight-kind validation, and guards preventing commit/undo while an
  admission flight is outstanding;
- `assemble_timeline/run.py`: captured native proposal generation using the
  existing `capture_assembled_media` command producer;
- `generic_host.py`: host-owned producer identity and exact child association
  reads, deterministic refusal of legacy assembler admissions, and deletion of
  the pre-settlement publication hook/call/payload;
- `workspace_client.py` and the rendering pack metadata: existing generated
  media-selection/verification operations and the native proposal contract.

No endpoint, DTO, schema, scope, worker authority, renderer no-write scope,
atomic cancellation/fence guard, retry identity, or historical render path was
added or broadened. The existing producer guard remains the only command
authority carrier. No inline proposal or PreparedProvider substitute was
introduced.

The old hook behavior remains represented by strict xfails with the D13
replacement named in the reason; it was not rewritten as a passing refusal.
The direct compatibility test asserts that a legacy admission fails before
execution and leaves its artifact untouched.

## Tests

Passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/sdk/test_timeline_assembly.py tests/sdk/test_timeline_sync.py \
  tests/sdk/test_timeline_producer_guard.py \
  tests/packs/video_editing/test_runtime_publication_chain.py -m 'not integration'
  90 passed, 2 deselected, 1 xfailed in 15.41s

/home/user/work/venv-agent/bin/ruff check --select E9,F401,F821,I001 \
  astrid/core/contracts/runtime_orchestration.py \
  astrid/packs/rendering/actions/assemble_timeline/run.py \
  astrid/sdk/timeline/assembly.py astrid/sdk/timeline/sync.py \
  astrid/sdk/workspace_client.py tests/sdk/test_timeline_assembly.py \
  tests/sdk/test_timeline_sync.py tests/packs/video_editing/test_runtime_publication_chain.py
  All checks passed

git diff --check
  passed
```

Adjacent GenericHost/handoff lane, attempted but not qualifying this unit:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/core/execution/test_generic_host_actions_v3.py \
  tests/core/execution/test_generic_host_handoff.py \
  tests/sdk/test_timeline_producer_guard_runtime.py \
  tests/sdk/test_timeline_sync_native.py -m 'not integration'
  230 passed, 58 deselected, 61 failed
```

The failures occurred before the changed D13 seam in child-process tests
because the direct worker environment did not expose shared `runtime_protocol`
to the spawned child; one handoff case also hit the sandbox's known
`PermissionError` on socket send. No test was weakened or skipped to obtain the
focused result. No full, browser, live-socket, MP4/ffprobe, or renderer tuple
run was performed here.

## Remaining coordinated evidence

The genuinely changed source tuple is current Agent Main `6ef` plus the
coordinated normal014 Runtime/client and pinned Remotion source. It needs one
focused live native render qualification of the already named registered
assembler positive (`test_daemon_backed_host_executes_authoring_and_final_render`)
with the existing requester/outbox, real managed proposal settlement, original
target/provenance, lost-ACK/restart retry, historical render admission, MP4
decode/ffprobe, and guarded undo. The unchanged qualified renderer cases were
not duplicated here. D13 remains held until that coordinated source merge and
test pass, followed by App adoption and the Runtime RT07 retirement order.

## Source references

- Plan: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/PLAN.md`
- Qualification: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-d13-current13-native-qualification.md`
- Runtime deletion handoff: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/runtime-rt07-current-deletion-candidate.md`
- Reviewed qualified Agent source: `7b3e1205a374443c46bad6b18753ef146e1e42c6`
- Current Agent base: `6efc81500a0e0688c2bb41e736503f0fc3e04abb`

## Proposed commit

`feat(timeline): retire legacy assembler publication path`

The harness should commit this staged unit only; no integration adoption is
claimed by this worker.
