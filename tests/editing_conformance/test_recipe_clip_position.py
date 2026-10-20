"""Flat raw position leaves from the App position panel and reset handler."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from astrid.core.timeline.authoring_bundle import compile_authoring_candidate
from astrid.sdk.timeline._clip_scalar_commands import capture_clip_set
from astrid.sdk.timeline._command_state import ABSENT, CommandError, State, present
from astrid.sdk.timeline._scalar_commands import capture_clip_set_params
from astrid.sdk.timeline.commands import _SCHEMA, execute, operations
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_clip_scalar_fields import CHILD, app_bundle
from tests.editing_conformance.test_recipe_m1_commands import bundle, clip, inverse, later
from tests.sdk.command_schema_compatibility import compatibility_errors

FIELDS = ('x', 'y', 'width', 'height', 'cropTop', 'cropBottom', 'cropLeft', 'cropRight')
PARENT = 'parent/clip:f2-app-clip'
REF = 'occurrence:occ-1/clip:picture-1'
FIXTURE = Path(__file__).parent / 'fixtures/recipe_m2_app_clip_position.json'


def app_position_calls(original):
    # ClipPanelBody onChange({field: value}) writes these flat canvas-pixel
    # fields. useClipPositioning resets the box plus the four crop fractions.
    box = capture_clip_set(original, PARENT, values={'x': -120.5, 'y': 64, 'width': 1280, 'height': 720})
    positioned = execute(original, [box]).bundle
    crop = capture_clip_set(positioned, CHILD, values={'cropTop': .125, 'cropRight': .25})
    cropped = execute(positioned, [crop]).bundle
    reset = capture_clip_set(cropped, PARENT, clear=FIELDS)
    return [box, crop, reset]


def test_app_position_panel_and_reset_portable_golden():
    original = app_bundle()
    plan = execute(original, app_position_calls(original))
    fixture = json.loads(FIXTURE.read_text())
    assert fixture == {'bundle': original, 'commands': plan.commands, 'records': plan.records,
                       'after_bundle': plan.bundle}
    assert execute(fixture['bundle'], fixture['commands']).bundle == fixture['after_bundle']
    assert all(field not in clip(plan.bundle, PARENT) for field in FIELDS)
    assert clip(plan.bundle, CHILD) == dict(clip(original, CHILD), cropTop=.125, cropRight=.25)
    assert State(plan.bundle).config('occurrence:shared-sibling') == State(original).config('occurrence:shared-sibling')
    assert plan.bundle['source_mapping'] == original['source_mapping']
    undone = inverse(plan.bundle, plan.records)
    assert undone.bundle == original
    assert inverse(undone.bundle, undone.records).bundle == plan.bundle
    assert replay(plan, original).records == plan.records
    compile_authoring_candidate(plan.bundle)


@pytest.mark.parametrize('ref', ['parent/clip:direct', REF])
@pytest.mark.parametrize('field', FIELDS)
@pytest.mark.parametrize('old', [ABSENT, present(None), present(''), present('=canvas.width / 2'),
                                 present({'opaque': [None, False, 0]})])
def test_position_set_clear_exact_tagged_inverse_redo_and_opaque_preservation(ref, field, old):
    original = bundle(fps={'numerator': 30000, 'denominator': 1001})
    row = clip(original, ref)
    row.update({key: '=stored.expression' for key in FIELDS})
    row.update(x_vendor={'v': 2, 'data': [None, {'keep': False}]},
               app={'vendor.position/v1': {'keep': [None, 0]}}, position={'future': [None]})
    State(original).set(ref, [field], old)
    if ref.startswith('parent/'):
        original['parent']['config']['clips'] = copy.deepcopy(original['parent']['clips'])
    before = copy.deepcopy(original)
    for args in ({'values': {field: -4096.25}}, {'clear': [field]}):
        plan = execute(original, [capture_clip_set(original, ref, **args)])
        expected = copy.deepcopy(row)
        after = present(-4096.25) if 'values' in args else ABSENT
        if 'values' in args:
            expected[field] = -4096.25
        else:
            expected.pop(field, None)
        assert clip(plan.bundle, ref) == expected
        assert plan.records[0]['writes'] == [{'ref': ref, 'path': [field], 'before': old, 'after': after}]
        assert plan.commands[0]['expect'] == {ref + '::' + field: old}
        assert inverse(plan.bundle, plan.records).bundle == original
        undone = inverse(plan.bundle, plan.records)
        assert inverse(undone.bundle, undone.records).bundle == plan.bundle
        assert original == before


@pytest.mark.parametrize('field', FIELDS)
@pytest.mark.parametrize('value', [None, '', '12', '=canvas.width / 2', False, {}, [], float('inf'), float('nan')])
def test_position_set_rejects_non_numeric_or_nonfinite_authored_values(field, value):
    with pytest.raises(CommandError):
        capture_clip_set(bundle(), REF, values={field: value})


@pytest.mark.parametrize('values,clear', [({'position': {'x': 1}}, []), ({'position.x': 1}, []),
    ({'rotation': 1}, []), ({'x': 1}, ['x']), ({}, ['position']), ({}, ['x', 'x'])])
def test_position_args_remain_closed_and_set_clear_disjoint(values, clear):
    with pytest.raises(CommandError):
        capture_clip_set(bundle(), REF, values=values, clear=clear)


@pytest.mark.parametrize('other', ['y', 'width', 'cropLeft', 'hold', 'params'])
def test_position_disjoint_leaves_and_different_properties_rebase_without_recapture(other):
    original = bundle()
    plan = execute(original, [capture_clip_set(original, REF, values={'x': -10})])
    command = copy.deepcopy(plan.commands)
    change = (capture_clip_set_params(original, REF, values={'opaque': [None, 0]}) if other == 'params'
              else capture_clip_set(original, REF, values={other: 2}))
    concurrent = execute(original, [change])
    rebased = replay(plan, concurrent.bundle, intervening_records=concurrent.records)
    assert rebased.commands == command
    assert clip(rebased.bundle, REF)['x'] == -10
    assert inverse(rebased.bundle, rebased.records).bundle == concurrent.bundle
    assert clip(rebased.bundle, 'occurrence:occ-2/clip:picture-1') == clip(original, 'occurrence:occ-2/clip:picture-1')


def test_same_leaf_conflict_unchanged_write_and_history_aba_refusal():
    original = bundle()
    clip(original, REF)['x'] = 1
    plan = execute(original, [capture_clip_set(original, REF, values={'x': 1})])
    assert plan.bundle == original
    assert plan.records[0]['writes'] == [{'ref': REF, 'path': ['x'], 'before': present(1), 'after': present(1)}]
    changed = execute(original, [capture_clip_set(original, REF, values={'x': 2})])
    snapshot = copy.deepcopy(changed.bundle)
    with pytest.raises(CommandError):
        replay(plan, changed.bundle, intervening_records=changed.records)
    assert changed.bundle == snapshot
    for history in ([later(REF, ['x'], 1)], [later(REF, ['x'], 2), later(REF, ['x'], 1)]):
        assert replay(plan, original, intervening_records=history).commands == plan.commands
        with pytest.raises(CommandError, match='intervening'):
            inverse(plan.bundle, plan.records, history)


@pytest.mark.parametrize('change', ['clip', 'owner', 'source', 'type', 'media'])
def test_position_stable_target_and_later_dependency_changes_refuse_atomically(change):
    original = bundle()
    plan = execute(original, [capture_clip_set(original, REF, values={'x': 1})])
    for baseline, action in ((original, lambda head: replay(plan, head)),
                             (plan.bundle, lambda head: inverse(head, plan.records))):
        head = copy.deepcopy(baseline)
        if change == 'clip':
            clip(head, REF)['id'] = 'different'
        elif change == 'owner':
            head['placements'][0]['shot_id'] = head['placements'][1]['shot_id']
        elif change == 'source':
            head['source_mapping']['shots'][head['placements'][0]['shot_id']]['shot_id'] = 'different'
        elif change == 'type':
            clip(head, REF)['clipType'] = 'different'
        else:
            State(head).entity('occurrence:occ-1/registry')['assets']['old-picture']['media_id'] = 'different'
        before = copy.deepcopy(head)
        with pytest.raises(CommandError):
            action(head)
        assert head == before


def test_position_does_not_consume_or_rewrite_rational_timing_or_dynamic_old_values():
    original = bundle(fps={'numerator': 30000, 'denominator': 1001})
    row = clip(original, REF)
    row.update(at=1.001, hold=2.002, speed=2, x='=signal.position', y=None,
               app={'on': 'marker:beat', 'astrid': {'formulas': {'x': '=old'}, 'opaque': [None]}})
    plan = execute(original, [capture_clip_set(original, REF, values={'width': 0, 'height': -1, 'cropLeft': 2})])
    assert clip(plan.bundle, REF) == dict(row, width=0, height=-1, cropLeft=2)
    assert inverse(plan.bundle, plan.records).bundle == original
    assert plan.bundle['placements'] == original['placements']
    assert all(dep['kind'] != 'time-map' for dep in plan.records[0]['dependencies'])
    assert not any(read['path'] in [['at'], ['hold'], ['speed']] for read in plan.records[0]['reads'])
    before, after = (compile_authoring_candidate(value) for value in (original, plan.bundle))
    def timing(compilation):
        publication = compilation.publication
        configs = [publication['parent_composition'], *(
            image['payload'] for image in publication['internal_timeline_revisions'])]
        return sorted(json.dumps([{key: value for key, value in row.items() if key in (
            'id', 'at', 'hold', 'from', 'to', 'speed', 'app')}
            for row in config['clips']], sort_keys=True) for config in configs)
    assert timing(before) == timing(after)


def test_position_schema_is_closed_numeric_and_preserves_published_ordinary_args():
    # Frozen ordinary Runtime publication from 752c43ad; no item-reference schema import.
    published = Path(__file__).parents[1] / 'fixtures/published-command-schemas/runtime-0.2.3.json'
    assert compatibility_errors(json.loads(published.read_text()), _SCHEMA) == []
    args = operations()['clip.set'].parameters
    assert args['additionalProperties'] is False
    assert args['properties']['values']['additionalProperties'] is False
    raw = json.loads((Path(__file__).parents[2] / 'astrid/core/timeline/schema/timeline-config.schema.json').read_text())
    for field in FIELDS:
        assert raw['definitions']['TimelineClip']['properties'][field] == {'type': 'number'}
        Draft202012Validator(args).validate({'values': {field: -1e12}, 'clear': []})
        Draft202012Validator(args).validate({'values': {}, 'clear': [field]})
