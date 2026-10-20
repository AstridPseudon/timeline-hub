"""Invocation-scoped Root preparation shared by rendering and read-only queries."""

from __future__ import annotations

import json
import os
import shutil
from contextlib import ExitStack, contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Callable, Iterator, Mapping, Sequence, cast

from astrid.core.env_vars import ASTRID_INTERNAL_INVOCATION
from astrid.core.rendering.contracts import FrameWindow
from astrid.core.rendering.remotion_runtime import RemotionRuntimeTools


def _accounted_attempt_root(
    staging_parent: Path,
    provenance_out_path: Path,
) -> Path | None:
    """Return the host-owned attempt root proved by its progress marker.

    The progress path is an existing internal invocation carrier.  Requiring
    the real, owner-only marker parent to contain both the service workspace
    and output prevents a caller from selecting an unrelated short directory.
    Direct callers and failed/foreign proofs retain the existing workspace
    parent.
    """
    if os.environ.get(ASTRID_INTERNAL_INVOCATION) != "1":
        return None
    raw_progress = os.environ.get("ASTRID_PROGRESS_PATH")
    if not raw_progress:
        return None
    progress = Path(raw_progress)
    if not progress.is_absolute() or progress.name != ".astrid-progress.json":
        return None
    try:
        if (progress.is_symlink() or not progress.parent.is_dir()
                or staging_parent.is_symlink() or not staging_parent.is_dir()
                or any(part.is_symlink() for part in (staging_parent, *staging_parent.parents))
                or any(part.is_symlink() for part in (provenance_out_path, *provenance_out_path.parents))):
            return None
        if any(part.is_symlink() for part in (progress.parent, *progress.parent.parents)):
            return None
        attempt = progress.parent.resolve(strict=True)
        facts = attempt.stat()
        if (not attempt.is_dir() or facts.st_uid != os.getuid()
                or facts.st_mode & 0o077):
            return None
        staging = staging_parent.resolve(strict=True)
        output = provenance_out_path.resolve(strict=False)
    except OSError:
        return None
    if (staging.parent != attempt
            or not output.is_relative_to(attempt)
            or not staging.is_relative_to(attempt)
            or not output.parent.name == "outputs"):
        return None
    return attempt


