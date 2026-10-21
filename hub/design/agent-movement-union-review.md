# APPROVE SOURCE — 3b3208 movement union

Reviewed commit `3b3208c43903b770010de0649691cfa566447822` (tree
`84120e176540fbc2281dcff4b7186ec8ae413274`) against its a191 base
`a19192ea789a209260da46bfbdd5b616fc7cc4ac`, using the settled Timeline plan
and the prior free-multi/parent-afterClip source reviews.

## Verdict

**APPROVE SOURCE.** This is a source-only Agent union. No generation, freeze,
pin, activation, App, Runtime, or product-caller qualification is implied.

## Findings

- The free-multi implementation remains the reviewed a191 implementation. The
  union's only changes relative to a191 are the narrow `_recording.py`,
  `commands.py`, parent-media source, and focused parent-media-test hunks;
  `_move_set.py`, its fixture/tests, and the command schema are not rewritten.
  The recording change reuses the already-captured `collection.clips.after`
  selection and its original order. The command change exposes prior records
  only to distinguish the explicit assembled-replacement sequence from a
  standalone after-anchor birth.

- The command schema is byte-identical to a191: raw SHA-256
  `f44b00983b2d5e8c3f137985baabb8b226fe00e821fed74e66444fa3fbdd3a69`;
  canonical formatted floor SHA-256
  `ba0c42d6a9359c32d89d8088416f7bc9092481dbd05f236e4d7e6e019c9246e7`;
  60 definitions, 34 operation clauses, and 12 explicit v2 clauses. Removing
  only `clip.move-set` reconstructs the exact `84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5`
  floor (59 definitions, 33 clauses, 12 v2 clauses).

- Parent after-clip capture requires the raw `parent/clip:<id>` anchor. It
  resolves that raw entity, records its collection membership/order, track,
  source asset, parent output FPS, and exact source row, with no display-ID,
  occurrence, lane-end, or mutable-catalog fallback. The verified media and
  reserved asset/clip identities remain exact and guarded.

- The destination is a deep clone of the raw anchor. Only the reserved clip
  identity, selected asset, effect identity, and authored start codecs are
  changed. Requested foreign row fields are not merged into the clone;
  `_clip` rejects alternate asset identities, timing maps/source aliases, and
  unsupported identity codecs. Peer rows are read as whole rows but only their
  `at`/`at_ms` fields are written. The source/peer timing guards validate
  `at`/`at_ms`, hold/source window, and positive speed through the canonical
  duration path, and the parent FPS is validated and recorded before writes.
  Thus there is no whole-row or foreign opaque-field rewrite. The only whole
  collection-looking write is the existing derived `config.clips` mirror,
  rebuilt from the already-authored parent rows to keep the two mirrors equal.

- The inserted start is `anchor start + max(0.05, clip_timeline_duration(anchor))`.
  Later rows after the anchor on the same track receive exactly that raw-span
  ripple; other tracks, occurrences, placements, and shots are untouched.
  `Recording.create(..., after=...)` inserts immediately after the captured
  anchor and preserves the captured order. Exact retry/created-ID, inverse,
  changed-anchor/order/peer, source/media, and rate guards are retained. The
  preceding `timeline.assembled-target` sequence remains the explicit
  non-ripple replacement exception.

- There is no unintended live caller for the new `after=` capture argument.
  Production callers continue to invoke `capture_clip_add_media` without it;
  the after-anchor path is exercised only by the focused conformance tests in
  this source tree. No App or Runtime consumer was changed or activated.

## Evidence

Reused the movement-union handoff evidence: the parent-media plus free-multi
targeted cohort passed **171 tests**, and the schema/current-union/timing cohort
passed **121 tests**. The preceding independent a191 review also verified the
equal-state forward ABA correction, changed-membership/source/identity/rate
guards, both rational FPS spellings, exact schema/floor hashes, and no weakened
passing expectations. Current source checks: `git diff --check` passed; the
schema has no diff from a191. No additional test run was needed for a concrete
doubt, and no full/live/browser/external suite was run.

## Boundaries

No blocker or source change request. Runtime's existing visual-seam rational-FPS
consumer mismatch remains the separately reported Runtime qualification item;
it is outside this Agent source review.
