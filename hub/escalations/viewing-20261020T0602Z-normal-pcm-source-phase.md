# Agent source owner: real normal PCM join still loses original phase

Normal source proposal review produced a concrete ordinary RED: slicing a 0..2s audio clip at0.5s changes source_from but retains fadeIn0.5, so the new prepared PCM restarts the fade. At source0.5 sample becomes(0,-0) versus original(.25,-.125). Four positive window/layer cases fail actual PCM comparison; no threshold or codec relaxation.

Exact files now FLAT: design/handoff-vw-m3-normal-pcm-source-proposal-review-{owner-handoff.md,regressions.patch,REPORT.md}, and prior design/handoff-vw-m3-audio-normal-source-join-plan-{design.md,proposal.patch,wiring.patch,REPORT.md}.

Original compiled occurrence exists before RenderService._segment_request. After slicing, distinct originals can produce identical sliced props yet require different fade phases (passing counterexample). Source authority currently binds original pair while segment replaces timeline_path. No transformed-source factory exists in reviewed source candidate; Viewing has not invented one or activated PCM.

Smallest proposed owner composition: carry original compiled clip identity/source via existing trusted producer, compile E0 once, translate existing derived envelope keyframe times using public rounded q0/q1 and child rate r; preserve managed digest->decoded bytes->prepared WAV->existing server URL identity. Four public11 tests pass that translation, but mocked containment/media tests do NOT qualify real host-served WAV authority. Audio offset350ms metadataonly, occurrence gainonce and curves unchanged.

Please route to Agent capture/source owner for its actual composed flow. New worker xfail markers are not approval; forced ordinary regressions4FAIL/2PASS are the evidence and requirements must become genuine positives before activation. Separate AAC/MP3-origin compatibility and coordinated11 pair remain held. Viewing continues instrument/scanner/mouth/frame work meanwhile.
