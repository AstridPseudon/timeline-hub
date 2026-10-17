"""Thin shared-scene consumers. Geometry and visibility are answered by the warm owner.

An unavailable owner is an explicit unknown finding. Structural editing and role
queries require neither this module nor a renderer; no fallback visibility math.
"""
from __future__ import annotations
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import threading
from typing import Literal

from .roles import element_coverage, role_of
from .astrid_ns import read_app
from astrid.core.execution.remotion_frame_owner import FrameOwnerError


@dataclass(frozen=True)
class Visible:
    clip_id: str
    address: str
    track: str
    z: int
    role: str
    opacity: float | None
    bounds: tuple[float, float, float, float] | None
    bounds_source: str
    full_frame: bool
    findings: tuple[str, ...] = ()
    # full_frame describes the bounds, not an opaque glyph/pixel rectangle.
    opaque_support: Literal['rect', 'none', 'unknown'] = 'unknown'


@dataclass(frozen=True)
class Span:
    start_frame: int
    end_frame: int
    cls: str
    content: str | None
    clips: tuple[str, ...]
    findings: tuple[str, ...] = ()


_local = threading.local()


def use_client(client):
    """Install an invocation-scoped client; returns the previous one for restoration."""
    old = getattr(_local, 'client', None)
    _local.client = client
    return old


def _client():
    client = getattr(_local, 'client', None)
    if client is not None:
        return client
    from astrid.core.execution.remotion_host_session import host_remotion_client
    if host_remotion_client() is None:
        raise FrameOwnerError('frame_owner_unavailable')
    from astrid.core.execution.remotion_evaluation import RemotionEvaluationClient
    from astrid.packs.rendering.actions.timeline_visualize.composed_frame import renderer_environment_identity
    project, node = os.environ.get('ASTRID_REMOTION_PROJECT_DIR'), os.environ.get('ASTRID_NODE_EXECUTABLE')
    if not project or not node:
        raise FrameOwnerError('evaluation_configuration_unavailable')
    # The executor cwd is its admitted attempt root; the host independently
    # validates every path against the original retained task lease.
    client = RemotionEvaluationClient(project_dir=project, node_executable=node,
        attempt_root=Path.cwd(), renderer_closure=renderer_environment_identity)
    _local.client = client
    return client


def _payload(config, fps, canvas, elements, assets=None):
    # Only renderer-relevant resolved fields enter the answer/revision cache.
    # Unrelated document notes, journal entries, and publication metadata don't.
    fields = {'id', 'at', 'hold', 'from', 'to', 'speed', 'asset', 'clipType', 'track',
              'x', 'y', 'width', 'height', 'opacity', 'cropTop', 'cropBottom', 'cropLeft',
              'cropRight', 'params', 'entrance', 'exit', 'transition', 'effects', 'modifiers', 'keyframeOrigin'}
    clips = [{k: v for k, v in clip.items() if k in fields} for clip in config.get('clips', ())]
    tracks = config.get('tracks')
    if not tracks:
        tracks = [{'id': key, 'kind': 'visual', 'label': key} for key in dict.fromkeys(c.get('track', 'v1') for c in clips)]
    tracks = [track for track in tracks if track.get('kind', 'visual') == 'visual']
    track_ids = {track['id'] for track in tracks}
    clips = [clip for clip in clips if clip.get('track', 'v1') in track_ids]
    roles = {str(c.get('id')): role_of(c, c.get('track'), elements) for c in clips}
    track_fields = {'id', 'kind', 'label', 'opacity', 'fit', 'scale', 'blendMode'}
    tracks = [{k: v for k, v in track.items() if k in track_fields} for track in tracks]
    registry = assets or config.get('assets') or {'assets': {}}
    referenced = {clip.get('asset') for clip in clips if clip.get('asset')}
    registry = {'assets': {k: v for k, v in registry.get('assets', {}).items() if k in referenced}}
    return {'timeline': {'theme': config.get('theme', 'banodoco-default'), 'clips': clips,
                'tracks': tracks, 'theme_overrides': config.get('theme_overrides', {})},
            'assets': registry, 'fps': fps,
            'width': canvas['width'], 'height': canvas['height'], 'roles': roles}


def frames_at(config, frames, fps, canvas, elements=None, assets=None):
    elements = elements if elements is not None else element_coverage({c.get('clipType') for c in config.get('clips', ()) if c.get('clipType')})
    payload = _payload(config, fps, canvas, elements, assets)
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()
    return _client().query_scene(revision_digest=digest, scene=payload, frames=list(frames))


def _findings(answer):
    return tuple(dict.fromkeys(f"{f['code']} {f['clipId']}: {f['reason']}" for f in answer.get('findings', ())))


def visible_at(config, frame, fps, canvas, elements=None):
    answer = frames_at(config, [frame], fps, canvas, elements)[0]
    clips = {str(c.get('id')): c for c in config.get('clips', ())}
    result = []
    for layer in answer['layers']:
        if layer['visible'] is False:
            continue
        clip = clips.get(layer['clipId'], {})
        app = read_app(clip)
        address = f"{app['cut']}.{app['layer']}" if app.get('cut') and app.get('layer') else str(layer['clipId']).split(':')[-1]
        b = layer['bounds']
        rect = b.get('rect') if b.get('status') == 'known' else None
        bounds = (rect['x'], rect['y'], rect['x'] + rect['width'], rect['y'] + rect['height']) if rect else None
        result.append(Visible(layer['clipId'], address, layer['track'], layer['z'], layer['role'], layer['opacity'],
            bounds, 'full' if layer['fullFrame'] else 'declared' if bounds is not None else 'unknown', layer['fullFrame'],
            _findings({'findings': layer.get('findings', [])}),
            opaque_support=layer.get('opaqueSupport', 'unknown')))
    return sorted(result, key=lambda layer: layer.z)


def coverage(config, fps, canvas, elements, *, start_frame, end_frame):
    spans = []
    for start in range(start_frame, end_frame, 120):
        frames = list(range(start, min(end_frame, start + 120)))
        try:
            answers = frames_at(config, frames, fps, canvas, elements)
        except FrameOwnerError as error:
            return [Span(start_frame, end_frame, 'UNKNOWN', None, (), (f'evaluation-unavailable: {error}',))]
        for answer in answers:
            value = (answer['coverage'], answer['content'], tuple(layer['clipId'] for layer in answer['layers'] if layer['visible'] is not False), _findings(answer))
            frame = answer['frame']
            if spans and (spans[-1].cls, spans[-1].content, spans[-1].clips, spans[-1].findings) == value:
                last = spans[-1]; spans[-1] = Span(last.start_frame, frame + 1, *value)
            else:
                spans.append(Span(frame, frame + 1, *value))
    return spans


def bounds_at(config, frame, fps, canvas, clip_id):
    try:
        layer = next((layer for layer in visible_at(config, frame, fps, canvas) if layer.clip_id == clip_id), None)
    except FrameOwnerError:
        return None, 'unknown'
    return (layer.bounds, layer.bounds_source) if layer else (None, 'unknown')
