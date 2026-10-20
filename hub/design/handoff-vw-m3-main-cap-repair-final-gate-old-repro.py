"""Offline independent gate; never starts capture, sockets, or a child renderer."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
from unittest.mock import patch

ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
OWN = ORCH / 'workers/vw-m3-main-cap-repair-final-gate'
PREFIX = ORCH / 'design/handoff-vw-m3-main-cap-repair-final-gate-'
TARGET = ORCH / 'design/handoff-vw-m3-main-cap-capture-controller-controller.py'
spec = importlib.util.spec_from_file_location('audited_controller', TARGET)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

if sys.argv[1] in ('preflight', 'preflight-diagnostic-repo'):
    # Redirect ONLY evidence output and disk-query location to our assigned paths.
    # Every source, fixture, original git object, and peer graph remains the target's.
    m.PREFIX = PREFIX
    m.OWN = OWN
    if sys.argv[1] == 'preflight-diagnostic-repo':
        # Diagnostic only: the frozen target still points at a recycled worktree.
        # Use our read-only git object store to finish the independent inventory.
        m.REPO = Path('/home/user/work/wt/vw-m3-main-cap-controller-final-gate')
    result = m.preflight()
    print(json.dumps({key: result[key] for key in (
        'status', 'blockers', 'free_bytes', 'required_before_extraction_bytes')}, indent=2))
    raise SystemExit(1 if result['blockers'] else 0)

assert sys.argv[1] == 'self-check'
for remaining in (0, m.HEADROOM + m.PNG_RAW):
    with patch.object(m.shutil, 'disk_usage', return_value=SimpleNamespace(free=m.FLOOR + remaining - 1)), patch.object(m, 'quiet', return_value=False):
        try:
            m.disk(remaining)
        except RuntimeError as exc:
            assert 'disk BLOCKED' in str(exc)
        else:
            raise AssertionError('reserve/headroom bypass')
    with patch.object(m.shutil, 'disk_usage', return_value=SimpleNamespace(free=m.FLOOR + remaining)), patch.object(m, 'quiet', return_value=False):
        assert m.disk(remaining) == m.FLOOR + remaining
with patch.object(m.shutil, 'disk_usage', return_value=SimpleNamespace(free=100 * m.FLOOR)), patch.object(m, 'quiet', return_value=True):
    try:
        m.disk(0)
    except RuntimeError as exc:
        assert 'QUIET' in str(exc)
    else:
        raise AssertionError('QUIET bypass')
with patch.object(m, 'GRANT', OWN / 'NONEXISTENT-GRANT'):
    try:
        m.central_grant()
    except RuntimeError as exc:
        assert 'exact grant missing' in str(exc)
    else:
        raise AssertionError('absent grant accepted')
with patch.object(m, 'disk', side_effect=RuntimeError('disk BLOCKED: self-check')), patch.object(m.subprocess, 'Popen', side_effect=AssertionError('spawned')):
    try:
        m.source_stage(OWN / 'UNCREATED-STAGE', {'unpacked_bytes': 100})
    except RuntimeError as exc:
        assert 'disk BLOCKED' in str(exc)
    else:
        raise AssertionError('disk-blocked allocation allowed')
assert not (OWN / 'UNCREATED-STAGE').exists()
print('PASS: seven reserve/headroom/QUIET/absent-grant/no-allocation guards')

# Regression probe: all admission/preflight/graph/process functions are mocked.
# The real source_stage refuses a pre-existing directory; mock rmtree prevents
# the real finally block from deleting even this private synthetic sentinel.
with tempfile.TemporaryDirectory(prefix='cleanup-probe-', dir=OWN) as temporary:
    private = Path(temporary)
    stage = private / 'capture-stage'
    stage.mkdir()
    sentinel = stage / 'must-survive.txt'
    sentinel.write_text('pre-existing private test data\n')
    result = {'status': 'MOCK_ONLY', 'blockers': [], 'free_bytes': 100 * m.FLOOR,
              'required_before_extraction_bytes': 0, 'source': {'unpacked_bytes': 0}}
    with patch.object(m, 'OWN', private), patch.object(m, 'central_grant', return_value='MOCK-NO-SERVICE'), patch.object(m, 'preflight', return_value=result), patch.object(m, 'graph_check', return_value=({}, {})), patch.object(m, 'source_check', return_value=result['source']), patch.object(m, 'verify_stage'), patch.object(m, 'inventory', return_value={}), patch.object(m, 'evidence'), patch.object(m, 'disk'), patch.object(m.shutil, 'rmtree') as remove, patch.object(m.subprocess, 'Popen', side_effect=AssertionError('spawned')), patch.object(sys, 'argv', [str(TARGET), 'capture']):
        try:
            m.main()
        except RuntimeError as exc:
            assert str(exc) == 'stage already exists; refusing overwrite', str(exc)
        else:
            raise AssertionError('pre-existing stage was accepted')
        remove.assert_called_once_with(stage)
        assert sentinel.read_text() == 'pre-existing private test data\n'
        print('REPRODUCED: refused pre-existing stage still passed to shutil.rmtree in finally (deletion mocked; sentinel intact)')
print('No source extraction, renderer, browser, sockets, service request, or shared write occurred')
