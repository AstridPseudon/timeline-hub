# Runtime normal media completion fence

Audit base: Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a` (tree
`7ab412cc4bcbe517efcfa806e092336390312e18`). Worker:
`rt-m2-media-completion-fence-audit`. Read PLAN and
`design/app-auto-requester-native-adapter-stage.md` before implementation.

**ACK for normal API invalidations through the existing exact selected-media
path. No product repair or contract change is justified by the tested races.**
Qualification results and exact commands are recorded below. This is Runtime
authority/acceptance evidence; it does not qualify App native command capture,
placement semantics, production activation, or an Agent/App release tuple.

## Existing authority path

`runtime_protocol/timeline_commit_port.py`:

- `MediaReads.selection` (614) resolves the managed output association and
  registered variant into the existing five-field `MediaSelection`.
- `_output_selection_binding` (653) requires project scope, durable eligible
  output lifecycle, unique variant binding, completed task, settled owning
  attempt, exact settled output tuple/digest/size/type/role, current task attempt
  ID and Runtime-authored historical provenance (task/attempt/capability/
  executor/fence/runtime_epoch). It requires an actual historical lease ID.
- `_selected_project_media` (709) requires the scoped managed object and
  completed generation, reconstructs intrinsic/catalog facts and association,
  then compares the exact `catalog_digest`. Selection never resolves a new
  primary variant. Presentation fields are excluded by `_media_metadata` (494).
- `MediaReads.selected` (803) requires all five exact fields. The public
  `get_project_verified_media` service uses this same authority read.
- `RequestCommitPort.selected_media` (267) permits only declared selections
  and records the captured value. `validate` (387) re-reads it at acceptance.
  `TimelineCommitStore.accept` (672) holds the store mutex and write
  transaction through revalidation and publication; no API writer can slip
  between the final check and publication.

`timeline_commit_execution.py::CommitCoordinator.execute` reads the accepted
ledger before constructing a port or invoking semantics. The store repeats
the lookup inside acceptance before dependency validation. Exact accepted
replay therefore does not depend on the continued availability of live media.

`timeline_commit_producer.py::ProducerReads.capture` (224) additionally requires
an admitted `authoring_proposal` output and its exact stored commands/rationale.
Plain media completion has no such proposal. Do not prepend `producer.guard`,
fabricate a proposal pin, or add App epoch/provenance fields to use this path.

## Race classifications and evidence

New permanent tests: `tests/test_timeline_media_completion_fence.py`. Existing
helpers publish real PNG/MP4 bytes through service admission/claim/settlement.
A prepared semantic provider declares and reads the exact selection and sends
its candidate through `RuntimeService.commit_timeline`, the coordinator, real
request port and transactional acceptance. It does not implement Agent's native
placement command. The single-variant cases also exercise
`generation.create_with_variant`; the main matrix uses `generation.publish_v1`.

For each negative case the snapshot taken **after the independent invalidating
change and before refusal** must equal the resulting complete SQL dump and CAS
file contents. This includes head/history/receipts/events/projections and all
object writes. The API matrix also checks the public verified-media service
refuses the original selection without writes. Both capture and acceptance
phases are tested for images and videos, without refreshing the original pin.

| Race | Result / classification |
| --- | --- |
| Retry of completed task | Normal API invalidation. `retry_task` clears status/result/current attempt/executor before another claim; original capture and acceptance refuse. |
| Replacement executor, increased lease fence | Normal supersession after retry. Real registration and claim produce a different executor/attempt and higher fence; both phases refuse. |
| Cancellation after retry | Normal invalidation. The queued task becomes cancelled without a current attempt; both phases refuse. |
| Current attempt, completed state, settled bit, settled result | Exact checks already present. Separate SQL corruption probes at both phases refuse. Retry tests provide the reachable noncompleted state; the corrupted completed/current-attempt case checks the direct identity comparison. |
| Attempt executor/fence/epoch or association provenance changed | SQL corruption probes refuse at both phases. Same-attempt edits to these historical facts are absent from the normal APIs. |
| Runtime epoch advance / restart | A completed settlement remains historical authority. Actual boot recovery between capture/acceptance and close/reopen before capture both accept the original pin. Running-task recovery is a different lifecycle. |
| Completed attempt lease deadline passes | Not an invalidation. Clock advance past the retained attempt deadline, real lease reaper and acceptance succeed without reaper writes. Completion already cleared the task's live deadline. |
| Worker heartbeat/fail/settle after completion | Normal APIs refuse even the original lease, with no SQL/CAS writes; subsequent media acceptance succeeds. Settled attempt identity cannot be mutated this way. |
| Cancel already completed task | Main-defined no-op on task/attempt authority; acceptance succeeds. The cancel command's own receipt is independent of a timeline edit. |
| Executor re-registration / capability refresh | Changes executor registration, not the completed task or attempt; acceptance succeeds. |
| Selected output promote/pin/lease | Normal catalog/lifecycle invalidations. Even an eligible promoted output has a different lifecycle version/digest; both phases refuse the original pin. No output lease is confused with a worker execution lease. |
| New primary variant with same bytes | Real admitted `generation.variant.append` and settlement promote a second variant in the same generation. Generation version advances; original exact variant remains selected and accepts. |
| Viewed state / unrelated output lifecycle | Normal noninvalidating changes; original verified selection and acceptance succeed. |
| Changed intrinsic catalog, lost ownership, foreign association scope | Separate SQL fault probes at both phases refuse. Public catalog metadata replacement and ownership/scope reassignment of an immutable completed output are not normal APIs. Neighbor HTTP tests cover foreign project, credential scope, door origin and malformed/exact selector behavior. |
| Authorization revoked after capture | Acceptance refuses; complete SQL/CAS snapshot unchanged. |
| Exact accepted retry after task retry and restart | Original response/receipt is byte-equivalent under canonical JSON, provider called zero times, no writes. Changed payload under same key refuses before provider; fresh key with invalid media refuses. |

### Why no task-row executor/fence/epoch repair

The App report correctly identified that media binding compares provenance
with the attempt row rather than duplicating `ProducerReads._current_attempt`.
The hypothesized same-attempt task-row mutation is not reachable through the
normal mutation paths inspected here. The task-field writer census is:

- `store._claim_task` (3751): executor/fence/epoch assigned on queued claim;
  `service.claim_next` assigns its newly inserted attempt ID.
- `service.retry_task` (6190), `store.retry_run` (5876): clear current authority
  and completed status before any new claim. Run retry selects failed children.
- `store.begin_runtime_session` (1139), `_overdue_lease_rows` (3476), cancellation
  and owned-cancellation reconciliation: operate on active/interruptible work;
  completed task cancellation is explicitly a no-op (`cancel_task`, 5748).
- `service.resume_attempt` (7748): recovery of an interrupted/checkpointed
  attempt, with a new attempt and a conditional running-task update.
  Worker mutation `_validate_attempt_lease` (7546) rejects settled attempts.
- `service.recover_task_placement` (5989) requires a targeted failed/cancelled
  task via `_assert_placement_recovery_quiescent` (5939), excluding completed
  settlements. Imported host tasks are a separate capability/ingress, not a
  mutation endpoint for an existing completed generation task.

Main reference read with `git show`, never checked out:
`origin/main = 29d0954b6d78a7d7937d81bc36567b6dee7ca976`.
Its `store.begin_runtime_session`, `_overdue_lease_rows`, `_settle_attempt`,
`cancel_task` and `service.retry_task` have these same lifecycle distinctions.
In particular main clears the task deadline on completion, retains the
historical attempt deadline, reaps only running/cancel_requested tasks and
preserves completed tasks across restart. Even producer `_current_attempt`
compares task epoch with attempt epoch, not with the service's new boot epoch.
Treating every completed lease deadline or later boot as revocation would
change main behavior. Arbitrary database edits are not public API authority;
this audit does not promise validation of every mutually consistent forged row.

### Separate observed limitation

An exploratory retry → replacement claim → repeat GEN D1 publication with the
same outputs hit `sqlite3.IntegrityError: UNIQUE constraint failed:
generations.id` in `store._apply_settlement_effect` (4781). Generation IDs are
derived from task/group and inserted, so a second completed publication of that
same task was not reached. This is an existing retry/publication availability
limitation, **not an intentional policy inferred by this audit**, and not an
accepted stale-media counterexample. The final tests retain successful
replacement claim/fence invalidation; they do not encode the publication error
as desired behavior. Recommend separate owner triage if repeated completion of
one generation task is required. No unrelated repair was made here.

## Qualification

Final source tree `446d9278f9912ee254335e21b4ad98c40c57b881`:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_timeline_media_completion_fence.py tests/test_timeline_media_selection.py tests/test_timeline_verified_media.py
```

