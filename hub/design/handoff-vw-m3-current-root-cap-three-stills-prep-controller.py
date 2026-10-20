"""One UNCERTIFIED currentRoot static reference; browser use requires central review grant."""
import argparse
import base64
import fcntl
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import statistics
import signal
import subprocess
import sys
import tarfile
import tempfile
import time

sys.dont_write_bytecode = True
ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
WORKER = 'vw-m3-current-root-cap-three-stills-prep'
OWN = ORCH / 'workers' / WORKER
PREFIX = ORCH / 'design' / ('handoff-' + WORKER + '-')
REPO = Path('/home/user/work/agent')
REV = '4ef1391c2c104d5d11b3a27265035c51be296045'
TREE = 'afb2ed8506a99a088d7be3dbadaf593338d2fb5a'
GRAPH = Path('/home/user/work/wt/vw-m1-ssr-snapshot/remotion/node_modules')
NODE = OWN / 'node'
PYTHON = Path('/home/user/work/venv-agent/bin/python')
CHROME = Path('/opt/google/chrome/chrome')
PACKAGE = ORCH / 'artifacts/banodoco-timeline-composition-0.0.12.tgz'
FIXTURE = ORCH / 'design/handoff-vw-m3-frame-retained-genesis-fixture-fixture.json'
MAIN = ORCH / 'design/handoff-vw-m3-main-cap-locked-theme-stage-'
SUITE = 'e2e-viewing-current-root-cap-three-stills'
PATHS = ('astrid', 'scripts/gen_effect_registry.py', 'remotion', 'pyproject.toml', 'tests/editing_conformance/fixtures/visual_compile_contract.json')
FRAMES = (90, 105, 119)
FLOOR = 10 * 1024**3
HEADROOM = 2 * 1024**3
RAW_PNG_BYTES = 3 * 1920 * 1080 * 4


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def file_sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def output(name):
    return Path(str(PREFIX) + name)


def save(name, value):
    path = output(name)
    real(path.parent)
    require(not path.is_symlink(), 'evidence symlink')
    path.write_text(json.dumps(value, indent=2) + '\n')


def real(path):
    require(path.is_absolute() and not any(p.is_symlink() for p in (path, *path.parents)), f'unsafe parent: {path}')


def resources(remaining=0):
    require(not any(p.exists() for p in (ORCH / 'QUIET.md', ORCH / 'managers/viewing/QUIET.md')), 'QUIET active')
    free = shutil.disk_usage(OWN).free
    require(free >= FLOOR + remaining, f'disk floor/headroom: {free} < {FLOOR + remaining}')
    return free


def inventory(root):
    result = {}
    def walk(folder, ancestors):
        target = folder.resolve(strict=True)
        require(target not in ancestors, f'cyclic dependency: {folder}')
        require(not any(str(target).startswith(p) for p in (
            '/home/user/work/app/node_modules', '/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules')), 'polluted graph')
        for path in sorted(folder.iterdir()):
            key = str(path.relative_to(root))
            if path.is_symlink():
                result[key + '@link'] = os.readlink(path)
            if path.is_dir():
                walk(path, ancestors | {target})
            else:
                require(path.is_file(), f'nonregular dependency: {path}')
                result[key] = file_sha(path)
    walk(root, set())
    return result


def chrome_tree():
    entries = []
    for path in sorted(CHROME.parent.rglob('*')):
        name = str(path.relative_to(CHROME.parent))
        if path.is_symlink():
            entries.append([name, 'symlink', digest(os.readlink(path).encode())])
        elif path.is_file():
            entries.append([name, 'executable' if path.stat().st_mode & 0o111 else 'file', file_sha(path)])
        else:
            require(path.is_dir(), 'unsupported Chrome tree member')
    entries.sort(key=lambda row: row[0])
    return {'sha256': digest(json.dumps(entries, separators=(',', ':'), ensure_ascii=False).encode()), 'fileCount': len(entries)}


