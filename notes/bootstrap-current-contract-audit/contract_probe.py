"""Pure source/SDK gap probes; no Runtime import, realm, SQL or publication."""
import ast
import json
import os
from pathlib import Path

from astrid.sdk.timeline._command_state import CommandError
from astrid.sdk.timeline.commands import operations, validate_command

root = Path(os.environ['AUDIT_SNAPSHOTS'])
fixture = json.loads((root / 'app-stage/src/tools/video-editor/commands/fixtures/recipe_m2_app_bootstrap.json').read_text())
assert 'timeline.init' not in operations()
try:
    validate_command(fixture['commands'][0])
except CommandError as error:
    assert error.kind == 'unsupported_operation'
    print('PASS current Agent native registry refuses timeline.init:', error.kind)
else:
    raise AssertionError('current provider must not be claimed init-ready')

source = root / 'runtime-s2/runtime_protocol/timeline_commit_store.py'
tree = ast.parse(source.read_text())
method = next(node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == 'adopt_empty_shell')
guard = next(node.test for node in ast.walk(method) if isinstance(node, ast.If) and ast.unparse(node.test).startswith('current is None'))
code = compile(ast.Expression(guard), str(source), 'eval')
cases = [
    ('no head row', None, True),
    ('null revision', {'revision_id': None, 'publication_id': None}, True),
    ('existing unpublished revision', {'revision_id': 'h0', 'publication_id': None}, False),
    ('accepted head', {'revision_id': 'h0', 'publication_id': 'p0'}, True),
]
for name, current, refused in cases:
    assert eval(code, {'__builtins__': {}}, {'current': current}) is refused
    print('SOURCE PREDICATE ONLY:', name, 'refused' if refused else 'passes this predicate; later checks still required')
print('No same-ID public create/adoption or actual Runtime transaction was executed')
