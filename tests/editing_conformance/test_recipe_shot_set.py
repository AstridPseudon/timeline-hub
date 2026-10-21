"""Native shot.set: occurrence-owned name/settings fields, exact presence and guarded inverse."""
from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from astrid.core.timeline.authoring_bundle import compile_authoring_candidate
from astrid.sdk.timeline._command_state import ABSENT, CommandError, State, present
from astrid.sdk.timeline._shot_commands import capture_shot_set
from astrid.sdk.timeline.commands import execute, operations
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_m1_commands import bundle, inverse, later
from tests.packs.video_editing.test_draft_voiceover import fixture as voiceover_fixture
from tests.packs.video_editing.test_draft_voiceover import synthesis, vo

FIXTURES = Path(__file__).parent / 'fixtures'
REF = 'occurrence:occ-1/shot'
OTHER = 'occurrence:occ-2/shot'
UNSUPPORTED = ('steerableMotionSettings', 'phaseConfig', 'pairConfigs', 'shotImageIds', 'loras',
               'structureVideo', 'modelSettingsByModel')


def payload(source, ref=REF):
    owner = ref.removesuffix('/shot')
    return source['shots'][State(source).occurrence(owner)['shot_id']]['payload']


def call(values=None, clear=(), ref=REF):
    return {'schema_version': 1, 'op': 'shot.set', 'version': '1', 'select': ref,
            'args': {'values': {} if values is None else values, 'clear': list(clear)}}


def test_registered_with_occurrence_only_intent():
    assert 'shot.set' in operations()
    command = capture_shot_set(bundle(), REF, values={'name': 'A'})
    assert command['intent'] == {'ownership': 'occurrence'}
    assert command['bindings'] == {'shot.owner': 'occurrence:occ-1'}


@pytest.mark.parametrize('container', [ABSENT, present(None), present({}),
                                      present({'prompt': 'Old', 'negativePrompt': None, 'x_unknown': [None, {}]})])
@pytest.mark.parametrize('mode', ['set', 'clear', 'null', 'empty'])
def test_exact_roundtrip_with_original_presence(container, mode):
    original = bundle()
    if container != ABSENT:
        payload(original)['settings'] = copy.deepcopy(container['value'])
    snapshot = copy.deepcopy(original)
    before = (container.get('value') or {}).get('prompt', ABSENT) if container != ABSENT else ABSENT
    before = present(before) if not isinstance(before, dict) else before
    values = {'set': {'prompt': 'New'}, 'null': {'prompt': None}, 'empty': {'prompt': ''}}.get(mode, {})
    command = capture_shot_set(original, REF, values={'settings': values} if values else {},
                               clear=['settings.prompt'] if mode == 'clear' else [])
    assert command['expect']['occurrence:occ-1/shot::payload.settings.prompt'] == before
    plan = execute(original, [command])
    assert original == snapshot
    expected = {'clear': ABSENT, 'set': present('New'), 'null': present(None),
                'empty': present('')}[mode]
    assert State(plan.bundle).get(REF, ['payload', 'settings', 'prompt']) == expected
    if container.get('value'):
        settings = payload(plan.bundle)['settings']
        assert settings.get('x_unknown', [None, {}]) == [None, {}]
        assert settings.get('negativePrompt', None) is None
    undone = inverse(plan.bundle, plan.records)
    assert undone.bundle == original
    assert inverse(undone.bundle, undone.records).bundle == plan.bundle
    assert replay(plan, original).records == plan.records
    assert execute(original, [plan.commands[0]]).records == plan.records


def test_clear_is_removal_and_distinct_from_empty_and_null():
    original = bundle()
    payload(original)['settings'] = {'prompt': 'Old'}
    outcomes = []
    for values, clear in (({'settings': {'prompt': ''}}, []), ({'settings': {'prompt': None}}, []),
                          ({}, ['settings.prompt'])):
        plan = execute(original, [capture_shot_set(original, REF, values=values, clear=clear)])
        outcomes.append(State(plan.bundle).get(REF, ['payload', 'settings', 'prompt']))
    assert outcomes == [present(''), present(None), ABSENT]
    assert 'prompt' not in payload(plan.bundle)['settings']


