# Explicit asset registration

`Checkout.register_asset(asset_id, entry)` records `timeline.register-asset`
through the normal EditCommand runner. Save the checkout, then publish through
the existing COMMIT route. Multiple registrations inside `checkout.edit(...)`
form one transaction and one undo step.

The equivalent OpCall is:

```json
{
  "op": "timeline.register-asset",
  "select": null,
  "args": {
    "asset_id": "poster",
    "entry": {
      "media_id": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "type": "image/png"
    }
  }
}
```

This assigns the complete entry under the parent registry's `assets` map.
It replaces an existing entry explicitly; it does not merge entry fields.
Opaque fields and explicit nulls are preserved. The recorder captures the
previous entry (or missing container) as a presence-tagged precondition, so a
changed entry conflicts on rebase and inverse restores the original presence.
Registrations do not resolve timing or change `app.astrid.v`.

The entry must identify an existing managed source by `media_id` or `object_id`.
The compiler's SHA-256 identity rules apply; any additional identity/digest
fields must agree. Runtime retains object admission and atomic acceptance
authority. This operation does not acquire media, inspect files, register
file-only assets, or target an occurrence registry. Those unsupported inputs
are refused. Existing snapshot publication adapters retain their legacy path.

An editor adapter may produce this call only from an explicit caller's
registration or entry-assignment intent. A replacement registry snapshot does
not prove which entries the caller intended to assign and must not be converted
into registration calls by diff inference.
