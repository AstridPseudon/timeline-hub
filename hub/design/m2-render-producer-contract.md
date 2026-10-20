# M2 writer bundle 3: render producer contract

Settled freeze 2026-10-20: PIN-only carrier, authoritative artifact hashing,
recipe value equality, completed-cancel NO-OP and persisted completed epoch follow
Agent INBOX `proposal-numeric-forwarding` / `producer-completed-cancel` and the
manager's 00:54Z admitted-target ACK. `producer-commit-port.md` owns the matching
Runtime port design.

Design + feasibility only, 2026-10-20. Governing decisions: PLAN §4.1/4.2,
Agent INBOX 00:35 “render-handoff-contract” + 00:40 “producer-attempt-guard”,
deletion ledger D13. These settled-result decisions supersede live delivery and
running-lease eligibility. No new coordinator is required. Reviewed Agent
`fc324e838fd668fc06cae906e8bcfccace86ad62`, Runtime
`9f9b25c000485e919f30f1411831fe2d5a3c1316`.
**Old endpoint 410 HELD; all M2 integration merges HELD pending PLAN's M1 record.**
No product code, schema, endpoint, permission, DTO, table or generated client changes here.
Updated by `agt-m2-proposal-forward-goldens`, based on settled-contract `f2df6c4f`;
contract goldens exercise existing commands and a bounded forwarding spike only,
not an installed producer guard, Runtime admission qualification or media cutover.

## Next implementation slice (one screen)

1. Agent: extend bundle 2's official media insertion to the **parent** owner and
   a separately reserved asset alias. Reuse create-or-require registration;
   preserve `derive_clip_id` / `derive_asset_key` and ordinal order. Do not copy
   R4's registry upsert or let selection's variant ID replace the reserved alias.
2. Agent: add a versioned, deterministic **replace-assembled** command as the
   explicit populated-target intent. It uses the same insertion primitive and
   records the exact removed authored content. No generic whole-document save.
   Unsupported target shapes refuse with the original proposal retained.
3. Producer settles a proposal as its **normal task output**. The **requesting
   App/CLI/SDK session** reads it and commits through its existing durable outbox
   with its own authority. Add ordinary registered `producer.guard` plus the
   Runtime-owned additive `producer_attempt` port check below. Acceptance checks
   the current completed/settled result and consumes it once, after exact replay.
   No live proposal channel, borrowed credential or new coordinator.
4. Requester: add captured batch queueing (the public session currently exposes
   move/inverse), and make ACK handling durably retain the accepted receipt and
   pending revision-pinned render before clearing the command flight. Reuse the
   outbox writer and existing separated task prepare/dispatch. Keep the exact
   admission until its task/run locator is durable. No second journal.
5. Runtime owns the render admission retry regression/fix. Only after the recipe
   below passes may the real host hook and exported publication helpers switch;
   only then can D13/old 410 retire. This task requests no integration merge.

## Existing source and historical lifecycle evidence

The legacy publication/lease rows describe the predecessor path, not settled-result
eligibility. Preserve its tests until the replacement qualifies.
Paths below are relative to the named checkout; Agent is
`/home/user/work/wt/agt-m2-render-producer-plan`, Runtime is `/home/user/work/runtime`.

