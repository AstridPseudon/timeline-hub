# Report — A3/P2

Implemented the minimum product fix in `src/tools/video-editor/components/TimelineEditor/TimelineEditorCore.tsx:502`.

Cause: direct clip selection omitted `marqueeOwner`, while popup controls read the owner-scoped selection store. The retained trace showed the projected action `f2-occurrence-copy:clip-0` selected in DOM, but no selected-label text and disabled Swap. The exact occurrence-qualified identity was correct; no oracle correction was made.

Change:

```ts
userSelectTimelineClip(clipId, { additive: false }, marqueeOwner);
```

Predicate map:

- Old: action selected, exact selected label absent — RED.
- New source route: direct selection uses the mounted editor owner.
- Canonical IDs, projected IDs, parent wrappers, reload, history, Undo, wrong occurrence/sibling/stale negatives remain unchanged.

Tests:

- Core + mounted controls Vitest: 21/21 passed.
- Neighbor Vitest suite: 62/62 passed.
- Selector oracle: passed; old selector RED, exact selector GREEN, strict negatives preserved.
- Node20 `tsconfig.node.json`, `tsconfig.app.json`, `tsconfig.json`: passed.
- Scoped ESLint `--max-warnings=0`: passed.
- `git diff --check`: passed.

Protected files were unchanged. Authorized product blob: `42a4cf9d0d1b70e38f1616fc5947ddea1c73f908`.

Limit: the live browser ADD run was not rerun per task restrictions, so post-fix live GREEN and later history/Undo remain unverified. Next step is the central original ADD rerun after independent review.

Ledger: prior 0056/0106 owner-scoped control fix and selector review remain preserved; the retained ADD3964 run failed first at the exact selected-label predicate, and this task traced and corrected the missing owner handoff without changing the protected oracle or later assertions.

Commit message and `DONE` marker created.