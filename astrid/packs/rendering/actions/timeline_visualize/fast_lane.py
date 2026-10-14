"""Bounded pixel verification through Runtime-owned V3 render and filmstrip actions.

The planner is pure. A capture uses the existing managed candidate-preview and
``rendering.timeline_visualize`` routes, then compares frames decoded from the
admitted managed videos. This module does not own a renderer or a second
timeline authority.
"""
from __future__ import annotations

import hashlib
import json
import math
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

FAST_ROOT = Path(tempfile.gettempdir()) / "astrid-v3-fast-lane"
MAX_MOMENTS = 4
_FFMPEG_TIMEOUT_S = 240


class FastLaneError(RuntimeError):
    """The bounded managed capture cannot proceed; the message gives the cause."""


@dataclass(frozen=True)
class Moment:
    t: float
    label: str
    clip: str | None = None


def frame_of(t: float, fps: float) -> int:
    """Map a timeline moment to its decoded frame using the editor's epsilon."""
    return max(0, int(math.floor(float(t) * float(fps) + 0.02)))


def moments_from_changes(
    changes: Iterable[Mapping[str, Any]], fps: float, *, limit: int = MAX_MOMENTS,
    names: Mapping[str, str] | None = None,
) -> list[Moment]:
    """Choose frames that expose added, removed, moved, or restyled clips."""
    if not math.isfinite(float(fps)) or float(fps) <= 0:
        raise ValueError("fps must be a positive finite number")
    if type(limit) is not int or limit < 0:
        raise ValueError("limit must be a non-negative integer")
    found: list[Moment] = []
    step = 1.0 / float(fps)
    for change in changes:
        raw = str(change.get("clip_id") or "?")
        short = raw.rsplit(":", 1)[-1]
        name = (names or {}).get(raw) or (names or {}).get(short) or short
        before, after = change.get("before"), change.get("after")
        fields = set(change.get("fields") or ())
        if after is None and before is not None:
            found.append(Moment(float(before[0]), f"{name} removed (was from {before[0]:.2f} s)", raw))
            continue
        if after is None:
            continue
        start, end = float(after[0]), float(after[1])
        if before is None or "start" in fields:
            found.extend((
                Moment(start - step, f"{name}: the frame before it starts", raw),
                Moment(start, f"{name} starts", raw),
            ))
        if before is not None and "end" in fields:
            found.extend((
                Moment(end - step, f"{name}: its last frame", raw),
                Moment(end, f"{name}: the first frame without it", raw),
            ))
        if before is not None and not fields & {"start", "end"}:
            found.append(Moment((start + end) / 2, f"{name} ({', '.join(sorted(fields)) or 'changed'}) mid-clip", raw))
    unique: dict[int, Moment] = {}
    for moment in found:
        if moment.t >= 0:
            unique.setdefault(frame_of(moment.t, fps), moment)
    return [unique[frame] for frame in sorted(unique)][:limit]


def _base_revision(draft: Any) -> str:
    bundle = getattr(draft, "bundle", None)
    parent = bundle.get("base_parent") if isinstance(bundle, Mapping) else None
    if not isinstance(parent, Mapping):
        raise FastLaneError("pixel verification needs the checkout's exact base parent revision")
    revision = parent.get("revision_id") or parent.get("parent_revision_id") or parent.get("head_revision_id")
    if not isinstance(revision, str) or not revision:
        raise FastLaneError("pixel verification needs the checkout's exact base parent revision")
    return revision


