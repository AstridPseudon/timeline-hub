# Optimistic suffix basis — narrow M0 proposal

HISTORICAL REJECTED PROPOSAL. Superseded in full by PLAN dependent-edit decision and suffix-basis.md. No base_view, original-result reconstruction or additional retention requirement is adopted. Retained only to explain the resolved escalation.

2026-10-19. Design/specification experiment only; no M1 implementation or gate
approval. PLAN governs. This closes the open basis question in edit-recipe.md
without changing that document or the Runtime/App drafts.

**Recommendation:** keep the original EditCommands, guards, bindings and allocated
IDs. Add one optional commit-envelope discriminator, `base_view`, whose default
is `accepted` and whose only other value is `original-result`. The existing base
publication identifies the acknowledged predecessor. Runtime reconstructs that
predecessor's original proposed result when `original-result` is selected. It
checks both that read basis and all relevant intervening publication writes.
The original result is a detached server computation, never an accepted revision.

This also requires retaining the original semantic request and its pinned
execution dependencies with each accepted publication. An irreversible request
hash and normalized **executed** commands alone are insufficient. This is a small
addition to existing semantic history, not another acceptance log or client
history. No new HTTP operation, outbox framework or preview token is proposed.

## Why the existing fields alone do not close it

Let B have label A. P changes opacity; its optimistic result O = P(B) still has
label A. While P is in flight, S is authored on O and changes that label, retaining
`expect(label=A)`. An Agent writes label A→B→A, then Runtime accepts P on that
newer head as publication p. Every value read by S, every binding, and every
created identity can now equal those in accepted p.

Submitting S with only p's base pair and its unchanged command fields is
indistinguishable from a new S authored **after observing accepted p**. The first
must see the intervening writes; the second legitimately starts after them.
Scanning history only after p accepts both. Comparing values accepts both.
Adding more value guards cannot distinguish them. A→A has the same problem even
when no immutable content revision changes.

`test_aba_is_executable_counterexample_to_relabelled_base` demonstrates this with
the real frozen R4 EditCommand envelope: the naive accepted-basis request passes;
the same commands with `base_view: original-result` correctly conflict. Existing
`expect`, recipe `reads`/`selections`, `bindings`, `created` and intention remain
necessary, but none currently names this origin. Encoding origin inside an op's
arguments or a magic binding would still add protocol context and overload those
fields. Since the existing publication pin already identifies p, one optional
two-valued discriminator is enough on the wire.

## Wire mapping and App handoff

P is sent normally, based on immutable pair B/b. After acknowledgement or exact
retry proves its acceptance at revision R/p, submit the retained suffix as:

```json
{
  "api_version": 1,
  "project_id": "project",
  "timeline_id": "timeline",
  "base_revision_id": "R",
  "base_publication_id": "p",
  "base_view": "original-result",
  "commands": ["the original S EditCommands, not replacement snapshots"]
}
```

The commands placeholder illustrates placement, not valid command JSON. Real
commands use the recipe's schema/version/op/select/args/recorder envelope.
The base pair **still names accepted R/p**. The new field explicitly says S was
authored on the original proposed result of p's request, which may differ from R.
It does not claim that optimistic bytes have become an accepted revision. The
ordinary omitted/`accepted` case continues to mean R itself.

Persist the exact in-flight P request/key before sending, and persist S's
commands plus their association with that in-flight predecessor separately.
On p's acknowledgement, atomically retire only P and resolve S's predecessor to
R/p with `base_view: original-result`. Reserve S's complete request and a new key
before its **first** send. This fills previously unknown acceptance identity;
it changes no command, read guard, binding or ID, and never changes a request
already sent. Exact P retries retain B/b, its original commands, optional fields
and key. Exact S retries likewise retain R/p and `base_view`.

Realm/project/timeline, stable authenticated actor and durable local owner/tab
fences remain the App contract. Credentials/door addresses may rotate only under
main's restart/relaunch rules. An uncertain prefix cannot be replaced by a new
request or inferred from the latest document. Do not send dependent S until p is
known; before P is sent, P+S may instead be one atomic batch.

One batch has one authoring basis. Keep unresolved suffix authoring on its
retained, revision-labelled optimistic preview. If the UI deliberately starts
authoring against a newly received accepted image, those commands form a new
accepted-basis batch; they cannot silently be coalesced with old S. Displaying a
canonical result does not itself retarget existing commands. This is a basis
rule for App's existing small outbox, not a new client semantic rebase.

## Runtime reconstruction and acceptance algorithm

For a publication p, define O(p) as the result of its **original submitted**
semantic request, evaluated on that request's declared basis, before server
rebase. This is not its accepted executed result A(p).

