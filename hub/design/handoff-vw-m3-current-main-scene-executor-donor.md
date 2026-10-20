# Viewing -> Agent: current-main Scene executor donor

Base `d30894a7abfa6e3163c13a59175b4a0d298c7fea`.

The current-compatible patch adds:

- `actions/timeline_visualize/scene_only.py` — managed Scene-only executor and filmstrip artifact writer;
- `filmstrip_execution.py` — `scene_only` admission dispatch;
- `pack.yaml` — implementation resource registration;
- `scene_answers._prepared_host_frames_at` — current `root_preparation._prepared_remotion_root` query adapter;
- direct executor/query/closure tests.

The adapter retains the existing Root lifetime and lock, exact inherited-source validation, full canonical frame extent, compiled clip IDs and scene address map, capture identity/video digest/timeline identity, and advisory-unavailable behavior. It does not add a source factory, provider, DTO, certification, second projector, save-path Scene, or SDK/Runtime edit.

Evidence: `35 passed` for `tests/packs/rendering/test_scene_only_executor.py tests/packs/test_pack_yaml_schema.py`; new-file Ruff passed; `git diff --check` passed. The existing `test_scene_host.py` neighbor had `28 passed, 15 setup errors` because this worktree lacks `remotion/node_modules/esbuild`; no shared install or render was attempted.

Combined patch stream SHA-256: `a92452636cec2c3be169dda4bb8d01e899e3cc40d9413d7eb7d1e4f54073dea8`.

Agent join instruction: consume this Viewing fragment on top of the active SDK caller join; do not port the old broad Scene merge or duplicate the executor in SDK.
