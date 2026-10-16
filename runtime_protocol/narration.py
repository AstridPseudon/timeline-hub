"""Immutable SCRIPT-REFLOW projections; speech text matching belongs to Astrid.

These helpers never tokenize, normalize, generate speech, or consult catalogs.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import re
from typing import TypedDict

from .errors import ValidationError


class ManagedTakeRef(TypedDict):
    association_id: str
    object_id: str


class NarrationTakeRefs(TypedDict):
    speech: ManagedTakeRef
    speech_words: ManagedTakeRef
    speech_manifest: ManagedTakeRef


class NarrationSpeech(TypedDict):
    object_id: str
    size: int
    media_type: str
    duration_seconds: float


class VerifiedNarrationTake(TypedDict):
    refs: NarrationTakeRefs
    speech: NarrationSpeech
    manifest: dict
    words: dict
    dependency_objects: list[str]
    dependency_digest: str


def json_digest(value):
    return 'sha256:' + hashlib.sha256(json.dumps(value, sort_keys=True,
        separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def validate_take_refs(refs):
    if not isinstance(refs, dict) or set(refs) != {'speech', 'speech_words', 'speech_manifest'}:
        raise ValidationError('narration take requires exactly three managed refs')
    for ref in refs.values():
        if (not isinstance(ref, dict) or set(ref) != {'association_id', 'object_id'}
                or not isinstance(ref['association_id'], str) or not ref['association_id']
                or not isinstance(ref['object_id'], str)
                or not re.fullmatch(r'sha256:[0-9a-f]{64}', ref['object_id'])):
            raise ValidationError('invalid managed narration ref')


def request_take_refs(value):
    """Only typed take slots authorize reads, never arbitrary object IDs."""
    if isinstance(value, dict):
        for key, item in value.items():
            if (key == 'take' and isinstance(item, dict)
                    and set(item) & {'speech', 'speech_words', 'speech_manifest'}):
                validate_take_refs(item)
                yield copy.deepcopy(item)
            else:
                yield from request_take_refs(item)
    elif isinstance(value, list):
        for item in value:
            yield from request_take_refs(item)


def internal_take_refs(payload):
    for clip in payload.get('clips', []):
        astrid = clip.get('app', {}).get('astrid', {})
        if 'take' in astrid:
            validate_take_refs(astrid['take'])
            yield astrid['take']


def validate_artifacts(refs, manifest, words):
    validate_take_refs(refs)
    audio = refs['speech']['object_id'][7:]
    if (not isinstance(manifest, dict) or type(manifest.get('schema_version')) is not int
            or manifest['schema_version'] != 1 or not isinstance(manifest.get('text'), str)
            or not manifest['text'] or not isinstance(manifest.get('settings'), dict)
            or manifest.get('text_sha256') != hashlib.sha256(manifest['text'].encode()).hexdigest()
            or manifest.get('audio_sha256') != audio):
        raise ValidationError('narration manifest identity mismatch')
    duration = manifest.get('duration_seconds')
    if (type(duration) not in (int, float) or not math.isfinite(duration) or duration <= 0
            or not isinstance(words, dict) or type(words.get('schema_version')) is not int
            or words['schema_version'] != 1 or words.get('audio_sha256') != audio
            or type(words.get('duration_seconds')) not in (int, float)
            or words['duration_seconds'] != duration
            or not isinstance(words.get('words'), list) or not words['words']):
        raise ValidationError('narration word/audio duration mismatch')
    previous = 0
    for row in words['words']:
        if (not isinstance(row, dict) or not isinstance(row.get('word'), str) or not row['word']
                or any(type(row.get(k)) not in (int, float) or not math.isfinite(row[k])
                       for k in ('start_s', 'end_s'))
                or not previous <= row['start_s'] < row['end_s'] <= duration):
            raise ValidationError('invalid narration word timing')
        previous = row['end_s']


def narration_lines(closure, *, require_takes=False):
    internals = {v['revision_id']: v for v in closure['internal_timeline_revisions']}
    shots = {(v['shot_id'], v['revision_id']): v for v in closure['shot_revisions']}
    seen = set()
    parent = closure['parent_revision']['payload']
    # Parent ordinary clips have no invented child/occurrence identity. The
    # accepted parent pin is recorded by narration_state in the same receipt.
    contexts = [(None, None, None, parent)]
    for occurrence in parent['occurrences']:
        shot = shots[(occurrence['shot_id'], occurrence['shot_revision_id'])]
        internal = internals[shot['internal_timeline_revision_id']]
        contexts.append((occurrence['occurrence_id'], shot, internal, internal['payload']))
    for occurrence_id, shot, internal, payload in contexts:
        for clip in payload.get('clips', []):
            astrid = clip.get('app', {}).get('astrid', {})
            if 'take' not in astrid:
                if require_takes and 'segment' in astrid:
                    raise ValidationError('narration line is missing its managed take')
                continue  # Legacy unbound narration is not upgraded by a read.
            validate_take_refs(astrid['take'])
            if any(not isinstance(v, str) or not v for v in (clip.get('id'), astrid.get('segment'), astrid.get('text'), clip.get('asset'))):
                raise ValidationError('narration line identity/text/asset is missing')
            key = (occurrence_id, clip['id'])
            if key in seen:
                raise ValidationError('duplicate scoped narration clip')
            seen.add(key)
            asset = payload.get('registry', {}).get('assets', {}).get(clip['asset'])
            if not isinstance(asset, dict) or asset.get('object_id') != astrid['take']['speech']['object_id']:
                raise ValidationError('narration speech object does not match registered clip asset')
            if not isinstance(astrid.get('words'), list):
                raise ValidationError('narration line words are missing')
            yield ({'occurrence_id': occurrence_id, 'shot_id': shot['shot_id'] if shot else None,
                    'shot_revision_id': shot['revision_id'] if shot else None,
                    'internal_timeline_id': internal['timeline_id'] if internal else None,
                    'internal_revision_id': internal['revision_id'] if internal else None, 'clip_id': clip['id'],
                    'segment': astrid['segment'], 'take': copy.deepcopy(astrid['take']),
                    'line_digest': json_digest(clip)}, astrid)


def narration_projection(closure):
    return {'version': 1, 'lines': sorted((v for v, _ in narration_lines(closure)),
                                         key=lambda v: (v['occurrence_id'] is not None,
                                                        v['occurrence_id'] or '', v['clip_id']))}


def validate_line_take(astrid, take):
    if astrid['text'] != take['manifest']['text']:
        raise ValidationError('authored narration text does not match immutable take')
    rows = []
    ids = set()
    for row in astrid['words']:
        # The established timeline word representation is [start, end, text].
        # Preserve optional word IDs; never mint new IDs or normalize text.
        if isinstance(row, list) and len(row) in (3, 4):
            row = {'start_s': row[0], 'end_s': row[1], 'word': row[2],
                   **({'id': row[3]} if len(row) == 4 else {})}
        if not isinstance(row, dict):
            raise ValidationError('invalid authored narration word')
        if 'id' in row:
            if not isinstance(row['id'], str) or not row['id'] or row['id'] in ids:
                raise ValidationError('invalid or duplicate narration word ID')
            ids.add(row['id'])
        rows.append({k: v for k, v in row.items() if k != 'id'})
    if json_digest(rows) != json_digest(take['words']['words']):
        raise ValidationError('authored narration words do not match immutable take')
