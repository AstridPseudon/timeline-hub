# Runtime RT07 current-source deletion candidate

## Scope

This candidate ports the approved RT07 cut/replay body onto Runtime current
source `2ef92e46535e5dddf9db62342824986d9de5b9ec`. Only these files changed:

- `runtime_protocol/service.py`
- `tests/test_timeline_render_publication_authority.py`

`RuntimeService.publish_timeline_render` no longer writes the legacy canonical
document, timeline event, CAS snapshot, render task, or publication checkpoint.
It retains the existing request parsing and authority guards for fresh calls,
then returns the visible retired-route `410` with the `/v1` commit replacement.
Prepared checkpoints are also refused with no recovery write.

The sole legacy success path is read-only replay of an already published
checkpoint. It requires the attempt/task relationship, an existing task
project, an exact request hash, and the checkpoint's stored timeline target.
It returns the stored result without consulting live target/spec/head state or
performing document, CAS, task, history, or checkpoint writes. Changed payloads
remain conflicts. No Runtime store, generated client, route, metadata,
artifact, WAV/null/rate, script-CAS, catalog-head, C4, occupancy, or headless
surface was copied or changed.

The three original fresh legacy positives remain unchanged and intentionally
red; no xfail, skip, assertion deletion, or fake provider was added.

## Evidence

Local compile and scoped authority lane:

```text
/home/user/work/venv-runtime/bin/python -m compileall -q runtime_protocol/service.py
  passed

/home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_render_publication_authority.py -k 'retired_writer_refuses_before_lookup_without_writes or retired_writer_refuses_without_prepare_or_publication_writes or published_checkpoint_replays_read_only_after_live_authority_changes or prepared_checkpoint_remains_retired_without_recovery_write or tracked_target_refuses or same_project_unadmitted_target or malformed_admitted_target or inconsistent_native_target or corrupt_immutable_spec'
  17 passed, 3 deselected in 9.19s
```

Central targeted request:

```text
request: rt-m2-rt07-current-body-deletion-targeted-1020181239-32318
command: /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_render_publication_authority.py tests/test_timeline_authority_door.py
result: 29 passed, 3 failed in 19.01s
```

The three failures are the intentionally preserved fresh positives named
above. No full suite, merge, release, browser, renderer, or native Agent gate
was run by this worker.

## Remaining landing evidence

Landing remains held for Agent ownership. The exact native gate is the named
`registered014-render-integration` qualification for the two original
`tests/packs/video_editing/test_runtime_publication_chain.py` integration
positives. Its recorded request
`agt-m2-d13-exact014-render-gate-registered014-render-integration-1020155702-1130`
reached the functional proposal/requester outbox, lost-ack restart/exact
retry, revision-pinned render, real CAS MP4/ffprobe, and undo assertions, but
failed teardown with `CustodyError: CPU attempt cleanup remains unresolved`.
It therefore does not yet prove the required native replacement.

Before this candidate can land, Agent must provide a fresh exact-source,
two-positive pass including that teardown and caller migration to the settled
proposal -> requester/outbox -> `/v1` commit path, with no legacy publication
traffic. The prior review's remaining callers to account for are
`astrid/core/execution/generic_host.py`,
`astrid/packs/rendering/shared/runtime_stitch.py`,
`astrid/sdk/remote.py`, and `astrid/sdk/workspace_client.py`. Runtime/Agent
paired qualification then needs to rerun the unchanged three legacy positives
as the native equivalence evidence.
