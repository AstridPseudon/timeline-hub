Fixed the retained ADD27885 label failure with one product expression in [ShotTimelineMediaControls.tsx](/home/user/work/wt/app-A3-ADD27885-selection-sol-0305/src/tools/travel-between-images/components/ShotTimelineMediaControls.tsx:301).

The trace proves pointer click `call@91` selected `f2-occurrence-copy:clip-0`. Its `hold` type makes `canSwap` false, which also suppressed the selected label. SWAP9674’s existing `media` clip passes that condition. The independent Luna report confirms this cause.

The label now uses the resolved owner-scoped selected clip. Swap, duplicate, capture, scheduler and save predicates remain unchanged.

| Predicate | Result |
|---|---|
| ADD pointerdown → pointerup → click → actual selection → exact label | Old source RED; new source GREEN |
| Selected ADD hold | Label visible; Swap and duplicate disabled |
| SWAP media sibling | Own label visible; ADD label absent |
| Wrong owner/occurrence, stale, multiple, empty selection | Fail closed |

The regression mounts the real Dialog, popup, Core, drag handler and selection store. No selection-path mock or direct callback supplies its positive result.

Validation used `/opt/node20/bin/node` (`v20.20.0`):

```bash
node_modules/vitest/vitest.mjs run \
  --config /tmp/w-2d49829e65/vitest.config.ts \
  --configLoader runner --no-cache --maxWorkers=2 \
  src/tools/video-editor/components/TimelineEditor/{TimelineEditorCore,ClipAction}.test.tsx \
  src/tools/video-editor/hooks/useClipDrag.test.tsx \
  src/tools/video-editor/data/shotCompositionProjection.test.ts \
  src/tools/travel-between-images/components/ShotTimelineMediaControls.test.tsx \
  src/tools/travel-between-images/components/ShotTimelinePreview{.test.ts,.integration.test.tsx}
```

**154/154 passed:** original Core 11, mounted controls 11, original neighbors 62, new regression 1, ClipAction 45, drag 24. The exact old source with the final integration file produced **9 passed, 1 failed**, at the missing selected label after selection succeeded.

Also passed:

- `TSX_DISABLE_CACHE=1 /opt/node20/bin/node --import tsx --test tests/e2e/local/support/p2-popup-oracle.test.mjs` — **4/4**.
- Under `flock -w 600 /home/user/work/.app-tsc.lock`: `/opt/node20/bin/node node_modules/typescript/bin/tsc -p <project> --noEmit --incremental false` for `tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json`.
- Scoped ESLint on both changed files with `--max-warnings=0`.
- Playwright `--list --reporter=list`, three-products config, original popup spec, grep `P2 popup mounted ADD on selected child uses shared occurrence fork and A2 commit$` — **exactly one test**.
- `git diff --check` and scope/hash checks.

Blobs:

- Product: `9afbf18c4b2ecd8c357c0ee0caa416575c2c639f` → `2cffede82391d5b73d984c2051f32bd518b94668`
- Integration test: `38e5de7dfd34cb9b1c17ad577280ce433cfabdb0` → `e028902bbfe1e317868297839b9f7593b7e12087`

Protected-six audit: popup spec, projection, CoreBody, ClipAction and TrackListRenderer are byte-identical; the popup control has only the authorized label-expression delta. No oracle correction or permission widening.

Ledger: prior owner fixes remain preserved. This proves the downstream display cause locally; it does **not** close the original browser ADD gate or qualify later history/Undo. Next: independent implementation review, then central original ADD rerun. No full suite, browser, service or Git mutation was run.

`commit-msg` and `DONE` created.