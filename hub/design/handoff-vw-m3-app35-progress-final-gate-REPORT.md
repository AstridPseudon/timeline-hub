# vw-m3-app35-progress-final-gate

## Decision

**APPROVE exact source for the App owner port:** `tl/vw-m3-app35-pcm-preserve-progress` at `30b8df2895536c471e270faf83ce710acd847065`.

The direct parent is the approved App consumer `35e3ebdf2`, whose parent is the approved public13 pin `2b3c431f`. The candidate delta changes exactly these three allowed files:

- `src/tools/video-editor/compositions/AudioTrack.tsx`
- `src/tools/video-editor/compositions/AudioTrack.test.tsx`
- `src/tools/video-editor/compositions/continuousPCM.lifetime.test.tsx`

No package, lockfile, root, DTO, store, compiler, or public API file changed. The normal public13 pin remains intact: archive SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, 77 archive members, version `0.0.13`; archive and installed-leaf path lists matched.

## Source review

The only product change streams `Response.body` chunks during the existing envelope-preparation fetch, joins those chunks into the same decode buffer, and invokes the existing attempt hold's `onProgress` callback for each chunk. Cleanup clears that callback and the existing abort/cancelled, stale-attempt, decoder-close, Blob URL revoke, retry, native readiness, and `AUDIO_HOLD_LIMIT_MS = 10_000` paths remain unchanged.

The stalled/slow regression passed with four delayed chunks: the same hold renewed while bytes arrived, the fetch count stayed at one, and late playable join remained possible after the bounded hold released. There is no timeout widening, primer, keepalive, mute reset, or additional decoder owner.

The restored lifetime test is byte-identical to approved `70e378e3f`; its mapping covers invalid speeds, all six curves, overlap, unsupported values, nested multiply/minimum boosts, exact boundaries, boosted occurrence timing, transitions, rerenders, the step-held negative, and the boosted below-unity sample. Prepared-source coverage includes the valid record and four forged records.

## Targeted evidence

- Private public13 Vitest source-chunk regression: **1 passed, 43 skipped**.
- Restored lifetime cases only: **26 passed, 18 skipped**.
- Prepared positive/4 forged negatives plus full-source step-held cases: **9 passed, 42 skipped**.
- Restored unsupported-fade matrix: **8 passed**.
- Scoped ESLint over the five review files: **passed**.
- `tsc -p tsconfig.strict-islands.json --noEmit --pretty false`: **passed**.
- Prior exact candidate qualification (from the completed descendant): **5 files / 143 tests passed**; this review did not rerun that full five-file matrix per the brief.

Exact test commands are in the sibling `handoff-vw-m3-app35-progress-final-gate-COMMAND` file.

## Limits

No browser, render, localhost/socket, network/install, full suite, whole-App typecheck, pin-adoption, physical parity, or Player/export parity claim was made. No Composition product files were changed in this review worktree.
