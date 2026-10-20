"""Private source proposal for the Main voiceover occurrence-duration carrier."""
from __future__ import annotations

import copy

import pytest

from astrid.packs.video_editing.shared import draft_voiceover as vo
from astrid.sdk.timeline._command_state import CommandError, State, present
from astrid.sdk.timeline.commands import execute, validate_command
from astrid.sdk.timeline.native_occurrence_resize import capture_occurrence_resize
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_m1_commands import inverse
from tests.packs.video_editing.test_draft_voiceover import fixture, synthesis


def voiceover_bundle():
    candidate, scripts = fixture()
    scripts['occurrences'][0]['text'] = 'Long new narration'
    candidate['placements'][0].update({
        'opaque_occurrence': {'keep': [None, False, 0]},
        'provenance': {'source': 'Main voiceover'},
    })
    candidate['placements'][0]['placement']['opaque_geometry'] = {'keep': True}
    prepared = vo.prepare_draft_voiceover(
        candidate, scripts, synthesize=synthesis, timing_policy='ripple', padding_seconds=.15,
    )
    # This is the existing authored candidate model. The native command
    # engine needs only its ordinary source-mapping envelope; this proposal
    # does not publish or materialize it.
    original = copy.deepcopy(candidate)
    original['parent']['config']['output'] = {'fps': {'numerator': 30000, 'denominator': 1001}}
    original['placements'][0].update(
        source_offset={'start': 0, 'end': 0}, speed={'numerator': 1, 'denominator': 1},
    )
    original['source_mapping'] = {'shots': {}, 'placements': {}}
    return original, prepared


def test_main_ripple_duration_is_carried_by_same_occurrence_identity():
    original, prepared = voiceover_bundle()
    command = capture_occurrence_resize(original, 'o1', prepared['candidate']['placements'][0]['duration_ms'])
    validate_command(command)
    plan = execute(original, [command])

    assert State(plan.bundle).occurrence('occurrence:o1')['occurrence_id'] == 'o1'
    assert State(plan.bundle).occurrence('occurrence:o1')['duration_ms'] == 4150
    assert State(plan.bundle).occurrence('occurrence:o1')['shot_id'] == 's1'
    assert State(plan.bundle).occurrence('occurrence:o1')['opaque_occurrence'] == {
        'keep': [None, False, 0]}
    assert State(plan.bundle).occurrence('occurrence:o1')['placement'] == {
        'start_ms': 0, 'opaque_geometry': {'keep': True}}
    assert [write['path'] for write in plan.records[0]['writes']] == [['duration_ms']]
    # Ripple's parent extent is a separate authored field; this carrier does
    # not invent a root writer or silently update it.
    assert plan.bundle['parent']['config']['duration'] == 6


def test_resize_inverse_redo_and_aba_guard_keep_the_original_identity():
    original, _ = voiceover_bundle()
    plan = execute(original, [capture_occurrence_resize(original, 'o1', 4150)])
    undone = inverse(plan.bundle, plan.records)
    assert undone.bundle == original
    assert inverse(undone.bundle, undone.records).bundle == plan.bundle
    with pytest.raises(CommandError, match='intervening'):
        inverse(plan.bundle, plan.records, [{
            'writes': [{'ref': 'occurrence:o1', 'path': ['duration_ms'],
                        'before': present(4150), 'after': present(4150)}]}])


def test_resize_rebases_over_disjoint_occurrence_property_and_preserves_sibling():
    original, _ = voiceover_bundle()
    plan = execute(original, [capture_occurrence_resize(original, 'o1', 4150)])
    head = copy.deepcopy(original)
    State(head).occurrence('occurrence:o1')['opaque_occurrence']['concurrent'] = True
    State(head).occurrence('occurrence:o2')['duration_ms'] = 3200
    rebased = replay(plan, head)
    assert State(rebased.bundle).occurrence('occurrence:o1')['duration_ms'] == 4150
    assert State(rebased.bundle).occurrence('occurrence:o1')['opaque_occurrence']['concurrent'] is True
    assert State(rebased.bundle).occurrence('occurrence:o2')['duration_ms'] == 3200
    assert inverse(rebased.bundle, rebased.records).bundle == head


@pytest.mark.parametrize('duration_ms', [0, -1, 1.5, True])
def test_resize_requires_a_finite_positive_integer(duration_ms):
    original, _ = voiceover_bundle()
    before = copy.deepcopy(original)
    with pytest.raises(CommandError):
        capture_occurrence_resize(original, 'o1', duration_ms)
    assert original == before


def test_resize_requires_a_stable_identity_without_mutating_the_draft():
    original, _ = voiceover_bundle()
    original['placements'][0].pop('occurrence_id')
    before = copy.deepcopy(original)
    with pytest.raises(CommandError):
        capture_occurrence_resize(original, 'o1', 4150)
    assert original == before