def graph_check():
    prior = json.loads((ORCH / 'design/handoff-vw-m3-main-image-cap-render-proof-preflight.json').read_text())
    tree = inventory(GRAPH)
    summary = {'entries': len(tree), 'sha256': digest(json.dumps(tree, sort_keys=True, separators=(',', ':')).encode()),
               'six_peers': {name: file_sha(GRAPH / name) for name in prior['six_peer_hashes_before']}}
    require(summary['entries'] == 21488 and summary['sha256'] == '9e556a876a02ee4f4ed3e8215eaaf793ac0ba66a6d85e503747f635521acc425', 'whole f816 graph changed')
    require(summary['six_peers'] == prior['six_peer_hashes_before'], 'six peers changed')
    require(subprocess.check_output(['git', '-C', str(GRAPH.parent), 'rev-parse', 'HEAD'], text=True).strip()
            == 'f8164bef73215272562c4d6974acadbd82c2898a', 'physical peer checkout changed')
    require(file_sha(NODE) == '43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490', 'Node executable changed')
    require(file_sha(CHROME) == 'cb19b59995072b86cc7f887b3b1c7ab1f63518a7f2ed9f0d33249e1a040e2c76', 'Chrome executable changed')
    chrome = chrome_tree()
    require(chrome == {'sha256': '5b9b48fad617dc414d4a18ccfe9c7933c7bc4a8efd78c70d4f7a9e853808de0e', 'fileCount': 255}, 'Chrome155 tree changed')
    return {**summary, 'node_sha256': file_sha(NODE), 'chrome': chrome}


def tar_members(archive, prefix=''):
    members = {}
    for member in archive:
        name = Path(member.name)
        require(not name.is_absolute() and '..' not in name.parts, 'unsafe tar path')
        if member.isdir():
            continue
        require(member.isfile(), 'tar links forbidden')
        key = str(name.relative_to(prefix)) if prefix else str(name)
        require(key not in members, 'duplicate tar member')
        members[key] = archive.extractfile(member).read()
    return members


def source():
    require(subprocess.check_output(['git', '-C', str(REPO), 'rev-parse', REV + '^{tree}'], text=True).strip() == TREE, 'wrong frozen source')
    raw = subprocess.check_output(['git', '-C', str(REPO), 'archive', REV, *PATHS])
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        members = tar_members(archive)
    require(file_sha(PACKAGE) == '0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3', 'immutable public12 tar changed')
    require(members['remotion/artifacts/' + PACKAGE.name] == PACKAGE.read_bytes(), 'Agent artifact is not immutable public12')
    lock = json.loads(members['remotion/package-lock.json'])['packages']['node_modules/@banodoco/timeline-composition']
    integrity = 'sha512-' + base64.b64encode(hashlib.sha512(PACKAGE.read_bytes()).digest()).decode()
    require(lock['version'] == '0.0.12' and lock['integrity'] == integrity, 'public12 lock integrity differs')
    with tarfile.open(PACKAGE) as archive:
        package = tar_members(archive, 'package')
    require(len(package) == 77, 'public12 membership changed')
    golden = json.loads(members['tests/editing_conformance/fixtures/visual_compile_contract.json'])
    case = golden['single_occurrence_cap_closure']
    require(case['physical_reference']['status'] == 'settled-main-image-reference' and case['expect']['opacity'] == 0.5, 'published Agent golden differs')
    expected_pngs = ('7640face10c33eb4c8682b890ddcc6faacaf0e57c0810e9438e4b2df8a88444a', 'c0b0adc7856e2750137315451a9657661925436746d0da1e9cd6a2527d14431b', '128017371420be346796916879dc2e5faac0f2761d5025018e392913abea63be')
    for frame, expected in zip(FRAMES, expected_pngs):
        require(file_sha(Path(str(MAIN) + f'frame-{frame}.png')) == expected, 'MAIN reference changed')
    return members, package


