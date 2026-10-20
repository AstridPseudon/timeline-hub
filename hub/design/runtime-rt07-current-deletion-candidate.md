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

## Current merge handoff (2026-10-20)

The current committed code-only retirement candidate is Runtime commit
`40e7dc7cd627c6c4e2bffb482926bb9b037f0143`, tree
`a7c86e8514c1cc095635e1484b71c98928debe01`, parent
`b88a56feb2e1879455b9f1eb2403e171aa125f3c`. It is the approved cut on the
current base, not a merged or released deletion. Its central evidence is the
bounded Runtime lane with 19 passed, 6 deselected, and 1 existing strict xfail,
plus the integration lane with 6 passed and 20 deselected. The strict xfail is
the obsolete legacy prepare/write seam; it is not a replacement qualification.

The exact committed ordinary014 Runtime staging candidate is commit
`202074110717146fc7f08af2306a8dd7f695b0b1`, tree
`ee39286bd0eb27d4075074cc4785d6d15e33f243`. It is unpublished Runtime
0.2.14. Its cohort identity remains producer `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`
(tree `4b7dd0fe44be973c344bab3de568eaf0bdd28476`), raw schema
`6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`, wire
`ce3781c…`, artifact version
`sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa`,
and 75-entry manifest digest
`ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815`.
The candidate predates the owner-strict `cd0` test-only marker transition;
that transition must be carried onto the final cohort without changing any
artifact, schema, generated client, or release metadata.

Remaining prerequisites, in owner order:

1. **Agent owns the current consumer/source repair.** Requalify the registered
   requester/outbox replacement on a current Agent source, including all four
   callers listed above, the two original native positives, and clean custody
   teardown. The later catalog/history failure is stale Agent `7b3` missing the
   already-merged `TimelineSession.restore` facade. The later hold-clear
   failure is also Agent-owned semantic capture refusal before a Runtime
   request. Do not call `7b3` current and do not make Runtime accept either
   failure as a projection or hold override.
2. **Runtime and Agent own the ordinary014 source boundary.** Carry the exact
   `cd0` transition from the current integration marker onto the final
   Runtime/Agent cohort. Preserve its current-public-013 refusal, the complete
   positive acceptance body, and its narrow strict xfail until the 0.2.14
   parent-ownership cohort is actually present. Requalify the same exact
   source/artifact tuple; the 202074 candidate's existing native/HTTP evidence
   is not adoption.
3. **App owns consumer adoption.** Consume that same Agent/Runtime cohort,
   update only the normal014 client/vendor source needed for it, and run the
   parent-media acceptance plus Gate 5 browser journey. Private checks are not
   central adoption evidence. Public 0.2.13 remains immutable; no public pin,
   release, or activation is authorized here.
4. **Runtime lands RT07 last.** After the Agent and App proofs and the unchanged
   three legacy positives requalified as native equivalence, merge the
   code-only `40e7` candidate. Only then may the ledger status change from
   `OPEN` to `DELETED`; this handoff does not make that status change.

The coordinated merge order is therefore **Agent current consumer/source -> App
normal014 consumer adoption -> Runtime ordinary014 requalification and RT07
code-only retirement**. This order keeps the old writer present until its
consumers have moved and keeps `TimelineSession.restore` in the Agent lifecycle
owner. Runtime catalog archive/unarchive remains a catalog lifecycle operation;
historical flat-film restore is the native `timeline.restore` command, not a
reason to revive the old route.

The advertised
`/v1/attempts/{attempt_id}/publish-timeline-render` operation and its generated
OpenAPI/Python client cleanup remain a separate future contract artifact/version
item after consumer migration. Do not silently mutate ordinary014's producer
or artifact to remove that operation in this retirement.
