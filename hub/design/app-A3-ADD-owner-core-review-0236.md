## PASS — A3/P2 review and apply

Applied only the exact two reviewed blobs onto clean `c101477597`:

- `TimelineEditorCore.tsx`: `42a4cf9d0d1b70e38f1616fc5947ddea1c73f908`
- `TimelineEditorCore.test.tsx`: `4ec734c6854627dc5211cff7b9bcd2a3b640eede`

The mounted `ClipAction` callback now passes `marqueeOwner` to the real owner-scoped selection store. Regression covers `f2-occurrence-copy:clip-0`, sibling exclusion, wrong-owner isolation, and stale contrasts via neighbors. No oracle or unrelated files changed.

Checks passed:

- Old source: expected RED, exit 1.
- Fixed Core test: 11/11.
- Mounted controls: 11/11.
- Neighbor suite: 62/62.
- Selector oracle: old RED, exact GREEN, strict negatives GREEN.
- TypeScript: `tsconfig.node.json`, `tsconfig.app.json`, `tsconfig.json`.
- Scoped ESLint `--max-warnings=0`.
- `git diff --check`.
- Protected-six and cumulative two-file diff exact checks.

Limit: this closes the missing post-click owner-state seam, but the historical live-browser ADD3964 reload/Undo journey remains unrerun.

Commit message written and `DONE` created. No commit or merge performed.