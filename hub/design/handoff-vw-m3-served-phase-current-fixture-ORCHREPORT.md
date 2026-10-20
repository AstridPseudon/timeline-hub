# Served-WAV current-entry phase fixture

Prepared the nine-case unapplied served-WAV fixture requested by the
orchestrator. No repository files changed.

## Change

The seven whole-source cases are carried forward byte-for-byte from the
guard-fix baseline, including native float PCM precision, actual
`InvocationAssetServer.port` checks, forged binding/double-apply rejection,
cleanup, and controller source postflight.

Only the two phase cases changed. Their preparation closure now accepts
keyword arguments, and each case passes the unsliced compiled Root props to
the current inactive producer entry:

```python
prepare(
    props,
    window=FrameWindow(start_frame=15, end_frame=45, fps_rational=(30, 1)),
    tracks=tracks,
)
```

The cases do not supply `original_clips` or rely on authored
`astrid_slice_origin`. They retain the full-source PCM oracle at absolute
float32 tolerance `2**-24`, source clock (`source_from=0.5`, unit playback
rate), clip/track asset binding, scalar gain, registry, served-file
containment, and input immutability assertions. The false app metadata is
only a non-authoritative negative input.

## Frozen artifacts

- `handoff-vw-m3-served-phase-current-fixture-test_normal_audio_served_sources.py`
- `handoff-vw-m3-served-phase-current-fixture-UNAPPLIED-tests.patch`
- `handoff-vw-m3-served-phase-current-fixture-controller.py`
- `handoff-vw-m3-served-phase-current-fixture-guard-regressions.py`
- `handoff-vw-m3-served-phase-current-fixture-READY.md`

Hashes are recorded in `READY.md`:

```text
controller 557a7f0cbc0a7c3136253576cf773c131efdb9073a99e93a4f4bc76576f99abd
fixture    f2a659a9a1fa0068ba4d105fd345c3729643b50705566a0d030b339b4a110736
regressions 2bed196e0930eccddb6824221fba56ece4ef97be3652844fcb48e076b98357bf
patch      77f8974abda095480d3ca460fbd2e5fffa18d6315522d85739c6c90710f1c404
```

## Checks

- `ruff check` on controller, fixture, and pure regressions: **PASS**.
- Pure guard regressions: **4 passed in 0.16s**; no listener/socket.
- Served fixture collection: **9 tests collected**; no fixture execution.
- `git apply --check` on the unapplied patch: **PASS**.
- `git diff --check`: **PASS**; repository worktree remained clean.
- Existing current-module targeted Agent tests, using the already-installed
  approved dependency project and Node 20.19.4: **24 passed in 4.96s**.

An initial direct targeted attempt was not evidence: inherited
`NODE_OPTIONS`/`NODE_PATH` was rejected by the runtime guard, and the retry
without those variables lacked the local Composition package and used Node
22. The successful retry used only the existing approved dependency project
and Node 20.19.4; no install or dependency mutation occurred.

No served fixture execution, listener, browser, socket-backed central run,
full suite, install, grant, or normal-route provenance/activation/parity claim
was made. A future `with-phase` run would prove only the inactive helper
transform; the source-owner Agent service join and normal rendering parity
remain separate.

The exact `redfixORCHREPORT` filename was absent; the matching
`handoff-vw-m3-pcm-producer-red-fix-ORCHREPORT.md` was used as the red-fix
handoff source, alongside the named served guard final-review report.
