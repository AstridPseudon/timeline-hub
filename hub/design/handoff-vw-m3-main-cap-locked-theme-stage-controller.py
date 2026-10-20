"""Offline preparation; capture is enabled only by a manager grant in the service.

No product policy is implemented here. MAIN's frozen replay supplies every prop.
"""
import argparse
import base64
import fcntl
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import signal
import statistics
import subprocess
import sys
import tarfile
import time

sys.dont_write_bytecode = True

ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
DESIGN = ORCH / 'design'
WORKER = 'vw-m3-main-cap-locked-theme-stage'
OWN = ORCH / 'workers' / WORKER
PREFIX = DESIGN / ('handoff-' + WORKER + '-')
FIXTURE = DESIGN / 'handoff-vw-m3-main-image-cap-source-vector-'
REPO = Path('/home/user/work/agent')  # Retained read-only object store; never a creator worktree.
GRAPH = Path('/home/user/work/wt/vw-m1-ssr-snapshot/remotion/node_modules')
NODE = Path('/tmp/vw-m3-agent-gate-node20.19.4/bin/node')
PYTHON = Path('/home/user/work/venv-agent/bin/python')
BROWSER = Path('/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell')
MAIN = 'a411628f8fd6129f9c58c332019b56769d997384'
COMPOSITION = '67b8aa3d0d6831d3e3504a340ff583c3da253707'
SOURCE_SHA = '6b89215fd014a062a2590c9739e39efd656effec0aefae45b6afa0db0ac4d96d'
ARCHIVE_SHA = '78746170f9c337650991dacca7a303c71be89ee5e61c25ef821390c7563df87b'
FREEZE_SHA = '40e8c939cccebacef245f16094dda5cadedf7374c66200727479391dadd68d6d'
PRIOR_SHA = '299da50a3d7d08068987d292e5e2d6d38fbae6129947372df1450fb569e758a9'
FLOOR = 10 * 1024**3
HEADROOM = 2 * 1024**3  # Bundle, private webpack/browser caches, temporary files.
PNG_RAW = 3 * 1920 * 1080 * 4
SUITE = 'e2e-viewing-main6-locked-theme-image-cap-three-stills'
GRANT = Path(str(PREFIX) + 'CAPTURE-GRANT.txt')  # Manager writes the suite line and both approved hashes; never created here.
FRAMES = (90, 105, 119)
OUTPUTS = ('main-projected-config.json', 'main-managed-registry.json',
           'main-materialized-timeline.json', 'main-serialized-timeline.json',
           'main-props-template.json', 'main-props-static-analog.json', 'trace.json')
SOURCE_PATHS = ('astrid', 'scripts/gen_effect_registry.py', 'remotion/src',
                'remotion/public', 'remotion/webpack-alias.mjs', 'remotion/package.json',
                'remotion/package-lock.json', 'pyproject.toml', 'tests')
FORBIDDEN = (Path('/home/user/work/app/node_modules'),
             Path('/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules'))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def file_sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def fixture(name):
    return Path(str(FIXTURE) + name)


def evidence(name, value):
    path = Path(str(PREFIX) + name)
    real_parents(path.parent)
    require(not path.is_symlink(), f'evidence leaf is a symlink: {path}')
    path.write_text(json.dumps(value, indent=2) + '\n')


def real_parents(path):
    require(path.is_absolute(), f'not absolute: {path}')
    require(not any(p.is_symlink() for p in (path, *path.parents)), f'symlink parent: {path}')


def quiet():
    return any(p.exists() for p in (ORCH / 'QUIET.md', ORCH / 'managers/viewing/QUIET.md'))


def disk(remaining):
    free = shutil.disk_usage(OWN).free
    require(free >= FLOOR + remaining,
            f'disk BLOCKED: free={free}, required={FLOOR + remaining} '
            f'(10 GiB reserve + {remaining} staging/headroom bytes)')
    require(not quiet(), 'QUIET active; no staging/capture permitted')
    return free


