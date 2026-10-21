"""Lossless raw-config capture for the registered pristine initializer."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline._command_state import CommandError
from astrid.sdk.timeline._recording import Recording
from astrid.sdk.timeline.commands import execute, validate_command
from astrid.sdk.timeline.commit import bundle_from_document, document_from_bundle
from astrid.sdk.timeline.native_initialize import capture_initialize_raw, initialize
from tests.editing_conformance.test_pristine_initialize import empty_document

RAW_CONFIG = {
    'tracks': [],
    'theme_overrides': {
        'visual': {
            'canvas': {'width': 1920, 'height': 1080, 'fps': 30, 'background': None},
            'opaque_visual': {'enabled': False},
        },
        'opaque_theme': [None, False],
    },
    'opaque_sibling': {'literal': 'preserve-me'},
}


def raw_init_command(config=RAW_CONFIG):
    return {'schema_version': 1, 'op': 'timeline.init', 'version': '2',
            'select': 'parent',
            'args': {'name': 'Custom', 'slug': 'custom', 'config': copy.deepcopy(config)}}


def inverse(publications):
    return {'schema_version': 1, 'op': 'timeline.inverse', 'version': '1', 'select': None,
            'args': {'publications': publications}}


def test_raw_init_preserves_authored_config_through_reload_and_guarded_inverse():
    original = bundle_from_document(empty_document())
    command = capture_initialize_raw(original, name='Custom', slug='custom', config=RAW_CONFIG)
    validate_command(command)
    plan = execute(original, [command])

    assert [write['path'] for write in plan.records[0]['writes']] == [
        ['config'], ['name'], ['slug']]
    assert plan.bundle['parent']['config'] == RAW_CONFIG
    reloaded = bundle_from_document(document_from_bundle(plan.bundle))
    canvas = reloaded['parent']['config']['theme_overrides']['visual']['canvas']
    assert canvas == RAW_CONFIG['theme_overrides']['visual']['canvas']
    assert 'background_scale' not in canvas
    assert list(canvas) == ['width', 'height', 'fps', 'background']

    undone = execute(reloaded, [inverse(['accepted-raw-init'])], inverse_records=plan.records)
    assert (document_from_bundle(undone.bundle)['parent_revision']['payload']
            == empty_document()['parent_revision']['payload'])


@pytest.mark.parametrize(
    'path,value',
    [
        (('tracks',), [{'id': 'born-track', 'kind': 'visual'}]),
        (('clips',), [{'id': 'born-clip', 'track': 'born-track'}]),
        (('groups',), {'group-1': ['born-clip']}),
        (('media',), {'asset-1': {'media_id': 'sha256:born'}}),
        (('references',), {'ref-1': {'target': 'born-clip'}}),
        (('registry', 'assets'), {'asset-1': {'media_id': 'sha256:born'}}),
    ],
)
def test_structural_birth_is_refused_before_any_recorded_write(path, value):
    config = copy.deepcopy(RAW_CONFIG)
    node = config
    for token in path[:-1]:
        node[token] = {}
        node = node[token]
    node[path[-1]] = value
    original = bundle_from_document(empty_document())
    command = raw_init_command(config)
    validate_command(command)

    ctx = Recording(original, command, 0)
    with pytest.raises(CommandError) as error:
        initialize(ctx, command)
    assert error.value.kind == 'unrecorded_birth'
    assert ctx.record['writes'] == []
    with pytest.raises(CommandError) as error:
        execute(original, [command])
    assert error.value.kind == 'unrecorded_birth'


def test_raw_init_rejects_nonpristine_and_keeps_v2_args_closed():
    original = bundle_from_document(empty_document())
    changed = copy.deepcopy(original)
    changed['parent']['registry']['opaque'] = [None, False]
    with pytest.raises(CommandError) as error:
        capture_initialize_raw(changed, name='Custom', slug='custom', config=RAW_CONFIG)
    assert error.value.kind == 'not_pristine'

    invalid = raw_init_command()
    invalid['args']['output'] = {}
    with pytest.raises(CommandError):
        validate_command(invalid)

    initialized = execute(
        original,
        [capture_initialize_raw(original, name='Custom', slug='custom', config=RAW_CONFIG)],
    ).bundle
    with pytest.raises(CommandError) as error:
        capture_initialize_raw(initialized, name='Custom', slug='custom', config=RAW_CONFIG)
    assert error.value.kind == 'not_pristine'
