"""Closed authored relation choices on the existing command runner.

No transaction or geometry inference lives here. Choices select exact source
owners; ordinary handlers still perform the requested structural edit.
"""
from __future__ import annotations

import copy
import math
from typing import Literal, NotRequired, TypedDict

from astrid.core.timeline import moments as mo
from astrid.sdk import timeline_intent as intent


class RelationChoice(TypedDict):
    target: str
    edge: Literal['start', 'end', 'sequence-land', 'sequence']
    choice: Literal['keep', 'detach', 'adjust-offset', 're-anchor', 'cancel']
    anchor: NotRequired[str]
    offset_seconds: NotRequired[float]
    offset_frames: NotRequired[int]


EDGES = ('start', 'end', 'sequence-land', 'sequence')
CHOICES = ('keep', 'detach', 'adjust-offset', 're-anchor', 'cancel')
RELATION_CHOICE_SCHEMA = {
    "type": "object", "required": ["target", "edge", "choice"], "additionalProperties": False,
    "properties": {
        "target": {"type": "string", "pattern": r"^(?:parent|occurrence:[^/\s]+)/clip:[^/\s]+$"},
        "edge": {"enum": list(EDGES)}, "choice": {"enum": list(CHOICES)},
        "anchor": {"type": "string"}, "offset_seconds": {"type": "number"},
        "offset_frames": {"type": "integer"},
    },
    "allOf": [
        {"if": {"properties": {"choice": {"enum": ["keep", "detach", "cancel"]}}},
         "then": {"not": {"anyOf": [{"required": [k]} for k in ("anchor", "offset_seconds", "offset_frames")]}}},
        {"if": {"properties": {"choice": {"enum": ["adjust-offset", "re-anchor"]}}},
         "then": {"anyOf": [{"required": ["offset_seconds"]}, {"required": ["offset_frames"]}]}},
        {"if": {"properties": {"choice": {"const": "re-anchor"}}}, "then": {"required": ["anchor"]},
         "else": {"not": {"required": ["anchor"]}}},
        {"if": {"properties": {"edge": {"const": "sequence"}}},
         "then": {"properties": {"choice": {"enum": ["keep", "detach", "cancel"]}}}},
    ],
}


OPERATIONS = {'clip.on', 'clip.nudge', 'clip.until', 'clip.enter-at', 'clip.end-at',
              'clip.trim', 'clip.set-duration', 'clip.hold-for', 'clip.for', 'clip.extend',
              'clip.clear', 'sequence.fit', 'timeline.add', 'timeline.insert-time', 'timeline.ripple-delete'}


def validate(value):
    from astrid.sdk.timeline.commands import CommandError, is_scoped_id
    if not isinstance(value, list) or not value:
        raise CommandError('relation_choices must be a nonempty array')
    seen = set()
    for row in value:
        if not isinstance(row, dict) or set(row) - {'target', 'edge', 'choice', 'anchor', 'offset_seconds', 'offset_frames'}:
            raise CommandError('Unknown relation choice field')
        if not isinstance(row.get('target'), str) or not is_scoped_id(row['target']) or '/clip:' not in row['target'] or not row['target'].startswith(('parent/', 'occurrence:')) or any(c.isspace() for c in row['target']):
            raise CommandError('Relation choice target must be an exact authored clip ScopedId')
        if row.get('edge') not in EDGES or row.get('choice') not in CHOICES:
            raise CommandError('Unknown relation edge or choice')
        key = row['target'], row['edge']
        if key in seen:
            raise CommandError('Duplicate relation choice for target and edge')
        seen.add(key)
        action = row['choice']
        if row['edge'] == 'sequence' and action not in {'keep', 'detach', 'cancel'}:
            raise CommandError('Sequence membership supports keep/detach/cancel; use start or sequence-land for Moment offsets')
        allowed = {'target', 'edge', 'choice'}
        if action in {'adjust-offset', 're-anchor'}:
            allowed |= {'offset_seconds', 'offset_frames'}
            if not ({'offset_seconds', 'offset_frames'} & row.keys()):
                raise CommandError('Offset choice requires explicit offset_seconds or offset_frames')
        if action == 're-anchor':
            allowed.add('anchor')
            if not isinstance(row.get('anchor'), str):
                raise CommandError('Re-anchor requires an explicit Moment anchor')
            m = mo.parse(row['anchor'])
            if m.offset_s or m.offset_frames:
                raise CommandError('Supply the re-anchor offset in its typed offset fields')
        if set(row) - allowed:
            raise CommandError(f'{action} does not accept anchor/offset fields')
        for field in ('offset_seconds', 'offset_frames'):
            if field in row and (isinstance(row[field], bool) or not isinstance(row[field], (float, int))
                                 or not math.isfinite(row[field]) or (field == 'offset_frames' and int(row[field]) != row[field])):
                raise CommandError(f'{field} must be finite' + (' integral frames' if field == 'offset_frames' else ' seconds'))
    return value


