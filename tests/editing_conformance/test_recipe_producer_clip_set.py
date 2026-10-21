"""Source-only Main-shaped producer updates for existing managed clips."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline._clip_scalar_commands import capture_clip_set
from astrid.sdk.timeline._command_state import CommandError, State
from astrid.sdk.timeline.commands import execute
from tests.editing_conformance.test_recipe_clip_scalar_fields import app_bundle
from tests.editing_conformance.test_recipe_m1_commands import clip, inverse

REF = 'parent/clip:f2-app-clip'
EXTENSION = 'haus.astrid.transcript-lane'
CONTRIBUTION = 'render-as-video-text'


def generated(source_revision='before'):
    return {
        'extensionId': EXTENSION,
        'contributionId': CONTRIBUTION,
        'provenance': {
            'contractVersion': 1,
            'sourceSchemaRef': 'astrid.transcript/v1',
            'sourceItemId': 'caption-1',
            'sourceFingerprint': 'astrid-fnv1a64-v1:source',
            'sourceRevision': source_revision,
            'generatorVersion': '1.0.0',
            'outputFingerprint': 'astrid-fnv1a64-v1:output',
            'conflictPolicy': 'regenerate-output',
        },
    }


def producer_bundle():
    bundle = app_bundle()
    for rows in (bundle['parent']['clips'], bundle['parent']['config']['clips']):
        row = next(item for item in rows if item['id'] == 'f2-app-clip')
        row.update({
            'clipType': 'text',
            'label': 'old caption',
            'text': {'content': 'old', 'fontSize': 42, 'color': '#fff', 'opaque': {'keep': True}},
            'app': {'opaque': {'keep': [None, False]}, 'managedBy': EXTENSION,
                    '__generated__': generated()},
        })
    return bundle


def update_values(source_revision='after'):
    return {
        'hold': 2.25,
        'label': 'new caption',
        'text': {'content': 'new', 'fontSize': 48, 'bold': True},
        'app': {'managedBy': EXTENSION, '__generated__': generated(source_revision)},
    }


def test_main_shaped_producer_capture_preserves_opaque_siblings_and_roundtrips():
    original = producer_bundle()
    before = copy.deepcopy(original)
    command = capture_clip_set(original, REF, values=update_values())
    assert command['args'] == {'values': update_values(), 'clear': []}
    assert command['expect'][REF + '::app.managedBy']['value'] == EXTENSION
    assert command['expect'][REF + '::app.__generated__']['value'] == generated()
    assert command['authorship'][REF + '::text.content'] == 'direct'

    plan = execute(original, [command])
    assert original == before
    updated = clip(plan.bundle, REF)
    assert updated['text'] == {
        'content': 'new', 'fontSize': 48, 'color': '#fff', 'bold': True, 'opaque': {'keep': True}}
    assert updated['app']['opaque'] == {'keep': [None, False]}
    assert updated['app']['managedBy'] == EXTENSION
    assert updated['app']['__generated__'] == generated('after')
    assert inverse(plan.bundle, plan.records).bundle == original
    assert inverse(inverse(plan.bundle, plan.records).bundle,
                   inverse(plan.bundle, plan.records).records).bundle == plan.bundle

    # The Main-shaped fixture is an authored bundle without a Runtime document
    # pin; a deep JSON reload is the honest source-only persistence boundary.
    reloaded = copy.deepcopy(plan.bundle)
    second = capture_clip_set(reloaded, REF, values=update_values('second'))
    second_plan = execute(reloaded, [second])
    assert clip(second_plan.bundle, REF)['app']['__generated__'] == generated('second')
    assert inverse(second_plan.bundle, second_plan.records).bundle == plan.bundle


def test_producer_metadata_refuses_user_foreign_and_identity_adoption_without_writes():
    for app in ({'opaque': True}, {'managedBy': 'other.extension', '__generated__': generated()}):
        original = producer_bundle()
        for rows in (original['parent']['clips'], original['parent']['config']['clips']):
            next(item for item in rows if item['id'] == 'f2-app-clip')['app'] = app
        before = copy.deepcopy(original)
        with pytest.raises(CommandError) as error:
            capture_clip_set(original, REF, values=update_values())
        assert error.value.kind == 'unsupported_ownership'
        assert original == before

    original = producer_bundle()
    changed = update_values()
    changed['app']['__generated__']['contributionId'] = 'other-contribution'
    with pytest.raises(CommandError) as error:
        capture_clip_set(original, REF, values=changed)
    assert error.value.kind == 'unsupported_ownership'


def test_producer_clip_shape_is_closed_and_geometry_stays_on_params_recipe():
    original = producer_bundle()
    with pytest.raises(CommandError):
        capture_clip_set(original, REF, values={'text': {'content': 'x', 'unknown': True}})
    with pytest.raises(CommandError):
        capture_clip_set(original, REF, values={'x': 10})
    params = execute(original, [
        capture_clip_set(original, REF, values={'text': {'content': 'x'}})]).bundle
    assert State(params).entity(REF)['text']['content'] == 'x'

