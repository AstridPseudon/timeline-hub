"""Current-policy first slice: exact inverse and final membership conflicts."""
import copy

import pytest

from astrid.sdk.timeline._command_state import CommandError, State
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.group_view import project_group_view
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_m1_commands import inverse, later
from tests.editing_conformance.test_recipe_m2_group_move import OWNER, capture, migrated


@pytest.mark.parametrize('change', ['birth', 'remove', 'reorder', 'lane-membership'])
def test_changed_membership_conflicts_atomically(change):
    _, _, bundle = migrated(second=True)
    plan = execute(bundle, capture(bundle))
    head = copy.deepcopy(bundle)
    rows = State(head).collection(OWNER, 'clip')
    if change == 'birth':
        rows.append({'id': 'later', 'at': 3, 'hold': 1, 'track': 'V1'})
    elif change == 'remove':
        rows.pop()
    elif change == 'reorder':
        rows.reverse()
    else:
        head['placements'][1]['track'] = 'V2'
        head['placements'][1]['placement']['track'] = 'V2'
    before = copy.deepcopy(head)
    with pytest.raises(CommandError):
        replay(plan, head)
    assert head == before


def test_lane_membership_aba_remains_strict_for_undo():
    _, _, bundle = migrated(second=True)
    plan = execute(bundle, capture(bundle))
    later_write = {'writes': [{'ref': 'occurrence:other-occ', 'path': ['track'],
                             'before': {'state': 'present', 'value': 'V3'},
                             'after': {'state': 'present', 'value': 'V2'}}]}
    with pytest.raises(CommandError, match='intervening'):
        inverse(plan.bundle, plan.records, [later_write])


def test_current_ordinary_equal_state_policy_does_not_weaken_inverse():
    _, _, bundle = migrated()
    plan = execute(bundle, capture(bundle))
    unchanged = later(OWNER + '/clip:c1', ['hold'], 2)
    assert project_group_view(replay(plan, bundle, intervening_records=[unchanged]).bundle) == project_group_view(plan.bundle)
    with pytest.raises(CommandError, match='intervening'):
        inverse(plan.bundle, plan.records, [unchanged])
