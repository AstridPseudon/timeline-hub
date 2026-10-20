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

## Runtime pairing still required

1. **Frozen schema**: unchanged integration Runtime rejects the generated `text-binding` guard with `invalid_prepared`, before acceptance. The manager must compose this additive operation and ref patterns into its current full superset (including S2/future operations), then use normal contract/client generation. This worker does not publish a partial public freeze.
2. **Removal**: `_project_text_binding` rejects every absent after-state with `text_binding_clear_unsupported`. Strict positive tests retain first-birth undo, explicit EMPTY clear/undo, and V1→V2→clear→restart→group inverse. Runtime owner must resolve removal using its existing binding tables/events. EMPTY is never used as clear.
3. **Actual retained main MIME**: the committed main-API film backup has a transcript object/descriptor with `mime_type: text/plain`. A new native rebind succeeds, but inverse of that rebind fails in `verify_text_object`, which requires `text/plain; charset=utf-8`. Its positive exact-inverse test is a separate strict xfail, scoped to that specific validation error. The descriptor is not rewritten or normalized. Runtime owner must reconcile old exact retained descriptors with P1 validation before old writers can be retired.

Qualification uses the real `RuntimeService` and restored committed main-API film/CAS backup (`timeline_commit_film_fixture.build_film_fixture`), never direct SQL writes or a fake prepared provider. The worker-private `runtime-schema-overlay` copies integration Runtime behavior unchanged and adds only this schema clause/definitions using Runtime's normal `timeline_commit_resources.render`; only the generated runtime schema bundle differs in `runtime_protocol`. It proves the prospective schema pair, not unchanged integration Runtime. The reproducible generator and commands are in the worker directory and `notes/report.md`.

Old writers remain. No full suite, socket/browser suite, App journey, shared-source authoring, public generated-client release, or qualified removal is claimed here.
