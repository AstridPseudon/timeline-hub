# D13: producer commit, fence and render handoff (source audit; implementation pending)

2026-10-20. Read-only Runtime `9f9b25c000485e919f30f1411831fe2d5a3c1316`, Agent `fc324e838fd668fc06cae906e8bcfccace86ad62`; held Runtime cohort `5ef5c5640b9c14dfcf867c1193123e9a38a35394` store inspected, not qualified. PLAN + Runtime INBOX render-producer-authority decision govern. Old endpoint 410 remains HELD; no implementation/migration acceptance claimed.

## Orchestrator decision (INBOX labelled 2026-10-20 00:35Z)
Historical immutable selector APPROVED additive on existing admission spec. Renderer returns proposal in task output; REQUESTING existing App/CLI session commits it through its normal authority/outbox. No new coordinator/journal/renderer write scope. Additive Runtime guard port + existing authority dependency/publication checkpoint; guards after exact receipt lookup. Historical/producer implementation waits M1 record; retry bug fix proceeds now. Earlier missing-coordinator recommendation below is superseded by this caller binding. Exact selector refinement: design/render-historical-admission.md; port/checkpoint refinement: design/producer-commit-port.md (workers drafting).

## Actual actor chain and earlier coordinator audit

- Agent `astrid/core/execution/generic_host.py:9631` invokes `_publish_assembled_timeline:8401` before settlement; it reads the typed proposal, admitted `runtime_dependencies.publication`, timeline/version and render settings, then calls `RuntimeProtocolClient.publish_timeline_render:4902` with the **same worker credential** and task-derived key `timeline-publication-<authoring_task_id>`.
- `RuntimeProtocolClient.WORKER_SCOPES:4412`: `handshake`, `worker:register`, `worker:execute`, `projects:read`, `tasks:read`, `objects:read`, `objects:write`; no `projects:write` or `tasks:write`. Credential actor is the executor, not a user/coordinator. Keep this boundary.
- Runtime `server.py:1013` authorizes old publication with `worker:execute`; `service.py:7613 publish_timeline_render` calls `_assert_attempt_identity:1260` against the executor/activation and `_validate_attempt_lease:8464` against Runtime's attempt rows.
- Distinguish two mechanisms: `store.py:2551 _continuation_predecessors` + `_admit_continuation:2611` freeze two distinct same-project succeeded children in edge order into `continuation_admissions`; they confer no user write scope. Host `admit_child:4710` instead obtains signed `issue_child_authority:5905` and calls `admit_delegated_child:6101` under `worker:execute`, tied to parent attempt/project/policy/identity. Neither is an authorized commit actor.
- `astrid/packs/video_editing/shared/runtime_orchestration.py:357 admit_runtime_task` calls a **supplied** `client.tasks.create`; `admit_runtime_handoff:378`/`admit_runtime_stitch:399` have only test callers in the inspected Agent tree. They do not retain a coordinator credential or consume a later proposal. `generic_host` has no parent user client to borrow.
- Normal commit `server.py:278 _timeline_commit` requires `projects:write`, preserves authenticated `actor` as `publisher`, and rechecks it in `_authorize_timeline_commit:258`; normal `/v1/tasks` admission requires `tasks:write` at `:901`. Runtime `_timeline_authorize:2612` also checks realm, exact project and live timeline membership. `CommitExecutionCoordinator` is an in-process serializer, **not an authenticated parent actor**.
- **Blocker / Agent owner:** identify the real existing authorized caller and durable proposal consumer (approval/auto-approval, realm/actor/project binding, return route) before routing bundle #3. No production coordinator with both required scopes was established by this trace; do not invent credentials or impersonate the executor in a user callback. Runtime owner must review that binding.

## Minimum guard and durable-stage contract

