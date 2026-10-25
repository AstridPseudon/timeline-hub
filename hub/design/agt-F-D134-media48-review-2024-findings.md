# F/D134 independent source/evidence review

## Verdict

`PASS_FINITE_UNAPPLIED`: the finished D134 packet correctly establishes no D134 production/test-source delta and preserves the finite 48-case authored scope. It does not establish setup, behavior, or whole-cohort credit.

## Confirmed source custody

- Agent `tl/agt-F-D134-media48-2016` resolves to `a30e74e901a28b39c28facba3deb00d76f186e23`, the current Agent `tl/integration` head.
- The assigned test source is SHA-256 `cf73444ebe59c7a5e62f29cff072d3c3dea87ead85043d92ef632d433cb110a1` (blob `c4f54e34536dabbf196fd9a17c337b78394506e3`). It is unchanged in the author commit and current integration.
- The author commit changes only the two unrelated graph-root test files. No D134 test, production source, fixture, generated file, schema, pin, or Runtime file changed.
- The five author evidence files reviewed here match their permanent flatdesign copies byte-for-byte. Private XML and the private experiment patch are not available; they are not reconstructed.

## Corrected caller finding

The author packet’s categorical “no existing registered caller can create the item correspondence” is too broad. The held D100/R1 Agent source at `9486cbb06e2ab53402086772e6c2bc18bc4849fc` explicitly handles the real boundary in `State.shot_item_map` / `_item_ids` / `project_shot_items`: an authenticated un-copied physical shot can receive a unique non-empty item set while preserving the empty `item_id_map`; copied or remapped placements retain exact correspondence checks. That is directly relevant to D134’s first `item-1` refusal.

This does not make D134 applied. The held D100 source is not present on current Agent integration, the D100 Agent behavior lane was not run, and App currentproof1939’s own9 stopped in setup before projection acceptance. Therefore the correct blocker is meaningful current D100 qualification through the existing registered `commitTimeline`/provider route, not a new API or scope decision.

The remaining current-caller facts still hold: `occurrence.create` creates an empty child; `occurrence.add-media` creates media/clip state but not shot-item correspondence; duplicate/fork require an authenticated existing occurrence; local or foreign `occurrence.place-shared` requires an authenticated source; and `timeline.duplicate` requires an authenticated foreign closure. No source closure, seed, fabricated accepted record, mapping repair, or new API was introduced.

## Evidence limits

The author’s targeted command used `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime`, not a qualified immutable `ab1e` checkout receipt. The current shared checkout is now `e319fdbd` (tree `d5cb9335`), so the observed setup refusal is retained as historical source evidence only. It cannot prove current behavior, parent RED, candidate GREEN, or credit for all 48 cases. No unchanged provider/test-body retry was run.
