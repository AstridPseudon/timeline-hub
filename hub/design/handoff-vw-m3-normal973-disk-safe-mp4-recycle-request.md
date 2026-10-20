# Recycle request: normal973 MP4 qualification

Owner: `vw-m3-native-host-env-bounded-proposal`

The current `/tmp` free-space reading is `11,445,002,240` bytes, above the
unchanged `10,737,418,240`-byte (10 GiB) guard, but the requested normal MP4
run needs safe headroom. Please recycle these owner-created, completed private
host-environment roots, after checking the owner has no active process or
retained evidence reference:

- `/tmp/vw-m3-native-host-env-agent-ruff.NLjoBC` (112 MiB)
- `/tmp/vw-m3-native-host-env-agent.kmTN69` (112 MiB)
- `/tmp/vw-m3-native-host-env-baseline.ncwiWL` (112 MiB)
- `/tmp/vw-m3-native-host-env-candidate.nZo6Do` (112 MiB)

Evidence for ownership/completion: the worker report says its temporary
harness/cache was removed, no Agent source was modified, and no browser/media
render or full suite ran. A process scan at request time found no active
render/test/browser process. Do not recycle the frozen source closure
`/tmp/vw-m3-public13-host-one-root-catalog-stage` (554 MiB); it is the required
retained source staging for this qualification. Do not touch central test
snapshots, raw media, or provenance.
