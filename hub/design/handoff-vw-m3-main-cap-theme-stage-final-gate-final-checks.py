"""Bind the review to the completed handoff and preserve the failed attempt."""
import ast
import hashlib
import json
from pathlib import Path
import sys

ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
PREFIX = ORCH / 'design/handoff-vw-m3-main-cap-theme-stage-final-gate-'
TARGET = ORCH / 'design/handoff-vw-m3-main-cap-locked-theme-stage-'
OLD = ORCH / 'design/handoff-vw-m3-main-cap-controller-repair-'


def path(prefix, name):
    return Path(str(prefix) + name)


def sha(file):
    return hashlib.sha256(file.read_bytes()).hexdigest()


assert (ORCH / 'workers/vw-m3-main-cap-locked-theme-stage/DONE').is_file()
report = path(TARGET, 'REPORT.md').read_text()
names = ('controller.py', 'render.mjs', 'resolve.mjs', 'theme-source.git.tar',
         'theme-proof.json', 'COMMAND.txt', 'REPORT.md')
hashes = {name: sha(path(TARGET, name)) for name in names}
for name in ('controller.py', 'render.mjs', 'resolve.mjs'):
    assert hashes[name] in report, name
if sys.argv[1] == 'freeze':
    path(PREFIX, 'reviewed-sha256.json').write_text(json.dumps(hashes, indent=2) + '\n')
    # Private copies redirect only the review's pure preflight artifacts/stage.
    for name in ('resolve.mjs', 'theme-source.git.tar', 'theme-proof.json'):
        path(PREFIX, name).write_bytes(path(TARGET, name).read_bytes())
    print(json.dumps(hashes, indent=2))
    raise SystemExit(0)

assert hashes == json.loads(path(PREFIX, 'reviewed-sha256.json').read_text())
preserved = json.loads(path(PREFIX, 'preserved-before.json').read_text())
preserved.update(json.loads(path(TARGET, 'preserved-before.json').read_text()))
assert all(sha(Path(name)) == digest for name, digest in preserved.items())
old_functions = {node.name: ast.dump(node, include_attributes=False)
                 for node in ast.parse(path(OLD, 'controller.py').read_text()).body
                 if isinstance(node, ast.FunctionDef)}
new_functions = {node.name: ast.dump(node, include_attributes=False)
                 for node in ast.parse(path(TARGET, 'controller.py').read_text()).body
                 if isinstance(node, ast.FunctionDef)}
unchanged = ('source_check', 'graph_check', 'run_process', 'measure', 'script_grant',
             'central_grant', 'disk', 'inventory', 'real_parents')
assert all(old_functions[name] == new_functions[name] for name in unchanged)
renderer = path(TARGET, 'render.mjs').read_text()
renderer = renderer.replace('vw-m3-main-cap-locked-theme-stage', 'vw-m3-main-cap-controller-repair')
renderer = renderer.replace('e2e-viewing-main6-locked-theme-image-cap-three-stills', 'e2e-viewing-main6-image-cap-three-stills')
renderer = renderer.replace('`${prefix}CAPTURE-GRANT.txt`', '`${own}/CAPTURE-GRANT.txt`')
renderer = renderer.replace('`${prefix}capture-stage`', '`${own}/capture-stage`')
start = renderer.index('// The original MAIN6 registry must keep resolving the historical real theme.')
end = renderer.index('const requirePeer =', start)
renderer = renderer[:start] + renderer[end:]
assert renderer == path(OLD, 'render.mjs').read_text()
source = json.loads(path(PREFIX, 'independent-source-proof.json').read_text())
theme = json.loads(path(TARGET, 'theme-proof.json').read_text())
assert theme['member_sha256'] == source['theme_all_members']
assert theme['main_lock_entry'] == source['theme_lock_entry']
assert theme['github_archive_integrity_verified'] is False
independent = json.loads(path(PREFIX, 'static-resolution.json').read_text())
target = json.loads(path(TARGET, 'dependencies.json').read_text())
assert target['status'] == 'PASS' and not target['failures'] and not target['nonliteral']
a = {(edge['from'], edge['specifier'], edge['resolved'].removeprefix('/__readonly_main__/'))
     for edge in independent['edges']}
b = {(edge['importer'], edge['request'], edge['target']) for edge in target['edges']}
assert a == b and len(a) == 362
assert len(target['source_files']) == independent['parsed_files'] == 101
assert len(target['generated_registry_bare_imports']) == 50
assert len(target['declared_main_packages']) == 19
for name in ('CAPTURE-GRANT.txt', 'CAPTURE-STARTED', 'capture.lock', 'capture-stage', 'resolver-stage'):
    assert not path(TARGET, name).exists() and not path(TARGET, name).is_symlink()
assert not list(ORCH.glob('design/handoff-vw-m3-main-cap-locked-theme-stage-frame-*.png'))
result = {'frozen_sha256': hashes, 'preserved_files': len(preserved),
          'unchanged_controller_functions': unchanged,
          'renderer_unchanged_except_identity_flat_paths_and_theme_checks': True,
          'source_dependency_edges_independently_equal': len(a),
          'source_files': 101, 'original_registry_bare_imports': 50, 'main_packages': 19,
          'capture_grant_marker_stage_and_pngs_absent': True}
path(PREFIX, 'final-checks.json').write_text(json.dumps(result, indent=2) + '\n')
print('PASS: exact frozen bytes; original guard functions and renderer body retained; independent362-edge proof equals target; preserved', len(preserved), 'prior files; no capture artifacts')