def _require_clean_base_render(client: Any, run_id: str, draft: Any) -> dict[str, Any]:
    """Verification supports normal BASE renders with matching authored canvas."""
    shown = client.runs.show(run_id)
    run = shown.data if getattr(shown, "ok", None) is True else None
    if not isinstance(run, Mapping) or (run.get("run_id") or run.get("id")) != run_id or run.get("status") != "completed":
        raise FastLaneError("verification BASE needs its exact completed managed render")
    task_ids = run.get("task_ids")
    if not isinstance(task_ids, list) or len(task_ids) != 1 or not isinstance(task_ids[0], str):
        raise FastLaneError("verification BASE needs one exact original render task")
    observed = client.tasks.show(task_ids[0])
    task = observed.data if getattr(observed, "ok", None) is True else None
    if (not isinstance(task, Mapping) or task.get("task_id") != task_ids[0]
            or task.get("run_id") != run_id or task.get("state") != "succeeded"
            or task.get("capability_id") != "rendering.render"):
        raise FastLaneError("verification BASE needs its successful original render task")
    envelope = task.get("spec")
    spec = envelope.get("spec") if isinstance(envelope, Mapping) else None
    inputs = spec.get("inputs") if isinstance(spec, Mapping) else None
    if not isinstance(inputs, Mapping):
        raise FastLaneError("verification BASE render input envelope is unavailable")
    if inputs.get("review", False) is not False or inputs.get("profile") is not None:
        raise FastLaneError("verification BASE must be a normal non-review render without a custom profile")
    snapshot = inputs.get("timeline_snapshot")
    config = snapshot.get("config") if isinstance(snapshot, Mapping) else None
    if not isinstance(config, Mapping):
        raise FastLaneError("verification BASE frozen canvas is unavailable")
    candidate = draft.document()
    parent = candidate.get("parent") if isinstance(candidate, Mapping) else None
    working_config = parent.get("config") if isinstance(parent, Mapping) else None
    if not isinstance(working_config, Mapping):
        raise FastLaneError("verification WORKING frozen canvas is unavailable")
    def canvas(value: Mapping[str, Any]) -> Any:
        theme = value.get("theme_overrides", {})
        visual = theme.get("visual", {}) if isinstance(theme, Mapping) else {}
        return visual.get("canvas", {}) if isinstance(visual, Mapping) else {}
    base_canvas, working_canvas = canvas(config), canvas(working_config)
    if not isinstance(base_canvas, Mapping) or not isinstance(working_canvas, Mapping) or dict(base_canvas) != dict(working_canvas):
        raise FastLaneError("verification BASE and WORKING must have the same frozen canvas dimensions and frame rate")
    return dict(base_canvas)


def prepare_pair(client: Any, project: str, timeline: str, draft: Any, *, media_root: Path) -> dict[str, Any]:
    """Pin the base render and freeze/render the working candidate through V3."""
    from astrid.sdk.authoring_bundle import render_authoring_candidate_preview
    from astrid.sdk.timeline_filmstrip import prepare_filmstrip

    remote = getattr(client, "_remote", client)
    base = prepare_filmstrip(
        {"timeline_slug": timeline, "revision_id": _base_revision(draft),
         "composed_capture": True, "include_media": True, "show": ["output"]},
        project=project, client=remote,
    )
    base_run = base.get("render_run_id")
    if not isinstance(base_run, str) or not base_run:
        raise FastLaneError("no exact managed render is available for the checkout's base revision")
    _require_clean_base_render(client, base_run, draft)

    # Resolve the exact managed BASE video without executing a frame capture.
    # The initial composed authority above only selects the saved BASE revision.
    base_authority = prepare_filmstrip(
        {"timeline_slug": timeline, "render_run": base_run, "show": ["output"], "include_media": True},
        project=project, client=remote,
    )
    base_snapshot = base_authority.get("filmstrip_snapshot")
    base_video, base_media = _base_video(base_authority, client=client, project=project,
                                         run_id=base_run, media_root=media_root)

    candidate = render_authoring_candidate_preview(
        draft.document(), client, project=project, timeline_ref=timeline, wait=True, review=False,
    )
    if getattr(candidate, "ok", None) is not True:
        error = getattr(candidate, "error", None)
        raise FastLaneError(f"candidate preview failed: {error or 'managed render did not succeed'}")
    working_run = getattr(candidate, "run_id", None)
    if not isinstance(working_run, str) or not working_run:
        raise FastLaneError("candidate preview returned no managed render identity")

    working_authority = prepare_filmstrip(
        {"timeline_slug": timeline, "render_run": working_run, "show": ["output"], "include_media": True},
        project=project, client=remote,
    )
    working_snapshot = working_authority.get("filmstrip_snapshot")
    working_video, working_media = _candidate_video(candidate, working_authority, client=client, project=project, media_root=media_root)
    if not isinstance(base_snapshot, Mapping) or not isinstance(working_snapshot, Mapping):
        raise FastLaneError("the exact managed renders did not yield filmstrip snapshots")
    return {"base_run": base_run, "working_run": working_run,
            "base_snapshot": base_snapshot, "working_snapshot": working_snapshot,
            "base_video": base_video, "base_media": base_media,
            "working_video": working_video, "working_media": working_media}


