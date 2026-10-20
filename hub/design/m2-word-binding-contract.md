# Stable word-choice recipe — executable design, awaiting review

Branch: `tl/agt-m2-word-recipe-recover`, base `b3e9d8ef31f9fcc8297ae2ac66ed7b56ad042d8d`.
No product registration, default compiler activation, schema/ABI change, Runtime
implementation or integration merge. PLAN still has M1 open. Bundle1/frozen R4 refs
remain untouched. `clip.anchor` is a DESIGN-ONLY operation name.

Recovery: predecessor `/home/user/work/wt/agt-m2-word-binding-recipe` was inspected
read-only with `git status --short`, `git diff --binary HEAD` and
`git ls-files --others --exclude-standard`. All were empty; its HEAD equals this
base. There was no partial source to transfer and no old tree was changed.

## Result and decision needed

Existing args, AgentBinding, exact transcript AgentDependency and accepted records
can preserve the complete chosen identity and recover the previous binding on undo,
INCLUDING an unchanged-text write. No persisted before-binding field or new history
store is necessary when complete authenticated ancestry is available.

**Revision-only restore is insufficient for binding-only changes.** Actual accepted
A (word 1) and B (word 2) with identical declaration text produce byte-identical
canonical documents, the SAME parent revision/digest, and DIFFERENT publications.
Current RestoreArgs `{revision_id,content_digest}` cannot distinguish A from B.
The spike refuses ambiguous extraction and retains the positive requirement as a
strict xfail. This is executable evidence requiring a manager decision before
wiring, not authorization to change the frozen schema or pick an arbitrary entry.

Smallest proposed GENERIC recipe addition, before product code: permit an
already existing general AgentRead to bind restore's exact selected publication:

```json
{"ref":"history.publication:<accepted-publication-id>","path":[],
 "state":{"state":"present","value":{"revision_id":"<revision-id>",
 "content_digest":"sha256:<64 lowercase hex>"}}}
```

This uses existing read envelopes, not a new DTO/ABI/store or private word undo.
Provider resolves this typed history reference using existing `history_entry` and
`revision_closure`, checks its exact scoped publication/revision/digest and ancestry,
and supplies that immutable value to the generic read resolver. A caller's read is
only a checked claim. Fold then selects that publication's binding state; inverse
of restore uses the ordinary accepted restore edge. No chosen publication is inferred
from a revision. Legacy restore without this read is safe only when ALL reachable
occurrences of that exact revision agree on binding state; otherwise refuse visibly.
Current State/get/claim validation does NOT implement this resolver. Review the
reference convention/context addition before code. Alternatively manager may choose
another exact publication carrier, but args alone demonstrably cannot work.

## Exact declaration serialization and first capture

`tests/editing_conformance/word_binding_recipe.py` contains the concrete closed
parameter schema and handler. Envelope: schema_version=1, op=`clip.anchor`,
version=`1`, select=`parent/clip:<raw-target-id>`, intent=`{anchor:follow}`.
This bounded spike supports parent targets and occurrence-owned source clips:

Example with deterministic main transcript IDs (project `example-project`, media `sha256:1111111111111111111111111111111111111111111111111111111111111111`, line `again again stop`):

```json
{
  "field": "on",
  "declaration": "\"again\"",
  "choice": {
    "source": "occurrence:occ/clip:voice",
    "document": {
      "document_id": "transcript:730ca2f9f65225055d1866602395f52e13323c5e943b26ee2864c96cc59df9b8",
      "version": 1,
      "content_digest": "sha256:faf5dac21aa910dfc2e994fff6e7c9833359bbc0b140ecdfcaec7651a3fab9cb"
    },
    "word_ids": [
      "word:e63e7363b2e57a71fd47b117b88342ff10a2b5ca34365f4ef81ce114692d7a95"
    ]
  }
}
```

