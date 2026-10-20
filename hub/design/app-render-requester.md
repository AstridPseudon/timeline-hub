# App requester-side render proposal handoff (D13)

Design only, before the M1 record. Source App `2bfde69eac32335eae0bc5fa2820940c0b3c694b`.
The settled decision in `INBOX.md` (2026-10-20 00:35Z), PLAN, D13, and the
Runtime/Agent designs govern this page. Reviewed companion pins: Agent
`fc324e838fd668fc06cae906e8bcfccace86ad62`; Runtime
`9f9b25c000485e919f30f1411831fe2d5a3c1316`. This page does not claim an
implementation, generated-artifact refresh, or D13 cutover.

## Boundary and ownership

The render worker/assembler produces an immutable settled task output containing
EditCommands and rationale. It does not commit, publish a timeline, or receive
`projects:write`/`tasks:write`. The requesting App session already has the user
authority and is the only producer consumer: it reads the settled proposal and
submits it through the existing command session/outbox. Runtime validates the
producer attempt after exact accepted-receipt lookup; Agent owns the proposal
carrier, `producer.guard` recipe and goldens. These are pending owned contracts,
not App-invented DTOs or op names.

The App keeps `publishTimelineRender` and its old worker publication tests until
the replacement proves the old behavior, including cancellation, replay,
restart, historical admission, and renderer-off save. No journal, coordinator,
inline provenance copy, renderer write authority, or second producer endpoint is
part of this design.

## Current App call map (verified at the source pin)

| Concern | Current call and source | Fact / D13 consequence |
| --- | --- | --- |
| Save barrier | `useRenderState.ts:830-864` calls `flushPendingSave()` and accepts a positive numeric `expectedVersion`. | This is a current-version expectation, not an immutable revision/publication selector. |
| Render admission | `renderRouter.ts:960-1017` gets the ready `rendering.render` capability, builds `BridgeTaskAdmissionRequest`, then calls `AstridLocalClient.tasks.admit()` (`taskRoutes.ts:50-121`) with `renderAdmissionKey()` (`:925-933`). | Current body uses `timeline_ref`, `selector`, `expected_version`, and canonical head metadata; it has no accepted `canonical_revision`. The operation ID is a React ref, not reload durability. |
| Admission identity | `useRenderState.ts:914-931` receives `admission.task_id`, stores it in `activeRenderTaskId`, and starts polling. | Task ID is transient UI state. No task/run locator is in the command outbox. |
| Task read/settlement | `useRenderState.ts:741-828` calls `client.tasks.get()`; `taskRoutes.ts:141-149` reads the task. | App reads status/progress/output only. It does not call `settleAttempt`; `generated.ts:264` exposes that method but no App caller uses it. `settlement_effect: {}` at admission is not attempt settlement. |
| Output | On success, `useRenderState.ts:751-765` chooses `task.outputs[*]` and uses `client.media.contentUrl(output.media_id)`. Runtime readback separately uses `useFinalVideoAvailable.ts:222-240` (`getTask`, managed outputs) and `:103-149` pins output identity. | Current render completion has no accepted commit receipt/head/digest handoff and must not be treated as proposal authority. |
| Cancel | `useRenderState.ts:998-1031` calls `cancelAstridRenderTask()`; `renderRouter.ts:1214-1243` first cancels, then refetches a status version on a fence conflict. | This is worker-task cancellation only; it must not revoke an accepted timeline commit or invent producer authority. |
| Commit | `commitSession.ts:102-156` builds the normal `/v1/projects/{P}/timelines/{T}/commit` request and calls `DataProvider.commitTimeline`; `dataProvider.ts:678-705` calls Runtime `commitTimeline()` and requires a receipt. | This is the reuse seam for the producer proposal. |

