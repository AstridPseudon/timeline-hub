# M2 authored stable word references (design and bounded spike)

Decision: the canonical authored value determines the film. Accepted records are
undo/rebase provenance; they are not needed to interpret a saved revision. This
supersedes the 437a4b6a accepted-history fold and its proposed restore provenance
read. RestoreArgs, Runtime DTOs, ports and ABI remain unchanged.

## Authored schema

Use the existing clip `app.astrid` namespace. Keep `on` and `until` as human text
echoes. Add one small typed map, `word_anchors`, with independently optional `on`
and `until` entries. Each entry has exactly this shape (optional defaults omitted):

```json
{
  "source": "occurrence:occ/clip:voice",
  "document": {
    "document_id": "transcript:<existing main document identity>",
    "version": 1,
    "content_digest": "sha256:<64 lowercase hex digits>"
  },
  "word_ids": ["word:<existing main-v1 stable word identity>"],
  "edge": "start",
  "offset_s": 0,
  "offset_frames": 0
}
```

`source`, `document`, and nonempty ordered unique `word_ids` are required.
`document` is the existing exact transcript DocumentPin, not a new DTO. The
transcript content must be `media.transcript/v1`; IDs use main's existing
`word:<64 hex>(:<positive collision suffix>)?` format. A phrase names every
consecutive word of one segment. `edge` is optional `start|end` (default start);
`offset_s` is an optional finite JSON number (default zero); `offset_frames` is an
optional integer (default zero). Seconds are read as decimal rationals and frame
offsets use the exact rational canvas fps. The spike lowers seconds through
main Moment grammar and refuses values beyond its six-decimal precision; it
preserves all supported digits instead of using the lossy human formatter. No extra type/version wrapper is needed:
the namespaced key defines the type, the pinned transcript defines the ID schema.
No unknown fields inside a typed entry; unrelated namespaced data is preserved.

The raw occurrence/clip reference is mandatory even when another clip has the
same CAS, exact transcript pin and exact word ID. The source shot is resolved
through the current occurrence; the binding never chooses by timeline order.
The spike bounds targets to parent clips and sources to occurrence-owned clips.
Production must use the canonical ownership/materialization adapter for all other
scopes; it must refuse unsupported shared-shot shapes, never guess an owner.

## Clear, precedence and reads

A present reference is authoritative, including edge and offsets. Its echo may be
stale, absent or differently worded; it is never used to reselect or retime it.
Changing a reference and its normal picker echo is one recorded edit. Clearing a
field removes BOTH the echo and the reference entry, preserving the other field
and all opaque siblings. Null is the command's explicit clear, not a stored ref.
An echo-only write cannot retarget a present reference. Replacing it with a legacy
text declaration must explicitly clear the reference in the same edit.

Without a reference, a legacy word declaration may compile only when exactly ONE
phrase occurrence in authorized retained inputs and visible source windows
matches. A line qualifier can narrow this pool; an ordinal cannot recover a lost
stable choice. Repeated matches, including reused-CAS raw clips, refuse with the
exact message `ambiguous anchor; choose occurrence`. Missing matches refuse. A
new picker selection stores the stable reference; legacy reads never persist one.
Nonword declarations retain their existing compiler semantics.

A missing stable ID, exact pin, source owner/raw clip, media match, or selected
word outside the half-open source/derived interval refuses clearly. Missing or
revoked inputs never cause latest-version, text, ordinal or alternate-clip fallback.
A word may end exactly at the source window end; a word starting there is outside.

## Compiler adapter, before registry activation

The pure test-local adapter first extracts the authored entries from a raw
canonical bundle and authorized retained VerifiedDocuments. It lowers each entry
into existing WordBinding values, resolving the owner through current placements.
It constructs a private Moment spelling from the exact selected IDs plus typed
edge/offsets, never from the human echo. The existing kernel checks identity,
scoped exact pin, media, consecutive IDs, source maps and windows. A small pure evaluator change resolves the bound edge directly, without any
text search; phrase spelling is checked against those exact IDs only. It cannot
search the transcript/film for a replacement. The adapter returns the unchanged authored bundle and derived timing.
A raw JSON canonical bundle plus retained inputs suffices, without accepted history.

This adapter is defined and tested before test-local operation registration.
`clip.anchor` (test-local only) takes field, declaration echo, and the typed choice
(or null/null clear). It records ordinary writes to BOTH namespaced fields,
source/target owner and media identity guards, the existing transcript dependency
and follow source binding. There is no binding-state fold or synthetic history read.

The test-local compile-input hook validates references after native command,
inverse, restore and replay execution, so source edits cannot accept invalidated
anchors in this experiment. This is not product registry or default compiler
activation. First-use authorization/hydration of pins from this operation's args,
all-scope ownership codecs, production persistence of derived timing and consumer
parity remain separate qualification work. The real Runtime fixture pre-retains
V1 through its existing immutable document input seam; it does not pretend to
implement first-use pin discovery.

## Guards, rebase, undo and restore

Record target clip identity; exact authored writes, including unchanged echoes;
source occurrence/shot/raw clip identity, asset and media; and exact transcript
pin. Source order/start/window are derived inputs, not direct follow-policy guards.
A disjoint source move/reorder rebases and follows the SAME selected IDs and raw
clip under the current supported map. Source loss/replacement, changed target
field/reference, concurrent clear, or out-of-window words refuse. Existing server
rebase and inverse guards handle competing writes, ancestry and ABA. Undo B
restores A's reference AND echo by normal recorded writes; inverse of inverse
restores B exactly. No whole-parent undo mechanism is added.

Two identical echoes choosing different words (or different raw clips of the same
CAS) MUST produce different canonical revisions and content digests. Revision-only
restore of either source recovers its own reference and timing, including after a
Runtime restart. Restoring and undoing the restore uses existing revision closure
and provenance checks. No full history binding fold is needed to define a film.

## Evidence and boundary

`tests/editing_conformance/word_binding_recipe.py` is the test-local adapter and
recipe; `test_word_binding_recipe.py` drives actual Runtime acceptance/rebase,
restart, guarded inverse/redo, native revision restore, source moves/reorder,
reused-CAS clips, rational fps, windows, clears and invalid IDs/pins/sources.
The original same-revision collision assertions remain as strict expected failure
(the obsolete history-fold assertion is retired with the fold); its positive restore requirement now passes.
The report records exact executed tests and remaining unverified boundaries.
No new production operation, port, restore argument, history semantics, general
feature, producer carrier or compiler activation is introduced.
