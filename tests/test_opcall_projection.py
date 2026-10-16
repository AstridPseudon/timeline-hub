"""Current admitted OpCall schema equivalence, without handler interpretation."""
import copy
import importlib.util
import json
import shutil
import sys
import subprocess
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from generators import generate
from runtime_protocol.edit_command import validate_edit_command, validate_edit_command_bytes

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'conformance/fixtures/opcall'
BASE = {'op': 'timeline.set', 'select': 'parent/clip:c1', 'args': {}}


def cases():
    values = []
    for kind in ['valid', 'invalid']:
        for path in sorted((FIXTURES / kind).glob('*.json')):
            values.append((path.name, json.loads(path.read_bytes())['instance'], kind == 'valid'))
    for suffix in ['\n', '\r', '\r\n', '\u2028', '\u2029']:
        values.append(('op-line-ending-' + repr(suffix), {**BASE, 'op': 'timeline.set' + suffix}, suffix == '\n'))
    values.append(('all-fields', {**BASE, 'expect': {'x': {'state': 'absent'}, 'null': {'state': 'present', 'value': None}, 'opaque': {'state': 'present', 'value': {'$absent': True}}},
                   'created': ['parent/clip:new', 'shot:s1/track:t1', 'occurrence:o1/clip:c1', 'cut:k'],
                   'resolved': ['parent/clip:c1'], 'bindings': {'"viral"': 'word:s1:2', 'beat': 'beat:0', 'cut': 'cut:k:end', 'track': 'parent/track:t1'},
                   'authorship': {'x': 'direct', 'y': 'consequence'}, 'version': None}, True))
    for field in ['args', 'expect', 'bindings', 'created', 'authorship', 'resolved']:
        for item in [None, True, 1, 'wrong']:
            values.append((f'{field}-{item}', {**BASE, field: item}, False))
    for item in [{}, {'state': 'present'}, {'state': 'absent', 'value': None}, {'state': 'unknown'}, {'state': 'present', 'value': 1, 'actor': 'root'}, {'$absent': True}]:
        values.append(('bad-tag-' + json.dumps(item), {**BASE, 'expect': {'x': item}}, False))
    for field in ['created', 'resolved']:
        for item in ['c1.rocket', 'parent/clip:', 'shot:/clip:c1', 'cut:k:start', 'parent/cut:k', 'project:p/clip:c1', 1, None]:
            values.append((f'{field}-bad-id-{item}', {**BASE, field: [item]}, False))
    for item in ['word:s1:no', 'beat:-1', 'cut:k:middle', 'c1.rocket', 'project:p/clip:c1', {}, None]:
        values.append((f'bad-binding-{item}', {**BASE, 'bindings': {'authored': item}}, False))
    for field in ['publisher', 'actor', 'asserted_actor', 'extra', '__proto__', 'constructor', 'toString']:
        values.append(('spoof-' + field, {**BASE, field: 'agent:root'}, False))
    values.append(('bad-authorship', {**BASE, 'authorship': {'x': 'actor:root'}}, False))
    for field in ['op', 'select', 'args']:
        value = copy.deepcopy(BASE); del value[field]
        values.append(('missing-' + field, value, False))
    values.extend([('opaque-map-keys', {**BASE, 'args': {'__proto__': {'opaque': None}}, 'expect': {'constructor': {'state': 'present', 'value': {'op': 'clear'}}}}, True),
                   ('no-defaults', BASE, True)])
    return values


CASES = cases()


