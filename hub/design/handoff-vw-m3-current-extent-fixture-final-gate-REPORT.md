**APPROVE — ready for the Agent owner gate.** Final producer source **5d0f1ddcad54936b36cedf1d89bf34f45fa612b5**, tree **dbd59878d5710b938a4107bbad4469a0da78e219**. This is a read-only qualification of the fixture-portability patch over **da10b0b7690a8c2a4032e75eb3d4a3e988121997**. No repository edits or merge/test-service requests were made. Nothing is blocked.

The producer was DONE, exited 0, had no running marker, and had its final harness commit before the review archive was created. I extracted an independent Git archive into my own worker folder, verified all **3,009 tracked blobs** before testing, and reverified them afterward. The final extraction contains **zero extra files**, no `.git`, and no old 0.0.10 archive. Imports of Agent and test modules resolve into this extraction. The frozen producer tip stayed unchanged and my assigned worktree stayed clean.

The entire patch changes only `tests/packs/rendering/test_remotion_layer_tail_compat.py`: it adds a helper resolving the package's local `file:` dependency, ensures that the resolved archive stays inside Remotion and exists, and substitutes that helper at the old archive assignment. The rest of `_root_probe` is AST-identical. All **9 existing tail test functions** are AST-identical; their complete **63-assertion multiset** survives (65 assertions now, including two helper checks). All other tracked files are byte-identical to da10, including the other three tests in the approved seven-file unit, native-window/callback/M2 neighbors, clocks, pins, and package/lock files. There are no changed expectations, skips, xfails, product edits, new DTOs, factories, projectors or authored stamps.

Protected product SHA-256 values, each byte-equal to da10:

| Path | SHA-256 |
|---|---|
| `astrid/core/rendering/service.py` | `930cb134e96d005816e8c2c3f690574c3c9f3097d5da216be43a8037b6c73dff` |
| `astrid/packs/rendering/rendering/renderers/remotion/run.py` | `5c3cd96bf8561eebc369090fe3c520fac40457802458959827c7903464837269` |
| `remotion/src/Root.tsx` | `afde359fcf7324f0885543e3f3292372bd1b94bb3f219477bd15a2a4ee704f90` |

The fixture resolves the **current committed** dependency `file:artifacts/banodoco-timeline-composition-0.0.12.tgz` from `remotion/package.json`. Its archive reports version **0.0.12**, matches the current lock's SHA-512 integrity, and has SHA-256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`. Its actual duration chunk has SHA-256 `887441a18596fd09bd145381f6745ca986372cd32fb59278733f6b8d161f494b`. The committed tail suite has no old-archive, private worker, ORCH, or historical Git dependency. An old revision name remains only in an unchanged explanatory docstring. Node 20.19.4 and shared TypeScript 5.9.3 are tooling prerequisites; no package install occurred. A private real Node scope contains only a read-only TypeScript leaf. Shared dependencies, runtimes and caches were not modified.

**177 bounded checks passed without provisioning 0.0.10:** 166 pytest cases and 11 Node cases. Of these, 167 are repository-native cases; 10 are retained independent reviewer probes.

| Executed lane | Result |
|---|---|
| Committed extent + tail files | **95 passed** (73 extent, 22 tail) |
| Native-window + scene-props callback | **36 passed** |
| Live-scene/M2 non-render subset | **17 passed**, 1 real-render test deselected |
| Clock/service/storage subset | **12 passed**, 106 unrelated tests deselected |
| Committed actual Root metadata callbacks | **7 passed** |
| Supplemental Root rational/boolean/bounded-clock cases | **4 passed** |
| Independent original-extent service→bounds cases | **4 passed** |
| Actual Three component source-props comparison | **2 passed** |

The native/legacy positives, refusals, 3D pins and opaque state, callbacks, half-open frame bounds, pre-tail positives, full-tail and no-clock controls therefore remain green. Three source props match native versus legacy routes and the previously saved baseline payloads at frames 0–30, including the absent source at the endpoint. The saved baseline comparison is optional reviewer evidence outside the repository suite; neither the committed fixture nor its ordinary test run needs historical Git/private worker files. Root callbacks and Three component bodies execute the actual frozen source with framework imports stubbed. This qualifies bounded source/command/props behavior.

