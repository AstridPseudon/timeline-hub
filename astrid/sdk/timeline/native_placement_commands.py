"""Explicit-owner placement using the existing absolute clip.move recipe.

This changes an existing clip's start, preserving its media and source window.
It does not implement the App's legacy generation placement/pooling algorithm.
"""
from __future__ import annotations

import re

from ._command_state import CommandError
from .capture import _duration, move, move_intent, number


def placement_move(ctx, command):
    ref = command['select']
    owner = ref.rsplit('/', 1)[0]
    if owner != 'parent':
        if ctx.select('placement.owners', owner) != [owner]:
            raise CommandError('shared authored placement is unsupported',
                               kind='unsupported_ownership', ref=owner)
    clip = ctx.state.entity(ref)
    asset = clip.get('asset', clip.get('asset_id'))
    if asset is not None:
        # Guard the entire existing binding, including opaque selection pins.
        # Read raw paths so accepted source writes also protect against ABA.
        if owner == 'parent':
            ctx.read('parent', ['registry', 'assets', str(asset)])
            ctx.read('parent', ['config', 'registry', 'assets', str(asset)])
        else:
            ctx.read(owner + '/source', ['registry', 'assets', str(asset)])
    move(ctx, command)
    if owner != 'parent':
        extent = number(ctx.read(owner, ['duration_ms']), 'occurrence.duration_ms', positive=True) / 1000
        moved = ctx.state.entity(ref)
        start = moved['at'] if 'at' in moved else moved['at_ms'] / 1000
        if start + _duration(moved) > extent + 1e-9:
            raise CommandError('placed interval exceeds occurrence duration',
                               kind='occurrence_boundary', ref=owner)


def capture_placement(bundle, owner, clip_id, on, *, ownership):
    """Capture global seconds on the original bundle, before local preview.

    owner is parent or occurrence:<raw ID>; clip_id is the raw child ID.
    ownership must explicitly match that scope. Shared authoring, pooling,
    automatic positioning, track changes and media selection are unsupported.
    The result is placement.move v1, with its authoritative capture.
    """
    if ownership == 'shared':
        raise CommandError('shared placement is unsupported', kind='unsupported_ownership')
    expected = ('parent' if owner == 'parent' else 'occurrence'
                if isinstance(owner, str) and re.fullmatch(r'occurrence:[^/]+', owner)
                and '::' not in owner else None)
    if expected is None or ownership != expected:
        raise CommandError('placement requires matching explicit parent or occurrence ownership',
                           kind='unsupported_ownership')
    if (not isinstance(clip_id, str) or not clip_id.strip()
            or '/' in clip_id or '::' in clip_id):
        raise CommandError('placement requires a raw clip identity', kind='identity_conflict')
    from .commands import execute

    ref = owner + '/clip:' + clip_id
    return execute(bundle, [{'schema_version': 1, 'op': 'placement.move', 'version': '1',
                             'select': ref, 'args': {'on': on},
                             'intent': move_intent(ref)}]).commands[0]