def inventory(root):
    result = {}

    def walk(directory, ancestors):
        real = directory.resolve(strict=True)
        require(real not in ancestors, f'dependency cycle: {directory}')
        require(not any(real == p or p in real.parents for p in FORBIDDEN),
                f'polluted graph traversal: {directory}')
        for path in sorted(directory.iterdir()):
            name = str(path.relative_to(root))
            if path.is_symlink():
                target = path.resolve(strict=True)
                require(not any(target == p or p in target.parents for p in FORBIDDEN),
                        f'polluted dependency symlink: {path}')
                result[name + '@link'] = os.readlink(path)
            if path.is_dir():
                walk(path, ancestors | {real})
            else:
                require(path.is_file(), f'unsupported dependency entry: {path}')
                result[name] = file_sha(path)
    walk(root, set())
    return result


def tar_hashes(archive):
    result = {}
    size = 0
    for member in archive:
        name = Path(member.name)
        require(not name.is_absolute() and '..' not in name.parts, f'unsafe archive: {name}')
        if member.isdir():
            continue
        require(member.isfile() and member.name not in result, f'nonregular/duplicate: {name}')
        result[member.name] = hashlib.file_digest(archive.extractfile(member), 'sha256').hexdigest()
        size += member.size
    return result, size


def source_check():
    require(fixture('READY.md').is_file(), 'completed source READY absent')
    require(file_sha(fixture('freeze.json')) == FREEZE_SHA, 'source freeze changed')
    freeze = json.loads(fixture('freeze.json').read_text())
    for name, digest in freeze['fixture_sha256'].items():
        require(file_sha(DESIGN / name) == digest, f'frozen artifact changed: {name}')
    require(file_sha(fixture('main-source.tar.gz')) == SOURCE_SHA, 'source archive changed')
    require(file_sha(fixture('locked-composition6.tar.gz')) == ARCHIVE_SHA, 'locked6 archive changed')
    identity = json.loads(fixture('source-identity.json').read_text())
    require((identity['main'], identity['composition_source']) == (MAIN, COMPOSITION), 'wrong source tuple')
    with tarfile.open(fixture('main-source.tar.gz')) as archive:
        staged, size = tar_hashes(archive)
    original = subprocess.check_output(['git', '-C', str(REPO), 'archive', MAIN, *SOURCE_PATHS])
    with tarfile.open(fileobj=io.BytesIO(original)) as archive:
        expected, _ = tar_hashes(archive)
    require(len(expected) == 2414, 'original MAIN membership changed')
    require(all(staged.get(k) == v for k, v in expected.items()), 'frozen source differs from original MAIN')
    package_prefix = 'remotion/node_modules/@banodoco/timeline-composition/'
    package = {k.removeprefix(package_prefix): v for k, v in staged.items() if k.startswith(package_prefix)}
    require(package == identity['package_after_generation'], 'generated locked6 members changed')
    generated_lock = {'remotion/.astrid-registry.lock': sha(b'')}
    require(staged == {**expected, **generated_lock, **{package_prefix + k: v for k, v in package.items()}},
            'unexpected source archive entries')
    require(all(expected.get(k) == v for k, v in identity['source_sha256'].items()), 'source subset differs')
    with tarfile.open(fixture('locked-composition6.tar.gz')) as archive:
        locked, _ = tar_hashes(archive)
    locked = {str(Path(k).relative_to('timeline-composition-0.0.6')): v for k, v in locked.items()}
    require(len(locked) == 29 and locked == identity['package_before'], 'locked6 is not exact 29-member archive')
    lock = json.loads(subprocess.check_output(['git', '-C', str(REPO), 'show', MAIN + ':remotion/package-lock.json']))
    integrity = 'sha512-' + base64.b64encode(hashlib.sha512(fixture('locked-composition6.tar.gz').read_bytes()).digest()).decode()
    require(lock['packages']['node_modules/@banodoco/timeline-composition'] == identity['lock_entry'], 'MAIN lock changed')
    require(identity['lock_entry']['version'] == '0.0.6' and identity['lock_entry']['integrity'] == integrity,
            'archive does not match MAIN lock integrity')
    return {'main': MAIN, 'composition6': COMPOSITION, 'source_archive_sha256': SOURCE_SHA,
            'archive_sha256': ARCHIVE_SHA, 'archive_integrity': integrity,
            'original_main_files': len(expected), 'locked_archive_members': locked,
            'generated_package_members': package, 'generated_maps': identity['generated_sha256'],
            'source_files': staged, 'unpacked_bytes': size,
            'seven_expected_output_hashes': {name: file_sha(fixture(name)) for name in OUTPUTS}}


