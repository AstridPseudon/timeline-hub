**Verdict: APPROVE the narrow plain-original-extent fix only.** No blocking defect found in frozen producer `61f1a420f1f355ee0d16ffb0dbeb617b83b1b044` (tree `2e1c782c0cf02316193905292d578ec00ec0497d`) against `abd41eb2a6a8fe9224028018ac65225018e490bd`. The producer completed with harness exit **0**, DONE, and a recycled worktree before final testing. This does **not** approve the whole inherited candidate or release integration/adoption holds.

The exact delta has five files: service, normal runner, Root, a new Python extent test file, and additions to the existing normal-audio tests (356 insertions / 6 deletions). No producer or repository files were edited by this review. The separate Root regression patch was applied only to private archives, byte-for-byte; its tests are absent from the producer commit.

**Source findings and reproduced behavior**

- `service.py:1072–1109` removes caller reserved request metadata before any early return, measures `Timeline.from_json_data(...).for_render().to_json_data()` with the existing duration helper **before** layer filtering, checks the original window end, then writes its own decimal extent. Source-role reference clips do not contribute. Authored duration metadata cannot enlarge the bound. Original selected clips, absolute window, alpha and materialized-input hashing remain.
- The runner parses a strictly positive decimal safe integer, rejects oversized/malformed/boolean/fractional values, and requires a native isolated-layer window. Support and locked execution use the same helper and canonical FPS. Original FPS equality, source-range/unit-speed checks and full-bound guard remain; the retained extent must cover local clips and the window. Both execution staging branches and protocol dispatch forward the same extent. Direct full/unlayered overrides and conflicting legacy/tail clocks refuse. This remains an internal invocation fact, not a source certificate or new authorization protocol.
- Both actual Root composition metadata callbacks honor 300/600-frame original extents for otherwise identical empty/sparse layers, including rational FPS. Absent override keeps empty=1, ordinary clip duration and legacy window=30. Invalid, unsafe, smaller and conflicting overrides refuse. Default/explicit canvas and existing full render-tail duration cases pass. Root tests transpile actual Root and stub React/Remotion/package imports; they prove callback behavior, not browser rendering or public-package parity.
- Actual socket-free normal locked execution prepares native stereo PCM and retains the extent prop through preparation. Existing source trim/rate, submillisecond placement, scalar clip/track gains, mute=0 and full native-source WAV assertions pass. Attempt WAVs and props clean up on success, failure, cancellation and timeout. Existing default, selected-PNG, Three.js and non-window legacy boundary tests pass.
- No Runtime DTO, auth protocol, authored extent stamp, second compiler or duration-helper change. Serializer, normal PCM helper and tail implementation bytes remain unchanged from `abd41eb2`; hashes are recorded.

**Independent test results**

| Command / lane | Base | Frozen candidate |
|---|---:|---:|
| Same independent Python service→native-window probe: empty/sparse × original300/600, window [150,180) | 4 failed, exit1; full-composition bound refusal | 4 passed, exit0 |
| Exact separate Root patch, direct Node node:test execution | 4 passed / 3 failed, exit1 | 7 passed, exit0 |
| Supplemental actual Root callbacks: 300/600, rational FPS, boolean refusal | 2 failed, exit1 | 2 passed, exit0 |
| Five targeted repository Python files | — | 127 passed, exit0, 13.90s |
| Service neighbors `-k 'window_timeline or segment_request'` | — | 5 passed / 47 deselected, exit0 |
| `git diff abd41eb2 tl/vw-m3-native-layer-extent-fix --check` | — | exit0 |

Exact replay command:

```sh
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-native-extent-final-review-exacttests.py
```

The targeted command inside the frozen private archive was `/home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider --tb=short tests/packs/rendering/test_native_layer_extent.py tests/packs/rendering/test_remotion_native_window.py tests/packs/rendering/test_normal_audio_run.py tests/packs/rendering/test_normal_audio_sources.py tests/packs/rendering/test_normal_audio_source_phase.py`. Full absolute working directories, environment, individual Node/probe commands and log paths are in `-exacttests.txt` and `-results.json` alongside this report. The first PCM attempt had 36 environment-induced failures because this review set NODE_PATH for both Root and PCM tests; runtime correctly refused that override. Initial logs are retained. The corrected run removes it for Python/PCM, without changing product code or expectations.

**Holds and next steps**

The inherited `abd41eb2` placement-precision change is **still HELD and separately unapproved by this extent grant**. The render serializer preserves `at=0.016682` (frame0 at 30000/1001), while persistence rounds it to `.017` (frame1); the passing existing witness confirms this distinction remains. Its shared serializer scope includes normal/default, PNG and Three.js consumers. This review does not implicitly approve that ancestry or its owner-visible behavior change.

Tail semantics are unchanged; combining this scalar with an explicit legacy/tail clock deliberately refuses. This review qualifies plain original-extent transport only and makes no claim about layered media-tail films. Runtime/public0.0.12 adoption and the shared graph repair hold remain. No full suite, browser, live socket, video render, HTTP, MP4 or cross-product pixel/audio parity test was run; no install, network, shared-dependency write or git mutation was performed. Native audio decode uses the checked-in public0.0.12 tarball in a private real scope directory with a private package leaf link; TypeScript uses a read-only leaf link for the stubbed Root tests. No test was weakened, skipped or marked xfail by this review.

Recommended next step: accept the **extent-only** delta and separately land the test-only Root regression patch through the orchestrator's gated workflow. Keep the generalized candidate held until the independent precision decision, tail ownership requirements, consumer adoption and later central HTTP/MP4/parity qualification are resolved. No review blocker remains for this bounded fix.

Artifacts are flat absolute paths under the requested design prefix: `-REPORT.md`, `-scope.patch`, `-sourcebytes.json`, `-exacttests.py`, `-exacttests.txt`, `-results.json`, `-probe.py`, `-root-supplement.test.cjs`, and the corresponding run logs. The source manifest includes exact baseline/candidate identities, file SHA-256/byte counts, original Root patch hash and checked-in public-package hash.