1. Agent bundle #3 owns official registered-media insertion and explicit populated-target replacement, ordered child/clip/asset IDs, original base revision/publication and guards. A proposal carries selectors, never authority merely because it names a task. Versioned command args can carry the proposed producer pin; no new top-level `CommitRequest` field is necessary for that alone.
2. Old `publish_timeline_render` holds the store mutex across prepare/recheck/one transaction: same-project timeline, exactly two dependency edges plus admitted continuation, task `status == running` and `task.attempt_id == attempt_id`; lease checks require unsettled attempt, current `runtime_epoch`, exact `lease_id`/`fence`, unexpired lease. `cancel_task:5495` uses the same mutex. The prepare checkpoint is committed separately and then task/lease are read again. Preserve these checks at **new commit acceptance**, not only proposal delivery.
3. Existing `RuntimeCommitPort` (`timeline_commit.py:24`) reads head/closures/history/media/Documents/narration; it cannot read an attempt or continuation authority. `AgentDependency.kind == authority` and `_recording.Recording.dependency` already record arbitrary exact JSON pins, but **no Runtime authority validator exists for them**. Generic `reads`/`expect` are authored-model guards, not live-task validation.
4. Recommended narrow addition (Runtime-owned port/DTO, Agent-owned capture): `producer_attempt(pin) -> VerifiedProducerAttempt`, scoped by context project/timeline and the reviewed coordinator binding. Pin names authoring task, attempt, lease, fence, epoch; verified result includes immutable continuation child order/outputs and target binding. Keep returned lease values as assertions, not transferable credentials. Use existing `AgentDependency` `kind: authority`, `policy: exact` to record the verified pin; Runtime binds that record to its private capture and rejects missing/mismatched captures for a producer command.
5. `RequestCommitPort._read:173` performs the initial authorized read under the mutex. Extend `RequestCommitPort.validate:321` to reread that capture under `TimelineCommitStore.accept:648`'s existing outer transaction/mutex, **after exact receipt lookup**, before `_persist_closure/_publish`. Recheck full lease/task/continuation/target/project and once-per-authoring-task checkpoint. No provider-side SQL or network calls; no renderer or scene evaluator in save.
6. Keep `_timeline_authorize`/`authorize()` for current credential/project authority, not live attempt guards: `CommitExecutionCoordinator.execute:69` and `TimelineCommitStore.lookup:86` must recover an already accepted winner after task cancellation, restart, head advance or lease expiry. A live-fence check in `authorize()` would incorrectly block lost-ACK recovery. Before acceptance, cancellation/stale fence must leave no new revision, history, acceptance checkpoint or render.
7. Reuse narrow Runtime `timeline_render_publications`/`prepare_timeline_render_publication:2690` for once-per-authoring-task preparation and pending render, and existing command receipt/history as acceptance truth. Bind exact proposal, original command request/key, render settings/key and actor scope before send. On acceptance, extend **existing** `RequestCommitPort.persist:356` hook (already called after `_publish` in the same commit transaction) to link receipt publication, accepted revision/digest and pending render to that row. No new journal/table. Preview writes no checkpoint.
8. This is proposed checkpoint evolution: current schema `canonical_schema.py:301` permits only `prepared/published`, has version/render IDs but no accepted phase. Runtime must explicitly version its JSON/stage semantics (or narrowly migrate the state constraint); never claim today's row already represents `accepted/pending_render`. Old publish's request hash excludes attempt fences; normal commit's hash includes the entire command request. Preserve once-per-task acceptance without changing an in-flight request.
9. Stable identities: scope by realm/project/timeline/actor + authoring task; persist one exact commit flight/key and use existing `timeline-publication-<authoring_task_id>` render key. A replacement attempt may rebind a **known unaccepted** preparation with a new immutable commit flight/key after authoritative reconciliation; it must not alter the old flight under its key or create a second acceptance for that authoring task. Ordered media/IDs/proposal remain fixed; changed intent is refused.
10. Agent reuse `sdk/timeline/outbox.py Outbox.write` atomic fsync/rename and `sync.py TimelineSession.flush:216`: retain exact request before send; atomically save verified accepted receipt + pinned pending render **before** clearing flight. Today `flush:269` clears it without a render continuation. Runtime checkpoint and exact commit replay close crash-before-local-ACK gaps; coordinator recovery submits ordinary task admission and persists its exact body/key until ACK, then records the task/run link. It never recommits merely to get current head.

Port compatibility is a real contract change: Runtime owns `RuntimeCommitPort`, verified pin DTO, validation and generated contract/client artifacts; Agent owns provider use and versioned command args/recording. Publish the reviewed port/DTO compatibility change explicitly (`timeline_commit_provider.py` currently checks interface v1 + schema digest), selecting version negotiation/bump with owners; do not silently add a required method to v1. No gateway/new producer endpoint or renderer scope widening.

## First-ever historical render: executable blocker, separate from retry

`store.py:1692 _freeze_managed_render_inputs` resolves **current** `parent_composition_heads`, loads/verifies/materializes that closure, then compares supplied `canonical_project_id`, `canonical_parent_document_id`, `canonical_head_revision_id`, `canonical_occurrence_ids` at `:1820`. `canonical_head_revision_id` is an expectation, not a revision selector. Held cohort `_freeze_managed_render_inputs:1704` retains this behavior; deferring snapshot writes does not change selection.

Public historical read `service.get_project_parent_composition_revision:2530` returns immutable A; it does not freeze a render of A. Snapshot refs (`snapshot_refs.py publish_snapshot`, `store._validate_spec_snapshot_refs:512`) validate CAS/project/revision provenance and can carry an **already obtained** snapshot, but are not a public authenticated historical-closure-to-render admission operation. Omitting `params.timeline_ref` bypasses managed closure selection; caller assembly/inline snapshot/provenance labels cannot substitute for kernel-verified closure or prove canonical A.

**Required Runtime-owned task-contract addition:** an explicit immutable revision selector (include accepted revision + receipt publication/digest binding) on the existing render admission spec, distinct from current-head expectations. Resolve verified retained closure, exact dependency objects and Runtime-produced snapshot for A under the admission transaction; preserve archive/project/media/integrity/readiness checks. No caller-supplied snapshot/digest invention. This is a reviewed render spec/contract/client change; not reinterpretation of `canonical_head_revision_id`. Until it exists, retain pending A and report visible refusal; D13/410 cannot claim replacement complete.

