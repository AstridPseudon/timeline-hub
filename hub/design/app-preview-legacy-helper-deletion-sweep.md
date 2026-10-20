# App preview legacy-helper deletion sweep

Result: no safe in-scope deletion exists on the assigned App tree. The
bounded sweep made no product or test changes.

## Inventory and caller evidence

- `src/tools/video-editor/compositions/compiledAudioSourceClock.ts` is the
  public13 PCM source-clock adapter, not dead support code. Its production
  callers are `AudioTrack.tsx:374` for the rendered clip playback rate and
  `AudioTrack.tsx:441` for the authored source origin. Its direct clock tests
  also cover invalid FPS, trim rounding, and rate sanitation. The public13
  handoff explicitly identifies this helper as the active App consumer seam.
- `src/tools/video-editor/lib/config-utils.ts` still has live compatibility
  consumers: `getSanitizedMediaTrimProps` is called by
  `compositions/VisualClip.tsx:317`; `getSanitizedPlaybackRate` is used by
  `compositions/playerEvaluation.ts:22-23` and `compositions/VisualClip.tsx:316`;
  and `getSanitizedVolume` is used by both `AudioTrack.tsx:373` and
  `VisualClip.tsx:314-315`. Removing these would require changing a live
  renderer/player path, which this task forbids.
- The prior private audio-fade module (`lib/audioFade.ts` and its test) is
  already deleted in the current history by the canonical public-envelope
  migration. The prior private trim formula is also already replaced by the
  public `computeMediaTrim` compatibility re-export and recorded as D08
  deleted in the inventory.
- No App adapter path contains an unreferenced preview audio/gain/clock
  helper. The unrelated `lib/editor-utils.ts:setTrackVolume` has only its
  own unit-test caller, but it is not a Timeline preview helper and deleting
  it would remove its only behavior assertion without an approved public
  equivalent; it was intentionally left unchanged.

## Scope decisions

No Viewing-owned live renderer/player policy, public SDK export, fallback,
DSP copy, or D10 source-owned wrapper was edited. The old frame-step baseline
remains truthful and untouched.

## Checks

- `git status --short`: clean before and after the sweep.
- `git diff --check`: pass (no product diff).
- No targeted behavior suite or lint run: no source/test path changed. No
  full suite, typecheck, build, install, browser, socket, or shared dependency
  write was performed.

Remaining blocker for a future broader deletion is the live `VisualClip` /
`playerEvaluation` caller set above; removing those helpers would need an
explicit owner-approved public-equivalent migration outside this bounded task.
