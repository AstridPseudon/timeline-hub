# App2 dormant after-anchor approved packet — 0518

Date: 2026-10-21 UTC

## Result

Prepared the reviewed dormant after-anchor missing/null raw-video-hold packet
on the current canonical App integration base. The working diff is exactly the
approved 0514 candidate delta reviewed and APPROVE'd by the 0516 report. It is
not activated and no merge was requested.

The correction allows an absent or explicit-null `hold` only for the dormant
after-anchor raw-video source-window path. Source-window duration remains
derived from `to - from`, placement remains speed-aware, and the raw field is
preserved. Explicit zero, non-video, ordinary append, and replacement-style
positive-hold validation remain strict. Complete command/record assertions,
ordered reads and selections, bindings, created IDs, both mirror writes,
JSON-reload guards, inverse/ABA guards, raw anchor/media/rate/peer guards,
one-to-one conversions, and all existing refusal controls remain present.

## Exact identities

- Canonical base: `hub/tl/integration` =
  `bc6f9dd39c7e5154ddf075cb87b7202cf5702e65`.
- App approved candidate: `91927b3cfc613ef395927e5de04cca51b8a678bc`,
  tree `2c0781c72e3a6d5d5fb2ddc50302c2501d32daff`, parent/base
  `bc6f9dd39c7e5154ddf075cb87b7202cf5702e65`.
- Agent prerequisite/source ACK: `452eceb391408185bfcc0c9e029e271d0ae3a229`,
  tree `18fc7e0b1cde4df1a24637509fa14b2351340c9`.
- Agent prerequisite was already independently APPROVE'd; no Agent files
  were changed here.
- App worktree HEAD remains the canonical base because workers do not commit;
  the harness must assign the final commit/tree.

## Exact final diff

The working diff equals `git diff hub/tl/integration 91927b3cfc613ef395927e5de04cca51b8a678bc`
for the two permitted paths, byte-for-byte:

```text
M  src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts   42 insertions, 17 deletions
M  src/tools/video-editor/commands/parentClipAddCapture.ts             4 insertions,  2 deletions
                                                                     46 insertions, 19 deletions
```

Changed-file SHA-256:

```text
6e036a410faea95f3104e602d19285b904975f85f29f9eb7c6af3d66541411a6  src/tools/video-editor/commands/parentClipAddCapture.ts
9415a4ea8ff89c2fc3fa4348d1657c773f0315cb9a67b9d090d24da6ac82fc03  src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts
```

No other App path changed. `public014`, Provider/session/activation routes,
generated fields, pin/session/afterClipId behavior, and Runtime paths were not
touched. Existing unrelated prepared-media `afterClipId` callers remain
unchanged and are not callers of this dormant after-anchor helper.

## Live callers

Exact non-test, non-helper search for
`captureParentClipAddMediaAfterAnchor`,
`finishParentClipAddMediaAfterAnchor`,
`executeParentClipAddMediaAfterAnchor`, and the dormant path's `afterClipId`
found **zero live external callers**. The only occurrences are the helper's
own declarations/internal aliases and its direct test. No UI, Provider, or
session caller was added.

## Verification

Passed:

```text
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts src/tools/video-editor/commands/parentClipAddCapture.test.ts
  2 files passed, 18 tests passed

./node_modules/.bin/eslint src/tools/video-editor/commands/parentClipAddCapture.ts src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts --max-warnings 0
  passed

git diff --check
  passed

exact candidate comparison against 91927b3cfc613ef395927e5de04cca51b8a678bc
  working diff equals approved candidate diff
```

Retained approved-candidate evidence (not replayed here): the 0514 exact
Agent452 comparison with 6 complete commands/records/bundles and replay plus
4 matched refusals, including absent/null raw-hold, explicit-zero, nonvideo,
and ordinary-birth controls. No full, browser, socket, HTTP/native Door,
generation, pin, install, or broad audit suite was run.

## Merge-forward and decisions

Immediately before packet finalization I ran:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/merge-forward ap2-m2-afteranchor-approved-current-packet-0518 hub/tl/integration
```

It failed before any source conflict because this sandbox's shared Git
metadata is read-only: Git could not create
`/home/user/banodoco/reigh-app/.git/worktrees/ap2-m2-afteranchor-approved-current-packet-0518/ORIG_HEAD.lock`
(`update_ref failed`, rc 128). The worker HEAD already equals the canonical
base, so there was no base delta to compose and no conflict or source drift.
No shared HOME file was edited or overwritten; no Git commit/merge metadata was
created by this worker.

No blocking source issue was found. The packet is ready for the manager's
remote merge request; the worker did not request that merge.
