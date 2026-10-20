"""Replay a flat closure with original MAIN's test transport and product helpers.

Run with PYTHONPATH pointing ONLY at the frozen MAIN archive, never integration.
This does not start Runtime, Node, browser, asset server, or a render.
"""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile

from tests.packs.rendering.test_managed_timeline_render import _Runtime
from astrid.core.rendering.assets import AssetMaterializer
from astrid.packs.rendering.actions.render.managed_timeline import (
    materialize_managed_render_snapshot, resolve_managed_render_snapshot, validate_managed_render_snapshot,
)
from astrid.packs.rendering.shared.rendering_backend import _resolved_theme_for_render, _serialize_timeline


def replay(prefix):
    prefix = str(prefix)
    raw_bytes = Path(prefix + 'raw-closure.json').read_bytes()
    closure = json.loads(raw_bytes)
    original = copy.deepcopy(closure)
    parent = closure['parent_revision']
    image = Path(prefix + 'image.png').read_bytes()
    digest = hashlib.sha256(image).hexdigest()
    runtime = _Runtime(media=[{'media_id': 'sha256:' + digest, 'digest': digest, 'project_id': 'project-demo'}])
    runtime.timeline['head_revision_id'] = parent['revision_id']
    runtime.parent_revisions[parent['revision_id']] = parent
    runtime.exact_shot_revisions = {(r['shot_id'], r['revision_id']): r for r in closure['shot_revisions']}
    runtime.internal_revisions = {r['revision_id']: r for r in closure['internal_timeline_revisions']}
    snapshot = resolve_managed_render_snapshot(project_ref='demo', timeline_ref='main', expected_version=1, client=runtime)
    validate_managed_render_snapshot(snapshot)
    assert closure == original and Path(prefix + 'raw-closure.json').read_bytes() == raw_bytes
    with tempfile.TemporaryDirectory(prefix='main-image-cap-replay-', dir=Path(prefix).parent) as folder:
        root = Path(folder)
        timeline_path, registry_path, authority = materialize_managed_render_snapshot(root, snapshot)
        theme = _resolved_theme_for_render(timeline_path, None)
        timeline = _serialize_timeline(timeline_path, default_theme=str(theme['id']))
        # Exactly the normal materializer's managed-byte verification. No socket.
        with AssetMaterializer(registry_path, materialized_objects={'sha256:' + digest: image}, staging_parent=root) as assets:
            staged = {key: {'sha256': hashlib.sha256(value.local_path.read_bytes()).hexdigest(),
                            'filename': value.local_path.name} for key, value in assets.assets.items()}
            assert assets.needs_server is True
            # Freeze an explicit static-public analog URL, never pretend this
            # is an InvocationAssetServer URL or live Runtime admission.
            class StaticPublicURL:
                def local_url(self, path):
                    assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest
                    return 'image-cap.png'
            resolved_registry = assets.resolved_registry(StaticPublicURL())
        outputs = {
            'main-projected-config.json': snapshot.config,
            'main-managed-registry.json': snapshot.registry,
            'main-materialized-timeline.json': json.loads(timeline_path.read_text()),
            'main-serialized-timeline.json': timeline,
            'main-props-template.json': {'timeline': timeline, 'assets': snapshot.registry, 'theme': theme, 'review': None},
            'main-props-static-analog.json': {'timeline': timeline, 'assets': resolved_registry, 'theme': theme, 'review': None},
            'trace.json': {'raw_clip': original['internal_timeline_revisions'][0]['payload']['clips'][0],
                          'projected_clips': snapshot.config['clips'], 'serialized_clips': timeline['clips'],
                          'occurrences': snapshot.expansion['occurrences'], 'staged_assets': staged,
                          'config_hash': snapshot.config_hash,
                          'normal_helpers': ['resolve_managed_render_snapshot', '_project_exact_parent_head',
                              'project_runtime_parent_composition', '_render_compatible_projection',
                              '_normalize_pinned_element_references', '_runtime_snapshot_registry',
                              'validate_managed_render_snapshot', 'materialize_managed_render_snapshot',
                              '_resolved_theme_for_render', '_serialize_timeline / Timeline.for_render',
                              'AssetMaterializer / resolved_registry'],
                          'normal_execute_remotion_run': False,
                          'url_binding': 'static-public analog only; capture may bind real InvocationAssetServer',
                          'runtime_acceptance': False, 'pixels': False}}
        for name, value in outputs.items():
            Path(prefix + name).write_text(json.dumps(value, indent=2) + '\n')
    print(json.dumps({'raw_hold': original['internal_timeline_revisions'][0]['payload']['clips'][0]['hold'],
                      'projected_hold': snapshot.config['clips'][0]['hold'], 'serialized_hold': timeline['clips'][0]['hold'],
                      'fps': timeline['output']['fps'], 'managed_byte_sha256': digest}))


if __name__ == '__main__':
    replay(sys.argv[1])
