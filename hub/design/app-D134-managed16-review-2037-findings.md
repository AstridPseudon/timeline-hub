# D134 managed16 protected source review

## Verdict

FAIL for the whole WIP source migration; disposition UNAPPLIED. No source adoption or product-defect claim is made.

## Findings

1. `tests/editing_conformance/test_recipe_occurrence_media.py:113-120` copies the original parent payload, stores its occurrences, then removes the `occurrences` key before calling `emit_document_commands`. The original registered fixture author at `tests/editing_conformance/test_commit_runtime_occurrence_media.py:69-72` explicitly replaces that field with `occurrences=[]`. This is not exact input conservation: absent and an explicit empty managed collection are different authored shapes. The emitter/patch path cannot use a top-level parent occurrence membership edit as a substitute; the authoritative guard is `astrid/sdk/timeline/_doc_patch.py:359-367`.

2. `tests/editing_conformance/test_recipe_occurrence_media.py:131-140` constructs a post-birth target containing the original shot payload, including `items[0].item_id == 'item-1'`, then asks `emit_document_commands` to derive a patch from the semantic-born empty shot. The semantic birth at `astrid/sdk/timeline/native_occurrence_create.py:41-45` creates `payload.items=[]`. The registered shot projection checks the authenticated item map at `astrid/sdk/timeline/_command_state.py:353-369` and applies that check for authored shot payload/item paths at `:626-631`; the corresponding item-bearing write therefore refuses changed correspondence. The emitter is a lossless adapter and does not add a semantic item-creation operation (`astrid/sdk/timeline/emitter.py:245-304`).

3. The helper's later `occurrence_patch` (`test_recipe_occurrence_media.py:141-152`) can preserve the authored occurrence fields only after the unsupported shot/internal baseline exists. It cannot repair the missing managed shot item or make the prior setup accepted. The final equality assertion at `:159-171` is a postcondition, not evidence that the route is supported.

4. `test_recipe_m2_shared_auto_placement.py:17-20,39-48` monkeypatches the runtime fixture caller, and `test_recipe_m2_shot_pool.py:57,125-128` imports/calls the helper directly. These are the actual registered Runtime `commit_timeline` setup callers for the shared-auto and pool cohorts. All 16 protected expansions route through `_create_managed_fixture`; none has an independent faithful seam.

5. The C0 v2 request shape is mostly present in `test_recipe_occurrence_media.py:89-111` (base revision/publication, commands, label, steps, merge, reads, dry_run, source, rationale, group_id, and external Idempotency-Key). That shape does not grant authority to change managed membership. `media.admit` at `:122-125` supplies verified media authority, but it has no shot-item creation semantics. No trust seed, authored-value rewrite, assertion weakening, skip, xfail, or refused-route retry was accepted.

## Preserved source evidence

- All three original `inputs()`/test function bodies are conserved; the 16-node expansion is unchanged: shared auto 4 replay cases + 2 provider cases; shot pool 3 replay cases + add/remove provider + 2 promotion cases + 1 pooled round trip; occurrence media 1 same-alias case + 2 provider operations.
- Original assertion AST counts are 71, 59, and 43 respectively for the shared-auto, shot-pool, and occurrence-media files.
- The original `inputs` body is AST-identical. The original authored fixture contains `item-1`, its exact media identity/metadata, explicit parent occurrence rows, internal clips, opaque fields, exact verified selections, and the original inverse/no-write/refusal predicates.
- Only the three authorized files differ from base; no product, Runtime, shared fixture, schema, pin, generated file, or other cohort file changed.

## Finite next step

Keep this partition UNAPPLIED unless Runtime/Agent exposes a registered semantic command that creates/restores the authored shot item with its exact item identity, media identity, opaque metadata, and verified closure history. Do not replace the item with a guessed allocation or use a doc.patch workaround.
