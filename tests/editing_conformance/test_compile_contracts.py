"""Shared compile-contract vectors: occurrence -> clip, as main's projection emits them.

The vectors are fixtures/audio_compile_contract.json and fixtures/visual_compile_contract.json;
the design is design/audio-compile-contract.md and design/visual-compile-contract.md.
"""
from __future__ import annotations

import json
import re
from fractions import Fraction
from pathlib import Path

import pytest

from astrid.core.timeline.duration import clip_end_frame, clip_start_frame
from astrid.core.timeline.shot_composition_projection import project_shot_composition

REPO = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).parent / 'fixtures'
AUDIO = json.loads((FIXTURES / 'audio_compile_contract.json').read_text(encoding='utf-8'))
VISUAL = json.loads((FIXTURES / 'visual_compile_contract.json').read_text(encoding='utf-8'))


def _graph(path):
    return json.loads((REPO / path).read_text(encoding='utf-8'))


def _revision(graph, shot_id, revision_id):
    return next(r for r in graph['shot_revisions'] if r['shot_id'] == shot_id and r['revision_id'] == revision_id)


def _clips(revision):
    return revision['internal_timeline_revision']['timeline']['clips']


def _lookup(clip, dotted):
    node = clip
    for part in dotted.split('.'):
        node = node.get(part) if isinstance(node, dict) else None
    return node


def _marked(vectors):
    cases = []
    for vector in vectors:
        marks = [pytest.mark.xfail(strict=True, reason=vector['xfail'])] if 'xfail' in vector else []
        cases.append(pytest.param(vector, id=vector['id'], marks=marks))
    return cases


def _audio_clip(vector):
    graph = _graph(AUDIO['base']['graph'])
    occurrence = next(o for o in graph['occurrences'] if o['occurrence_id'] == AUDIO['base']['occurrence'])
    occurrence.update(vector['occurrence'])
    child = next(c for c in _clips(_revision(graph, 'shot-alpha', 'rev-a')) if c['id'] == AUDIO['base']['child'])
    child.pop('duration_ms')
    child.update(AUDIO['base']['child_default'])
    child.update(vector['child'])
    projection = project_shot_composition(graph)
    return next(c for c in projection.config['clips']
                if c.get('shot_occurrence_id') == AUDIO['base']['occurrence']
                and c['app']['astrid_shot_composition']['source_clip_id'] == AUDIO['base']['child'])


@pytest.mark.parametrize('vector', _marked(AUDIO['vectors']))
def test_audio_vector(vector):
    clip = _audio_clip(vector)
    for key, want in vector['expect'].items():
        if key == 'metadata':
            meta = clip['app']['astrid_shot_composition']
            assert {name: meta[name] for name in want} == want
        elif want is None:
            assert _lookup(clip, key) is None
        elif isinstance(want, bool):
            assert bool(_lookup(clip, key)) is want
        else:
            assert _lookup(clip, key) == pytest.approx(want)


def _closure_graph():
    graph = _graph(VISUAL['base']['graph'])
    rows = VISUAL['closure']['occurrences']
    for row in rows:
        occurrence = next(o for o in graph['occurrences'] if o['occurrence_id'] == row['occurrence_id'])
        occurrence.update(at_ms=row['at_ms'], duration_ms=row['duration_ms'])
        child = next(c for c in _clips(_revision(graph, *row['shot_revision'])) if c['track'] == VISUAL['lane'])
        child['duration_ms'] = row['child_duration_ms']
    keep = [row['occurrence_id'] for row in rows]
    graph['occurrences'] = [next(o for o in graph['occurrences'] if o['occurrence_id'] == oid) for oid in keep]
    for ordinal, occurrence in enumerate(graph['occurrences']):
        occurrence['ordinal'] = ordinal
    return graph


def _lane_clips(projection):
    return [c for c in projection.config['clips'] if c['track'] == VISUAL['lane']]


def _clock():
    # main's rational clock is the [num, den] pair (filmstrip_cards.py:466); the frame helpers take a Real, so pass the Fraction.
    return Fraction(*VISUAL['fps_rational'])


@pytest.mark.parametrize('vector', _marked(VISUAL['vectors']))
def test_visual_vector(vector):
    fps = _clock()
    projection = project_shot_composition(_closure_graph())
    clip = next(c for c in _lane_clips(projection) if c['shot_occurrence_id'] == vector['occurrence_id'])
    start = clip_start_frame(clip, fps)
    end = clip_end_frame(clip, fps)
    rows = {'start_frame': start, 'end_frame': end, 'duration_frames': end - start}
    assert rows[vector['field']] == vector['expect']


def test_popup_closure_occurrences_are_half_open_on_the_shared_lane():
    fps = _clock()
    projection = project_shot_composition(_closure_graph())
    spans = sorted((clip_start_frame(c, fps), clip_end_frame(c, fps)) for c in _lane_clips(projection))
    assert len(spans) == len(VISUAL['closure']['occurrences'])
    for (_, earlier_end), (later_start, _) in zip(spans, spans[1:]):
        assert earlier_end <= later_start


def test_render_pin_gives_element_clips_the_clip_look():
    # origin/main pins Composition 0.0.6, which mounts effect clips bare (docs/reference/timeline-composition-v0.0.6/TimelineComposition.tsx:121-132).
    # 0.0.7 added the ClipLook on element clips (composition 6bd784d); the intended change is already in this tree's pin.
    package = json.loads((REPO / 'remotion/package.json').read_text(encoding='utf-8'))
    pin = package['dependencies']['@banodoco/timeline-composition']
    version = tuple(int(part) for part in re.search(r'(?:tags/v|timeline-composition-)(\d+)\.(\d+)\.(\d+)(?:\.tar\.gz|\.tgz)$', pin).groups())
    assert version >= (0, 0, 7)