def graph_check():
    prior_path = DESIGN / 'handoff-vw-m3-main-image-cap-render-proof-preflight.json'
    require(file_sha(prior_path) == PRIOR_SHA, 'retained peer preflight changed')
    prior = json.loads(prior_path.read_text())
    graph_revision = subprocess.check_output(['git', '-C', str(GRAPH.parent), 'rev-parse', 'HEAD'], text=True).strip()
    require(graph_revision == 'f8164bef73215272562c4d6974acadbd82c2898a', 'physical SSR checkout changed')
    graph = inventory(GRAPH)
    digest = sha(json.dumps(graph, sort_keys=True, separators=(',', ':')).encode())
    require(digest == prior['graph_manifest_sha256'], 'complete physical SSR graph changed')
    peers = {name: file_sha(GRAPH / name) for name in prior['six_peer_hashes_before']}
    require(peers == prior['six_peer_hashes_before'], 'six peer hashes changed')
    for name, info in prior['peer_versions'].items():
        path = GRAPH / name / 'package.json'
        require(file_sha(path) == info['package_json_sha256'], f'peer package changed: {name}')
        require(json.loads(path.read_text())['version'] == info['version'], f'peer version changed: {name}')
    tools = {'node': file_sha(NODE), 'browser': file_sha(BROWSER)}
    require(tools == prior['tools'], 'Node/browser bytes changed')
    return {'path': str(GRAPH), 'checkout': graph_revision, 'entries': len(graph), 'sha256': digest,
            'six_peer_hashes': peers, 'versions': prior['peer_versions'], 'tools': tools}, graph


THEME_REPO = Path('/home/user/work/composition')
THEME_COMMIT = '1db8440aabf0769b01453831a06f3c609bbc90c9'
THEME_OLD = '4974bdb471cf4dda0ce39d2cc24a1d62420a1305'
THEME_ARCHIVE_SHA = '796f0691882f78ae8627cd384f6a46561e73c007f3816bc3afb75d444496f3e2'
THEME_PROOF_SHA = '02bc75eb4f55b09461d98de808a12b8927f1848fa553b5606de333a082369cac'
RESOLVER_SHA = '4bf946ba237fec6dbda323bb7a133eb07973f36c2c33679d76b3278c293b4c9f'


def theme_check():
    archive_path = Path(str(PREFIX) + 'theme-source.git.tar')
    proof_path = Path(str(PREFIX) + 'theme-proof.json')
    require(file_sha(archive_path) == THEME_ARCHIVE_SHA, 'theme git archive changed')
    require(file_sha(proof_path) == THEME_PROOF_SHA, 'theme proof changed')
    proof = json.loads(proof_path.read_text())
    original = subprocess.check_output(['git', '-C', str(THEME_REPO), 'archive', THEME_COMMIT])
    previous = subprocess.check_output(['git', '-C', str(THEME_REPO), 'archive', THEME_OLD])
    with tarfile.open(fileobj=io.BytesIO(original)) as archive:
        expected, size = tar_hashes(archive)
    with tarfile.open(fileobj=io.BytesIO(previous)) as archive:
        old, _ = tar_hashes(archive)
    with tarfile.open(archive_path) as archive:
        actual, _ = tar_hashes(archive)
        package = json.load(archive.extractfile('package.json'))
    require(actual == expected == proof['member_sha256'] and len(actual) == 20, 'theme members differ from git tag source')
    require(old == proof['v0.1.0_member_sha256'] and old.keys() == actual.keys(), 'historical theme membership differs')
    require([k for k in old if old[k] != actual[k]] == ['package.json'], 'theme implementation differs')
    lock = json.loads(subprocess.check_output(['git', '-C', str(REPO), 'show', MAIN + ':remotion/package-lock.json']))
    manifest = json.loads(subprocess.check_output(['git', '-C', str(REPO), 'show', MAIN + ':remotion/package.json']))
    entry = lock['packages']['node_modules/@banodoco/timeline-theme-2rp']
    require(entry == proof['main_lock_entry'] and entry['version'] == package['version'] == '0.1.1', 'theme MAIN version differs')
    require(manifest['dependencies'][package['name']] == entry['resolved'] == proof['main_dependency'], 'theme MAIN dependency differs')
    require(proof['github_archive_integrity_verified'] is False, 'must not claim GitHub archive integrity')
    return {**proof, 'unpacked_bytes': size}


