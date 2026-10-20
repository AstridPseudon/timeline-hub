"""Independent local object/fixture proof. Does not extract or execute sources."""
import base64
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile

ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
PREFIX = ORCH / 'design/handoff-vw-m3-main-cap-theme-stage-final-gate-'
FIXTURE = ORCH / 'design/handoff-vw-m3-main-image-cap-source-vector-'
MAIN = 'a411628f8fd6129f9c58c332019b56769d997384'
THEME = '1db8440aabf0769b01453831a06f3c609bbc90c9'
OLD_THEME = '4974bdb471cf4dda0ce39d2cc24a1d62420a1305'


def git(repo, *args):
    return subprocess.check_output(['git', '-C', repo, *args])


def sha(data):
    return hashlib.sha256(data).hexdigest()


def members(data):
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        regular = [item for item in archive if not item.isdir()]
        assert all(item.isfile() for item in regular)
        result = {item.name: archive.extractfile(item).read() for item in regular}
        assert len(result) == len(regular)
        return result


source_paths = ('astrid', 'scripts/gen_effect_registry.py', 'remotion/src',
                'remotion/public', 'remotion/webpack-alias.mjs', 'remotion/package.json',
                'remotion/package-lock.json', 'pyproject.toml', 'tests')
original = members(git('/home/user/work/agent', 'archive', MAIN, *source_paths))
assert len(original) == 2414
staged = members(Path(str(FIXTURE) + 'main-source.tar.gz').read_bytes())
assert all(staged[name] == value for name, value in original.items())
lock = json.loads(original['remotion/package-lock.json'])
manifest = json.loads(original['remotion/package.json'])
theme_lock = lock['packages']['node_modules/@banodoco/timeline-theme-2rp']
assert theme_lock['version'] == '0.1.1'
assert manifest['dependencies']['@banodoco/timeline-theme-2rp'] == theme_lock['resolved']
theme_members = members(git('/home/user/work/composition', 'archive', THEME))
old_theme_members = members(git('/home/user/work/composition', 'archive', OLD_THEME))
assert len(theme_members) == len(old_theme_members) == 20
assert set(theme_members) == set(old_theme_members)
changed = [name for name in theme_members if theme_members[name] != old_theme_members[name]]
assert changed == ['package.json']
theme_package = json.loads(theme_members['package.json'])
assert theme_package['name'] == '@banodoco/timeline-theme-2rp'
assert theme_package['version'] == theme_lock['version']
assert theme_package['peerDependencies'] == theme_lock['peerDependencies']
locked_archive = Path(str(FIXTURE) + 'locked-composition6.tar.gz').read_bytes()
locked = members(locked_archive)
assert len(locked) == 29
integrity = 'sha512-' + base64.b64encode(hashlib.sha512(locked_archive).digest()).decode()
assert lock['packages']['node_modules/@banodoco/timeline-composition']['integrity'] == integrity
assert lock['packages']['node_modules/@banodoco/timeline-composition']['version'] == '0.0.6'
failed = ORCH / 'design/handoff-vw-m3-main-cap-controller-repair-'
postflight = json.loads(Path(str(failed) + 'postflight.json').read_text())
replay = json.loads(Path(str(failed) + 'seven-output-replay.json').read_text())
assert postflight['valid'] is False
assert postflight['source_byte_equal'] and postflight['graph_unchanged']
assert postflight['post_errors'] == []
assert replay['byte_equal'] and len(replay['outputs']) == 7
assert all(sha(Path(str(FIXTURE) + name).read_bytes()) == digest for name, digest in replay['outputs'].items())
assert not list(ORCH.glob('design/handoff-vw-m3-main-cap-controller-repair-frame-*.png'))
assert "Can't resolve '@banodoco/timeline-theme-2rp/" in Path(str(failed) + 'capture.log').read_text()
result = {
    'main': MAIN,
    'original_main_files': len(original),
    'original_main_hashes': {name: sha(value) for name, value in original.items()},
    'theme_commit': THEME,
    'theme_tree': git('/home/user/work/composition', 'rev-parse', THEME + '^{tree}').decode().strip(),
    'old_theme_commit': OLD_THEME,
    'only_changed_theme_file': changed,
    'theme_version': theme_package['version'],
    'theme_lock_entry': theme_lock,
    'theme_all_members': {name: sha(value) for name, value in theme_members.items()},
    'theme_archive_integrity': 'NOT re-verified: archive URL 403; accepted git-tag source proof only',
    'composition6_archive_integrity': integrity,
    'composition6_members': {name: sha(value) for name, value in locked.items()},
    'prior_failed_attempt': {'source_byte_equal': True, 'graph_unchanged': True,
                             'seven_byte_equal_outputs': replay['outputs'], 'no_pngs': True},
}
Path(str(PREFIX) + 'independent-source-proof.json').write_text(json.dumps(result, indent=2) + '\n')
print('PASS: 2414 original MAIN files; lock-exact 29-member Composition6; 20 git-tag theme0.1.1 files; only manifest differs from0.1.0')
print('PASS: failed attempt preserved seven equal outputs and source/full-graph postflight; no PNGs')
print('Theme archive integrity NOT re-verified (prior403); accepted tag-tree proof retained')
