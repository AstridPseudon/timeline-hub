# Agent private 0.2.15 outer-carrier readiness

Status: bounded owner review complete; HOLD for implementation and normal-pin proof.

This note is the Agent-side companion to
`runtime-private15-native-proof-readiness.md`. It is a source review, not a
normal pin, execution, replay, or full-suite qualification.

## Reviewed identity and scope

The Agent source reviewed here is exactly:

- commit `4d4535882f1e028805c3da178bf9a7fa53696da8`
- tree `f18245ced9c231ddf8f6f2ee64405a84d3517921`

The Runtime counterpart is exactly:

- commit `c3d26567ff6fe4e20a959476d40aff90ad23a0ca`
- tree `f3ae49d38454ce73a9c91a954bb530b3ce51c122`

The handoff reviewed was
`runtime-private15-native-proof-readiness.md`. The approved inner speech
change `74925baff` is a child of the Agent commit above. It is relevant only
as the settled inner-generation boundary: its `_speech_generation_intent`
describes the audio request passed to `generation.generate_speech`. That
inner intent, task, attempt, and managed audio identity must not be reused as
the outer authoring producer identity.

## Bounded verdict

The Runtime carrier is ready for the proposed normal producer task. The Agent
outer action is not yet executable as the requested proof at this source
identity: `video_editing.sync_draft_voiceover` still returns a report/receipt
and ends by calling the caller-bound `bound.publish(...)` path. It does not
settle the existing `timeline/authoring-proposal` result or hand it to the
existing requester outbox.

The smallest executable split is three seams around existing code, with no
new DTO, action whitelist, store, renderer, scope, or delegation mechanism:

1. **Outer producer result seam** — retain the existing
   `sync_draft_voiceover` action and pack declaration, but make its successful
   outer result the existing six-key settled producer proposal, written and
   declared through the existing managed-output mechanism as one
   `timeline/authoring-proposal` artifact. The action must stop before
   caller-bound publication. Its producer identity is the outer task's
   existing task/attempt/executor/fence/runtime-epoch context; it must not be
   synthesized from the inner speech run.
2. **Capture seam** — in
   `astrid/packs/video_editing/shared/draft_voiceover.py`, keep the existing
   script pinning, inner `generation.generate_speech` call, managed-WAV
   validation, provenance, and candidate preparation. Replace only the final
   direct publish boundary with the already-existing
   `native_voiceover.capture_draft_voiceover(...)` and
   `producer.build_producer_batch(...)` path. The capture receives the exact
   five-field project media selection and Runtime-verified intrinsic duration;
   it does not accept a caller duration or fabricate a selection.
3. **Requester seam** — after the existing producer proposal result is
   settled, the requester opens `TimelineSession`, calls
   `queue_proposal(...)`, and flushes once. Ambiguous loss or restart retries
   the same durable flight body and idempotency key. Accepted publication is
   then the only input to the existing guarded undo path. There is no second
   publish call and no worker-owned authoring authority.

The native capture, producer guard, and requester outbox are already the
small supporting units for those seams; they do not need a replacement
abstraction. If the current Python action runner cannot expose its existing
managed-output destination or outer execution context to the action, that is
the concrete implementation blocker to resolve at the current host boundary.
It is not a reason to add a new result DTO, route, scope, or caller-owned
identity field.

## Existing carrier and caller map

| Concern | Existing source and carrier | Required owner change |
| --- | --- | --- |
| Outer invocation | `astrid/packs/video_editing/actions/sync_draft_voiceover/run.py`; currently calls shared `sync_draft_voiceover` and returns `report`/`receipt` | Return/settle the existing proposal result and do not publish |
| Action declaration | `astrid/packs/video_editing/pack.yaml`; currently declares JSON `report` and `receipt` outputs | Declare the existing authoring-proposal artifact using the current output convention; retain the action and inputs |
| Human/action contract | `astrid/packs/video_editing/actions/sync_draft_voiceover/STAGE.md` | Describe proposal settlement plus requester submission, not direct publication |
| Preparation and inner call | `astrid/packs/video_editing/shared/draft_voiceover.py`; `prepare_draft_voiceover` and `runtime_synthesizer` | Preserve the inner call and all validation; split at legacy `bound.publish` |
| Five-field media carrier | `astrid/sdk/timeline/native_voiceover.py`; `_selection` and `capture_draft_voiceover` | Pass the verified selection and intrinsic duration; preserve exact-key and source-identity refusal |
| Producer carrier | `astrid/sdk/timeline/producer.py`; `guard_pin`, `capture_producer`, `build_producer_batch` | Use the existing six-key proposal and first `producer.guard`; preserve digest and outer pin |
| Requester carrier | `astrid/sdk/timeline/sync.py`; `TimelineSession.queue_proposal`, `flush`, `undo` | Submit exactly once through the durable outbox and use its guarded inverse |

The current direct caller that must be removed from the outer path is the
`bound.publish(prepared["candidate"], idempotency_key=...)` call in
`sync_draft_voiceover`. The existing `bound.validate`, `bound.diff`, and
`bound.preview` checks remain useful preparation checks, but they are not the
settlement carrier.

## Acceptance nodes

These are the exact nodes for the bounded proof. They are ordered so the
outer proposal cannot be produced before genuine speech settlement.

### 1. Runtime admission of the outer task

Use the normal producer admission already present in Runtime:

- `runtime_dependencies.publication.admitted_target` contains exactly the
  existing four target fields.
- The script is an explicit ordered input descriptor with matching ordered
  `input_object_ids` (one UTF-8 script object, with its object ID and digest
  supplied by the admitted task).
