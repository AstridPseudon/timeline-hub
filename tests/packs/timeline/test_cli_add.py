"""Current ADD dispatch, source/destination identity and atomic Runner proofs."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from astrid.packs.timeline import cli
from astrid.sdk import timeline_intent as intent
from astrid.sdk.timeline import commands
from astrid.sdk.timeline_checkout import Checkout
from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline_sheet import apply_sheet
from tests.sdk.test_timeline_reflow_golden import film


def checkout(tmp_path):
    tl = Checkout(film())
    tl.save(tmp_path / 'add.checkout.json', quiet=True)
    return tl


def invoke(tl, *args):
    parsed = cli.build_parser(None).parse_args(['edit', '--file', str(tl.path), *args])
    return parsed.handler(parsed)


def test_cli_default_and_explicit_placement_overrides_and_unique_ids(tmp_path):
    tl = checkout(tmp_path)
    source = copy.deepcopy(tl.clip('c1.rocket').data)
    assert invoke(tl, '--add', 'c2', '--like', 'c1.rocket', '--set', 'x=42') == 0
    tl = Checkout.load(tl.path)
    clone = tl.clip('c2.rocket')
    assert clone.cut_id == 'c2' and clone.start == tl.cut('c2').start
    assert intent.on(clone.data) == 'c2' and clone.get('x') == 42
    assert clone.asset == 'R' and clone.track == 'sprite'
    assert tl.clip('c1.rocket').data == source
    assert invoke(tl, '--add', 'c2', '--like', 'c1.rocket', '--on', 'c2 +0.5s') == 0
    reloaded = Checkout.load(tl.path)
    second = reloaded.clip('c2.rocket-2')
    assert second.id != clone.id and second.start == pytest.approx(clone.start + .5)
    records = reloaded.log(outcome='changed')
    assert len(records) >= 2 and records[-1].calls[0]['op'] == 'timeline.add'
    assert records[-1].calls[0]['args']['from'] == 'occurrence:occ-F/clip:c1-rocket'


@pytest.mark.parametrize('extra', [[], ['--clip', 'c1.rocket'], ['--instance-id', 'mixed'],
    ['--params', '{}'], ['--component-pack-root', '/nonexistent'], ['--add-media', 'M']])
def test_missing_like_and_mixed_forms_refuse_before_mutation(tmp_path, extra):
    tl = checkout(tmp_path)
    before = Path(tl.path).read_bytes()
    args = ['--add', 'c2'] + ([] if not extra else ['--like', 'c1.rocket']) + extra
    assert invoke(tl, *args) == 2
    assert Path(tl.path).read_bytes() == before


def test_python_preview_replay_sheet_and_single_undo(tmp_path):
    tl = checkout(tmp_path)
    before = copy.deepcopy(tl.document())
    source = tl.clip('c1.rocket')
    source.data['opaque'] = {'null': None, 'number': 1.0}
    tl = Checkout(copy.deepcopy(tl.bundle))
    tl.save(tmp_path / 'opaque.checkout.json', quiet=True)
    source = tl.clip('c1.rocket')
    before = copy.deepcopy(tl.document())
    call = commands.layer_copy_call(tl, 'c2', 'c1.rocket', set_values={'x': 72})
    preview = commands.run(tl, call, dry_run=True)
    assert tl.document() == before and len(preview.calls) == 1
    bound = preview.calls[0]
    assert bound.op == 'timeline.add' and bound.created == bound.resolved
    assert bound.args['destination'] == 'occurrence:occ-F/clip:c2-plate'
    assert bound.expect[bound.args['from'] + '::']['state'] == 'present'
    assert bound.bindings['c2'] == 'cut:c2:start'
    applied = commands.run(tl, bound)
    clone = commands.authored_owner(tl, bound.created[0], selected=True)
    assert clone.data['opaque'] == source.data['opaque']
    assert type(clone.data['opaque']['number']) is float
    assert clone.get('x') == 72 and applied.changed
    assert tl.undo(1)
    from astrid.sdk.timeline.identity import retain_cut_reservations
    retain_cut_reservations(before, tl.document())
    assert tl.document() == before
    assert tl.redo(1)
    other = Checkout(copy.deepcopy(before))
    apply_sheet(other, 'edit ' + json.dumps(bound.to_json()))
    assert other.document() == tl.document()


def test_stale_source_destination_assets_and_failed_override_are_atomic(tmp_path):
    for case in ('source', 'destination', 'asset', 'override'):
        tl = checkout(tmp_path / case)
        call = commands.layer_copy_call(tl, 'c2', 'c1.rocket')
        bound = commands.run(tl, call, dry_run=True).calls[0]
        if case == 'source': tl.clip('c1.rocket').data['opaque'] = 'changed'
        if case == 'destination': tl.clip('c2.field').data['hold'] = 1
        if case == 'asset': tl._registry('F')['R']['opaque'] = 'changed'
        if case == 'override':
            bound = copy.deepcopy(bound.to_json())
            bound['args']['set_values'] = {'not_a_declared_parameter': 2}
        tl = Checkout(copy.deepcopy(tl.bundle))
        before = copy.deepcopy(tl.document())
        with pytest.raises(TimelineEditError):
            commands.run(tl, bound)
        assert tl.document() == before


def test_cross_owner_requires_explicit_existing_asset_and_track_mapping(tmp_path):
    from tests.sdk.test_timeline_sheet import named
    tl = Checkout(named())
    call = commands.layer_copy_call(tl, 'c2', 'c1.rocket')
    before = copy.deepcopy(tl.document())
    with pytest.raises(commands.CommandError, match='cross-owner'):
        commands.run(tl, call)
    assert tl.document() == before
    for track, asset in [('missing', 'Q'), ('type', 'missing'), ('vo', 'Q')]:
        with pytest.raises(commands.CommandError):
            commands.run(tl, commands.layer_copy_call(tl, 'c2', 'c1.rocket', track=track, asset=asset))
        assert tl.document() == before
    plan = commands.run(tl, commands.layer_copy_call(tl, 'c2', 'c1.rocket', track='type', asset='Q'))
    clone = commands.authored_owner(tl, plan.calls[0].created[0], selected=True)
    assert clone.shot_id == 'B' and clone.cut_id == 'c2' and clone.asset == 'Q' and clone.track == 'type'


def test_copy_refuses_malformed_source_and_retained_creation_identity(tmp_path, monkeypatch):
    from astrid.sdk.timeline import shot_groups
    tl = checkout(tmp_path)
    call = commands.layer_copy_call(tl, 'c2', 'c1.rocket')
    before = copy.deepcopy(tl.document())
    for bad in (None, 'c1.rocket', 'occurrence:missing/clip:missing'):
        changed = copy.deepcopy(call)
        changed['args']['from'] = bad
        with pytest.raises(commands.CommandError):
            commands.run(tl, changed)
        assert tl.document() == before
    preview = commands.run(tl, call, dry_run=True)
    monkeypatch.setattr(shot_groups, 'reservations', lambda checkout: list(preview.calls[0].created))
    with pytest.raises(commands.CommandError, match='retained image snapshot'):
        commands.run(tl, preview.calls[0])
    assert tl.document() == before
