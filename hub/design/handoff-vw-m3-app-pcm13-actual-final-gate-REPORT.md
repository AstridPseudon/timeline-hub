# Independent D08 review — App public13 continuous-PCM consumer

## Decision

**REJECT for merge / owner-port approval.** The product leaf is directionally
correct and its new lifecycle controls are useful, but the actual commit has
unapproved assertion loss in the migrated AudioTrack tests. Restore the listed
continuous-PCM assertions and re-run the exact App neighbor set before asking
for merge. This is a narrow test-qualification rejection, not a claim that
the PCM implementation is intrinsically incorrect.

Reviewed App ref: `tl/vw-m3-app-pcm13-actual-consumer-unit` at
`2e9939810cbe600d1f7cfcf16d987e50bdecaaeb`, against `b1ef4b9b9`.
Changed paths are exactly the five reported paths: `AudioTrack.tsx`,
`AudioTrack.test.tsx`, `TimelineComposition.media-conformance.test.tsx`,
`continuousPCM.contract.test.tsx`, and `continuousPCM.lifetime.test.tsx`.

## Exact old/new assertion mapping

The old neighbor run was reported as 91 passing tests. The candidate adds 24
direct tests and reports 83 post-migration tests; the worker also recorded 38
AudioTrack and 3 conformance callback-policy failures while converting the
leaf. The lower count is not itself the finding. The finding is that these old
audible assertions have no one-to-one replacement:

| Old assertion | Candidate replacement | Gate result |
| --- | --- | --- |
| `AudioTrack.test.tsx:196-224`: eight-case fade matrix, every frame, including 24/30/60 fps, overlap, fractional fades, trimmed source, and track gain | `:198-209`: one 30-fps bake/constant-gain shape check; exact PCM is covered only by the separate 44.1/48-kHz fixture | **Partial; restore a parametrized PCM matrix** |
| `:227-250`: fixed music fade boundary/duration values at source frames | `:292-301`: occurrence trim/sequence props only; no matching sample/boundary assertions | **Missing** |
| `:253-272`: overlap and seven unsupported fade inputs | `:239-244`: only `{fadeIn: 0.001}` | **Missing six inputs and overlap output** |
| `:275-282`: speed `0`, `-1`, `NaN` sanitization before envelope compilation | No candidate test covers an invalid speed; new tests use positive speed `2` | **Missing rate behavior** |
| `:284-290` and `:391-406`: authored equal-power plus all six curves, with exact audible values | `:265-280`: only `linear`, `equal-power`, `s-curve`, and only native/Blob shape assertions; `exponential-fast`, `exponential-moderate`, and `exponential-slow` are absent | **Missing curve behavior** |
| `:292-303` and `:305-333`: authored envelope precedence and rerendered envelope *and curve* output | `:226-237`: envelope re-bake/fetch count only; no exact precedence or curve-rerender sample assertion | **Partial; restore semantic output assertions** |
| `:373-389`: four nested multiply/minimum boost forms with exact gain and Web Audio admission | `:256-263`: one flat boost | **Missing nested boost matrix** |
| `:410-418`: nested boost remains Web Audio even when another node silences it | No replacement | **Missing** |
| `:435-467`: envelope backend transitions in both directions, equivalent callback identity, request teardown, and readiness holds | `:304-317`: ordinary scalar threshold only; lifetime tests cover stale work but not this transition contract | **Partial; restore transition/readiness assertion** |
| `:469-484`: boosted envelope exact authored-time values across occurrence bounds, trim, speed, and >1 sample | `:292-301` checks native props only; lifetime line 172 checks bytes for a non-boosted shortened window | **Partial; add exact boosted PCM samples** |
| `:501-513`: boosted fade contains below-unity fade frames while preserving Web Audio and readiness | No equivalent exact fade-frame assertion | **Missing** |

The conformance change at `TimelineComposition.media-conformance.test.tsx:169-210`
is an intentional policy conversion: all three fps cases now assert the same
admitted prepared URL, `data-callback` false, and constant track×clip gain.
The other conformance matrices remain present. That change is acceptable only
after the missing AudioTrack audible coverage above is restored.

Native no-envelope behavior, premount, hold/starvation, abort/stale decode,
AudioContext close, Blob revocation, retry/chrome Retry, readiness, ordinary
failure, mute, boost scalar, occurrence trim, prepared positive, four forged
prepared negatives, and export no-browser-decode are covered by the retained
tests/new lifetime suite. I found no `skip`, `xfail`, `only`, `todo`, or positive
conversion to refusal. The product imports public Composition evaluation APIs;
there is no deep import or copied DSP implementation.

## Independent evidence

- Tiny exact Git extraction of the five changed App files: **5 files**, from
  `2e9939810`, with no whole-App copy.
- Private public13 archive SHA256:
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
- Fresh private Vitest run over exact candidate `AudioTrack.test.tsx` and both
  new direct suites: **3 files / 63 passed**, exit 0, 3.38s. It used only the
  read-only App dependency leaves and a reviewer-owned cache.
- Fresh public13 API probe: **PASS** — six public exports, full-source float
  WAV metadata/length, matching prepared positive, wrong envelope, fractional
  origin, wrong child rate, and `blob:` negatives.
- Exact candidate `git diff --check b1ef4b9b9..2e9939810`: **FAIL**, with new
  blank lines at EOF in both `continuousPCM.contract.test.tsx:84` and
  `continuousPCM.lifetime.test.tsx:351`. This must be fixed before merge.
- Producer’s exact-base overlay report records **5 files / 83 passed** and
  targeted lint pass. I treat that as producer evidence, not independent
  rerun evidence; the normal App public13 pin/lock was not adopted.

The conformance neighbor was attempted from the tiny extraction but stopped at
the current shared App integration’s unrelated font/admission fixture boundary
(`DepartureMono-Regular.woff2?url` / virtual admissions). No shared files were
changed. No browser, render, localhost, network, install, typecheck, full
suite, or physical Player/export parity run was performed.

## Required next step

The App owner should add small parametrized continuous-PCM replacements for the
missing invalid-speed, six-curve, overlap/unsupported-input, nested boost and
exact occurrence/export audible assertions; fix the two EOF whitespace errors;
then rerun the exact five-file App lane on the adopted public13 pin/lock. Only
that repaired result can receive owner-port approval. Normal public13 pin/lock,
typecheck, physical parity, and Gate 6 remain pending as already stated.
