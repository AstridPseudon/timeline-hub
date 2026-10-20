"""Offline whole-registry positive/negative calibrations in an owned temporary stage."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

sys.dont_write_bytecode = True
PREFIX = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-main-cap-locked-theme-stage-')
spec = importlib.util.spec_from_file_location('controller', Path(str(PREFIX) + 'controller.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
source = m.source_check()
theme = m.theme_check()
before, manifest_before = m.graph_check()
original_check = m.dependency_check
checks = []


def resolve(root):
    env = dict(os.environ, ASTRID_PACKS_PATH='')
    env.pop('NODE_OPTIONS', None)
    env.pop('NODE_PATH', None)
    process = subprocess.run([str(m.NODE), str(PREFIX) + 'resolve.mjs', str(root)],
                             env=env, text=True, capture_output=True)
    assert process.stdout, process.stderr
    return process.returncode, json.loads(process.stdout)


def calibrate(root, name):
    modules = root / 'remotion/node_modules'
    scope = modules / '@banodoco'
    composition = scope / 'timeline-composition'
    package = scope / 'timeline-theme-2rp'
    for directory in (modules, scope, composition, package):
        assert directory.is_dir() and not directory.is_symlink(), directory
    assert m.inventory(composition) == source['generated_package_members']
    assert m.inventory(package) == theme['member_sha256']
    checks.append({'test': 'real private scopes, exact MAIN6 and historical theme members', 'pass': True})
    result = original_check(root, 'resolution-positive.json')
    assert result['status'] == 'PASS' and len(result['generated_registry_bare_imports']) == 50
    assert len(result['source_files']) == 101 and len(result['edges']) == 362
    checks.append({'test': 'all four original registries and owned transitive imports resolve', 'pass': True})
    withheld = root / 'withheld-theme'
    package.rename(withheld)
    try:
        code, failed = resolve(root)
        assert code == 1
        assert len(failed['failures']) == 5, failed['failures']
        requests = [row['request'] for row in failed['failures'] if 'request' in row]
        assert len(requests) == 4 and all(r.startswith('@banodoco/timeline-theme-2rp/src/effects/') for r in requests)
        assert any(r.get('declared_package') == '@banodoco/timeline-theme-2rp' for r in failed['failures'])
        m.evidence('resolution-missing-theme.json', failed)
        checks.append({'test': 'missing whole theme catches all four registry imports plus declaration together', 'pass': True})
    finally:
        withheld.rename(package)
    leaf = package / 'src/effects/art-card/component.tsx'
    saved = leaf.read_bytes()
    leaf.rename(leaf.with_suffix('.withheld'))
    try:
        code, failed = resolve(root)
        assert code == 1 and len(failed['failures']) == 1, failed['failures']
        assert failed['failures'][0]['request'].endswith('art-card/component')
        checks.append({'test': 'missing single original component refuses', 'pass': True})
    finally:
        leaf.with_suffix('.withheld').rename(leaf)
    assert leaf.read_bytes() == saved
    manifest = package / 'package.json'
    original = manifest.read_bytes()
    try:
        changed = json.loads(original)
        changed['version'] = '0.1.0'
        manifest.write_text(json.dumps(changed))
        code, failed = resolve(root)
        assert code == 1 and len(failed['failures']) == 1, failed['failures']
        assert failed['failures'][0]['declared_package'] == '@banodoco/timeline-theme-2rp'
        checks.append({'test': 'implementation-equal version 0.1.0 is still rejected against MAIN 0.1.1', 'pass': True})
    finally:
        manifest.write_bytes(original)
    with patch.object(m, 'RESOLVER_SHA', 'not-approved'), patch.object(m.subprocess, 'run', side_effect=AssertionError('spawn forbidden')):
        try:
            original_check(root, 'UNCREATED.json')
        except RuntimeError as exc:
            assert 'offline resolver changed' in str(exc)
        else:
            raise AssertionError('changed resolver accepted')
    checks.append({'test': 'changed static checker refuses before subprocess', 'pass': True})
    m.verify_stage(root.parent, source, replayed=False)
    return result


with patch.object(m, 'dependency_check', side_effect=calibrate):
    m.offline_dependencies(source, theme)
after, manifest_after = m.graph_check()
assert before == after and manifest_before == manifest_after
assert not Path(str(PREFIX) + 'resolver-stage').exists()
checks.append({'test': 'temporary stage cleaned and complete shared graph unchanged', 'pass': True})
m.evidence('resolution-calibrations.json', {'checks': checks, 'passed': len(checks), 'graph_before': before, 'graph_after': after})
print(json.dumps({'passed': len(checks), 'checks': checks}, indent=2))