From the assigned worker worktree: **133 passed in 91.00s, exit 0**.

Central request (the HTTP/socket tests ran only here):

```sh
$ORCH/bin/request-test rt-m2-media-completion-fence-audit targeted --files "tests/test_timeline_media_completion_fence.py tests/test_timeline_media_selection.py tests/test_timeline_verified_media.py tests/test_timeline_verified_media_http.py tests/test_timeline_commit_port.py tests/test_timeline_commit_acceptance.py tests/test_timeline_producer_guards.py tests/test_generation_publish_v1_settlement.py tests/test_generation_variant_append_settlement.py tests/test_placement_recovery.py"
$ORCH/bin/wait-test rt-m2-media-completion-fence-audit-targeted-1020113424-2460
```

Here `$ORCH` is
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch`.
**307 passed, 1 default-marker deselection in 150.61s, exit 0**; summary and
full log are under `orch/tests/rt-m2-media-completion-fence-audit-targeted-1020113424-2460/`.
`git diff --check` passed. No full suite was requested or run. Only test source
changed (+411/-1 lines including the new file); product and public artifacts
are untouched. The complete report is in this worker's `DetailedReport.md`.

App may use the existing declared five-field selection and selected-media
read/acceptance guard for normal media completion fencing. It must retain its
original approval, request identity and local continuation/claim checks. This
ACK does not authorize inventing producer pins, recapturing a newer selection
after a refusal, or removing native semantic capture and production ingress
qualification. A policy requiring global restart revocation or cancellation of
already completed media would require an explicit cross-contract decision;
it is not the current Runtime/main lifecycle.
