"""Completion auto-placement: a pure builder over existing placement/media birth.

Resolves the legacy "anchor-after" choice once, on the caller's original bundle,
and emits one ordinary command with a literal start. Nothing new is executed:
images use placement.create, videos use occurrence.add-media. The capture dict
names the anchor timing and the fallback it consumed. Resolution is never
re-run on replay, so replay and inverse are exact whatever happened to the anchor.

Start rule (frames at the pinned rational fps, intervals half-open):
  anchor present  -> the anchor's end frame (start + max(1, round(duration * fps))).
  anchor absent   -> the lane end: the greatest end frame of the occurrence's own
                     clips on the occurrence lane, or the occurrence start if none.
Absent means no anchor id was given or no such clip exists in the occurrence.
A present anchor with unusable timing refuses; it never falls back.
Completion holds are distinct from the shared 4 s hold: image 5 s, video 5 s
unless the caller supplies the completed asset's duration.
"""
from __future__ import annotations

import math
from fractions import Fraction

from astrid.core.timeline.duration import clip_end_frame

from ._command_state import CommandError, State
from .capture import number, occurrence_start, rate
from .native_occurrence_media_commands import capture_occurrence_add_media
from .native_placement_commands import _explicit_occurrence, _raw_clip_id, capture_placement_create

COMPLETION_SECONDS = 5


def _end_frame(clip, origin, fps):
    at = clip['at'] if 'at' in clip else number(clip.get('at_ms'), 'clip.at_ms') / 1000
    try:
        return clip_end_frame({**clip, 'at': origin + number(at, 'clip.at')}, float(fps))
    except ValueError as exc:
        raise CommandError(str(exc), kind='unsupported_timing', ref=clip.get('id')) from exc


def _kind(media, verified_media):
    for value in verified_media:
        if value['selection'] == media:
            return str(value['media_type']).split('/')[0]
    raise CommandError('completed media is not verified', kind='dependency_unavailable')


def auto_place_completion(bundle, owner, clip_id, media, *, ownership, verified_media,
                          anchor=None, duration=None):
    """Return {'commands': [...], 'capture': {...}} for one completed generation.

    owner is occurrence:<raw ID> with ownership='occurrence'; parent-owned media
    birth is not available in this stack. clip_id is the caller-reserved raw ID
    and media the exact five-field selection of the completed variant.
    """
    _explicit_occurrence(owner, ownership)
    _raw_clip_id(clip_id)
    kind = _kind(media, verified_media)
    if kind not in ('image', 'video'):
        raise CommandError('completion placement requires image or video media', kind='unsupported_media')
    state = State(bundle)
    row = state.occurrence(owner)
    # placement.create re-checks this at replay; occurrence.add-media does not, so
    # the video path is guarded at capture only.
    if sum(1 for other in bundle['placements'] if other['shot_id'] == row['shot_id']) != 1:
        raise CommandError('shared authored placement is unsupported', kind='unsupported_ownership', ref=owner)
    origin = occurrence_start(row)
    lane = (row.get('placement') or {}).get('track', row.get('track'))
    fps = rate(state.config('parent').get('output', {}).get('fps'))
    clips = state.collection(owner, 'clip')
    found = next((clip for clip in clips if anchor is not None and clip.get('id') == anchor), None)
    if found is not None:
        frame, resolution = _end_frame(found, origin, fps), 'anchor-after'
    else:
        ends = [_end_frame(clip, origin, fps) for clip in clips if clip.get('track') == lane]
        frame = max(ends, default=math.floor(origin * fps + Fraction(1, 2)))
        resolution = 'lane-end'
    on = float(Fraction(frame, 1) / fps)
    length = COMPLETION_SECONDS if kind == 'image' or duration is None else duration
    if kind == 'image':
        command = capture_placement_create(bundle, owner, clip_id, media, on, length,
                                           ownership=ownership, verified_media=verified_media)
    else:
        number(length, 'duration', positive=True)
        clip = {'id': clip_id, 'clipType': 'video', 'asset': media['asset'], 'track': lane,
                'at': on - origin, 'hold': length, 'from': 0, 'to': length, 'speed': 1}
        command = capture_occurrence_add_media(bundle, owner, clip, media, verified_media=verified_media)
    return {'commands': [command],
            'capture': {'owner': owner, 'clip': clip_id, 'kind': kind, 'media': dict(media),
                        'anchor': {'id': anchor, 'state': 'present' if found is not None else 'absent'},
                        'resolution': resolution, 'fps': {'numerator': fps.numerator,
                                                          'denominator': fps.denominator},
                        'start_frame': frame, 'on': on, 'seconds': length}}