@contextmanager
def _prepared_remotion_root(
    timeline_path: Path,
    assets_path: Path,
    staged_video: Path,
    *,
    provenance_out_path: Path,
    project_dir: Path,
    composition_id: str,
    theme_path: Path | None,
    min_free_gb: float | None,
    review: Mapping[str, Any] | None = None,
    materialized_root: Path | None = None,
    staging_parent: Path | None = None,
    materialized_objects: Mapping[str, str] | None = None,
    composition_clip_types: frozenset[str] = frozenset(),
    encode_aac_at_stitch: bool = False,
    frame_numbers: Sequence[int] | None = None,
    frame_output_dir: Path | None = None,
    on_scene_props: Callable[[Mapping[str, Any], Sequence[int]], None] | None = None,
    window: FrameWindow | None = None,
    composition_duration_frames: int | None = None,
) -> Iterator[tuple[
    dict[str, Any], Path, RemotionRuntimeTools, dict[str, Any], dict[str, Any],
    dict[str, Any], Path, int, str, Path, str | None, bool, Path | None, bool, Path,
]]:
    """Hold final Root props and their assets until the caller finishes.

    The caller owns the non-recursive Remotion lock. Preparation keeps the
    existing backend admission/staging seams and never launches the renderer.
    Props are read-only to the consumer; a query does not certify a capture.
    """
    from astrid.packs.rendering.rendering.renderers.remotion import run as backend

    if window is not None and frame_numbers is not None:
        raise ValueError("native render windows cannot be combined with frame_numbers")
    window_argument = None
    if window is not None or composition_duration_frames is not None:
        window_argument = backend._native_window_argument(
            window,
            backend._serialize_timeline(timeline_path),
            backend._canonical_profile(timeline_path, backend._load_registry_mapping(assets_path), theme_path),
            composition_duration_frames=composition_duration_frames,
        )
    runtime_tools = backend._validate_project_dir(project_dir)
    backend._regenerate_element_registries(project_dir, theme_path)
    # Render admission: the catalog and the active composition's generated
    # EFFECT_REGISTRY must agree.  A catalog effect that the registry cannot
    # mount would otherwise pass validation and silently drop to the base
    # plate; fail closed here with an actionable diagnostic.
    timeline_data = backend._serialize_timeline(timeline_path)
    backend._validate_renderer_effect_registry(project_dir, timeline_data)
    registry_state = backend._effective_registry_state(theme_path)
    backend._require_free_space(provenance_out_path.parent, min_free_gb)
    remotion_port = backend._available_remotion_port()
    remotion_origin = f"http://localhost:{remotion_port}"
    props_path = (provenance_out_path.parent / ".remotion-props.json").resolve()
    render_hash = backend._render_asset_stage_hash(
        timeline_path,
        assets_path,
        provenance_out_path,
    )
    staged_public_root = project_dir / "public" / "astrid-effects" / render_hash
    with ExitStack() as asset_lifecycle:
        try:
            requested_parent = staging_parent or provenance_out_path.parent
            attempt_root = _accounted_attempt_root(
                requested_parent, provenance_out_path,
            )
            temp_parent = attempt_root or requested_parent.resolve()
            temp_parent.mkdir(parents=True, exist_ok=True)
            remotion_temp_root = Path(
                asset_lifecycle.enter_context(
                    TemporaryDirectory(
                        prefix=".r-" if attempt_root is not None else ".remotion-runtime-",
                        dir=str(temp_parent),
                    )
                )
            )
            backend._assert_outside_public(remotion_temp_root, project_dir)
            materializer = asset_lifecycle.enter_context(
                backend.AssetMaterializer(
                    assets_path,
                    materialized_objects=materialized_objects,
                    materialized_root=materialized_root,
                    allow_derived_files=materialized_root is not None,
                    reuse_materialized_paths=materialized_root is not None,
                    staging_parent=staging_parent,
                )
            )
            asset_server = None
            if materializer.needs_server:
                try:
                    asset_server = asset_lifecycle.enter_context(
                        backend.InvocationAssetServer(
                            materializer.serving_root,
                            allowed_origin=remotion_origin,
                        )
                    )
                except OSError as exc:
                    raise RuntimeError(
                        f"Permission denied (1100): local HTTP asset server blocked: {exc}"
                    ) from exc
            resolved_registry = materializer.resolved_registry(asset_server)
            # ``theme_path`` is either the host's absolute materialized
            # document or None, which selects the intentional built-in style.
            theme_for_props = backend._resolved_theme_for_render(timeline_path, theme_path)
            merged_props = {
                "timeline": backend._serialize_timeline(
                    timeline_path,
                    default_theme=str(theme_for_props.get("id") or "banodoco-default"),
                ),
                "assets": resolved_registry,
                "theme": theme_for_props,
                "review": review,
            }
            if composition_duration_frames is not None:
                merged_props["astridCompositionDurationInFrames"] = composition_duration_frames
            # Batch 4 (layer stack): the service stamps
            # ``metadata.astrid_layer.alpha = z > 0`` onto the materialized
            # timeline of z-layer segments.  When the stamp says alpha, emit
            # TRANSPARENT output (PNG frames -> ProRes 4444/yuva444p12le in
            # MOV -- remotion 4.0.509 muxes NO alpha plane for vp9/webm, so
            # ProRes 4444 is the alpha path); the unstamped path keeps
            # today's jpeg/h264/MP4 contract exactly.
            alpha = backend._timeline_alpha(merged_props["timeline"])
            # Remotion 4.0.509 otherwise compresses the mix to raw ADTS AAC
            # before copying it into MP4, losing encoder priming metadata.
            # Keep this correction explicit and scoped to opaque MP4 capture.
            # PCM requires a .mov/.mkv CLI name; the Astrid config hook writes
            # MP4 bytes to this invocation-private .mov, then we stage them at
            # the original path without changing the published output profile.
            frame_mode = frame_numbers is not None
            if frame_mode:
                if not frame_numbers or any(
                    type(frame) is not int or frame < 0 for frame in frame_numbers
                ):
                    raise ValueError("frame capture requires non-negative integer frames")
                if frame_output_dir is None:
                    raise ValueError("frame capture requires an output directory")
                frame_output_dir = frame_output_dir.resolve()
                frame_output_dir.mkdir(parents=True, exist_ok=True)
            pcm_aac_mp4 = (
                encode_aac_at_stitch
                and not frame_mode
                and not alpha
                and staged_video.suffix.lower() == ".mp4"
            )
            cli_video = (
                frame_output_dir if frame_mode else
                remotion_temp_root / "capture.mov" if pcm_aac_mp4 else staged_video
            )
            if alpha:
                # Theme background neutralization: the DOM
                # TimelineComposition paints ``theme.visual.color.bg`` as an
                # opaque AbsoluteFill (node_modules/@banodoco/...:272), so a
                # stamped top layer would still emit opaque corners even with
                # the threejs <color> skip.  Making the serialized theme's bg
                # transparent keeps BOTH compositions from painting anything
                # opaque.  This mutates only the per-run props copy; the
                # resolved theme dict is built fresh for this render.
                theme_color = merged_props["theme"].setdefault("visual", {}).setdefault("color", {})
                theme_color["bg"] = "transparent"
            stage_summary = backend._stage_effect_assets_for_timeline(
                merged_props["timeline"],
                project_dir=project_dir,
                theme_path=theme_path,
                render_hash=render_hash,
                composition_clip_types=composition_clip_types,
                asset_registry=resolved_registry,
            )
            if not frame_mode and composition_id == backend.DEFAULT_COMPOSITION_ID:
                audio_attempt = Path(asset_lifecycle.enter_context(TemporaryDirectory(
                    prefix="normal-audio-attempt-",
                    dir=materializer.serving_root if asset_server is not None else remotion_temp_root,
                )))
                audio_profile = backend._canonical_profile(
                    timeline_path, backend._load_registry_mapping(assets_path), theme_path,
                )
                merged_props = backend.prepare_normal_audio_sources(
                    merged_props, materializer=materializer, asset_server=asset_server,
                    attempt_directory=audio_attempt, project_dir=project_dir,
                    runtime_tools=runtime_tools,
                    fps=audio_profile.fps_rational[0] / audio_profile.fps_rational[1],
                )
            staged_video.parent.mkdir(parents=True, exist_ok=True)
            props_path.write_text(json.dumps(merged_props), encoding="utf-8")
            if on_scene_props is not None and frame_numbers is not None:
                on_scene_props(merged_props, frame_numbers)
            yield (
                merged_props, props_path, runtime_tools, theme_for_props,
                registry_state, stage_summary, remotion_temp_root, remotion_port,
                render_hash, staged_public_root, window_argument, alpha,
                frame_output_dir, pcm_aac_mp4, cast(Path, cli_video),
            )
        finally:
            props_path.unlink(missing_ok=True)
            # The external owner has finished consuming the staged request
            # before it replies. Always remove invocation-scoped media after
            # the response; retaining it would leak one public root per task.
            shutil.rmtree(staged_public_root, ignore_errors=True)