def read(clip, edge):
    if edge == 'start':
        return intent.on(clip.data)
    if edge == 'end':
        until = intent.until(clip.data)
        duration = intent.for_s(clip.data)
        return until if until is not None else ({'for_seconds': duration} if duration is not None else None)
    if edge == 'sequence':
        return intent._get(clip.data, 'sequence')
    return (intent.sequence_fit(clip.data) or {}).get('land')


def write(clip, edge, text):
    if edge == 'start':
        intent.set_on(clip.data, text)
        if text is None:
            # Explicit marker preserves cached absolute geometry without changing
            # legacy absent/null on semantics or removing cut membership.
            intent._set(clip.data, "fixed_start", True)
    elif edge == 'end':
        intent.set_until(clip.data, text if isinstance(text, str) else None)
        intent.set_for(clip.data, text['for_seconds'] if isinstance(text, dict) else None)
    elif edge == 'sequence':
        intent._set(clip.data, 'sequence', copy.deepcopy(text))
        if text is None:
            intent._set(clip.data, 'sequence_index', None)
    else:
        spec = intent.sequence_fit(clip.data) or {}
        if text is None:
            spec.pop('land', None)
        else:
            spec['land'] = text
        intent.set_sequence_fit(clip.data, spec or None)


def path(edge):
    return {'start': 'intent.on', 'end': 'intent.until', 'sequence-land': 'intent.sequence_fit.land', 'sequence': 'intent.sequence'}[edge]


def affected(tl, seeds):
    """Authored transitive dependencies, never screen overlap or generated spans."""
    from astrid.sdk.timeline import commands
    from astrid.sdk.timeline.model import _MomentContext
    from astrid.sdk.timeline.music_beds import sources
    owners = {commands.scoped_clip(tl, c): c for c in tl.clips()}
    for sid in sources(tl):
        owners[sid] = commands.authored_owner(tl, sid)
    deps = {sid: set() for sid in owners}
    for sid, clip in owners.items():
        ctx = _MomentContext(tl, clip)
        def visit(m):
            if m.kind in {'clip_start', 'clip_end'}:
                deps[sid].add(m.clip)
            elif m.kind == 'word':
                hits = mo.find_words(m, ctx.words())
                if m.n:
                    hits = hits[m.n - 1:m.n]
                for run in hits:
                    for word in run:
                        deps[sid].update(k for k, c in owners.items() if c.shot_id == word.shot_id and c.id == word.clip_id)
            elif m.kind in {'beat', 'downbeat'}:
                deps[sid].update(k for k, c in owners.items() if c.is_audio and intent.beat_sources(c.data, m.kind))
                if m.base:
                    visit(m.base)
            elif m.kind in {'cut', 'cut_end', 'end', 'cut_start'}:
                cid = m.cut or intent.cut_of(clip.data)
                deps[sid].update(k for k, c in owners.items() if cid and intent.cut_of(c.data) == cid and c.track == 'plate')
        for edge in EDGES:
            text = read(clip, edge)
            if edge != 'sequence' and isinstance(text, str):
                visit(mo.parse(text))
        seq = intent.sequence(clip.data)
        if seq:
            deps[sid].update(k for k, c in owners.items() if intent.sequence(c.data) and
                             intent.sequence(c.data)[0] == seq[0] and c.shot_id == clip.shot_id)
    hit = set(seeds)
    while True:
        more = {sid for sid, dependencies in deps.items() if dependencies & hit}
        if more <= hit:
            break
        hit |= more
    return [dict(target=sid, edge=edge, relation=copy.deepcopy(read(owners[sid], edge)))
            for sid in sorted(hit) if sid in owners for edge in EDGES if read(owners[sid], edge) is not None]


