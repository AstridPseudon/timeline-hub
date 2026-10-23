# P1 encoder real-corpus handoff

- App worktree: `/home/user/work/wt/ap2-P1-encoder-real-corpus`
- Base HEAD: `e77f142406ec57f639ba8ad1fbdd7badd5c5651d`
- New file SHA-256: `cb76d90c7228e75638f84439a6539d753b9eeb3dc5d43b35cfd72d27b7eedc88`
- Test: `src/tools/video-editor/commands/p1EncoderCorpus.test.ts`

The production `documentPatchIntent` successfully encoded the real App trim
fixture's authored payload: complete `hold/from/to` changes, exact tagged
before values, explicit `for`/`until` removes, parent physical root binding,
mirror preservation, registry preservation, and no invented IDs. It also ran
on the real Agent split authored output and encoded `list.insert` plus
`created: ["parent/clip:right"]`.

The split→trim dependent leg remains unverified and is deliberately not fake
green. `tests/fixtures/p1-feasibility/cases.json` is still `authored-not-go`:
there is no authored App canonical after-document for trimming the newly
created `right` clip, and no App production split capture/submit caller that
binds the created ID. Mounted save remains pending because
`documentPatchIntent.ts` is currently unsent; its only prior caller is
`documentPatchIntent.test.ts`, plus this corpus test.

Targeted corpus test: PASS (2/2 new tests). Typecheck, ESLint, and diff check:
PASS. Combined required targeted command: 13 passed / 1 failed because the
existing feasibility provenance assertion for `tests/e2e/local/support/harness.ts`
expects `2ba2164…` but the current file hashes to `b243b340…`. No full/browser/
socket/Runtime/H3 execution was run.
