# Native occurrence text bindings

Source: `design/m2-text-binding-contract.md` in the orchestrator directory, adopted against Agent base `ba5f2756f50a84f570aa9699ef621873f7521abc` and Runtime `8609333456b9537339ee1a5dfc7ffd9609242de8`. Runtime's existing implementation is authoritative for CAS selection: `runtime_protocol/timeline_commit.py:RuntimeCommitPort.text_selection`, `timeline_commit_port.py:verify_text_object` / `RequestCommitPort.text_selection`, and `timeline_commit_store.py:_project_text_bindings` / `_project_text_binding`.

`astrid/sdk/timeline/native_text_binding.py` registers this closed command through the existing registry and Document/Media dependency recipe:

```json
{
  "schema_version": 1,
  "op": "text-binding.set",
  "version": "1",
  "select": "occurrence:occurrence-1",
  "intent": {"ownership": "occurrence"},
  "args": {
    "binding": {"kind": "voiceover_script", "slot": null},
    "text": {
      "object_id": "sha256:<64 lowercase hex digits>",
      "digest": "sha256:<same digest>",
      "size": 0,
      "media_type": "text/plain; charset=utf-8"
    }
  }
}
```

Exactly one of `text` and `clear: true` is required. Kind is `prompt`, `voiceover_script`, or `transcript`; only prompt accepts a non-null slot, matching `[a-z][a-z0-9-]{0,63}`. Size is 0..1,048,576 UTF-8 bytes. The MIME contains a space after the semicolon: this is Runtime's exact existing P1 spelling, not a normalized alias. Object ID equals digest. Runtime checks project-managed custody, actual hash/size/MIME, strict UTF-8, and re-verifies at atomic acceptance. Empty bytes have their real SHA-256 and remain a present zero-byte row. Clear removes the row; clear of an absent key refuses.

The stable row ref is `occurrence:<id>/text-binding:<kind>[:<slot>]`. The command records occurrence and source-shot identity, exact tagged prior row, keyed write (including same-value writes), and an exact `media` dependency keyed `text:<digest>`. Provider input capture calls the existing `port.text_selection`; detached capture requires its complete `{object_id,digest,size,media_type,utf8:true}` result. No inline content, Document config facade, new endpoint, table, or projection event is introduced.

Occurrence ownership is explicit and exclusive for this slice. The recorded `text-binding.owners` query compares source shot identities, so separately materialized authoring aliases cannot conceal a shared source. Shared sources refuse. New authored rows contain `kind, slot, media_id, content_hash, byte_size, mime_type`; rebind preserves unknown fields but strips Runtime projection fields and legacy cached `text`. Existing complete descriptors with a cached inline copy remain readable as descriptors; rows carrying only inline text refuse. Unrelated rows and payloads remain exact. Live `binding_id`, `head`, stream and timestamps come from Runtime. Inverse restores the complete retained prior row, including legacy fields, without reading a mutable latest binding.

Order remains authored. Rebind replaces a row in place. Clear records the full guarded collection order, and inverse reinstalls the original position. Birth appends and records `collection.text-bindings.append` using the existing `include-concurrent` policy: replay permits only additions after the original ordered prefix. The public command retains its original claims while the authoritative accepted record captures the actual rebased input order. Disjoint births and disjoint existing-key rebinds can rebase; changed original membership/order or a changed target guard refuses. Missing versus empty collections retain tagged presence through inverse. Undo checks intervening writes, including unchanged writes and A→B→A, and resolves whole-payload aliases against the source owner. Redo uses accepted history/boundaries.

## Private Runtime pairing; public successor still required

Agent ACK for Runtime's exact clear representation is granted in the orchestrator's
`design/agent-text-binding-clear-ack.md` (2026-10-20 10:58 UTC). The existing binding
stream remains a retention anchor. Existing created/rebound events carry hash-covered
present/absent state; omitted legacy state means present. Empty UTF-8 stays present.

Private acceptance uses Runtime S2 base `2c4ac18` plus the approved clear unit
`bfec49af4e2bcb82ae2beed922dda99a977b7d72`. Its complete S2 schema is extended only
with the native text operation and reference definitions, preserving the complete
legacy and S2 reference branches. Runtime's normal Python/TypeScript/schema and
conformance generators and artifact manifest generation/checks run on that private
candidate. This is neither an in-memory schema override nor a published tuple;
public pins remain unchanged.

The three original strict clear positives now pass against that real RuntimeService
and the restored committed main-API film/CAS backup: first-birth inverse restores
absence; empty-text clear/inverse restores the descriptor at its original list
position; V1 remains retained through V2, clear, restart and grouped inverse.
Tests also assert GET/list absence, exact retry, historical shot payloads, event
presence transitions and store integrity. They no longer carry expected failures.

Exact retained legacy MIME remains blocked in Runtime. Agent's inverse already
loads accepted history/boundaries and restores the entire recorded row verbatim;
unit tests prove legacy `text/plain`, cached text, opaque fields and position for
both clear and rebind. Newly selected text still requires canonical
`text/plain; charset=utf-8`. Runtime `_project_text_binding` instead calls the same
`verify_text_object` new-selection validator for all after descriptors, and even
for the retained current descriptor when clearing. The original legacy rebind
inverse positive and an added legacy clear/inverse positive remain strict xfails
for that exact error. Their failed attempts preserve the entire SQLite state and
retained CAS bytes. Runtime needs a bounded distinction between new selection and
authenticated retained descriptor verification, preserving scope/hash/size/UTF-8
and exact recorded MIME; arbitrary MIME admission or normalization is not a fix.
No Runtime product code is changed by this Agent worker.

Reproduction, private candidate source/generation inventory and exact test commands
are outside the repository under orchestrator worker
`agt-m2-text-clear-retained-pair/notes/report.md`. Old writers and App cutover stay
held. No public generated-client release, full suite, browser/socket/App journey,
legacy restoration completion or writer retirement is claimed.
