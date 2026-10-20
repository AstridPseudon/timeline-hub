# Long-source/current decoder scope

Base 9fd669e481cf94ee641d9719f3ed7341910c2dcf already contains both reviewed
file-backed >64MiB decode and exact-tick gapless MP3 admission. No helper fix
appears missing. This worker will add only
`remotion/tests/normal-audio-native-sources.test.mjs`, exercising the existing
normal adapter with native full-source MP3 bytes/origin controls and >64MiB PCM.
Existing helper-level long-source tests will also run unchanged.

No Python normal_audio.py, slice transport/phase tests, normal-audio-sources.mjs,
core/provider/route/pins edits. These remain the red-fix/source owners' scope.
No activation, installation, full suite, socket, browser, or other worker write.
Tests use own disposable ORCH project with unchanged released public12 and
read-only existing dependency links; exact module/test copies are checked.
