# D09a final semantic-retirement review

**REQUEST CHANGES — do not approve `e83aa8253` yet.**

The approved `ef7f39af3` producer files are unchanged, and the consumer cut
correctly keeps the named private fallback plus the deferred crop/statistics
lane. The blocker is in the new public-positive lookup:

- `motion/sheet.py:173-192` now carries a dense semantic frame set while
  `ctx.frames` remains the sparse PNG-card set.
- `layers/builtin.py:478-483` builds `public_states` only from sparse
  `ctx.frames`.
- `layers/builtin.py:493-496` indexes that map for every frame in the
  presenter interval.

A valid sparse-card/dense-semantic motion or cut page can therefore raise
`KeyError` for a frame with no PNG card instead of consuming its source/frame
bound public row or taking the named fallback. The new source-carry test does
not cover this consumer shape.

Required smallest follow-up: make the consumer lookup cover the complete
admitted semantic clock (without expanding PNG capture), and add a focused
sparse-card public-positive regression. Preserve the original default,
partial, null, raw-invalid, mixed, forged, and missing-row fallback controls;
do not delete `mouth_state` or touch the deferred pixel crop/statistics path.

Checks completed: producer equality against `ef7f39af3`, `git diff --check`,
and AST parse all passed. Source worker evidence was `31 passed, 2 skipped`
aggregate/model, `21 passed` source-carry transport, and `1 passed` new join
test; its native lane had 20 missing-`react` setup errors. Reviewer renderer
fallback cases were unqualifiable because Node `v20.19.4` was unavailable;
the two non-renderer controls passed. No broad/full/browser/install/shared
dependency run was performed.