The existing command outbox (`commitOutbox.ts:11-47,229-281`) atomically stores
the exact request/key, original intent, accepted `OutboxHead`, and serialized
`TimelineCommitResult`. That result contains the receipt, accepted revision /
publication, canonical closure, and `data.document_digest`
(`DataProvider.ts:64-72`; generated types `timeline-commit-types.ts:53-63`).
`commitSession.ts:123-143` consumes those facts to project the accepted closure.
This is enough to retain A while an intent or request is pending, but the
outbox currently has no render-continuation record. On reload, `list()` only
offers owners with `intents` or `pending` (`commitSession.ts:279-283`); an
accepted-only owner is not recovered. A fresh `loadTimelineCommandBasis()` can
read the current history head and immutable parent digest, but cannot discover
which accepted render needs admission.

## Facts the replacement must carry

Keep three facts separate and label them atomically at the App/Viewing seam:

1. **Current head:** the latest observed `TimelineCommandBasis.head`, a
   revision/publication pair. It may advance to C while a task or proposal was
   admitted from A. It is not permission to retarget A.
2. **Immutable historical target:** the accepted A pair and its content digest,
   plus the accepted receipt identity. Runtime's additive existing-spec
   selector is `canonical_revision` with the five closed fields
   `project_id`, `timeline_id`, `revision_id`, `publication_id`, and
   `content_digest`. The selector is separate from
   `canonical_head_revision_id`, which remains a current-head expectation.
3. **Unsaved preview:** the App's local command projection and its original
   command basis/generation. `commitSession.ts:196-210` already preserves a
   dependent suffix's original guards and display basis while A is in flight.
   Preview bytes are not accepted history, a render target, or producer proof.

The requester must freeze the original task-admission body/key and approved
render intent before dispatch. After the producer task settles, it reads the
normal output and forwards the original proposal commands/rationale plus the
PIN-only `producer.guard` through the same outbox. The App does not reproduce
the Agent proposal digest or rewrite numeric spelling; Runtime checks the
authoritative artifact and Agent recipe. The task/attempt pin is the settled
contract's exact `task_id`, `attempt_id`, `executor_id`, `fence`,
`runtime_epoch`, admitted target pair, and `proposal_digest`; the App stores and
forwards only the contract-provided values.

## Handoff and recovery order

The future requester flow is one serialized chain, using the existing outbox
lock and request reservation:

1. Flush/queue the user's current command intent. Capture accepted A's receipt,
   head pair and document digest; do not use the mutable head read after this
   point to rebuild the render. Freeze the immutable render admission selector,
   exact body and idempotency key before task admission.
2. Admit the render through the existing task primitive with Runtime's additive
   historical selector. Persist the task/run locator before clearing its
   admission intent. Poll the exact task ID; read the settled proposal output
   only after Runtime reports the completed/settled result.
3. Append the proposal as a normal command batch to the requesting session:
   `producer.guard` first, then the exact Agent commands and rationale. Use the
   command session's ordinary `/v1` commit and its own project authority. The
   worker never calls this path. Runtime's `producer_attempt` port rechecks
   task/attempt/project/target/digest and records the existing exact authority
   dependency; App does not add a top-level commit field.
4. On acceptance, atomically retain the accepted receipt/head/digest and the
   approved historical render continuation in the same outbox transition before
   clearing the commit flight. Runtime reuses the existing publication
   checkpoint and `AgentDependency(kind="authority", policy="exact")`; no App
   journal is introduced.
5. Admit the historical render from the retained selector and persist its exact
   task/run locator before clearing the pending admission. A render failure
   leaves the accepted edit and continuation recoverable; it never rolls back
   accepted history or silently switches to current C.

Recovery ordering is deliberately observable:

* **Lost commit ACK:** reload the outbox; retry the exact stored commit body/key.
  Runtime's exact accepted lookup returns A before producer checks. Persist the
  returned receipt and pending render, then continue; never create a new key.
* **Restart after accepted commit / before first admission:** recover A's
  selector and admit A even if the current head is C. Do not re-pin to C or
  recommit A merely to obtain a newer head.
