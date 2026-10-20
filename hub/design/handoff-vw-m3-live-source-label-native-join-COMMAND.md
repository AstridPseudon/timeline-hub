Worktree: /home/user/work/wt/vw-m3-live-source-label-native-join
Base: 634867fed71b4ae53acaa3c3162315527c2bdb23
Runtime used for final named proof: frozen git archive 7f6dd8920e1ceec41b137358df5e7fecc304888d (clean integration HEAD when selected). The brief's 0132c4 object is absent here; this compatible Runtime executes the real provider capture verification successfully.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider -o addopts= \
  tests/packs/rendering/test_fast_lane.py \
  tests/packs/rendering/test_timeline_filmstrip_cards.py \
  tests/packs/rendering/test_timeline_filmstrip_execution.py \
  tests/packs/rendering/test_timeline_offline_inspection.py \
  tests/sdk/test_timeline_commit_provider.py::test_move_reload_and_inverse_import_no_renderer \
  tests/sdk/test_timeline_capture_projection.py::test_capture_method_imports_and_runs_without_renderer_or_runtime \
  tests/editing_conformance/test_recipe_scalar_commands.py::test_scalar_capture_and_save_import_no_renderer_or_runtime \
  tests/editing_conformance/test_recipe_shot_set.py::test_shot_set_capture_and_save_import_no_renderer_or_runtime
# 100 passed, 1 existing Pillow deprecation warning; 17.38s.

/home/user/work/venv-agent/bin/python -m ruff check --no-cache \
  tests/packs/rendering/test_live_source_label_native.py \
  astrid/packs/rendering/actions/timeline_visualize/provenance.py \
  tests/packs/rendering/test_fast_lane.py
# All checks passed.
git diff --check
# exit 0.

O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
R=$("$O/bin/request-test" vw-m3-live-source-label-native-join integration-viewing-live-source-label-native) && "$O/bin/wait-test" "$R"
# 1020142410-15489: 18 passed in 81.97s; tree 1e6fc112e17e8b811e7aaf206a556ebfa63551f3.
# Final uncached request 1020142658-20591: 18 passed in 96.60s, same tree; complete frozen-source/toolchain pre/post manifests byte-identical.
```

The named suite invokes the adjacent flattened run-integration.py source. It runs pytest under a private copied Python environment, clears ambient Node/Git loader overrides, selects the private public12/f816 Remotion graph and frozen Runtime source, and binds the native host imports to the central service's actual Agent snapshot. No readiness, admission, renderer, source factory or scene answer is replaced. Normal owned launch validation, lock, Root preparation, invocation asset HTTP server, URL byte reads and public native query execute in the test service. No Browser, renderer or fresh PNG is produced.

Preparation source is flattened alongside this file. The private environments are disposable; rebuild by copying the flat preparation scripts into this worker directory, running prepare.py, copying the shared Agent venv into workers/vw-m3-live-source-label-native-join/python-overlay (symlinks preserved, no install), and extracting `git -C /home/user/work/runtime archive 7f6dd8920e1ceec41b137358df5e7fecc304888d` into its runtime-source directory. Do not run the integration test directly in the sandbox. The helper selects its Remotion project from ASTRID_REMOTION_PROJECT_DIR; `--no-cache` on a named rerun is only needed when independently qualifying new external environment inputs.

Initial iterations are retained in central result logs: fixture omitted required output.file, track labels, renderer-supported clip fields and explicit asset digest pins; owned validation initially absent, then a test-local lock override correctly refused by the owned generator. Fixed only the new pre-retention fixture/normal test setup; no admitted snapshot was repaired and no failure expectation weakened. Initial direct neighbors: 94 passed / 2 expected metadata-label assertion failures; the explicitly requested one-to-one expectations were updated. One attempted direct command named an absent prior-worker test_scene_check_save_boundary.py and collected zero tests; final NoNode evidence uses the four existing repository cases above.

Final bracketing command (after expanded preflight):
```sh
R=$("$O/bin/request-test" vw-m3-live-source-label-native-join integration-viewing-live-source-label-native --no-cache) && "$O/bin/wait-test" "$R"
# 18 passed in 96.60s. No further test request.
python3 "$O/workers/vw-m3-live-source-label-native-join/inventory.py" final-post
cmp "$O/workers/vw-m3-live-source-label-native-join/qualified-pre.json" "$O/workers/vw-m3-live-source-label-native-join/final-post.json"
# exit 0; both e1b4ad6c9a53e0e439de9264ec55685f8e9c5060e694c6bf8135ea4d2309c3ed.
```
Private environments and pytest scratch are removed after postflight, as requested. Reconstruct them with the preparation steps above before replay. No installed package or shared cache is edited by that procedure.