Targeted three-test-file Ruff and `git diff --check da10b0b76 5d0f1ddcad54936b36cedf1d89bf34f45fa612b5` both **pass**. No broader lint/typecheck, full suite, browser, socket, render, MP4/encoder/decoder, pixel/audio parity or actual Runtime qualification was run or claimed. The prior report's missing-fixture failure is resolved for this exact frozen tip; this gate does not rerun historical branches or widen the tail policy.

The choice was to qualify the final producer commit without modifying it; its one-file scope preserves the previously approved product behavior. Recommended next step: submit this exact tip and evidence to the Agent owner gate. No remote request was made.

Exact replay drivers (all evidence paths are absolute):

```sh
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-extent-fixture-final-gate-freeze.py
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-extent-fixture-final-gate-tests.py
```

The freeze driver intentionally refuses to overwrite its existing archive. The retained source archive is `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-extent-fixture-final-gate/final-source.tar` (SHA-256 `4cbdd353fc032c9573ea6c729f75c42a260defcba189f24af9c22e126dbe6287`). Tests use cwd `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-extent-fixture-final-gate/candidate`, `PYTHONPATH` and `REVIEW_SOURCE_ROOT` bound to that directory, bytecode and pytest caches disabled, private pytest basetemps, `NODE_PATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-extent-fixture-final-gate/root-modules/node_modules`, `ROOT_SOURCE_DIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-extent-fixture-final-gate/candidate/remotion/src`, and pinned Node first on PATH. The import check, full environments, exact argument arrays, exits and log paths are recorded in [handoff-vw-m3-current-extent-fixture-final-gate-results.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-extent-fixture-final-gate-results.json). Integrity/scope details are in [handoff-vw-m3-current-extent-fixture-final-gate-freeze.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-extent-fixture-final-gate-freeze.json), [handoff-vw-m3-current-extent-fixture-final-gate-all-blobs.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-extent-fixture-final-gate-all-blobs.json), [handoff-vw-m3-current-extent-fixture-final-gate-scope.patch](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-extent-fixture-final-gate-scope.patch), and [handoff-vw-m3-current-extent-fixture-final-gate-postcheck.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-extent-fixture-final-gate-postcheck.json).

Exact test/lint commands (each exits 0; cwd/environment as above):

```sh
/home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider --tb=short tests/packs/rendering/test_native_layer_extent.py tests/packs/rendering/test_remotion_layer_tail_compat.py --basetemp=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-extent-fixture-final-gate/tmp-extent-tail
/home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider --tb=short tests/packs/rendering/test_remotion_native_window.py tests/packs/rendering/test_remotion_capture_scene_props.py --basetemp=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-extent-fixture-final-gate/tmp-native-callback
/home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider --tb=short tests/packs/rendering/test_live_scene_composition.py -k 'not real_render' --basetemp=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-extent-fixture-final-gate/tmp-live-scene17
/home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider --tb=short tests/core/rendering/test_service.py tests/core/rendering/test_storage.py tests/packs/rendering/test_managed_timeline_render.py -k 'render_clock or declared_render_tail or window_timeline or segment_request' --basetemp=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-extent-fixture-final-gate/tmp-clock-service
/tmp/vw-m3-agent-gate-node20.19.4/bin/node /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-extent-fixture-final-gate/candidate/remotion/tests/root-metadata.test.cjs
/tmp/vw-m3-agent-gate-node20.19.4/bin/node /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-extent-fixture-final-gate-root-supplement.test.cjs
/home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider --tb=short /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-extent-fixture-final-gate-probe.py --basetemp=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-extent-fixture-final-gate/tmp-independent
/home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider --tb=short /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-extent-fixture-final-gate-three-source.py --basetemp=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-extent-fixture-final-gate/tmp-three-source
/home/user/work/venv-agent/bin/python -B -m ruff check --no-cache tests/packs/rendering/test_native_layer_extent.py tests/packs/rendering/test_remotion_layer_tail_compat.py tests/packs/rendering/test_live_scene_composition.py
```
