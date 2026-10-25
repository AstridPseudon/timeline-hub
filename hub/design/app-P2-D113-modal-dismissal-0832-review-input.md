# P2 D113 review input

## Authorized scope

The manager INBOX D113 decision at `INBOX.md:11579` approves one protected-original UI-step correction. The exact change is in `tests/e2e/local/three-products.p2-elements-assets.spec.ts` after the two existing placement reload-row assertions and before the existing parent Undo gesture:

```ts
await reloadedDialog.getByRole('button', { name: 'Close', exact: true }).click();
await expect(reloadedDialog).toHaveCount(0);
```

The first line mirrors the passing ADD19078 control at `tests/e2e/local/three-products.p2-popup.spec.ts:896`; the second explicitly proves that the same dialog is gone before the unchanged parent Undo at `three-products.p2-elements-assets.spec.ts:1265` (after the two added lines).

## D69 upstream comparison

Frozen App upstream `3881e9440688f774878e18806da2dc5c993a9b00` is the D69 reference. Its `src/shared/components/ui/overlay/dialog.tsx:70-73` uses `useOverlayBridge({ type: 'dialog', modal: true })`, and its `src/tools/video-editor/components/AstridTimelineEditor.tsx:616-661` mounts the embedded canonical editor in that Dialog and clears `canonicalShotEditor` when `onOpenChange` closes it. The current files are byte-identical to those frozen sources:

- `dialog.tsx`: frozen/current SHA-256 `78eb0cfe3e3c511279d4d0ce7f0435037dd530b94f2163ac337ab4856c79fa60`
- `AstridTimelineEditor.tsx`: frozen/current SHA-256 `bea86bb573dd76dad202e373c151bf95cb3821b077a6356b66c85f24c4ec869b`

The retained Sol0819 facts show the parent Undo remains enabled but under an `aria-hidden` ancestor while this modal is open, so its role locator never resolves and no click dispatch occurs. The exact source comparison shows this inert-background modal behavior is upstream, not an App regression. No product change or test workaround is justified.

## Protected-source and predicate map

The target is exactly base plus the two lines above. Removing those two lines restores the target byte-for-byte to base. The only changed file is the target; there are no deletions. The other five protected specs are unchanged byte-for-byte.

Existing target predicates remain in place: media-import and media-selection waits; authored file/geometry input; exact semantic request, base, owner, selection, row and media fields; accepted reply and receipt identity; canonical closure, registry and manifest preservation; history and zero-legacy assertions; post-commit occurrence-scoped reload assertions; unchanged v2 `timeline.inverse` request and parent Undo; canonical restoration, history, guarded Undo, and final reload assertions. The placement-only `14` fixture setup, default-12 neighbors, all existing waits/timeouts, locators, and product sources are unchanged.

The source-only map is not browser or inverse credit. D113's next proof remains the authorized full P2 tour.

## Checks

- Focused Node controls: `node --test tests/e2e/local/support/p2-elements-assets-receipt.test.mjs tests/e2e/local/support/p2-placement-receipt.test.mjs` — 139 passed.
- App TypeScript: `flock -w 180 /home/user/work/.app-tsc.lock node_modules/typescript/bin/tsc --noEmit -p tsconfig.app.json` — PASS.
- Node TypeScript: `flock -w 180 /home/user/work/.app-tsc.lock node_modules/typescript/bin/tsc --noEmit -p tsconfig.node.json` — PASS.
- Scoped ESLint: `node_modules/.bin/eslint tests/e2e/local/three-products.p2-elements-assets.spec.ts --max-warnings 0` — PASS.
- `git diff --check` — PASS.
- Full protected-hash/predicate map — PASS: one target file, two insertions, no deletions, target restores to base after removing additions, five neighbors unchanged, all named existing predicate anchors present.
- No browser, service, original/body, full suite, build, install, or live inverse run was performed.
