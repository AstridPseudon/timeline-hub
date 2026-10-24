"""F-D85 source inspection only; never imports or executes product/test bodies."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path('/home/user/work/wt/agt-F-native-cli-sol-2350')
EVIDENCE = Path(__file__).resolve().parent
MANIFEST = json.loads((EVIDENCE / 'source-manifest.json').read_text())
BASE = MANIFEST['baseline']


def functions(source):
    return {node.name: ast.dump(node, include_attributes=False)
            for node in ast.parse(source).body
            if isinstance(node, ast.FunctionDef) and node.name.startswith('test_')}


for name, expected in MANIFEST['files'].items():
    baseline = subprocess.check_output(['git', 'show', f'{BASE}:{name}'], cwd=ROOT)
    candidate = (ROOT / name).read_bytes()
    assert hashlib.sha256(baseline).hexdigest() == expected['baseline_sha256']
    assert hashlib.sha256(candidate).hexdigest() == expected['candidate_sha256']
    assert baseline == candidate
    compile(baseline, name, 'exec')
    compile(candidate, name, 'exec')
    if name.startswith('tests/'):
        assert functions(baseline) == functions(candidate)

selectors = (EVIDENCE / 'later-main-selectors.txt').read_text().splitlines()
assert len(selectors) == 24
assert selectors == MANIFEST['conservation']['assigned_selectors']


def find(path, name):
    tree = ast.parse((ROOT / path).read_text())
    return next(node for node in ast.walk(tree)
                if isinstance(node, ast.FunctionDef) and node.name == name)


def calls(node, name):
    return [call for call in ast.walk(node)
            if isinstance(call, ast.Call) and ast.unparse(call.func) == name]


cli = 'astrid/packs/timeline/cli.py'
native = 'astrid/packs/timeline/cli_native.py'
session = 'astrid/sdk/timeline/commit_session.py'
sync = 'astrid/sdk/timeline/sync.py'
assert calls(find(cli, '_cmd_commit'), 'commit_document')
assert calls(find(native, 'commit_document'), '_detached_document')
assert calls(find(native, 'commit_document'), '_preview_detached_document')
assert calls(find(native, '_preview_detached_document'), 'working.commit')
assert calls(find(session, '_capture_free_edits'), 'emit_document_commands')
submit = calls(find(session, 'commit'), 'self.session.submit')
assert len(submit) == 1
assert 'via' not in {keyword.arg for keyword in submit[0].keywords}
assert calls(find(sync, 'submit'), 'self._flush')
assert calls(find(sync, '_flush'), 'self.client.timelines.commit')
print('SOURCE ONLY: five files unchanged and compile; full test AST conserved; 24 selectors retained.')
print('SOURCE ONLY: detached CLI -> emitter -> submit -> Runtime commit; CLI provenance omitted.')
print('No functional result; inherited original parser-test rewrite is recorded in source-manifest.json.')
