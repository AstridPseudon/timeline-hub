"""Change only the authored duration of one canonical occurrence."""
from __future__ import annotations

from ._command_state import CommandError, root_identity
from .capture import MAP_FIELDS

OCCURRENCE_RESIZE_INTENT = {'ownership': 'occurrence'}


def occurrence_resize(ctx, command):
    owner, args = command['select'], command['args']
    identity = root_identity(owner)
    if identity is None or identity[0] != 'occurrence' or '/' in owner:
        raise CommandError('resize requires an exact occurrence root', kind='unsupported_ownership')
    if ctx.read('parent', ['config', 'pinnedShotGroups']) not in (None, []):
        raise CommandError('legacy groups require recorded migration', kind='migration_needed')
    if ctx.select('placement.owners', owner) != [owner]:
        raise CommandError('shared occurrence isolation needs a materialization carrier',
                           kind='unsupported_ownership', ref=owner)
    ctx.select('collection.occurrences', 'parent')

    occurrence_id = ctx.read(owner, ['occurrence_id'])
    shot_id = ctx.read(owner, ['shot_id'])
    ctx.read(owner, ['shot_revision_id'])
    if occurrence_id != identity[1] or not isinstance(shot_id, str) or not shot_id:
        raise CommandError('resize requires a stable occurrence and shot identity',
                           kind='identity_conflict', ref=owner)

    current = ctx.read(owner, ['duration_ms'])
    if type(current) is not int or current <= 0:
        raise CommandError('resize requires an existing positive integer duration_ms',
                           kind='unsupported_timing', ref=owner)
    duration_ms = args['duration_ms']
    if type(duration_ms) is not int or duration_ms <= 0:
        raise CommandError('duration_ms must be a positive integer',
                           kind='unsupported_timing', ref=owner)

    # Read the existing raw timing codecs as exact replay basis. This carrier
    # preserves them and never quantizes or normalizes their rational values.
    for path in MAP_FIELDS:
        ctx.read(owner, path)

    ctx.bind('resize.owner', owner)
    ctx.bind('resize.shot', 'shot:' + shot_id)
    ctx.write(owner, ['duration_ms'], duration_ms)


def capture_occurrence_resize(bundle, occurrence_id, duration_ms):
    """Capture one explicit occurrence-duration write on the original bundle."""
    from .commands import execute

    owner = 'occurrence:' + occurrence_id
    return execute(bundle, [{'schema_version': 1, 'op': 'occurrence.resize', 'version': '1',
                             'select': owner, 'args': {'duration_ms': duration_ms},
                             'intent': OCCURRENCE_RESIZE_INTENT}]).commands[0]