1. Authenticate/recheck scope and authority, then perform normal exact-key/hash
   lookup **first**. A matching accepted retry returns the stored receipt/result,
   with no reconstruction, current-head query or mutable dependency discovery.
   Include `base_view`, including its presence/absence, in the existing request
   hash. Changing it under the same key is an idempotency mismatch.
2. Verify R/p against immutable scoped accepted history. With `accepted`, load R.
   With `original-result`, load p's retained original request. If that request's
   view is accepted, load its original immutable base B. If its view is itself
   original-result, apply this same rule to its acknowledged predecessor. Replay
   the original ordered commands with their original versioned defaults,
   allocated IDs, selections, bindings and pinned dependencies. Obtain O(p).
   Nothing here publishes or reruns P on current head. References only traverse
   already accepted records backwards; they cannot point to an uncertain request.
3. Run S sequentially on a detached O(p) through the provider recorder. Verify
   supplied guards/reads/selections/bindings/created IDs against the reconstructed
   values and effective operation policy; reconstruct omitted recorder claims.
   A caller cannot omit a read and thereby omit the provider's actual read, or
   substitute guards captured from A(p). Mismatching supplied claims refuse.
   The reconstructed original plan is immutable for all head-race attempts.
4. Compare that plan with the accepted path, using publication ancestry **from
   its original read origins**, not just from p. A dependency inherited from B
   sees every relevant external write from B through head, including writes
   before p. Writes already represented by acknowledged predecessor commands
   are aligned by accepted publication + command ordinal + stable target ID:
   P's own acknowledged creation/set is not an external clash with S's read of
   P's result. Check its actual accepted result against the original read and
   declared merge policy; never exempt unrelated intervening publications.
   Default same-path/ancestor writes, changed authored reads, structural/reference
   dependencies, selection membership/order, ABA and unchanged writes conflict.
   Use recipe token overlap/ownership rules rather than string prefix tests.
5. Only Runtime's provider replays retained S intent on the exact current
   accepted head, preserving validated original claims and provenance. Check
   authored dependencies against that head, resolve declared follow references,
   compile timing and validate structure/references/authority. A versioned merge
   policy may explain a permitted difference; generic guard refresh cannot.
   Compiler consequences are recomputed, not copied from the optimistic preview.
   Record original proposal and actual execution separately in the same accepted
   history entry. Only the actual execution supplies writes/inverse facts for
   the new publication.
6. Runtime's normal accept transaction CASes both head pins and captures all
   consumed immutable dependencies/history. On a head race use the same original
   plan for the established three-attempt budget. Atomically publish S once with
   ordinary receipt/history/events. No scene evaluation participates.

The default experimental implementation collects the external write sets from
the original accepted ancestor through head, excluding represented predecessor
edges, and checks them against S's read/write set. It then rechecks S's original
guards on the accepted head. This is sufficient for the four-operation model.
Production must use the recipe's full structural overlap/provenance recorder;
it must not blindly ignore everything before p or exempt P's whole entity scope.
An operation with an exceptional merge policy must test its precise dependency
translation. The experiment does not implement such custom policies.

No client projection is authority. The server can prove consistency with a
declared deterministic original basis; it cannot prove what pixels a user saw.
All loaded requests/IDs remain scoped data, and current command authority is
checked again even when a predecessor was once authorized.

## Required retained context, without a second history

Add the original parsed semantic request (including base pins/view and original
commands) and original pinned dependency captures to the existing accepted
semantic record. Preserve supported operation/recorder/compiler versions needed
for that reconstruction. The accepted executed plan already has its own versions
and captures. These can share identical immutable values; no duplicate authored
branch is published. Runtime's scoped `history_entry`/`revision_closure` and
existing dependency ports can supply them; the provider DTO must expose this
context. No additional transport operation is required.

The existing exact-result ledger may retain only hash+result: do not assume it
already retains the request merely because retry works. A hash cannot reconstruct
P(B). Accepted normalized commands can also lose original intent or guards.
Recipe retention therefore needs to explicitly include the original semantic
proposal. If reconstructing an older version is unsupported, an immutable
server-derived original execution record may supply equivalent read/provenance
context; a client-supplied snapshot or freshly refreshed guards cannot.

Missing original request, original dependency versions, ancestry, or supported
execution version is a typed basis/history-unavailable refusal for a **new** S;
do not guess, silently use A(p), discover today's media, or relax guards. An
already accepted exact retry still returns its stored result. Bounds on history
reconstruction may refuse explicitly; they cannot silently truncate ancestry.
Each later optimistic generation uses the same rule recursively over the one
accepted history. An implementation may cache detached server reconstruction,
but this proposal requires no persistent virtual revision, branch, or extra log.

