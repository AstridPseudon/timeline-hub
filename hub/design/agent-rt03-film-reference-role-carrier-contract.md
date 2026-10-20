# RT03 film-reference role carrier: bounded Agent contract

Status: semantic answer only, published 2026-10-20 22:32 UTC. No command, DTO,
endpoint, table, generated artifact, or Runtime behavior is changed by this
document.

## Decision

ACK the existing canonical occurrence's `provenance` as the carrier. It is the
narrowest existing scope for a film reference placed on one occurrence. The
binding is versioned under Agent's existing `astrid` namespace:

```json
{
  "provenance": {
    "astrid": {
      "timeline_reference": {
        "version": 1,
        "reference_id": "<opaque stable timeline-reference id>",
        "role": "source",
        "asset": "<existing occurrence-owned asset alias>"
      }
    }
  }
}
```

The exact v1 vocabulary is `version`, `reference_id`, `role`, and `asset`.
`role` is currently the single value `source`: it is the role in the original
strict timeline-reference positive and the existing Main timeline vocabulary
for reference material. It is not a catalog relation (`canonical`,
`used_as_input`, `depicts`, or `inspired_by`), and it is not
`ShotRevisionRecord.assets[*].role` or `generation_inputs[*].role`. Those are
source-input semantics and must remain distinct. A future role needs a new
contract/version; v1 must not silently accept catalog or generation roles.

`reference_id` is the exact stable identity that would be the existing
`timeline_references.id` value. It is not a display name and must not be
resolved by a catalog lookup. `asset` is the existing raw asset alias in the
occurrence's canonical internal-timeline registry. The outer occurrence scope
is part of its identity; conceptually the stable source reference is
`occurrence:<occurrence_id>/asset:<asset>`. Do not store `object_id` or a
second `media_id` in this binding.

## Runtime derivation and guards

For an accepted parent revision, Runtime should derive the projected
`timeline_references.object_id` as follows:

1. Read the exact accepted occurrence and its pinned shot/internal-timeline
   closure, not caller input or a mutable project catalog.
2. Resolve `provenance.astrid.timeline_reference.asset` against that accepted
   internal timeline's existing registry asset entry. Native media commands
   already bind that asset to the exact selected media `object_id`/`media_id`.
3. Normalize the selected media identity using the existing Agent media
   identity rules and require it in the accepted Runtime dependency manifest.
   The guarded `MediaSelection`/dependency custody remains the media source
   authority; the provenance binding only names the existing asset.
4. Project the verified identity and `role: "source"` into the existing
   `timeline_references` row and `timeline_revisions.references_json` snapshot
   in the same canonical acceptance transaction.

If the asset is absent, resolves to more than one identity, or does not match
the accepted manifest/selection custody, reject the canonical acceptance. Do
not guess from a display id, query `project_references`/`media_references`, or
create a duplicate object authority. If the accepted closure cannot expose
the existing asset binding and its manifest membership, the minimal missing
carrier witness is precisely that stable occurrence-scoped `asset` selector
linked to the verified `MediaSelection`; no new DTO, port, table, or endpoint
is justified.

## Preservation requirements

- **Materialization:** keep the binding on the parent occurrence. Agent's
  authoring bundle already deep-copies occurrence provenance and preserves it
  through placement materialization; a shared shot revision must not merge
  delivery/reference state from two placements.
- **Undo/restore:** the binding is already inside the immutable parent
  occurrence and Runtime's retained `provenance_json`; restore/replay must
  restore or remove the derived reference projection with that accepted
  closure, without a second authority.
- **Scope:** use the authenticated project/timeline and exact occurrence
  closure that accepted the command. `reference_id` is timeline-scoped as in
  the existing read model.
- **Identity/idempotency:** an exact retry replays the same derived row;
  changing `role` or `asset` for the same identity is a conflict, and a
  different command may not overwrite an occupied identity with different
  media/role. Do not revive the retired direct flat-film writer.
- **Open requirement:** the original strict positive remains OPEN until an
  executable current native command and Runtime projection demonstrate
  creation, restart retry, changed-payload refusal, different-key refusal,
  and durable `role == "source"`. Catalog-only success is not equivalent.

## Main evidence

- `docs/timeline-editing-guide.md:96-111` names one occurrence's
  `candidate["placements"][i]["provenance"]` as the narrow scope and says
  agent-owned extension data stays namespaced.
- `astrid/core/timeline/astrid_ns.py:1-20` establishes `astrid` as the
  application-owned namespace; `astrid/core/timeline/banodoco_composer.py:130-141`
  defines `role: "source"` as reference material.
- `astrid/sdk/timeline/native_occurrence_media_commands.py:60-104` and
  `native_placement_commands.py:132-142` show the existing exact five-field
  media selection and its registry asset binding; the conformance recipes
  prove the accepted dependency manifest is updated with that selection.
- `astrid/core/timeline/authoring_bundle.py:492-513,778-805` resolves the
  existing asset/media identity and compiles occurrence provenance into the
  accepted parent closure.
- Runtime's current `composition_revision_occurrences.provenance_json` and
  `_normalize_occurrence` preserve opaque occurrence provenance; its retained
  dependency manifest is the immutable media verification boundary.
- Runtime's original strict positive is
  `tests/test_runtime_exact_idempotency.py:81-122`; on current Main it is
  strict `xfail`, so this contract does not claim that behavior is implemented.