def test_name_and_coupled_settings_are_one_atomic_command_preserving_unmentioned_fields():
    original = bundle()
    payload(original)['settings'] = {'selectedModel': 'a', 'motionMode': 'basic', 'customWidth': 0,
                                    'x_unknown': {'__proto__': [1, 1]}}
    payload(original)['provenance']['name'] = 'Legacy'
    before = copy.deepcopy(payload(original))
    command = capture_shot_set(original, REF, values={
        'name': '', 'settings': {'selectedModel': 'b', 'motionMode': 'advanced', 'advancedMode': True}},
        clear=['settings.customWidth'])
    plan = execute(original, [command])
    result = payload(plan.bundle)
    assert result['name'] == '' and result['settings'] == {
        'selectedModel': 'b', 'motionMode': 'advanced', 'advancedMode': True,
        'x_unknown': {'__proto__': [1, 1]}}
    # The legacy name field is read-only compatibility data; shot.set never rewrites it.
    assert result['provenance'] == before['provenance']
    assert {key: value for key, value in result.items() if key not in ('name', 'settings')} == {
        key: value for key, value in before.items() if key not in ('name', 'settings')}
    assert inverse(plan.bundle, plan.records).bundle == original


def test_original_draft_voiceover_fixture_outcome_lowers_to_one_metadata_leaf():
    candidate, scripts = voiceover_fixture()
    scripts['occurrences'][0]['text'] = 'Long new narration'
    prepared = vo.prepare_draft_voiceover(candidate, scripts, synthesize=synthesis,
                                          timing_policy='ripple', padding_seconds=.15)
    draft = prepared['candidate']['shots']['s1']['payload']['metadata']['draft_voiceover']

    original = bundle(shared=False)
    metadata = payload(original)['metadata']
    metadata.update({'opaque': {'keep': [None, True]}, 'namespaced': {'future': 'value'}})
    command = capture_shot_set(original, REF, values={'metadata': {'draft_voiceover': draft}})
    plan = execute(original, [command])

    assert payload(plan.bundle)['metadata'] == {
        'draft_voiceover': draft,
        'opaque': {'keep': [None, True]},
        'namespaced': {'future': 'value'},
        'settings': {'look': 'warm'},
    }
    assert any(write['path'] == ['payload', 'metadata', 'draft_voiceover']
               for write in plan.records[0]['writes'])
    assert inverse(plan.bundle, plan.records).bundle == original


def test_draft_voiceover_clear_preserves_metadata_and_has_exact_inverse():
    original = bundle(shared=False)
    metadata = payload(original)['metadata']
    metadata.update({'draft_voiceover': {'text': 'old', 'duration': 2}, 'opaque': [1, None]})
    command = capture_shot_set(original, REF, clear=['metadata.draft_voiceover'])
    plan = execute(original, [command])
    assert payload(plan.bundle)['metadata'] == {'opaque': [1, None], 'settings': {'look': 'warm'}}
    assert inverse(plan.bundle, plan.records).bundle == original
    assert execute(original, [command]).records == plan.records


def test_draft_voiceover_disjoint_opaque_and_aba_guards():
    original = bundle(shared=False)
    draft = {'text': 'new', 'text_digest': 'sha256:' + 'a' * 64,
             'settings': {'rate': '+5%'}, 'audio_media_id': 'sha256:' + 'b' * 64,
             'run_id': 'run', 'task_id': 'task', 'base_head': 'h'}
    payload(original)['metadata']['opaque'] = {'keep': True}
    a = execute(original, [capture_shot_set(original, REF,
                                            values={'metadata': {'draft_voiceover': draft}})])
    b = execute(original, [capture_shot_set(original, REF,
                                            values={'settings': {'prompt': 'disjoint'}})])
    rebased = replay(b, a.bundle, intervening_records=a.records)
    assert payload(rebased.bundle)['metadata']['draft_voiceover'] == draft
    assert payload(rebased.bundle)['metadata']['opaque'] == {'keep': True}
    with pytest.raises(CommandError, match='intervening'):
        inverse(a.bundle, a.records, [later(REF, ['payload', 'metadata', 'draft_voiceover'], draft)])