def prepare(tl, call, selected):
    from dataclasses import replace

    from astrid.sdk.timeline import commands
    rows = validate(call.args['relation_choices'])
    if call.op not in OPERATIONS:
        raise commands.CommandError(f'{call.op} does not accept relation_choices')
    if call.op == 'timeline.add' and 'from' not in call.args:
        raise commands.CommandError('Relation choices on timeline.add require an exact from source')
    seeds = [call.args['from']] if call.op == 'timeline.add' else list(selected)
    if call.op in {'timeline.insert-time', 'timeline.ripple-delete'}:
        start = tl.time(call.args['at'] if call.op == 'timeline.insert-time' else call.args['start'])
        from astrid.sdk.timeline.music_beds import sources
        seeds = sorted({commands.scoped_clip(tl, c) for c in tl.clips() if c.end > start} | set(sources(tl)))
    affected_rows = affected(tl, seeds)
    old = call.args.get('relation_affected')
    if old is not None and old != affected_rows:
        raise commands.SemanticConflict('dependent', seeds[0], 'relation_affected', old, affected_rows,
                                        'Affected authored relations changed; record explicit choices on this head')
    if call.op in {'timeline.insert-time', 'timeline.ripple-delete'}:
        covered = {(r['target'], r['edge']) for r in rows}
        missing = [r for r in affected_rows if (r['target'], r['edge']) not in covered]
        if missing:
            raise commands.SemanticConflict('dependent', missing[0]['target'], path(missing[0]['edge']),
                                            missing[0]['relation'], None, 'Ripple needs a choice for every affected authored relation')
    allowed = set(seeds) | {r['target'] for r in affected_rows}
    for row in rows:
        if row['target'] not in allowed:
            raise commands.CommandError('Relation choice target is outside the captured affected structure')
        clip = commands.authored_owner(tl, row['target'], selected=True)
        if row['edge'] == 'sequence-land':
            seq = intent.sequence(clip.data)
            members = [c for c in tl.clips() if c.shot_id == clip.shot_id and intent.sequence(c.data)
                       and seq and intent.sequence(c.data)[0] == seq[0]]
            if not members or clip.id != min(members, key=lambda c: intent.sequence(c.data)[1]).id:
                raise commands.CommandError('sequence-land must select the actual sequence head clip')
        if row['choice'] not in {'re-anchor', 'cancel'} and read(clip, row['edge']) is None:
            raise commands.CommandError('Selected edge has no authored Moment relation')
    expected = dict(call.expect or {})
    states = commands.entity_states(tl)
    for row in affected_rows + rows:
        key = row['target'] + '::' + path(row['edge'])
        expected.setdefault(key, commands.state_at(states, row['target'], path(row['edge'])))
        if row['edge'] == 'end':
            expected.setdefault(row['target'] + '::intent.for', commands.state_at(states, row['target'], 'intent.for'))
    for row in rows:
        if row['choice'] == 'detach':
            for clock in ('at', 'hold'):
                expected.setdefault(row['target'] + '::' + clock, commands.state_at(states, row['target'], clock))
    if any(row['edge'] == 'sequence' for row in rows):
        for sid in allowed:
            key = sid + '::intent.sequence_fit'
            expected.setdefault(key, commands.state_at(states, sid, 'intent.sequence_fit'))
    return replace(call, args={**call.args, 'relation_affected': affected_rows}, expect=expected)


def position(clip, edge):
    if edge in {'start', 'sequence'}:
        return clip.start
    if edge == 'sequence-land':
        seq = intent.sequence(clip.data)
        members = [c for c in clip._tl.clips() if c.shot_id == clip.shot_id and intent.sequence(c.data)
                   and intent.sequence(c.data)[0] == seq[0]]
        return max(members, key=lambda c: intent.sequence(c.data)[1]).end
    return clip.end