def _base_video(authority: Mapping[str, Any], *, client: Any, project: str,
                run_id: str, media_root: Path) -> tuple[Path, dict[str, Any]]:
    """Materialize the exact admitted saved BASE render, without Chrome capture."""
    snapshot = authority.get("filmstrip_snapshot")
    if (authority.get("render_run_id") != run_id or not isinstance(snapshot, Mapping)
            or snapshot.get("render_run_id") != run_id
            or (snapshot.get("metadata") or {}).get("selection") not in
                {"explicit_current_render", "explicit_historical_render"}
            or authority.get("include_media") is not True):
        raise FastLaneError("BASE media is not an admitted exact saved render")
    expected = str(authority.get("video_digest") or "").removeprefix("sha256:")
    if (len(expected) != 64 or any(char not in "0123456789abcdef" for char in expected)
            or snapshot.get("video_digest") != authority.get("video_digest")):
        raise FastLaneError("BASE managed-video digest authority is invalid")
    observed = (client.runs.show(run_id), client.projects.show(project))
    if any(getattr(value, "ok", None) is not True or not isinstance(getattr(value, "data", None), Mapping)
           for value in observed):
        raise FastLaneError("BASE original run or project is unavailable")
    run, project_row = (value.data for value in observed)
    project_id = project_row.get("project_id") or project_row.get("id")
    task_ids = run.get("task_ids")
    if (not project_id or authority.get("project_id") != project_id
            or (run.get("run_id") or run.get("id")) != run_id or run.get("project_id") != project_id
            or run.get("status") != "completed" or not isinstance(task_ids, list)
            or len(task_ids) != 1 or not isinstance(task_ids[0], str)):
        raise FastLaneError("BASE media does not belong to its exact original render and project")
    observed_task = client.tasks.show(task_ids[0])
    task = observed_task.data if getattr(observed_task, "ok", None) is True else None
    if (not isinstance(task, Mapping) or (task.get("task_id") or task.get("id")) != task_ids[0]
            or task.get("run_id") != run_id or task.get("state") != "succeeded"
            or task.get("capability_id") != "rendering.render"):
        raise FastLaneError("BASE media has no successful exact original render task")
    result = task.get("result")
    outputs = result.get("outputs") if isinstance(result, Mapping) else None
    videos = [output for output in (outputs if isinstance(outputs, list) else [])
              if isinstance(output, Mapping)
              and (output.get("name") or output.get("output_port") or output.get("port")) == "video"]
    if len(videos) != 1 or str(videos[0].get("digest") or "").removeprefix("sha256:") != expected:
        raise FastLaneError("BASE media digest does not identify its original task video")
    object_id = authority.get("video_object_id")
    read_bytes = getattr(getattr(client, "media", None), "read_bytes", None)
    if not isinstance(object_id, str) or not object_id or not callable(read_bytes):
        raise FastLaneError("BASE media has no admitted object byte materialization route")
    data = read_bytes(object_id)
    if not isinstance(data, bytes) or hashlib.sha256(data).hexdigest() != expected:
        raise FastLaneError("original BASE video does not match its admitted managed digest")
    owned = Path(tempfile.mkdtemp(prefix="astrid-base-render-", dir=media_root))
    video = owned / "video.mp4"
    try:
        with video.open("xb") as stream:
            stream.write(data)
        with video.open("rb") as stream:
            if hashlib.file_digest(stream, "sha256").hexdigest() != expected:
                raise FastLaneError("materialized BASE video changed before decoding")
    except BaseException:
        shutil.rmtree(owned)
        raise
    return video, {"render_run_id": run_id, "digest": "sha256:" + expected,
                   "selection": (snapshot.get("metadata") or {})["selection"], "verified": True}


