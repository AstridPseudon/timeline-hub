## Result

**PASS — causal classification: harness/spec source mismatch, not a product projection defect.** The retained browser case still fails because it queries the wrong rendered ID.

- Real seed child: `f2-agent-clip` in `tests/e2e/local/support/harness.ts:791-797`.
- Shared popup occurrence: `f2-occurrence-copy` in `tests/e2e/local/three-products.p2-popup.spec.ts:261-291`.
- Popup projection selects that occurrence and calls the production projector: `ShotTimelinePreview.tsx:83-125`.
- Production identity mapping prefixes the occurrence: `shotCompositionProjection.ts:336-348`, producing `f2-occurrence-copy:f2-agent-clip`.
- Timeline rows preserve that ID: `timeline-data.ts:243-258`; `ClipAction` emits it as `data-clip-id`: `ClipAction.tsx:572-581`.
- Retained ADD/SWAP selectors incorrectly use raw `f2-agent-clip`: `three-products.p2-popup.spec.ts:813,821`.

The genuine offline projection reproduced the scoped ID and canonical `clipRef` using the real production projector; no DOM stub or alias was used. Raw aliasing or waiving the retained-raw collision guard remains invalid (`shotTimelineDataProvider.ts:157-176`, `serialize.ts:59-107`).

A genuine scoped target can preserve the existing raw field, authority, occurrence fork, selection, history, and undo assertions: selection captures `ownerRef`/`clipRef` (`ShotTimelineMediaControls.tsx:40-72`), and the provider maps the scoped identity back to the raw child. Browser/backend end-to-end confirmation remains unverified.

## Checks

Reused author 0352 evidence on unchanged source:

- Vitest: 4 files, 70 passed.
- TypeScript root/app/node configs: passed.
- Scoped ESLint: passed.
- `git diff --check`: passed.
- Independent offline projector reproduction: 1 passed.
- Worktree clean; popup spec blob matches retained source exactly.

The 0349 branch has no committed candidate beyond `f90e708b37`; no source overlay was inspected or applied.

## Smallest next action

P2 harness owner should adjust only the target lookup at `three-products.p2-popup.spec.ts:813,821` to use the rendered scoped identity (or an equivalent stable rendered-identity selector), while retaining raw `TARGET_CLIP_ID` for command and document assertions. No product-source change is proven necessary.