| Seam | Existing behavior / required reuse |
| --- | --- |
| Runtime `runtime_protocol/store.py:_admit_continuation` | Two ordered dependency edges; completed children materialized once into `continuation_admissions`. Outputs retain settlement descriptors; unique CAS input list alone cannot represent duplicate child media. |
| Agent `astrid/packs/rendering/actions/assemble_timeline/run.py:build_authoring_proposal`, `_candidate_outputs` | Exactly ordinal 0/1, distinct task IDs bound to succeeded fenced edges; one primary video each. Ignores `is_primary:false` and metadata `status:superseded`; rejects ambiguity. Child completion/list order does not choose clip order. Emits visual track, clips at 0/first duration, source [0,duration), two continuation-derived clip IDs and two asset aliases even for identical media. Registry entries include media ID, unprefixed SHA, type, duration, `origin:immutable-public`. |
| Agent `astrid/core/execution/generic_host.py:run_task`, `_publish_assembled_timeline` (~8401, 9632) | Validates attempt-local proposal path; target/version/render come from immutable admitted spec, not proposal labels. Calls publication **before** uploading/settling assembler outputs; lease pump still runs. Key is `timeline-publication-<author task ID>`. |
| Runtime `runtime_protocol/service.py:publish_timeline_render` (~7613) | Checks worker/executor identity. Exact published checkpoint replay wins before live lease checks, even after cancellation; changed semantic payload refuses. Unfinished work checks lease/fence/epoch, running/current attempt, admitted two-child continuation and target project; prepares durably, rechecks after prepare, then atomically updates projection config/registry/version, creates frozen render task and publishes checkpoint. It does not create an EditCommand parent revision/history. |
| Agent `astrid/core/execution/generic_host.py:_typed_outputs`, `_upload_outputs`, `run_task`; Runtime `store.py:_settle_attempt`, `_task_resource` | Existing normal execution artifacts are uploaded with task/attempt/project custody, settled as `result.outputs`, and read by the requesting client. New proposal content uses this return path; it does not require an in-process coordinator or pre-settlement delivery. Existing host publication runs before this settlement and must be removed only after its replacement qualifies. |
| Authority | `RuntimeProtocolClient.WORKER_SCOPES` (~4412) includes worker execution/CAS, excludes `projects:write`, `tasks:write`, admin. Runtime `server.py:_timeline_commit` requires `projects:write`; ordinary task admission requires `tasks:write`. The requesting client must already possess those scopes; unavailable requester authority leaves a proposal pending. Never lend its credential to the worker or fabricate an owner client. |
| Official acceptance | Agent `astrid/sdk/timeline/commit.py:RuntimeCommitService.commit` -> Runtime `service.py:commit_timeline` -> `timeline_commit_execution.py:CommitExecutionCoordinator.execute` -> `timeline_commit_store.py:TimelineCommitStore.accept`. Accepted receipt lookup precedes preparation/live dependency reads; acceptance has the outer transaction. `timeline_commit_port.py:RequestCommitPort.validate` rechecks captured media there. |

## Proposed commands and guards (design names, not implemented APIs)

Use the existing `EditCommand`/`CommitRequest` envelope, `args`, recorder,
`AgentDependency(kind="authority", policy="exact", pin=<JSON>)`, and grouping.
No new top-level wire fields or ABI major version are proposed. The additive port
method and normal registered command schema require coordinated official artifact
generation and consumer pins; today’s installed API does not implement them.

* Empty target: `track.create(parent, visual row)` and two official media-add
  commands in one commit. Each add captures a five-field Runtime selection,
  reserved clip ID **and independent asset alias**, fixed non-ripple start and
  source window. Registration is an insertion or an exact requirement, never an
  upsert. Media bytes remain outside deterministic command execution.
* Populated target: explicit `timeline.replace-assembled` v1, selected at parent,
  takes the approved ordered media insertions. Its schema, not an implicit diff,
  states replacement of the observed config/registry authored content. Capture
  every removed value (including unknown/null fields), collection membership and
  order, target/base publication, occupied IDs and dependencies before work.
  Preserve outer parent metadata; unsupported occurrences/shared content refuse
  until a lossless command lowering exists. Never silently append to a populated
  target, recapture against latest head, or interpret `timeline.restore` as import.
* Both routes record created track/clip/asset IDs, reads/selections, unchanged
  writes and exact media dependencies. Inverse restores removed authored bytes,
  recompiles timing and guards intervening writes including A→B→A and later
  references to newly created entities. No inverse may remove a reused binding.

The requester resolves each child's exact managed association through existing
`managed_output_page` / `managed_output` and
`timeline_commit_port.py:MediaReads.selection(association_id,object_id,version)`.
The result is `{asset,generation_id,variant_id,object_id,catalog_digest}`;
`RequestCommitPort.selected_media` captures it and `validate` rechecks it at
acceptance. This proves same project, durable available/promoted lifecycle,
unique registered variant and exact completed settlement provenance. An assembler
role flag, bare CAS digest, or a lookup of today's primary is insufficient. Keep
ordinary generation publication/settlement; do not synthesize missing variants.
The prior assembler spike's role filter is **not** a registered-lifecycle authorization proof.

## Exact settled proposal and closed command carrier

Proposed JSON object (all objects closed; version 1 is integer, command versions
remain strings; nonempty IDs, positive non-bool fence/epoch):

