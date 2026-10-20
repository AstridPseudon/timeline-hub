# Viewing Timeline Core — current M4 size census

Refreshed 2026-10-20 from committed blobs at the current `tl/integration`
heads. This measures authored Timeline Read/See/Edit product code in the
settled Viewing boundary; it is not a target-achievement claim. Physical lines
are UTF-8 `splitlines()` counts and nonblank lines use `strip()`.

## Revisions

| repository | `origin/main` baseline | current `tl/integration` |
| --- | --- | --- |
| Composition | `67b8aa3d0d6831d3e3504a340ff583c3da253707` | `4f325f1e14f03a3418f04bd81b3635c810a40cf2` |
| Agent | `a411628f8fd6129f9c58c332019b56769d997384` | `a8a40afd37e5560a14fa5e1a09ace6018596793e` |
| App | `580508eed1bf6ed95caaf476c9d69a4672472a2f` | `8c0e1f799b64e9b6f179018b7dff01479d43c85c` |

Runtime is omitted because its commit/inspection and visual-seam paths belong
to the Runtime-owned census.

## Canonical authored source

The same path boundary and manifest as the prior 206-file census are used for
both snapshots. Counts are files / bytes / physical / nonblank; delta is
current minus baseline.

| owned slice | baseline | current | delta |
| --- | ---: | ---: | ---: |
| Composition `typescript/src/**`, excluding generated registries/curves and timer declaration | 16 / 45,621 / 1,550 / 1,398 | 79 / 190,569 / 4,442 / 4,097 | +63 / +144,948 / +2,892 / +2,699 |
| Agent `timeline_visualize/**`, excluding schemas, stage/docs, fonts, inspector assets | 54 / 1,253,951 / 27,700 / 24,911 | 55 / 1,293,193 / 28,516 / 25,676 | +1 / +39,242 / +816 / +765 |
| Agent explicit render/evaluator adapters and `rendering/elements/**` text | 29 / 375,489 / 11,381 / 10,993 | 20 / 361,897 / 11,026 / 10,662 | −9 / −13,592 / −355 / −331 |
| Agent `onscreen.py`, `scene_answers.py` | 1 / 18,156 / 452 / 375 | 2 / 24,162 / 568 / 470 | +1 / +6,006 / +116 / +95 |
| Agent Remotion host source, excluding adjacent paths and generated/declaration/test files | 11 / 24,264 / 631 / 573 | 10 / 28,084 / 690 / 630 | −1 / +3,820 / +59 / +57 |
| App non-test source in `PreviewPanel/**`, `compositions/**`, `render/**`, excluding fallback | 29 / 282,934 / 7,533 / 6,932 | 31 / 309,641 / 8,018 / 7,402 | +2 / +26,707 / +485 / +470 |
| **Viewing-owned canonical total** | **140 / 2,000,415 / 49,247 / 45,182** | **197 / 2,207,546 / 53,260 / 48,937** | **+57 / +207,131 / +4,013 / +3,755** |

The preceding snapshot used Composition `5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8`,
Agent `d0a5072bbe7b7ce9489f43aa0a81027ec400343b`, and App
`20ea14c26526fe4924354f10a177aebbaf6002bc`: 206 files / 2,203,235 bytes /
53,452 physical / 49,103 nonblank. Since that snapshot, the same manifest
therefore changes by −9 files / +4,311 bytes / −192 physical / −166 nonblank.

## Exact counted changes since the 206-file snapshot

- Agent added `astrid/packs/rendering/actions/timeline_visualize/_filmstrip_cache.py`;
  `astrid/packs/rendering/actions/timeline_visualize/filmstrip_cards.py` was
  refactored around it. The row changes by +12 physical / +13 nonblank lines.
  `astrid/packs/rendering/elements/catalog.ts` is modified with no byte or
  line-count change.
- Agent deleted these nine duplicate Composition wrapper components:
  `astrid/packs/rendering/rendering/elements/animations/{fade-up,fade,scale-in,slide-left,slide-up,type-on}/component.tsx`,
  `astrid/packs/rendering/rendering/elements/effects/text-card/component.tsx`,
  and `astrid/packs/rendering/rendering/elements/transitions/{cross-fade,fade}/component.tsx`.
  The render/evaluator row changes by −27 physical / −18 nonblank lines.
- App deleted `src/tools/video-editor/render/renderPipeline.ts` (−177
  physical / −161 nonblank lines).
- Composition has no counted source-path changes. The App vendored Composition
  copy was already absent from the preceding snapshot and remains excluded;
  App vendored Agent/browser text, tests, generated clients/contract data,
  archives, and untouched infrastructure remain outside the canonical total.

The owner-pending cache extraction is not yet integrated as an approved
ownership/deletion result; this census makes no forecast about it. The
currently committed `_filmstrip_cache.py` helper is counted once in the Agent
`timeline_visualize` row, with no duplicate helper attribution elsewhere.

## Reproduction and boundary

The read-only established manifest is:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-size-census-gate-review-script.mjs
```

It reads only `git ls-tree`/`git show` blobs from
`/home/user/work/{composition,agent,app}`. Reproduce the current path list and
byte/nonblank counts without changing the preserved script with:

```sh
sed \
  -e 's/46bd700b2b46ae1cab1e8a1502ed6504e81aa8d8/4f325f1e14f03a3418f04bd81b3635c810a40cf2/g' \
  -e 's/931d7ec56dadffc2efdc893fec80b4c4aadf8a8e/a8a40afd37e5560a14fa5e1a09ace6018596793e/g' \
  -e 's/18becfbede00038830b97e63345445eeef54fa42/8c0e1f799b64e9b6f179018b7dff01479d43c85c/g' \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-size-census-gate-review-script.mjs \
  | node
```

Use each emitted `paths` array with `git show <sha>:<path>` and Python
`len(blob.splitlines())` for the physical-line column. The boundary remains:
Composition authored `typescript/src/**`; Agent authored visualize files plus
the explicit scene/render/elements/Remotion host paths; and App non-test source
under the three named preview/composition/render roots. Generated data,
tests/fixtures, archives, vendored copies, and unrelated infrastructure are
not silently reattributed or counted.

The PLAN size guide is rough guidance, not a gate; no working feature is cut to
reach it.
