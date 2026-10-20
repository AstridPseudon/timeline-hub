"""Run the actual current M2 publication compiler and canonical projector once."""
import copy
import json
from pathlib import Path
from unittest.mock import patch

from astrid.core.timeline import authoring_bundle as compiler
from astrid.core.timeline import shot_composition_projection as projector
from astrid.packs.rendering.actions.render.managed_timeline import _render_compatible_projection
from tests.timeline.test_authoring_bundle import _closure

parent, shots, internals = _closure(shared=False)
bundle = compiler.open_authoring_bundle(parent, shot_revisions=shots, internal_timeline_revisions=internals)
placement = bundle['placements'][0]
placement['duration_ms'] = 1200
placement['track'] = 'V1'
placement['placement']['track'] = 'V1'
placement['gain'] = 0.5
child = bundle['shots'][placement['shot_id']]['internal_timeline']
child['tracks'] = [{'id': 'A1', 'kind': 'audio', 'label': 'Audio', 'volume': 0.5}]
child['clips'] = [
    {'id': 'voice-1', 'track': 'A1', 'clipType': 'media', 'asset': 'voice',
     'at': 0.016682, 'from': 0.051, 'to': 3.051, 'speed': 1.5, 'volume': 3,
     'params': {'fadeIn': 0.2, 'fadeOut': 0.2, 'fadeInCurve': 'equal-power'},
     'app': {'astrid_slice_origin': {'at': 99}, 'opaque': [None, False]}},
    {'id': 'overlap', 'track': 'A1', 'clipType': 'media', 'asset': 'voice',
     'at': 0.2, 'from': 0, 'to': 3, 'volume': 0, 'params': {'fadeIn': 0.1}},
]
bundle['parent']['config']['tracks'] = [{'id': 'V1', 'kind': 'visual', 'label': 'Visual'}]
bundle['parent']['config']['clips'][0]['track'] = 'V1'
bundle['parent']['clips'][0]['track'] = 'V1'
raw_child = copy.deepcopy(child['clips'][0])
before = copy.deepcopy(bundle)
with patch.object(compiler, 'compile_authoring_candidate', wraps=compiler.compile_authoring_candidate) as compile_call:
    result = compiler.compile_authoring_candidate(bundle)
    assert compile_call.call_count == 1
publication = result.publication
with patch.object(projector, 'project_runtime_parent_composition', wraps=projector.project_runtime_parent_composition) as project_call:
    projected = projector.project_runtime_parent_composition(
        {'project_id': publication['project_id'], 'timeline_id': publication['timeline_id'],
         'revision_id': publication['parent_revision_id'], 'payload': publication['parent_composition']},
        shot_revisions=publication['shot_revisions'],
        internal_timeline_revisions=publication['internal_timeline_revisions'],
    )
    assert project_call.call_count == 1
config, registry = _render_compatible_projection(projected.config, projected.registry)
assert bundle == before
clip = next(c for c in config['clips'] if c['id'] == 'occ-1:voice-1')
assert clip['at'] == raw_child['at']
assert clip['volume'] == 1.5
assert abs(clip['to'] - 1.825977) < 1e-12
assert clip['speed'] == 1.5
assert clip['asset'] == 'occ-1:voice'
output = {'config': config, 'registry': registry, 'raw_child': raw_child,
          'compile_calls': 1, 'projector_calls': 1, 'candidate_unchanged': True}
prefix = Path(__file__).with_name('handoff-vw-m3-precision-compat-split-proof-compiled.json')
prefix.write_text(json.dumps(output, indent=2) + '\n')
print(json.dumps({'compile_calls': 1, 'projector_calls': 1, 'compiled_clip': clip, 'raw_child': raw_child}, indent=2))
