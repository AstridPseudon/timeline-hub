"""New parameter edits must respect the selected immutable pack declaration."""
from __future__ import annotations

import copy
import json

import pytest
from jsonschema import Draft202012Validator

from astrid.core.element import project_packs
from astrid.core.timeline.authoring_bundle import AuthoringBundleError, compile_authoring_candidate
from astrid.sdk.timeline._clip_commands import capture_clip_add
from astrid.sdk.timeline._command_state import CommandError, State
from astrid.sdk.timeline._scalar_commands import capture_clip_set_params
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import bundle_from_document, create_runtime_commit_service
from tests.editing_conformance import test_recipe_scalar_commands as scalar_recipes
from tests.editing_conformance.test_recipe_m2_clip_add import empty_document
from tests.sdk.test_timeline_commit_provider import (
    CommitRejected,
    DetachedPort,
    DetachedRealm,
    inverse,
    track_create,
)
from tests.sdk.test_timeline_commit_provider import runtime_abi as runtime_abi
from tests.sdk.test_timeline_commit_provider_scalar import current

REF = 'parent/clip:effect'
admitted_param_revisions = scalar_recipes.admitted_param_revisions
configured_project_pack = scalar_recipes.configured_project_pack


def commit(realm, commands):
    context = realm.context(commands)
    # Use the same realm/project as the real admission fixture.
    context['realm_id'] = 'realm'
    return create_runtime_commit_service().commit(context, DetachedPort(realm, context))


@pytest.fixture
def selected_effect(admitted_param_revisions):
    _, selected = admitted_param_revisions
    record = project_packs.resolve_admitted_element('realm', 'project-1', selected)
    schema = record['descriptor']['schema']
    assert schema['properties']['seed']['maximum'] == 10
    Draft202012Validator(schema).validate({'seed': 4})
    Draft202012Validator(schema).validate({'seed': 8})
    errors = list(Draft202012Validator(schema).iter_errors({'seed': 16}))
    assert len(errors) == 1 and errors[0].validator == 'maximum'

    realm = DetachedRealm(empty_document())
    commit(realm, [track_create('picture')])
    row = {'id': 'effect', 'clipType': selected['id'], 'elementRef': selected,
           'at': 0, 'hold': 2, 'track': 'picture',
           'params': {'seed': 4, 'future': {'keep': [None, False, {}]}}}
    commit(realm, [capture_clip_add(current(realm), 'parent', row)])
    assert State(current(realm)).entity(REF) == row
    return realm, selected, schema


def test_new_valid_selected_param_compiles_commits_reloads_and_roundtrips(selected_effect):
    realm, selected, schema = selected_effect
    original = copy.deepcopy(realm.documents[realm.head['revision_id']])
    opaque = {'literal': [None, False, {}, 'ƒ(keep literal)']}
    command = capture_clip_set_params(current(realm), REF, values={'seed': 8, 'other': opaque})
    plan = execute(current(realm), [command])
    compile_authoring_candidate(plan.bundle)
    accepted = commit(realm, [command])
    assert accepted['data']['commands'] == [command]
    document = accepted['data']['canonical_document']
    reloaded = bundle_from_document(json.loads(json.dumps(document)))
    row = State(reloaded).entity(REF)
    assert row['elementRef'] == selected
    assert row['params'] == {'seed': 8, 'other': opaque, 'future': {'keep': [None, False, {}]}}
    Draft202012Validator(schema).validate(row['params'])
    assert project_packs.resolve_admitted_element(
        'realm', 'project-1', row['elementRef'])['descriptor']['schema'] == schema
    undone = commit(realm, [inverse([accepted['receipt']['receipt_id']])])
    assert undone['data']['canonical_document'] == original
    redone = commit(realm, [inverse([undone['receipt']['receipt_id']])])
    assert redone['data']['canonical_document'] == document


@pytest.mark.parametrize('stage', ['capture', 'compile', 'provider'])
# Requirement: validate newly authored declared values against the exact admitted
# owner/revision, while retaining unknown opaque data. Type-only lookup misses it.
@pytest.mark.xfail(strict=True, reason='selected admitted seed maximum is ignored by new parameter edits')
def test_new_invalid_selected_param_refuses_without_acceptance(selected_effect, stage):
    realm, selected, schema = selected_effect
    original = current(realm)
    before = copy.deepcopy((realm.head, realm.entries, realm.documents))
    assert State(original).entity(REF)['elementRef'] == selected
    assert list(Draft202012Validator(schema).iter_errors({'seed': 16}))
    with pytest.raises((CommandError, AuthoringBundleError, CommitRejected), match='seed|16|10'):
        command = capture_clip_set_params(original, REF, values={'seed': 16})
        if stage != 'capture':
            plan = execute(original, [command])
            compile_authoring_candidate(plan.bundle)
        if stage == 'provider':
            commit(realm, [command])
    assert (realm.head, realm.entries, realm.documents) == before
    assert current(realm) == original
