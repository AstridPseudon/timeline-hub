# Opaque item-reference remap contract

When an authoring candidate copies a shot revision for a new placement, every
shot item gets a new identity. The remap rewrites only the item references the
shot codec owns. Everything else in the payload is opaque data and must come
out byte-for-byte as it went in.

- Source of truth: `astrid/core/timeline/authoring_bundle.py::_remap_known_item_references`
- Shared fixture: `tests/editing_conformance/fixtures/opaque_remap.json` (schema `opaque-remap/v1`)
- Python consumers: `tests/timeline/test_opaque_remap_fixture.py` (every case) and
  `tests/timeline/test_authoring_bundle.py` (end-to-end, uses the fixture's `opaque` block).
- App consumer: App's TS `remapItems` in `authoringBundle.ts` loads the same fixture file via hub-sync.

## Inputs

- `payload`: a shot revision payload. Only `payload.items` is visited.
- `item_ids`: a map from source item id to remapped item id. It is applied once. Remapped
  values are never re-remapped, and ids absent from the map are left unchanged.

## Allowed fields (the complete list)

For each element `item` of `payload.items`:

1. **Identity.** `item.item_id` and `item.id`. The identity is `item.item_id` when present,
   otherwise `item.id`. A field is rewritten only if its current value equals that identity.
   So `item_id` and `id` are remapped together when they are equal mirrors. If `id` differs
   from `item_id`, it is opaque and stays as it is.
2. **Dependency links.** `source_item_id` and `source_item` on the descriptor. The descriptor
   is `item.metadata` when that value is a mapping, otherwise `item` itself. A link is
   rewritten only when its value is a string.

No other key, at any depth, is an identity or link. This includes `metadata` as a whole,
`data`, `app`, `opaque`, `provenance`, `selected_variants`, `generation_inputs`, `pools`,
`audio_bindings`, `text_bindings`, `selected_item_id`, `parent_item_id`, `foreign_item_id`,
`foreign_item_ids`, any key ending in `_item_id`, nested lists, and every namespaced key
such as `org.example.notes/v1`. Anything outside `payload.items` is never visited.

## Byte-for-byte rule

Everything outside the allowed fields must match the input exactly. "Exactly" means the
canonical JSON text, not Python `==`. Canonical JSON is `json.dumps(value, sort_keys=True,
separators=(",", ":"), ensure_ascii=False)`, which is the same encoder as `_canonical_json`.
So the JSON number `0` stays `0` and the JSON number `0.0` stays `0.0`. A cross-language
implementation must preserve the integer/float distinction. `JSON.parse` on its own does
not, so compare the canonical text, not parsed values.

The input payload is never mutated.

## Fixture format

```json
{
  "schema": "opaque-remap/v1",
  "opaque": { "org.example.notes/v1": { } },
  "cases": [
    { "name": "...", "item_ids": { }, "payload": { }, "expected": { } }
  ]
}
```

- `opaque` is the reusable unknown-namespace block for end-to-end tests.
- Each case is a pure input/output pair. `expected` is written by hand, not generated from
  the function. A case passes when `canonical(remap(payload, item_ids)) == canonical(expected)`.
- To change behaviour, change the fixture and the function in the same commit, and say
  which allowed field changed.