def stage_theme(root, theme):
    target = root / 'remotion/node_modules/@banodoco/timeline-theme-2rp'
    real_parents(target)
    require(not target.exists(), 'theme would overwrite existing package')
    target.mkdir(parents=True)
    with tarfile.open(Path(str(PREFIX) + 'theme-source.git.tar')) as archive:
        for member in archive:
            if member.isdir():
                continue
            require(member.name in theme['member_sha256'] and member.isfile(), 'unapproved theme member')
            leaf = target / member.name
            real_parents(leaf.parent)
            leaf.parent.mkdir(parents=True, exist_ok=True)
            leaf.write_bytes(archive.extractfile(member).read())
    require(inventory(target) == theme['member_sha256'], 'staged theme differs')


def stage_peers(root):
    modules = root / 'remotion/node_modules'
    for item in sorted(GRAPH.iterdir()):
        if item.name.startswith('.'):
            continue
        if item.name.startswith('@'):
            scope = modules / item.name
            real_parents(scope)
            scope.mkdir(exist_ok=True)
            for leaf in sorted(item.iterdir()):
                if item.name == '@banodoco' and leaf.name in ('timeline-composition', 'timeline-theme-2rp'):
                    continue
                (scope / leaf.name).symlink_to(leaf.resolve(strict=True), target_is_directory=leaf.is_dir())
        else:
            (modules / item.name).symlink_to(item.resolve(strict=True), target_is_directory=item.is_dir())


def dependency_check(root, name, granted=False):
    resolver = Path(str(PREFIX) + 'resolve.mjs')
    require(file_sha(resolver) == RESOLVER_SHA, 'offline resolver changed')
    if granted:
        script_grant()
    env = dict(os.environ, ASTRID_PACKS_PATH='', PYTHONDONTWRITEBYTECODE='1')
    for key in ('NODE_PATH', 'NODE_OPTIONS'):
        env.pop(key, None)
    process = subprocess.run([str(NODE), str(resolver), str(root)], env=env, text=True, capture_output=True)
    require(process.stdout, f'offline resolver failed before report: {process.stderr}')
    result = json.loads(process.stdout)
    evidence(name, result)
    require(process.returncode == 0 and result['status'] == 'PASS', f'dependency resolution failed: {name}')
    require(len(result['registry_files']) == 4, 'incomplete original registry scan')
    return result


def offline_dependencies(source, theme):
    stage = Path(str(PREFIX) + 'resolver-stage')
    real_parents(stage)
    require(not stage.exists(), 'offline resolver stage exists; refusing overwrite')
    disk(source['unpacked_bytes'] + theme['unpacked_bytes'] + HEADROOM + PNG_RAW + 16 * 1024**2)
    stage.mkdir()
    try:
        root = stage / 'main'
        root.mkdir()
        with tarfile.open(fixture('main-source.tar.gz')) as archive:
            for member in archive:
                if member.isdir():
                    continue
                require(member.name in source['source_files'] and member.isfile(), 'unapproved source member')
                target = root / member.name
                real_parents(target.parent)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(archive.extractfile(member).read())
        stage_theme(root, theme)
        stage_peers(root)
        verify_stage(stage, source, replayed=False)
        result = dependency_check(root, 'dependencies.json')
        verify_stage(stage, source, replayed=False)
        return result
    finally:
        real_parents(stage)
        shutil.rmtree(stage)