## Intent and hard cases

| Case | Required behavior |
| --- | --- |
| Lost P ACK; disjoint Agent edit; S; process restart | Persist P bytes/key and S unchanged. Exact P retry returns p once; S uses p's original-result basis. Disjoint authored paths survive. The spike intervenes both before P acceptance and after it. |
| Upstream authored dependency changes | Retain its original expectation and origin. A write before or after p conflicts unless the command's explicit versioned policy permits it. Never recapture a guard at accepted p. |
| Relative nudge on a following anchor | Retain delta, same stable anchor, authored expression/offset and follow policy. Re-evaluate timing at accepted head: a cut end moving 10→20 plus a +2 suffix gives 22, not an old absolute 12 or double application. The derived number is not an independent authored equality guard. |
| Fixed positioning | Preserve the authored fixed value, with provenance where a picker consumed an anchor. A +2 nudge of fixed 12 remains 14 when unrelated compiler timing changes. Changing a real fixed-resolution dependency still follows that operation's declared guard policy. |
| Anchor/source disappears or selection changes | Reject the actual binding/source/membership dependency; do not rediscover a same-text word or pick another ordinal. A follow policy permits motion of the same identity, not replacement by another identity. |
| P creates object consumed by S | Reconstruct P with its reserved scoped IDs. Align those exact IDs with P's accepted created record; S binds to that object, not to an absent object in B and not to a new allocation. Collision/deletion/ownership change conflicts. The experiment tests successful consumption; collision/ownership production behavior remains recipe work. |
| ABA or A→A publication | Inspect publication writes since original origins, including pre-p edges; equal content does not erase them. Both cases conflict in the experiment. |
| Head advances before receipt/readback | Receipt's `accepted_revision_id` and immutable child closure identify the exact accepted result. Use returned canonical document or the existing exact revision read, not ordinary head GET. Publication remains receipt identity even when content revision is reused. |

R4 source check: `commands.EditCommand` has expect/bindings/created/authorship but
no original-result basis. `rebase.rebase` requires recorded fields and replays
guards on a detached head; it cannot recover a discarded origin. `commands.py`
normalizes some `clip.nudge` calls into `clip.on`; the forward recipe's retained
explicit relative/follow intent must be sufficient to reproduce the declared
operation, rather than assuming every normalized R4 command preserves all of it.
Compiler prefix probes in `finish_recording` are not accepted prefix receipts.
These observations support additions already identified by M0, not a direct
R4 port or a claim that the current production runner meets this proposal.

## Executable experiment and verification

Agent branch `tl/agt-m0-suffix-basis`, base `e51595c68fc23d3d1734a0885c84a6511999697b`.
`tests/m0_suffix/test_suffix_basis.py` extracts **only the actual EditCommand
class** via AST from frozen ref
`origin/codex/handover-timeline-r4-20261019-candidate-sdk`
(`11caf1d9de291d76f491cf69f7942606b7471d7a`), read with `git show`.
No frozen files are checked out or overlaid. It executes its real constructor,
dataclass replacement and `to_json`. It does **not** execute `coerce`, generated
wire validation, R4 handlers, rebase, compiler, Runtime storage or App code.

The small interpreter uses four operation names (`clip.set-param`, `clip.on`,
`clip.nudge`, `timeline.add`) with deliberately reduced parameter/state semantics;
its anchor expression objects and flattened state are model data, not the
production timeline format. Recipe reads fit in `expect` in this model. JSON
round-trip simulates loss of in-memory state; it is not a database/browser crash
test. Content-identity strings stand in for revision IDs. Locks, atomicity,
authority, real schema/recorder completeness, dependency pin retention, general
path overlap, structural edits and version migration are not proven here.

Commands run from the assigned Agent worktree, with no installation/network:

```bash
python3 -B -m unittest discover -s tests/m0_suffix -v
# Initial experiment: 13 tests passed; rerun with final additions below.
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider tests/m0_suffix
# Initial experiment: 13 passed, 2 warnings (system pytest lacks pytest-timeout).
PYTHONPATH="$PWD" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/m0_suffix
# Final experiment: 14 passed in 0.15s, no warnings.
```

The shared Agent venv became ready during the task; it was not modified. No
product files were changed. Full `make check`, default pytest lanes,
editing-conformance, Runtime suites and App journeys were not run for this
isolated M0 specification. These results are **specification experiments, not
production proof**. Before M1, managers should reconcile the proposed field and
original-proposal retention into their existing schemas/provider port, then
promote these cases into main's semantic/atomic-acceptance suites and the actual
App lost-ACK/restart journey. A product implementation must prove the same
outcomes through the real recorder/compiler and durable Runtime/App boundaries.
