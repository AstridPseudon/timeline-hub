# Optimistic suffix basis — M0 proposal

Design only, 2026-10-19. PLAN §§2.6–7 and 4.1 govern. Agent owns command
semantics/schema; Runtime owns request/port/history DTOs; App owns its outbox.
This proposes a narrow addition to shared `design/commit-contract.md` §4.1;
it does not change that canonical contract or claim implementation/approval.
The Agent worker has published shared `design/suffix-basis.md`; this Runtime
contribution uses the same selector and adds an exact proposed history projection,
ID mapping, refusal and multi-gesture details. Canonical reconciliation remains
with the three managers.

## Smallest addition

Let B be the accepted base pair, P the exact in-flight prefix, V = P(B) its
original optimistic result, I intervening accepted edits, C P's accepted result,
and H the current accepted head. S was authored on V, which need not equal C.
`expect`, bindings, allocated IDs and recorded reads describe S's dependencies;
they do not identify V. Existing wire fields alone cannot prove that basis.

Add **one optional request field**:

```text
CommitRequest.base_view?: "accepted"|"original-result"  # default accepted
```

Absence or `accepted` retains the accepted-image meaning. With this selector, the existing
`base_publication_id` names accepted P and `base_revision_id` must equal P's
accepted revision C. Together they identify the accepted predecessor, while the
selector explicitly makes S's semantic base P's **original** result V. This is
a documented alternate base view, not a claim that S was authored on C. No
additional prefix publication ID, client snapshot, digest, or replay plan is
needed on the request. The selector participates in the existing request hash.

Retain original semantic input at each accepted publication, alongside the
existing executed `records`:

```text
HistoryEntry.original: {request: CommitRequest, captures: SavedCaptures}|null
SavedCaptures = {
  selected_media: {selection: MediaSelection, value: VerifiedMedia}[],
  transcript_source: {pin: DocumentPin, value: VerifiedDocument}[],
  narration_take: {refs: NarrationTakeRefs, value: VerifiedNarrationTake}[]
}
```

These reuse §4.1 types. Runtime copies `request` from its immutable captured
context and `captures` from actual request-scoped reads, then persists them in
the same transaction/record as the receipt, history edge and executed recorder.
They are never caller-supplied authority. Empty capture arrays are valid. Exact
base/source/shot closures remain in existing immutable revision storage and are
read through `revision_closure`/`shot_closure`; retain their declared pins and
verified closure rows too. A source value which cannot be recovered exactly
must be retained, or reconstruction fails. Do not rediscover today's media
selection, transcript version, narration association, defaults or created IDs.

The required pinned operation versions and preallocated IDs in the original
request make detached reconstruction deterministic. A retained normalized
original-base plan may replace repeated normalization internally, but **executed
head-relative commands are not that plan**. No extra `PreparedCommit` field is
required when Runtime retains the original request and its scoped captures.
Existing `provider_version`/`compiler_version` on the history entry identify
reconstruction semantics. Unsupported historic versions refuse; current code
must not reinterpret them. `original:null` on bootstrap/legacy entries cannot
serve as an optimistic predecessor. These are retained semantic history fields,
not a second retry ledger or publication mechanism.

Existing `history_entry`, bounded `history`, closure and dependency reads suffice;
no endpoint or port method is added. Extend their request-bound admission to
include the verified original-input chain and its declared immutable source pins.
Current digest equality still rejects incompatible generated consumers; ABI 1
and the existing renderer-free commit door remain unchanged.

## Provider algorithm and checks

1. Authenticate, authorize and check exact idempotent replay first, as in the
   contract. An accepted retry returns the stored response without reconstructing
   P or reading current sources/head. A different selector/body under the same
   key is an idempotency mismatch.
2. Resolve the base pair to an actual same-realm/project/timeline publication.
   For accepted view, load its exact closure and stop: this is root R. For
   original-result view, require non-null original input, reconstruct its request's
   base view first, then deterministically apply its retained commands/captures.
   This produces V. Collect only the publication IDs traversed as optimistic
   predecessors into K. Use an iterative visited set/memoization, not unbounded
   Python recursion. Each referenced base pair must agree with its receipt and
   be an earlier ancestor of that publication's previous head; prove R and K are
   on H's accepted ancestry in order. Reject cycles, mismatched pairs, missing
   history/captures/closures and unrecognized versions. A preview or local key
   is never a predecessor. Publication IDs grant no authority: recheck current
   caller access to the timeline and every source read. Another publisher's
   record is usable only with the same ordinary scoped read/write permissions;
   the caller cannot impersonate its publisher or manufacture its dependencies.
3. Apply/normalize/record S once on detached V. Resolve original selections,
   bindings and IDs there; verify supplied guards against **that image at each
   command ordinal**, and derive required reads, writes, membership/order and
   structural dependencies server-side. Supplied refreshed, omitted or extra
   metadata cannot waive actual dependencies. No created ID is allocated twice.
