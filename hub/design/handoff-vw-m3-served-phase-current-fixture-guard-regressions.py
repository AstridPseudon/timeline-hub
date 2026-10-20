"""Pure red-before/green-after regressions for the served-PCM guards.

These tests deliberately do not import the producer, start HTTP, or run pytest
through the controller.  They exercise only the controller/fixture guard
functions and a temporary local Git repository.
"""

import importlib.util
import subprocess
import urllib.parse
from pathlib import Path

import pytest

ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
DESIGN = ORCH / 'design'


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


controller = _load(
    'served_pcm_guard_controller',
    DESIGN / 'handoff-vw-m3-served-phase-current-fixture-controller.py',
)
fixture = _load(
    'served_pcm_guard_fixture',
    DESIGN / 'handoff-vw-m3-served-phase-current-fixture-test_normal_audio_served_sources.py',
)


def _git(root, *args):
    return subprocess.run(
        ['git', '-C', str(root), *args], check=True, text=True, capture_output=True,
    )


def _committed_repo(root):
    _git(root, 'init', '-q')
    _git(root, 'config', 'user.email', 'guard-regression@example.invalid')
    _git(root, 'config', 'user.name', 'served-pcm-guard-regression')
    (root / 'tracked.txt').write_text('baseline\n')
    _git(root, 'add', 'tracked.txt')
    _git(root, '-c', 'commit.gpgsign=false', 'commit', '-qm', 'baseline')


def test_redbefore_greenafter_untracked_source_drift(tmp_path):
    root = tmp_path / 'source'
    root.mkdir()
    _committed_repo(root)
    (root / 'untracked-import.py').write_text('changed import\n')

    # RED before: the predecessor's tracked-only check accepts the untracked file.
    assert controller.output('git', 'diff', '--name-only', 'HEAD', cwd=root) == ''
    # GREEN after: the central source guard includes every untracked path.
    with pytest.raises(AssertionError, match='tracked or untracked'):
        controller.assert_clean_source(root)


def test_redbefore_greenafter_finally_revalidation(monkeypatch, capsys):
    class Result:
        returncode = 0

    def fake_run(*args, **kwargs):
        return Result()

    def drifted_preflight(*args, **kwargs):
        raise AssertionError('source has tracked or untracked edits')

    monkeypatch.setattr(controller.subprocess, 'run', fake_run)
    monkeypatch.setattr(controller, 'preflight', drifted_preflight)

    # RED before: a runner that returns pytest's success without a finally check.
    assert fake_run(['pytest']).returncode == 0
    # GREEN after: drift found by finally makes an otherwise-successful run fail.
    assert controller.run_test(
        ['pytest'], {}, Path('.'), 'a' * 40, Path('.'), Path('/bin/node'),
    ) == 1
    assert 'POSTFLIGHT FAILED: source has tracked or untracked edits' in capsys.readouterr().err


def test_redbefore_greenafter_wrongport():
    url = 'http://127.0.0.1:43123/managed.wav'

    # RED before: the predecessor checked loopback but accepted any port.
    parsed = urllib.parse.urlsplit(url)
    assert parsed.scheme == 'http' and parsed.hostname == '127.0.0.1'
    # GREEN after: only this invocation server's live port is accepted.
    with pytest.raises(AssertionError):
        fixture._validate_invocation_url(url, expected_port=43124)
    assert fixture._validate_invocation_url(url, expected_port=43123).port == 43123


def test_redbefore_greenafter_preserves_pytest_failure_code(monkeypatch, capsys):
    class Result:
        returncode = 7

    monkeypatch.setattr(controller.subprocess, 'run', lambda *args, **kwargs: Result())
    def drifted_preflight(*args, **kwargs):
        raise AssertionError('source has tracked or untracked edits')

    monkeypatch.setattr(controller, 'preflight', drifted_preflight)

    assert controller.run_test(
        ['pytest'], {}, Path('.'), 'a' * 40, Path('.'), Path('/bin/node'),
    ) == 7
    assert 'preserving pytest return code: 7' in capsys.readouterr().err