def preflight():
    source = source_check()
    theme = theme_check()
    before, graph = graph_check()
    after, graph_after = graph_check()
    require(before == after and graph == graph_after, 'physical graph changed during preflight')
    remaining = source['unpacked_bytes'] + theme['unpacked_bytes'] + HEADROOM + PNG_RAW + 16 * 1024**2
    blockers = []
    try:
        free = disk(remaining)
    except RuntimeError as exc:
        free = shutil.disk_usage(OWN).free
        blockers.append(str(exc))
    dependencies = None
    if not blockers:
        dependencies = offline_dependencies(source, theme)
    after, graph_after = graph_check()
    require(before == after and graph == graph_after, 'physical graph changed during dependency preflight')
    result = {'status': 'STAGE_BLOCKED' if blockers else 'OFFLINE_PREFLIGHT_PASS_NOT_CAPTURE_GRANTED',
              'blockers': blockers, 'source': source, 'theme': theme, 'dependencies': dependencies, 'graph_before': before, 'graph_after': after,
              'free_bytes': free, 'reserve_bytes': FLOOR, 'staging_headroom_bytes': remaining,
              'required_before_extraction_bytes': FLOOR + remaining,
              'capture_grant_present': GRANT.is_file(), 'capture_run': False,
              'metadata_expected_not_measured': {'width': 1920, 'height': 1080, 'fps': 30, 'durationInFrames': 120},
              'frames': FRAMES, 'estimated_png_count': 3, 'png_raw_total_bytes': PNG_RAW,
              'png_retained_estimate': '<1 MiB total for this flat image; not a measured size',
              'binding': 'explicit static-public executable analog only'}
    evidence('graph-pre.json', graph)
    evidence('preflight.json', result)
    return result


def run_process(command, cwd, env, log):
    script_grant()  # Recheck approved bytes before every generator/replay/renderer execution.
    real_parents(log.parent)
    require(not log.is_symlink(), f'log symlink: {log}')
    with log.open('x') as stream:
        process = subprocess.Popen([str(x) for x in command], cwd=cwd, env=env,
                                   stdout=stream, stderr=subprocess.STDOUT, start_new_session=True)
        try:
            while process.poll() is None:
                disk(0)
                time.sleep(0.5)
            require(process.returncode == 0, f'command exit {process.returncode}; see {log}')
        except BaseException:
            try:
                os.killpg(process.pid, signal.SIGTERM)
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            except ProcessLookupError:
                pass
            raise


def source_stage(stage, source):
    disk(source['unpacked_bytes'] + theme_check()['unpacked_bytes'] + HEADROOM + PNG_RAW + 16 * 1024**2)
    real_parents(stage)
    require(stage.is_dir(), 'attempt-owned stage missing')
    root = stage / 'main'
    root.mkdir()
    with tarfile.open(fixture('main-source.tar.gz')) as archive:
        for member in archive:
            if member.isdir():
                continue
            target = root / member.name
            require(member.name in source['source_files'] and member.isfile(), 'unapproved archive member')
            real_parents(target.parent)
            target.parent.mkdir(parents=True, exist_ok=True)
            disk(HEADROOM + PNG_RAW)
            target.write_bytes(archive.extractfile(member).read())
    verify_stage(stage, source, replayed=False)
    # Original generator, original packs, existing locked package. No peer access yet.
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONPATH=str(root), ASTRID_PACKS_PATH='',
               ASTRID_TIMELINE_COMPOSITION_SRC=str(root / 'remotion/node_modules/@banodoco/timeline-composition/typescript/src'))
    for name in ('NODE_PATH', 'NODE_OPTIONS'):
        env.pop(name, None)
    run_process([PYTHON, root / 'scripts/gen_effect_registry.py'], root, env,
                Path(str(PREFIX) + 'generator.log'))
    verify_stage(stage, source, replayed=False)
    replay = stage / 'replayed-'
    for name in ('raw-closure.json', 'image.png'):
        shutil.copyfile(fixture(name), Path(str(replay) + name))
    run_process([PYTHON, fixture('replay.py'), replay], root, env, Path(str(PREFIX) + 'replay.log'))
    checks = {}
    for name in OUTPUTS:
        actual = Path(str(replay) + name)
        require(actual.read_bytes() == fixture(name).read_bytes(), f'raw closure replay differs: {name}')
        checks[name] = file_sha(actual)
    evidence('seven-output-replay.json', {'byte_equal': True, 'outputs': checks})
    # The only runtime URL binding change: static-public analog, never a server claim.
    public_image = root / 'remotion/public/image-cap.png'
    require(not public_image.exists(), 'static analog would replace original MAIN public file')
    shutil.copyfile(fixture('image.png'), public_image)
    stage_theme(root, theme_check())
    stage_peers(root)
    modules = root / 'remotion/node_modules'
    # This is a REAL private cache parent; no shared scope/cache symlinks.
    (modules / '.cache/webpack').mkdir(parents=True)
    for folder in ('tmp', 'cache'):
        (stage / folder).mkdir()
    verify_stage(stage, source)
    dependency_check(root, 'capture-dependencies.json', granted=True)
    return root