def _candidate_video(candidate: Any, authority: Mapping[str, Any], *, client: Any, project: str, media_root: Path) -> tuple[Path, dict[str, Any]]:
    """Check the original managed preview artifact without saved-parent capture."""
    run_id = getattr(candidate, "run_id", None)
    snapshot = authority.get("filmstrip_snapshot")
    if (not isinstance(run_id, str) or not run_id
            or authority.get("render_run_id") != run_id
            or not isinstance(snapshot, Mapping) or snapshot.get("render_run_id") != run_id):
        raise FastLaneError("candidate media authority does not identify the exact managed preview")
    if (snapshot.get("metadata") or {}).get("selection") != "explicit_candidate_preview":
        raise FastLaneError("working media is not an admitted explicit candidate preview")
    expected = str(authority.get("video_digest") or "").removeprefix("sha256:")
    if (len(expected) != 64 or any(char not in "0123456789abcdef" for char in expected)
            or snapshot.get("video_digest") != authority.get("video_digest")):
        raise FastLaneError("candidate managed-video digest authority is invalid")
    # InvocationResult carries durable output identities, not local video paths.
    # Revalidate the original task in the exact successful, frozen preview run.
    task_id = getattr(candidate, "kernel_task_id", None)
    if (getattr(candidate, "ok", None) is not True
            or getattr(candidate, "kernel_run_id", None) != run_id
            or not isinstance(task_id, str) or not task_id):
        raise FastLaneError("candidate preview has no exact original kernel run and task")
    observed = (client.runs.show(run_id), client.tasks.show(task_id), client.projects.show(project))
    if any(getattr(result, "ok", None) is not True or not isinstance(getattr(result, "data", None), Mapping)
           for result in observed):
        raise FastLaneError("candidate original run, task or project is unavailable")
    run, task, project_row = (result.data for result in observed)
    project_id = project_row.get("project_id") or project_row.get("id")
    if (not project_id or authority.get("project_id") != project_id
            or (run.get("id") or run.get("run_id")) != run_id
            or run.get("project_id") != project_id
            or task_id not in (run.get("task_ids") or [])
            or (task.get("task_id") or task.get("id")) != task_id
            or run.get("status") != "completed"
            or (task.get("state") or task.get("status")) != "succeeded"
            or authority.get("include_media") is not True):
        raise FastLaneError("candidate media does not belong to its successful original task and project")
    object_id = authority.get("video_object_id")
    if not isinstance(object_id, str) or not object_id:
        raise FastLaneError("candidate preview returned no admitted managed video reference")
    read_bytes = getattr(getattr(client, "media", None), "read_bytes", None)
    if not callable(read_bytes):
        raise FastLaneError("the connected SDK client has no object byte materialization route")
    data = read_bytes(object_id)
    if not isinstance(data, bytes) or hashlib.sha256(data).hexdigest() != expected:
        raise FastLaneError("original candidate video does not match its admitted managed digest")
    # Materialize only to a new owned directory; rehash before decoding.
    owned = Path(tempfile.mkdtemp(prefix="astrid-working-preview-", dir=media_root))
    video = owned / "video.mp4"
    try:
        with video.open("xb") as stream:
            stream.write(data)
        with video.open("rb") as stream:
            if hashlib.file_digest(stream, "sha256").hexdigest() != expected:
                raise FastLaneError("materialized candidate video changed before decoding")
    except BaseException:
        shutil.rmtree(owned)
        raise
    return video, {"render_run_id": run_id, "digest": "sha256:" + expected,
                   "selection": "explicit_candidate_preview", "verified": True}