def environment(stage, root):
    env = {k: v for k, v in os.environ.items() if k not in ('NODE_PATH', 'NODE_OPTIONS', 'NODE_COMPILE_CACHE')}
    env.update(PYTHONDONTWRITEBYTECODE='1', PYTHONPATH=str(root), ASTRID_PACKS_PATH='',
               ASTRID_REMOTION_PROJECT_DIR=str(root / 'remotion'), TMPDIR=str(stage), TMP=str(stage), TEMP=str(stage),
               XDG_CACHE_HOME=str(stage / 'cache'), XDG_CONFIG_HOME=str(stage / 'config'))
    return env


def run(command, stage, root, name):
    with output(name).open('a') as stream:
        process = subprocess.Popen(list(map(str, command)), cwd=root, env=environment(stage, root),
                                   stdout=stream, stderr=subprocess.STDOUT, start_new_session=True)
        try:
            while process.poll() is None:
                resources()
                time.sleep(0.5)
            require(process.returncode == 0, f'exit {process.returncode}: {command[1]}; see {output(name)}')
        finally:
            if process.poll() is None:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()


def verify_outputs(stage, root, observed):
    for name, expected in observed['generated'].items():
        require(file_sha(root / name) == expected, f'generated registry changed: {name}')
    for name, expected in observed['replay'].items():
        require(file_sha(stage / 'replayed' / name) == expected, f'compiled output changed: {name}')
    require(file_sha(root / 'remotion/public/image-cap.png') == 'ec19e1c7d1d247d56db54f73e6514c92a82147a1b6ab59eaa30edeebca2e82b6', 'static PNG changed')


def verify(root, members, package):
    for name, data in members.items():
        real(root / name)
        require(file_sha(root / name) == digest(data), f'original Agent file changed: {name}')
    pkg = root / 'remotion/node_modules/@banodoco/timeline-composition'
    require(inventory(pkg) == {k: digest(v) for k, v in package.items()}, 'public12 overlay changed')


def stage_source(stage, members, package):
    root = stage / 'agent'
    root.mkdir()
    for name, data in members.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    pkg = root / 'remotion/node_modules/@banodoco/timeline-composition'
    for name, data in package.items():
        path = pkg / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    run([PYTHON, root / 'scripts/gen_effect_registry.py'], stage, root, 'generator.log')
    run([PYTHON, output('replay.py'), root, FIXTURE, stage / 'replayed'], stage, root, 'replay.log')
    modules = root / 'remotion/node_modules'
    for item in sorted(GRAPH.iterdir()):
        if item.name.startswith('.'):
            continue
        if item.name.startswith('@'):
            scope = modules / item.name
            real(scope)
            scope.mkdir(exist_ok=True)
            for leaf in sorted(item.iterdir()):
                if item.name == '@banodoco' and leaf.name == 'timeline-composition':
                    continue
                (scope / leaf.name).symlink_to(leaf.resolve(strict=True), target_is_directory=leaf.is_dir())
        else:
            (modules / item.name).symlink_to(item.resolve(strict=True), target_is_directory=item.is_dir())
    verify(root, members, package)
    process = subprocess.run([str(NODE), str(output('resolve.mjs')), str(root)], env=environment(stage, root), text=True, capture_output=True)
    require(process.stdout, process.stderr)
    resolution = json.loads(process.stdout)
    save('dependencies.json', resolution)
    require(process.returncode == 0 and resolution['status'] == 'PASS', 'dependency resolution failed')
    normalized = json.loads(json.dumps(resolution).replace(str(root), '<source>'))
    observed = {'source_files': {k: digest(v) for k, v in members.items()},
                'public12_members': {k: digest(v) for k, v in package.items()},
                'generated': {str(p.relative_to(root)): file_sha(p) for p in (root / 'remotion/src').glob('*.generated.ts')},
                'replay': {p.name: file_sha(p) for p in (stage / 'replayed').iterdir()},
                'resolution_sha256': digest(json.dumps(normalized, sort_keys=True, separators=(',', ':')).encode())}
    return root, observed


def suite_line():
    return f'composition {SUITE} {PYTHON} {PREFIX}controller.py capture'


