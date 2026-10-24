## Report

Result: all five original never-run gestures are **LIVE (source-proven)**. No dead-scope/deferred case was found; no D52 cut applies. Retain all eight P2 originals.

| Gesture / original test | Current production caller → outbox → POST | Effects / reload / undo |
|---|---|---|
| Transition None single — `three-products.p2-tour.spec.ts:722` | Transition selector → `ClipTransitionSection` → `PropertiesPanelBody` → `useClipEditing` transition basis → local save session → generated `/timelines/:id/commit` POST with `Idempotency-Key`. | `doc.patch` removes only `parent/clips/id:<id>/transition`; guarded inverse restores it. |
| Transition None bulk — `three-products.p2-tour.spec.ts:742` | Same mounted path through bulk `handleUpdateClipsDeep`. | Two guarded transition removals; opaque/order data preserved; reload and inverse restore both. |
| `registerAsset` save — `three-products.p2-elements-assets.spec.ts:468` | Timeline file drop → `useExternalDrop` → `prepareGenerationAsset`/registry path → `applyEdit` → outbox → semantic `clip.add-media` POST. | Adds one parent row and registry asset; reload shows it; inverse removes both. |
| Automatic child placement — `three-products.p2-elements-assets.spec.ts:526` | Embedded shot file input → `ShotTimelineMediaControls` → `addClip` → popup provider’s unshared branch → `occurrence.add-media` POST. | Adds one occurrence child/asset only; parent and sibling closure remain unchanged; reload and inverse verified by test assertions. |
| Popup mounted SWAP — `three-products.p2-popup.spec.ts:823` | Selected child → `ShotTimelineMediaControls` → `addClip(replaceClipId)` → shared popup command builder → `[occurrence.fork, occurrence.swap-media]` POST. | Forks ownership, swaps authenticated old/new media, preserves siblings/opaque data; reload and guarded undo are asserted. |

The complete C0 request/reply funnel remains intact: base IDs, commands, labels, steps, patches/reads, merge mode, source/rationale/group metadata, dry-run, idempotency key, `{data, receipt}`, canonical document/digest/id map, authoritative steps/dependencies, merge/accepted IDs, durable receipt, conflict head, invalid code/path/hint, and dry-run handling.

`trackReorderCapture` and `parentAfterAnchorCapture` are dormant: current production census found only their test imports. Neither is the sole behavior for any of these five gestures.

Evidence reused from exact current-tree qualification `d6ed8cbda122d810d5836ebfce3c56c10e76e9b4` / tree `542b772e6deed676b917f857708445b7d37a5aa8`:

- Pure1036: 695/695 tests, popup 67/67, controls 30/30, diagnostics 11/11; all three TypeScript configs and scoped lint passed.
- Strict oracle integrations: HOME `182c65242d` and tour/D50 HOME `28b0f11e1c`.
- No browser/live-runtime/original journey was rerun, so this is source/control evidence rather than live-tested credit.

Checks run:

- `git diff --check` — passed.
- `git diff --quiet` — passed.
- Worktree status — clean; no product/test/config changes.

Required commit message and `DONE` marker created.