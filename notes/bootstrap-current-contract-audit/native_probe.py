"""Probe native state/history boundaries; never construct or publish Runtime history."""
import copy
import json
import os
from pathlib import Path

from astrid.sdk.timeline._command_state import CommandError
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.rebase import replay

root = Path(os.environ['AUDIT_SNAPSHOTS'])
fixture = json.loads((root / 'app-stage/src/tools/video-editor/commands/fixtures/recipe_m2_app_bootstrap.json').read_text())
original = fixture['bundle']
if os.environ['AUDIT_NATIVE'] == '31d':
    from astrid.sdk.timeline._init_commands import capture_timeline_init as capture
    from tests.editing_conformance.test_recipe_m1_commands import inverse
    command = capture(original, **fixture['commands'][0]['args'])
    plan = execute(original, fixture['commands'])
    assert plan.records == fixture['records'] and plan.bundle == fixture['after_bundle']
    undone = inverse(plan.bundle, plan.records)
    assert undone.bundle == original
    assert inverse(undone.bundle, undone.records).bundle == plan.bundle
    recaptured = capture(undone.bundle, **fixture['commands'][0]['args'])
    assert recaptured == command
    assert replay(plan, undone.bundle).bundle == plan.bundle
    try:
        replay(plan, undone.bundle, intervening_records=[*plan.records, *undone.records])
    except CommandError as error:
        assert error.kind == 'intervening_write'
    else:
        raise AssertionError('history-aware replay must refuse')
    from astrid.sdk.timeline.capture import capture_track_create
    track = execute(original, [capture_track_create(original, 'parent', {'id': 'later', 'kind': 'visual'})])
    restored = inverse(track.bundle, track.records)
    assert restored.bundle == original
    try:
        replay(plan, restored.bundle, intervening_records=[*track.records, *restored.records])
    except CommandError as error:
        unrelated = 'refused:' + error.kind
    else:
        unrelated = 'allowed'
    assert unrelated == 'allowed', unrelated
    print('31d unrelated track create/undo with actual records:', unrelated)
    print('PASS 31d: exact App capture/records/defaults, inverse/redo; value-equal undone state permits recapture/history-free replay; supplied init+undo records refuse intervening_write')
else:
    from astrid.sdk.timeline.native_initialize import capture_initialize as capture
    command = capture(original, **fixture['commands'][0]['args'])
    assert command != fixture['commands'][0]
    assert command['expect']['parent::registry.assets'] == {'state': 'absent'}
    assert 'parent::registry' not in command['expect']
    before = copy.deepcopy(original)
    try:
        execute(original, fixture['commands'])
    except CommandError as error:
        assert original == before
        print('PASS successor: retained 31d App batch refused unchanged:', error.kind)
    else:
        raise AssertionError('obsolete App claims must not be silently accepted')
    print('PASS successor: capture writes assets leaf; provider-history and CAS-race cases separately run from frozen main-suite tests')
