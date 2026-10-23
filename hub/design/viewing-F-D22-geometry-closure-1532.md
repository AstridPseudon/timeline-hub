# F-D22/V3 geometry closure

**PASS — corrected source-attribution packet is closed.**

## Exact diff

`diff -u` between `viewing-F-D22-geometry-cause-1520.md` and
`viewing-F-D22-geometry-cause-return-1530.md` has exactly one content hunk:
the Composition citation changes from `TimelineComposition.tsx:569-603` to
`TimelineComposition.tsx:232-262, 258-260, 278-280`. No other content differs.

## Hash and live source verification

- Corrected report hash:
  `abbe4d10a8ce6bb65d6290da7750fcf2ae7fa5cf`.
- `git show 635f4de06:typescript/src/TimelineComposition.tsx | nl -ba`
  verifies preparation at lines `232-262`, capability preparation at
  `258-260`, and the `querySceneFrame` call at `278-280`.
- The verified source blob is
  `076163d3d049397e04abc547ba480e193700c9f6`.
- `git diff --check`: PASS.
- `git status --porcelain`: clean.

## Limits

This is a citation/source-attribution closure only. Prior independent source,
math, and production-caller evidence is reused; no substantive review or
tests were rerun. No Composition fix is identified. This does not claim a
behavior, rendering, parity, product, test, or full-suite PASS, and does not
approve a merge. H9 V4, D14, and D23 remain unchanged. The retained full v2
request/reply contract and caller trace remain unchanged. The preserved
`819acf...` approved artifact and legacy `21fde...` hash failure are not
reopened here.