```json
{
  "schema_version": 1,
  "producer": {
    "task_id": "assembler-task", "attempt_id": "assembler-attempt",
    "executor_id": "render-worker", "fence": 7, "runtime_epoch": 3
  },
  "admitted_target": {
    "project_id": "p", "timeline_id": "main",
    "base_revision_id": "pr", "base_publication_id": "bootstrap-publication"
  },
  "commands": ["<nonempty array of captured existing EditCommand objects>"],
  "rationale": "Move the clip to 4 seconds; preserve café and source timing.",
  "proposal_digest": "sha256:<64 lowercase hex>"
}
```

The command placeholder is illustrative only. The complete, executable JSON is
`tests/editing_conformance/fixtures/settled_proposal_move.json` in
`/home/user/work/wt/agt-m2-proposal-forward-goldens`. Its separate authoritative
`settled_proposal_move.artifact.json` retains the unchanged captured command from
`recipe_m1_move.json` with its rational-fps timing and unknown/null authoring state. Golden proposal digest:
`sha256:a4939d8873bd3bdc4f8eb79fc973267b0b1e37bb468d89f9ea9ca3d635de0a1b`.
This is a move golden, **not assembled media insertion/replacement evidence**;
those actual commands await bundle 2 and the parent-owner work above.

Hash the ENTIRE proposal except its own top-level `proposal_digest` with existing
`astrid.sdk.timeline.commit._digest` / `_json`: sorted object keys, compact
separators, `ensure_ascii=False`, `allow_nan=False`, UTF-8, SHA-256 prefixed
`sha256:`. Retain command order, every capture/guard/reserved identity, rationale,
metadata, null and absence. No stripping recorder claims, path normalization,
recapture or default insertion before hashing. Reject duplicate/non-string keys,
nonfinite numbers and unpaired surrogates at ingress; preserve Unicode scalars
without NFC. This is the existing Python JSON profile, **not RFC 8785**: `1` and
`1.0`, `-0.0` and `0` have different digest bytes. The tests pin a finite-float and
Unicode vector. Runtime recomputes this hash from the authoritative artifact,
never from caller-reserialized commands. App forwards ordinary commands/rationale
and the original pin; it need not reproduce Python's numeric spelling. Compare
the entire suffix and rationale using existing `_command_state.equal`: finite
numbers by value, booleans distinct, object keys/presence/null and array order
preserved. No fields are stripped and no hash scheme changes. Future App
qualification must include fractional/exponent/integral-float capture values.
The raw CAS artifact digest is separate: whitespace/key layout can change that
raw digest without changing the canonical proposal digest.

`AgentDependency` is recorder output, **not** an accepted EditCommand input field.
Therefore propose the minimal ordinary registered command `producer.guard` v1:

```text
request.commands = [
  {schema_version:1, op:"producer.guard", version:"1", select:null,
   args:{pin:<ProducerAttemptPin>}},
  ...proposal.commands
]
pin = {...proposal.producer, admitted_target:proposal.admitted_target,
       proposal_digest:proposal.proposal_digest}
```

The future registry entry has closed args `{pin}` ONLY and empty intention
policy. No rationale/string binding/unknown intent encodes authority. It is the
first and only guard in the batch; nested guards, inverse, restore and extra
sibling edits refuse. `proposal.commands` contains ordinary registered edits;
unknown operations fail closed under normal registry validation. Guard envelope
validation alone is not evidence that this operation is installed.

The request-scoped Runtime port resolves the authoritative immutable settled
artifact, checks raw byte custody and recomputes its exact original proposal_digest.
It requires the derived original pin to equal `guard.args.pin`, compares the WHOLE
request suffix `commands[1:]` and request rationale with artifact commands/rationale
using existing `_command_state.equal`, and verifies request project/timeline/original
base pair against admitted_target. It repeats all checks inside acceptance AFTER
exact scoped accepted-ledger lookup and BEFORE writes. The provider checks the
closed carrier and records the returned verified pin, not caller authority.
No proposal copy, serialized JSON string or raw-byte forwarding API is carried in
the guard. A requester cannot replace commands, alter capture claims/IDs/reasons/
groups, reorder/add/remove edits, or rehash a forged artifact and retain the original
pin. Client source/actor attribution comes from the authenticated request scope;
rationale never grants it authority.