4. Read every accepted edge in (R,H], excluding **only** K, since those prefix
   effects are already represented in V. Check remaining direct writes against
   S's complete read/write/selection/reference/ownership footprint, using token
   ancestry and structural overlap. This includes I before P's acceptance and
   same-value A→A / A→B→A. Never start this scan at C, ignore all of P's ancestry,
   exclude all same-author edits, or infer safety from V/H value equality.
   Unknown writer intent/history fails closed under the existing contract.
5. Translate original scoped identities through verified accepted predecessor
   `receipt.result.id_map` values only. Maps compose in predecessor order, must
   be injective/same-kind and refer to actual created identities/declared
   references in accepted closures. Missing entry means identity only if the
   accepted created record proves the identical ID survived. A missing/colliding
   target is a dependency conflict. R4 also uses id_map for revision metadata;
   do not treat those entries as entity renames. Rewrite only typed references
   and recorded states on a detached server plan, never opaque strings or App
   request bytes. Server replay may return its own authoritative map for S.
6. Use S's original recorded intention for the sole semantic replay onto H;
   P is reconstructed for verification and **not reapplied to H**. Prefix writes
   are excluded from the foreign-write scan, but differences between their
   original and accepted results are still checked by replay's value/selection/
   binding guards. A changed read conflicts by default. Only an operation's
   declared versioned policy can admit a changed value or following anchor;
   refreshing guards is not a merge policy. Preserve absolute versus relative
   intent and distinguish authored anchor relations from derived compiler time.
7. Compile/validate the candidate and accept against H's revision/publication
   pair through the existing transaction. At most three head attempts reuse S's
   original plan, IDs and verified basis; refresh history/head checks, not its
   semantic origin. Runtime rechecks authority and S's consumed dependencies.
   Reconstructing P uses retained old captures, without treating P as a new
   mutation or reviving withdrawn permission. Current dependencies needed by S
   must still pass ordinary acceptance checks.

A malformed view/pair/guard is refused with structured invalid-input details;
missing historic inputs use `history_unavailable`; real overlap/changed bindings
use existing semantic conflicts. Agent/Runtime assign final discriminators in
their owned schemas. No failed path publishes partial edits or substitutes a
whole document. Exact accepted retry remains available if reconstruction of a
new descendant would now fail.

## App reservation and multiple gestures

Persist P's exact body/path/key/realm/actor and ordered newer gestures before
sending. Preserve the suffix commands, IDs, original guards and optimistic
predecessor link independently of preview snapshots. Resolve P by exact retry
after relaunch, respecting main's changed-instance fence. Atomically record its
receipt/result and remove only that prefix under the durable owner/tab fence.

Only then reserve S, with a fresh key, P's accepted base pair and
`base_view:"original-result"`. This fills a previously unknown predecessor
identity in an **unsent** envelope; it changes neither P's in-flight bytes nor
S's authored semantic commands. Durably reserve S before transmission. Crashes
before, during and after this transition must recover either the P reservation
or its acknowledgement plus S's reservation/unsent work, without losing both or
allocating a replacement for an ambiguous send. Canonical accepted output is
revision-pinned; a later head read cannot replace receipt readback. The preview
may display pending work, but cannot rewrite guards from the new accepted image.

For gestures P,Q,T authored successively on one optimistic branch: accept P;
reserve Q against P's original-result view; accept Q; reserve T against Q's
original-result view. Q's retained request recursively names P, so reconstructing
T obtains Q(P(B)), even when accepted Q is different. FIFO has one in-flight
request and one immediate predecessor link per generation; server history can
handle an arbitrary finite chain by paging/memoization. In a single pending
suffix batch, later command guards are checked after earlier commands, so
multiple queued gestures can also be sent atomically in original order. Batch
only commands belonging to the same recorded basis chain; commands authored
after adopting a different accepted image start a distinct generation. Group
IDs do not make separate publications atomic. An explicit resource limit must
return refusal and preserve unsent work; it cannot silently reset the basis.

If P is refused/conflicted, its dependent suffix has no accepted predecessor.
Keep it for explicit resolution; do not send it as if P succeeded. If acceptance
is uncertain, keep retrying P exactly. Undo of accepted P is a new edge and
counts as an intervening write/dependency change, not disappearance from K.

## Worked adversarial cases

All examples concern authored properties; other fields remain intact. These
are specification cases, not production test results. Default policy conflicts
on overlapping foreign writes; a declared policy is required where stated.