@pytest.mark.parametrize('name,value,valid', CASES, ids=[c[0] for c in CASES])
def test_python_validators_match_exact_schema(name, value, valid):
    assert Draft202012Validator(generate.opcall_schema()).is_valid(value) is valid
    spec = importlib.util.spec_from_file_location('opcall_package', ROOT / 'packages/python/banodoco_workspace_client/generated.py')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    original = copy.deepcopy(value)
    for validate in [validate_edit_command, module.validate_edit_command]:
        if valid:
            assert validate(value) is value
            raw = (' \n' + json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()
            assert validate_edit_command_bytes(raw) is raw
        else:
            with pytest.raises(ValueError, match='OpCall'):
                validate(value)
    assert value == original


def test_typescript_matches_schema_and_rejects_non_json_values():
    node = shutil.which('node')
    if node is None or int(subprocess.check_output([node, '--version'], text=True).split('.')[0][1:]) < 22:
        pytest.skip('Node 22+ required to execute the generated TypeScript directly')
    script = r'''
import {readFileSync} from 'node:fs';
import {pathToFileURL} from 'node:url';
const {validateEditCommand: validate} = await import(pathToFileURL(process.argv[1]));
const cases = JSON.parse(readFileSync(0, 'utf8'));
const accepts = value => { try { return validate(value) === value; } catch { return false; } };
for (const [name, value, expected] of cases) {
  const before = JSON.stringify(value);
  if (accepts(value) !== expected || JSON.stringify(value) !== before) throw Error(name);
}
const base = {op: 'timeline.set', select: null, args: {}};
const cycle = {}; cycle.self = cycle;
const sparse = []; sparse.length = 1;
const getter = Object.defineProperty({}, 'x', {enumerable: true, get() { throw Error('getter ran'); }});
for (const args of [{n: NaN}, {n: Infinity}, {n: undefined}, {n: 1n}, {n: new Date()}, {n: cycle}, {n: sparse}, getter, {[Symbol('x')]: 1}]) {
  if (accepts({...base, args})) throw Error('accepted non-JSON');
}
if (accepts(Object.assign(Object.create(base), {}))) throw Error('inherited envelope');
console.log(`${cases.length} schema cases and 10 non-JSON/spoof checks passed`);
'''
    result = subprocess.run([node, '--experimental-transform-types', '--input-type=module', '-e', script, str(ROOT / 'packages/typescript/src/generated.ts')], input=json.dumps(CASES), capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize('mutation', ['root-keyword', 'nested-keyword', 'items-keyword', 'unknown-ref', 'external-ref', 'cycle', 'regex', 'type', 'ref-sibling'])
def test_generator_refuses_unsupported_constraints_before_output(tmp_path, monkeypatch, mutation):
    schema = generate.opcall_schema()
    if mutation == 'root-keyword': schema['unevaluatedProperties'] = False
    if mutation == 'nested-keyword': schema['properties']['expect']['additionalProperties']['oneOf'][0]['minProperties'] = 1
    if mutation == 'items-keyword': schema['properties']['created']['items']['maxLength'] = 1
    if mutation == 'unknown-ref': schema['properties']['created']['items'] = {'$ref': '#/$defs/missing'}
    if mutation == 'external-ref': schema['properties']['created']['items'] = {'$ref': 'https://example.test/id'}
    if mutation == 'cycle': schema['$defs']['scopedId'] = {'$ref': '#/$defs/scopedId'}
    if mutation == 'regex': schema['properties']['op']['pattern'] = r'\A.*\Z'
    if mutation == 'type': schema['properties']['created']['items'] = {'type': 'integer'}
    if mutation == 'ref-sibling': schema['properties']['created']['items']['enum'] = ['anything']
    source = tmp_path / 'schema.json'; source.write_text(json.dumps(schema))
    monkeypatch.setattr(generate, 'OPCALL_SCHEMA', source)
    with pytest.raises(SystemExit, match='unsupported schema'):
        generate.render()


def test_json_bytes_and_recursion_fail_closed():
    for raw in [b'{"op":"timeline.set","select":null,"args":{},"expect":{"x":{"state":"present","state":"absent"}}}',
                b'{"op":"timeline.set","select":null,"args":{"n":NaN}}']:
        with pytest.raises(ValueError): validate_edit_command_bytes(raw)
    cycle = {}; cycle['self'] = cycle
    with pytest.raises(ValueError): validate_edit_command({**BASE, 'args': cycle})
