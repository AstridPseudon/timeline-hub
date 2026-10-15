"""Scene completeness gates publication, independently of structural edits."""
from types import SimpleNamespace
import pytest
from astrid.core.timeline import scene_answers
from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline.publish import _PublishMixin
from astrid.sdk.timeline_checkout import Checkout
from test_timeline_reflow_golden import film


def test_actual_reflow_and_edit_check_work_with_owner_unavailable(monkeypatch):
    scene_answers.use_client(None)
    def unavailable():
        return None
    monkeypatch.setattr('astrid.core.execution.remotion_host_session.host_remotion_client', unavailable)
    tl = Checkout(film())
    tl.remove_line('s2')
    for name in ('c2.field', 'c2.live', 'c2.dot'):
        tl.clip(name).remove()
    tl.clip('c3.card').set(delay=.2)
    report = tl.check()
    assert not report.blocking
    assert report.evaluation_complete is False
    assert any('evaluation-unavailable' in value for value in report.problems)
    with pytest.raises(TimelineEditError, match='scene evaluation incomplete'):
        tl.publish('must refuse before any publication')


def test_publish_refuses_unknown_even_when_structurally_valid_and_force_is_true():
    host = SimpleNamespace(notes=[], _sync_film_length=lambda: [], check=lambda: SimpleNamespace(
        evaluation_complete=False, valid=True, problems=['evaluation unknown-component-bounds p: No declaration']))
    with pytest.raises(TimelineEditError, match='unknown-component-bounds'):
        _PublishMixin.publish(host, 'unknown cannot be accepted', force=True)


def test_publish_blocking_gap_and_empty_consume_exact_shared_span_classes(monkeypatch):
    tl = Checkout(film())
    spans = [scene_answers.Span(0, 120, 'GAP', None, ()),
             scene_answers.Span(120, 180, 'COVERED', 'EMPTY', ('background',))]
    monkeypatch.setattr(tl, '_on_screen', lambda: spans)
    gaps = tl.picture_gaps()
    empty, _ = tl.empty_cuts()
    assert gaps and 'GAP' in gaps[0]
    assert empty and 'EMPTY' in empty[0]
    report = tl.check()
    assert any(line.startswith('picture ') for line in report.blocking)
    assert any(line.startswith('EMPTY') for line in report.blocking)