| Case | Original basis and accepted history | Required result |
| --- | --- | --- |
| Absolute same field | B.x=0; P sets x=10; S sets x=12 on V.x=10; I writes unrelated y=7; P accepted at C | S.x=12, y=7. P's write is represented, I's y survives. No delta conversion to 22. |
| Relative suffix | Same P; S nudges +2 from V.x=10 | Record at V once; replay gives x=12 with disjoint I. A changed x dependency produces conflict unless a declared relative policy admits it; never infer a new delta from C. R4 may normalize fixed nudge into absolute clip.on. |
| Prefix creates | B has no clip n; P creates n; S labels n on V | Reconstruct n from P's original input, verify accepted created record, then use accepted n (or proven mapped identity). Applying S at B would incorrectly fail. P is not added twice. |
| Disjoint I | P changes opacity; S changes label; I changes unrelated clip's authored gain | Preserve all three. Do not classify every stale base as conflict. |
| Conflicting I before P | P changes opacity; I changes label A→Z before P accepts; S expects label A | P can accept, S conflicts. Scanning only after C would hide I and permit a refreshed guard. |
| ABA/no-op | Previous case but I writes label A→B→A, or A→A | S conflicts even though V.label=H.label=A and content revision may be unchanged. Publication writes prove interference. |
| Follow versus fixed | S authors anchor a+2; I changes a's compiled time 10→20 while anchor identity survives | Explicit follow policy can yield 22 by recompilation; fixed time remains its recorded value or conflicts if its actual read changed. Stable binding alone does not authorize arbitrary changed authored dependencies. |
| Conflict/refusal of P | I deletes P's target, or P's source validation fails; no accepted P | Retain S, submit nothing as its descendant. No fabricated publication or snapshot fallback. |
| Dependent Q,T | P creates n; Q labels n; T positions n, all authored while P ambiguous | FIFO original-result links reconstruct P(B), then Q(P(B)); n remains stable. A foreign edit of T's dependency anywhere after B conflicts. |
| Restart/lost ACK | P accepted, ACK lost; S persists; Runtime and App restart; head advances | Exact P returns the original receipt/C. Reserve S against that publication's original result, then check the complete history through current H. Discovery port/credential may change after relaunch; actor/realm/path/body/key do not. |
| Invalid basis | Foreign/mismatched P/C, stale guard invented on C, missing original input/source, cycle, unavailable operation version, invalid ID map | Refuse or return the actual dependency conflict without mutation. No guessed basis, guard refresh or history from a diff. |

The **original semantic apply** V→S(V) determines intent and future optimistic
reconstruction. The **final executed apply** H→S(H) determines accepted direct
writes, read dependencies, compiler consequences and guarded inverse footprint.
Keep executed `records` as the latter; do not replace them with original writes
or a diff. For an operation explicitly allowing overwrite, if V.x=10 but H.x=20
and S sets 12, accepted inverse must restore 20, not 10. Default setter policy
would conflict in this example. Undo still checks all writes after S, including
ABA/no-ops and dependencies on created entities; it does not skip K from another
request's suffix calculation. Compiler timing is rederived, not blindly restored.

## Inspected evidence and owner follow-up

Frozen refs were read with `git show`, never checked out. Source anchors below
are relative to their respective repositories at the named R4 ref or Runtime
base `8c1830d`; these are observations, not proof of implemented suffix support.

| Source | Finding |
| --- | --- |
| Agent R4 `astrid/sdk/timeline/commit.py:RuntimeCommitService.commit` | Applies once at base; three head attempts call rebase(plan.calls). Response/acceptance retain current_plan, which may be rebased; original plan is not separately retained. |
| Agent R4 `commands.py:_invoke`, `check_expectations`, `transaction.py:Plan` | Records direct unchanged writes, expectations, bindings and created IDs; relative nudge can normalize to clip.on. Expectation checking reads the supplied checkout; it cannot authenticate an unnamed optimistic image. |
| Agent R4 `rebase.py:rebase`, `_mapping`, `_rewrite` | Replays guarded recorded calls; validates injective same-kind maps and typed rewrites. Cut split/duplicate have real identity producers; generic creation collisions conflict. |
| Runtime R4 `runtime_protocol/timeline_commit.py:accept` | Stores result/evidence/current commands/direct writes and request hash. It does not retain original request/base plan; its revision-only CAS and old no_change behavior are already superseded by the contract. |
| Runtime main `runtime_protocol/service.py:_command_record`, `_command_replay_state`; `idempotency.py:command_result` | Ledger hash/result is not the original request body. Keep main infrastructure; add original semantic input to the same accepted history and preserve its required lifetime. |
| App R4 `timelineDraftIndexedDb.ts:reserveTimelineDraftCommit`, `clearTimelineDraftCommit` | Exact request reservation and compare/delete fences are useful pieces. The file is a one-slot snapshot draft, not the required ordered semantic outbox. |
| Same file `advanceTimelineDraftBaseAfterAcknowledgement` / `advanceTimelineDraftBaseAfterHeadAcknowledgement` | Advances head/graph markers without proving S's original basis. Porting these as semantic reconciliation would leave the gap. |
| App main `src/integrations/runtime/client.ts` restart fence | Runtime instance/realm change fences operations pending relaunch; suffix recovery must preserve it. |

Owner decisions remaining: Agent confirms the canonical base-view semantics,
versioned normalization/selection/read policies and typed identity mapping;
Runtime confirms field spelling, exact capture projection/storage and generated
schema change within its existing DTOs; App confirms durable generation tracking,
reservation/ACK atomicity and preview handling. Same-publisher ancestry is not
required for integrity; current scope/authority and proven history are required.
No arbitrary client-supplied guards, map, original request or captures are trusted.

No product suites or infrastructure/install were run for this design task.
M1 owners should add the table's cases to Agent conformance, Runtime's normal
acceptance/restart/history suites and App's three-products journey, including
lost ACK plus newer suffix plus restart plus undo. Specification experiments by
another worker are separate evidence, not a Runtime/Agent/App production pass.
