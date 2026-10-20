# Inactive CURRENT producer prerequisite — interface in progress

Worktree /home/user/work/wt/vw-m3-normal-pcm-producer-current; no normal path activation/core/provider/pin edits.

Planned callable (same prior proposal import):
`astrid.packs.rendering.rendering.renderers.remotion.normal_audio.prepare_normal_audio_sources(props, *, materializer, asset_server, attempt_directory, project_dir, runtime_tools, original_clips=None) -> dict`
`original_clips: Mapping[str, Mapping[str, Any]] | None` maps disposable current clip ID to the actual original compiled occurrence clip, retained by the source owner before slicing. This is ordinary internal data, NOT a source grant or factory. Only owner-validated input is allowed; the helper never reads app.astrid_slice_origin as authority. Source owner must bind actual transformed pair before calling. Without that join, no actual normal/window/layer positive is claimed.

Caller keeps a TemporaryDirectory under materializer.serving_root via its existing ExitStack through consumption, then cleanup. Helper produces only its own subdirectories and removes those on failure; success files survive for caller consumption. Existing actual base has AssetMaterializer.resolved_registry and InvocationAssetServer.local_url; no register_attempt_file exists here. Use those actual APIs. Exact Root assets registry must match materializer; clips resolve by asset key to verified local_path, Node decodes that path with unchanged public12 apply/WAV/trim/rate helpers and returns WAV path/clock/envelope, Python registers via local_url. No caller render_source is accepted.

Served-source fixture counterpart: please prepare against this callable; original signature remains compatible. No sockets/service/browser/render/full runs in this worker. Public12 test runtime lives in ORCH only; official package remains 0.0.10 pending owner.
