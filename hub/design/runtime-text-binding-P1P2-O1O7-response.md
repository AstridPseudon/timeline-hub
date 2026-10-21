# Runtime text-binding P1/P2 and O1–O7 response

Status: Runtime response for `AG-M2-TB01`, 2026-10-21.  This is a source
review against Runtime `b92d3e7` and the current Agent `tl/integration` tree.
It does not change the Agent-owned contract, product code, schemas, or tests.

## Decision summary

Runtime accepts the Agent proposal with the boundaries below.  P1 and P2 are
already present in the current Runtime commit path.  The Runtime response does
not add an endpoint, table, event journal, inline text authority, or a second
media source kind.

| Item | Decision | Implementation state |
| --- | --- | --- |
| P1 | Use the existing request-scoped commit port for an exact, project-scoped UTF-8 text selection. | Already implemented; qualification remains. |
| P2 | Derive the live binding projection and append-only event in the existing acceptance transaction. | Already implemented; qualification remains. |
| O1 | New `timeline.commit` authored rows are identity-only; old pinned rows remain read-only compatibility data. | Implemented across the current command/commit seam; legacy publication validation remains intentionally pin-oriented. |
| O2 | New selections use `text/plain; charset=utf-8`. Existing authenticated retained descriptors may remain `text/plain`. | Implemented. |
| O3 | The command selects an occurrence, whose accepted shot is the owner. | Implemented. |
| O4 | Preserve order through the Agent's recorded collection selection; do not impose Runtime canonical sorting or add an order column. | Implemented in the Agent command state; Runtime projection is keyed. |
| O5 | ACK the current exclusive-occurrence command only. Shared ownership is a separate, unqualified scope; this response does not authorize deleting shared or legacy positives or declare the whole text-binding ledger complete. | Current command is fail-closed outside exclusive occurrence ownership. |
| O6 | Runtime does not auto-migrate legacy inline `{slot, text}` rows or add a new writer. Existing kept legacy positives/callers remain live/held until an explicit Agent-owned recorded migration preserves them before retirement. | Deliberately not implemented in Runtime. |
| O7 | Runtime ACKs P1/P2 and the current scoped schema shape. Agent owns the canonical semantic schema/source; Runtime owns normal official schema/client generation, artifact digest/version, and coordinated pins. This ACK is not new release authorization. | Runtime compatibility ACK complete; normal Runtime generation/pinning and Agent source ownership remain as stated. |

## P1 — exact text selection

Decision: accept the proposed shape, but keep it as a method on the existing
`RequestCommitPort`; it is not a new public port or DTO.  The authenticated
commit request supplies the project scope.  The method accepts exactly
`object_id`, `digest`, `size`, and `media_type`, returns those fields plus
`utf8: true`, and returns no bytes.

Runtime source already provides this seam at
`runtime_protocol/timeline_commit_port.py:276-283` and the shared exact
validation at `runtime_protocol/timeline_commit_port.py:584-629`.  The latter
checks `object_id == digest`, the 0–1 MiB size range, managed project ownership,
the exact new-selection MIME, CAS size/hash, and strict UTF-8; zero bytes pass
because the lower bound is zero.  A selection must first be declared through
the port (`timeline_commit_port.py:267-283`), and captured text is rechecked
during acceptance (`timeline_commit_port.py:387-403`).

Agent already consumes this method for `text-binding.set` inputs at
`/home/user/work/agent/astrid/sdk/timeline/commit.py:900-913`.  Required owner
action: Runtime has no shape change; Agent keeps this call as the only source
of verified text input.  No fallback to inline text or to `selected_media` is
allowed.

## P2 — recorded before/after projection

Decision: accept the existing projection implementation as the Runtime
authority.  Projection happens inside the same transaction as closure
persistence and publication: `runtime_protocol/timeline_commit_store.py:712-741`.
It is derived from the accepted document and recorder facts, not from a
client-supplied projection field.

