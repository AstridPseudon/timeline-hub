"""Reproduce the real Scene preparation refusal and qualify the owner overlay.

Only the proposed host materialization method is overlaid. Source minting,
child inheritance and AssetMaterializer integrity checks remain production code.
"""
import hashlib
import inspect
import json
import os
import subprocess
import sys
import textwrap
from copy import deepcopy
from pathlib import Path
from types import MethodType

import pytest

from astrid.core.execution import generic_host
from astrid.core.rendering.verified_source import PreparedTimelineInputs
from scripts.run_scene_only_central import _apply_private_registry_digest_patch
from tests.packs.rendering.test_verified_source import admitted


def _materialize(tmp_path, *, corrected):
    host, spec, snapshot, ref = admitted(tmp_path, capture=True, media=True)
    media_id = snapshot['registry']['assets']['image']['object_id']
    snapshot['registry']['assets']['image'] = {'media_id': media_id, 'type': 'image'}
    payload = json.dumps(snapshot, sort_keys=True, separators=(',', ':')).encode()
    snapshot_digest = hashlib.sha256(payload).hexdigest()
    original_fetch = host.client.get_object
    host.client.get_object = lambda key: payload if key == snapshot_digest else original_fetch(key)
    spec['input_object_ids'].append(snapshot_digest)
    ref['digest'] = 'sha256:' + snapshot_digest
    spec['spec']['inputs']['filmstrip_authority'] = json.dumps({'capture_snapshot_ref': ref})
    original = deepcopy(snapshot)
    if corrected:
        method = textwrap.dedent(inspect.getsource(generic_host.GenericPackHost._materialize_inputs))
        # The helper matches the full file's indentation, so wrap the method
        # in its class indentation before applying the exact one-line patch.
        patched = _apply_private_registry_digest_patch(textwrap.indent(method, '    ').encode())
        namespace = {}
        exec(compile(textwrap.dedent(patched.decode()), '<private-owner-overlay>', 'exec'),
             vars(generic_host), namespace)
        host._materialize_inputs = MethodType(namespace['_materialize_inputs'], host)
    values = host._materialize_inputs(spec, tmp_path / 'attempt')
    assert snapshot == original
    assert values.timeline_source.read()['snapshot'] == original
    return values


@pytest.mark.parametrize('corrected', [False, True])
@pytest.mark.parametrize('tampered', ['none', 'registry', 'object'])
def test_content_addressed_source_survives_real_child_materialization(tmp_path, corrected, tampered):
    values = _materialize(tmp_path, corrected=corrected)
    env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}
    PreparedTimelineInputs.handoff_source(values, env)
    if tampered == 'registry':
        # Same path, different bytes: the retained source stays strictly bound.
        with open(values['assets_registry'], 'a') as stream:
            stream.write(' ')
    elif tampered == 'object':
        Path(next(iter(values['materialized_objects'].values()))).write_bytes(b'replaced bytes')
    code = '''
import json, sys
from pathlib import Path
from astrid.core.rendering.verified_source import inherited_source, VerifiedTimelineSource
from astrid.core.rendering.assets import AssetMaterializer
values = json.loads(sys.argv[1])
try:
    source = inherited_source(values['timeline'], values['assets_registry'])
    assert type(source) is VerifiedTimelineSource
    with AssetMaterializer(values['assets_registry'], materialized_root=values['materialized_root'],
                           materialized_objects=values['materialized_objects'],
                           allow_derived_files=True, reuse_materialized_paths=True) as assets:
        assert assets.assets['image'].local_path.read_bytes() == b'source media bytes'
    source.validate(values['timeline'], values['assets_registry'])
except ValueError as exc:
    print(str(exc))
    sys.exit(2)
print('exact source and managed bytes preserved')
'''
    child = subprocess.run([sys.executable, '-B', '-c', code, json.dumps(values)],
                           env=env, capture_output=True, text=True, check=False)
    if tampered == 'registry':
        assert child.returncode == 2, child.stderr
        assert child.stdout.strip() == 'verified source prepared registry bytes differ'
    elif corrected and tampered == 'object':
        assert child.returncode == 2, child.stderr
        assert child.stdout.strip() == "Asset 'image' managed object failed integrity check"
    elif corrected:
        assert child.returncode == 0, child.stderr
        assert child.stdout.strip() == 'exact source and managed bytes preserved'
    else:
        assert child.returncode == 2, child.stderr
        assert child.stdout.strip() == "Asset 'image' requires a runtime-managed digest"


