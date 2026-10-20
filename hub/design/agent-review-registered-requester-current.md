# APPROVE bounded — registered assembler requester

Independent read-only review, 2026-10-20. No blocking defect found in the cumulative requester delta. Approval covers consuming a settled registered assembler proposal and submitting it through the requesting client's existing outbox on the qualified private native cohort. Public native activation remains HELD.

## Exact source and scope

- Reviewed commit: `32d6de6a8a50f05032a9b1f110ff1ac5a8975f4f`, branch `tl/agt-m2-registered-proposal-requester`.
- Reviewed tree: `4c000d64c9048910889266f00fd4036a47ffebd3`, exactly matching final central result 25049.
- Delta base/sole parent: `0536d2467aa73bb89d16657bc21fd9b856a4a149`. Seven changed files, +403/-23; product changes only `astrid/sdk/timeline/assembly.py` (+80) and `sync.py` (+31).
- Assigned review checkout remained unchanged at `ce363f6d6d60e504dbd4d79803c2d6299f648ade`, tree `78af007de1d7c5a59f86fffacd9823de355cd260`. Tests used private archives of the reviewed revisions, rather than this different checkout revision.
- Native Agent parent: `b5cfce5096f91f39bfb86d39823f97f0f59ce8a2`; Runtime: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`. All seven product overlay SHA256 values match the handoff. The unmodified parent schema has 53 definitions, including the full S2 floor, SHA256 `fafb1985a326e6121aa8c9fb34bbda196edc3dfaf462352070372e631bea1f52`.

Read PLAN.md first and reviewed the handoff/report, complete delta, relevant parent producer/outbox/schema code, and Runtime producer capture/acceptance code. No host credential, publication, family mapping, public artifact, pin, schema or canonical format change occurs in this delta. No accepted journal was introduced. The two held legacy completion tests are unchanged byte-for-byte against the base.

## Findings

1. **Custody and provenance are bounded correctly.** `assembly.py:60` reads public getTask, requires the exact completed task/attempt/project/capability and admitted target, selects a unique declared proposal output and matching task-scoped managed association, checks selectors, durable eligible lifecycle, size/media/object identity and provenance, and hashes the downloaded bytes. Duplicate JSON keys, unknown proposal/producer/target/command envelope fields, altered inner digest and changed original target refuse before queueing. Child admission retains exact association ID/object/version and ordered occurrences; unique CAS authorization does not collapse duplicate occurrences. The proposal association is selected by task/attempt/output port; Runtime, rather than a requester-supplied association token, captures and rechecks its complete ID/version-bearing row.
2. **The original proposal survives queueing and retry.** `sync.py:218` delegates to the existing producer batch builder; `queue_proposal` preserves admitted revision/publication, commands and rationale and isolates the batch. `flush` writes the complete serialized request and key through the fsynced atomic outbox before POST, and retries that flight without reading a new head or artifact. ACK cleanup removes its rationale only after successful acceptance. Local probes cover invalid metadata/bytes/schema, pending/body/base/path/key/mode mismatches and exact retry. Noncanonical serialized rationale tampering was tested locally; changed rationale acceptance refusal is separately covered by real Runtime tests and the existing HTTP evidence. These checks do not make the outbox a tamper-proof authority store.
3. **Runtime supplies the acceptance authority.** On Runtime `2c4ac180`, `timeline_commit_producer.py` checks persisted current task/attempt/executor/fence/epoch/project, completed settlement, managed object custody and actual CAS bytes, strict proposal shape/digest, original admitted target, and exact commands/rationale. It rejects nested/duplicate authority guards and extra authority operations. `RequestCommitPort._producer_captures` rechecks the complete capture, including association lifecycle/version and child custody; `TimelineCommitStore.accept` validates inside its existing mutex/transaction before persistence. The local Runtime tests assert unchanged database dumps AND total_changes on refusal, including stale attempts, cancellation before completion, changed values/digests/rationale, forged provenance and capture races. Completed-task cancellation is an existing no-op, not a new cancellation fence.
4. **Rebase and inverse limits are honest.** The unchanged final central pair proves disjoint existing-track label preservation, original membership conflict refusal, exact full undo and refusal after a peer edits a born clip. Local producer conformance additionally covers membership/order/value interference and ABA/same-value publication guards on created assets. The latter is command-engine evidence; it is not a newly run registered-requester HTTP ABA journey.

## Tests executed for this review

All commands exited 0. Shared dependencies were read-only; bytecode and pytest caches were disabled. No full/full* suite or localhost/browser/live-socket suite was requested or run.

Set `W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-registered-requester-current`.

In `$W/review-source` (exact reviewed commit archive):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_assembly.py tests/sdk/test_timeline_sync.py tests/sdk/test_timeline_sync_native.py tests/packs/rendering/test_runtime_stitch.py tests/packs/rendering/test_assemble_timeline.py
```

