"""Scene completeness gates publication, independently of structural edits."""
import pytest
from astrid.core.timeline import scene_answers
from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline_checkout import Checkout
from test_timeline_reflow_golden import film
from test_timeline_saved_publish import setup, synthetic_scene_answers, edit  # noqa: F401


def test_actual_reflow_and_edit_check_work_with_owner_unavailable(monkeypatch, setup):
    scene_answers.use_client(None)
    def unavailable():
        return None
    monkeypatch.setattr('astrid.core.execution.remotion_host_session.host_remotion_client', unavailable)
    tl = Checkout(film())
    tl.remove_line('s2', visuals='remove')
    tl.clip('c3.card').set(delay=.2)
    report = tl.check()
    assert not report.blocking
    assert report.evaluation_complete is False
    assert any('evaluation-unavailable' in value for value in report.problems)
    with pytest.raises(TimelineEditError, match='scene evaluation incomplete'):
        draft, runtime = setup
        edit(draft, x=90)
        draft.publish('must refuse before any publication', client=runtime.client())
    assert runtime.calls == [] and runtime.publications == []


def test_publish_refuses_unknown_and_force_cannot_bypass_commit(setup, monkeypatch):
    draft, runtime = setup
    edit(draft, x=90)
    unknown = [scene_answers.Span(0, 270, 'UNKNOWN', None, (),
        ('unknown-component-bounds p: No declaration',))]
    monkeypatch.setattr(Checkout, '_on_screen', lambda self: unknown)
    assert draft.check().valid
    with pytest.raises(TimelineEditError, match='unknown-component-bounds'):
        draft.publish('unknown cannot be accepted', client=runtime.client())
    with pytest.raises(TimelineEditError, match='expectations'):
        draft.publish('unknown cannot be forced', client=runtime.client(), force=True)
    assert runtime.calls == [] and runtime.publications == []


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
