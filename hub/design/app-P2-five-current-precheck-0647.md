# Report

Read PLAN and current integrated source at `9b810408cc` / tree `9a37265f0286`. No product/test/spec changes made.

| Original NEVER-RUN case | Current selector → caller / owner basis | Expected command, claims, intended fields | POST / evidence / remaining |
|---|---|---|---|---|
| Transition None single | `.clip-action[data-clip-id]` → Effects → `ClipTransitionSection` → `useClipEditing` → `transitionClearBasis` → local handoff. Parent clip ownership; reads original config/registry, clip id/transition, pinned groups. | `doc.patch` removing `parent/clips/id:<id>/transition`; `created: []`; only raw transition key removed. Source emits `merge: fields`, request/step reads, and intent `Clear transitions: <id>`. Reload and guarded Undo restore the exact raw field. | Source reaches POST through outbox → generated client `/commit` with UUID `Idempotency-Key`. Evidence is source plus fake transport only; no mounted witness. **Certain mismatch:** original helper expects `merge: atomic`, no reads, no `created`, and generic intent. Owner: App A2/P2 reconciliation in `three-products.p2-tour.spec.ts:326-359` against `timelineLocalSaveHandoff.ts:478-495,569-577` and `localSaveSession.ts:168-185`. |
| Transition None bulk | Same path; shift-selected parent clips. Basis carries both ids and original parent closure. | Two guarded `doc.patch remove` changes; `created: []`; only each selected transition changes; opaque fields/order preserved. | Same POST/evidence qualification. Same certain helper mismatch as single; reads cover both clip ids plus pinned groups. |
| `registerAsset save` | `.timeline-wrapper` file drop → `useExternalDrop` → `prepareGenerationAsset` → `placePreparedAsset` → prepared-media handoff. Parent output track `V1`, media selection is the owner basis. | `clip.add-media`, `select: parent`, `intent: {}`; created claims `parent/asset:<asset>` and `parent/clip:<clip>` for this new asset/row. Only one parent row plus one registry entry changes. | Outbox semantic append → generated `/commit` + `Idempotency-Key`; media import/upload and selection lookup remain browser-unknown. **Certain mismatch:** original helper expects `atomic`, no reads, and non-empty step patch; current semantic route emits `fields`, no reads, and `patch: []` (`three-products.p2-elements-assets.spec.ts:172-203`, `localSaveSession.ts:176-185`). |
| Automatic child placement | Embedded popup child `.clip-action[data-clip-id]` drag → `ShotTimelinePreview` provider → `sharedPopupMediaCommands` unshared one-add branch. Owner is `occurrence:<id>` with verified shot/internal closure and authenticated media selection. | `occurrence.add-media`, occurrence ownership, created occurrence asset/clip claims; only one V2 child row and child registry entry change; parent/shot revisions remain unchanged. | Source reaches POST through semantic outbox; upload/dispatch/reopen remain unknown. Same certain `atomic`/non-empty-patch helper mismatch as registerAsset. |
| Popup mounted SWAP | Shared selector `.clip-action[data-clip-id="${sharedOccurrenceId}:${TARGET_CLIP_ID}"]` → `Swap selected clip` → file input → `ShotTimelineMediaControls` → shared popup provider. | `[occurrence.fork, occurrence.swap-media]`; fork creates `shot:<fork-id>`, swap creates no ids, and carries authenticated old/new media selections. Only selected occurrence/clip asset changes; sibling and opaque data remain intact. | Source reaches POST with `merge: fields`, one step, empty patch, and generated `Idempotency-Key`; source plus fake transport only. Original reload and guarded Undo expectations align. |

Common transport source: `localSaveSession.ts`, `dataProvider.ts:751-762`, and generated client `generated.ts:202`; successful replies preserve canonical document, digest, id map, records, dependencies/effects, history and receipt keyed by the same idempotency key.

Pinned Agent `079580ca` admits `clip.add-media`, `occurrence.add-media`, `occurrence.swap-media`, and inverse; Runtime `37eb6c` schema admits the same shapes.

Checks:

- `git diff --check` — passed.
- Worktree unchanged and clean.
- Current tree equals reviewed 0629 tree.
- Original P2 spec files are byte-identical to the reviewed tree.
- No tests rerun, per task scope. Existing 0629 evidence remains fake-transport/source evidence, not genuine mounted/browser proof.
- `DONE` marker created; no commit metadata needed.