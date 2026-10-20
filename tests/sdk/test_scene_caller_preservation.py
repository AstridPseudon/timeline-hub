"""Formatter positives with supplied scene spans; these do not certify a renderer/source."""
from types import SimpleNamespace

import pytest

from astrid.sdk import timeline_filmstrip
from astrid.sdk.timeline_checkout import Checkout
from tests.sdk.test_coverage_empty_cut import _empty_cut_bundle
from tests.sdk.test_timeline_reflow_golden import film


def span(start, end, cls, content=None, clips=(), findings=()):
    return SimpleNamespace(start_frame=start, end_frame=end, cls=cls, content=content,
                           clips=clips, findings=findings)


def test_c02_background_and_deliberate_hold_keep_original_formatter_buckets(monkeypatch):
    checkout = Checkout(_empty_cut_bundle())
    spans = [span(120, 240, 'COVERED', 'EMPTY', ('b-plate',))]
    sustained, incidental = checkout.empty_cuts(spans)
    assert len(sustained) == 1 and incidental == []
    assert 'EMPTY   c02 4.00–8.00 s (4.00 s): only a background' in sustained[0]
    assert 'c02.field' in sustained[0] and '--hold deliberate' in sustained[0]
    monkeypatch.setattr(checkout, '_on_screen', lambda *args, **kwargs: spans)
    report = checkout.check()
    assert report.valid and not report.blocking
    assert sustained[0] in report.problems
    checkout.set_cut_note('c02', hold='deliberate')
    assert checkout.empty_cuts(spans) == ([], sustained)
    report = checkout.check()
    assert report.valid and not report.blocking
    assert sustained[0] in report.problems
    assert not any('UNKNOWN' in line or 'UNAVAILABLE' in line for line in report.problems)


def test_c2_removed_picture_keeps_live_address_and_original_gap_wording(monkeypatch):
    checkout = Checkout(film())
    checkout.resolve()
    checkout.clip('c2.field').remove()
    spans = [span(120, 180, 'GAP', 'CONTENT')]
    expected = checkout.picture_gaps(spans)
    assert len(expected) == 1 and expected[0].startswith('4.000–6.000 s')
    assert 'c2.live' in expected[0] and 'nothing covers the canvas (GAP)' in expected[0]
    monkeypatch.setattr(checkout, '_on_screen', lambda *args, **kwargs: spans)
    report = checkout.check()
    assert 'picture ' + expected[0] in report.problems
    assert not any(line.startswith('picture ') for line in report.blocking)


def test_c02_declared_half_second_dip_keeps_cut_and_duration(monkeypatch):
    checkout = Checkout(_empty_cut_bundle(effects={'fade_in': 0.5}))
    spans = [span(120, 135, 'DIP', 'CONTENT', ('b-plate',))]
    expected = checkout.dips(spans)
    assert expected == ['DIP     c02 4.00–4.50 s (0.50 s): a declared fade/dip (not a gap)']
    monkeypatch.setattr(checkout, '_on_screen', lambda *args, **kwargs: spans)
    report = checkout.check()
    assert report.valid and not report.blocking
    assert expected[0] in report.problems
    assert not any('GAP' in line or 'UNKNOWN' in line for line in report.problems)


def test_known_covered_content_is_an_answer_not_a_refusal(monkeypatch):
    checkout = Checkout(_empty_cut_bundle())
    monkeypatch.setattr(checkout, '_on_screen', lambda *args, **kwargs: [span(0, 240, 'COVERED', 'CONTENT')])
    report = checkout.check()
    assert report.valid and not report.blocking
    assert not any(line.startswith(('picture ', 'scene ', 'EMPTY', 'DIP')) for line in report.problems)


@pytest.mark.parametrize(('cls', 'content', 'finding'), [
    ('UNKNOWN', 'UNKNOWN', 'unknown-component-bounds'),
    ('UNAVAILABLE', None, 'exact source unavailable'),
    ('COVERED', 'UNKNOWN', 'unknown-glyph-presence'),
])
def test_only_actual_unknown_or_unavailable_answers_are_labelled_so(monkeypatch, cls, content, finding):
    checkout = Checkout(_empty_cut_bundle())
    spans = [span(120, 240, cls, content, findings=(finding,))]
    monkeypatch.setattr(checkout, '_on_screen', lambda *args, **kwargs: spans)
    report = checkout.check()
    assert report.valid and not report.blocking
    assert any(finding in line for line in report.problems)
    assert not any('EMPTY' in line or 'GAP' in line for line in report.problems)


