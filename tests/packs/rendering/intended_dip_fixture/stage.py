"""Disposable actual MAIN and unified hosts; shared dependencies stay read-only."""
import base64
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile

MAIN = 'a411628f8fd6129f9c58c332019b56769d997384'
OLD = '67b8aa3d0d6831d3e3504a340ff583c3da253707'
LOCK_INTEGRITY = 'sha512-QV17ysuqgzAiewEGsF84yo3DKFffLNoius5WP3yI/AKcHP2zdySrYjE5YXv6UtXgouJqxCO18/qnMNPOMgtsZg=='
PUBLIC_SHA256 = 'cd83b77f72ce436e25eef697b289d33adae2087d92035aa37a27a308975ddea7'
FILM_SHA256 = '1c85d02743545c04b905fc09e7cd1b6720ca466560a85e38a604f8a17bd457d9'
FIXTURE = Path(__file__).parent


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])


def unpack(data, destination, strip=False):
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        for member in archive.getmembers():
            if member.isdir():
                continue
            assert member.isfile(), f'non-file archive entry: {member.name}'
            relative = Path(member.name)
            if strip:
                relative = Path(*relative.parts[1:])
            assert relative.parts and not relative.is_absolute() and '..' not in relative.parts
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.extractfile(member).read())


def locked_archive(composition_repo):
    assert git(composition_repo, 'rev-parse', 'v0.0.6').decode().strip() == OLD
    tar = git(composition_repo, 'archive', '--format=tar',
              '--prefix=timeline-composition-0.0.6/', 'v0.0.6')
    data = subprocess.check_output(['gzip', '-n'], input=tar)
    assert 'sha512-' + base64.b64encode(hashlib.sha512(data).digest()).decode() == LOCK_INTEGRITY
    return data


def hashes(root):
    return {str(p.relative_to(root)): digest(p) for p in sorted(root.rglob('*')) if p.is_file()}


def stage(repo, destination, *, old_archive, public_archive, peers):
    repo, destination, peers = Path(repo), Path(destination), Path(peers)
    old = old_archive is not None
    revision = MAIN if old else 'HEAD'
    paths = ['astrid', 'scripts/gen_effect_registry.py', 'remotion/src', 'remotion/public',
             'remotion/webpack-alias.mjs', 'remotion/package.json',
             'remotion/package-lock.json', 'pyproject.toml']
    unpack(git(repo, 'archive', revision, *paths), destination)
    project = destination / 'remotion'
    modules = project / 'node_modules'
    package = modules / '@banodoco/timeline-composition'
    package.mkdir(parents=True)
    if old:
        entry = json.loads((project / 'package-lock.json').read_text())['packages'][
            'node_modules/@banodoco/timeline-composition']
        assert entry['version'] == '0.0.6' and entry['integrity'] == LOCK_INTEGRITY
        assert 'sha512-' + base64.b64encode(hashlib.sha512(old_archive).digest()).decode() == entry['integrity']
        data = old_archive
    else:
        assert digest(public_archive) == PUBLIC_SHA256
        data = Path(public_archive).read_bytes()
    unpack(data, package, strip=True)
    version = json.loads((package / 'package.json').read_text())['version']
    assert version == ('0.0.6' if old else '0.0.10')
    before = hashes(package)
    if not old:
        assert len(before) == 77
    for peer in peers.iterdir():
        if peer.name != '@banodoco':
            (modules / peer.name).symlink_to(peer, target_is_directory=peer.is_dir())
    # Old index re-exports these packages; retain/bind their real source, even
    # though this 2D AM film selects neither theme effects nor schema code.
    for name in ('timeline-theme-2rp', 'timeline-schema'):
        (modules / '@banodoco' / name).symlink_to(
            Path('/home/user/work/app/vendor') / name, target_is_directory=True)
    for name, expected in (('react', '18.3.1'), ('react-dom', '18.3.1'),
                           ('remotion', '4.0.509'), ('@remotion/bundler', '4.0.509'),
                           ('@remotion/renderer', '4.0.509'), ('@remotion/media', '4.0.509')):
        assert json.loads((modules / name / 'package.json').read_text())['version'] == expected
    source_before = {str(p.relative_to(destination)): digest(p)
                     for part in ('astrid', 'remotion/src', 'scripts')
                     for p in (destination / part).rglob('*') if p.is_file()}
    env = {k: v for k, v in os.environ.items() if k not in
           ('NODE_OPTIONS', 'NODE_PATH', 'PYTHONPYCACHEPREFIX', 'ASTRID_REMOTION_PROJECT_DIR')}
    env.update(PYTHONPATH=str(destination), PYTHONDONTWRITEBYTECODE='1', ASTRID_PACKS_PATH='')
    if old:
        env['ASTRID_TIMELINE_COMPOSITION_SRC'] = str(package / 'typescript/src')
    else:
        env['ASTRID_REMOTION_PROJECT_DIR'] = str(project)
    result = subprocess.run([sys.executable, str(destination / 'scripts/gen_effect_registry.py')],
                            cwd=destination, env=env, text=True, capture_output=True, timeout=60)
    assert result.returncode == 0, result.stdout + result.stderr
    generated = {f'{kind}.generated.ts' for kind in ('effects', 'animations', 'transitions')}
    for relative, sha in source_before.items():
        if old or not (relative.startswith('remotion/src/') and Path(relative).name in generated):
            assert digest(destination / relative) == sha, relative
    after = hashes(package)
    if old:
        for relative in before:
            if relative not in {f'typescript/src/{name}' for name in generated}:
                assert after[relative] == before[relative], relative
    else:
        assert after == before
    return project, {'agent': git(repo, 'rev-parse', revision).decode().strip(),
                     'composition_version': version, 'archive_sha256': hashlib.sha256(data).hexdigest(),
                     'package_before': before, 'package_after_generation': after,
                     'source_sha256': source_before,
                     'generated_sha256': {name: digest((package / 'typescript/src' if old else project / 'src') / name)
                                          for name in sorted(generated)},
                     'main_lock_verified': old}