@pytest.mark.parametrize('shared', [True, False])
def test_occurrence_only_isolation_and_compiled_shot_content(shared):
    original = bundle(shared=shared)
    payload(original)['settings'] = {'prompt': 'Old'}
    sibling = copy.deepcopy(payload(original, OTHER)) if shared else None
    plan = execute(original, [capture_shot_set(original, REF, values={'name': 'Mine', 'settings': {
        'prompt': 'New'}})])
    assert payload(plan.bundle)['name'] == 'Mine'
    if shared:
        assert payload(plan.bundle, OTHER) == sibling
        assert State(plan.bundle).occurrence('occurrence:occ-2')['shot_id'] != \
            State(plan.bundle).occurrence('occurrence:occ-1')['shot_id']
    published = compile_authoring_candidate(plan.bundle).publication
    names = sorted(row['payload']['name'] for row in published['shot_revisions'])
    assert names.count('Mine') == 1 and (names.count('Opening') == (1 if shared else 0))
    assert inverse(plan.bundle, plan.records).bundle == original


def test_unchanged_write_and_aba_allow_rebase_but_guard_inverse():
    original = bundle()
    payload(original)['settings'] = {'prompt': 'Same'}
    plan = execute(original, [capture_shot_set(original, REF, values={'settings': {'prompt': 'Same'}})])
    assert plan.bundle == original
    path = ['payload', 'settings', 'prompt']
    assert any(w['path'] == path and w['before'] == w['after'] for w in plan.records[0]['writes'])
    for history in ([later(REF, path, 'Same')], [later(REF, path, 'away'), later(REF, path, 'Same')]):
        with pytest.raises(CommandError, match='intervening'):
            inverse(plan.bundle, plan.records, history)
        assert replay(plan, original, intervening_records=history).records == plan.records


def test_disjoint_leaf_rebase_and_inverse_but_same_leaf_conflicts():
    original = bundle()
    payload(original)['settings'] = {'prompt': 'Old', 'turboMode': True}
    a = execute(original, [capture_shot_set(original, REF, values={'settings': {'prompt': 'A'}})])
    b = execute(original, [capture_shot_set(original, REF, values={'settings': {'turboMode': False}})])
    result = replay(b, a.bundle, intervening_records=a.records)
    assert payload(result.bundle)['settings'] == {'prompt': 'A', 'turboMode': False}
    assert result.commands == b.commands
    assert inverse(result.bundle, result.records).bundle == a.bundle
    clash = execute(original, [capture_shot_set(original, REF, values={'settings': {'prompt': 'B'}})])
    with pytest.raises(CommandError):
        replay(clash, a.bundle, intervening_records=a.records)


@pytest.mark.parametrize('change', ['value', 'name', 'container', 'owner', 'source', 'delete'])
def test_original_guards_refuse_without_partial_writes(change):
    original = bundle()
    payload(original)['settings'] = {'prompt': 'Old'}
    command = capture_shot_set(original, REF, values={'name': 'N', 'settings': {'prompt': 'New'}})
    head = copy.deepcopy(original)
    if change == 'value':
        payload(head)['settings']['prompt'] = 'Theirs'
    elif change == 'name':
        payload(head)['name'] = 'Theirs'
    elif change == 'container':
        payload(head)['settings'] = ['array']
    elif change == 'owner':
        head['placements'][0]['shot_id'] = head['placements'][1]['shot_id']
    elif change == 'source':
        head['source_mapping']['shots'][head['placements'][0]['shot_id']]['shot_id'] = 'other-source'
    else:
        head['placements'].pop(0)
    snapshot = copy.deepcopy(head)
    with pytest.raises(CommandError):
        execute(head, [command])
    assert head == snapshot


@pytest.mark.parametrize('container', [[], 'text', False, 0])
def test_set_refuses_nonobject_settings_root(container):
    original = bundle()
    payload(original)['settings'] = container
    with pytest.raises(CommandError):
        capture_shot_set(original, REF, values={'settings': {'prompt': 'x'}})


@pytest.mark.parametrize('damage', ['unknown-arg', 'missing-clear', 'overlap', 'name-overlap', 'empty',
                                   'empty-settings', 'duplicate', 'shared-select', 'shot-root', 'unscoped',
                                   'version', 'shared-intent', 'unknown-key', 'legacy-name',
                                   'wrong-type', 'name-null', 'nan', 'unknown-clear'])
