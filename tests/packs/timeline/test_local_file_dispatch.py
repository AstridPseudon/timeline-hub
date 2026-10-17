"""Public file routes must stay offline; managed routes must still acquire."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from types import SimpleNamespace

import pytest

from astrid.core.cli.domain_product import local_file_command
from astrid.core.gateway.dispatch import _dispatch_product
from astrid.packs.timeline import cli
from astrid.sdk.timeline import journal, store
from astrid.sdk.timeline.checkout import Checkout
from tests.packs.timeline.test_cli_edit_flags import bundle


@pytest.fixture
def public_cli(tmp_path):
    source = Path(__file__).resolve().parents[3]
    hooks = tmp_path / 'hooks'
    hooks.mkdir()
    (hooks / 'sitecustomize.py').write_text('''import os
from pathlib import Path
from astrid.sdk.client import AstridClient
log = Path(os.environ['ASTRID_ACQUISITION_SENTINEL'])
def record(event):
    with log.open('a') as stream:
        stream.write(str(os.getpid()) + ' ' + event + '\\n')
record('installed')
def forbidden(*args, **kwargs):
    record('ACQUISITION_FORBIDDEN')
    os._exit(86)
for name in ('open', 'open_from_launcher', 'open_existing_from_launcher'):
    setattr(AstridClient, name, forbidden)
''')
    sequence = 0

    def run(*args):
        nonlocal sequence
        sequence += 1
        stem = tmp_path / f'process-{sequence:02d}'
        sentinel = stem.with_suffix('.sentinel')
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1',
                   PYTHONPATH=os.pathsep.join((str(hooks), str(source))),
                   BANODOCO_LOCAL_DATA_ROOT=str(tmp_path / 'unconfigured-data'),
                   ASTRID_ACQUISITION_SENTINEL=str(sentinel))
        argv = [sys.executable, '-B', '-m', 'astrid', 'timelines', *map(str, args)]
        started = time.time()
        process = subprocess.Popen(argv, cwd=source, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(timeout=60)
        duration = time.time() - started
        stem.with_suffix('.stdout').write_bytes(stdout)
        stem.with_suffix('.stderr').write_bytes(stderr)
        events = sentinel.read_text()
        stem.with_suffix('.json').write_text(json.dumps(dict(
            argv=argv, cwd=str(source), pid=process.pid, started_epoch=started,
            duration_seconds=duration, exit=process.returncode,
            stdout_sha256=hashlib.sha256(stdout).hexdigest(),
            stderr_sha256=hashlib.sha256(stderr).hexdigest(), sentinel=events,
        ), indent=2))
        assert f'{process.pid} installed\n' in events
        return process.returncode, stdout.decode(), stderr.decode(), events

    return run


@pytest.fixture
def local(tmp_path):
    path = tmp_path / 'checkout.json'
    Checkout(bundle()).save(path, quiet=True)
    return path


def saved_calls(path):
    records = journal.read(path.with_suffix('.json.journal.jsonl'))
    changed = [row for row in records if row.kind == 'save' and row.outcome == 'changed']
    return changed[-1].calls


@pytest.mark.parametrize(('old', 'canonical', 'kind'), [
    ('--duration', '--for', 'duration'),
    ('--line', '--replace-line', 'replace'),
    ('--line-text', '--text', 'text'),
    ('--gap', '--insert-gap-after', 'insert'),
    ('--script-gaps', '--gaps', 'script'),
])
def test_public_edit_aliases_offline(public_cli, tmp_path, old, canonical, kind):
    words = tmp_path / 'words.json'
    words.write_text(json.dumps([[0.1, 0.3, 'it'], [0.4, 0.6, 'rose'], [0.8, 1.2, 'fast']]))
    takes = tmp_path / 'takes'
    takes.mkdir()
    script = tmp_path / 'script.json'
    script.write_text(json.dumps({'segments': [{'id': 's1', 'text': 'it went viral', 'gap_after_s': 0.5},
                                                {'id': 's2', 'text': 'Live now'}]}))
    results = []
    for spelling, name in ((old, 'old'), (canonical, 'canonical')):
        folder = tmp_path / name
        folder.mkdir()
        path = folder / 'checkout.json'
        Checkout(bundle()).save(path, quiet=True)
        args = {
            'duration': ['--clip', 'R', spelling, '0.5'],
            'replace': [spelling, 's1', '--take', 'P', '--words', words, '--text', 'it rose fast'],
            'text': ['--replace-line', 's1', '--take', 'P', '--words', words, spelling, 'it rose fast'],
            'insert': ['--insert-line', 's3', '--after', 's1', '--take', 'P', '--words', words, spelling, '0.25'],
            'script': ['--from-script', script, '--takes', takes, spelling],
        }[kind]
        code, out, err, events = public_cli('edit', '--file', path, *args)
        assert (code, err) == (0, ''), (out, err)
        assert 'ACQUISITION_FORBIDDEN' not in events
        assert len(list(store._history_dir(path).glob('*.json'))) == 1
        assert saved_calls(path)
        saved = Checkout.load(path)
        if kind == 'duration':
            assert saved.clip('R').duration == pytest.approx(0.5)
        elif kind in ('replace', 'text'):
            assert saved.voice('s1').text == 'it rose fast'
            assert [word.text for word in saved.voice('s1').words] == ['it', 'rose', 'fast']
            assert saved.voice('s1').clips[0].asset == 'P'
        elif kind == 'insert':
            assert [voice.segment for voice in saved.lines()] == ['s1', 's3', 's2']
            assert saved.voice('s3').gap_after == pytest.approx(0.25)
        else:
            assert saved.voice('s1').gap_after == pytest.approx(0.5)
        results.append((path.read_bytes(), saved.document(), out.replace(str(path), '<file>'), saved_calls(path)))
    assert results[0] == results[1]


def test_public_lines_reads_text_gap_script_share_history(public_cli, local, tmp_path):
    original = Checkout.load(local)
    original_words = [(w.id, w.start, w.end, w.text) for w in original.words()]
    for args in ([], ['--line', 's1']):
        before = local.read_bytes()
        code, out, err, events = public_cli('lines', '--file', local, *args)
        assert (code, err) == (0, '')
        assert 'it went viral' in out and 'take P' in out
        assert local.read_bytes() == before
        assert 'ACQUISITION_FORBIDDEN' not in events
    assert not store._history_dir(local).exists()
    code, out, err, events = public_cli('lines', '--file', local, '--line', 's1', '--text', 'A revised line.')
    assert (code, err) == (0, '')
    assert out == ('line s1: script text updated (narration re-pins on publish)\n'
                   f'edited working copy\nnext: timelines lines --file {local}\n')
    saved = Checkout.load(local)
    assert saved.voice('s1').text == 'A revised line.'
    assert [(w.id, w.start, w.end, w.text) for w in saved.words()] == original_words
    assert saved.voice('s1').clips[0].asset == 'P'
    assert [call['op'] for call in saved_calls(local)] == ['voice.set-text']
    code, out, err, events = public_cli('lines', '--file', local, '--gap-after', 's1=0.5')
    assert (code, err) == (0, '')
    assert out == f'edited working copy\nnext: timelines lines --file {local}\n'
    assert Checkout.load(local).voice('s1').gap_after == pytest.approx(0.5)
    assert 'voice.set-gap-after' in [call['op'] for call in saved_calls(local)]
    script = tmp_path / 'lines-script.json'
    script.write_text(json.dumps({'segments': [{'id': 's1', 'text': 'Final first line.'},
                                               {'id': 's2', 'text': 'Final second line.'}]}))
    before_script = Checkout.load(local)
    code, out, err, events = public_cli('lines', '--file', local, '--from-script', script)
    assert (code, err) == (0, '')
    saved = Checkout.load(local)
    assert [v.text for v in saved.lines()] == ['Final first line.', 'Final second line.']
    assert [(w.id, w.start, w.end, w.text) for w in saved.words()] == [(w.id, w.start, w.end, w.text) for w in before_script.words()]
    assert [call['op'] for call in saved_calls(local)] == ['timeline.apply-script']
    assert len(list(store._history_dir(local).glob('*.json'))) == 3
    final = saved.document()
    saved.undo()
    assert saved.document() == before_script.document()
    saved.redo()
    assert saved.document() == final
    rows = journal.read(local.with_suffix('.json.journal.jsonl'))
    assert [row.kind for row in rows][-2:] == ['undo', 'redo']
    assert not (tmp_path / 'unconfigured-data' / 'runtime').exists()


@pytest.mark.parametrize('args', [
    ['--published'], ['--draft', 'working'], ['named-timeline'],
    ['--text', 'missing line'], ['--takes', 'takes'], ['--gaps'],
    ['--line', 's1', '--from-script', 'missing.json'], ['--verify'],
])
def test_public_lines_invalid_file_combinations_do_not_mutate(public_cli, local, args):
    before = local.read_bytes()
    code, out, err, events = public_cli('lines', '--file', local, *args)
    assert code == 2, (out, err)
    assert err
    assert local.read_bytes() == before
    assert not store._history_dir(local).exists()
    assert 'ACQUISITION_FORBIDDEN' not in events


@pytest.mark.parametrize('args', [
    ['edit', '--file', 'unused.json', '--from-script', 'managed.json'],
    ['edit', '--file', 'unused.json', '--clip', 'x', '--verify', '--nudge', '1'],
    ['edit', '--file', 'unused.json', '--clip', 'x', '--shape-from', 'other@rev', '--fit-sequence'],
    ['edit', '--file', 'unused.json', '--clip', 'x', '--swap-asset', 'run:managed/media#0'],
    ['edit', '--file', 'unused.json', '--clip', 'x', '--trim-in', '0.2'],
    ['edit', '--file', 'unused.json', '--command', '{"op":"timeline.narration-reflow","args":{}}'],
    ['publish', '--file', 'unused.json', '--idempotency-key', 'task-only'],
    ['lines', 'task-timeline', '--project', 'task-project', '--published'],
])
def test_public_managed_routes_still_enter_acquisition(public_cli, args):
    code, out, err, events = public_cli(*args)
    assert code == 86, (out, err)
    assert 'ACQUISITION_FORBIDDEN' in events


def test_no_file_current_project_is_resolved_after_acquisition(monkeypatch, capsys):
    from contextlib import contextmanager
    from astrid.sdk.client import AstridClient
    order = []
    def current():
        order.append('current')
        return SimpleNamespace(ok=True, data={'project': {'project_id': 'task-project'}})
    client = SimpleNamespace(projects=SimpleNamespace(current=current))
    @contextmanager
    def opened(**kwargs):
        order.append('acquired')
        yield client
    monkeypatch.setattr(AstridClient, 'open_from_launcher', opened)
    monkeypatch.setattr(cli, '_cmd_status', lambda parsed: order.append((parsed.project, parsed.client)) or 0)
    assert _dispatch_product(['timelines', 'status', 'task-timeline']) == 0
    assert order == ['acquired', 'current', ('task-project', client)]
    assert local_file_command('timelines', ['status', 'task-timeline']) is None


def test_script_with_local_wav_retains_authenticated_import(local, tmp_path):
    script = tmp_path / 'script.json'
    script.write_text(json.dumps({'segments': [{'id': 's1', 'text': 'it went viral'}]}))
    takes = tmp_path / 'takes'
    takes.mkdir()
    (takes / 's1.wav').write_bytes(b'task-owned-import-candidate')
    assert local_file_command('timelines', ['lines', '--file', str(local), '--from-script', str(script), '--takes', str(takes)]) is None
    assert local_file_command('timelines', ['edit', '--file', str(local), '--from-script', str(script), '--takes', str(takes)]) is None


def test_public_local_dry_run_and_atomic_text_gap_refusal(public_cli, local):
    before = local.read_bytes()
    code, out, err, events = public_cli('edit', f'--file={local}', '--clip', 'R', '--for', '0.5', '--dry-run')
    assert (code, err) == (0, '')
    assert json.loads(out)['changed'] is True
    assert local.read_bytes() == before
    assert not store._history_dir(local).exists()
    code, out, err, events = public_cli('lines', '--file', local, '--line', 's1', '--text', 'Do not persist', '--gap-after', 'bad')
    assert code == 2 and 'SEG=SECONDS' in err
    assert local.read_bytes() == before
    assert not store._history_dir(local).exists()


def test_public_lines_rejects_managed_script_before_mutation(public_cli, local, tmp_path):
    script = tmp_path / 'managed.json'
    script.write_text(json.dumps({'version': 1, 'lines': [], 'remove': []}))
    before = local.read_bytes()
    code, out, err, events = public_cli('lines', '--file', local, '--from-script', script)
    assert code == 2 and 'does not prepare or verify managed takes' in err
    assert 'ACQUISITION_FORBIDDEN' not in events
    assert local.read_bytes() == before
    assert not store._history_dir(local).exists()