def test_private_project_keeps_the_native_pack_alias_source(tmp_path, monkeypatch):
    from scripts import run_scene_only_central as central

    repo = tmp_path / 'agent-overlay'
    remotion = repo / 'remotion'
    artifacts = remotion / 'artifacts'
    artifacts.mkdir(parents=True)
    import shutil

    root = Path(__file__).resolve().parents[3]
    shutil.copyfile(root / 'remotion/webpack-alias.mjs', remotion / 'webpack-alias.mjs')
    shutil.copyfile(root / 'remotion/artifacts' / central.PUBLIC13_NAME,
                    artifacts / central.PUBLIC13_NAME)
    peers = tmp_path / 'read-only-peers'
    peers.mkdir()
    monkeypatch.setattr(central, 'PEERS', peers)
    pack = repo / 'astrid/packs/probe'
    (pack / 'effects/box').mkdir(parents=True)
    (pack / 'pack.json').write_text(json.dumps({'id': 'probe', 'rendering': {
        'effects/box': {'type': 'element', 'path': 'effects/box/element.yaml'},
    }}))
    project = central._project(repo, tmp_path)
    script = """
import {remotionPrimitiveAliasesFor} from './webpack-alias.mjs';
const aliases = remotionPrimitiveAliasesFor(process.cwd())({}).resolve.alias;
console.log(JSON.stringify(aliases));
"""
    child_env = {key: value for key, value in os.environ.items()
                 if key not in {'NODE_OPTIONS', 'NODE_PATH', 'ASTRID_PACKS_PATH'}}
    result = subprocess.run([str(central.NODE_PIN), '--input-type=module', '-e', script],
                            cwd=project, env=child_env, capture_output=True, text=True, check=True)
    aliases = json.loads(result.stdout)
    assert aliases['@pack-probe-elements-effects'] == str(pack / 'effects')
    detached = tmp_path / 'detached/remotion'
    detached.mkdir(parents=True)
    shutil.copyfile(remotion / 'webpack-alias.mjs', detached / 'webpack-alias.mjs')
    counterexample = subprocess.run([str(central.NODE_PIN), '--input-type=module', '-e', script],
                                    cwd=detached, env=child_env, capture_output=True,
                                    text=True, check=True)
    assert '@pack-probe-elements-effects' not in json.loads(counterexample.stdout)
    assert project == repo / 'remotion'
    assert (project / 'node_modules/@banodoco').is_dir()
    assert not (project / 'node_modules/@banodoco').is_symlink()


@pytest.mark.integration
def test_private_candidate_changes_a_real_authored_clip(tmp_path):
    from types import SimpleNamespace

    from tests.helpers.runtime import use_runtime
    from tests.packs.rendering.test_live_scene_only_managed_carrier import (
        _candidate_preview,
        _seed,
    )

    use_runtime()
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore

    from astrid.sdk.timeline_filmstrip import _scene_only_request

    realm = tmp_path / 'realm'
    RealmStore.initialize(realm).close()
    service = RuntimeService(realm)
    try:
        runtime = _seed(SimpleNamespace(service=service))
        _, saved = _scene_only_request({'timeline_ref': 'main', 'revision_id': 'scene-parent-1'},
                                       project=runtime.project_id, client=runtime)
        preview = _candidate_preview(runtime)
        _, candidate = _scene_only_request({'timeline_ref': 'main', 'authoring_preview': preview},
                                           project=runtime.project_id, client=runtime)
        assert candidate['capture_identity'] != saved['capture_identity']
        snapshot = candidate['capture_snapshot']
        assert snapshot['metadata']['working_copy']['base_parent']['revision_id'] == 'scene-parent-1'
        clip = next(row for row in snapshot['config']['clips'] if row['id'] == 'direct')
        assert clip['opacity'] == 0.5
        assert 'opacity' not in saved['capture_snapshot']['config']['clips'][0]
    finally:
        service.close()