- No `edges`, `aggregation`, `script_pins`, new route, or special DTO is
  introduced.

The Runtime source uses the wire keys
`project_id`, `timeline_id`, `base_revision_id`, and
`base_publication_id` in `ProducerAdmittedTarget`. The handoff uses the
shortened names `project`, `timeline`, `base_revision`, and
`base_publication`. This note does not alter that decision: an executable
proof must use the exact c3 wire schema, or the owner must explicitly
reconcile the handoff wording before pinning.

### 2. Genuine inner speech settlement

For each planned voiceover job, the existing inner boundary remains
`generation.generate_speech`. The approved `74925baff` intent is an inner
audio request only: audio modality, required original speech selection, and
the existing voice/text metadata. It does not become the outer proposal's
producer pin.

The outer flow may proceed only after managed output validation and project
media settlement provide:

- one exact `MediaSelection` with keys
  `asset`, `generation_id`, `variant_id`, `object_id`, and `catalog_digest`;
- a matching Runtime-verified intrinsic duration; and
- the existing generated-audio/provenance fields needed by
  `capture_draft_voiceover`.

The caller cannot supply the duration, select a convenient object, or use the
inner generation task as outer authority.

### 3. Native capture and proposal construction

Call the existing native capture after speech settlement and before any
requester publication:

- `capture_draft_voiceover` validates the exact five-field selection, source
  identity, literal source extents, track, occurrence, and verified duration.
- Existing timing commands carry the concrete consequences of derived-only
  padding. `padding_seconds` is not copied into a command or metadata carrier.
- Preserve the original media on swap, the old exact selection, the
  `draft_voiceover` provenance leaf, and the existing capture shot metadata.
- `build_producer_batch` adds exactly one first `producer.guard` and retains
  the original proposal digest; it does not reserialize or rehash the
  proposal.

The settled outer proposal remains the existing six-key shape:
`schema_version`, `producer`, `admitted_target`, `commands`, `rationale`, and
`proposal_digest`. The producer fields are the outer task's identity and
fence. The proposal is not the inner generation result and contains no new
voiceover-specific DTO.

### 4. Managed proposal settlement

The action's successful output is one managed
`timeline/authoring-proposal` artifact/result through the existing generic
output settlement path. It must be durable and readable by the requester.
There is no renderer call, `assemble_timeline` call, direct authoring
publication, or second worker-side mutation in this node.

### 5. One-shot requester submission

The requester uses the existing `TimelineSession` private outbox:

1. open the session for the proposal's project/timeline;
2. `queue_proposal` once, preserving the proposal's original admitted base;
3. `flush` once;
4. if acknowledgement is ambiguous or the requester restarts, reopen and
   retry the persisted flight with the identical body and key; and
5. use the accepted publication in the existing guarded `undo` path.

The outbox must reject a second pending producer proposal, a mixed target,
or an ordinary edit while the producer guard is pending. No caller-bound
`publish` remains on this path.

### 6. Positive and refusal gates

The split is acceptable only if it keeps the existing positives and fences:

- original22 authoring positives remain positive, including ripple/hold,
  source-window, provenance, source identity, history, receipt, retry, and
  undo behavior;
- the native recipe's ripple timing remains concrete (including the existing
  4150ms outcome), while padding stays derived-only;
- stale source identity, unsupported timing, mismatched five-field media,
  mismatched intrinsic duration, missing producer guard, changed producer
  pin, mixed outbox target, duplicate pending submission, and stale/invalid
  undo remain refusals;
- the requester sees one accepted publication and the outer producer never
  adopts inner speech identity.

## One-screen implementation briefs

### `astrid/packs/video_editing/actions/sync_draft_voiceover/run.py` + `pack.yaml`

Keep the existing action name, input surface, normal task admission, and
generic host invocation. Change the success seam from report/receipt plus
caller-bound publish to one existing authoring-proposal managed result. Make
the output declaration and `STAGE.md` agree with that carrier. Do not add a
new action or whitelist. Obtain outer identity and output destination only
from the current host/runtime context; if those are not exposed, stop at
that host-boundary gap rather than inventing fields.

### `astrid/packs/video_editing/shared/draft_voiceover.py`

Preserve preparation, script pinning, inner speech invocation, managed-WAV
checks, media/provenance validation, head recheck, and existing preview/diff
checks. Replace only the final direct publication seam with native capture
and existing producer-batch construction. Pass verified five-field media and
intrinsic duration from the settled result. Do not implement speech again.

### `astrid/sdk/timeline/native_voiceover.py`, `producer.py`, and `sync.py`

Treat these as existing carriers, not new APIs: native capture lowers the
prepared result to commands; producer construction adds the one guard; and
`TimelineSession` owns durable one-shot submission, retry, and guarded undo.
Only make the smallest caller wiring needed to connect the outer proposal to
these functions. Preserve every existing exact-key, fence, digest, custody,
and replay check.

## Explicitly out of scope

- no Runtime admission/schema change;
- no new Agent DTO, action whitelist, store, renderer, scope, or delegation;
- no normal pin or execution in this review;
- no caller-provided durations or fabricated media selections;
- no repeated implementation of `generation.generate_speech`;
- no use of inner speech task/attempt/output identity as outer producer
  identity;
- no broad matrix, live replay, browser, or full-suite run.

The next owner step is to implement only these seams in the exact Agent
source, then run the targeted native recipe and producer/outbox tests. The
normal private pin and the named proof command remain a later central-service
qualification step after this source split is reviewed.
