"""Independent offline probes: no capture, service, source extraction, or renderer."""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
from types import SimpleNamespace
from unittest.mock import patch

ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
OWN = ORCH / 'workers/vw-m3-main-cap-repair-final-gate'
PREFIX = ORCH / 'design/handoff-vw-m3-main-cap-repair-final-gate-'
TARGET_PREFIX = ORCH / 'design/handoff-vw-m3-main-cap-controller-repair-'
TARGET = Path(str(TARGET_PREFIX) + 'controller.py')
RENDER = Path(str(TARGET_PREFIX) + 'render.mjs')


def load(path):
    spec = importlib.util.spec_from_file_location('reviewed_controller', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def refused(function, fragment):
    try:
        function()
    except (RuntimeError, FileNotFoundError) as exc:
        assert fragment in str(exc), str(exc)
    else:
        raise AssertionError('accepted: ' + fragment)


if sys.argv[1] == 'final-checks':
    new = json.loads(Path(str(PREFIX) + 'reviewed-sha256.json').read_text())
    old = json.loads((ORCH / 'design/handoff-vw-m3-main-cap-controller-final-gate-reviewed-sha256.json').read_text())
    for name, digest in new.items():
        assert hashlib.sha256(Path(str(TARGET_PREFIX) + name).read_bytes()).hexdigest() == digest
    for name, digest in old.items():
        assert hashlib.sha256((ORCH / 'design' / name).read_bytes()).hexdigest() == digest
    worker = ORCH / 'workers/vw-m3-main-cap-controller-repair'
    assert all(not (worker / name).exists() for name in ('CAPTURE-GRANT.txt', 'capture-stage', 'CAPTURE-STARTED'))
    assert all(not Path(str(TARGET_PREFIX) + f'frame-{frame}.png').exists() for frame in (90, 105, 119))
    assert not list(OWN.glob('offline-calibration-*'))
    print('PASS: repaired frozen hashes stable; old rejected artifacts/instrument unchanged; actual grant/stage/attempt/PNGs absent; private temporary fixtures cleaned')
    raise SystemExit(0)


if sys.argv[1] == 'preflight':
    m = load(TARGET)
    assert m.REPO == Path('/home/user/work/agent')
    # Redirect only output and the disk-query directory, never the source repo.
    m.OWN = OWN
    m.PREFIX = PREFIX
    result = m.preflight()
    print(json.dumps({key: result[key] for key in (
        'status', 'blockers', 'free_bytes', 'required_before_extraction_bytes')}, indent=2))
    raise SystemExit(1 if result['blockers'] else 0)

if sys.argv[1] == 'postflight':
    m = load(TARGET)
    m.OWN = OWN
    m.PREFIX = PREFIX
    before = json.loads(Path(str(PREFIX) + 'preflight.json').read_text())
    source = m.source_check()
    graph, inventory = m.graph_check()
    assert source == before['source']
    assert graph == before['graph_before'] == before['graph_after']
    assert inventory == json.loads(Path(str(PREFIX) + 'graph-pre.json').read_text())
    m.evidence('graph-post.json', inventory)
    m.evidence('offline-postflight.json', {'source_unchanged': True,
        'full_graph_and_six_peers_unchanged': True, 'graph': graph,
        'free_bytes': m.shutil.disk_usage(OWN).free,
        'capture_grant_present': m.GRANT.exists(), 'capture_executed': False})
    print('PASS: pinned MAIN source/fixture and full graph/six peers unchanged after all independent offline probes')
    raise SystemExit(0)

assert sys.argv[1] == 'calibrations'
m = load(TARGET)
assert m.REPO == Path('/home/user/work/agent')
for remaining in (0, m.HEADROOM + m.PNG_RAW):
    with patch.object(m.shutil, 'disk_usage', return_value=SimpleNamespace(free=m.FLOOR + remaining - 1)), patch.object(m, 'quiet', return_value=False):
        refused(lambda: m.disk(remaining), 'disk BLOCKED')
    with patch.object(m.shutil, 'disk_usage', return_value=SimpleNamespace(free=m.FLOOR + remaining)), patch.object(m, 'quiet', return_value=False):
        assert m.disk(remaining) == m.FLOOR + remaining
with patch.object(m.shutil, 'disk_usage', return_value=SimpleNamespace(free=100 * m.FLOOR)), patch.object(m, 'quiet', return_value=True):
    refused(lambda: m.disk(0), 'QUIET')
print('PASS: four floor/headroom boundary cases and QUIET')

# This is a tiny private synthetic mirror, never a manager/service grant.
with tempfile.TemporaryDirectory(prefix='offline-calibration-', dir=OWN) as folder:
    private = Path(folder)
    controller = private / 'controller.py'
    renderer = private / 'render.mjs'
    controller.write_bytes(TARGET.read_bytes())
    renderer.write_bytes(RENDER.read_bytes())
    m = load(controller)
    m.OWN = private
    # PREFIX is a filename prefix, so use an explicit trailing slash string.
    m.PREFIX = str(private) + '/'
    m.GRANT = private / 'SYNTHETIC-GRANT.txt'
    expected = '\n'.join([m.suite_line(),
                          'controller_sha256=' + m.file_sha(controller),
                          'render_sha256=' + m.file_sha(renderer)]) + '\n'
    m.GRANT.write_text(expected)
    m.script_grant()
    for path in (controller, renderer):
        original = path.read_bytes()
        path.write_bytes(original + b'\n# synthetic byte tamper\n')
        refused(m.script_grant, 'controller/render SHA256')
        with patch.object(sys, 'argv', [str(controller), 'capture']), patch.object(m, 'preflight', side_effect=AssertionError('preflight before grant')), patch.object(m.subprocess, 'Popen', side_effect=AssertionError('spawned')):
            refused(m.main, 'controller/render SHA256')
            refused(lambda: m.run_process(['NEVER-EXECUTE'], private, {}, private / 'NO-LOG'), 'controller/render SHA256')
        assert not (private / 'capture-stage').exists()
        assert not (private / 'capture.lock').exists()
        assert not (private / 'CAPTURE-STARTED').exists()
        assert not (private / 'NO-LOG').exists()
        path.write_bytes(original)
    m.GRANT.write_text(m.suite_line() + '\n')
    refused(m.script_grant, 'controller/render SHA256')
    m.GRANT.unlink()
    refused(m.script_grant, 'exact grant missing')
    print('PASS: exact both-hash positive; real controller-byte and renderer-byte tamper negatives; path-only and absent grants refused')

    # With no grant, real main must stop before any preflight/stage/process.
    with patch.object(sys, 'argv', [str(controller), 'capture']), patch.object(m, 'preflight', side_effect=AssertionError('preflight before grant')), patch.object(m.subprocess, 'Popen', side_effect=AssertionError('spawned')):
        refused(m.main, 'exact grant missing')
    assert not (private / 'capture-stage').exists()
    assert not (private / 'capture.lock').exists()
    assert not (private / 'CAPTURE-STARTED').exists()
    print('PASS: ungranted real main stops before lock/marker/stage/preflight/process')

    uncreated = private / 'NO-SOURCE-EXTRACTION'
    with patch.object(m, 'disk', side_effect=RuntimeError('disk BLOCKED: synthetic')), patch.object(m.subprocess, 'Popen', side_effect=AssertionError('spawned')):
        refused(lambda: m.source_stage(uncreated, {'unpacked_bytes': 100}), 'disk BLOCKED')
    assert not uncreated.exists()
    print('PASS: real source_stage resource guard stops before archive read/allocation/process')

    m.GRANT.write_text(expected)
    result = {'status': 'OFFLINE_MOCK_ONLY', 'blockers': [],
              'free_bytes': 100 * m.FLOOR, 'required_before_extraction_bytes': 0,
              'source': {'unpacked_bytes': 0}}
    stage = private / 'capture-stage'
    actual_rmtree = shutil.rmtree

    def lifecycle(kind):
        sentinel_parent = private / 'sentinel-parent'
        sentinel_parent.mkdir(exist_ok=True)
        sentinel = sentinel_parent / 'must-survive.txt'
        sentinel.write_text('pre-existing private sentinel\n')
        if kind == 'refusal-directory':
            stage.mkdir()
            (stage / 'sentinel.txt').write_text('pre-existing stage\n')
        elif kind == 'refusal-file':
            stage.write_text('pre-existing stage file\n')
        elif kind == 'refusal-symlink':
            stage.symlink_to(sentinel_parent, target_is_directory=True)

        def partial_stage(*args):
            assert args[0] == stage
            assert stage.is_dir() and not stage.is_symlink()
            (stage / 'main').mkdir()
            (stage / 'main/partial.bin').write_bytes(b'partial synthetic staging')
            raise RuntimeError('synthetic partial staging failure')

        with contextlib.ExitStack() as stack:
            stack.enter_context(patch.object(sys, 'argv', [str(controller), 'capture']))
            stack.enter_context(patch.object(m, 'central_grant', return_value='OFFLINE-NO-SERVICE'))
            stack.enter_context(patch.object(m, 'preflight', return_value=result))
            stack.enter_context(patch.object(m, 'graph_check', return_value=({}, {})))
            stack.enter_context(patch.object(m, 'source_check', return_value=result['source']))
            stack.enter_context(patch.object(m, 'verify_stage'))
            stack.enter_context(patch.object(m, 'inventory', return_value={}))
            stack.enter_context(patch.object(m, 'disk'))
            stack.enter_context(patch.object(m, 'source_stage', side_effect=partial_stage))
            stack.enter_context(patch.object(m.subprocess, 'Popen', side_effect=AssertionError('spawned')))
            remove = stack.enter_context(patch.object(m.shutil, 'rmtree', wraps=actual_rmtree))
            if kind == 'postflight-failure':
                stack.enter_context(patch.object(m, 'evidence', side_effect=RuntimeError('synthetic postflight write failure')))
            else:
                stack.enter_context(patch.object(m, 'evidence'))
            if kind == 'late-tamper':
                stack.enter_context(patch.object(m, 'script_grant', side_effect=RuntimeError('late hash mismatch')))
            with contextlib.redirect_stdout(io.StringIO()):
                try:
                    m.main()
                except RuntimeError as exc:
                    reason = str(exc)
                else:
                    raise AssertionError('synthetic failure accepted')
            if kind.startswith('refusal') or kind == 'late-tamper':
                remove.assert_not_called()
            else:
                remove.assert_called_once_with(stage)
                assert not stage.exists()
            if kind.startswith('refusal'):
                assert 'stage was not allocated by this attempt' in reason
                if kind == 'refusal-directory':
                    assert (stage / 'sentinel.txt').read_text() == 'pre-existing stage\n'
                elif kind == 'refusal-file':
                    assert stage.read_text() == 'pre-existing stage file\n'
                else:
                    assert stage.is_symlink()
            assert sentinel.read_text() == 'pre-existing private sentinel\n'
            if kind == 'partial-staging':
                with contextlib.redirect_stdout(io.StringIO()):
                    try:
                        m.main()
                    except FileExistsError:
                        pass
                    else:
                        raise AssertionError('automatic retry accepted')
                assert not stage.exists()
                print('PASS: exclusive attempt marker prevents automatic retry')
        if stage.is_symlink():
            stage.unlink()
        elif stage.is_file():
            stage.unlink()
        elif stage.exists():
            actual_rmtree(stage)
        for name in ('capture.lock', 'CAPTURE-STARTED'):
            (private / name).unlink(missing_ok=True)
        print('PASS: ' + kind + '; only attempt-allocated stage eligible for deletion; sentinel preserved')

    for kind in ('refusal-directory', 'refusal-file', 'refusal-symlink', 'partial-staging', 'postflight-failure', 'late-tamper'):
        lifecycle(kind)

    # Full-size synthetic solids exercise the actual RGB analyzer, never MAIN pixels.
    from PIL import Image

    colors = {90: (240, 240, 240, 255), 105: (122, 124, 130, 255), 119: (13, 16, 27, 255)}
    for frame, color in colors.items():
        Image.new('RGBA', (1920, 1080), color).save(private / f'frame-{frame}.png')
    measured = m.measure()
    estimates = measured['opacity_inferred_from_rgb']
    assert estimates[90]['median'] == 1
    assert abs(estimates[105]['median'] - 0.5) <= 1 / 220
    assert abs(estimates[119]['median'] - 1 / 30) <= 1 / 220
    assert all(sample[3] == 255 for entry in measured['files'].values() for sample in entry['sample_rgba'])
    assert measured['visual_golden_selected'] is False
    Image.new('RGBA', (1920, 1080), (0, 0, 0, 255)).save(private / 'frame-90.png')
    refused(m.measure, 'full-opacity pixel control failed')
    Image.new('RGBA', (16, 16), (240, 240, 240, 255)).save(private / 'frame-90.png')
    refused(m.measure, 'wrong PNG dimensions')
    print('PASS: actual analyzer on synthetic full-size RGB solids; alpha255 does not imply layer opacity; control/dimension negatives')

print('All lifecycle/preflight/graph/service/process substitutions above are synthetic; no capture or source archive extracted')
