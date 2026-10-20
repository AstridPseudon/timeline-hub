"""Pure legacy-shaped display view with explicit canonical ownership bindings."""
from __future__ import annotations

import copy
from fractions import Fraction

from ._command_state import CommandError, State
from .capture import number, occurrence_start, rate
from .new_group_commands import _geometry
from .occurrence_commands import lane


def project_group_view(bundle):
    """Read current ordered canonical children; provenance supplies display metadata only.

    `bindings` is parallel to clips. Display IDs are never edit selectors.
    Intervals are half-open global seconds; source hold/speed/window stay authored.
    """
    state = State(bundle)
    clips = copy.deepcopy(state.collection('parent', 'clip'))
    bindings = [{'occurrence': None, 'clip': 'parent/clip:' + row['id'],
                 'raw_child_track': None, 'parent_track': 'parent/track:' + row['track']}
                for row in clips]
    groups = []
    output = copy.deepcopy(state.config('parent').get('output'))
    rate((output or {}).get('fps'))
    for occurrence in bundle['placements']:
        owner = 'occurrence:' + occurrence['occurrence_id']
        provenance = occurrence.get('provenance') or {}
        migration = provenance.get('group_migration') or {}
        if (isinstance(occurrence.get('source_offset'), bool) or isinstance(occurrence.get('speed'), bool)
                or occurrence.get('source_offset') not in (None, 0) or occurrence.get('speed') not in (None, 1)
                or any(occurrence.get(k) is not None for k in ('time_map', 'timeMap'))):
            raise CommandError('group view requires a translation-only occurrence')
        rows = state.collection(owner, 'clip')
        parent_track = 'parent/track:' + lane(occurrence)
        origin = Fraction(str(occurrence_start(occurrence)))
        extent = Fraction(str(number(occurrence['duration_ms'], 'duration_ms', positive=True))) / 1000
        for row in rows:
            start, end = _geometry(row)
            if end > extent:
                raise CommandError('group child exceeds occurrence duration')
            clip = copy.deepcopy(row)
            clip['at'] = float(origin + start)
            clip['track'] = lane(occurrence)
            clips.append(clip)
            bindings.append({'occurrence': owner, 'clip': owner + '/clip:' + row['id'],
                             'raw_child_track': owner + '/track:' + row['track'], 'parent_track': parent_track})
        if 'legacy_group' in migration:
            group = copy.deepcopy(migration['legacy_group'])
            group.update(trackId=lane(occurrence), clipIds=[row['id'] for row in rows])
            groups.append(group)
    return {'clips': clips, 'pinnedShotGroups': groups, 'bindings': bindings, 'output': output}
