# Exact commands and results

Run from /home/user/work/wt/vw-m3-tail-layer-legacy-proof unless stated otherwise.
No installation, render, browser, socket, full suite, or git mutation.

Preparation (read-only git archive into private real directories):
```bash
mkdir -p /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tail-layer-legacy-proof/old-source
git archive 2019d7e69 astrid tests astrid_runtime_client pyproject.toml remotion/src/Root.tsx remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz | tar -x -C /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tail-layer-legacy-proof/old-source
python3 - <<'PY'
import tarfile
from pathlib import Path
with tarfile.open('remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz') as archive:
    data = archive.extractfile('package/dist/chunk-SE4TPVLW.js').read()
Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tail-layer-legacy-proof/package-duration-chunk.js').write_bytes(data)
PY
```

Python probes (each exit 0; 296 cases per revision):
```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/vw-m3-tail-layer-legacy-proof /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-tail-layer-legacy-proof-probe.py abd41eb2 > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-tail-layer-legacy-proof-new.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tail-layer-legacy-proof/old-source /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-tail-layer-legacy-proof-probe.py 2019d7e69 > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-tail-layer-legacy-proof-old.json
```

Actual Root callbacks and component tree (exit 0; 296 rows per revision; both registered metadata callbacks; 176 ordinary/full-timeline-only rows identical):
```bash
node /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-tail-layer-legacy-proof-root.cjs > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-tail-layer-legacy-proof-root.log 2>&1
```

Existing main-suite targeted tests, new revision (cwd worktree; exit 0; 36 passed in 3.56s):
```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/vw-m3-tail-layer-legacy-proof /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/core/timeline/test_source_role_tracks.py tests/core/rendering/test_storage.py tests/core/rendering/test_service.py::test_window_timeline_allowlist_slices_to_layer_tracks tests/core/rendering/test_service.py::test_window_timeline_without_allowlist_keeps_existing_pruning tests/core/rendering/test_service.py::test_window_timeline_allowlist_track_without_window_clips_stays_present tests/core/rendering/test_service.py::test_segment_request_stamps_astrid_layer_metadata_merged tests/core/rendering/test_service.py::test_segment_request_z0_stamps_alpha_false tests/packs/rendering/test_managed_timeline_render.py::test_render_clock_keeps_authored_and_rendered_extents_distinct tests/packs/rendering/test_managed_timeline_render.py::test_render_clock_rejects_ambiguous_or_short_tail tests/packs/rendering/test_managed_timeline_render.py::test_managed_render_clock_requires_runtime_admitted_tail_identity tests/packs/rendering/test_remotion_native_window.py::test_native_window_half_open_range_preserves_original_input tests/packs/rendering/test_remotion_native_window.py::test_native_window_none_does_not_change_full_render tests/packs/rendering/test_remotion_native_window.py::test_native_window_manifest_keeps_planner_input_intact > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-tail-layer-legacy-proof-pytest-new.log 2>&1
```

Existing main-suite targeted tests, old revision (cwd private old-source; exit 0; 36 passed in 3.65s):
```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tail-layer-legacy-proof/old-source /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/core/timeline/test_source_role_tracks.py tests/core/rendering/test_storage.py tests/core/rendering/test_service.py::test_window_timeline_allowlist_slices_to_layer_tracks tests/core/rendering/test_service.py::test_window_timeline_without_allowlist_keeps_existing_pruning tests/core/rendering/test_service.py::test_window_timeline_allowlist_track_without_window_clips_stays_present tests/core/rendering/test_service.py::test_segment_request_stamps_astrid_layer_metadata_merged tests/core/rendering/test_service.py::test_segment_request_z0_stamps_alpha_false tests/packs/rendering/test_managed_timeline_render.py::test_render_clock_keeps_authored_and_rendered_extents_distinct tests/packs/rendering/test_managed_timeline_render.py::test_render_clock_rejects_ambiguous_or_short_tail tests/packs/rendering/test_managed_timeline_render.py::test_managed_render_clock_requires_runtime_admitted_tail_identity tests/packs/rendering/test_remotion_native_window.py::test_native_window_half_open_range_preserves_original_input tests/packs/rendering/test_remotion_native_window.py::test_native_window_none_does_not_change_full_render tests/packs/rendering/test_remotion_native_window.py::test_native_window_manifest_keeps_planner_input_intact > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-tail-layer-legacy-proof-pytest-old.log 2>&1
```

The original and current versions of the selected test files are byte-identical (`git diff 2019d7e69 abd41eb2 -- <selected files>` empty).