**123 passed, 1 xfailed in 35.41s.** The strict xfail is the named admission task-create ACK recovery requirement.

In `$W/native-source` (native parent archive with the seven exact handoff product overlays, no generated-client substitution):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_producer_guard.py
```

**17 passed in 5.82s.** Detached provider capture and outbox tests; no Runtime acceptance claim.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_producer_insertion.py
```

**64 passed in 13.69s.** Producer lowering, duplicate-CAS order, rebase, inverse and ABA conformance.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=$W/probe-tmp $W/notes/test_requester_review.py
```

**60 passed in 3.84s.** Independent adversarial carrier/outbox probes; the review script is retained beside this report. These use fake read transports and source-archive helpers, not production generation or render evidence.

In `$W/runtime-source` (exact Runtime archive):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD ASTRID_CHECKOUT=$W/native-source /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_timeline_producer_guards.py tests/test_timeline_commit_producer.py
```

**120 passed in 99.16s.** Real Runtime service/store/CAS/port/transaction tests without HTTP; prepared provider fixtures do not prove Agent command semantics.

```sh
git diff --check 0536d246..32d6de6a
```

**Passed.** Final branch SHA rechecked unchanged; assigned checkout status clean.

## Existing central evidence inspected, not rerun

[Final central summary](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-m2-registered-proposal-requester-identity-pin94114269-integration-1020124516-25049/summary) and [log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-m2-registered-proposal-requester-identity-pin94114269-integration-1020124516-25049/log.txt): exit 0; exact reviewed tree; private inner **9 passed / 2 unchanged strict xfailed**, outer **4 passed**. Named `identity-pin94114269-integration` runs identity controls plus the private pair wrapper. The wrapper normally generates Python/TypeScript and checks the complete schema and all 75 manifest artifact hashes before running the actual registered action/host/requester tests against private Runtime `2c4ac180`; its outer identity-control Runtime is separately pinned to `94114269d1ce23ab3224d7eca5a85138ce2b5fed`. Handoff private contract `0.2.14`, manifest `sha256:48c7b6533e2774a70e36517948a18fd5cee07f4d30e8f339776be9b3ec74ed4e`.

This evidence covers authenticated HTTP createTimeline/admission, real assembler file settlement and managed reads, requester native commit, duplicate/distinct CAS cases, lost commit ACK plus requester/Runtime restart, byte-exact retry and unchanged receipt/history, immutable readback, peer preservation/conflict, and undo. The generator and HTTP pair were not independently rerun here; source identity and relevant local adversarial controls were independently checked.

## Holds and next steps

- **Public native activation HELD.** The requester tree alone lacks its next native parent helper/schema cohort; `queue_proposal` imports the parent's producer module. Compose the reviewed full source/schema/generated cohort normally before activation. This approval does not declare current public pins usable.
- **Admission ACK recovery remains unqualified.** `tests/sdk/test_timeline_assembly.py:239` retains the new strict requirement: persist the original task-create body/key in the existing outbox before sending. Current admission can recapture a new head after restart under the old key. Solve this through the existing outbox; do not add an accepted journal. Commit-flight durability is a separate proven boundary.
- **D13 deletion and render restoration remain HELD.** Preserve both legacy completion expectations/strict xfails. Child video-labelled fixture bytes, dataclass resources and source archives are not registered production generation, media decode, historical render, film playback or pixel/audio parity proof. No approval for deleting the legacy hook or changing STITCH/render mappings.

No new blocker or reason to deviate from PLAN. Recommended next step: compose this bounded requester unit with its reviewed native parent/cohort, then qualify admission recovery and render on their own requirements. No repository source changes, git mutations or shared dependency writes were made. Disposable source archives and probe temporary output were cleaned after review; retained deliverables are the report and independent probe script.
