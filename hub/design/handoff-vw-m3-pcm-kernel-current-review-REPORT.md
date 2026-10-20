# APPROVE — inactive PCM kernel producer only

Candidate: `e2ad59584addc892f1a6dd9fd644c75f80a2e28f` (harness merge of
`b85eb0573b733d51f7b7aa695763d3960dee5553`). Current integration base:
`df2739f903edac02bd36b4446deeea847524c040`.

The exact approved ten-path delta is present and limited to the inactive
producer/helper unit and its tests. No defect found for this bounded merge.
No production import/call to `normal_audio` or its JS helpers exists, and no
`saveScene`/`saveSceneDependency` dependency exists. Current Root/scene/M2
files, public12 ownership/fixtures, package pin/lock, and historical old-archive
state remain unchanged; no old archive was added or re-adopted. The ten product/test paths are byte-identical to the approved
`ab935f77378ba5ea1df55ba775654f8bba233ebc` and `2019d7e69ceb9b10f18cc311e570d635b16c15d8`
sources.

## Evidence

- Python targeted baseline: `tests/packs/rendering/test_normal_audio_sources.py tests/packs/rendering/test_normal_audio_source_phase.py tests/editing_conformance/test_compile_contracts.py` → **51 passed, 2 existing xfailed**.
- Python service-window/segment baseline: `tests/core/rendering/test_service.py -k 'window_timeline or segment_request'` → **5 passed, 100 deselected**. Aggregate requested baseline: **56 passed, 2 existing xfailed**.
- Native Node direct suites on the private real package scope: `normal-audio-sources.test.mjs` → **8 passed**; `normal-audio-native-sources.test.mjs` → **5 passed**; `gapless-mp3-source-origin.test.mjs` → **4 passed**; `TIMELINE_HEAVY=1 long-audio-source.test.mjs` → **2 passed**. Aggregate: **19 passed, 0 skipped/failed**.
- Native evidence includes full stereo WAV/envelope/phase/gain/mute/trim/rational-rate/source-error/cleanup cases, gapless MP3 origin characterization, and the 8,388,609-frame / 67,108,872-byte file-backed decode. No production encoder, MP4, render, parity, or adoption claim is made.
- Public12 archive: SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`; **77 regular members**, all private extracted member bytes match after tests. Compiled export probe passed for eight public exports, peer identity (React/DOM 18.3.1; Remotion/media/layout-utils 4.0.509), `TimelineComposition`, and exact current Agent `BUILTIN_DEFAULT_THEME` equality.
- Quality checks: Ruff passed for the three Python paths; Node syntax checks passed for all seven changed JS paths; `git diff --check` passed; review worktree is clean.

## Scope and limitations

The producer is intentionally inactive: `_execute_remotion_locked` does not
call it. These tests qualify the real native inactive kernel and its local
materialization/cleanup seam, not source-owner admission, transformed/original
compiled-source transport, served HTTP lifetime, normal-route activation,
actual encoder output, MP4, Player/export parity, or public12 adoption. The
two existing compiler-vector xfails remain unchanged. No full suite, browser,
socket, network, install, or git mutation ran.

Ready for owner merge of this inactive-only unit.
