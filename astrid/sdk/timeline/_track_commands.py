"""Native track collection recipes and compatibility exports."""
from __future__ import annotations

import copy

from ._collections import order
from ._command_state import CommandError, equal, present
from ._scalar_commands import capture_track_set, track_set


_DATA_LANE_PLACEMENT_PATH = ['config', 'app', 'timelineDataLanePlacement']


def _validate_data_lane_placement(value, *, label):
    """Validate Main's authored lane-placement leaf without normalizing it."""
    if (not isinstance(value, dict) or type(value.get('version')) is not int
            or value['version'] != 1 or set(value) != {'version', 'lanes'}
            or not isinstance(value['lanes'], list)):
        raise CommandError(f'{label} must be a version 1 lane placement object',
                           kind='selection_changed', ref='parent')
    seen = set()
    for entry in value['lanes']:
        if (not isinstance(entry, dict) or set(entry) != {'laneId', 'beforeTrackId'}
                or not isinstance(entry['laneId'], str) or not entry['laneId']
                or entry['laneId'] in seen
                or not (entry['beforeTrackId'] is None
                        or isinstance(entry['beforeTrackId'], str))):
            raise CommandError(f'{label} has invalid lane membership or identity',
                               kind='selection_changed', ref='parent')
        seen.add(entry['laneId'])
    return seen


def track_reorder_with_data_lane_placement_candidate(ctx, command):
    """Unregistered v2 source candidate for Main's mixed row reorder.

    The public v1 operation deliberately remains media-only.  This candidate
    records the same virtual track-order write plus the one authored App leaf;
    it is intentionally not present in ``operations()`` until App2/Runtime
    ACK the proposed wire shape.
    """
    if command.get('version') != '2' or command.get('select') != 'parent':
        raise CommandError('mixed track reorder candidate requires parent v2 command')
    args = command['args']
    if ('data_lane_placement' not in args
            or 'expected_data_lane_placement' not in args):
        raise CommandError('mixed track reorder requires both lane placement fields')

    expected = args['expected_data_lane_placement']
    desired = args['data_lane_placement']
    expected_ids = _validate_data_lane_placement(expected, label='expected data lane placement')
    desired_ids = _validate_data_lane_placement(desired, label='data lane placement')
    if desired_ids != expected_ids:
        raise CommandError('data-lane membership changed', kind='selection_changed', ref='parent')

    current = ctx.state.get('parent', _DATA_LANE_PLACEMENT_PATH)
    if current['state'] != 'present' or not isinstance(current.get('value'), dict):
        raise CommandError('mixed track reorder requires an existing authored lane placement',
                           kind='unsupported_dependency', ref='parent',
                           path=_DATA_LANE_PLACEMENT_PATH)
    if not equal(current['value'], expected):
        raise CommandError('original data-lane placement changed', kind='dependency_changed',
                           ref='parent', path=_DATA_LANE_PLACEMENT_PATH,
                           base=present(expected), theirs=current)

    # Validate every input before either authored carrier is changed.
    order_args = {'select': 'parent',
                  'args': {'order': args['order'], 'expected_order': args['expected_order']}}
    expected_order, desired_order = _validated_track_order(ctx, order_args)
    ctx.read('parent', _DATA_LANE_PLACEMENT_PATH)
    ctx.write('parent', ['track_order'], desired_order)
    ctx.write('parent', _DATA_LANE_PLACEMENT_PATH, desired)


def _validated_track_order(ctx, command):
    if command.get('select') != 'parent':
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
    return expected, desired


def track_reorder(ctx, command):
    """Replace the complete authored parent track permutation.

    The order is a virtual authored property. Raw track rows remain the
    carrier, so this handler never reconstructs or normalizes their payloads.
    """
    _, desired = _validated_track_order(ctx, command)
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


__all__ = [
    'capture_track_reorder', 'capture_track_set', 'order_for_parent', 'track_reorder',
    'track_reorder_with_data_lane_placement_candidate', 'track_set',
]
