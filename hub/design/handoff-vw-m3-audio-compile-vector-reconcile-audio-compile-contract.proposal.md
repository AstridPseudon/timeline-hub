# Proposed amendments for Agent domain review

This is a review proposal against `fd82c36c7cd66d1d58aa0250a008245a43e6fbaa:design/audio-compile-contract.md`, not a replacement contract or permission to change product policy. The completed Agent worker publishes a DRAFT. Both original JSON corpora are retained byte-for-byte in this App worktree; the original Viewing five-RED report is untouched.

## Corpus identity

Replace the implication that the reconstructed Agent eleven supersede Viewing's eleven with a reference to `audio-corpus-map.json`. It preserves the exact original vector, actual authored child/occurrence, full output clip from both Agent entrypoints, and a complete Runtime closure/output artifact for every input. Relations describe semantic coverage, never identity. No pair has identical complete authored inputs.

Viewing-only coverage: explicit child .8 at unity occurrence; source hold cap; source trim cap; opaque fixture effects shape. Agent-only coverage: absent child volume at unity; absent child volume at zero gain; child speed 2 alongside occurrence speed 1.5. The combined Viewing fade has related but different separate Agent in/out rows. Source offset differs literally: Viewing 350 and Agent .35. Both values stay in metadata; neither is a source-clock input. Do not convert either corpus's authored input to make them match.

The existing `project_runtime_parent_composition` is authoritative for the exact immutable Runtime parent/shot/internal revision closure. `project_shot_composition` is retained as the original corpus's graph entrypoint, and both outputs are independently compared in full against literal real-output snapshots. Test closure adaptation only reshapes transport/pins, retaining authored occurrence values. It does not calculate gain, duration, trim, speed or fades. Four current App errors remain explicit ordinary RED requirements. App repair waits for Agent domain review/authorization.

## Clock section correction

`source_from` is **not raw child `from`**. For an already compiled clip and resolved fps, use the public11 `computeMediaTrim(compiledClip, fps).trimBefore / fps`. The public helper owns rounding, including the 30000/1001 frame rate. `playback_rate` is the existing public11 `getSanitizedPlaybackRate(compiledClip.speed)`. There is no new clock implementation or inference from status, clip shape or provenance.

Concrete original inputs: `from=.125` gives trimBefore=4 at both 30 and 30000/1001 fps. The clock origin is 4/30 or 4/(30000/1001), respectively, not .125. The original combined fade's `from=.05` gives trimBefore=2 at 30 and 1 at 30000/1001; these distinct origins must reach the prepared-source admission unchanged. Trim remains downstream and speed remains the child's rate. Occurrence offset/speed remain metadata only. Gain remains a separate scalar, already multiplied once by the Agent projector; the downstream consumer applies track volume times compiled clip volume, without multiplying occurrence gain again.

## Curve section correction

Remove the open decision about dropping versus honouring `curve=`. PLAN's 2026-10-20 decision now requires honouring the authored curve through the public `fadeInCurve` / `fadeOutCurve` semantics. Main's historical parser accepts then drops the curve; that evidence explains the intended change and owner-film review requirement, not a reason to keep dropping it. The bounded test uses a separate compiled-input curve control and leaves both original corpora unchanged. This proposal grants no parser/source/compiler product edit.

## Normal export join remains RED

Neither a compiled clip nor a test-supplied admission record proves a trusted normal-route producer. Keep the original `ENVELOPE_UNRENDERED` requirement ordinary RED until the actual normal render producer supplies the exact public envelope identity, frame-rounded source origin and sanitized child rate. No relaxed admission, xfail, invented new refusal, copied DSP, second compiler, new canonical clock or authored `audio.render_source`.

The positive public-boundary controls use a deliberately synthetic HTTP endpoint only to check matching clock/trim/rate/scalar plumbing under SSR. No endpoint is fetched. They do not exercise decoding, PCM gain, normal preparation, browser playback, capture, actual render, codec or physical parity. No preparation repair is authorized by their success.