| Interruption | Required result / current seam |
| --- | --- |
| Cancel/stale fence BEFORE commit, including after prepare | Refuse atomically, no accepted revision/render; original guards retained. Existing old-endpoint tests prove this only for old path. |
| Commit A accepted, ACK lost, then head C | Exact persisted commit retry returns A + original receipt before live producer checks; one acceptance. Current commit replay has correct ordering; producer guard/handoff not implemented. |
| Crash AFTER commit BEFORE first render admission; head now C | Recover A receipt/pending intent and FIRST admit A with stable render key. Current managed API refuses A; new immutable selector is required, not just retry-order fix. |
| Render A admitted, admission ACK lost, then C + restart/exact retry | Same original task, snapshot and object set; changed body under the same key refused. Separate owner `rt-m2-render-admission-retry` owns permanent test/fix; not duplicated here. |

## Evidence and next permanent tests (three requirements)

1. Agent+Runtime actual authorized coordinator journey: proposal order/media pins/IDs and populated-target intent; renderer write-scope denials; race cancellation/attempt replacement between capture and acceptance; no partial writes and one per-task acceptance. Include rebind of known-unaccepted preparation and exact accepted replay after cancellation/expiry.
2. Runtime+Agent crash after accepted commit but before first admission: publish C, restart coordinator/Runtime, recover exact A receipt and admit historical A once; assert snapshot/dependency bytes and artifact-only settlement, never latest C. Restore all existing old-endpoint fencing/recovery expectations on this replacement before 410.
3. Runtime permanent original-admission lost ACK → C → restart → exact retry returns original task (separate retry worker); distinguish from `tests/test_canonical_render_admission.py:520`, which tests **execution** retry via `retry_task`, not original create-task replay.

Targeted command (Runtime base, no sockets/full suite):
```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/rt-m2-producer-fence-design /home/user/work/venv-runtime/bin/python -B -m pytest -q -p no:cacheprovider tests/test_timeline_render_publication.py::test_publication_is_fenced_atomic_and_exactly_replayable tests/test_timeline_render_publication.py::test_prepared_checkpoint_cannot_publish_after_cancel_or_stale_fence tests/test_timeline_render_publication.py::test_prepared_checkpoint_resumes_on_retried_attempt_after_runtime_restart tests/test_timeline_commit_port.py::test_authority_revoked_during_provider_rolls_back tests/test_timeline_commit_port.py::test_exact_retry_rechecks_authority_without_provider tests/test_canonical_render_admission.py::test_canonical_stale_head_rejected_when_legacy_version_is_unchanged tests/test_canonical_render_admission.py::test_canonical_claim_and_retry_keep_snapshot_and_objects_after_later_publication
```
Result: **7 passed in 0.84s**. No new permanent tests/product edits; no full/browser/network runs. Source audit and test/probe results do not qualify the proposed replacement.

Actual ephemeral **service-level** API probe (no prior render, fabricated snapshot, DB audit or sockets; does not qualify HTTP credential authority):
```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/rt-m2-producer-fence-design /home/user/work/venv-runtime/bin/python -B - <<'PY'
from pathlib import Path
from tempfile import TemporaryDirectory
import runpy
from runtime_protocol.errors import ConflictError
ns = runpy.run_path('tests/test_canonical_render_admission.py')
with TemporaryDirectory(prefix='rt-producer-fence-') as tmp:
    fixture = ns['canonical_scene'].__wrapped__(Path(tmp))
    f = next(fixture)
    try:
        ns['_publish'](f)
        ns['_publish'](f, revision='parent-C', expected_head='parent-1')
        old = f['service'].get_project_parent_composition_revision(f['project'], 'main', 'parent-1')
        print('historical immutable A readable:', old['revision_id'])
        req = ns['_request'](f, head='parent-1', key='first-ever-historical-A')
        try:
            f['service'].create_task(req)
        except ConflictError as exc:
            print('first-ever historical A after C REFUSED:', str(exc), exc.details)
        else:
            raise AssertionError('unexpected historical admission success')
        result = f['service'].create_task(ns['_request'](f, head='parent-C', key='first-ever-current-C'))
        print('current C admission:', result['task']['spec']['spec']['inputs']['timeline_authority']['parent_revision_id'])
    finally:
        fixture.close()
PY
```
Output: `historical immutable A readable: parent-1`; **ConflictError** `render canonical_head_revision_id does not match the canonical timeline`, details `expected: parent-1, actual: parent-C`; control FIRST current-C admission succeeded with authority `parent-C`. Exit 0; temporary realm removed on exit.

**Ready for owner review; STOP.** Next slice: resolve actual coordinator actor/consumer, approve narrow port + historical admission contracts, then implement/test jointly with bundle #3. Existing infrastructure wins; all M2 remains held.

Latest00:40decision supersedes live lease recommendations: settled current completed attempt, target+proposal_digest binding, one-shot digest consumed in same accept transaction after exact lookup. No lease token in history. Exact accepted replay wins after cancellation/expiry. Precise final contract being drafted in producer-commit-port.md.