def verify_stage(stage, source, replayed=True):
    root = stage / 'main'
    composition_root = root / 'remotion/node_modules/@banodoco/timeline-composition'
    real_parents(composition_root)
    require(inventory(composition_root) == source['generated_package_members'], 'staged MAIN6 membership/bytes changed')
    theme_root = root / 'remotion/node_modules/@banodoco/timeline-theme-2rp'
    if theme_root.exists():
        require(not theme_root.is_symlink(), 'theme package must be real')
        require(inventory(theme_root) == theme_check()['member_sha256'], 'staged historical theme changed')
    elif replayed:
        require(False, 'staged historical theme missing')
    for name, digest in source['source_files'].items():
        target = root / name
        real_parents(target)
        require(file_sha(target) == digest, f'staged source changed: {name}')
    if replayed:
        for name in OUTPUTS:
            require(Path(str(stage / 'replayed-') + name).read_bytes() == fixture(name).read_bytes(),
                    f'replayed output changed: {name}')
        require(file_sha(root / 'remotion/public/image-cap.png') == file_sha(fixture('image.png')), 'analog image changed')


def suite_line():
    return f'agent {SUITE} {PYTHON} {PREFIX}controller.py capture'


def script_grant():
    require(GRANT.is_file() and not GRANT.is_symlink(), f'manager exact grant missing: {GRANT}')
    controller = Path(__file__).absolute()
    render = Path(str(PREFIX) + 'render.mjs')
    require(controller == Path(str(PREFIX) + 'controller.py'), 'unapproved controller path')
    for path in (GRANT, controller, render):
        real_parents(path)
    approved = [suite_line(), f'controller_sha256={file_sha(controller)}', f'render_sha256={file_sha(render)}']
    require(GRANT.read_text().strip().splitlines() == approved,
            'manager grant must bind the exact suite and controller/render SHA256')


def central_grant():
    script_grant()
    lines = (ORCH / 'tests/suites.conf').read_text().splitlines()
    require(lines.count(suite_line()) == 1, 'manager named suite absent/different/duplicated')
    cwd = Path.cwd().resolve()
    require(cwd.parent == Path('/home/user/work/wt') and cwd.name.startswith('.test-'), 'capture is central-service-only')
    result = ORCH / 'tests' / cwd.name.removeprefix('.test-')
    require((result / 'status').read_text().strip() == 'running', 'service request is not running')
    request = (result / 'request').read_text().splitlines()
    require(f'target={WORKER}' in request and f'suite={SUITE}' in request, 'wrong service worker/suite')
    return str(result)


