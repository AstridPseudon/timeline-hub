## Result

Implemented the one narrow owned-caller fix on base `bc888522c` (`tl/vw-m3-native-fresh-export-label-join`). `run.py` keeps `ASTRID_REMOTION_PROJECT_DIR` for the ephemeral Remotion CLI, but omits it only when a frame-mode `PersistentRemotionFrameSession` is present. The native request still carries `projectDir`; the existing host lease binds and checks that exact admitted project. No core/runtime/SDK/save/DTO/pin/source-factory/registry-policy code changed.

Added direct regression coverage that the existing `HostRemotionSession` request projection rejects a redundant `ASTRID_REMOTION_PROJECT_DIR`, while the existing foreign `projectDir` refusal remains covered. Added caller coverage through the existing final staging callback transport fixtures for text, image, and frame-overlay.

## Evidence

Passed:

`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/core/execution/test_remotion_host_session.py::test_task_cannot_modify_host_scope_inputs_or_escape_attempt tests/core/execution/test_remotion_host_session.py::test_child_cannot_select_a_different_native_executable_or_project 'tests/packs/rendering/test_scene_source_carry.py::test_sdk_source_reaches_real_final_staging_callback[transport-text-card]' 'tests/packs/rendering/test_scene_source_carry.py::test_sdk_source_reaches_real_final_staging_callback[transport-image]' 'tests/packs/rendering/test_scene_source_carry.py::test_sdk_source_reaches_real_final_staging_callback[transport-frame-overlay]'` — **10 passed in 3.67s**.

`git diff --check` — passed.

`PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B -m ruff check --no-cache astrid/packs/rendering/rendering/renderers/remotion/run.py tests/core/execution/test_remotion_host_session.py tests/packs/rendering/test_scene_source_carry.py` reports 16 diagnostics. The same 16 filename/code/message diagnostics are present on the three `HEAD` files; no new lint diagnostic was introduced.

New controller preflight produced fingerprint `191f60f79a03d7d8dd690c1d4084dd36011fe02066bd19d87110d856319f50d4`. Its reviewed capture invocation was deliberately run only to verify the gate and exited 1 with: `physical capture refused: HostRemotionSession._start drops ASTRID_REMOTION_BROWSER_EXECUTABLE; wait for the Agent core fix and refresh this fingerprint`.

The broader targeted invocation selected 29 tests and reported **26 passed / 3 sandbox-blocked**, not product failures. The blocked pre-existing tests require sockets: `test_raw_primary_and_cleanup_fields_cross_inherited_channel`, `test_two_public_command_workers_settle_task_leases_then_host_drains_original`, and `RemotionBackendRegistryGenerationTest::test_remotion_render_env_is_explicit_not_host_inherited`; each hit `PermissionError: [Errno 1] Operation not permitted` before its behavior assertion. No full suite, browser, render, local server, network, or central physical command was run.

## Physical proof status

Not qualified or run. The unchanged core source proves the native host currently projects only `HOME`, `LANG`, `LC_ALL`, `LC_CTYPE`, and `PATH` into its original Node child in `_start`; it does not carry `ASTRID_REMOTION_BROWSER_EXECUTABLE`. The existing `shared-browser.mjs` seam and `astrid-frame-worker.mjs` selector are therefore unreachable from an explicit host environment on this base. Per the brief, the new controller stops with that precise source proof rather than selecting another browser, adding an alias/cache, or weakening validation. A manager/core repair must refresh the new fingerprint and review before one physical frame is attempted.

The approved existing shared-browser cache seam remains the only proposed physical route: isolated HOME, normal explicit source paths/credentials, installed Chrome155 executable and complete tree resolution, private 0700 test cache, cleanup. It was not exercised here.

No settled plan decision was changed. The final source path remains Runtime admission -> materializer -> final Root -> fresh-only revision label; cache/mixed paths remain uncertified.