`field` is on/until; `word_ids` is a nonempty unique ORDERED array of main's
`word:<64hex>` IDs, optionally suffixed `:<positive duplicate ordinal>` as emitted
by media_transcript.line_segment. No conversion to legacy word:segment:index.
DocumentPin has exactly document_id/version/content_digest. Clear is exactly
`{field:on,declaration:null,choice:null}` and records an absent authored leaf;
a null choice with text or a choice with null text refuses. The handler records
writes even when text is unchanged. No synthetic whole-parent image is used for
undo of a declaration.

Frontend picker operates ONCE on its original authorized snapshot: identify the
clicked source occurrence/raw clip, exact Document and consecutive words; resolve
an initial text/#n query there if used. The executable picker models a word click
in a known raw clip. The existing main-Moment ordinal counterexample is exercised
alongside it: after source reordering, the old #2 would select `other` despite the
same document and word ID. Explicit stable choice is command intent; declaration
text validates the selected phrase/line, and #n is never searched again on replay.
The direct-click form allows two identical declaration strings to bind different
words. Product UI/CLI spelling/disambiguation still needs review; there is no new
production picker here.

Server validates registered args against its schema and derives records itself.
It resolves the scoped source clip and owner identity from the original request
base, reads source asset/media identity, and checks against Runtime-captured exact
VerifiedDocuments. The pure timing kernel verifies document scope/id/version/raw
content digest, actual media, ordered/consecutive stable words, matching phrase and
line, half-open source window, supported maps and current availability. No inline
schema, inline VerifiedDocument, caller recorder or latest source is authority.
The spike first retains the transcript through the existing real Runtime fixture;
first-use pin discovery/hydration from this new operation's args remains production
work, not something this fixture pretends to implement.

## Existing accepted record carriers

Authoritative recorder emits (in addition to ordinary reads/writes/claims):

```json
[
  {
    "key": "anchor.transcript",
    "kind": "transcript",
    "pin": {
      "document_id": "transcript:730ca2f9f65225055d1866602395f52e13323c5e943b26ee2864c96cc59df9b8",
      "version": 1,
      "content_digest": "sha256:faf5dac21aa910dfc2e994fff6e7c9833359bbc0b140ecdfcaec7651a3fab9cb"
    },
    "policy": "exact"
  },
  {
    "key": "anchor.choice",
    "kind": "entity",
    "pin": {
      "target": "parent/clip:card",
      "field": "on",
      "declaration": "\"again\"",
      "choice": {
        "source": "occurrence:occ/clip:voice",
        "document": {
          "document_id": "transcript:730ca2f9f65225055d1866602395f52e13323c5e943b26ee2864c96cc59df9b8",
          "version": 1,
          "content_digest": "sha256:faf5dac21aa910dfc2e994fff6e7c9833359bbc0b140ecdfcaec7651a3fab9cb"
        },
        "word_ids": [
          "word:e63e7363b2e57a71fd47b117b88342ff10a2b5ca34365f4ef81ce114692d7a95"
        ]
      }
    },
    "policy": "exact"
  },
  {
    "key": "anchor.source",
    "ref": "occurrence:occ/clip:voice",
    "policy": "follow",
    "dependencies": [
      "anchor.transcript",
      "anchor.choice"
    ]
  }
]
```

Ordered main word IDs live in typed
args/entity pin, source occurrence/raw clip in the scoped ref, exact transcript pin
in its SEPARATE transcript dependency. `Recording.finish` already forwards the
source clip ref into command bindings; it never needs to widen legacy AnchorIdentity.
Actual Runtime acceptance validates the unchanged record envelope. No new on-disk
format, side history, retention ledger or ABI is introduced.

## Pure accepted-history extraction, inverse and restore

Input is complete scoped Runtime history pinned through the accepted head PAIR,
including bootstrap and all recorded publications. Existing Runtime verifies receipt
and record correspondence; Agent `_history` checks/paginates adjacency and `_records`
checks record shape. The test uses the authenticated public history method (one
bounded page, JSON round-trip); it does not fabricate receipts or write SQL.

Fold chronologically into a disposable map keyed by `(target,field)`:

