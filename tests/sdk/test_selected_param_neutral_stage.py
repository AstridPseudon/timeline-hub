"""Selected authority survives neutral native stages, never a different binding."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline._clip_scalar_commands import capture_clip_set
from astrid.sdk.timeline._command_state import CommandError, State
from astrid.sdk.timeline._selected_param_authority import resolve_selected_param_source
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import create_runtime_commit_service
from tests.sdk import test_timeline_selected_param_authority as selected
from tests.sdk.test_timeline_commit_provider import CommitRejected, DetachedPort
from tests.sdk.test_timeline_commit_provider import runtime_abi as runtime_abi

configured_project_pack = selected.configured_project_pack
two_pins = selected.two_pins
REF = selected.REF


def _sequence(element, options):
    return [
        {'schema_version': 1, 'op': 'clip.set-element', 'version': '1', 'select': REF,
         'args': {'elementRef': element, 'schema_source': options['schema_source']}},
        {'schema_version': 1, 'op': 'clip.set', 'version': '1', 'select': REF,
         'args': {'values': {'hold': 3}, 'clear': []}},
        selected._params(options, {'seed': 8}),
    ]


def _context(realm, calls, v2):
    context = realm.context(calls)
    context['realm_id'] = 'realm'
    if v2:
        context['request'].update(label='Select, hold and PARAM', merge='fields', reads=[],
            steps=[{'id': 'element', 'label': 'Update element', 'intent': '', 'tags': [],
                    'command_ordinals': list(range(len(calls))), 'patch': [], 'reads': []}])
    return context


@pytest.mark.parametrize('v2', [False, True])
def test_reselection_hold_param_preserves_exact_new_source(two_pins, v2):
    element, p1, p2 = two_pins
    realm = selected._realm(two_pins)
    selected._birth(realm, element)
    selected._reselect(realm, element, p1)
    before = copy.deepcopy(State(selected.current(realm)).entity(REF))
    calls = _sequence(element, p2)
    captured = execute(selected.current(realm), calls,
                       schema_inputs=p2['schema_inputs'], realm_id='realm').commands
    context = _context(realm, captured, v2)
    accepted = create_runtime_commit_service().commit(context, DetachedPort(realm, context))
    assert accepted['data']['commands'] == captured
    assert State(selected.current(realm)).entity(REF) == {
        **before, 'hold': 3, 'params': {'seed': 8}}
    authority = resolve_selected_param_source(DetachedPort(realm, context), context=context,
                                             through=realm.head, select=REF)
    assert authority == next(dep['pin'] for dep in realm.entries[-1]['records']['commands'][-1][
        'dependencies'] if dep['key'] == 'params.snapshot')
    assert authority['source'] == p2['schema_source']
    assert authority['element'] == element
    with pytest.raises(CommitRejected, match='source changed'):
        selected._commit(realm, [selected._params(p1, {'seed': 9})])


@pytest.mark.parametrize('damage', ['selection', 'source', 'owner', 'binding', 'history'])
def test_neutral_stage_cannot_repair_invalid_authority(two_pins, damage):
    element, p1, p2 = two_pins
    realm = selected._realm(two_pins)
    selected._birth(realm, element)
    selected._reselect(realm, element, p1)
    calls = _sequence(element, p2)[:2]
    if damage == 'selection':
        calls[0]['select'] = 'parent/clip:other'
    elif damage == 'source':
        calls[0]['args']['schema_source'] = p1['schema_source']
    elif damage == 'owner':
        calls[0]['args']['elementRef'] = {**element, 'packId': 'foreign'}
    elif damage == 'binding':
        calls[1]['bindings'] = {'scalar.target': 'parent/clip:other'}
    else:
        realm.entries[-1]['previous'] = copy.deepcopy(realm.entries[0]['previous'])
    calls.append(selected._params(p2, {'seed': 8}))
    before = copy.deepcopy((realm.head, realm.entries, realm.documents, realm.accepted))
    with pytest.raises(CommitRejected):
        selected._commit(realm, calls)
    assert (realm.head, realm.entries, realm.documents, realm.accepted) == before


def test_hold_without_selection_does_not_create_authority(two_pins):
    element, p1, _ = two_pins
    realm = selected._realm(two_pins)
    selected._birth(realm, element)
    before = copy.deepcopy((realm.head, realm.entries, realm.documents))
    with pytest.raises(CommitRejected, match='authority is unavailable'):
        selected._commit(realm, _sequence(element, p1)[1:])
    assert (realm.head, realm.entries, realm.documents) == before


def test_neutral_hold_keeps_accepted_authority(two_pins):
    element, p1, _ = two_pins
    realm = selected._realm(two_pins)
    selected._birth(realm, element)
    selected._reselect(realm, element, p1)
    hold = capture_clip_set(selected.current(realm), REF, values={'hold': 3})
    selected._commit(realm, [hold, selected._params(p1, {'seed': 8})])
    assert State(selected.current(realm)).entity(REF)['hold'] == 3


@pytest.mark.parametrize('path', [
    ['elementRef'], ['params'], ['id'], ['clipType'], ['asset'], ['source'], [],
])
def test_set_record_with_non_neutral_effect_invalidates_authority(two_pins, path):
    element, p1, _ = two_pins
    realm = selected._realm(two_pins)
    selected._birth(realm, element)
    selected._reselect(realm, element, p1)
    plan = execute(selected.current(realm), [capture_clip_set(
        selected.current(realm), REF, values={'hold': 3})])
    record = copy.deepcopy(plan.records[0])
    record['writes'][0]['path'] = path
    context = realm.context([])
    with pytest.raises(CommandError, match='authority is unavailable'):
        resolve_selected_param_source(DetachedPort(realm, context), context=context,
                                      through=realm.head, select=REF, staged=[record])


@pytest.mark.parametrize('damage', ['ref', 'policy', 'dependencies', 'duplicate', 'unknown'])
def test_v2_staged_association_keeps_strict_semantic_binding(two_pins, damage):
    element, _, p2 = two_pins
    realm = selected._realm(two_pins)
    selected._birth(realm, element)
    calls = _sequence(element, p2)[:2]
    context = _context(realm, calls, True)
    plan = execute(selected.current(realm), calls, schema_inputs=p2['schema_inputs'],
                   realm_id='realm', commit_request=context['request'], evaluated_head=realm.head)
    binding = next(item for item in plan.records[0]['bindings'] if item['key'] == 'params.element')
    assert binding['physical_ref'] == 'parent'
    assert binding['boundary']['command_ordinal'] == 0
    assert binding['path'] == ['config', 'clips', 'id:effect']
    port = DetachedPort(realm, context)
    authority = resolve_selected_param_source(port, context=context, through=realm.head,
                                             select=REF, staged=plan.records)
    assert authority['source'] == p2['schema_source']
    if damage == 'duplicate':
        plan.records[0]['bindings'].append(copy.deepcopy(binding))
    elif damage == 'unknown':
        binding['unauthenticated'] = True
    else:
        binding[damage] = {'ref': 'parent/clip:other', 'policy': 'floating',
                           'dependencies': ['params.schema']}[damage]
    before = copy.deepcopy((realm.head, realm.entries, realm.documents))
    with pytest.raises(CommandError, match='authority is unavailable'):
        resolve_selected_param_source(port, context=context, through=realm.head,
                                      select=REF, staged=plan.records)
    assert (realm.head, realm.entries, realm.documents) == before
