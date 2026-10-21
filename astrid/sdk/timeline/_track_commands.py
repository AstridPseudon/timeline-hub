"""Native track collection recipes and compatibility exports."""
from __future__ import annotations

import copy

from ._collections import order
from ._command_state import CommandError
from ._scalar_commands import capture_track_set, track_set


def track_reorder(ctx, command):
    """Replace the complete authored parent track permutation.

    The order is a virtual authored property. Raw track rows remain the
    carrier, so this handler never reconstructs or normalizes their payloads.
    """
    if command['select'] != 'parent':
        raise CommandError('track.reorder requires the parent track collection')
    expected = command['args']['expected_order']
    desired = command['args']['order']
    current = ctx.select('collection.tracks', 'parent')
    if current != expected:
        raise CommandError('original track order changed', kind='selection_changed',
                           ref='parent')
    if (len(desired) != len(current) or len(desired) != len(set(desired))
            or set(desired) != set(current)
            or any(not item.startswith('parent/track:') for item in desired)):
        raise CommandError('track order must be a complete unique same-owner permutation',
                           kind='selection_changed', ref='parent')
    ctx.write('parent', ['track_order'], copy.deepcopy(desired))


def capture_track_reorder(bundle, order, *, expected_order=None):
    """Capture a complete parent media-track permutation from authored rows."""
    if expected_order is None:
        from ._command_state import State
        expected_order = order_for_parent(State(bundle))
    return _capture(bundle, {
        'schema_version': 1,
        'op': 'track.reorder',
        'version': '1',
        'select': 'parent',
        'args': {'order': copy.deepcopy(order),
                 'expected_order': copy.deepcopy(expected_order)},
        'intent': {},
    })


def order_for_parent(state):
    return order(state, 'parent', 'track')


def _capture(bundle, command):
    from .commands import execute
    return execute(bundle, [command]).commands[0]


__all__ = ['capture_track_reorder', 'capture_track_set', 'order_for_parent', 'track_reorder', 'track_set']
