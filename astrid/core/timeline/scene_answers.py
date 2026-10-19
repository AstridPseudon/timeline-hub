"""Read-only batches against the admitted Composition public scene evaluator."""

from __future__ import annotations

import json
import math
import os
import subprocess
import sys
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
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
    return _run_query({**payload, "frames": requested}, expected_count=len(requested),
                      expected_frames=requested)


def _run_query(payload: dict[str, Any], *, expected_count: int,
               expected_frames: list[int] | None = None) -> list[dict[str, Any]]:
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
        if (not isinstance(answers, list) or len(answers) != expected_count
                or any(not isinstance(answer, dict) for answer in answers)
                or (expected_frames is not None
                    and any(answer.get("frame") != frame
                           for answer, frame in zip(answers, expected_frames)))):
            raise SceneQueryUnavailable("invalid scene query response")
        return answers
    except (OSError, ValueError, TypeError, subprocess.SubprocessError, RemotionValidationError) as exc:
        raise SceneQueryUnavailable(f"scene evaluation unavailable: {exc}") from exc


def _occlusion_inputs(answers: Iterable[Mapping[str, Any]],
                      targets: Iterable[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if not isinstance(answers, (list, tuple)):
        raise SceneQueryUnavailable("invalid occlusion answers: expected an ordered list")
    if not isinstance(targets, (list, tuple)):
        raise SceneQueryUnavailable("invalid occlusion targets: expected an ordered list")

    answer_rows: list[dict[str, Any]] = []
    answer_frames: set[int] = set()
    for index, answer in enumerate(answers):
        if not isinstance(answer, Mapping):
            raise SceneQueryUnavailable(f"invalid occlusion answer at index {index}: expected an object")
        frame = answer.get("frame")
        if isinstance(frame, bool) or not isinstance(frame, int) or not (0 <= frame <= 2**53 - 1):
            raise SceneQueryUnavailable(f"invalid occlusion answer frame at index {index}: expected a nonnegative safe integer")
        if frame in answer_frames:
            raise SceneQueryUnavailable(f"duplicate occlusion answer frame: {frame}")
        answer_frames.add(frame)
        answer_rows.append(dict(answer))

    target_rows: list[dict[str, Any]] = []
    seen_targets: set[tuple[int, str, float]] = set()
    for index, target in enumerate(targets):
        if not isinstance(target, Mapping):
            raise SceneQueryUnavailable(f"invalid occlusion target at index {index}: expected an object")
        frame = target.get("frame")
        if isinstance(frame, bool) or not isinstance(frame, int) or not (0 <= frame <= 2**53 - 1):
            raise SceneQueryUnavailable(f"invalid occlusion target frame at index {index}: expected a nonnegative safe integer")
        clip_id = target.get("clip_id")
        if not isinstance(clip_id, str) or not clip_id:
            raise SceneQueryUnavailable(f"invalid occlusion target clip_id at index {index}: expected a nonempty string")
        minimum_fraction = target.get("min_fraction")
        if (isinstance(minimum_fraction, bool) or not isinstance(minimum_fraction, (int, float))
                or not 0 < minimum_fraction <= 1 or not math.isfinite(minimum_fraction)):
            raise SceneQueryUnavailable(
                f"invalid occlusion target min_fraction at index {index}: expected a finite number in (0, 1]")
        row = {"frame": frame, "clip_id": clip_id, "min_fraction": minimum_fraction}
        identity = (frame, clip_id, float(minimum_fraction))
        if identity in seen_targets:
            raise SceneQueryUnavailable(f"duplicate occlusion target at index {index}: {row}")
        seen_targets.add(identity)
        target_rows.append(row)
    return answer_rows, target_rows


def occlusions_from_frames(answers: Iterable[Mapping[str, Any]],
                           targets: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Query public occlusion facts from already-produced public SceneFrames.

    The evaluator is not prepared again: the installed public helper receives
    only the serialized frame answers and ordered targets. A target whose frame
    is absent is an explicit unavailable result, not a known empty occlusion.
    """
    answer_rows, target_rows = _occlusion_inputs(answers, targets)
    return _run_query({"query": "occlusion", "answers": answer_rows, "targets": target_rows},
                      expected_count=len(target_rows))


@dataclass(frozen=True)
class Span:
    start_frame: int
    end_frame: int
    cls: str
    content: str | None
    clips: tuple[str, ...]
    findings: tuple[str, ...] = ()


def host_frames_at(props: Mapping[str, Any], basis: Mapping[str, Any],
                   frames: Iterable[int]) -> list[dict[str, Any]]:
    """Prepare exact Root props with the admitted host's complete element maps.

    The caller retains the loaded revision, registry and runtime-resolved theme.
    Missing inputs are unavailable, never an empty registry or a config theme slug.
    """
    from astrid.core.timeline.scene_roles import element_coverage, role_of

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
    declarations = element_coverage({c.get("clipType", "") for c in clips})
    roles = {c["id"]: role_of(c, c.get("track"), declarations) for c in clips}
    return _query({"props": dict(props), "basis": dict(basis), "roles": roles}, frames)


def coverage(props: Mapping[str, Any], basis: Mapping[str, Any], *,
             start_frame: int, end_frame: int) -> list[Span]:
    """Run-length encode one batch of public frame answers, including UNKNOWN."""
    return spans_from_frames(host_frames_at(props, basis, range(start_frame, end_frame)))


def spans_from_frames(answers: Iterable[Mapping[str, Any]]) -> list[Span]:
    spans: list[Span] = []
    for answer in answers:
        frame = answer["frame"]
        cls, content = answer["coverage"], answer["content"]
        clips = tuple(layer["clipId"] for layer in answer["layers"] if layer["visible"] is not False)
        findings = tuple(dict.fromkeys(f["code"] for f in answer["findings"]))
        if (spans and (spans[-1].cls, spans[-1].content, spans[-1].clips, spans[-1].findings)
                == (cls, content, clips, findings)):
            previous = spans[-1]
            spans[-1] = Span(previous.start_frame, frame + 1, cls, content, clips, findings)
        else:
            spans.append(Span(frame, frame + 1, cls, content, clips, findings))
    return spans