def test_scene_advice_does_not_erase_structural_invalidity(monkeypatch):
    candidate = _empty_cut_bundle()
    candidate['schema_version'] = 999
    checkout = Checkout(candidate)
    monkeypatch.setattr(checkout, '_on_screen', lambda *args, **kwargs: [span(0, 240, 'COVERED', 'CONTENT')])
    report = checkout.check()
    assert not report.valid
    assert any('invalid:' in line for line in report.problems)


def _scene_context():
    return {
        'mode': 'filmstrip',
        'capture_identity': 'capture-1',
        'video_digest': 'video-1',
        'video_object_id': 'object-1',
        'managed_object_reference': 'managed-1',
        'capture_snapshot': {
            'duration_frames': 2,
            'metadata': {'scene_clips': {'compiled-1': {'address': 'c01.field'}}},
        },
    }


def test_private_scene_only_request_reuses_managed_capture_without_png_or_caller_authority(monkeypatch):
    context = _scene_context()
    seen = {}
    def prepare(inputs, **kwargs):
        seen['inputs'] = dict(inputs)
        return context

    monkeypatch.setattr(timeline_filmstrip, 'prepare_filmstrip', prepare)

    request, prepared = timeline_filmstrip._scene_only_request(
        {'timeline_ref': 'tl'}, project='project', client=object(),
    )

    assert prepared is context
    assert request['mode'] == 'scene_only'
    assert request['formats'] == ['md']
    assert request['composed_capture'] is True and request['include_media'] is True
    assert not any(key in request for key in (
        'source_ref', 'certification', 'authority_context', 'provider', 'store', 'endpoint',
    ))
    assert seen['inputs'] == request


def test_private_scene_only_stale_result_is_advisory_unavailable():
    context = _scene_context()
    result = {
        'ok': True,
        'scene_result': {
            'capture_identity': 'old-capture',
            'source_label': 'committed revision r1',
            'compiled_id_address_map': {'compiled-1': 'c01.field'},
            'scene_answers': [],
        },
    }

    spans = timeline_filmstrip._scene_only_spans(result, context)

    assert len(spans) == 1
    assert spans[0].cls == 'UNAVAILABLE'
    assert 'stale scene capture' in spans[0].findings


def test_private_scene_only_known_result_joins_compiled_addresses_and_findings():
    context = _scene_context()
    result = {
        'ok': True,
        'scene_result': {
            'capture_identity': 'capture-1',
            'source_label': 'committed revision r1',
            'managed_object_reference': 'managed-1',
            'compiled_id_address_map': {'compiled-1': 'c01.field'},
            'scene_answers': [
                {'frame': 0, 'coverage': 'COVERED', 'content': 'CONTENT',
                 'layers': [{'clipId': 'compiled-1', 'bounds_source': 'declared'}],
                 'findings': []},
                {'frame': 1, 'coverage': 'COVERED', 'content': 'CONTENT',
                 'layers': [{'clipId': 'compiled-1', 'bounds_source': 'declared'}],
                 'findings': []},
            ],
        },
    }

    spans = timeline_filmstrip._scene_only_spans(result, context)

    assert [(span.start_frame, span.end_frame, span.cls, span.content, span.clips) for span in spans] == [
        (0, 2, 'COVERED', 'CONTENT', ('c01.field',)),
    ]


def test_private_scene_only_invokes_existing_managed_visualization(monkeypatch):
    context = _scene_context()
    calls = []

    class Client:
        def invoke_result(self, capability, **kwargs):
            calls.append((capability, kwargs))
            return {
                'ok': True,
                'scene_result': {
                    'capture_identity': 'capture-1',
                    'source_label': 'committed revision r1',
                    'compiled_id_address_map': {'compiled-1': 'c01.field'},
                    'scene_answers': [
                        {'frame': 0, 'coverage': 'COVERED', 'content': 'CONTENT',
                         'layers': [{'clipId': 'compiled-1'}], 'findings': []},
                        {'frame': 1, 'coverage': 'COVERED', 'content': 'CONTENT',
                         'layers': [{'clipId': 'compiled-1'}], 'findings': []},
                    ],
                },
            }

    monkeypatch.setattr(timeline_filmstrip, 'prepare_filmstrip', lambda inputs, **kwargs: context)
    spans, _prepared = timeline_filmstrip._invoke_scene_only(
        {'timeline_ref': 'tl'}, project='project', client=Client(),
    )

    assert calls[0][0] == 'rendering.timeline_visualize'
    assert calls[0][1]['kind'] == 'executor'
    assert calls[0][1]['wait'] is True
    assert calls[0][1]['read_managed_outputs'] is True
    assert calls[0][1]['inputs']['mode'] == 'scene_only'
    assert spans[0].clips == ('c01.field',)
