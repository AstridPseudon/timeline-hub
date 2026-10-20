"""The official parent-track command through the real CLI parser and outbox."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from astrid.sdk.timeline._command_state import State
from astrid.sdk.timeline._track_commands import capture_track_set
from tests.packs.timeline import test_cli_commit_move

command = test_cli_commit_move.command
sync_connection = test_cli_commit_move.sync_connection


@pytest.mark.parametrize('args,value', [(('--set', '画面 🎬'), '画面 🎬'), (('--set', ''), ''),
                                       (('--clear',), None)])
def test_track_label_dispatch_matches_native_capture(command, capsys, args, value):
    run, generated = command
    original = copy.deepcopy(generated.bundles['r0'])
    assert run('edit', 'track-label', 't', '--track', 'parent/track:picture', *args, '--json') == 0
    expected = capture_track_set(original, 'parent/track:picture',
                                 values={} if value is None else {'label': value},
                                 clear=['label'] if value is None else [])
    body = json.loads(generated.calls[0][0])
    assert body['commands'] == [expected] and body['source'] == {'via': 'cli'}
    result = json.loads(capsys.readouterr().out)
    assert result['receipt']['receipt_id'] == result['data']['accepted_publication_id'] == 'pub1'
    track = State(generated.bundles['r1']).entity('parent/track:picture')
    assert ('label' not in track) if value is None else track['label'] == value


def test_cli_matches_full_app_portable_golden(command, capsys):
    run, generated = command
    fixture = json.loads((Path(__file__).parents[2] / 'editing_conformance/fixtures/'
                         'recipe_m2_app_track_label.json').read_text())
    generated.bundles['r0'] = copy.deepcopy(fixture['bundle'])
    assert run('edit', 'track-label', 't', '--project', 'p', '--track', fixture['input']['target_ref'],
               '--set', fixture['input']['label'], '--json') == 0
    assert json.loads(generated.calls[0][0])['commands'] == [fixture['command']]
    assert generated.bundles['r1'] == fixture['after_bundle']
    capsys.readouterr()


def test_cli_native_preview_and_lost_ack_retry(command, capsys):
    run, generated = command
    args = ('edit', 'track-label', 't', '--track', 'parent/track:picture', '--set', 'Picture')
    assert run(*args, '--dry-run') == 0
    assert capsys.readouterr().out.strip() == 'preview only; no publication accepted'
    assert not generated.accepted
    generated.lose_ack = True
    assert run(*args, '--json') == 1
    assert not json.loads(capsys.readouterr().out)['ok']
    assert run(*args, '--json') == 0
    assert generated.calls[-1] == generated.calls[-2]
    assert json.loads(capsys.readouterr().out)['data']['accepted_publication_id'] == 'pub1'


@pytest.mark.parametrize('args', [(), ('--set', 'A', '--clear'), ('--set', 'A', '--remove'),
                                ('--set', 'A', '--set-values', 'opaque=x')])
def test_cli_requires_explicit_set_or_clear_and_refuses_legacy_flags(command, args):
    run, generated = command
    with pytest.raises(SystemExit) as error:
        run('edit', 'track-label', 't', '--track', 'parent/track:picture', *args)
    assert error.value.code == 2 and generated.calls == []


def test_cli_native_track_selector_is_parent_scoped(command, capsys):
    run, generated = command
    assert run('edit', 'track-label', 't', '--track', 'picture', '--set', 'A', '--json') == 1
    assert not json.loads(capsys.readouterr().out)['ok']
    assert generated.calls == []


def test_help_exposes_native_entry_and_explicit_legacy_working_copy(command, capsys):
    run, _ = command
    for args in [('edit', '--help'), ('edit', 'track-label', '--help')]:
        with pytest.raises(SystemExit) as error:
            run(*args)
        assert error.value.code == 0
    output = capsys.readouterr().out
    assert 'legacy' in output and 'track-label' in output
    assert '--set STRING' in output and '--clear' in output
