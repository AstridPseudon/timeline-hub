# Runtime source reply: native parent SWAP old binding

Date: 2026-10-21 UTC  
Scope: source/API answer only; no Runtime, Agent, App, schema, DTO, wire,
clear-policy, or generation changes.

## Answer

For an accepted legacy parent clip, the authoritative owner is the raw
parent target `parent/clip:<raw_clip_id>`. The authoritative old source is
the effective parent registry entry at `registry.assets[clip.asset]`, where
the effective registry is the existing `parent.registry` declaration, or
`parent.config.registry` when that is the only declaration. If both are
present they must be identical; this is the existing
`effective_parent_registry()` rule.

When that entry contains the original managed binding, the existing Runtime
read can recover the old selection with the legacy selector form:

```python
old_media = client.get_project_media_selection(project_id, {
    "asset": clip["asset"],
    "generation_id": old_binding["generationId"],
    "variant_id": old_binding["variantId"],
})
```

The returned value is the exact five-field `MediaSelection`:
`asset`, `generation_id`, `variant_id`, `object_id`, and `catalog_digest`.
The existing output-association selector
`{association_id, object_id, version}` is also valid, but only when those
accepted association fields already exist; they must not be inferred from a
display ID or a gallery lookup.

The new gallery choice is independent:

```python
new_media = client.get_project_media_selection(project_id, new_selector)
verified = [
    client.get_project_verified_media(project_id, old_media),
    client.get_project_verified_media(project_id, new_media),
]
command = capture_parent_swap_media(
    bundle,
    "parent/clip:" + clip["id"],
    old_media,
    new_media,
    verified_media=verified,
)
```

The captured command is exactly:

```json
{
  "op": "clip.swap-media",
  "version": "1",
  "select": "parent/clip:<raw_clip_id>",
  "args": {"old_media": "<old five-field selection>", "media": "<new five-field selection>"},
  "intent": {"ownership": "parent"}
}
```

`old_media` and `media` are closed command arguments. Capture verifies both
selections against the detached Runtime `VerifiedMedia` inputs and preserves
their separate `media.old`/`media.new` dependencies. The swap checks the old
registry binding against `old_media`, creates/checks the new alias from
`media`, and writes only the target clip's `asset`.

Occurrence SWAP is the same closed argument shape but is intentionally
different ownership: `select="occurrence:<occurrence_id>/clip:<raw_id>"`,
`op="occurrence.swap-media"`, and occurrence intent. A popup parent row must
not be converted to that route or selected by a display ID.

## Bounded capability gap

There is no existing nullable/raw-source branch for an old unregistered
parent object. If the accepted parent has only a retained raw `media_id` /
`object_id`, or has no effective registry asset entry, the old selection
cannot be completed honestly. Runtime's existing selection API accepts only
the complete legacy `(asset, generation_id, variant_id)` selector or the
complete `(association_id, object_id, version)` selector; it has no
object-only lookup. The native `_registry(..., create=False)` path then reads
`parent/asset:<clip.asset>` and refuses an absent/mismatched binding. It also
refuses legacy locator/identity codecs rather than interpreting them.

Therefore Main has one bounded capability gap: an accepted legacy parent with
no complete authoritative registry/output binding cannot enter native SWAP.
The original positive remains OPEN. Preserve App's selected-new draft on this
refusal; do not fabricate `generation_id`, `variant_id`, `catalog_digest`, an
association/version, or an owner from UI/display identity.

## Tiny source witness

Reviewed source packet: Runtime final normal target `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
`d3a290b407fa61e6ab2d476f50c068073f70df00`; ordinary Agent contract
`sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`
(55 definitions / 29 operations). The reviewed current-source helper is
`astrid/sdk/timeline/native_occurrence_media_commands.py`, where
`parent_swap_media()` binds `media.owner` to `parent`, `_swap()` calls
`_registry(... old, alias=row['asset'])` before creating/checking the new
binding, and `capture_parent_swap_media()` emits the closed command above.
The source-packet helper digest is
`sha256:6aaa6c167c3dbad0783c095d04868c8a67e88f7f7b698178596160b06e781442`.

The existing Runtime authority is visible in
`runtime_protocol/service.py` (`get_project_media_selection` and
`get_project_verified_media`) and
`runtime_protocol/timeline_commit_port.py` (`MediaReads.selection` and
`selected_media`). The parent registry fallback is
`astrid/core/timeline/parent_registry.py`; absent direct and nested registries
resolve only to an empty `assets` map, not to a raw-object source.

No real HTTP probe was run: the reviewed normal Agent consumer pin was not
available as a current matched pin in this task context, and the brief
requires waiting for that pin. Existing non-HTTP source/acceptance evidence
is not relabeled as HTTP evidence.