def detach_step(clip):
    from astrid.sdk.timeline.commands import CommandError
    seq = intent.sequence(clip.data)
    members = sorted((c for c in clip._tl.clips() if c.shot_id == clip.shot_id and intent.sequence(c.data)
                      and intent.sequence(c.data)[0] == seq[0]), key=lambda c: intent.sequence(c.data)[1])
    head = members[0]
    recipe = intent.sequence_fit(head.data)
    if recipe:
        if any(k in recipe for k in ('lead', 'race', 'cycle', 'then')):
            raise CommandError('Generated sequence membership requires an explicit recipe partition')
        weights = recipe.get('weights')
        if weights is not None:
            if len(weights) != len(members):
                raise CommandError('Sequence weights do not match captured membership')
            recipe['weights'] = [w for c, w in zip(members, weights) if c.id != clip.id]
        remaining = [c for c in members if c.id != clip.id]
        if remaining:
            intent.set_sequence_fit(remaining[0].data, recipe)
        if clip.id == head.id:
            intent.set_sequence_fit(clip.data, None)
    write(clip, 'sequence', None)


def _owned_edit(tl, sid, function):
    from astrid.sdk.timeline import commands, music_beds
    clip = commands.authored_owner(tl, sid, selected=True)
    if sid in music_beds.sources(tl):
        # Use the existing source-edit adapter so source/projection validation,
        # basis shifts and final projection have their established owner.
        return music_beds.source_edit(function)(clip)
    return function(clip)


def apply_choices(tl, rows, *, copy_target=None):
    """Freeze detaches before the ordinary edit using existing owner adapters."""
    from astrid.sdk.timeline import commands
    captured = getattr(tl._open_edit, 'base_document', None)
    base = tl.__class__(copy.deepcopy(captured)) if captured is not None and copy_target is None else None
    saved = []
    for row in rows:
        def apply_one(clip):
            edge, action = row['edge'], row['choice']
            old = read(clip, edge)
            frozen = position(clip, edge)
            if action == 'detach' and base is not None:
                original = commands.authored_owner(base, row['target'], selected=True)
                frozen = position(original, edge)
            text = old
            if action in {'adjust-offset', 're-anchor'}:
                if action == 'adjust-offset' and isinstance(old, dict):
                    text = {'for_seconds': float(row.get('offset_seconds', 0)) + int(row.get('offset_frames', 0)) / tl.fps}
                else:
                    anchor = mo.parse(row['anchor'] if action == 're-anchor' else old)
                    from dataclasses import replace
                    text = mo.format_moment(replace(anchor, offset_s=float(row.get('offset_seconds', 0)),
                                                   offset_frames=int(row.get('offset_frames', 0))))
            elif action == 'detach':
                text = None
                if edge == 'sequence':
                    detach_step(clip)
                else:
                    write(clip, edge, None)
                if edge == 'start':
                    clip._set_start(frozen)
                elif edge == 'end':
                    from astrid.sdk.timeline.doc import _set_length
                    if frozen <= clip.start:
                        raise commands.CommandError('Captured end precedes the edited start')
                    _set_length(clip.data, frozen - clip.start)
                    intent.set_for(clip.data, clip.duration)
                elif edge == 'sequence':
                    clip._set_start(frozen)
                    write(clip, 'start', intent.on(clip.data))
                    intent.set_for(clip.data, clip.duration)
            return (clip, edge, action, old, text, frozen)
        saved.append(apply_one(copy_target) if copy_target is not None else _owned_edit(tl, row['target'], apply_one))
    return saved


def finish(tl, saved):
    from astrid.sdk.timeline import commands
    for selected, edge, action, old, text, frozen in saved:
        sid = commands.scoped_clip(tl, selected)
        def finish_one(clip):
            actual = position(clip, edge)
            expected = frozen
            if action == 'keep' and edge != 'sequence':
                expected = clip.start + old['for_seconds'] if isinstance(old, dict) else tl._moment_time(old, clip)
            if action == 'keep' and abs(actual - expected) > 0.5 / tl.fps:
                raise commands.SemanticConflict('dependent', sid, path(edge), old, actual,
                                                'keep conflicts with the requested geometry')
            write(clip, edge, text)
            if edge == 'sequence':
                return
            if text:
                value = clip.start + text['for_seconds'] if isinstance(text, dict) else tl._moment_time(text, clip)
                if edge == 'start':
                    clip._set_start(value)
                elif edge == 'end':
                    from astrid.sdk.timeline.doc import _set_length
                    if value <= clip.start:
                        raise commands.CommandError('Chosen end relation precedes clip start')
                    _set_length(clip.data, value - clip.start)
            elif edge == 'start':
                clip._set_start(actual)
            elif edge == 'end':
                intent.set_for(clip.data, clip.duration)
        _owned_edit(tl, sid, finish_one)