The implementation resolves the accepted occurrence to its accepted shot and
requires the recorder's `/shot` read to match at
`runtime_protocol/timeline_commit_store.py:743-764`.  It compares the recorded
before state with the live row before writing (`:766-805`), verifies the
selected object through the new-selection or retained-descriptor MIME path,
and appends the chained `shot.text_binding` event with publication identity at
`:819-832`.  A same-value binding projection returns without advancing the live
head or adding a projection event at `:813-814`; clear of an absent row is
refused at `:792-795`.  That unchanged projection result does not suppress the
explicit unchanged accepted film record/history edge: the accepted command is
still recorded in the film history.  Undo and redo therefore create their own
accepted projection events; history is not rewritten.

Required owner action: Runtime needs no new persistence shape.  The Agent must
continue recording the owner shot read and whole-row before/after write that
these checks consume.  Any missing owner read or mismatched before state stays
a visible refusal, never an overwrite.

## O1 — identity-only authored rows

Decision: yes for the new `timeline.commit` path.  An authored row contains
only the binding identity and immutable object descriptor:
`kind`, `slot`, `media_id`, `content_hash`, `byte_size`, and `mime_type`.
`binding_id`, project/shot identity, stream head, and timestamps are Runtime
projection fields, not Agent-authored authority.

The Agent implementation explicitly excludes those derived fields at
`/home/user/work/agent/astrid/sdk/timeline/native_text_binding.py:9-12` and
constructs the authored row at `:63-67`.  Runtime persists the submitted shot
payload without injecting projection fields at
`runtime_protocol/timeline_commit_store.py:834-856`, while the live resource
adds `binding_id`, `event_stream_id`, and `head` at
`runtime_protocol/service.py:3662-3689`.

Compatibility boundary: the older project-shot publication path still
requires a complete pinned descriptor, including `binding_id` and positive
`head`, at `runtime_protocol/service.py:1465-1502`.  That validator is for
historical/legacy pin publication and must not be weakened or treated as the
new command's authored shape.  Pinned script/render readers may continue using
their immutable descriptor; live readers use the Runtime projection.

Required owner action: Agent keeps the identity-only row for new commands and
adapts remaining legacy callers before retiring them.  Runtime has no code
action and must not rewrite old revisions.

## O2 — MIME string

Decision: `text/plain; charset=utf-8` is the exact MIME for a new text
selection.  `text/plain` is accepted only when it is authenticated as an
existing retained binding descriptor; it is not a new-selection alternative.

The new-selection constant and exact check are at
`runtime_protocol/timeline_commit_port.py:30` and `:584-629`.  The retained
compatibility path checks the binding's append-only event history and then
validates the old exact `text/plain` descriptor at `:588-605`.  This matches
Runtime's existing materialization of old text objects at
`runtime_protocol/service.py:3760-3803`, where the legacy object is stored as
`text/plain`.

The Agent command schema already closes new input to the charset form at
`/home/user/work/agent/astrid/core/timeline/schema/edit-command.schema.json:2631-2655`.
The Agent's `media_open` response uses `text/plain` at
`/home/user/work/agent/astrid/sdk/media_open.py:327-337`; that is a read
presentation MIME, not permission to submit a new selection with the legacy
string.

Required owner action: Runtime keeps the split policy above.  Agent keeps the
charset form in new command descriptors and treats old `text/plain` rows as
retained compatibility data only.  No MIME normalization or byte rewrite is
needed.

## O3 — occurrence versus clip/element selection

Decision: select `occurrence:<id>`.  Text is stored in the shot payload, and
the occurrence is the stable placement that supplies the ownership read; a
clip/element selector would require inventing a new text authority on those
objects.

The Agent command requires an occurrence and reads its shot at
`/home/user/work/agent/astrid/sdk/timeline/native_text_binding.py:36-45`.
Runtime makes the same decision from the accepted closure at
`runtime_protocol/timeline_commit_store.py:749-764`.

Required owner action: none for Runtime or the current Agent implementation.
Future shared-shot behavior must not be smuggled in through a clip/element
alias.

## O4 — binding order and clear inverse

Decision: use the recorded membership/order selection, not canonical
`(kind, slot)` sorting.  The authored shot payload is the order authority for
the command; a clear's inverse restores the exact prior position.  Runtime's
relational projection is a keyed live view and must not acquire a second order
authority or a new table column.

