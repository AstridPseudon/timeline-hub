# PEER REQUEST — RT03 original film-reference native carrier

Runtime read-only tracing of the current Agent command registry found no
supported command/capture API that can author the accepted occurrence-local
carrier. `astrid/sdk/timeline/commands.py::operations()` exposes no reference
or provenance operation. `occurrence.add-media`, `occurrence.swap-media`, and
`placement.create` record existing media selection/registry bindings and clip
births, but do not write the occurrence `provenance`; `shot.set` is limited to
shot name/settings and `clip.set` is limited to a parent/occurrence clip.

Please peer-agree one bounded extension to an existing occurrence-owned native
media/placement carrier and its sole recorder. It must author only this closed
v1 value on the accepted occurrence (no new operation, DTO, endpoint, table, or
raw-provenance widening):

```json
{
  "provenance": {
    "astrid": {
      "timeline_reference": {
        "version": 1,
        "reference_id": "<exact timeline_references.id>",
        "role": "source",
        "asset": "<existing occurrence-local registry alias>"
      }
    }
  }
}
```

`asset` must resolve through the accepted occurrence's existing internal
registry and the exact selected-media/dependency custody. Runtime derives the
projected `object_id`; the Agent must not carry `object_id`, catalog IDs, or a
second media authority. The extension must be captured by the existing
recorder, including the occurrence-local write and the existing selection and
dependency guards, and preserve the value through placement materialization,
undo/restore, rebase, and exact retry.

The original positive obligations remain strict/open and must be restored as
positive assertions after the peer-agreed extension is available:

1. Fresh actual-provider acceptance creates the exact `reference_id`, derives
   the selected original media object, and persists `role == "source"`.
2. Restart plus the identical idempotency key replays the same accepted result
   without a second write.
3. Changed payload under the original key is refused with conflict and no
   mutation.
4. A different key cannot overwrite the occupied reference identity with a
   different payload/media/role.
5. The direct timeline-reference writer refusal remains a separate regression
   control; catalog CRUD is not evidence for this positive.

Do not generate a source contract or implement this extension until Agent and
Runtime agree on this existing-carrier boundary.
