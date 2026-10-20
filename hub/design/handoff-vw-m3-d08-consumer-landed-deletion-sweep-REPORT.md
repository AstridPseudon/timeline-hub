# D08 consumer-landed deletion sweep — Agent hold

No bounded deletion is eligible on current Agent.

The smallest active duplicate timing adapter is `remotion/compiled-audio-source-clock.mjs`. Its remaining real production caller is `remotion/normal-audio-sources.mjs:6,26,29`, which feeds the Agent normal render PCM preparation. The Agent tree still pins Composition `0.0.12` (`remotion/package.json:18`; lock `:10,423-425`), so the normal13 Agent pin04f prerequisite is not present. App public13 landing does not migrate this caller.

The existing public-equivalent tests remain named and unchanged: `remotion/tests/normal-audio-sources.test.mjs`, `remotion/tests/normal-audio-native-sources.test.mjs`, `remotion/tests/gapless-mp3-source-origin.test.mjs`, `remotion/tests/long-audio-source.test.mjs`, and the Agent neighbor `tests/packs/rendering/test_normal_audio_run.py` all still import `compiledAudioSourceClock` directly. Deleting it now would remove live behavior, so no code/test/ledger edit was made. Keep pixel verification and `_timing_evaluators`.

Focused evidence: the direct-preparation guard passed 2 tests; all three adapter modules passed `node --check`. The broader normal-run file collected 2 passing tests and 33 fixture errors because this isolated worktree lacks `ASTRID_REMOTION_PROJECT_DIR`; this is an environment limitation, not a deletion qualification.
