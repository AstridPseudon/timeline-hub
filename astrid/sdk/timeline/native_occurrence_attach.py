"""Place an existing destination child again without allocating another shot."""
from __future__ import annotations

from ._command_state import CommandError, root_identity
from .native_occurrence_create import occurrence_row
from .native_occurrence_duplicate import OCCURRENCE_INTENT


def occurrence_attach(ctx, command):
    owner = command['select']
    root = root_identity(owner)
    if root is None or root[0] != 'occurrence':
        raise CommandError('attach requires one destination occurrence', kind='unsupported_ownership')
    source = ctx.read(owner)
    if not isinstance(source, dict):
        raise CommandError('attach source disappeared', kind='identity_conflict', ref=owner)
    # Equal bytes at a different revision do not authorize another physical image.
    ctx.read('timeline')
    ctx.read(owner + '/shot', ['shot_id'])
    ctx.read(owner + '/shot', ['payload'])
    ctx.read(owner + '/source')
    ctx.bind('attach.source', owner)
    row, _ = occurrence_row(ctx, {**command['args'], 'shot_id': source['shot_id']})
    ctx.create_entity('occurrence:' + row['occurrence_id'], kind='occurrence', owner='parent', value=row)


def capture_occurrence_attach(bundle, owner, occurrence_id, *, track, on, duration):
    """Capture a fresh occurrence of the selected, already reachable child."""
    from .commands import execute

    return execute(bundle, [{'schema_version': 1, 'op': 'occurrence.attach', 'version': '1',
                             'select': owner, 'args': {'occurrence_id': occurrence_id,
                                 'track': track, 'on': on, 'duration': duration},
                             'intent': OCCURRENCE_INTENT}]).commands[0]
