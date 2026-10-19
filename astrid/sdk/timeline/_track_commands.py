"""The bounded native parent-track label edit."""
from __future__ import annotations

import copy
import re

from ._command_state import CommandError


def _target(ctx, command):
    ref = command['select']
    if not isinstance(ref, str) or not re.fullmatch(r'parent/track:[^/]+', ref) or '::' in ref:
        raise CommandError(f"{command['op']} requires a parent track identity")
    if ctx.read(ref, ['id']) is None:
        raise CommandError('track target disappeared', kind='identity_conflict', ref=ref)
    ctx.dependency('scalar.images', 'entity', {'parent': copy.deepcopy(ctx.state.bundle.get('base_parent', {}))})
    ctx.bind('scalar.target', ref, dependencies=['scalar.images'])
    return ref


def track_set(ctx, command):
    ref = _target(ctx, command)
    values, clear = command['args']['values'], command['args']['clear']
    if set(values).intersection(clear):
        raise CommandError('a track key cannot be both set and cleared')
    for key in sorted(values):
        ctx.write(ref, [key], values[key])
    for key in sorted(clear):
        ctx.clear(ref, [key])


def capture_track_set(bundle, select, *, values=None, clear=()):
    from .commands import execute

    return execute(bundle, [{
        'schema_version': 1,
        'op': 'track.set',
        'version': '1',
        'select': select,
        'args': {
            'values': copy.deepcopy({} if values is None else values),
            'clear': list(clear),
        },
    }]).commands[0]
