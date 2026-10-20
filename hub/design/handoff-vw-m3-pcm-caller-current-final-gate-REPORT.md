**APPROVE source. APPROVE prerequisites. APPROVE bounded tests. Ready for the Agent owner gate.** No defect found in final producer `b6ec4922abebe0672cb7115f073c1ab555870fa1`, tree `303452fe7aa075d8451f641f577db7dcd0b74ca2`. No source edits, test weakening, new xfails, merge or test-service request were made by this reviewer. Nothing is blocked.

The final producer was DONE, exited 0, had no running marker, and had its harness commit before I archived it. My independent Git archive has SHA-256 `c0e7e786f221501fa2afeac8e0a9f38027fed16c316b4751e014d5dc70cbd6ae`. All **3,033 tracked blobs and executable modes** were verified; every blob was rechecked after testing. The extraction has zero extra files, no `.git`, no old 0.0.10 archive, backups, `.orig`, `.rej`, reports or build output. Agent/test imports resolve into my extraction. The assigned worktree stayed clean.

I froze initial current integration `43d567f9d972386dc4cf585fbacc3ad9afc56bdd`, then applied ONLY the seven approved extent paths from `df2739f903edac02bd36b4446deeea847524c040` to final fixture-portable extent `5d0f1ddcad54936b36cedf1d89bf34f45fa612b5`, with zero fuzz. That is the before-caller baseline. The final producer differs from it in exactly four paths:

- `astrid/packs/rendering/rendering/renderers/remotion/run.py`
- `astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py`
- `tests/packs/rendering/test_normal_audio_run.py`
- `tests/packs/rendering/test_normal_audio_http.py`

The runner adds one import and the normal TimelineComposition PCM preparation call before final props serialization. Only `_execute_remotion_locked` changes among its function ASTs; capture and the current final-props callback survive. The helper adds the internal FPS input, accepts a missing server only for a scene with no audio, and preserves the existing managed source/attempt path. The helper and 29-case normal test file are byte-identical to the previously reviewed frozen caller at `b24a2acf565a3ab3ce23b35c6ea0a5196c6decd6`; the HTTP file is byte-identical to portable source `e5a636d59`.

Every other file equals current integration plus the approved extent patch. This includes Root, public12 archive/pins/lock, serializer/quantization, current M2 compiler/provider/schema/client, and the ten already-owned kernel paths except the explicitly reviewed Python helper. There is no DTO, factory, projector, authoring stamp, flag, DSP copy, unrelated M2 change or new Three.js PCM activation. Existing test migration is exactly the approved native/legacy extent migration; no further expectations changed.

The owner landing unit remains the producer's four-path `caller-only.patch`, SHA-256 `ebe571848275f7a7181a7e005cd3595ee8b6d254fcb114741e4f7f4710cf5397`, relative to its current-kernel-plus-extent tree `3e26c4a33f4799cfaa83237462c40dac5fa5cb81`. My separately generated caller-only patch has SHA-256 `734f85185825c2fda1b51a705d5b4dcf1a9dd4cdcb7b7f254341336e77a6b01d`; its formatting/order differs, and all four resulting files match the frozen producer. Do not land the whole-main delivery diff as this caller unit.

**Paired results: 232 passed before caller; 261 passed after caller; each has one prohibited real-render case deselected.** All six old prerequisite failures are GREEN in both trees: the four native layer/window cases, the legacy null-window rejection case, and the locked public package fixture. Current owner fixtures and the approved extent/test migration resolve them without an old archive or private fixture dependency.