Provider calls the agreed additive `producer_attempt(pin) -> {pin:<verified pin>}`.
It passes this detached verified pin into pure execution as a private immutable
input, similar to authenticated inverse closures. The guard handler has no clock,
lease read, credential or Runtime call; it uses `Recording.dependency` to emit
`{key:"producer_attempt:"+task_id,kind:"authority",policy:"exact",pin}` and no
writes. Following commands execute normally at ordinals 1..N with their existing
records/guards/created IDs; the entire commit is one undo step. No nested record
format or invented child writes. Inverse/redo operate accepted authored records,
not a new consumption of the old proposal. Rebase retains the original admitted
base and exact commands; only normal provider replay updates expected_head.

The immutable admission must bind the same original head pair. The Agent manager's
00:54Z ACK freezes the location in the EXISTING open task spec at
`spec.runtime_dependencies.publication.admitted_target`, containing exactly the
four target fields above, alongside existing `publication.render`. This is
capability-owned spec data, not a Task/CommitRequest DTO addition. Legacy numeric
`expected_version` cannot stand in for either revision or publication. Scope and
any legacy timeline aliases must agree; missing base pair refuses. This exact
placement agrees with `producer-commit-port.md`; no builder/schema change is made
here and no old task is upgraded by inference. The current builder still lacks
this pair, so missing/corrupt original admission refuses.

## Settled authority and durable handoff

Runtime's aligned design is `design/producer-commit-port.md` (see the review
exchange in ABSOLUTE `design/runtime-coordination.md`). Exact pin spellings are
`task_id`, `attempt_id`, `executor_id`, `fence`, `runtime_epoch`,
`admitted_target:{project_id,timeline_id,base_revision_id,base_publication_id}`,
`proposal_digest`. Never persist a lease token. The requesting session retains
the original proposal/batch, base pair, approved render intent and exact scoped
commit bytes/key in its existing outbox before sending.

Runtime resolves the UNIQUE normal settled `result.outputs` object descriptor
named `authoring_proposal`, matches its immutable declared output port and actual
project/task/attempt managed association, durable available/promoted lifecycle,
raw digest and size, then reads verified CAS bytes and recomputes proposal_digest.
No worker-local path, caller URL, bare hash or today's primary output is proof.
The port captures this evidence privately; acceptance rechecks it and the exact
request/recorder/capture pin bijection, artifact byte custody, original digest and
whole suffix/rationale value equality. Caller-supplied recorder data alone cannot
authorize a producer edit. Assembly's ordered child/selection/reserved-ID checks
remain additional requirements; the move golden does not exercise them.

Inside `TimelineCommitStore.accept`, AFTER current user authorization and exact
accepted-ledger lookup, BEFORE any write, Runtime must require:

* task's CURRENT attempt equals pin; task completed (`succeeded` publicly),
  attempt settled=1; pre-settlement cancellation and supersession refuse;
* exact persisted executor/fence/epoch, admitted target and settled digest match;
  no RUNNING/unsettled eligibility, current live lease or lease pump requirement;
* unconsumed proposal. Reuse the existing publication checkpoint keyed by
  authoring task, consuming once per task (also prevents another key/actor/attempt
  consuming that digest again), in the SAME transaction as revision/history and
  receipt. Rollback/preview do not consume. Undo does not reset consumption.

Cancellation/supersession and acceptance serialize in the same transaction/mutex:
pre-settlement invalidation first refuses atomically; acceptance first preserves
the edit. Cancelling an already completed task remains main's NO-OP and does not
revoke its proposal. A requester declines by keeping/discarding unsent outbox intent
without committing it; no server revocation endpoint, journal or status.
Exact accepted replay bypasses fresh producer checks after cancellation, lease
expiry, head advance or restart, subject to current ordinary user authority. No
producer checks in replay authorization or port construction. Compare completed
epoch with its persisted epoch-matched task+attempt, not current boot/live executor.
An unconsumed completed proposal survives restart. Missing/corrupt original admitted
spec or output fails closed; no live-lease or new retention requirement.

Reuse `timeline_render_publications`: discriminator in prepared_json distinguishes
the new command handoff from legacy rows; accepted receipt + revision/publication/
content digest + approved pending render consume the proposal in acceptance.
State prepared means accepted/render-pending for that format; published retains
original render task/run. Runtime must atomically link admission and checkpoint;
today's completion helper alone is not proof. Retain old-format replay unchanged.
No separately committed preparation or second receipt journal.

