"""Pure compiled S2 reference: no Runtime, admission, source certificate or server."""
import base64
import copy
import hashlib
import json
from pathlib import Path
import sys

from astrid.core.timeline.shot_composition_projection import project_runtime_parent_composition
from astrid.packs.rendering.actions.render.managed_timeline import _render_compatible_projection
from astrid.packs.rendering.shared.rendering_backend import _resolved_theme_for_render, _serialize_timeline

root, fixture, output = map(Path, sys.argv[1:])
source = json.loads(fixture.read_text())
doc = copy.deepcopy(source['canonical_document'])
original = copy.deepcopy(doc)
parent = dict(doc['parent_revision'], project_id=doc['project_id'], timeline_id=doc['timeline_id'])
projection = project_runtime_parent_composition(parent, shot_revisions=doc['shot_revisions'],
    internal_timeline_revisions=doc['internal_timeline_revisions'])
config, registry = _render_compatible_projection(projection.config, projection.registry)
assert len(parent['payload']['occurrences']) == 1
assert parent['payload']['occurrences'][0]['duration_ms'] == 4000
raw = doc['internal_timeline_revisions'][0]['payload']['clips'][0]
assert raw['hold'] == 5 and raw['effects'] == [{'fade_out': 1}]
assert len(config['clips']) == 1 and config['clips'][0]['hold'] == 4
path = root / 'compiled.json'
path.write_text(json.dumps(config, indent=2) + '\n')
theme = _resolved_theme_for_render(path, None)
serialized = _serialize_timeline(path, default_theme=theme['id'])
assert serialized['clips'][0]['hold'] == 4 and doc == original
assert serialized['output']['fps'] == 30
image = base64.b64decode(source['media'][0]['bytes_base64'])
assert hashlib.sha256(image).hexdigest() == 'ec19e1c7d1d247d56db54f73e6514c92a82147a1b6ab59eaa30edeebca2e82b6'
public = root / 'remotion/public/image-cap.png'
assert not public.exists()
public.write_bytes(image)
# Explicit static asset analog: no assertion of managed-byte admission.
assets = copy.deepcopy(registry)
for asset in assets['assets'].values():
    asset['file'] = 'image-cap.png'
props = {'timeline': serialized, 'assets': assets, 'theme': theme, 'review': None}
output.mkdir()
for name, value in {'projected.json': dict(projection.config), 'compiled.json': config,
    'serialized.json': serialized, 'props.json': props,
    'trace.json': {'raw': raw, 'stored_cap_ms': 4000, 'projected_hold': 4, 'serialized_hold': 4,
        'source_unchanged': doc == original, 'runtime_admission': False, 'certified': False,
        'claim': 'UNCERTIFIED static compiled S2/currentRoot reference',
        'helpers': ['project_runtime_parent_composition', '_render_compatible_projection',
            '_resolved_theme_for_render', '_serialize_timeline / Timeline.for_render']}}.items():
    (output/name).write_text(json.dumps(value, indent=2) + '\n')
print(json.dumps({'raw_hold': 5, 'stored_ms': 4000, 'projected_hold': 4, 'serialized_hold': 4,
    'theme_background': theme['visual']['color']['bg'], 'certified': False}))