* **Lost admission ACK:** if the exact admission body/key is durable, replay it;
  if the task locator is durable, poll that task. A changed body under the same
  key remains an idempotency refusal. Persist the original task/run linkage
  before clearing the continuation.
* **Cancelled or superseded attempt:** before settlement, acceptance refuses
  atomically and leaves the proposal/intent visibly pending or conflicted; it
  must not create a revision, receipt, checkpoint, or render. Cancellation of a
  completed task is a NO-OP. If acceptance already won, exact accepted replay
  remains valid after cancellation, lease expiry, Runtime restart, or head C.
* **Exact accepted replay:** ordinary user authority is checked, then the
  original accepted receipt wins before live producer reads. The result is the
  original receipt/revision/digest and one render, not a second proposal
  consumption. Undo does not reset producer consumption.

## Small implementation slices after the M1 record

1. **Requester/outbox worker:** extend the existing command-session ACK
   transition and recovery owner to retain the accepted render continuation;
   add a producer batch ingress that keeps original guards and dependent suffix
   order. Scope: `commitOutbox.ts`, `commitSession.ts`, provider/session seam;
   no Runtime wire edits.
2. **Render admission worker:** replace the numeric/current-head handoff at the
   App seam with the coordinated historical selector and durable task/run
   recovery. Scope: `renderRouter.ts`, `useRenderState.ts`, task read adapter;
   retain client/browser render and cancellation behavior. Viewing receives
   facts only; it does not become an App owner.
3. **Qualification/cutover worker:** prove proposal settlement/output read,
   reload/replay, and renderer-off acceptance; then audit zero old publication
   traffic. Scope: focused App tests and the existing render/task read seams.
   Delete/retire `publishTimelineRender` callers only after the paired Runtime /
   Agent qualification and D13 evidence, never as a transition shortcut.

## Exact replacement test nodes and blockers

Preserve current positives: `renderRouter.test.tsx` “produces the
SD-034-shaped payload from valid input”; `useRenderState.test.tsx` “admits a
scoped render, polls on the declared 2s cadence…”; the operation-identity and
late-cancel tests at `:900` and `:1011`; `commitOutbox.test.ts` exact A-before-B,
ACK atomicity, and reopened-owner cases; and `commitSession.test.ts` original
display closure/recovery cases. Add the following exact nodes in those existing
suites:

* `commitOutbox.test.ts`: “retains accepted receipt, immutable render target,
  and task locator before clearing a commit flight”; “replays accepted A before
  producer validation after reload/head C”; and “keeps a cancelled-before-
  settlement proposal conflicted without writing history”.
* `commitSession.test.ts`: “forwards a settled proposal through the requesting
  session with producer guard first and original rationale/guards”; “persists
  pending historical admission before ACK cleanup”; and “does not repin a
  dependent preview to current C after A acceptance”.
* `renderRouter.test.tsx`: “sends the coordinated canonical_revision selector
  and omits mutable current-head expectations”; “replays the exact admission
  key/body after reload”; and “keeps old publishTimelineRender compatibility
  until replacement qualification”.
* `useRenderState.test.tsx`: “recovers accepted A and polls its original task
  after restart/head C”; “refuses cancelled/superseded proposal settlement
  without a commit”; and “reports accepted edit/render pending separately from
  unsaved preview”.

The blockers are settled cross-repo dependencies, not reasons to invent an App
shape: (a) PLAN's recorded M1 exit; (b) Runtime's retry fix and coordinated
historical selector/artifact pin; (c) Agent's installed `producer.guard`,
proposal goldens, and executable admitted-target builder at
`spec.runtime_dependencies.publication.admitted_target`; and (d) a paired
requester/Runtime test proving the App-authenticated session's write authority.
Until those pins and tests exist, the old publication path remains live and D13
is not complete. No App full, browser, network, install, or product test was
run for this design task.
