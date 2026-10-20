"""Shared compile-contract vectors for projected timing and public source clocks.

The vectors are fixtures/audio_compile_contract.json and fixtures/visual_compile_contract.json;
the design is docs/design/audio-compile-contract.md and docs/design/visual-compile-contract.md.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tarfile
from copy import deepcopy
from fractions import Fraction
from pathlib import Path

import pytest

from astrid.core.timeline.duration import clip_end_frame, clip_start_frame, clip_timeline_duration
from astrid.core.timeline.shot_composition_projection import (
    project_runtime_parent_composition,
    project_shot_composition,
)

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


def _projection(closure='native'):
    # The native ADD closure, projected by main's runtime parent path (shot_composition_projection.py, identical to main e51595c6).
    # The overhang closure is the same parent with only its occurrence list replaced.
    native = VISUAL['native_add_output']
    payload = native['parent_revision']['payload']
    if closure == 'overhang':
        payload = dict(payload, occurrences=VISUAL['overhang_closure']['occurrences'])
    parent = {
        'project_id': native['project_id'],
        'timeline_id': native['timeline_id'],
        'revision_id': native['parent_revision']['revision_id'],
        'payload': payload,
    }
    return project_runtime_parent_composition(
        parent,
        shot_revisions=native['shot_revisions'],
        internal_timeline_revisions=native['internal_timeline_revisions'],
    )


def _source_clip(projection, occurrence_id, source_clip_id):
    return next(c for c in projection.config['clips']
                if c.get('shot_occurrence_id') == occurrence_id
                and c['app']['astrid_shot_composition']['source_clip_id'] == source_clip_id)


def _clock():
    # The native fps is {numerator, denominator}; the frame helpers take a Real, so pass the Fraction built from it.
    # Passing the dict or the [num, den] list to clip_start_frame raises ValueError at _positive_fps (duration.py:45-49).
    fps = VISUAL['fps']
    return Fraction(fps['numerator'], fps['denominator'])


@pytest.mark.parametrize('vector', _marked(VISUAL['vectors']))
def test_visual_vector(vector):
    fps = _clock()
    clip = _source_clip(_projection(vector.get('closure', 'native')), vector['occurrence_id'], vector['source_clip_id'])
    start = clip_start_frame(clip, fps)
    end = clip_end_frame(clip, fps)
    rows = {'start_frame': start, 'end_frame': end, 'duration_frames': end - start}
    assert rows[vector['field']] == vector['expect']


def test_closure_places_occurrences_at_eight_and_ten_seconds_on_the_picture_lane():
    projection = _projection()
    placed = {o['occurrence_id']: (o['at'], o['hold']) for o in projection.occurrences}
    expected = {row['occurrence_id']: (row['at_ms'] / 1000, row['duration_ms'] / 1000) for row in VISUAL['closure']['occurrences']}
    assert placed == expected
    assert all(c['track'] == VISUAL['lane'] for c in projection.config['clips'] if 'shot_occurrence_id' in c)


def test_popup_closure_source_windows_are_half_open_on_the_shared_lane():
    # Occurrence spans overlap (A 8-18 s, B 10-20 s). The source-window children do not: A's child ends where B's begins.
    fps = _clock()
    projection = _projection()
    first, second = VISUAL['closure']['occurrences']
    earlier = _source_clip(projection, first['occurrence_id'], first['source_clip_id'])
    later = _source_clip(projection, second['occurrence_id'], second['source_clip_id'])
    assert clip_end_frame(earlier, fps) <= clip_start_frame(later, fps)


def test_native_child_keeps_its_opaque_and_null_params_fields():
    clip = _source_clip(_projection(), 'occ-a', 'reserved-child')
    assert clip['opaque'] == [None, False, {}]
    assert clip['params'] is None


def test_overhang_child_is_clamped_to_its_occurrence_end():
    # Clamp on, the one policy: the child is absolute [3, 5) s but occ-c ends at 3.5 s, so only 0.5 s is visible.
    clip = _source_clip(_projection('overhang'), 'occ-c', 'clip-a')
    assert clip['at'] == pytest.approx(3.0)
    assert clip_timeline_duration(clip) == pytest.approx(0.5)
    assert clip['at'] + clip_timeline_duration(clip) == pytest.approx(3.5)


def test_cap_fade_editor_projection_keeps_clamped_timing_and_authored_source():
    vector = VISUAL['cap_fade_closure']
    graph = deepcopy(vector['app_fixture'])
    occurrence = next(o for o in graph['occurrences']
                      if o['occurrence_id'] == vector['base']['occurrence_id'])
    # App derives this cap from the next same-lane cut. This Agent analog
    # receives that cap explicitly; it does not implement App's lane policy.
    occurrence.update(at_ms=vector['occurrence_cap']['start_ms'],
                      duration_ms=vector['occurrence_cap']['duration_ms'])
    revision = _revision(graph, vector['base']['shot_id'], vector['base']['revision_id'])
    revision['internal_timeline_revision']['timeline']['clips'] = [deepcopy(vector['child'])]
    before = deepcopy(graph)
    projection = project_shot_composition(graph)
    clip = _source_clip(projection, occurrence['occurrence_id'], vector['child']['id'])
    editor = vector['editor_projection']
    for field in ('id', 'at', 'track', 'clipType', 'asset', 'hold', 'effects'):
        assert clip[field] == editor[field]
    assert clip_end_frame(clip, vector['fps']) == vector['end_frame']
    assert graph == before
    assert _clips(_revision(projection.graph, vector['base']['shot_id'],
                            vector['base']['revision_id'])) == [vector['child']]


@pytest.fixture(scope='module')
def public_visual_evaluation(tmp_path_factory):
    package = json.loads((REPO / 'remotion/package.json').read_text(encoding='utf-8'))
    pin = package['dependencies']['@banodoco/timeline-composition']
    assert pin.startswith('file:')
    # Evaluate the shipped public package in a private temp directory. Its
    # pure evaluation entry needs no install, shared dependencies or cache.
    with tarfile.open(REPO / 'remotion' / pin.removeprefix('file:')) as archive:
        destination = tmp_path_factory.mktemp('visual-contract-package')
        members = [m for m in archive.getmembers() if m.isfile() and (
            m.name == 'package/package.json' or m.name.startswith('package/dist/'))]
        archive.extractall(destination, members=members, filter='data')
    return (destination / 'package/dist/evaluation.js').as_uri()


def _public_visual_result(module, clip, vector):
    result = subprocess.run(
        ['node', '--input-type=module', '-e', '''
import {readFileSync} from 'node:fs';
const {clipOpacity, prepareScene, queryTrackFrame} = await import(process.argv[1]);
const {clip, fps, sample, last, end} = JSON.parse(readFileSync(0, 'utf8'));
const scene = prepareScene([{track: {id: clip.track, kind: 'visual'}, clips: [clip],
  transitions: [], incomingTransitions: [null]}], {assets: {}}, fps, 1920, 1080);
const prepared = scene.tracks[0].prepared;
const plan = prepared.plans[0];
console.log(JSON.stringify({opacity: clipOpacity(clip, sample, fps),
  own_duration_frames: plan.ownDuration, draw_duration_frames: plan.drawDuration,
  last_clip_indices: queryTrackFrame(prepared, last).layers.map(l => l.clipIndex),
  end_layers: queryTrackFrame(prepared, end).layers}));
''', module],
        input=json.dumps({'clip': clip, 'fps': vector['fps'], 'sample': vector['sample_frame'],
                          'last': vector['last_draw_frame'], 'end': vector['end_frame']}),
        text=True, capture_output=True, check=True, timeout=30,
    )
    return json.loads(result.stdout)


@pytest.mark.parametrize('case', ['clamped-analog', 'editor', 'raw-diagnostic'])
def test_cap_fade_public_source_clock_and_half_open_draw_cap(case, public_visual_evaluation):
    vector = VISUAL['cap_fade_closure']
    input_key, expect_key = {
        'clamped-analog': ('editor_projection', 'render'),
        'editor': ('editor_projection', 'editor'),
        'raw-diagnostic': ('render_input', 'diagnostic_raw'),
    }[case]
    result = _public_visual_result(public_visual_evaluation, vector[input_key], vector)
    assert result == {
        **vector['expect'][expect_key], 'last_clip_indices': [0], 'end_layers': [],
    }


def test_single_occurrence_cap_through_normal_managed_projection(tmp_path, public_visual_evaluation):
    from astrid.packs.rendering.actions.render.managed_timeline import (
        materialize_managed_render_snapshot,
        resolve_managed_render_snapshot,
        validate_managed_render_snapshot,
    )
    from astrid.packs.rendering.shared.rendering_backend import _serialize_timeline
    from tests.packs.rendering.test_managed_timeline_render import _Runtime

    vector = VISUAL['single_occurrence_cap_closure']
    path = FIXTURES / vector['raw_fixture']
    raw_bytes = path.read_bytes()
    assert hashlib.sha256(raw_bytes).hexdigest() == vector['raw_fixture_sha256']
    closure = json.loads(raw_bytes)
    before = deepcopy(closure)
    parent = closure['parent_revision']
    assert len(parent['payload']['occurrences']) == 1
    assert parent['payload']['occurrences'][0]['duration_ms'] == 4000
    child = closure['internal_timeline_revisions'][0]['payload']['clips'][0]
    assert child['hold'] == 5
    assert child['effects'] == {'fade_out': 1}
    asset = closure['internal_timeline_revisions'][0]['payload']['registry']['assets']['image']
    runtime = _Runtime(media=[{'media_id': asset['media_id'], 'digest': asset['content_sha256'],
                               'project_id': parent['project_id']}])
    runtime.timeline['head_revision_id'] = parent['revision_id']
    runtime.parent_revisions[parent['revision_id']] = parent
    runtime.exact_shot_revisions = {(r['shot_id'], r['revision_id']): r for r in closure['shot_revisions']}
    runtime.internal_revisions = {r['revision_id']: r for r in closure['internal_timeline_revisions']}
    snapshot = resolve_managed_render_snapshot(
        project_ref='demo', timeline_ref='main', expected_version=1, client=runtime,
    )
    validate_managed_render_snapshot(snapshot)
    projected = project_runtime_parent_composition(
        parent, shot_revisions=closure['shot_revisions'],
        internal_timeline_revisions=closure['internal_timeline_revisions'],
    )
    assert snapshot.config == projected.config == vector['projected_config']
    assert snapshot.registry == projected.registry == vector['registry']
    timeline_path, _, _ = materialize_managed_render_snapshot(tmp_path, snapshot)
    timeline = _serialize_timeline(timeline_path)
    assert timeline == vector['serialized_timeline']
    assert timeline['clips'][0]['hold'] == 4
    assert clip_end_frame(timeline['clips'][0], vector['fps']) == vector['end_frame']
    assert closure == before
    assert path.read_bytes() == raw_bytes

    # Evaluate the actual serialized output, with no synthetic cap/next cut or
    # canonicalTiming added. No-transition preparation is sufficient for this closure.
    result = subprocess.run(
        ['node', '--input-type=module', '-e', '''
import {readFileSync} from 'node:fs';
const {clipOpacity, prepareScene, queryTrackFrame} = await import(process.argv[1]);
const {timeline, assets, vector, raw} = JSON.parse(readFileSync(0, 'utf8'));
const fps = timeline.output.fps;
const scene = prepareScene(timeline.tracks.map(track => ({track,
  clips: timeline.clips.filter(c => c.track === track.id), transitions: []})),
  assets, fps, 1920, 1080);
const {clips, prepared} = scene.tracks[0];
const plan = prepared.plans[0];
console.log(JSON.stringify({opacity: clipOpacity(clips[0], vector.sample_frame, fps),
  control_opacity: clipOpacity(clips[0], vector.control_frame, fps),
  last_opacity: clipOpacity(clips[0], vector.last_draw_frame, fps),
  own_duration_frames: plan.ownDuration, draw_duration_frames: plan.drawDuration,
  last_clip_indices: queryTrackFrame(prepared, vector.last_draw_frame).layers.map(l => l.clipIndex),
  end_layers: queryTrackFrame(prepared, vector.end_frame).layers,
  raw_diagnostic_opacity: clipOpacity(raw, vector.sample_frame, fps)}));
''', public_visual_evaluation],
        input=json.dumps({'timeline': timeline, 'assets': snapshot.registry, 'vector': vector, 'raw': child}),
        text=True, capture_output=True, check=True, timeout=30,
    )
    observed = json.loads(result.stdout)
    assert observed.pop('raw_diagnostic_opacity') == 1
    assert observed.pop('last_opacity') == pytest.approx(vector['expect']['last_opacity'])
    assert observed == {key: value for key, value in vector['expect'].items() if key != 'last_opacity'}


def test_render_pin_gives_element_clips_the_clip_look():
    # origin/main pins Composition 0.0.6, which mounts effect clips bare (docs/reference/timeline-composition-v0.0.6/TimelineComposition.tsx:121-132).
    # 0.0.7 added the ClipLook on element clips (composition 6bd784d); the intended change is already in this tree's pin.
    package = json.loads((REPO / 'remotion/package.json').read_text(encoding='utf-8'))
    pin = package['dependencies']['@banodoco/timeline-composition']
    version = tuple(int(part) for part in re.search(r'(?:tags/v|timeline-composition-)(\d+)\.(\d+)\.(\d+)(?:\.tar\.gz|\.tgz)$', pin).groups())
    assert version >= (0, 0, 7)
