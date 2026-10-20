# App PCM13 audible-case restoration

## Result

Restored the rejected continuous-PCM assertions on top of the parent
`tl/vw-m3-app-pcm13-actual-consumer-unit` candidate. This worker changed only
tests: `AudioTrack.test.tsx` and `continuousPCM.lifetime.test.tsx`; the product
leaf, public13 pin/lock, and media-conformance migration were not changed.

The exact private public13 consumer lane passed **5 files / 116 tests**:
`AudioTrack.test.tsx`, `RemotionPreview.audioFailure.test.tsx`,
`TimelineComposition.media-conformance.test.tsx`,
`continuousPCM.contract.test.tsx`, and `continuousPCM.lifetime.test.tsx`.
The lifetime suite alone passed **44/44** after restoration. Targeted ESLint
passed with exit 0. Both `git diff --check b1ef4b9b9` and `git diff --check HEAD`
passed; both new test files now have exactly one final newline.

Restored coverage uses public13 compile/apply/WAV output and constant native
gain for invalid speeds, all six curve modes, overlap multiplication, exact
fade boundaries, envelope precedence/rerenders, nested multiply/minimum boost
forms, the silenced-minimum admission case, occurrence-bounded boosted
samples, backend transitions/readiness, and boosted fade frames below unity.
The complete old unsupported-fade matrix remains on the native path. The
existing public13 admission positive/four forged negatives and continuous-vs-
step-held between-frame mismatch remain intact. The line-by-line mapping is in
the sibling `-mapping` artifact.

## Decisions

- Kept the old unsupported native-input behavior, including `undefined`, `{}`,
  zero/negative/NaN values, string, infinity, tiny fade, and no-fade inputs;
  there was no approved policy change for those cases.
- Used small private decoded PCM fixtures. The old trimmed-source boundary
  values retain their original authored times; a private 3 kHz fixture aligns
  source samples to 30-fps boundaries without changing product behavior.
- Did not add public types, DSP, thresholds, refusal positives, xfails, or
  architectural/store/clock/DTO/root changes.

## Not run / pending

The normal App public13 package/lock adoption remains owner-held, so this is
private overlay qualification only. No browser, render, localhost/socket,
network/install, project typecheck, full suite, or physical Player/export
parity run was performed. Do not infer those gates from this result.

## Files and handoff

The exact commands, mapping, changed-file list, and patch note are the sibling
flat artifacts with this report stem. The harness should commit the worktree
changes with the supplied commit message and then consume the `DONE` marker.
