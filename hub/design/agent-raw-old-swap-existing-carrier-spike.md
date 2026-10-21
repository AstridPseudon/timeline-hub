# Agent raw OLD swap: existing-carrier spike

Status: source proposal plus boundary-fake unit spike only. The frozen v1
schema, operation registry, Runtime, App, CLI, and generated artifacts are
unchanged. This is not a Runtime-positive qualification or an adoption/freeze
request.

## Finding

The App handoff is real and locally present:

- `reigh-app/src/tools/video-editor/hooks/useStaleVariants.ts:163-185`
  (`applyVariantToAsset`) updates one registry key's `file` and `variantId`.
- `reigh-app/src/tools/video-editor/commands/media.ts:244-270`
  (`buildSwapMediaCommandEffect`) changes one clip and writes the supplied
  registry entry, but it has no authoritative OLD media selection.
- `reigh-app/src/tools/video-editor/types/index.ts:584-614` permits a registry
  entry with project-owned `media_id`/`file` and optional `generationId` and
  `variantId`; it does not make a legitimate Runtime five-field selection.

The current Agent occurrence recipe instead requires both `old_media` and
`media` to be `MediaSelection` (the exact five fields) in
`astrid/sdk/timeline/native_occurrence_media_commands.py:149-165`, via
`_media_inputs._verified`. The same limitation applies to the proposed parent
swap shape in candidate commit `7afcd2dab`: it reuses the occurrence recipe
and still calls `_verified` for OLD. Filling OLD's generation/variant/catalog
from the registry would be forbidden adoption; fabricating latest values or
using caller duration is not a substitute.

## Smallest closed successor proposal (not registered)

Keep the existing operation family and its v1 semantics. After peer ACK, add a
private versioned successor (suggested `version: "2"`; exact public spelling is
still subject to the Agent/Runtime pair review) with this closed payload:

```json
{
  "schema_version": 1,
  "op": "clip.swap-media",
  "version": "2",
  "select": "parent/clip:raw-1",
  "args": {
    "old_media": {
      "owner": "parent",
      "clip_id": "raw-1",
      "alias": "old-key",
      "media": {
        "media_id": "sha256:<64 lowercase hex>",
        "content_digest": "sha256:<same digest>"
      }
    },
    "media": {
      "asset": "new-key",
      "generation_id": "generation-new",
      "variant_id": "variant-new",
      "object_id": "sha256:<64 lowercase hex>",
      "catalog_digest": "sha256:<64 lowercase hex>"
    }
  },
  "intent": {"ownership": "parent"}
}
```

The exact naming above is a proposal, not a schema edit. The `select` plus
`owner`/`clip_id`/`alias` is deliberately redundant: it makes the raw owner,
raw clip, and old registry alias explicit and rejects display IDs. The recorder
must capture the scoped `collection.clips` membership/order and exactly these
affected members: target raw clip, old alias binding, and new alias binding.
There is no alias-wide fanout and no inferred owner from display IDs. An
occurrence variant has the same envelope with
`select: "occurrence:<raw-id>/clip:<raw-id>"` and
`intent.ownership: "occurrence"`; its affected members remain that occurrence
only.

The outer existing commit request supplies the original
`base_revision_id`/`base_publication_id`; it is not replaced by a caller field.
The recorder also emits the normal exact `expect` guard for the OLD clip row,
the OLD alias entry, target membership/order, and any NEW alias already
present. A changed original base, row, membership/order, or old binding
refuses before mutation.

Execution is closed as follows:

1. Runtime checks the declared OLD `MediaManifestEntry` through the existing
   private, request-scoped `raw_media_info(pin)` carrier from Runtime source
   `f53bf588bf70b090ce8e0bed5ccb7d91157771b6` / tree
   `d82f37052847949e77c12e1704c3f27c6dd56a46`. The existing BASE-only
   `media_info` and `selected_media` reads stay unchanged. No caller metadata,
   latest lookup, managed-generation fabrication, or caller duration is used.
2. Runtime verifies the NEW exact five-field `MediaSelection` through the
   existing `selected_media` path. The new alias is created from that result,
   or an existing alias must equal the exact derived registry binding; a
   conflicting occupied alias refuses.
3. The old registry entry must equal the supplied manifest pin. Preserve the
   authored source window and validate it against Runtime-returned intrinsic
   info where available; do not rewrite timing or infer a duration. The only
   authored write is the selected raw clip's asset alias, plus a scoped NEW
   registry creation when absent.
4. Recorded reads/selections/bindings and normal guarded inverse machinery
   cover reload, exact inverse, rebase, and A→B→A refusal. A later use of the
   created alias is a surviving dependent, not a reason to fan out or prune
   aliases.

This reuses the existing `MediaManifestEntry` only for the OLD project-owned
raw binding and retains the existing exact five-field carrier for NEW. It does
not make an unplaced/raw object a generation selection, and it does not add a
registry mutation authority to CLI or raw input.

## Executable boundary spike

`tests/sdk/test_raw_old_swap_existing_carrier_spike.py` is test-only and uses
small fakes for `raw_media_info` and `selected_media`. It proves:

- a raw OLD manifest plus exact NEW five-field selection swaps one explicit
  parent clip, preserves a sibling and the OLD alias, and creates/requires the
  NEW binding;
- the occurrence variant is scoped to one occurrence and cannot create a
  parent alias;
- display-ID/owner ambiguity, incomplete affected-member scope, and attempted
  sibling/global fanout refuse atomically;
- caller-supplied OLD metadata and a changed original base are ignored/refused;
- inverse refuses an equal-state A→B→A after an intervening write epoch.

The fake is intentionally not an actual Runtime positive: it cannot prove
Runtime custody, request declaration membership, CAS identity, acceptance
revalidation, or App persistence. Those require a peer-ACKed Agent/Runtime
successor pair and must remain unclaimed here.

## Existing positive-test map

The successor should preserve and extend, rather than rewrite, these current
Main controls:

- `tests/editing_conformance/test_recipe_occurrence_media.py::test_exact_capture_replay_scoped_birth_and_inverse`
  — occurrence swap/add timing, scope, replay and inverse;
- `::test_asset_address_alias_overlap_and_guarded_dependency` and
  `::test_disjoint_edit_rebases_but_same_value_asset_write_blocks_undo` —
  alias dependency and guarded rebase/undo;
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_exact_capture_acceptance_inverse_redo_restart_and_retry`
  — real selected-media acceptance lifecycle (the future raw-old lane must add
  a separate Runtime-positive after peer ACK);
- `tests/editing_conformance/test_occurrence_media_manifest_inverse.py` —
  manifest preservation, later dependents, ABA, and scoped inverse;
- `tests/test_timeline_clip_replacement.py::test_remote_parent_media_replacement_publishes_exact_closure_once`
  — historical parent replacement intent/closure control. Candidate parent
  native positives are in `7afcd2dab`'s `test_recipe_parent_media.py` and
  `test_commit_runtime_parent_media.py`; they are not evidence for this raw
  OLD carrier until the new pair is qualified.

No UI was invented: the inspected App paths above are the existing handoff.
No full, browser, network, model, generation, pin, or live Runtime suite was
run for this source-only spike.
