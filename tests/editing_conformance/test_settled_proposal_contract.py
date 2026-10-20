"""Design goldens only; no registered producer guard or Runtime acceptance yet."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from astrid.core.timeline.authoring_bundle import AuthoringBundleError
from astrid.sdk.timeline._recording import Recording
from astrid.sdk.timeline.capture import capture_move
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import _digest, _json
from tests.editing_conformance.test_recipe_m1_commands import inverse

FIXTURES = Path(__file__).parent / 'fixtures'
SCHEMA = json.loads((Path(__file__).parents[2]
                     / 'astrid/core/timeline/schema/edit-command.schema.json').read_text())
BATCH_SCHEMA = {**SCHEMA, '$ref': '#/$defs/CommandBatch'}


def golden():
    return json.loads((FIXTURES / 'settled_proposal_move.json').read_text())


def payload(proposal):
    return {key: value for key, value in proposal.items() if key != 'proposal_digest'}


def test_settled_move_golden_uses_existing_capture_execution_and_inverse():
    fixture = golden()
    source = json.loads((FIXTURES / fixture['source_fixture']).read_text())
    guard, *commands = fixture['commands']
    proposal, pin = guard['args']['proposal'], guard['args']['pin']
    command = capture_move(source['bundle'], source['select'], source['on'])
    assert commands == proposal['commands'] == [command]
    assert proposal['admitted_target'] == {
        'project_id': source['bundle']['project_id'],
        'timeline_id': source['bundle']['timeline_id'],
        'base_revision_id': source['bundle']['base_parent']['revision_id'],
        'base_publication_id': 'bootstrap-publication',
    }
    assert set(proposal) == {'schema_version', 'producer', 'admitted_target',
                             'commands', 'rationale', 'proposal_digest'}
    assert pin == {**proposal['producer'], 'admitted_target': proposal['admitted_target'],
                   'proposal_digest': _digest(payload(proposal))}
    assert pin['proposal_digest'] == proposal['proposal_digest']
    plan = execute(source['bundle'], commands)
    assert plan.bundle == source['after_bundle']
    assert inverse(plan.bundle, plan.records).bundle == source['bundle']
    assert execute(source['bundle'], commands).records == plan.records


def test_guard_fits_closed_envelope_and_authority_is_only_recorder_output():
    fixture = golden()
    guard = fixture['commands'][0]
    Draft202012Validator(BATCH_SCHEMA).validate(fixture['commands'])
    assert {key: value for key, value in guard.items() if key != 'args'} == {
        'schema_version': 1, 'op': 'producer.guard', 'version': '1', 'select': None,
    }
    assert set(guard['args']) == {'pin', 'proposal'}
    assert set(guard['args']['pin']) == {'task_id', 'attempt_id', 'executor_id', 'fence',
                                         'runtime_epoch', 'admitted_target', 'proposal_digest'}
    assert fixture['dependency'] == {
        'key': 'producer_attempt:assembler-task', 'kind': 'authority', 'policy': 'exact',
        'pin': guard['args']['pin'],
    }
    Draft202012Validator({**SCHEMA, '$ref': '#/$defs/AgentDependency'}).validate(
        fixture['dependency'])
    # This checks the existing recorder carrier, not task authority verification.
    source = json.loads((FIXTURES / fixture['source_fixture']).read_text())
    before = copy.deepcopy(source['bundle'])
    recorder = Recording(source['bundle'], guard, 0)
    recorder.dependency(fixture['dependency']['key'], 'authority', guard['args']['pin'])
    assert recorder.finish()['dependencies'] == [fixture['dependency']]
    assert recorder.finish()['writes'] == []
    assert source['bundle'] == before
    invalid = copy.deepcopy(fixture['commands'])
    invalid[0]['dependencies'] = [fixture['dependency']]
    assert not Draft202012Validator(BATCH_SCHEMA).is_valid(invalid)


@pytest.mark.parametrize('field,replacement', [
    ('args', {'on': 5}), ('select', 'parent/clip:substitute'), ('version', '2'),
    ('expect', {}), ('reads', []), ('selections', []), ('bindings', {}),
    ('created', ['parent/clip:reserved']), ('authorship', {}), ('intent', {}),
    ('rationale', 'requester changed reason'), ('group_id', 'another-group'),
    ('resolved', []), ('op', 'track.create'),
])
def test_digest_binds_all_settled_command_fields(field, replacement):
    proposal = golden()['commands'][0]['args']['proposal']
    changed = copy.deepcopy(proposal)
    changed['commands'][0][field] = replacement
    assert _digest(payload(changed)) != proposal['proposal_digest']


@pytest.mark.parametrize('scope,field,replacement', [
    ('producer', 'task_id', 'other-task'), ('producer', 'attempt_id', 'new-attempt'),
    ('producer', 'executor_id', 'other-executor'), ('producer', 'fence', 8),
    ('producer', 'runtime_epoch', 4), ('admitted_target', 'project_id', 'elsewhere'),
    ('admitted_target', 'timeline_id', 'other-film'),
    ('admitted_target', 'base_revision_id', 'new-revision'),
    ('admitted_target', 'base_publication_id', 'new-publication'),
])
def test_digest_binds_attempt_and_original_target(scope, field, replacement):
    proposal = golden()['commands'][0]['args']['proposal']
    changed = copy.deepcopy(proposal)
    changed[scope][field] = replacement
    assert _digest(payload(changed)) != proposal['proposal_digest']


def test_digest_binds_rationale_presence_order_and_extra_commands():
    proposal = golden()['commands'][0]['args']['proposal']
    for rationale in ('different', None):
        assert _digest({**payload(proposal), 'rationale': rationale}) != proposal['proposal_digest']
    without_reason = payload(proposal)
    del without_reason['rationale']
    assert _digest(without_reason) != proposal['proposal_digest']
    changed = copy.deepcopy(proposal)
    changed['commands'][0]['reads'].reverse()
    assert _digest(payload(changed)) != proposal['proposal_digest']
    changed = copy.deepcopy(proposal)
    changed['commands'].append(copy.deepcopy(changed['commands'][0]))
    assert _digest(payload(changed)) != proposal['proposal_digest']
    a = proposal['commands'][0]
    b = {**a, 'args': {'on': 5}}
    assert _digest([a, b]) != _digest([b, a])
    assert _digest({**payload(proposal), 'extra': None}) != proposal['proposal_digest']


def test_canonicalization_is_existing_finite_utf8_json_without_normalization():
    value = {'z': [None, True, 1, 1.0, -0.0, 0.000001], 'é': 'e\u0301', 'a': 'café'}
    expected = '{"a":"café","z":[null,true,1,1.0,-0.0,1e-06],"é":"é"}'
    assert _json(value).encode('utf-8') == expected.encode('utf-8')
    assert _json(dict(reversed(list(value.items())))) == expected
    assert _digest({'x': 'é'}) != _digest({'x': 'e\u0301'})
    assert _digest({'x': 1}) != _digest({'x': 1.0})


@pytest.mark.parametrize('value', [float('nan'), float('inf'), float('-inf')])
def test_nonfinite_proposal_cannot_have_a_digest(value):
    proposal = golden()['commands'][0]['args']['proposal']
    proposal['commands'][0]['args']['on'] = value
    with pytest.raises(AuthoringBundleError, match='finite JSON'):
        _digest(payload(proposal))
