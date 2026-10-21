"""Native track collection recipes and compatibility exports."""
from __future__ import annotations

import copy

from ._collections import order
from ._command_state import ABSENT, CommandError, equal, present
from ._scalar_commands import capture_track_set, track_set

_DATA_LANE_PLACEMENT_PATH = ['config', 'app', 'timelineDataLanePlacement']


def _validate_data_lane_placement(value, *, label):
    """Validate Main's authored lane-placement leaf without normalizing it."""
    if value is None:
        return set()
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


def _layout_data_lane_placement(value, track_ids, *, label):
    """Apply Main's read-side empty/unknown-anchor interpretation.

    This is only a comparison view.  The recorder always receives the raw
    authored value, so an unknown anchor is not rewritten as ``None``.
    Structurally malformed data still refuses visibly instead of being
    silently discarded like a permissive UI projection.
    """
    if value is None:
        return {'version': 1, 'lanes': []}
    _validate_data_lane_placement(value, label=label)
    return {
        'version': 1,
        'lanes': [
            {
                'laneId': entry['laneId'],
                'beforeTrackId': (entry['beforeTrackId']
                                  if entry['beforeTrackId'] is None
                                  or entry['beforeTrackId'] in track_ids else None),
            }
            for entry in value['lanes']
        ],
    }


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
    if 'data_lane_placement' not in args:
        raise CommandError('mixed track reorder requires the lane placement field')

    expected_supplied = 'expected_data_lane_placement' in args
    expected = args.get('expected_data_lane_placement')
    desired = args['data_lane_placement']

    current = ctx.state.get('parent', _DATA_LANE_PLACEMENT_PATH)
    if current == ABSENT:
        if expected_supplied:
            raise CommandError('original data-lane placement changed', kind='dependency_changed',
                               ref='parent', path=_DATA_LANE_PLACEMENT_PATH,
                               base=present(expected), theirs=current)
        current_value = None
    else:
        current_value = current.get('value')
        if current_value is not None and not isinstance(current_value, dict):
            raise CommandError('authored data-lane placement has unsupported shape',
                               kind='unsupported_dependency', ref='parent',
                               path=_DATA_LANE_PLACEMENT_PATH)
        if not expected_supplied or not equal(current_value, expected):
            raise CommandError('original data-lane placement changed', kind='dependency_changed',
                               ref='parent', path=_DATA_LANE_PLACEMENT_PATH,
                               base=present(expected) if expected_supplied else ABSENT,
                               theirs=current)

    # Validate the complete track permutation before using its IDs to mirror
    # Main's unknown-anchor-to-null layout rule.  The raw values remain the
    # values written below.
    _, desired_order = _validated_track_order(ctx, {
        'select': 'parent',
        'args': {'order': args['order'], 'expected_order': args['expected_order']},
    })
    track_ids = {ref.rsplit(':', 1)[1] for ref in args['expected_order']}
    current_layout = _layout_data_lane_placement(
        current_value, track_ids, label='current data lane placement')
    desired_layout = _layout_data_lane_placement(
        desired, track_ids, label='data lane placement')
    current_ids = {entry['laneId'] for entry in current_layout['lanes']}
    desired_ids = {entry['laneId'] for entry in desired_layout['lanes']}
    # Main materializes visible lanes omitted from absent/null/empty metadata;
    # only a non-empty authored list can provide a membership guard here.
    if current_ids and desired_ids != current_ids:
        raise CommandError('data-lane membership changed', kind='selection_changed', ref='parent')

    # Validate every input before either authored carrier is changed.
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