The Agent records the collection selection before appending a new row and
writes whole keyed rows at
`/home/user/work/agent/astrid/sdk/timeline/native_text_binding.py:45-67`;
the state layer restores/removes the row at its prior list index at
`/home/user/work/agent/astrid/sdk/timeline/_command_state.py:367-388`.
This is also the needed behavior for noncanonical existing order.  Runtime's
live listing is a keyed projection ordered by its existing identity query at
`runtime_protocol/service.py:3963-3972`; it does not claim to replace the
authored payload's order.

Required owner action: Agent preserves the recorded selection and exact inverse
behavior.  Runtime has no implementation action and must not sort or persist
an order field.

## O5 — shared chapter ownership

Decision: ACK the current exclusive-occurrence command only.  The current
handler refuses a shared chapter/shot closed with `unsupported_ownership`, but
shared ownership is a separate, unqualified scope rather than a Runtime
deletion or retirement decision.  This response does not authorize deleting
shared or legacy positive rows/callers and does not declare the whole
text-binding ledger complete.

The Agent checks for an exclusive occurrence at
`/home/user/work/agent/astrid/sdk/timeline/native_text_binding.py:39-43`.
Runtime independently resolves the accepted occurrence owner and refuses a
changed owner at `runtime_protocol/timeline_commit_store.py:750-764`.

Required owner action: none in Runtime for the current ACK.  Agent owns any
future shared-owner design and its fixtures; no Runtime branch, new source kind,
or cross-shot projection is authorized by this response.

## O6 — legacy inline rows

Decision: Runtime will not auto-migrate or read inline rows such as
`{"slot": "voiceover", "text": "hello"}` as authority, and will not add a
new writer for them.  The native immutable-input handler refuses inline
authority, while existing kept legacy positives and callers remain live/held
until an explicit Agent-owned recorded migration preserves them before their
retirement.  Runtime only projects a recorded immutable descriptor on the new
path.

The Agent's current row validator requires the immutable descriptor fields and
rejects an inline shape for the native path at
`/home/user/work/agent/astrid/sdk/timeline/native_text_binding.py:24-33`.
Runtime's projection consumes only a recorded text-binding write with a
validated before/after state at `runtime_protocol/timeline_commit_store.py:751-805`;
there is no inline-text branch.

Required owner action and timing: keep existing legacy positives and callers
live/held until Agent adds one explicit, recorded migration that materializes a
managed UTF-8 CAS descriptor and emits the existing binding semantics while
preserving them.  No option to discard authored rows or replace Main success
with refusal is part of this response.  A Runtime auto-conversion, new writer,
or second migration endpoint is rejected because it would create a second text
authority.  Runtime then accepts only the resulting immutable descriptor on
the new path and does nothing in this response.

## O7 — Runtime ACK and schema regeneration

Decision: Runtime ACKs P1 and P2 and the current scoped shape only.  Agent owns
the canonical semantic schema/source.  The scoped reference and command shape
are already present in that current Agent schema: the text-binding reference
pattern is at
`/home/user/work/agent/astrid/core/timeline/schema/edit-command.schema.json:48-54`,
and the operation's occurrence selector and closed argument reference are at
`:1840-1871`.  The Runtime side has the matching internal method at
`runtime_protocol/timeline_commit_port.py:276-283` and matching projection
regex at `runtime_protocol/timeline_commit_store.py:21`.

Required owner action: Agent keeps the canonical semantic schema/source and
normal command validation proof.  Runtime owns normal official schema/client
generation, artifact digest/version, and coordinated pins; it does not add a
second schema, endpoint, DTO, or acceptance exception.  Until the relevant
artifact checks and coordinated pins are recorded, this is a compatibility
ACK, not new release authorization and not a claim that cross-repository
qualification is complete.

## Remaining concrete handoff

There is no unresolved Runtime data-model shape in P1/P2 or O1–O5.  The only
deliberately held cross-area item is O6: Agent must choose and own an explicit
legacy migration that preserves existing positives/callers before legacy writer
retirement; the Runtime recommendation is to keep them live/held until then.
O7's remaining work is the coordinated Agent semantic source plus Runtime
official generation, artifact digest/version, and pins—not a new Runtime
implementation or release authorization in this response.

No tests were run for this documentation-only response, as requested.