def grant():
    real(output('CAPTURE-GRANT.txt'))
    manifest = json.loads(output('manifest.json').read_text())
    for name, expected in manifest['scripts'].items():
        require(file_sha(output(name)) == expected, f'reviewed script changed: {name}')
    require(output('CAPTURE-GRANT.txt').read_text().strip().splitlines() == [suite_line(),
        'controller_sha256=' + file_sha(output('controller.py')),
        'manifest_sha256=' + file_sha(output('manifest.json'))], 'manager exact grant required')
    require((ORCH / 'tests/suites.conf').read_text().splitlines().count(suite_line()) == 1, 'exact central suite missing')
    cwd = Path.cwd().resolve()
    require(cwd.parent == Path('/home/user/work/wt') and cwd.name.startswith('.test-'), 'central-service-only capture')
    result = ORCH / 'tests' / cwd.name.removeprefix('.test-')
    require((result / 'status').read_text().strip() == 'running', 'central service inactive')
    lines = (result / 'request').read_text().splitlines()
    require(f'target={WORKER}' in lines and f'suite={SUITE}' in lines, 'wrong central request')
    return result


def compare():
    from PIL import Image, ImageChops
    files = {}
    for frame in FRAMES:
        current, reference = output(f'frame-{frame}.png'), Path(str(MAIN) + f'frame-{frame}.png')
        with Image.open(current) as a, Image.open(reference) as b:
            require(a.size == b.size == (1920, 1080), 'PNG dimensions differ; no resize allowed')
            rgb, baseline = a.convert('RGB'), b.convert('RGB')
            difference = ImageChops.difference(rgb, baseline)
            maximum = max(upper for _, upper in difference.getextrema())
            changed = sum(1 for value in difference.getdata() if max(value) > 2)
            files[str(frame)] = {'sha256': file_sha(current), 'bytes': current.stat().st_size,
                'reference_sha256': file_sha(reference), 'rgb_sha256': digest(rgb.tobytes()),
                'rgba_extrema': a.convert('RGBA').getextrema(), 'rgb_histogram': rgb.getcolors(1920 * 1080),
                'center_rgb': rgb.getpixel((960, 540)),
                'all_pixels': 1920 * 1080, 'max_rgb_channel_difference_255': maximum,
                'pixels_exceeding_2_255': changed, 'pass': maximum <= 2}
    control = files['90']['center_rgb']
    midpoint = files['105']['center_rgb']
    background = (5, 8, 20)
    require(all(abs(c - 240) <= 1 for c in control), 'actual frame90 RGB control failed')
    fraction = statistics.median((midpoint[i] - background[i]) / (control[i] - background[i]) for i in range(3))
    # No exemptions: known intended source differences are reported separately.
    save('comparison.json', {'files': files, 'threshold_255': 2, 'pass': all(f['pass'] for f in files.values()),
        'opacity105_inferred_from_actual_rgb': fraction,
        'opacity_method': '(frame105RGB - backgroundRGB) / (actual frame90RGB - backgroundRGB); median RGB, never alpha',
        'approved_known_intended_pixel_differences': [], 'claim': 'UNCERTIFIED static compiled currentRoot vs exact MAIN stills'})
    require(all(f['pass'] for f in files.values()), 'full RGB comparison failed; preserve outputs and report')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('freeze', 'preflight', 'capture'))
    mode = parser.parse_args().mode
    service = grant() if mode == 'capture' else None
    resources()
    before = graph_check()
    members, package = source()
    remaining = sum(map(len, members.values())) + sum(map(len, package.values())) + HEADROOM + RAW_PNG_BYTES
    free = resources(remaining)
    manifest = None if mode == 'freeze' else json.loads(output('manifest.json').read_text())
    if manifest:
        for name, expected in manifest['scripts'].items():
            require(file_sha(output(name)) == expected, f'script changed: {name}')
        for path, expected in manifest['inputs'].items():
            require(file_sha(path) == expected, f'input changed: {path}')
    lock_path = Path('/tmp/timeline-viewing-browser.lock') if mode == 'capture' else OWN / 'offline.lock'
    real(lock_path)
    with lock_path.open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if service:
            grant()
            with output('CAPTURE-STARTED').open('x') as marker:
                marker.write(str(service) + '\n')
        stage = Path(tempfile.mkdtemp(prefix='vw-cap-', dir='/tmp'))
        require(stage.stat().st_mode & 0o777 == 0o700, 'short temp must be private 0700')
        error = None
        observed = None
        try:
            root, observed = stage_source(stage, members, package)
            if manifest:
                require(observed == manifest['observed'], 'staged source/generator/replay/resolution changed')
            if mode == 'freeze':
                require(not output('manifest.json').exists(), 'refusing manifest replacement')
                inputs = [FIXTURE, PACKAGE, Path(str(MAIN) + 'metadata.json'),
                          ORCH / 'design/handoff-vw-m3-main-image-cap-render-proof-preflight.json']
                inputs += [Path(str(MAIN) + f'frame-{frame}.png') for frame in FRAMES]
                save('manifest.json', {'revision': REV, 'tree': TREE, 'observed': observed, 'graph': before,
                    'scripts': {n: file_sha(output(n)) for n in ('controller.py', 'render.mjs', 'resolve.mjs', 'replay.py')},
                    'inputs': {str(p): file_sha(p) for p in inputs},
                    'expected_metadata_not_measured': {'width': 1920, 'height': 1080, 'fps': 30, 'durationInFrames': 120},
                    'frames': FRAMES, 'expected_opacity105_not_measured': 0.5,
                    'approved_known_intended_pixel_differences': [], 'certified': False})
            for path in (stage / 'replayed').iterdir():
                if mode != 'capture':
                    shutil.copyfile(path, output(path.name))
            if service:
                grant()
                graph_check()
                env_service = os.environ.get('CURRENT_CAP_SERVICE_RESULT')
                os.environ['CURRENT_CAP_SERVICE_RESULT'] = str(service)
                try:
                    run([NODE, output('render.mjs'), stage], stage, root, 'capture.log')
                finally:
                    if env_service is None:
                        os.environ.pop('CURRENT_CAP_SERVICE_RESULT', None)
                    else:
                        os.environ['CURRENT_CAP_SERVICE_RESULT'] = env_service
                compare()
            verify(root, members, package)
            verify_outputs(stage, root, observed)
        except BaseException as exc:
            error = str(exc)
            raise
        finally:
            try:
                post_errors = []
                after = None
                try:
                    verify(stage / 'agent', members, package)
                    require(observed is not None, 'staging did not finish')
                    verify_outputs(stage, stage / 'agent', observed)
                except Exception as exc:
                    post_errors.append(str(exc))
                try:
                    after = graph_check()
                    require(before == after, 'graph/tool changed during run')
                    resources()
                except Exception as exc:
                    post_errors.append(str(exc))
                save('postflight.json' if service else 'offline-postflight.json',
                     {'valid': error is None and not post_errors, 'error': error, 'post_errors': post_errors,
                      'before': before, 'after': after, 'source_outputs_unchanged': not post_errors,
                      'capture_run': service is not None, 'temp_removed_on_exit': str(stage)})
                require(not post_errors, f'postflight failed: {post_errors}')
            finally:
                real(stage)
                shutil.rmtree(stage)
    save('preflight.json', {'status': 'OFFLINE_PASS_NOT_CAPTURE_GRANTED' if not service else 'CAPTURE_COMPLETED',
        'revision': REV, 'tree': TREE, 'free_bytes_before_staging': free, 'reserve_bytes': FLOOR,
        'staging_headroom_bytes': remaining, 'required_bytes': FLOOR + remaining,
        'source_members': len(members), 'source_bytes': sum(map(len, members.values())),
        'public12_members': len(package), 'graph': before, 'capture_run': service is not None,
        'scope': 'UNCERTIFIED static compiled currentRoot reference; no Runtime/MP4/Player/export/audio/Gate6 claim'})
    print(json.dumps({'mode': mode, 'status': 'PASS', 'capture_run': service is not None}))


if __name__ == '__main__':
    main()