| Direct lane | Result |
|---|---|
| Paired common source/scene/package/native/extent/callback/tail/PCM tests, before caller | 232 passed, 1 real-render deselected |
| Same lane plus the normal caller tests, final producer | 261 passed, 1 real-render deselected |
| Actual Root metadata callbacks, each tree | 7 passed each |
| Service window/segment cases, each tree | 5 passed each; 47 unrelated deselected |
| HTTP fixture portability only, final producer | 3 passed; 19 live-server cases deselected |
| Public12 native Node suite | 5 passed |
| Public12 normal Node suite | 8 passed |
| Independent normal-route retry/partial-failure/boost probes | 9 passed |
| Current M2 compiler/projector neighbors | 81 passed, 2 unchanged existing xfailed, 161 subtests passed |
| Helper and both new test files, Ruff | passed |
| Runner Ruff diagnostic comparison | same seven inherited diagnostics; zero new |
| `git diff --check 43d567f9d b6ec4922abebe0672cb7115f073c1ab555870fa1` | passed |

The six normal goldens cover full/native-window/native-layer at 30/1 and 30000/1001, with actual compiler publication and canonical projection, MAIN's serialized `at=0.017`, trim origin `2/fps`, rate 1.5, projected clip gain and track gain, and full native stereo float WAV bytes checked against public12 primitives. The overlap remains muted in consumer props with nonzero PCM, proving mute/scalar gain are not baked again. Whole/sliced tests preserve fade phase. Cancellation, timeout, consumer error, native decode failure and digest refusal preserve cleanup ordering. The independent probes additionally exercise failed-consumer retry with distinct attempt paths, partial PCM failure followed by repaired retry, and boosted track/clip scalar props with unscaled PCM. That boost probe modifies the disposable serialized props via a test double; it does not qualify an encoder or audible output.

The portable HTTP helper defaults to `remotion.REPO_ROOT / "remotion"`, handles an empty override the same way, and accepts explicit `ASTRID_REMOTION_PROJECT_DIR`. Its three socket-free cases pass. The file contains no private worker/home/ORCH path or historical archive dependency. This gate ran no live HTTP/socket case; actual serving is a separate central qualification.

The private Node graph uses real own directories/scopes and links only to individual existing peer leaves. All 77 public12 archive members match before and after; archive SHA-256 remains `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`. All 2,056 entries of the shared Composition dependency graph match before and after. Shared dependencies, runtimes, venvs and caches were not written. Pytest basetemps were removed.

Exact replay commands, all exit 0:

```sh
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-caller-current-final-gate-prepare.py
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-caller-current-final-gate-tests.py baseline
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-caller-current-final-gate-freeze.py
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-caller-current-final-gate-tests.py candidate
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-caller-current-final-gate-postcheck.py
```

The archive drivers intentionally refuse to overwrite existing extraction directories. The retained independent archive is `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-pcm-caller-current-final-gate/candidate-source.tar`.

Every exact test argv, cwd, environment, exit and log path is recorded in the flat absolute files `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-caller-current-final-gate-baseline-results.json` and `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-caller-current-final-gate-candidate-results.json`. The driver uses `/home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider --tb=short` with private basetemps, each source tree as cwd/PYTHONPATH, pinned Node `/tmp/vw-m3-agent-gate-node20.19.4/bin/node`, and private public12/peer leaves. The results JSON includes the complete selectors and environment for every lane. Source/scope/byte proof is in the matching `-freeze.json`, `-blobs.json`, `-postcheck.json`, and patches.

An initial baseline diagnostic mistakenly exported NODE_PATH into native preparation and produced 18 failed / 214 passed / 1 deselected. The unchanged launch policy correctly refused that interpreter/loader override. Its original log/results are retained as `-initial-env-baseline-*`. Removing NODE_PATH from Python test environments made the exact same source pass 232/232; NODE_PATH is now set only for the isolated Root Node callback command. No source or expectation changed to fix this reviewer setup mistake.

Decision: qualify the final harness commit against the independently composed current baseline, rather than reviewing mutable producer files. The owner can gate/land the exact approved extent prerequisite, then this caller-only unit. A changed integration base needs its own reconciliation. No full suite, browser, render, install, network, local socket or git mutation/push ran here. Root tests stub framework imports. Runtime/P1 safeSourceTuple, actual encoder/MP4 and Player/export parity remain unqualified by this gate.