def test_closed_schema_and_semantic_args_refuse(damage):
    command = call({'settings': {'prompt': 'x'}, 'name': 'N'})
    if damage == 'unknown-arg':
        command['args']['settings'] = {}
    elif damage == 'missing-clear':
        del command['args']['clear']
    elif damage == 'overlap':
        command['args']['clear'] = ['settings.prompt']
    elif damage == 'name-overlap':
        command['args']['clear'] = ['name']
    elif damage == 'empty':
        command['args'] = {'values': {}, 'clear': []}
    elif damage == 'empty-settings':
        command['args'] = {'values': {'settings': {}}, 'clear': []}
    elif damage == 'duplicate':
        command['args'] = {'values': {}, 'clear': ['name', 'name']}
    elif damage == 'shared-select':
        command['select'] = 'shot:source'
    elif damage == 'shot-root':
        command['select'] = 'parent'
    elif damage == 'unscoped':
        command['select'] = 'shot'
    elif damage == 'version':
        command['version'] = '2'
    elif damage == 'shared-intent':
        command['intent'] = {'ownership': 'shared'}
    elif damage == 'unknown-key':
        command['args']['values']['settings']['x_other'] = 1
    elif damage == 'legacy-name':
        command['args']['values']['provenance'] = {'name': 'Legacy'}
    elif damage == 'wrong-type':
        command['args']['values']['settings']['turboMode'] = 'yes'
    elif damage == 'name-null':
        command['args']['values']['name'] = None
    elif damage == 'nan':
        command['args']['values']['settings']['prompt'] = float('nan')
    else:
        command['args'] = {'values': {}, 'clear': ['settings.loras']}
    original = bundle()
    snapshot = copy.deepcopy(original)
    with pytest.raises(CommandError):
        execute(original, [command])
    assert original == snapshot


@pytest.mark.parametrize('key', UNSUPPORTED)
def test_compound_settings_roots_are_unsupported_set_or_clear(key):
    original = bundle()
    with pytest.raises(CommandError):
        capture_shot_set(original, REF, values={'settings': {key: []}})
    with pytest.raises(CommandError):
        capture_shot_set(original, REF, clear=['settings.' + key])


def test_mixed_supported_and_unsupported_batch_refuses_atomically():
    original = bundle()
    commands = [call({'name': 'ok'}), call({'settings': {'loras': []}})]
    with pytest.raises(CommandError):
        execute(original, commands)


def test_portable_shot_set_golden():
    fixture = json.loads((FIXTURES / 'recipe_m2_shot_set.json').read_text())
    plan = execute(fixture['bundle'], [fixture['command']])
    assert plan.commands == [fixture['command']]
    assert execute(fixture['bundle'], [fixture['request']]).commands == plan.commands
    assert plan.bundle == fixture['after_bundle']
    schema = json.loads((Path(__file__).parents[2] / 'astrid/core/timeline/schema/edit-command.schema.json').read_text())
    Draft202012Validator(schema).validate(fixture['command'])
    assert inverse(plan.bundle, plan.records).bundle == fixture['bundle']
    assert replay(plan, fixture['head_bundle']).bundle == fixture['rebased_bundle']
    compiled = compile_authoring_candidate(plan.bundle).publication
    assert compiled['shot_revisions'] == fixture['compiled_shot_revisions']


def test_shot_set_capture_and_save_import_no_renderer_or_runtime():
    script = '''
import json, sys
class Block:
    def find_spec(self, fullname, *args):
        if fullname.startswith(('runtime_protocol', 'composition', 'remotion', 'astrid.packs.rendering',
                                'astrid.sdk.authoring_render_preview', 'astrid.core.timeline.compatibility')) or '.scene' in fullname:
            raise AssertionError(fullname)
sys.meta_path.insert(0, Block())
from astrid.sdk.timeline.commands import execute
for path in sys.argv[1:]:
    f = json.load(open(path))
    assert execute(f['bundle'], [f['request']]).commands == [f['command']]
'''
    result = subprocess.run([sys.executable, '-c', script,
                             *map(str, sorted(FIXTURES.glob('recipe_m2_shot_set.json')))],
                            env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'},
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
