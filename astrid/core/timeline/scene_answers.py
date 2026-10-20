"""Low-level public scene transport; input shape is not render-source authority."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from collections.abc import Iterable, Mapping
from typing import Any


def remotion_runtime_status(*args, **kwargs):
    """Resolve renderer admission only when a native scene query is requested."""
    from astrid.core.rendering.remotion_runtime import remotion_runtime_status as _status

    return _status(*args, **kwargs)


def probe_context(*args, **kwargs):
    """Resolve renderer environment probing only when a native scene query is requested."""
    from astrid.core.rendering.remotion_runtime import probe_context as _probe

    return _probe(*args, **kwargs)


class SceneQueryUnavailable(RuntimeError):
    """No scene answer was obtained; this is different from an empty scene."""


def frames_at(scene: Mapping[str, Any], frames: Iterable[int]) -> list[dict[str, Any]]:
    """Query resolved visual ``SceneTrackInput`` records, never authored timelines.

    ``scene`` contains tracks, assets, fps, width and height, with optional roles
    and element IDs. The host supplies bottom-to-top painter order, clips sorted
    by at, and one resolved Composition TransitionSpec (or null) per adjacent
    pair, as in prepareCompositionScene. Compiled clips/IDs pass through intact.
    No component capabilities, modifier declarations or media alpha evidence are
    synthesized here. Canonical UNKNOWN findings pass through unchanged.
    """
    return _query({"scene": dict(scene)}, frames)


def _query(payload: dict[str, Any], frames: Iterable[int]) -> list[dict[str, Any]]:
    requested = list(frames)
    payload = {**payload, "frames": requested}
    try:
        from astrid.core.rendering.remotion_runtime import RemotionValidationError
    except ImportError as exc:
        raise SceneQueryUnavailable(f"scene evaluation unavailable: {exc}") from exc

    try:
        runtime = remotion_runtime_status(require_explicit_project=True)
        if not runtime.available or runtime.project_dir is None or runtime.node_executable is None:
            raise SceneQueryUnavailable(runtime.reason or "scene runtime unavailable")
        helper = (runtime.project_dir / "scene-query.mjs").resolve(strict=True)
        helper.relative_to(runtime.project_dir.resolve())
        if not helper.is_file():
            raise SceneQueryUnavailable("scene query helper is not a file")
        if "props" in payload:
            for name in ("native-scene.mjs", "src/host-scene.ts"):
                entry = (runtime.project_dir / name).resolve(strict=True)
                entry.relative_to(runtime.project_dir.resolve())
                if not entry.is_file():
                    raise SceneQueryUnavailable(f"scene host entry is not a file: {name}")
        environment = probe_context(environment=os.environ, python_executable=sys.executable)["node_env"]
        # Status validated this selector as part of the renderer's registry
        # context. The alias resolver must see that same admitted pack set.
        if "ASTRID_PACKS_PATH" in os.environ:
            environment["ASTRID_PACKS_PATH"] = os.environ["ASTRID_PACKS_PATH"]
        result = subprocess.run(
            [str(runtime.node_executable), str(helper), str(runtime.project_dir)],
            input=json.dumps(payload, allow_nan=False),
            cwd=runtime.project_dir, env=environment, capture_output=True, text=True, timeout=30,
        )
        if result.returncode:
            raise SceneQueryUnavailable(result.stderr.strip() or "scene query failed")
        answers = json.loads(result.stdout)
        if (not isinstance(answers, list) or len(answers) != len(requested)
                or any(not isinstance(answer, dict) for answer in answers)
                or any(type(answer.get("frame")) is not int or answer["frame"] != frame
                       for answer, frame in zip(answers, requested))):
            raise SceneQueryUnavailable("invalid scene query response")
        return answers
    except (OSError, ValueError, TypeError, subprocess.SubprocessError, RemotionValidationError) as exc:
        raise SceneQueryUnavailable(f"scene evaluation unavailable: {exc}") from exc


def host_frames_at(props: Mapping[str, Any], basis: Mapping[str, Any],
                   frames: Iterable[int]) -> list[dict[str, Any]]:
    """Evaluate supplied Root props with the selected host's complete element maps.

    Shape checks do not certify a revision, candidate, assets or theme. The source
    owner must retain the exact prepared inputs and occurrence identity before
    using these answers in a check or capture. No production caller is activated
    here. Missing inputs are unavailable, never a guessed registry or theme.
    """
    from astrid.core.timeline.onscreen import element_coverage, role_of

    timeline = props.get("timeline")
    if (not isinstance(timeline, Mapping) or not isinstance(timeline.get("tracks"), list)
            or not isinstance(timeline.get("clips"), list)
            or not isinstance(props.get("assets"), Mapping)
            or not isinstance(props["assets"].get("assets"), Mapping)
            or not isinstance(props.get("theme"), Mapping)
            or not isinstance(props["theme"].get("visual"), Mapping)):
        raise SceneQueryUnavailable("exact Root timeline, assets registry and resolved runtime theme required")
    clips = timeline["clips"]
    if any(not isinstance(c, Mapping) or not isinstance(c.get("id"), str) for c in clips):
        raise SceneQueryUnavailable("scene requires compiled clips with their exact IDs")
    # Reuse current role declarations only; no private visibility math.
    declarations = element_coverage({c.get("clipType", "") for c in clips})
    roles = {c["id"]: role_of(c, c.get("track"), declarations) for c in clips}
    return _query({"props": dict(props), "basis": dict(basis), "roles": roles}, frames)