1. A declaration/ancestor write invalidates the previous binding, EVEN when the
   before/after authored text is identical. An accepted registered declaration's
   exact entity pin, transcript dependency and follow binding install its choice.
   Clear installs no binding. Ordinary writes cannot accidentally resurrect one.
2. For each publication keep a disposable sparse first-before/last-after delta of
   binding state. A/B choices remain distinct even when their text writes compare
   equal. Before-A is obtained from the authenticated prefix, never inferred from
   text or submitted by a caller. Bootstrap declarations without recorded choice
   remain unknown; compiling them refuses until an explicit reviewed selection.
3. A guarded inverse uses its existing explicit target publications, coalesces
   their binding deltas, verifies the final binding state and restores first-before.
   Inverse of inverse works identically. This is generic accepted-history folding,
   not per-operation undo or restoring a parent's authored snapshot. Existing
   product inverse guards still run on authored writes/selections/intervening ABA.
4. A native explicit restore takes the target revision's historical binding map
   only if that revision is unambiguous. Unique-history restore and its inverse
   execute successfully in the spike. Ambiguous same-revision/different-binding
   restore requires the proposed generic provenance read above. Discarded maps
   are never persisted. Production needs the exact digest and selected publication
   verification alongside the existing closure checks, not only this fixture fold.
5. At compile, construct WordBinding from these verified maps and current owner
   projection, then pass only authorized captured sources to TimingInputs. Missing,
   foreign, revoked, ambiguous, stale or incomplete history fails closed. A pin's
   deletion/revocation must never trigger latest/ordinal fallback. There is no IO
   in the declaration handler or fold.

An after-only record viewed in isolation cannot restore A from B. Complete prefix
reconstruction is the existing-format solution; the native provider currently
loads only target/suffix records for undo and needs the generic full-history binding
context before the adapter can honestly claim this behavior in production.

## Merge/follow policy

Original args and checked recorder claims are replayed at the server. Target
identity, authored declaration writes (including same-value writes), selected source
identity/asset/media, and exact transcript pin guard author intent. A competing target
declaration/clear conflicts, including intervening ABA. Structural identity loss,
source media replacement or missing/out-of-window selected word also refuses.

Follow does NOT record source start/order or every timing read as a direct authored
intention guard. A source move/reorder may succeed; compiler recomputes timing from
the SAME source occurrence/raw clip and word IDs under its current supported map.
The exact transcript remains pinned: producer V2 is not silently adopted. Selection
membership/order is consecutive words WITHIN the exact pinned transcript, not a
guard that freezes the timeline-wide ordinal pool. No client rebase or recapture.

## Executable coverage and boundaries

`test_word_binding_recipe.py` drives native Agent execution, server rebase,
Runtime acceptance/history, restart, inverse/redo and explicit native restore via
a TEST-LOCAL registry patch. Product registry/default compiler are untouched.
Coverage includes different/equal-text A->B->undoB AFTER a source move/reorder;
word-identical reused-CAS raw sources; original-choice stale rebase; phrase order;
last-write, clear/undo, unique restore/inverse; revision collision counterexample;
missing/foreign/withdrawn pure captures, invented claims, missing IDs and incomplete
history. Existing retained-input neighbors prove actual Runtime missing/foreign/
revoked-source refusal and a fresh interpreter with retained V1 after producer V2.
The spike reload proof closes/reopens Runtime and rebuilds state from JSON history;
it is not a newly qualified production startup compiler or UI feature.

Next small implementation, AFTER review and PLAN M1: authorize the declaration's
name/schema and exact restore provenance carrier; add a generic immutable history
read/binding context over existing port methods; capture exact first-use transcript
pins from args; register the handler and pure fold; connect the compiler input adapter
without changing default compilation. Then qualify native known/unknown declarations,
all source/target ownership/materialization codecs, multi-field anchors, clear aliases,
accepted projection/reload/restore and existing consumer timing parity. Only the later
reviewed migration can activate the sole compiler and delete old derived writers.
Pack snapshot custody, completed-cancel and producer numeric forwarding remain their
owners' separate agreed seams. This task adds no alternate port or producer carrier.
