# Runtime private15 current outer-source handoff check

Date: 2026-10-21 UTC

## Disposition

**BLOCKED — do not execute the native outer workflow.** The Agent source is
committed, but the combined source has not received an independent custody
approval and the native requester proof has not been authorized by the Runtime
manager. No `request-test` entry was submitted.

## Exact source identities

- Agent normal private pin: `8444290337e2f7cb22e39b995834a80cb1cc1ef2`, tree
  `238da4afbb635ca4ba3ea4730494a7bdb14c38e2`. The owned-pin review approves
  this as source-only staging against C3d; it does not approve execution.
- Agent combined outer source: `6a8dfb2286659dd67c108a230d24f14ba4599344`,
  parent `8444290337e2f7cb22e39b995834a80cb1cc1ef2`, tree
  `5f5449a2b668c96a9bc816cea1dd73eacc04f7ab`.
- Runtime private producer: `c3d26567ff6fe4e20a959476d40aff90ad23a0ca`,
  tree `f3ae49d38454ce73a9c91a954bb530b3ce51c122`; schema digest
  `84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc`
  (59 definitions, 33 operations, 12 v2 clauses).

The committed Agent source contains the reviewed host-context accessor and
advisory split, fixed `WorkspaceClient` media readers, exact selection/size/
hash/duration checks, private proposal output, and the original public
publication path. The source report records 246 targeted passes, 21 action
passes, 22 copied public-baseline passes, and one in-process C3d media-read
probe. Those are recorded source evidence, not native requester evidence.

## Why this is not ready

1. `agent-private15-combined-executable-source.md` explicitly requires the
   harness to confirm the commit/tree, an independent combined custody review,
   and one later native requester proof. It says no outer registered-task or
   native requester proof was run.
2. The ref named
   `tl/agt-review-private15-combined-custody` points to the same commit
   `6a8dfb2286659dd67c108a230d24f14ba4599344` and has no review-only diff. It
   is therefore not independent custody evidence. The similarly named
   `tl/agt-m2-private15-native-requester-proof` ref also points to `6a8dfb22`;
   it is a source alias, not proof that the requester workflow ran.
3. Earlier component reviews are not a final combined review: the host-context
   review requested changes for the advisory regression in `64f8a02`; the
   media review specifies the fixed normal-client adapter but is not an
   approval of the combined tree; and the native-proposal review rejected the
   caller-settable authority/requester/media path in `8e7b828`.
4. The combined source has the existing `TimelineSession.queue_proposal`,
   `flush`, and `undo` primitives, but the committed outer action only settles
   the managed `timeline/authoring-proposal` artifact. `queue_proposal` appears
   in the action STAGE documentation, not as an executed outer workflow in the
   changed action. Durable requester submission, lost-ack/restart retry, and
   guarded undo remain unqualified.
5. The in-process Runtime read probe does not establish the normal HTTP
   credential scopes. Runtime readiness also records execution held pending
   reciprocal Agent review and the reviewed normal pin.

## Required owner actions

- Agent manager/independent reviewer: review the exact combined Agent commit
  `6a8dfb2286659dd67c108a230d24f14ba4599344` as one source closure, including
  host lifetime, fixed client dispatch, identity conflicts, original revision
  and publication, advisory/report versus proposal settlement, and pack/host/
  SDK closure; publish a real approval or a precise finding.
- Runtime manager: after that approval, explicitly authorize the exact Agent
  commit/tree plus Runtime `c3d26567`/`f3ae49d` tuple and confirm the existing
  credential has the needed task, project media-read, and object-read scopes.
- Only then: submit one centrally managed native outer proof using the existing
  admission shape, genuine settled `generation.generate_speech` media, a
  distinct outer producer identity, the existing proposal artifact, and
  `TimelineSession` queue/flush/retry/undo. Do not replay the old inner Speech,
  group9/107, admission-only, or private392 proofs.

No Runtime source, schema, DTO, endpoint, generation, pin, release, adoption,
or test change was made by this handoff.
