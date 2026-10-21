# Agent D13 final95 custody review

Date: 2026-10-21

## Verdict

**HOLD / request changes. Do not approve adoption or delete the D13 ledger entry.**

The source port at `0963d9452ec2a5720ffed834017b28b0a5413c8e` (tree
`27e62d0797dbc74c1f1753a10b0ac3570e51be73`) is staged on current Agent `6efc81500a0e0688c2bb41e736503f0fc3e04abb` and preserves the reviewed
custody shape, but its current test conversion marks the registered native
end-to-end positive as strict xfail. The approved `7b3e1205`/`65c87dd5`
source had an active replacement for that positive. The current tree has no
one-to-one active replacement proving producer.guard -> requester outbox ->
Runtime admission/settlement -> ordinary render -> retry/restart -> undo.

## Source/custody review

The following current seams are present and consistent with the approved D13
source:

- `runtime_orchestration.py` and `sdk/timeline/assembly.py` are byte-identical
  to the corresponding `7b3e1205` files. `build_native_proposal` in
  `assemble_timeline/run.py` is logic-identical; current differences are only
  docstring/formatting.
- Request capture freezes project, timeline, base revision and base publication;
  it accepts exactly two ordered, distinct child associations and checks
  association object/version/lifecycle/durability/role/media type against the
  exact Runtime media selection and verified-media result.
- Admission construction preserves the original target, child task IDs,
  association identity and ordered object IDs. It does not add a new endpoint,
  public DTO, role, scope, fallback writer, or renderer authority.
- Settled proposal reading requires the exact task/project/capability/state and
  attempt, output association, task run, CAS bytes/digest, durable lifecycle,
  and producer provenance including task ID, attempt ID, executor, fence and
  runtime epoch. The admitted target and proposal digest are checked again
  before the proposal is converted to commands.
- `TimelineSession` persists the exact admission body in the durable outbox,
  uses the strict `assembly-admission` flight kind, refuses unknown flight kinds,
  retries without recapturing mutable media/project inputs, and blocks normal
  commit/undo while the admission flight is unresolved. `queue_proposal` remains
  on the existing producer path, which supplies `producer.guard`.
- `GenericPackHost` removes `_publish_assembled_timeline` and the
  pre-settlement `publication_result` path. A legacy assembler admission is
  refused before execution. Native materialization stages host-owned producer
  identity and exact child association reads; existing cancellation checks still
  run before final settlement, whose handoff retains attempt/fence/epoch.

The rendering metadata/module prose still says that “legacy admissions retain
Runtime publication”. That wording is inherited from the approved donor and is
in tension with the current GenericHost refusal. It is not treated as a new
wire or authority path, but should be aligned before adoption so the removal is
unambiguous.

## Test conversion audit

Against current base `6efc815`:

- `tests/packs/video_editing/test_runtime_publication_chain.py` had no xfail
  markers. It had an active legacy GenericHost hook positive and an active
  registered GenericHost/real-render positive; its only skip was the existing
  ffmpeg/ffprobe/node availability guard.
- Current `0963d945` adds two strict xfails. The old hook positive is now an
  xfail with the reason that D13 removes the hook. That is an acceptable
  removed-behavior marker, and the active refusal/artifact-preservation test is
  useful compatibility coverage.
- The registered native end-to-end positive is also now an xfail. This is not
  equivalent to native success: the current tree does not retain the approved
  `7b3e1205` active replacement assertions for `TimelineSession.admit_assembly`,
  `read_assembly_proposal`, `queue_assembly`, `producer.guard`, lost commit ACK,
  restart/exact retry, ordinary render/ffprobe, and guarded undo. The remaining
  active publication test exercises the older explicit `publish_authoring_proposal`
  route, not this native requester path.
- The newly added SDK unit tests cover frozen admission capture, strict flight
  recovery and no recapture after a lost admission ACK. They do not provide the
  missing active one-to-one Runtime/host/render ledger mapping.

The adjacent `230 passed, 58 deselected, 61 failed` result is not baseline
qualification. Trace inspection classifies the failures as spawned-child
`ModuleNotFoundError: runtime_protocol` from the direct worker environment,
plus one sandbox `PermissionError: [Errno 1] Operation not permitted` on the
handoff socket. These failures occur before the D13 seam and were not relabeled
as product failures.

## Evidence run here

Passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/sdk/test_timeline_assembly.py tests/sdk/test_timeline_sync.py \
  tests/packs/video_editing/test_runtime_publication_chain.py -m 'not integration'
73 passed, 2 deselected, 1 xfailed in 10.10s

/home/user/work/venv-agent/bin/ruff check --select E9,F401,F821,I001 \
  astrid/core/contracts/runtime_orchestration.py \
  astrid/packs/rendering/actions/assemble_timeline/run.py \
  astrid/sdk/timeline/assembly.py astrid/sdk/timeline/sync.py \
  astrid/sdk/workspace_client.py tests/sdk/test_timeline_assembly.py \
  tests/sdk/test_timeline_sync.py \
  tests/packs/video_editing/test_runtime_publication_chain.py
All checks passed

git diff --check 6efc81500a0e0688c2bb41e736503f0fc3e04abb \
  0963d9452ec2a5720ffed834017b28b0a5413c8e
passed
```

The full changed-file Ruff command reports 13 diagnostics in
`generic_host.py`; the exact same 13 diagnostics are present on `6efc815`, so
this is pre-existing lint debt, not a D13 regression. No full suite, live
socket suite, browser suite or renderer rerun was performed.

## Required next step

Static/direct compatibility is insufficient for this port because the changed
seams cross the Runtime transport, GenericHost source/attempt custody and the
registered renderer. After restoring the approved active native positive (or an
equivalent current-main test with the same assertions), request exactly one
bounded central run on the exact ordinary95 Runtime/source tuple. It must keep
the original positive active and prove the registered native path, producer.guard,
exact source/target/media/attempt/fence/epoch custody, requester outbox lost-ACK
and restart retry, cancellation/admission idempotency, ordinary MP4/ffprobe,
and guarded undo. Do not substitute the old explicit publication test or a
donor-tree result.

D13 remains staged/HOLD pending that active replacement and bounded current-tree
qualification, followed by coordinated adoption.
