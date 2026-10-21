# Reviewed14 Composition source-delivery handoff

Delivery is intentionally held: `tl/integration` is still
`e7ef7a0729a2d7dad3c0ae60da9e6bb8f844d332`, while the approved source port is
`c1f4c0b5e24742b61090fdb2a47774e2189709db` with tree
`585e8c4784ee78ccbfbff4b6ce26f577b8eda05e`. No stale 0.0.14 patch/bundle or
package archive was emitted.

After the merge, run the worker `COMMAND`. It is fail-closed on the exact
reviewed main `67b8aa3d0d6831d3e3504a340ff583c3da253707`, source commit/tree,
13-path e7 frontier, 109 main-to-source changed paths, and 113 tracked target
paths. It preserves scanner/carrier hashes, creates a small source diff and
bundle, and applies the diff to a private fresh-main archive for exact path,
mode, and byte comparison.

The source frontier includes the independently approved NodeNext `.js`
specifier fixes in `index.ts`, `lib/animation-easing.ts`,
`lib/audio-envelope.ts`, and `theme-api.ts`; the old `3a675f38`/`d2fcf410`
metadata identity is not used. Public13 and source14 package publication
remain unchanged/held.
