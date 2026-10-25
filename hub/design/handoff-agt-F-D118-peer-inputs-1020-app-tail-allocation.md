# D118 App tail allocation

Status: RESERVED_EXISTING_ASSIGNMENTS. These are the three reservations already named by the Agent manager; no competing cluster is opened.

Retained source: service `agt-F-D108b-core-local-0811-agent-core-full-1025081835-2016`, XML SHA-256 `72872c77087719a692bff4b48b8d85ea62b9931d59a502c8e246daee0c81c18a`, outcomes JSON SHA-256 `c180c1c153264d09e2ae79e0ad63007d9551e43e7b72e87973f0927140a6e2eb`. Counts are 8763 passed, 159 failed, 347 errors. Current source is Agent `e9e3b8f78a103331c38b70c008bf020f13c46413`, tree `b1d90e5f2cfe42858efb7226c56192b948e1108c`; Runtime is `d23a8e0d24bf2aeaf984072eaca0d3dcf8873c2e`, tree `6283b5fbb128447f1b333e0e6af334d35637cf69`.

## audio2 — existing reservation

Allowed file: `tests/editing_conformance/test_compile_contracts.py` (current SHA-256 `519a2aa5431aa8ad324f88cc649ff2bdc631f55d3e8b7b482a8e1200d3e37b4a`).

Node IDs, retained locations and failure hashes:

| ordinal | node ID | location | failure-text SHA-256 |
|---:|---|---|---|
| 27 | `tests/editing_conformance/test_compile_contracts.py::test_audio_vector[fade-in-needs-prepared-envelope-source]` | `tests/editing_conformance/test_compile_contracts.py:154` | `a260ae0bb7ae0daba0d82a020353782bc98785f7184b00fa853cd54aa8f3c6bf` |
| 34 | `tests/editing_conformance/test_compile_contracts.py::test_audio_vector[fade-out-needs-prepared-envelope-source]` | `tests/editing_conformance/test_compile_contracts.py:154` | `9ab421312980fc7ee5f7822a53f1864c78a502dd9c59eddc1efdc7be1119fc52` |

Upstream scope: compile contract vectors; retain authored intervals, values, purpose, and both assertions. Do not touch any other path, production module, Runtime, generated file, registry, ledger, harness, or retained run.

Focused commands:

    PYTHONPATH=.:/home/user/work/wt/rt-pin-1daca2a3 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 tests/editing_conformance/test_compile_contracts.py -k 'test_audio_vector and (fade-in-needs-prepared-envelope-source or fade-out-needs-prepared-envelope-source)'
    ruff check --no-cache tests/editing_conformance/test_compile_contracts.py
    python -m py_compile tests/editing_conformance/test_compile_contracts.py
    git diff --check

## current-sheet15 — existing reservation

Allowed file: `tests/editing_conformance/test_native_sheet_current_runtime.py` (current SHA-256 `3d391f6362053159a15f7d8ee15c7088c4b4e44a85431c0b094195a07027b8b7`).

Node IDs, retained locations and failure hashes:

| ordinal | node ID | location | failure-text SHA-256 |
|---:|---|---|---|
| 1262 | `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_emitter_null_presence_and_track_roundtrip_is_authenticated` | `tests/editing_conformance/test_native_sheet_current_runtime.py:544` | `c7538bad075c2d4d83f6ed05799a4c69b127e59101dfd064ca8106cba6483683` |
| 1264 | `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_omitted_native_clip_row_delete_retries_rebases_and_refuses_changed_selection` | `astrid/sdk/timeline/sync.py:556` | `37ce2a09f663b7d0f6a0d32053e5f78b92ad2d6f47e9bdc6f04e976ec6e512a6` |
| 1268 | `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_cut_owned_native_sheet_hold_reloads_and_undoes` | `tests/editing_conformance/test_native_sheet_current_runtime.py:817` | `27a21484325c0cde1cc9943f359e33fbbf2c2515465e6928f04cf368238b8bd6` |
| 1271 | `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_label_clear_is_lossless_across_native_frontends[python]` | `tests/editing_conformance/test_native_sheet_current_runtime.py:871` | `3195968d02abd4fc53eae4eee598314c1e3c8d3b0761ab39b93c12f80f2e7547` |
| 1273 | `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_label_clear_is_lossless_across_native_frontends[cli]` | `tests/editing_conformance/test_native_sheet_current_runtime.py:871` | `0e6eb33ca5369b0b8ba7dd7b714c0d8460b56b58b2320244ee2ffb31f7fe16e6` |
| 1275 | `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_label_clear_is_lossless_across_native_frontends[sheet]` | `tests/editing_conformance/test_native_sheet_current_runtime.py:871` | `1ea4179bd6e1298026720c66ca9ba7cbdefe7f0a9947d0eff199db1243a7729f` |
| 1276 | `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_attached_parent_label_publish_retries_exact_capture_and_inverse` | `tests/editing_conformance/test_native_sheet_current_runtime.py:933` | `ffbebe9f6162f4226597586bd8a92dd156a3a888e9d0e259ad7d7822ebf6c48e` |
| 1277 | `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_original_attached_add_track_publish_retries_exact_capture_and_guarded_inverse` | `tests/editing_conformance/test_native_sheet_current_runtime.py:992` | `c65c8a013b7f5bb1ec7ed92e4848f651910c05a85dadc3e53a43d7680d41cd8d` |
| 1279 | `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_rational_move_is_lossless_across_native_frontends[python]` | `tests/editing_conformance/test_native_sheet_current_runtime.py:1051` | `db22014da106a11865c2f9ea9c6972fb9944a907cd3d184b5872bc374896e3fa` |
| 1281 | `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_rational_move_is_lossless_across_native_frontends[cli]` | `tests/editing_conformance/test_native_sheet_current_runtime.py:1051` | `5f0155cfffdb10a9ac45fff49a13b23c1b3417d01f8ef3e8f2deadca2fb69a8d` |
| 1283 | `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_rational_move_is_lossless_across_native_frontends[sheet]` | `tests/editing_conformance/test_native_sheet_current_runtime.py:1051` | `bda7ce3e95bedee889fc52cbe78d23c7c94b98393e37cc700a052639ace53a59` |
| 1285 | `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_occurrence_move_preserves_shared_source_across_native_frontends[python]` | `tests/editing_conformance/test_native_sheet_current_runtime.py:1129` | `40ecb15f5f8225be3e52bdc67ffa80716e0fb9d23cfc58d4abaed925a46ff271` |
| 1288 | `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_occurrence_move_preserves_shared_source_across_native_frontends[cli]` | `tests/editing_conformance/test_native_sheet_current_runtime.py:1129` | `3dde3318db215cfdf56b4ec3dacf8b7bd22673665366f6fcd1c5e55321e4a08b` |
| 1291 | `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_occurrence_move_preserves_shared_source_across_native_frontends[sheet]` | `tests/editing_conformance/test_native_sheet_current_runtime.py:1129` | `276b786ff6e9d5673eba4293a3956826158abc4a40a1d4c9e061ac681b4bdba6` |
| 1299 | `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_semantic_batch_original_pins_reload_inverse_redo[cli]` | `tests/editing_conformance/test_native_sheet_current_runtime.py:1238` | `7d3f06987fb996165951e9e9c0761692dd103ffc20cc6fa8228bfc8948728cd3` |