`TimelineSession.flush` currently advances base/deletes pending/clears flight
without retaining the receipt. Extend that SAME durable ACK transition to retain
accepted receipt/immutable selector + pending render BEFORE clearing the flight.
Unknown outcome -> exact original commit retry. Known acceptance -> never
recommit; resume pending render. Use `RemoteTasks.prepare_admission`, freeze its
exact arguments/key durably in the existing outbox, then `dispatch_admission`;
persist the returned task/run locator before clearing admission. `AdmissionReceipt`
in `sdk/recovery.py` demonstrates the existing prepare/dispatch boundary.

Historical render is approved ADDITIVE on the existing admission spec: immutable
accepted revision + receipt publication/digest, separately named from
`canonical_head_revision_id` (a current-head expectation, not a historical
selector). Runtime owns the exact selector, retained closure resolution and
normal generated artifacts/pin coordination; see `render-historical-admission.md`.
It closes commit A -> first admission after C. For accepted render admission A,
lost ACK + C + restart + exact retry must return A's ORIGINAL task; Runtime owns
the separate freeze-before-replay bug/fix and permanent test. Never silently repin
to C. Render failure/cancellation leaves accepted edit and pending recovery intact.
No credential lending, extra write scopes, new coordinator or live proposal API.

## Acceptance recipe and evidence

1. Agent conformance: reverse child completion/list order, duplicate media with
   distinct aliases, inactive/superseded output distractors, registered output
   lifecycle/version race, occupied track/clip/asset IDs, exact create-or-require,
   empty insertion and explicit populated replacement. Assert golden authored
   state, recorder reads/order/created IDs, deterministic replay, unknown/null
   round trip, guarded inverse/redo, later dependencies and A→B→A refusal.
2. Agent guard tests after implementation: closed args and private verified pin;
   changed command/guard/identity/rationale, missing/extra/reordered siblings,
   substituted or recomputed digest, nested guard/inverse/restore, missing original
   base pair, wrong project/timeline and old-port support all refuse. Actual
   provider dry-run records authority without consuming; replay preserves original
   guards. Guarded grouped inverse/redo never consumes again.
3. Runtime existing port/acceptance suites: real settled artifact success; running,
   unsettled, failed, cancelled, superseded/current-attempt-NULL refusal; wrong
   executor/fence/epoch/target, missing/ambiguous/foreign artifact, raw/CAS/canonical
   digest mismatch and missing/extra/forged authority record refusal. Completed
   cancellation is a NO-OP; pre-settlement cancellation and supersession refuse.
   Race supersession after capture/inside acceptance: zero partial revision/
   history/receipt/checkpoint/task. Test both serialization orders. Real Node
   JSON.parse/stringify of ordinary 1.0 MUST accept; 1.5, boolean substitution,
   reordered commands/claims, changed IDs/rationale and artifact tampering refuse.
4. One-shot: two different commit keys/actors race for the same proposal, only one
   accepts; another commit after undo still refuses. Exact accepted commit retry
   returns original result after cancel/lease expiry/boot/head C without producer
   reads, while changed payload at the same key refuses. Failure before/after
   checkpoint persistence rolls back consumption WITH the receipt. Preview never
   consumes; an unconsumed completed proposal survives boot through its exact
   persisted task/attempt epoch. Declining unsent intent does not revoke it.
5. Paired real worker/requester lane with renderer stopped: worker retains denied
   commit/admission write scopes, requester commits under its own attribution,
   normal settled output is the delivery seam, zero legacy calls, reload/show/undo.
   Keep existing publication-chain positive tests until replacement qualifies.
6. Faults before send, accepted-before-response, ACK fsync, ACK before admission
   freeze, freeze before send, accepted admission before response and task-locator
   fsync: restart requester/Runtime, retain one edit/receipt and one render of A.
   Include head C before FIRST historical admission and after accepted admission
   ACK loss; Runtime owns historical selector + original-task retry proofs. App
   must qualify the same digest vectors and numeric representations on the wire.

Executable spike added only to Agent's existing suites:
`test_assembly_keeps_ordered_clip_and_asset_ids_when_inactive_outputs_precede_primary`
(two cases), and
`test_render_publication_worker_has_no_project_or_task_write_scope`.
These prove old role filtering/aliases/order and configured scope limits, not
HTTP denial, cancellation races or completed migration. Existing host-hook,
orchestration and session-recovery neighbors were also run:

