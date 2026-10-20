"""Regenerate/check parent-only delete cases with frozen Agent 027bd16d on PYTHONPATH."""
import copy
import json
import sys
from pathlib import Path

from astrid.sdk.timeline.capture import capture_clip_delete
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline._command_state import CommandError
from astrid.sdk.timeline.commit import bundle_from_document
from tests.editing_conformance.test_recipe_clip_delete import delete_document

TARGET = Path(__file__).with_name('recipe_m2_app_clip_delete.json')
AGENT = '027bd16d96010544331c953c0e1014e161786e71'


def main():
    stored = json.loads(TARGET.read_text())
    original = stored['bundle']
    cases = []

    def add(name, bundle, select=stored['select']):
        before = copy.deepcopy(bundle)
        command = capture_clip_delete(bundle, select)
        plan = execute(bundle, [command])
        assert bundle == before, name
        cases.append(dict(name=name, bundle=bundle, select=select, command=command,
                          record=plan.records[0], after_bundle=plan.bundle))

    add('whole-row', copy.deepcopy(original))
    final = copy.deepcopy(original)
    row = copy.deepcopy(final['parent']['clips'][1])
    row['id'] = 'raw:clip-b'
    final['parent']['clips'] = [copy.deepcopy(row)]
    final['parent']['config']['clips'] = [copy.deepcopy(row)]
    add('final-colon-row', final, 'parent/clip:raw:clip-b')
    for name, key in [('config-only', 'clips'), ('payload-only', 'config')]:
        value = copy.deepcopy(original)
        if key == 'clips':
            del value['parent']['clips']
        else:
            del value['parent']['config']['clips']
        add(name, value)
    nulls = copy.deepcopy(original)
    for row in nulls['parent']['clips']:
        row['transition'] = None
        row['app'] = {'on': None, 'astrid': {'duck': None}, 'canonical': {'ownerRef': 'opaque'}}
    nulls['parent']['config']['clips'] = copy.deepcopy(nulls['parent']['clips'])
    add('null-relations-opaque-identity', nulls)
    for name, key in [('null-payload', 'clips'), ('null-mirror', 'config')]:
        value = copy.deepcopy(original)
        if key == 'clips':
            value['parent']['clips'] = None
        else:
            value['parent']['config']['clips'] = None
        add(name, value)
    child_bundle = bundle_from_document(delete_document())
    add('retained-occurrence-closure', child_bundle)

    refusals = []

    def refuse(name, bundle=None, select=None, command=None):
        bundle = copy.deepcopy(original if bundle is None else bundle)
        supplied = command or dict(schema_version=1, op='clip.delete', version='1',
                                   select=stored['select'] if select is None else select, args={}, intent={})
        before = copy.deepcopy(bundle)
        try:
            execute(bundle, [supplied])
        except CommandError as error:
            refusals.append(dict(name=name, bundle=bundle, command=supplied, kind=error.kind))
        else:
            raise AssertionError(('native accepted unsupported input', name))
        assert before == bundle, name

    for select in ['parent', 'clip-b', 'parent/clip:', 'parent/clip:clip-b/extra',
                   'parent/clip:clip-a::x', 'occurrence:occ-a/clip:clip-b', 'shot:s/clip:clip-b', 'parent/clip:missing']:
        refuse('scope:' + select, select=select)
    for key, value in [('clipType', 'shot'), ('clip_type', 'shot'), ('clips', []), ('children', {})]:
        bundle = copy.deepcopy(original)
        bundle['parent']['clips'][1][key] = value
        bundle['parent']['config']['clips'] = copy.deepcopy(bundle['parent']['clips'])
        refuse('ownership:' + key, bundle)
    for prefix in [['app'], ['app', 'astrid']]:
        for key in ['on', 'until', 'until_film_end', 'cut', 'formulas', 'sequence', 'sequence_index',
                    'sequence_fit', 'sequence_shape_from', 'segment', 'words', 'beats', 'slot',
                    'replaces', 'standin', 'standin_for', 'intended', 'group', 'duck']:
            bundle = copy.deepcopy(original)
            row = bundle['parent']['clips'][0]
            for part in prefix:
                row = row.setdefault(part, {})
            row[key] = 'clip-b'
            bundle['parent']['config']['clips'] = copy.deepcopy(bundle['parent']['clips'])
            refuse('relation:' + '.'.join([*prefix, key]), bundle)
    for prefix in [[], ['app'], ['app', 'astrid']]:
        for key in ['sequences', 'formulas', 'slots']:
            bundle = copy.deepcopy(original)
            config = bundle['parent']['config']
            for part in prefix:
                config = config.setdefault(part, {})
            config[key] = ['declared']
            refuse('config:' + '.'.join([*prefix, key]), bundle)
    for key, value in [('pinnedShotGroups', [{'id': 'g'}])]:
        bundle = copy.deepcopy(original)
        bundle['parent']['config'][key] = value
        refuse(key, bundle)
    bundle = copy.deepcopy(original)
    bundle['parent']['clips'][0]['transition'] = {'id': 'crossfade'}
    bundle['parent']['config']['clips'] = copy.deepcopy(bundle['parent']['clips'])
    refuse('neighbor-transition', bundle)
    bundle = copy.deepcopy(original)
    bundle['parent']['config']['clips'].reverse()
    refuse('divergent-mirrors', bundle)
    bundle = copy.deepcopy(original)
    bundle['parent']['clips'][0]['id'] = 'clip-b'
    bundle['parent']['config']['clips'] = copy.deepcopy(bundle['parent']['clips'])
    refuse('duplicate-identity', bundle)
    bundle = copy.deepcopy(original)
    bundle['parent']['config'] = None
    refuse('null-owner', bundle)
    for identity in ['', 'bad/id', 'bad::id', None, 7]:
        bundle = copy.deepcopy(original)
        bundle['parent']['clips'][0]['id'] = identity
        bundle['parent']['config']['clips'] = copy.deepcopy(bundle['parent']['clips'])
        refuse('invalid-member:' + repr(identity), bundle)
    bundle = copy.deepcopy(original)
    bundle['parent']['clips'][0] = None
    bundle['parent']['config']['clips'] = copy.deepcopy(bundle['parent']['clips'])
    refuse('nonobject-member', bundle)
    bundle = copy.deepcopy(original)
    del bundle['parent']['clips']
    del bundle['parent']['config']['clips']
    refuse('absent-collection', bundle)
    for key, value in [('transition', {'id': 'fade'}), ('app', {'astrid': {'on': 'clip-b'}})]:
        bundle = copy.deepcopy(child_bundle)
        next(iter(bundle['shots'].values()))['internal_timeline']['clips'][0][key] = value
        refuse('child-dependency:' + key, bundle)
    for key, value in [('args', {'unknown': None}), ('intent', {'ripple': 'following'}), ('unexpected', None)]:
        command = dict(schema_version=1, op='clip.delete', version='1', select=stored['select'], args={}, intent={})
        command[key] = value
        refuse('envelope:' + key, command=command)

    expected = {**{key: stored[key] for key in ['bundle', 'select']}, 'agent_source': AGENT,
                'command': cases[0]['command'], 'records': [cases[0]['record']],
                'after_bundle': cases[0]['after_bundle'], 'cases': cases, 'refusals': refusals}
    encoded = json.dumps(expected, ensure_ascii=False, allow_nan=False, separators=(',', ':')) + '\n'
    if sys.argv[1:] == ['--update']:
        TARGET.write_text(encoded)
    elif sys.argv[1:]:
        raise SystemExit('usage: clip_delete_parity.py [--update]')
    else:
        assert TARGET.read_text() == encoded, 'native parent-delete golden changed'
    print(f'{len(cases)} exact native commands/records/full after-bundles; {len(refusals)} atomic native refusals verified ({AGENT})')


if __name__ == '__main__':
    main()
