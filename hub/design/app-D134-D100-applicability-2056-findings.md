# D134 finite D100 applicability correction

## Verdict

`PASS_FINITE_D100_APPLICABLE_UNAPPLIED` for exactly 30 original managed-edge
selectors. The earlier categorical conclusion that no existing caller could
reach the authored item-birth correspondence was too broad. The held D100
source at `9486cbb…`, with qualified source state `42040a9…`, directly covers
that first physical boundary through the existing registered `doc.patch` path.

This is a source-applicability correction only. It is not D134 behavior credit,
current setup acceptance, all-tail proof, retirement, REG/core, ship, or source
home/publication credit.

## Exact finite scope

The 30 selectors are conserved as:

- video unplace: 4 (`image/video × keep false/true`);
- completion auto-placement: 6 (`image/video × anchor/absent` replay plus the
  two provider selectors);
- placement create/unplace: 4 (two replay selectors plus two provider
  selectors);
- shared auto-placement: 6 (four replay cases plus two provider selectors);
- shot pool: 7 (three replay cases, add/remove provider, two pooled promotion
  cases, and the provider promotion/keep round trip);
- occurrence media: 3 (same-alias whole-payload and provider add/swap).

The exact selector list, source-file SHA-256 values, selector AST hashes,
common `inputs()` hash, and assertion counts are in `predicate-map.json` and
`source-manifest.json`. The six source files are byte-identical to Agent base
`a30e74e901a28b39c28facba3deb00d76f186e23`; no source delta was introduced.

## Source comparison

All 30 routes share the same first setup boundary:

1. `test_commit_runtime_occurrence_media.py:_create_fixture:21-115` starts from
   the empty bootstrap, explicitly patches parent membership to `[]`, runs
   registered `occurrence.create`, and then restores the authored internal and
   shot payloads.
2. `native_occurrence_create.py:41-50` creates the semantic-born shot with
   `items: []`.
3. The authored shot patch contains the original `item-1`, media identity,
   opaque metadata, internal link, and exact managed source fields.
4. The parent occurrence is patched as an existing semantic row, so its
   provider-managed edges remain the same; this is not the WIP16 helper’s
   removal of the explicit `occurrences=[]` shape.

The current guard rejects the item correspondence at
`_command_state.py:341-369,371-390,626-637`, and generic closure membership or
edge changes remain guarded by `_doc_patch.py:359-376,450-456`. The held D100
change in `shot_item_map`, `_item_ids`, and `project_shot_items`
(`42040a9…:_command_state.py:341-420`) adds the precise physical-source branch:

- require the same shot ID, shot revision, shot digest, internal timeline ID,
  internal revision, internal digest, and empty `item_id_map`;
- allow unique, non-empty physical item IDs on that unchanged, un-copied
  source, without extending the alias map;
- preserve strict item correspondence for copied/remapped placements.

That is the same first boundary reached by all six cohorts. Later operations
are downstream: media/placement/pool commands do not allocate the shot item.
No cohort has a distinct unsupported first route or a separately missing record
shown by this source pass.

## Caller and contract applicability

The source uses the existing registered operations in `commands.py:29-115` and
the existing commit engine. The setup request shapes contain the C0 fields
(`api_version`, scope/base pair, commands, label, steps, merge, reads, source,
rationale/group where used, and external idempotency key) in the cited source
locations recorded in `predicate-map.json`. The mounted App route is already
documented as durable persistence → `RuntimeDataProvider` save methods →
`client.commitTimeline`; the Agent source registers the provider through the
existing Runtime path. No API or product-author decision was added.

The existing D100 source-security review and product27 review are reused as
source evidence. The current joined original9 remains pending and was not
rerun. Therefore D100 applicability changes the source dependency wording to
“requires the existing meaningful D100 qualification plus faithful current
setup review”; it does not make D134 applied.

## Preserved predicates and boundaries

The original inputs, authored topology, item/media identities, opaque values,
timing/source windows, sibling ownership, pins, request reads, inverse/replay,
no-write, conflict, refusal, reload, retry, and provider predicates remain
unchanged. Cohort-specific predicate inventories are recorded in the map.

The managed14 author/reviewer evidence assessed only original normal `a30e`,
not held D100. The managed16 WIP `6c5c…` was input-changed/invalid and rejected
by review2037; it has no final PASS. First return2050 restored exact `a30e`
blobs and all 173 assertion ASTs, and the WIP remains unmerged. Those facts are
preserved as provenance, not replaced by this derivative.

No behavior, setup, or all-tail result is claimed. No source, product, test,
fixture, shared seed, schema, generated file, pin, Runtime, App, Git ref, or
hub file was changed.