```sh
PYTHONPATH=/home/user/work/wt/agt-m2-render-producer-plan PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/packs/rendering/test_assemble_timeline.py tests/packs/video_editing/test_runtime_publication_chain.py::test_render_publication_worker_has_no_project_or_task_write_scope tests/packs/video_editing/test_runtime_publication_chain.py::test_generic_host_hook_materializes_and_publishes_without_local_save_or_invoke tests/packs/video_editing/test_runtime_orchestration.py tests/sdk/test_timeline_sync.py
```

**Prior worker: 83 passed in 8.20s.** Steps 1–6 above are the required future acceptance recipe,
not executed evidence. Socket/browser/full suites, production credentials and
Runtime retry were not exercised. Use the central test service for paired/socket
tests, e.g. after implementation:
`request-test <implementation-worker> targeted --files "tests/editing_conformance/test_commit_runtime_m1.py tests/packs/video_editing/test_runtime_publication_chain.py"`,
then `wait-test <returned-result-dir>`; extend these real suites with the cases
above rather than add an isolated fake acceptance harness.


Historical settled-contract worker verification (2026-10-20, before this freeze):

```sh
PYTHONPATH=/home/user/work/wt/agt-m2-settled-proposal-contract PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_settled_proposal_contract.py tests/editing_conformance/test_recipe_m1_commands.py
```

**86 passed in 3.22s** (30 new proposal/carrier/hash cases + 56 existing recipe
cases). The first run exposed a test's wrong schema root (EditCommand instead of
CommandBatch); corrected to the existing CommandBatch definition, no schema or
product change. That predecessor's full-copy carrier and withdrawal statements
are superseded by this freeze; its positive command/hash evidence is retained.
Digest mutations demonstrate binding, not Runtime refusal.
The envelope/recorder case proves the existing closed carrier and authority
output shape only; the proposed guard is not registered or executed.
Re-ran the prior exact 83-case command above with only PYTHONPATH changed to this
worktree: **83 passed in 8.17s**. Existing source tests were not rewritten.
Touched test Ruff and `git diff --check` passed. Full/make check, socket/browser,
real-credential acceptance, cancellation/one-shot races and render admission were
not run. Product implementation and all M2 merges remain held for PLAN M1.


PIN-only forwarding freeze verification (2026-10-20, no installs):

`settled_proposal_move.json` now carries `{pin}` only, with its proposal stored as
separate authoritative fixture bytes. The original full move proposal digest above
and all prior positive capture/metadata/hash assertions remain intact.
`settled_proposal_numeric.artifact.json` adds two ordinary captured moves: first
`on:1.0`, then the original target at 4. The second command retains its actual
post-first-move capture claims; two commands expose reordering. Its exact original
proposal digest is
`sha256:a2669f27bcf2cabb6705215a1d694e08efbfb051303ce5cc2c847463865d4052`.
Both artifact files have fixed raw size/SHA descriptors in the fixture. Neither
reference digest is derived from the caller's round trip during verification.

Installed Node `v22.22.0` actually JSON.parse/stringifies the numeric artifact into
ordinary commands/rationale plus a PIN-only guard. Its `1.0 -> 1` suffix passes the
bounded helper's original artifact hash + `_command_state.equal` comparison and
executes/inverts through the existing command engine with identical records.
The helper refuses `1.5`, `true` for `1`, changed capture claims/IDs/rationale,
order/addition/removal/presence changes, pin/target/digest mutation, proposal copies
or strings, and tampered artifact bytes. Tampering also refuses if a hypothetical
descriptor is rebound, both with the stale digest and with a new artifact digest
that cannot equal the original pin. This is a value/custody spike, not an installed
Runtime guard, real CAS association, request-scoped port or admission simulation.

```sh
PYTHONPATH="$PWD" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_settled_proposal_contract.py tests/editing_conformance/test_recipe_m1_commands.py
```

From `/home/user/work/wt/agt-m2-proposal-forward-goldens`: **121 passed in 3.54s**
(the original 86 plus 35 forwarding cases). The exact 83-case render/orchestration/
session command recorded above, with PYTHONPATH set to this worktree: **83 passed
in 8.65s**. Scoped Ruff and `git diff --check` passed. No behavior test was removed,
weakened, skipped or marked xfail. No full suite, install, socket/browser lane,
actual Runtime producer acceptance/lifecycle race, historical admission or builder
qualification. Product implementation, all M2 merges and D13 cutover remain held
pending PLAN M1.
