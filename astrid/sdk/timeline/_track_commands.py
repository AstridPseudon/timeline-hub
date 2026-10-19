"""Bounded parent track removal using the shared declared dependency scan."""
from __future__ import annotations

import re

from ._command_state import CommandError
from .inverse import _dependents


def track_delete(ctx, command):
    ref = command['select']
    if not isinstance(ref, str) or not re.fullmatch(r'parent/track:(?!.*::)[^/]+', ref):
        raise CommandError('track.delete v1 requires a parent track identity')
    ctx.select('collection.tracks', 'parent')
    if ctx.read(ref) is None:
        raise CommandError('track disappeared', kind='identity_conflict', ref=ref)
    ctx.bind('delete.target', ref)
    if _dependents(ctx.state, ref, recording=ctx):
        raise CommandError('track has surviving dependents', kind='surviving_dependents', ref=ref)
    ctx.clear(ref, [])


def capture_track_delete(bundle, select):
    from .commands import execute

    return execute(bundle, [{'schema_version': 1, 'op': 'track.delete', 'version': '1',
                             'select': select, 'args': {}}]).commands[0]
