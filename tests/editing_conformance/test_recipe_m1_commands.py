"""Executable M1 recipe contract on real main authoring bundles."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from astrid.core.timeline.authoring_bundle import (
    compile_authoring_candidate,
    open_authoring_bundle,
)
from astrid.sdk.timeline._command_state import (
    ABSENT,
    CommandError,
    State,
    address,
    equal,
    overlaps,
    present,
)
from astrid.sdk.timeline.capture import capture_move, capture_track_create
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.rebase import replay
from tests.timeline.test_authoring_bundle import _closure, _digest

FIXTURES = Path(__file__).parent / 'fixtures'


def bundle(*, shared=True, app='missing', fps=30):
    parent, shots, internals = _closure(shared=shared)
    parent['payload']['config']['output'] = {'fps': fps}
    for index, row in enumerate(parent['payload']['occurrences']):
        row['placement']['start_ms'] = 10000 + index * 10000
        row['duration_ms'] = 10000
        row['source_offset'], row['speed'] = 0, 1
    if app != 'missing':
        internals[0]['payload']['clips'][0]['app'] = copy.deepcopy(app)
        parent['payload']['clips'][0]['app'] = copy.deepcopy(app)
        parent['payload']['config']['clips'][0]['app'] = copy.deepcopy(app)
    for image in [parent, *shots, *internals]:
        image['content_digest'] = _digest(image['payload'])
    return open_authoring_bundle(parent, shot_revisions=shots, internal_timeline_revisions=internals)


def clip(bundle, ref='parent/clip:direct'):
    return State(bundle).entity(ref)


def inverse(bundle, records, intervening=()):
    return execute(bundle, [{'schema_version': 1, 'op': 'timeline.inverse', 'version': '1',
                             'select': None, 'args': {'publications': ['accepted-publication']}}],
                   inverse_records=records, intervening_records=intervening)


def later(ref, path, value):
    return {'writes': [{'ref': ref, 'path': path, 'before': present(value), 'after': present(value)}]}


@pytest.mark.parametrize('app', ['missing', None, {}, {'astrid': None},
                                 {'on': None, 'until': 'end', 'until_film_end': True, 'opaque': [True],
                                  'astrid': {'on': 'word:old:0', 'until': None, 'cut': 'cut-old',
                                             'until_film_end': None, 'opaque': {'a': 1}}}])
def test_exact_authored_move_inverse_redo(app):
    original = bundle(app=app)
    before = copy.deepcopy(original)
    command = capture_move(original, 'parent/clip:direct', 4)
    plan = execute(original, [command])
    assert original == before
    moved = clip(plan.bundle)
    assert moved['at'] == 4
    assert moved['app']['astrid']['fixed_start'] is True
    assert moved['app']['astrid']['for'] == 1
    for container in (moved['app'], moved['app']['astrid']):
        assert all(key not in container for key in ('on', 'until', 'until_film_end'))
    undone = inverse(plan.bundle, plan.records)
    assert undone.bundle == before
    redone = inverse(undone.bundle, undone.records)
    assert redone.bundle == plan.bundle
    assert replay(plan, before).bundle == plan.bundle
    assert replay(plan, before).records == plan.records


def test_same_value_writes_and_presence_are_authoritative():
    original = bundle(app={'astrid': {'fixed_start': True, 'for': 1}})
    command = capture_move(original, 'parent/clip:direct', 3)
    plan = execute(original, [command])
    assert plan.bundle == original
    writes = plan.records[0]['writes']
    assert any(w['path'] == ['at'] and equal(w['before'], w['after']) for w in writes)
    assert any(w['path'] == ['app', 'on'] and w['before'] == ABSENT == w['after'] for w in writes)
    assert all(command['authorship'][w['ref'] + '::' + ('.'.join(w['path']))] == 'direct' for w in writes)
    with pytest.raises(CommandError, match='intervening'):
        inverse(plan.bundle, plan.records, [later('parent/clip:direct', ['at'], 3)])


def test_trimmed_positive_speed_nonzero_occurrence_and_sibling_isolation():
    original = bundle()
    ref = 'occurrence:occ-1/clip:picture-1'
    target = clip(original, ref)
    target.pop('hold')
    target.update({'from': 2, 'to': 6, 'speed': 2, 'at': .5})
    sibling = copy.deepcopy(clip(original, 'occurrence:occ-2/clip:picture-1'))
    plan = execute(original, [capture_move(original, ref, 12.5)])
    moved = clip(plan.bundle, ref)
    assert moved['at'] == 2.5
    assert moved['app']['astrid']['for'] == 2
    assert (moved['from'], moved['to'], moved['speed']) == (2, 6, 2)
    assert clip(plan.bundle, 'occurrence:occ-2/clip:picture-1') == sibling
    assert inverse(plan.bundle, plan.records).bundle == original
    compilation = compile_authoring_candidate(plan.bundle)
    assert compilation.publication['parent_composition']['occurrences'][0]['placement']['start_ms'] == 10000


def test_quantization_once_with_rational_fps_and_ms_codec():
    original = bundle(fps={'numerator': 30000, 'denominator': 1001})
    target = clip(original)
    target['at_ms'] = target.pop('at') * 1000
    original['parent']['config']['clips'] = copy.deepcopy(original['parent']['clips'])
    plan = execute(original, [capture_move(original, 'parent/clip:direct', 1001 / 60000)])
    assert clip(plan.bundle)['at_ms'] == pytest.approx(1001 / 30)
    pin = next(d['pin'] for d in plan.records[0]['dependencies'] if d['key'] == 'move.quantization')
    assert pin['numerator'] == 30000 and pin['denominator'] == 1001
    assert inverse(plan.bundle, plan.records).bundle == original


@pytest.mark.parametrize('field,value,kind', [('speed', 0, 'unsupported_timing'),
                                            ('speed', -1, 'unsupported_timing'),
                                            ('speed', {'numerator': 1, 'denominator': 1}, 'unsupported_timing'),
                                            ('time_map', {'kind': 'piecewise'}, 'unsupported_map'),
                                            ('children', [], 'unsupported_map')])
def test_unsupported_child_maps_fail_precisely(field, value, kind):
    original = bundle()
    clip(original)[field] = value
    with pytest.raises(CommandError) as error:
        capture_move(original, 'parent/clip:direct', 4)
    assert error.value.kind == kind


@pytest.mark.parametrize('field,value', [('speed', 2), ('speed', {'numerator': 1, 'denominator': 1}),
                                       ('speed', True), ('source_offset', 100),
                                       ('source_offset', {'start': 2}), ('time_map', {})])
def test_unsupported_occurrence_maps_fail_closed(field, value):
    original = bundle()
    original['placements'][0][field] = value
    with pytest.raises(CommandError) as error:
        capture_move(original, 'occurrence:occ-1/clip:picture-1', 12)
    assert error.value.kind == 'unsupported_map'


@pytest.mark.parametrize('on', [9, 19.1, 20])
def test_complete_interval_must_fit_occurrence(on):
    original = bundle()
    with pytest.raises(CommandError) as error:
        capture_move(original, 'occurrence:occ-1/clip:picture-1', on)
    assert error.value.kind == 'occurrence_boundary'
    assert capture_move(original, 'occurrence:occ-1/clip:picture-1', 19)['args']['on'] == 19


def test_disjoint_same_child_rebase_and_original_guards_after_materialization():
    original = bundle()
    ref = 'occurrence:occ-1/clip:picture-1'
    a = execute(original, [capture_move(original, ref, 12)])
    b_command = capture_move(a.bundle, ref, 14)
    # A's first materialization gives each shared occurrence its real owner.
    publication = compile_authoring_candidate(a.bundle).publication
    head = open_authoring_bundle(
        {'project_id': original['project_id'], 'timeline_id': original['timeline_id'],
         'revision_id': publication['parent_revision_id'], 'content_digest': publication['content_digest'],
         'payload': publication['parent_composition']},
        shot_revisions=[dict(row, project_id=original['project_id']) for row in publication['shot_revisions']],
        internal_timeline_revisions=[dict(row, project_id=original['project_id']) for row in publication['internal_timeline_revisions']])
    clip(head, ref)['opaque_clip']['concurrent'] = 'other author'
    next(iter(head['source_mapping']['shots'].values()))['content_digest'] = 'sha256:' + 'f' * 64
    b = execute(head, [b_command])
    assert clip(b.bundle, ref)['at'] == 4
    assert clip(b.bundle, ref)['opaque_clip']['concurrent'] == 'other author'
    assert b.commands[0] == b_command
    head2 = copy.deepcopy(head)
    clip(head2, ref)['opaque_clip']['more'] = 'preserve'
    rebased = replay(b, head2)
    assert clip(rebased.bundle, ref)['opaque_clip']['more'] == 'preserve'
    changed = copy.deepcopy(head)
    clip(changed, ref)['at'] = 3
    with pytest.raises(CommandError) as error:
        execute(changed, [b_command])
    assert error.value.kind == 'dependency_changed'
    # Dependent handoff predicates allow equal-state A->A; accepted inverse does not.
    execute(head, [b_command])
    with pytest.raises(CommandError):
        replay(b, head, intervening_records=[later(ref, ['at'], 2)])


@pytest.mark.parametrize('change', ['owner', 'source', 'rate', 'blocker', 'order'])
def test_changed_map_source_owner_and_query_order_refuse(change):
    original = bundle()
    ref = 'occurrence:occ-1/clip:picture-1'
    plan = execute(original, [capture_move(original, ref, 12)])
    head = copy.deepcopy(original)
    if change == 'owner':
        head['placements'][0]['shot_id'] = head['placements'][1]['shot_id']
    elif change == 'source':
        State(head).entity('occurrence:occ-1/registry')['assets']['old-picture']['media_id'] = 'sha256:' + 'f' * 64
    elif change == 'rate':
        head['parent']['config']['output']['fps'] = 25
    elif change == 'blocker':
        added = copy.deepcopy(head['placements'][1])
        added['occurrence_id'] = 'new'
        head['placements'].append(added)
    else:
        head['placements'].reverse()
    with pytest.raises(CommandError):
        replay(plan, head)


def test_replay_permits_disjoint_and_rejects_leaf_ancestor_aba_and_noop():
    original = bundle(app={'opaque': {'x': 1}, 'astrid': {'opaque': 2}})
    plan = execute(original, [capture_move(original, 'parent/clip:direct', 4)])
    head = copy.deepcopy(original)
    clip(head)['app']['opaque']['x'] = 2
    assert clip(replay(plan, head).bundle)['app']['opaque']['x'] == 2
    for path in (['at'], ['app'], ['app', 'astrid', 'for'], ['track']):
        with pytest.raises(CommandError) as error:
            replay(plan, original, intervening_records=[later('parent/clip:direct', path, 3)])
        assert error.value.kind == 'intervening_write'
    inverse(plan.bundle, plan.records, [later('parent/clip:direct', ['opaque'], 1)])
    with pytest.raises(CommandError) as error:
        inverse(plan.bundle, plan.records, [later('parent/clip:direct', ['at'], 4)])
    assert error.value.kind == 'intervening_write'


def test_group_coalesces_intermediate_writes_without_capturing_other_work():
    original = bundle(app={'opaque': 'original'})
    a = execute(original, [capture_move(original, 'parent/clip:direct', 4)])
    b = capture_move(a.bundle, 'parent/clip:direct', 5)
    group = execute(original, [a.commands[0], b])
    head = copy.deepcopy(group.bundle)
    clip(head)['opaque_clip'] = {'later': True}
    head['parent']['config']['clips'] = copy.deepcopy(head['parent']['clips'])
    undone = inverse(head, group.records)
    expected = copy.deepcopy(original)
    clip(expected)['opaque_clip'] = {'later': True}
    expected['parent']['config']['clips'] = copy.deepcopy(expected['parent']['clips'])
    assert undone.bundle == expected
    assert inverse(undone.bundle, undone.records).bundle == head


def test_track_create_inverse_redo_exact_opaque_row_and_identity_collision():
    original = bundle()
    row = {'id': 'new', 'kind': 'visual', 'label': 'New track', 'opaque': {'keep': [None, True]}}
    command = capture_track_create(original, 'occurrence:occ-1', row)
    plan = execute(original, [command])
    assert plan.records[0]['created'] == [{'ref': 'occurrence:occ-1/track:new', 'kind': 'track', 'owner': 'occurrence:occ-1'}]
    assert inverse(plan.bundle, plan.records).bundle == original
    undone = inverse(plan.bundle, plan.records)
    assert inverse(undone.bundle, undone.records).bundle == plan.bundle
    assert replay(plan, original).bundle == plan.bundle
    occupied = copy.deepcopy(original)
    State(occupied).config('occurrence:occ-1')['tracks'].append(row)
    with pytest.raises(CommandError):
        replay(plan, occupied)
    with pytest.raises(CommandError, match='identity pairs'):
        replay(plan, original, id_map={'new': 'replacement'})
    assert replay(plan, original, id_map={'new': 'new'}).bundle == plan.bundle
    populated = copy.deepcopy(plan.bundle)
    State(populated).config('occurrence:occ-1')['clips'].append({'id': 'later', 'track': 'new', 'at': 0, 'hold': 1})
    with pytest.raises(CommandError) as error:
        inverse(populated, plan.records)
    assert error.value.kind == 'surviving_dependents'
    reordered = copy.deepcopy(plan.bundle)
    State(reordered).config('occurrence:occ-1')['tracks'].reverse()
    with pytest.raises(CommandError):
        inverse(reordered, plan.records)


def test_paths_json_equality_claims_and_frozen_schema():
    assert address('parent/clip:direct::app["a::b"].x', []) == ('parent/clip:direct', ('app', 'a::b', 'x'))
    assert address('app["astrid"].for', ['parent/clip:direct']) == ('parent/clip:direct', ('app', 'astrid', 'for'))
    assert overlaps(('x', ('params',)), ('x', ('params', 'x')))
    assert not overlaps(('x', ('params',)), ('x', ('paramsExtra',)))
    assert not equal(present(True), present(1))
    assert not equal(present(None), ABSENT)
    original = bundle()
    command = capture_move(original, 'parent/clip:direct', 4)
    alternate = copy.deepcopy(command)
    alternate['expect']['at'] = alternate['expect'].pop('parent/clip:direct::at')
    execute(original, [alternate])
    forged = copy.deepcopy(command)
    forged['reads'] = []
    with pytest.raises(CommandError) as error:
        execute(original, [forged])
    assert error.value.kind == 'capture_mismatch'
    schema = json.loads((Path(__file__).parents[2] / 'astrid/core/timeline/schema/edit-command.schema.json').read_text())
    Draft202012Validator(schema).validate(command)
    for unknown in ({'x': 1}, {'on': 4, 'relative': True}):
        bad = dict(command, args=unknown)
        with pytest.raises(CommandError):
            execute(original, [bad])
    with pytest.raises(CommandError):
        inverse(original, [])
    with pytest.raises(CommandError):
        inverse(original, [{'writes': []}], [None])


@pytest.mark.parametrize('name', ['recipe_m1_move.json', 'recipe_m1_occurrence.json', 'recipe_m1_shared.json'])
def test_published_capture_golden_fixture(name):
    fixture = json.loads((FIXTURES / name).read_text())
    command = capture_move(fixture['bundle'], fixture['select'], fixture['on'])
    assert command == fixture['command']
    assert execute(fixture['bundle'], [command]).bundle == fixture['after_bundle']


@pytest.mark.parametrize('codec', ['duration', 'duration_ms'])
def test_duration_codec_uses_main_positive_speed_semantics(codec):
    original = bundle()
    target = clip(original)
    target.pop('hold')
    target[codec] = 4 if codec == 'duration' else 4000
    target['speed'] = 2
    original['parent']['config']['clips'] = copy.deepcopy(original['parent']['clips'])
    plan = execute(original, [capture_move(original, 'parent/clip:direct', 4)])
    assert clip(plan.bundle)['app']['astrid']['for'] == 2
    assert plan.semantic_events == []
    assert inverse(plan.bundle, plan.records).bundle == original


def test_inverse_preserves_disjoint_app_fields_and_guards_real_owner_aba():
    original = bundle(app={'astrid': {'opaque': 'base'}, 'opaque': 'base'})
    ref = 'occurrence:occ-1/clip:picture-1'
    plan = execute(original, [capture_move(original, ref, 12)])
    head = copy.deepcopy(plan.bundle)
    clip(head, ref)['app']['astrid']['opaque'] = 'later author'
    clip(head, ref)['app']['opaque'] = 'later author'
    undone = inverse(head, plan.records, [later(ref, ['app', 'opaque'], 'later author')])
    assert clip(undone.bundle, ref)['at'] == 0
    assert clip(undone.bundle, ref)['app']['astrid']['opaque'] == 'later author'
    assert clip(undone.bundle, ref)['app']['opaque'] == 'later author'
    with pytest.raises(CommandError) as error:
        inverse(head, plan.records, [later('occurrence:occ-1', ['shot_id'], 'same-owner')])
    assert error.value.kind == 'intervening_write'
    with pytest.raises(CommandError):
        replay(plan, original, intervening_records=[later('parent', [], {})])


@pytest.mark.parametrize('dependency', ['audio', 'effects', 'audio_bindings', 'external'])
def test_track_inverse_checks_surviving_declared_reference_edges(dependency):
    original = bundle()
    plan = execute(original, [capture_track_create(original, 'occurrence:occ-1', {'id': 'new', 'kind': 'audio'})])
    head = copy.deepcopy(plan.bundle)
    if dependency in ('audio', 'effects'):
        State(head).config('occurrence:occ-1').setdefault(dependency, []).append({'track_id': 'new'})
    elif dependency == 'audio_bindings':
        owner = State(head).occurrence('occurrence:occ-1')['shot_id']
        head['shots'][owner]['payload']['audio_bindings'].append({'track_id': 'new'})
    else:
        clip(head, 'occurrence:occ-2/clip:picture-1')['track_ref'] = 'occurrence:occ-1/track:new'
    with pytest.raises(CommandError) as error:
        inverse(head, plan.records)
    assert error.value.kind == 'surviving_dependents'


def test_structural_group_uses_generic_creation_and_restores_order():
    original = bundle()
    a = capture_track_create(original, 'occurrence:occ-1', {'id': 'a', 'kind': 'visual'})
    first = execute(original, [a])
    b = capture_track_create(first.bundle, 'occurrence:occ-1', {'id': 'b', 'kind': 'audio'})
    group = execute(original, [a, b])
    undone = inverse(group.bundle, group.records)
    assert undone.bundle == original
    assert inverse(undone.bundle, undone.records).bundle == group.bundle
    head = copy.deepcopy(original)
    head['placements'][0]['shot_id'] = head['placements'][1]['shot_id']
    with pytest.raises(CommandError):
        replay(first, head)


def test_boolean_is_not_numeric_guard_and_atomic_failure_does_not_mutate():
    original = bundle()
    clip(original)['enabled'] = False
    command = capture_move(original, 'parent/clip:direct', 4)
    head = copy.deepcopy(original)
    clip(head)['enabled'] = 0
    with pytest.raises(CommandError):
        execute(head, [command])
    before = copy.deepcopy(original)
    with pytest.raises(CommandError):
        execute(original, [command, dict(command, args={'on': -1})])
    assert original == before
    assert execute(original, [dict(command, rationale='Keep this', group_id='gesture')]).commands[0]['rationale'] == 'Keep this'


def test_fixed_move_executes_without_runtime_or_renderer_imports():
    import os
    import subprocess
    import sys

    source = '''
import importlib.abc, json, sys
class Block(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, *args):
        if fullname.startswith(('astrid.packs.rendering', 'banodoco_workspace_client', 'runtime_protocol')):
            raise AssertionError('save imported ' + fullname)
sys.meta_path.insert(0, Block())
from astrid.sdk.timeline.commands import execute
f=json.load(open(sys.argv[1]))
assert execute(f['bundle'], [f['command']]).bundle == f['after_bundle']
'''
    result = subprocess.run([sys.executable, '-c', source, str(FIXTURES / 'recipe_m1_move.json')],
                            env={**os.environ, 'PYTHONPATH': str(Path(__file__).parents[2])},
                            capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr


def test_output_blockers_capture_activity_role_and_negative_membership():
    original = bundle()
    ref = 'occurrence:occ-1/clip:picture-1'
    original['placements'][1]['hidden'] = True
    plan = execute(original, [capture_move(original, ref, 22)])
    head = copy.deepcopy(original)
    head['placements'][1]['hidden'] = False
    with pytest.raises(CommandError) as error:
        replay(plan, head)
    assert error.value.kind == 'selection_changed'
    # Same-lane audio occurrences do not impose a picture boundary.
    original['parent']['config']['tracks'][0]['kind'] = 'audio'
    original['placements'][1]['hidden'] = False
    plan = execute(original, [capture_move(original, ref, 22)])
    head = copy.deepcopy(original)
    head['parent']['config']['tracks'][0]['kind'] = 'visual'
    with pytest.raises(CommandError):
        replay(plan, head)


@pytest.mark.parametrize('layout', ['both', 'payload', 'config', 'empty-payload', 'empty-config'])
def test_parent_clip_layout_and_recorded_mirror_survive_readback_inverse(layout):
    from astrid.core.timeline.shot_composition_projection import (
        project_runtime_parent_composition,
    )

    original = bundle()
    parent = original['parent']
    if layout == 'payload':
        parent['config'].pop('clips')
    elif layout == 'config':
        parent.pop('clips')
    elif layout == 'empty-payload':
        parent['clips'] = []
    elif layout == 'empty-config':
        parent['config']['clips'] = []
    command = capture_move(original, 'parent/clip:direct', 4)
    assert command['intent'] == {'ripple': 'none', 'anchor': 'fixed', 'position': 'absolute'}
    plan = execute(original, [command])
    derived = plan.records[0]['derived_writes']
    if layout == 'both':
        assert derived == [{'ref': 'parent', 'path': ['config', 'clips'],
                            'before': present(original['parent']['config']['clips']),
                            'after': present(plan.bundle['parent']['clips']), 'cause': 0}]
        assert plan.bundle['parent']['config']['clips'] == plan.bundle['parent']['clips']
    else:
        assert derived == []
    assert plan.semantic_events == []
    publication = compile_authoring_candidate(plan.bundle).publication
    project_runtime_parent_composition(
        {'project_id': original['project_id'], 'timeline_id': original['timeline_id'],
         'revision_id': publication['parent_revision_id'], 'payload': publication['parent_composition']},
        shot_revisions=publication['shot_revisions'],
        internal_timeline_revisions=publication['internal_timeline_revisions'])
    assert inverse(plan.bundle, plan.records).bundle == original
    assert replay(plan, original).records == plan.records


def test_semantic_owner_refuses_actual_source_change_and_inverse_source_aba():
    original = bundle()
    ref = 'occurrence:occ-1/clip:picture-1'
    plan = execute(original, [capture_move(original, ref, 12)])
    changed = copy.deepcopy(original)
    shot_id = changed['placements'][0]['shot_id']
    changed['source_mapping']['shots'][shot_id]['shot_id'] = 'different-source'
    with pytest.raises(CommandError):
        replay(plan, changed)
    with pytest.raises(CommandError) as error:
        inverse(plan.bundle, plan.records, [later('occurrence:occ-1', ['shot_id'], shot_id)])
    assert error.value.kind == 'intervening_write'


@pytest.mark.parametrize('kind', ['transcript', 'config'])
def test_compiler_records_exact_retained_document_pin_without_evaluating_anchor(kind):
    original = bundle(app={'astrid': {'on': 'word:old-source:word-1'}})
    content = {'retained': True}
    pin = {'document_id': 'retained:' + kind, 'version': 1, 'content_digest': _digest(content)}
    unused = dict(pin, document_id='unused')
    document_kind = 'media.transcript' if kind == 'transcript' else 'timeline.config'
    original['source_mapping'].update(
        _runtime_document={'dependency_manifest': {'documents': [pin]}},
        pinned_documents=[{'pin': p, 'document': {'kind': document_kind, 'content': content}}
                          for p in (pin, unused)])
    command = capture_move(original, 'parent/clip:direct', 4)
    plan = execute(original, [command])
    dependencies = plan.records[0]['dependencies']
    assert [d for d in dependencies if d['kind'] in ('transcript', 'source')] == [
        {'key': 'compile.document:' + _digest(pin),
         'kind': 'transcript' if kind == 'transcript' else 'source', 'pin': pin, 'policy': 'exact'}]
    assert not any(d['pin'] == unused for d in dependencies)
    assert next(d for d in dependencies if d['key'] == 'move.images')['kind'] == 'entity'
    assert clip(plan.bundle)['app']['astrid'].get('on') is None
    assert inverse(plan.bundle, plan.records).bundle == original


def test_shared_first_materialization_golden_preserves_original_sibling_capture():
    fixture = json.loads((FIXTURES / 'recipe_m1_shared.json').read_text())
    original, head = fixture['bundle'], fixture['head_bundle']
    ref = fixture['select']
    owner = ref.rsplit('/', 1)[0]
    assert State(original).occurrence(owner)['shot_id'] != State(head).occurrence(owner)['shot_id']
    assert State(original).entity(owner + '/shot') == State(head).entity(owner + '/shot')
    plan = execute(original, [fixture['command']])
    rebased = replay(plan, head)
    assert rebased.commands == [fixture['command']]
    assert rebased.bundle == fixture['rebased_bundle']
    undone = inverse(rebased.bundle, rebased.records)
    assert undone.bundle == head
    assert inverse(undone.bundle, undone.records).bundle == rebased.bundle



def test_materialization_alias_is_exact_for_arbitrary_source_ids():
    from astrid.core.timeline.authoring_bundle import _authoring_shot_id

    parent, shots, internals = _closure()
    source = 'shot-placement-' + 'a' * 64
    shots[0]['shot_id'] = source
    for index, row in enumerate(parent['payload']['occurrences']):
        row.update(shot_id=source, source_offset=0, speed=1)
        row['placement']['start_ms'] = index * 10000
    parent['content_digest'] = _digest(parent['payload'])
    original = open_authoring_bundle(parent, shot_revisions=shots,
                                     internal_timeline_revisions=internals)
    ref = 'occurrence:occ-1/clip:picture-1'
    command = capture_move(original, ref, 1)
    plan = execute(original, [command])
    read = next(r for r in command['reads'] if r['ref'] == 'occurrence:occ-1/shot')
    assert read['state'] == present(source)
    head = copy.deepcopy(original)
    old = head['placements'][0]['shot_id']
    materialized = _authoring_shot_id(original['project_id'], original['timeline_id'],
                                     'occ-1', source, shared=True)
    assert old == materialized
    head['source_mapping']['shots'][old]['shot_id'] = materialized
    assert replay(plan, head).commands == [command]
    head['source_mapping']['shots'][old]['shot_id'] = 'shot-placement-' + 'b' * 64
    with pytest.raises(CommandError):
        replay(plan, head)


@pytest.mark.parametrize('source', ['source-shot', 'shot-placement-' + 'a' * 64])
def test_reverse_materialization_alias_requires_exact_source_and_occurrence(source):
    from astrid.core.timeline.authoring_bundle import _authoring_shot_id

    parent, shots, internals = _closure()
    shots[0]['shot_id'] = source
    for row in parent['payload']['occurrences']:
        row['shot_id'] = source
    parent['content_digest'] = _digest(parent['payload'])
    original = open_authoring_bundle(parent, shot_revisions=shots,
                                     internal_timeline_revisions=internals)
    state = State(original)
    ref = 'occurrence:occ-1/shot'
    expected = present(_authoring_shot_id(original['project_id'], original['timeline_id'],
                                          'occ-1', source, shared=True))
    assert state.matches(ref, ['shot_id'], expected)
    assert not state.matches('occurrence:occ-2/shot', ['shot_id'], expected)
    for project, timeline, identity in [(original['project_id'], original['timeline_id'], 'other-source'),
                                       ('other-project', original['timeline_id'], source),
                                       (original['project_id'], 'other-timeline', source)]:
        unrelated = present(_authoring_shot_id(project, timeline, 'occ-1', identity, shared=True))
        assert not state.matches(ref, ['shot_id'], unrelated)
    owner = state.occurrence('occurrence:occ-1')['shot_id']
    original['source_mapping']['shots'][owner]['shot_id'] = 'other-source'
    with pytest.raises(CommandError) as error:
        state.matches(ref, ['shot_id'], expected)
    assert error.value.kind == 'identity_conflict'