def _invoke_video(client: Any, project: str, timeline: str, run_id: str, frame: int) -> Path:
    """Ask the existing V3 filmstrip action for the exact managed video and frame."""
    visualize = getattr(getattr(client, "timelines", None), "visualize", None)
    if not callable(visualize):
        raise FastLaneError("the connected SDK client has no canonical timeline visualization route")
    result = visualize(
        project, timeline, mode="composed", formats=("png",),
        options={"render_run": run_id, "view": "filmstrip",
                 "show": ["output"], "frame": int(frame), "include_media": True},
    )
    if getattr(result, "ok", None) is not True:
        error = getattr(result, "error", None)
        raise FastLaneError(f"managed filmstrip for render {run_id} failed: {error or 'invocation failed'}")
    outputs = getattr(result, "outputs", None)
    media = outputs.get("media") if isinstance(outputs, Mapping) else None
    if not isinstance(media, str) or not Path(media).is_file():
        raise FastLaneError(f"managed filmstrip for render {run_id} returned no verified video attachment")
    index_path = outputs.get("frame_index") if isinstance(outputs, Mapping) else None
    if not isinstance(index_path, str) or not Path(index_path).is_file():
        raise FastLaneError(f"managed filmstrip for render {run_id} returned no frame-index receipt")
    try:
        index = json.loads(Path(index_path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise FastLaneError("managed filmstrip frame-index receipt is unreadable") from exc
    # Capture provenance identifies composition frames; managed media has its own exact run.
    media_record = index.get("media") if isinstance(index, Mapping) else None
    if not isinstance(media_record, Mapping) or str(media_record.get("render_run_id")) != run_id:
        raise FastLaneError("filmstrip frame-index does not identify the requested managed render")
    if not isinstance(media_record, Mapping) or media_record.get("verified") is not True:
        raise FastLaneError("filmstrip frame-index does not attest its managed video attachment")
    expected = str(media_record.get("digest") or "").removeprefix("sha256:")
    if len(expected) != 64 or any(ch not in "0123456789abcdef" for ch in expected):
        raise FastLaneError("filmstrip managed-video digest is invalid")
    with Path(media).open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    if digest != expected:
        raise FastLaneError("materialized managed video does not match its filmstrip digest")
    return Path(media)


def decode_frames(video: Path, frames: Sequence[int], out_dir: Path) -> dict[int, Path]:
    """Decode selected full-resolution PNG frames from a verified managed video."""
    unique = sorted({int(frame) for frame in frames})
    if not unique:
        return {}
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise FastLaneError("ffmpeg is required to compare decoded managed-render pixels")
    if any(frame < 0 for frame in unique):
        raise FastLaneError("frame numbers must be non-negative")
    out_dir.mkdir(parents=True, exist_ok=True)
    expression = "+".join(f"eq(n\\,{frame})" for frame in unique)
    pattern = out_dir / "frame-%05d.png"
    command = [ffmpeg, "-v", "error", "-i", str(video), "-vf", f"select={expression}",
               "-fps_mode:v", "passthrough", "-frames:v", str(len(unique)), "-y", str(pattern)]
    try:
        completed = subprocess.run(command, capture_output=True, text=True, timeout=_FFMPEG_TIMEOUT_S, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise FastLaneError(f"ffmpeg could not decode managed video frames: {exc}") from exc
    if completed.returncode != 0:
        detail = (completed.stderr or "ffmpeg failed").strip().splitlines()
        raise FastLaneError(f"ffmpeg could not decode managed video frames: {detail[-1] if detail else 'unknown error'}")
    paths = sorted(out_dir.glob("frame-*.png"))
    if len(paths) != len(unique):
        raise FastLaneError(f"managed video yielded {len(paths)} of {len(unique)} requested decoded frames")
    try:
        from PIL import Image

        for path in paths:
            with Image.open(path) as image:
                image.verify()
    except Exception as exc:  # PIL reports several decode exception types
        raise FastLaneError(f"a decoded managed frame is not a valid PNG: {exc}") from exc
    return dict(zip(unique, paths))


def difference(a: Path, b: Path) -> tuple[float, int, tuple[int, int, int, int] | None, tuple[int, int]]:
    """Return the fraction, count, bounds, and size of pixels that differ."""
    from PIL import Image, ImageChops

    with Image.open(a) as left, Image.open(b) as right:
        left, right = left.convert("RGB"), right.convert("RGB")
        if left.size != right.size:
            raise FastLaneError(f"managed renders have different decoded sizes: {left.size} and {right.size}")
        delta = ImageChops.difference(left, right).convert("L").point(lambda value: 255 if value > 8 else 0)
        box, count, size = delta.getbbox(), delta.histogram()[255], left.size
    return count / float(size[0] * size[1]), count, box, size


def _parse_region(value: Sequence[int] | str | None) -> tuple[int, int, int, int] | None:
    if value is None:
        return None
    try:
        if isinstance(value, str):
            x, y, width, height = (int(round(float(part))) for part in value.split(","))
        else:
            x, y, width, height = (int(part) for part in value)
    except (TypeError, ValueError) as exc:
        raise FastLaneError("region must be x,y,width,height in canvas pixels") from exc
    if width <= 0 or height <= 0:
        raise FastLaneError("region width and height must be positive")
    return x, y, x + width, y + height


def zoom_region(snapshots: Sequence[Mapping[str, Any]], address: str, t: float, fps: float,
                canvas: tuple[int, int]) -> tuple[int, int, int, int] | None:
    """Find a padded V3 motion-box union for the requested layer on the sampled frame."""
    from astrid.core.timeline.astrid_ns import read_app
    from astrid.packs.rendering.actions.timeline_visualize.motion import model
    from astrid.packs.rendering.actions.timeline_visualize.motion.sheet import snapshot_elements

    rects: list[tuple[float, float, float, float]] = []
    for snapshot in snapshots:
        _occurrences, elements = snapshot_elements(snapshot)
        for element in elements:
            app = read_app(element.clip)
            target = f"{app.get('cut')}.{app.get('layer')}"
            if target != address.strip() and element.short_id != address.strip() and not str(element.id).endswith(address.strip()):
                continue
            boxes = [box.rect for box in model.boxes_at(element, t + 1e-6, fps)]
            anchor = element.params.get("anchor") if isinstance(element.params.get("anchor"), Mapping) else None
            if boxes and anchor and all(isinstance(anchor.get(key), (int, float)) for key in ("x", "y")):
                boxes.append((anchor["x"], anchor["y"], anchor["x"] + 1, anchor["y"] + 1))
            rects.extend(boxes)
    if not rects:
        return None
    x0, y0 = min(rect[0] for rect in rects), min(rect[1] for rect in rects)
    x1, y1 = max(rect[2] for rect in rects), max(rect[3] for rect in rects)
    width, height = max(x1 - x0, 1.0), max(y1 - y0, 1.0)
    grow_x, grow_y = max(width * 0.25, (160 - width) / 2), max(height * 0.25, (160 - height) / 2)
    return (max(0, int(x0 - grow_x)), max(0, int(y0 - grow_y)),
            min(canvas[0], int(math.ceil(x1 + grow_x))), min(canvas[1], int(math.ceil(y1 + grow_y))))


def _crop(path: Path, box: tuple[int, int, int, int], out: Path) -> Path:
    from PIL import Image

    with Image.open(path) as image:
        image.convert("RGB").crop(box).save(out)
    return out


def _canvas(snapshot: Mapping[str, Any]) -> tuple[int, int]:
    config = snapshot.get("config") if isinstance(snapshot.get("config"), Mapping) else {}
    canvas = (((config.get("theme_overrides") or {}).get("visual") or {}).get("canvas") or {})
    try:
        return int(canvas.get("width") or 1920), int(canvas.get("height") or 1080)
    except (TypeError, ValueError):
        return 1920, 1080


def _canvas_bounds(box: tuple[int, int, int, int] | None, size: tuple[int, int],
                   canvas: tuple[int, int], *,
                   offset: tuple[int, int] = (0, 0)) -> tuple[int, int, int, int] | None:
    """Map a raw decoded-frame rectangle to authored canvas coordinates."""
    if box is None:
        return None
    sx, sy = (1.0, 1.0) if offset != (0, 0) else (canvas[0] / float(size[0]), canvas[1] / float(size[1]))
    x0, y0 = round(offset[0] + box[0] * sx), round(offset[1] + box[1] * sy)
    x1, y1 = round(offset[0] + box[2] * sx), round(offset[1] + box[3] * sy)
    return x0, y0, x1, y1


def _pixel_line(share: float, count: int, box: tuple[int, int, int, int] | None,
                size: tuple[int, int], canvas: tuple[int, int], *,
                offset: tuple[int, int] = (0, 0)) -> str:
    if box is None:
        return "pixels: identical to published"
    amount = f"{share * 100:.2f}%" if share >= 0.001 else f"<0.1% ({count} px)"
    canvas_bounds = _canvas_bounds(box, size, canvas, offset=offset)
    if canvas_bounds is None:
        return "pixels: identical to published"
    x0, y0, x1, y1 = canvas_bounds
    return f"pixels: {amount} differ, changed area {x0},{y0}–{x1},{y1} canvas px"


def _compose_page(rows: Sequence[Mapping[str, Any]], path: Path, *, title: str,
                  footer: Sequence[str] = ()) -> Path:
    from PIL import Image, ImageDraw

    tile = (640, 360)
    margin, gap, row_height = 16, 12, 402
    width = margin * 2 + 2 * tile[0] + gap
    height = 54 + max(1, len(rows)) * row_height + len(footer) * 20 + margin
    page = Image.new("RGB", (width, height), "#111827")
    draw = ImageDraw.Draw(page)
    draw.text((margin, 12), title, fill="white")
    draw.text((margin, 34), "published render  |  working candidate · decoded managed-video frames", fill="#9ca3af")
    top = 54
    for row in rows:
        for side, x in (("published", margin), ("working", margin + tile[0] + gap)):
            frame_path = Path(str(row.get(f"{side}_display") or row[side]))
            if frame_path.is_file():
                with Image.open(frame_path) as image:
                    page.paste(image.convert("RGB").resize(tile, Image.Resampling.LANCZOS), (x, top))
        draw.text((margin, top + tile[1] + 6),
                  f"{row['label']} · {float(row['t']):.3f}s · frame {row['frame']}", fill="white")
        draw.text((margin, top + tile[1] + 24), str(row["pixels"]), fill="#d1d5db")
        top += row_height
    for line in footer:
        draw.text((margin, top), str(line)[:180], fill="#d1d5db")
        top += 20
    path.parent.mkdir(parents=True, exist_ok=True)
    page.save(path)
    return path


def _labelled_tiles(
    snapshots: Mapping[str, Mapping[str, Any]], frame: int, fps: float,
    paths: Mapping[str, str | Path | None], out_dir: Path, index: int,
) -> dict[str, str]:
    """Create labeled display copies; retain the decoded files for pixel comparison."""
    from PIL import Image

    from .overlays.labels import overlay_labels_frame

    labelled: dict[str, str] = {}
    for side, path in paths.items():
        snapshot = snapshots.get(side)
        if not path or not isinstance(snapshot, Mapping):
            continue
        config = snapshot.get("config")
        if not isinstance(config, Mapping):
            continue
        with Image.open(path) as source:
            tile = source.convert("RGB")
        target = out_dir / f"labelled-{index}-{side}.png"
        overlay_labels_frame(tile, config, frame, fps).save(target)
        labelled[side] = str(target)
    return labelled


def _moment_label(moment: Moment) -> str:
    label = str(getattr(moment, "label", "") or "").strip()
    return label or f"{moment.t:.2f}"


def verify(
    client: Any, project: str, timeline: str, moments: Sequence[Moment], *, draft: Any = None,
    footer: Sequence[str] = (), resolution: Sequence[int] = (640, 360), root: Path | None = None,
    served: Mapping[str, Any] | None = None, zoom: str | None = None,
    region: Sequence[int] | str | None = None, labels: bool = False,
) -> dict[str, Any]:
    """Compare published and candidate pixels from their exact managed videos."""
    del resolution, served  # V3 compares native decoded frames; page scaling never affects the diff.
    if not moments:
        raise FastLaneError("no moment to verify")
    if draft is None:
        raise FastLaneError("pixel verification needs the checkout working copy")
    if zoom and region:
        raise FastLaneError("choose zoom or region, not both")
    root = root or FAST_ROOT
    root.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    run_dir = Path(tempfile.mkdtemp(prefix="verify-", dir=root))
    pair = None
    try:
        pair = prepare_pair(client, project, timeline, draft, media_root=run_dir)
        rational = pair["base_snapshot"].get("fps_rational", [30, 1])
        fps = float(Fraction(int(rational[0]), int(rational[1])))
        requested = list(moments)
        selected, skipped = requested[:MAX_MOMENTS], requested[MAX_MOMENTS:]
        frames = sorted({frame_of(moment.t, fps) for moment in selected})
        published_video = pair["base_video"]
        working_video = pair["working_video"]
        published = decode_frames(published_video, frames, run_dir / "published")
        working = decode_frames(working_video, frames, run_dir / "working")
        canvas = _canvas(pair["base_snapshot"])
        fixed_region = _parse_region(region)
        rows = []
        for index, moment in enumerate(selected):
            frame = frame_of(moment.t, fps)
            pub_path, work_path = published[frame], working[frame]
            crop = fixed_region or (zoom_region(
                (pair["base_snapshot"], pair["working_snapshot"]), zoom, moment.t, fps, canvas,
            ) if zoom else None)
            compare_pub, compare_work = pub_path, work_path
            if crop:
                compare_pub = _crop(pub_path, crop, run_dir / f"compare-{index}-published.png")
                compare_work = _crop(work_path, crop, run_dir / f"compare-{index}-working.png")
            share, count, box, size = difference(compare_pub, compare_work)
            offset = (crop[0], crop[1]) if crop else (0, 0)
            line = _pixel_line(share, count, box, size, canvas, offset=offset)
            if zoom and crop is None:
                line = f"zoom {zoom}: not on screen at this moment · {line}"
            row = {"t": moment.t, "frame": frame, "label": moment.label,
                         "published": str(pub_path), "working": str(work_path),
                         "pixels": line, "share": share, "different_pixels": count,
                         "bounds": box, "canvas_bounds": _canvas_bounds(box, size, canvas, offset=offset),
                         "size": size, "region": crop,
                         "verdict": f"published: frame {frame} · working copy: frame {frame} · {line}"}
            if labels:
                row["labelled"] = _labelled_tiles(
                    {"published": pair["base_snapshot"], "working": pair["working_snapshot"]},
                    frame, fps, {"published": pub_path, "working": work_path}, run_dir, index,
                )
                for side, labelled_path in row["labelled"].items():
                    row[f"{side}_display"] = labelled_path
            rows.append(row)
        page = _compose_page(rows, run_dir / "verify.png", title=f"verify {timeline} · {len(rows)} moment(s)", footer=footer)
        notes: list[str] = []
        if skipped:  # one page holds MAX_MOMENTS; say what was left out instead of dropping it silently
            notes.append(f"verified the first {len(selected)} of {len(requested)} moments (a page holds {MAX_MOMENTS}); "
                         f"not shown: {', '.join(_moment_label(m) for m in skipped)}: check again with those --at")
        result = {"page": str(page), "rows": rows,
                  "timing": {"total_s": round(time.monotonic() - started, 1)},
                  "notes": notes, "render_runs": {"published": pair["base_run"], "working": pair["working_run"]},
                  "base_media": pair["base_media"], "working_media": pair["working_media"]}
        result["lines"] = [f"verify: {len(rows)} decoded frame(s) compared"] + [row["verdict"] for row in rows] + notes
        return result
    except FastLaneError:
        shutil.rmtree(run_dir, ignore_errors=True)
        raise
    except Exception as exc:  # SDK and image errors should retain an actionable verify boundary.
        shutil.rmtree(run_dir, ignore_errors=True)
        raise FastLaneError(str(exc) or type(exc).__name__) from exc

    finally:
        # Only this invocation's exclusive materialization is disposable;
        # comparison PNGs/page remain as the returned inspection artifacts.
        if pair is not None:
            for key in ("base_video", "working_video"):
                video = pair.get(key)
                if isinstance(video, Path) and video.parent.parent == run_dir and video.parent.is_dir():
                    shutil.rmtree(video.parent)