Upstream scope: current parent, opaque values, native and HTTP frontends, rational timing, reload, undo/redo, ABA, and no-write assertions. Do not touch any other path, production module, Runtime, generated file, registry, ledger, harness, or retained run.

Focused commands:

    PYTHONPATH=.:/home/user/work/wt/rt-pin-1daca2a3 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 tests/editing_conformance/test_native_sheet_current_runtime.py -k 'emitter_null_presence or omitted_native_clip_row_delete or cut_owned_native_sheet_hold or connected_label_clear or attached_parent_label_publish or original_attached_add_track or connected_rational_move or connected_occurrence_move or semantic_batch_original_pins'
    ruff check --no-cache tests/editing_conformance/test_native_sheet_current_runtime.py
    python -m py_compile tests/editing_conformance/test_native_sheet_current_runtime.py
    git diff --check

## WC6three — existing reservation

Allowed files: `tests/sdk/test_wc6_completion_capture.py` (current SHA-256 `d4888723f78c2e37f5a22c7584decc57d16e81c155c429943a3eed38a5c1d0ec`) and `tests/sdk/test_wc6_completion_capture_runner.py` (current SHA-256 `edaca1d4f1098ba756b5a8b1126838921e983e865072c9956e45dd187c862443`).

Node IDs, retained locations and failure hashes:

| ordinal | node ID | location | failure-text SHA-256 |
|---:|---|---|---|
| 7645 | `tests/sdk/test_wc6_completion_capture.py::test_preserved_original_and_mounted_source_attachment` | `tests/sdk/test_wc6_completion_capture.py:234` | `e61226d8f0f591fa2b7fab9dc129ca72e8de2dc85d70f6d4a18ebebd1c7c20a7` |
| 7646 | `tests/sdk/test_wc6_completion_capture.py::test_session_calls_mounted_service_real_provider_and_port_offline` | `tests/sdk/test_wc6_completion_capture.py:304` | `e72f531c4d699d9f4cb459bcbf0995edf28c20698e40d6b1fccedaf0fd12c6f9` |
| 7649 | `tests/sdk/test_wc6_completion_capture_runner.py::test_wc6_runner_guards_argv_helper_sink_budgets_and_retention` | `tests/sdk/test_wc6_completion_capture_runner.py:19` | `a121faeb3f9bc9764f33f4ba2953730b9eff94895ba953e26835f5341b42fcb8` |

Upstream scope: mounted real provider and port call shape; preserve assertions, budgets, privacy, and no-write behavior. Do not touch any other path, production module, Runtime, generated file, registry, ledger, harness, or retained run.

Focused commands:

    PYTHONPATH=.:/home/user/work/wt/rt-pin-1daca2a3 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 tests/sdk/test_wc6_completion_capture.py tests/sdk/test_wc6_completion_capture_runner.py
    ruff check --no-cache tests/sdk/test_wc6_completion_capture.py tests/sdk/test_wc6_completion_capture_runner.py
    python -m py_compile tests/sdk/test_wc6_completion_capture.py tests/sdk/test_wc6_completion_capture_runner.py
    git diff --check

This is a read-only allocation packet. It claims no functional pass and opens no new author cluster. The full JSON packet carries the exact node IDs and hashes.
