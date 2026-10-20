"""Freeze original MAIN code and a synthetic image/occurrence closure offline."""
import base64
import hashlib
import io
import json
import os
from pathlib import Path
import struct
import subprocess
import tarfile
import zlib

OWN = Path(__file__).resolve().parent
ORCH = OWN.parents[1]
MAIN = 'a411628f8fd6129f9c58c332019b56769d997384'
OLD = '67b8aa3d0d6831d3e3504a340ff583c3da253707'
REPO = Path('/home/user/work/wt/vw-m3-main-image-cap-source-vector')
COMPOSITION = Path('/home/user/peteromallet/timeline-composition')
PYTHON = '/home/user/work/venv-agent/bin/python'
PREFIX = ORCH / 'design/handoff-vw-m3-main-image-cap-source-vector-'


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2) + '\n')


def unpack(data, destination, strip=False):
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        for member in archive.getmembers():
            if member.isdir():
                continue
            assert member.isfile(), member.name
            parts = Path(member.name).parts[1:] if strip else Path(member.name).parts
            relative = Path(*parts)
            assert parts and not relative.is_absolute() and '..' not in parts
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            assert not any(p.is_symlink() for p in [target, *target.parents])
            target.write_bytes(archive.extractfile(member).read())


def main():
    assert not (ORCH / 'managers/viewing/QUIET.md').exists(), 'viewing QUIET'
    assert git(REPO, 'rev-parse', 'origin/main').decode().strip() == MAIN
    source = OWN / 'main-source'
    source.mkdir(exist_ok=False)
    unpack(git(REPO, 'archive', MAIN, 'astrid', 'scripts/gen_effect_registry.py',
               'remotion/src', 'remotion/public', 'remotion/webpack-alias.mjs',
               'remotion/package.json', 'remotion/package-lock.json', 'pyproject.toml',
               'tests'), source)
    assert git(COMPOSITION, 'rev-parse', 'v0.0.6').decode().strip() == OLD
    archive = subprocess.check_output(['gzip', '-n'], input=git(
        COMPOSITION, 'archive', '--format=tar', '--prefix=timeline-composition-0.0.6/', OLD))
    lock = json.loads((source / 'remotion/package-lock.json').read_text())['packages'][
        'node_modules/@banodoco/timeline-composition']
    assert 'sha512-' + base64.b64encode(hashlib.sha512(archive).digest()).decode() == lock['integrity']
    Path(str(PREFIX) + 'locked-composition6.tar.gz').write_bytes(archive)
    package = source / 'remotion/node_modules/@banodoco/timeline-composition'
    unpack(archive, package, strip=True)
    before = {str(p.relative_to(package)): sha(p.read_bytes()) for p in package.rglob('*') if p.is_file()}
    env = dict(os.environ, PYTHONPATH=str(source), PYTHONDONTWRITEBYTECODE='1',
               ASTRID_PACKS_PATH='', ASTRID_TIMELINE_COMPOSITION_SRC=str(package / 'typescript/src'))
    result = subprocess.run([PYTHON, str(source / 'scripts/gen_effect_registry.py')],
                            cwd=source, env=env, text=True, capture_output=True)
    (OWN / 'generator.log').write_text(result.stdout + result.stderr)
    assert result.returncode == 0, result.stdout + result.stderr
    after = {str(p.relative_to(package)): sha(p.read_bytes()) for p in package.rglob('*') if p.is_file()}
    generated = {f'typescript/src/{kind}.generated.ts' for kind in ('effects', 'animations', 'transitions')}
    assert all(after[name] == digest for name, digest in before.items() if name not in generated)
    identity = {'main': MAIN, 'composition_source': OLD, 'lock_entry': lock,
                'artifact_lock_verified': True, 'archive_sha256': sha(archive),
                'archive_regular_members': len(before), 'package_before': before,
                'package_after_generation': after, 'generated_sha256': {name: after[name] for name in generated},
                'source_sha256': {str(p.relative_to(source)): sha(p.read_bytes())
                                  for part in ('astrid', 'scripts', 'remotion/src')
                                  for p in (source / part).rglob('*') if p.is_file()},
                'main_manifest_sha256': sha((source / 'remotion/package.json').read_bytes()),
                'main_lock_sha256': sha((source / 'remotion/package-lock.json').read_bytes())}
    write_json(str(PREFIX) + 'source-identity.json', identity)
    # Plain, opaque test pixels, not a captured/rendered frame or owner media.
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data))
    png = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', 16, 16, 8, 2, 0, 0, 0))
    png += chunk(b'IDAT', zlib.compress((b'\x00' + bytes([240, 240, 240]) * 16) * 16)) + chunk(b'IEND', b'')
    Path(str(PREFIX) + 'image.png').write_bytes(png)
    digest = sha(png)
    track = {'id': 'picture', 'kind': 'visual', 'label': 'Picture', 'fit': 'cover'}
    config = {'tracks': [track], 'clips': [], 'output': {'fps': 30, 'resolution': '1920x1080', 'file': 'output.mp4'},
              'theme_overrides': {'visual': {'canvas': {'width': 1920, 'height': 1080, 'fps': 30}}}}
    closure = {
        'parent_revision': {'project_id': 'project-demo', 'timeline_id': 'timeline-1', 'revision_id': 'image-cap-parent',
            'payload': {'config': config, 'registry': {'assets': {}}, 'occurrences': [{
                'occurrence_id': 'image-occurrence', 'shot_id': 'image-shot', 'shot_revision_id': 'image-shot-revision',
                'placement': {'start_ms': 0, 'track': 'picture'}, 'duration_ms': 4000,
                'source_offset': 0, 'speed': 1, 'gain': 1, 'mute': False}]}},
        'shot_revisions': [{'project_id': 'project-demo', 'shot_id': 'image-shot', 'revision_id': 'image-shot-revision',
                            'internal_timeline_revision_id': 'image-internal', 'payload': {'name': 'Image cap analog', 'text_bindings': []}}],
        'internal_timeline_revisions': [{'project_id': 'project-demo', 'timeline_id': 'timeline-1', 'revision_id': 'image-internal',
            'payload': {'tracks': [track], 'clips': [{'id': 'image', 'clipType': 'image', 'asset': 'image', 'track': 'picture',
                'at': 0, 'hold': 5, 'effects': {'fade_out': 1}}], 'registry': {'assets': {'image': {
                    'media_id': 'sha256:' + digest, 'content_sha256': digest, 'type': 'image', 'resolution': '16x16'}}}}}]}
    for record in [closure['parent_revision'], *closure['shot_revisions'], *closure['internal_timeline_revisions']]:
        record['content_digest'] = 'sha256:' + sha(json.dumps(record['payload'], sort_keys=True, separators=(',', ':')).encode())
    write_json(str(PREFIX) + 'raw-closure.json', closure)
    write_json(str(PREFIX) + 'fixture-label.json', {
        'kind': 'synthetic executable analog; not native App output or owner film',
        'request': 'prepared shot image hold5 / fade_out1 / occurrence duration4000ms / frame105 at numeric30fps',
        'image_sha256': digest, 'image_size': [16, 16], 'rgb': [240, 240, 240],
        'pins': 'offline synthetic immutable revision IDs; digests computed from exact payloads',
        'source': 'original MAIN _Runtime test transport plus original MAIN normal managed resolver and render-prep helpers',
        'capture': 'NOT RUN; native managed URL resolver must be bound by capture worker, or explicitly label static-public analog'})
    result = subprocess.run([PYTHON, str(OWN / 'replay.py'), str(PREFIX)], cwd=source, env=env,
                            text=True, capture_output=True)
    (OWN / 'replay.log').write_text(result.stdout + result.stderr)
    assert result.returncode == 0, result.stdout + result.stderr
    print('Frozen MAIN source, locked Composition6, generated maps and closure replay: PASS')


if __name__ == '__main__':
    main()
