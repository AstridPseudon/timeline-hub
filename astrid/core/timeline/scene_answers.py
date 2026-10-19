"""Read-only batches against the admitted Composition public scene evaluator."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from collections.abc import Iterable, Mapping
from typing import Any

from astrid.core.rendering.remotion_runtime import (
    RemotionValidationError,
    probe_context,
    remotion_runtime_status,
)


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
    try:
        runtime = remotion_runtime_status(require_explicit_project=True)
        if not runtime.available or runtime.project_dir is None or runtime.node_executable is None:
            raise SceneQueryUnavailable(runtime.reason or "scene runtime unavailable")
        helper = (runtime.project_dir / "scene-query.mjs").resolve(strict=True)
        helper.relative_to(runtime.project_dir.resolve())
        if not helper.is_file():
            raise SceneQueryUnavailable("scene query helper is not a file")
        requested = list(frames)
        environment = probe_context(environment=os.environ, python_executable=sys.executable)["node_env"]
        result = subprocess.run(
            [str(runtime.node_executable), str(helper), str(runtime.project_dir)],
            input=json.dumps({"scene": dict(scene), "frames": requested}, allow_nan=False),
            cwd=runtime.project_dir, env=environment, capture_output=True, text=True, timeout=30,
        )
        if result.returncode:
            raise SceneQueryUnavailable(result.stderr.strip() or "scene query failed")
        answers = json.loads(result.stdout)
        if (not isinstance(answers, list) or len(answers) != len(requested)
                or any(not isinstance(answer, dict) or answer.get("frame") != frame
                       for answer, frame in zip(answers, requested))):
            raise SceneQueryUnavailable("invalid scene query response")
        return answers
    except (OSError, ValueError, TypeError, subprocess.SubprocessError, RemotionValidationError) as exc:
        raise SceneQueryUnavailable(f"scene evaluation unavailable: {exc}") from exc