def measure():
    from PIL import Image

    props = json.loads(fixture('main-props-static-analog.json').read_text())
    color = props['theme']['visual']['color']['bg']
    require(color == '#050814', 'unexpected background; review before measurement')
    background = tuple(int(color[i:i + 2], 16) for i in (1, 3, 5))
    coordinates = [(x, y) for x in (192, 576, 960, 1344, 1728) for y in (108, 324, 540, 756, 972)]
    pixels = {}
    files = {}
    for frame in FRAMES:
        path = Path(str(PREFIX) + f'frame-{frame}.png')
        with Image.open(path) as image:
            require(image.size == (1920, 1080), 'wrong PNG dimensions')
            rgba = image.convert('RGBA')
            pixels[frame] = [rgba.getpixel(point) for point in coordinates]
            extrema = rgba.getextrema()
        files[frame] = {'path': str(path), 'sha256': file_sha(path), 'bytes': path.stat().st_size,
                        'sample_rgba': pixels[frame], 'full_image_rgba_extrema': extrema}
    control = pixels[90]
    require(all(max(abs(value[c] - 240) for c in range(3)) <= 1 for value in control),
            'frame90 full-opacity pixel control failed; no opacity inference accepted')
    estimates = {}
    for frame in FRAMES:
        ratios = [(sample[c] - background[c]) / (reference[c] - background[c])
                  for sample, reference in zip(pixels[frame], control) for c in range(3)]
        estimates[frame] = {'median': statistics.median(ratios), 'min': min(ratios), 'max': max(ratios)}
    return {'files': files, 'background_rgb': background,
            'background_basis': 'unchanged MAIN6 AbsoluteFill and exact prepared theme; no separate background PNG',
            'control': 'actual frame90 RGB versus known input RGB240; never output PNG alpha',
            'method': '(frameRGB-backgroundRGB)/(frame90RGB-backgroundRGB), 25 points x 3 channels',
            'opacity_inferred_from_rgb': estimates,
            'source_prediction_only': {'90': 1, '105': 0.5, '119': 1 / 30},
            'visual_golden_selected': False, 'binding': 'static-public executable analog'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('preflight', 'capture'))
    args = parser.parse_args()
    service = None
    if args.mode == 'capture':
        service = central_grant()  # Before staging, imports of renderer, sockets, or render.
    result = preflight()
    print(json.dumps({k: result[k] for k in ('status', 'blockers', 'free_bytes', 'required_before_extraction_bytes')}, indent=2))
    if result['blockers']:
        return 1
    if args.mode == 'preflight':
        return 0
    stage = Path(str(PREFIX) + 'capture-stage')
    with Path(str(PREFIX) + 'capture.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        # One actual attempt only. A failed attempt requires manager review, never automatic resubmission.
        with Path(str(PREFIX) + 'CAPTURE-STARTED').open('x') as marker:
            marker.write(service + '\n')
        before, _ = graph_check()
        error = None
        source_post = False
        stage_allocated = False
        try:
            script_grant()
            disk(result['source']['unpacked_bytes'] + result['theme']['unpacked_bytes'] + HEADROOM + PNG_RAW + 16 * 1024**2)
            real_parents(stage.parent)
            require(not stage.exists() and not stage.is_symlink(), 'stage already exists; refusing overwrite')
            stage.mkdir()
            stage_allocated = True
            root = source_stage(stage, result['source'])
            disk(HEADROOM + PNG_RAW)
            graph_check()
            env = dict(os.environ, TMPDIR=str(stage / 'tmp'), XDG_CACHE_HOME=str(stage / 'cache'),
                       ASTRID_PACKS_PATH='', PYTHONDONTWRITEBYTECODE='1', MAIN_CAP_SERVICE_RESULT=service)
            for name in ('NODE_OPTIONS', 'NODE_PATH'):
                env.pop(name, None)
            run_process([NODE, Path(str(PREFIX) + 'render.mjs'), stage], root / 'remotion', env,
                        Path(str(PREFIX) + 'capture.log'))
            evidence('measurement.json', measure())
        except BaseException as exc:
            error = str(exc)
            raise
        finally:
            try:
                post_errors = []
                after = None
                try:
                    require(stage_allocated, 'stage was not allocated by this attempt')
                    verify_stage(stage, result['source'])
                    require(source_check() == result['source'], 'immutable fixture changed across capture')
                    source_post = True
                except Exception as exc:
                    post_errors.append(str(exc))
                try:
                    # Retain the actual graph even when strict identity validation fails.
                    evidence('graph-post.json', inventory(GRAPH))
                    after, _ = graph_check()
                    require(before == after, 'graph changed across capture; result invalid')
                    disk(0)
                except Exception as exc:
                    post_errors.append(str(exc))
                evidence('postflight.json', {'service_result': service, 'error': error, 'post_errors': post_errors,
                         'source_byte_equal': source_post, 'graph_before': before, 'graph_after': after,
                         'graph_unchanged': before == after, 'free_bytes': shutil.disk_usage(OWN).free,
                         'valid': error is None and not post_errors})
                require(not post_errors, f'postflight failed: {post_errors}; capture error: {error}')
            finally:
                # Allocation ownership survives partial staging and postflight failures.
                if stage_allocated:
                    real_parents(stage)
                    shutil.rmtree(stage)
        require(source_post, 'source postflight failed')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        evidence('last-blocker.json', {'status': 'BLOCKED', 'reason': str(exc), 'capture_claim': False})
        print(f'BLOCKED: {exc}', flush=True)
        raise SystemExit(1)
