# App PCM13 restored D08 gate

## Decision

**APPROVE SOURCE/TEST repair for the App owner’s `actual13` port only.** The
repaired branch is `tl/vw-m3-app-pcm13-preserve-audible-cases` at
`70e378e3f`, atop rejected `2e9939810`. This does not approve the normal App
13 pin/lock, release, typecheck, browser, render, or physical Player/export
parity gates; those remain owner-held/pending.

## Independent checks

- `AudioTrack.tsx` is byte-identical between `2e9939810` and `70e378e3f`:
  SHA-256 `8d881bad20dcccf50d28ce4c0eb85cc1555af71628f3d4c20f385a2fdd9250cc`;
  `cmp` passed.
- The repair delta is only the three intended test files: 6 additions/3
  deletions in `AudioTrack.test.tsx`, removal of two trailing blank lines in
  `continuousPCM.contract.test.tsx`, and 248 additions/3 deletions in
  `continuousPCM.lifetime.test.tsx`. The parent’s product leaf and existing
  media-conformance policy migration are unchanged by this repair.
- `git diff --check b1ef4b9b9..tl/vw-m3-app-pcm13-preserve-audible-cases` and
  `git diff --check 2e9939810cbe600d1f7cfcf16d987e50bdecaaeb..tl/vw-m3-app-pcm13-preserve-audible-cases` both passed, including new files.
- The exact prior-worker five-file public13 overlay report is 116/116, with
  lifetime 44/44 and targeted lint passing. The required old-to-new mapping is
  explicit for invalid speeds, all six curves, overlap plus unsupported native
  fades, nested multiply/minimum and silenced minimum, exact boundaries,
  boosted occurrence samples, transitions/rerenders, and the retained native
  lifecycle. No old valid positive was converted to a refusal; the four
  refusal cases are forged negatives. No `skip`, `xfail`, `only`, or `todo`
  appears in the final exact test paths.
- The existing one-policy proposal is legitimate: Composition exports the
  public envelope compiler/apply/WAV/admission API, and its source-time
  `applyAudioEnvelope`/float-WAV contract is the policy documented in
  `app-preview-audio-seam.md`. The App product leaf calls those public APIs;
  it contains no copied DSP and no frame-volume callback implementation.

## Focused reruns

Using a private six-file App overlay, immutable public13 package leaf, shared
dependencies read-only, and a cache under the private overlay:

```text
/home/user/work/app/node_modules/.bin/vitest run --no-cache --configLoader=runner --maxWorkers=1 --config /tmp/vw-m3-app-pcm13-restored-final-gate-review.1x6a9c/.pcm13-review.config.mjs --testNamePattern='keeps unsupported fade values|sanitizes invalid authored speed|applies the public continuous PCM envelope|preserves exact authored fade boundaries|multiplies overlapping fade ramps|preserves continuous PCM for the retained fade matrix|uses an authored public envelope before legacy fades|transitions between native and prepared envelope sources|keeps boosted fade frames below unity|applies nested|retains Web Audio admission for a nested boost|keeps boosted PCM samples in authored time' src/tools/video-editor/compositions/AudioTrack.test.tsx src/tools/video-editor/compositions/continuousPCM.lifetime.test.tsx
# PASS: 2 files, 34 passed, 56 intentionally unselected; exit 0

/home/user/work/app/node_modules/.bin/vitest run --no-cache --configLoader=runner --maxWorkers=1 --config /tmp/vw-m3-app-pcm13-restored-final-gate-review.1x6a9c/.pcm13-review.config.mjs --testNamePattern='keeps the public full-source PCM/WAV positive exact|plays a matching prepared positive|refuses (wrong envelope|raw fractional origin|wrong child rate|non-attempt URL)' src/tools/video-editor/compositions/continuousPCM.contract.test.tsx
# PASS: 1 file, 6 passed; exit 0
```

The first command intentionally did not run the full matrix. The prior
116/116 five-file overlay and 44/44 lifetime result remain producer evidence;
this run independently reran only the restored groups requested by D08 plus
the valid-positive/four-forged admission group.

## Limits and next step

No normal App 13 manifest/lock adoption, release qualification, project
typecheck, browser/socket test, render, full suite, or physical parity was run
or claimed. The App owner should byte-verify and adopt the approved public13
pin/lock, then rerun the exact five-file lane on that actual13 cohort before
release or Gate 6 claims.
