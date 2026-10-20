"""Runtime source admission is distinct from caller JSON and prepared file identity."""
import hashlib
import json
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from astrid.core.execution.generic_host import GenericPackHost, HostError
from astrid.core.rendering.contracts import RenderRequest
from astrid.core.rendering.errors import RendererException
from astrid.core.rendering.service import RenderService
from astrid.core.rendering.transport import _build_environment
from astrid.core.rendering.verified_source import (
    SOURCE_ENV,
    VerifiedTimelineSource,
    inherited_source,
)
from astrid.core.subprocess_env import build_child_subprocess_env
from astrid.packs.rendering.actions.render import run as facade
from astrid.packs.rendering.actions.timeline_visualize.composed_frame import _validate_capture_files
from astrid.packs.rendering.shared.rendering_backend import _serialize_timeline


def admitted(tmp_path, *, capture=False, working_copy=False, media=False, config=None):
    """A Runtime claim double; history/admission itself is not qualified here."""
    config = config or {"tracks": [{"id": "v", "kind": "visual", "label": "Visual"}], "clips": []}
    authority = {"project_id": "project", "timeline_id": "timeline", "parent_revision_id": "old-parent",
                 "parent_content_digest": "sha256:" + "a" * 64,
                 "expansion": {"shots": [{"shot_id": "shot", "revision_id": "shot-1", "content_digest": "sha256:" + "b" * 64}],
                               "children": [{"timeline_id": "internal", "revision_id": "internal-1", "config_hash": "sha256:" + "c" * 64}]}}
    snapshot = {"config": config, "registry": {"assets": {}}}
    objects = {}
    if media:
        payload = b"source media bytes"
        media_digest = hashlib.sha256(payload).hexdigest()
        objects[media_digest] = payload
        snapshot["registry"]["assets"]["image"] = {"object_id": "sha256:" + media_digest, "digest": media_digest, "type": "image/png"}
    if capture:
        snapshot["metadata"] = {"capture_authority": authority}
    else:
        authority["dependency_digests"] = [
            {"dependency_kind": "shot", "dependency_id": "shot-1", "content_digest": "sha256:" + "b" * 64},
            {"dependency_kind": "internal", "dependency_id": "internal-1", "content_digest": "sha256:" + "c" * 64}]
    ref = {"project_id": "project", "timeline_id": "timeline", "revision_id": "old-parent",
           "revision_digest": authority["parent_content_digest"], "source_kind": "revision"}
    if working_copy:
        assert capture
        marker = {"candidate_parent_revision_id": "old-parent", "candidate_digest": "sha256:" + "d" * 64,
                  "publication_digest": "sha256:" + "e" * 64,
                  "base_parent": {"revision_id": "base", "content_digest": "sha256:" + "f" * 64}}
        snapshot["metadata"]["working_copy"] = marker
        ref.update(source_kind="working_copy", revision_digest=marker["candidate_digest"], working_copy={
            "candidate_digest": marker["candidate_digest"], "publication_digest": marker["publication_digest"],
            "base_revision_id": "base", "base_revision_digest": marker["base_parent"]["content_digest"]})
    payload = json.dumps(snapshot, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(payload).hexdigest()
    objects[digest] = payload
    ref["digest"] = "sha256:" + digest
    if not capture:
        authority["snapshot_digest"] = ref["digest"]
    inputs = {"timeline_snapshot_ref": ref, "timeline_authority": authority}
    spec = {"input_object_ids": list(objects), "spec": {"inputs": inputs}}
    if capture:
        inputs.clear()
        inputs["filmstrip_authority"] = json.dumps({"capture_snapshot_ref": ref})
        spec["authority_context"] = {"capture_snapshot_ref": ref}
    host = GenericPackHost(pack_roots=[tmp_path], client=SimpleNamespace(get_object=lambda key: objects[key]))
    return host, spec, snapshot, ref


def materialize(tmp_path, monkeypatch, **kwargs):
    host, spec, snapshot, ref = admitted(tmp_path, **kwargs)
    values = host._materialize_inputs(spec, tmp_path / "attempt")
    monkeypatch.setenv(SOURCE_ENV, values.timeline_source._anchor)
    return host, spec, snapshot, ref, values


def request(values, **kwargs):
    return RenderRequest(schema_version=1, timeline_path=values["timeline"],
                         assets_registry_path=values["assets_registry"], output_name="result.mp4", **kwargs)


@pytest.mark.parametrize("capture,working_copy", [(False, False), (True, False), (True, True)])
def test_exact_reference_authority_dependencies_and_prepared_files(tmp_path, monkeypatch, capture, working_copy):
    _, _, snapshot, ref, values = materialize(tmp_path, monkeypatch, capture=capture, working_copy=working_copy, media=True)
    source = values.timeline_source
    binding = source.read()
    assert binding["ref"] == ref
    assert binding["snapshot"] == snapshot
    assert binding["authority"]["expansion"]["shots"][0]["content_digest"] == "sha256:" + "b" * 64
    assert binding["authority"]["expansion"]["children"][0]["config_hash"] == "sha256:" + "c" * 64
    assert not {"verified_source", "timeline_source"}.intersection(values)
    prepared_registry = json.loads(Path(values["assets_registry"]).read_text())
    assert prepared_registry != snapshot["registry"]
    assert Path(prepared_registry["assets"]["image"]["file"]).read_bytes() == b"source media bytes"
    parsed = request(values)
    assert parsed.verified_source == source
    assert RenderRequest.from_dict(parsed.to_dict()).for_backend("rendering.remotion").verified_source == source
    assert "verified_source" not in parsed.to_dict()
    if capture:
        _validate_capture_files(snapshot, Path(values["timeline"]), Path(values["assets_registry"]))


@pytest.mark.parametrize("port", ["inputs", "params", "backend_config"])
def test_host_rejects_reserved_source_ports(tmp_path, port):
    host, spec, _, _ = admitted(tmp_path)
    if port == "backend_config":
        spec["spec"]["inputs"][port] = {"rendering.remotion": {"verified_source": {"canonical": True}}}
    else:
        spec["spec"].setdefault(port, {})["verified_source"] = True
    with pytest.raises(HostError, match="host-owned"):
        host._materialize_inputs(spec, tmp_path / "attempt")
    assert not (tmp_path / "attempt").exists()


@pytest.mark.parametrize("name", ["timeline", "assets_registry", "timeline_snapshot"])
def test_host_refuses_caller_replacement_of_verified_source(tmp_path, name):
    host, spec, _, _ = admitted(tmp_path)
    spec["spec"]["inputs"][name] = {"config": {}} if name == "timeline_snapshot" else "caller.json"
    with pytest.raises(HostError, match="caller replaced"):
        host._materialize_inputs(spec, tmp_path / "attempt")


@pytest.mark.parametrize("field,value", [("timeline_id", "foreign"), ("parent_revision_id", "newer"),
                                         ("parent_content_digest", "sha256:" + "0" * 64)])
def test_forged_authority_cannot_replace_admitted_ref(tmp_path, field, value):
    host, spec, _, _ = admitted(tmp_path)
    spec["spec"]["inputs"]["timeline_authority"][field] = value
    with pytest.raises(HostError, match="differs"):
        host._materialize_inputs(spec, tmp_path / "attempt")


def test_missing_authority_fails_closed(tmp_path):
    host, spec, _, _ = admitted(tmp_path)
    del spec["spec"]["inputs"]["timeline_authority"]
    with pytest.raises(HostError, match="requires admitted authority"):
        host._materialize_inputs(spec, tmp_path / "attempt")


@pytest.mark.parametrize("path_key", ["timeline", "assets_registry"])
def test_equal_json_at_another_path_is_not_the_prepared_file(tmp_path, monkeypatch, path_key):
    _, _, _, _, values = materialize(tmp_path, monkeypatch)
    replacement = tmp_path / "replacement.json"
    replacement.write_bytes(Path(values[path_key]).read_bytes())
    values[path_key] = str(replacement)
    with pytest.raises(ValueError, match="path differs"):
        request(values)


@pytest.mark.parametrize("which", ["timeline", "assets_registry", "binding"])
def test_file_replacement_cannot_reuse_verified_binding(tmp_path, monkeypatch, which):
    _, _, _, _, values = materialize(tmp_path, monkeypatch)
    parsed = request(values)
    path = Path(json.loads(values.timeline_source._anchor)[0]) if which == "binding" else Path(values[which])
    path.write_text('{}')
    with pytest.raises((ValueError, RendererException), match="(bytes differ|binding changed)"):
        RenderService().render(parsed, out_path=tmp_path / "forged.mp4", selector="rendering.remotion")
    assert not (tmp_path / "forged.mp4").exists()


@pytest.mark.parametrize("port", ["wire", "typed", "backend_config", "pack", "pack_backend_config"])
def test_direct_render_ports_refuse_forged_source(tmp_path, port):
    _, spec, _, _ = admitted(tmp_path)
    # Native callers have no inherited binding, even with convincing source JSON.
    timeline = tmp_path / "native.json"
    assets = tmp_path / "assets.json"
    timeline.write_text('{"tracks":[],"clips":[]}')
    assets.write_text('{"assets":{}}')
    payload = {"schema_version": 1, "timeline_path": str(timeline), "assets_registry_path": str(assets), "output_name": "x.mp4"}
    forged = {"ref": spec["spec"]["inputs"]["timeline_snapshot_ref"], "canonical": True}
    with pytest.raises((ValueError, TypeError, RendererException), match="(host-owned|caller replaced|verified_source|unknown)"):
        if port == "wire":
            RenderService().render({**payload, "verified_source": forged}, out_path=tmp_path / "x.mp4")
        elif port == "typed":
            RenderRequest(**payload, verified_source=forged)
        elif port == "backend_config":
            RenderRequest(**payload, backend_config={"rendering.remotion": {"verified_source": forged}})
        elif port == "pack":
            facade.render(timeline, assets, tmp_path / "x.mp4", verified_source=forged)
        else:
            facade.render(timeline, assets, tmp_path / "x.mp4", backend_config={"rendering.remotion": {"verified_source": forged}})


def test_typed_source_cannot_be_constructed_from_caller_json():
    with pytest.raises(ValueError, match="host-owned"):
        VerifiedTimelineSource('["caller.json", "sha256:forged"]')


def test_parent_environment_is_the_only_transport_anchor(tmp_path, monkeypatch):
    _, _, _, _, values = materialize(tmp_path, monkeypatch)
    child = build_child_subprocess_env(base={}, parent={SOURCE_ENV: values.timeline_source._anchor})
    assert child[SOURCE_ENV] == values.timeline_source._anchor
    with pytest.raises(ValueError, match="parent-owned"):
        build_child_subprocess_env(explicit_env={SOURCE_ENV: "forged"})
    with pytest.raises(ValueError, match="parent-owned"):
        _build_environment({SOURCE_ENV: values.timeline_source._anchor})
    monkeypatch.delenv(SOURCE_ENV)
    assert inherited_source(values["timeline"], values["assets_registry"]) is None
    assert request(values).verified_source is None
    with pytest.raises(ValueError, match="caller replaced"):
        replace(request(values), verified_source=values.timeline_source)


def test_pack_authority_replacement_is_refused_before_service(tmp_path, monkeypatch):
    _, _, _, _, values = materialize(tmp_path, monkeypatch)
    service = Mock()
    monkeypatch.setattr(facade, "_default_service", lambda: service)
    with pytest.raises(ValueError, match="authority differs"):
        facade.render(Path(values["timeline"]), Path(values["assets_registry"]), tmp_path / "x.mp4",
                      timeline_authority={"parent_revision_id": "newer"})
    service.render.assert_not_called()


def test_capture_replacement_uses_same_binding(tmp_path, monkeypatch):
    _, _, snapshot, _, values = materialize(tmp_path, monkeypatch, capture=True)
    for key in ("config", "registry", "metadata"):
        forged = deepcopy(snapshot)
        forged[key] = {"forged": True}
        with pytest.raises(ValueError, match="capture .*differs"):
            _validate_capture_files(forged, Path(values["timeline"]), Path(values["assets_registry"]))


@pytest.mark.parametrize("key,value", [("hold", True), ("duration", 2.0)])
def test_capture_replacement_is_exact_across_bool_and_numeric_encoding(tmp_path, monkeypatch, key, value):
    config = {"tracks": [], "clips": [], "hold": 1, "duration": 2}
    _, _, snapshot, _, values = materialize(tmp_path, monkeypatch, capture=True, config=config)
    forged = deepcopy(snapshot)
    forged["config"][key] = value
    assert forged["config"] == snapshot["config"]  # equal to Python, different on the wire
    with pytest.raises(ValueError, match="capture .*differs"):
        _validate_capture_files(forged, Path(values["timeline"]), Path(values["assets_registry"]))


def test_caller_labels_clip_shape_and_backend_toggles_never_select_canonical(tmp_path, monkeypatch):
    _, _, _, _, values = materialize(tmp_path, monkeypatch)
    monkeypatch.delenv(SOURCE_ENV)
    config = {"tracks": [{"id": "v", "kind": "visual", "label": "Visual"}], "clips": [{
        "id": "a", "clipType": "text", "track": "v", "text": {"content": "first"}, "at": 0, "hold": .2,
        "transition": {"id": "fade", "durationFrames": 100},
        "shot_occurrence_id": "occurrence", "app": {"canonical_source": True}}],
        "app": {"canonical_source": True, "transition_policy": "incoming"}}
    config['clips'].append({'id': 'next', 'track': 'v', 'at': .2, 'hold': 1})
    Path(values["timeline"]).write_text(json.dumps(config))
    native = request(values, backend_config={"rendering.remotion": {"canonical": True, "transition_policy": "incoming"}},
                     metadata={"snapshot_label": "canonical"})
    assert native.verified_source is None
    with pytest.raises(ValueError, match="(next|successor|transition)"):
        _serialize_timeline(Path(values["timeline"]))


def test_host_action_service_and_backend_subprocesses_keep_one_binding(tmp_path, monkeypatch):
    """Real process transports and facade; the backend is a metadata probe."""
    from astrid.core.foundation.paths import REPO_ROOT
    from tests.test_generic_host import _write_manifest

    host, spec, snapshot, ref = admitted(tmp_path)
    values = host._materialize_inputs(spec, tmp_path / "attempt")
    pack = tmp_path / "probe"
    manifest_path = _write_manifest(pack)
    backend = pack / "backend.py"
    backend.write_text(f"import sys; sys.path.insert(0, {str(REPO_ROOT)!r})\n" + '''
import argparse, json, os
from pathlib import Path
from astrid.core.rendering.contracts import SupportReport
from astrid.packs.rendering.rendering.renderers.remotion.run import _load_request
p = argparse.ArgumentParser()
p.add_argument('verb'); p.add_argument('--request'); p.add_argument('--result')
a = p.parse_args()
r = _load_request(Path(a.request))
assert r.verified_source is not None
Path(a.result).write_text(json.dumps(SupportReport(schema_version=1,
    backend='rendering.remotion', backend_version='1.0.0', supported=True,
    reasons=[], alternatives=[], features={'binding': json.dumps(r.verified_source.read()), 'backend_pid': str(os.getpid())}).to_dict()))
''')
    action = pack / "action.py"
    action.write_text('''
import json, os, sys
from pathlib import Path
from types import SimpleNamespace
from astrid.core.rendering.registry import RendererRegistry, PlannerRegistry, FinalizerRegistry
from astrid.core.rendering.service import RenderService
from astrid.packs.rendering.actions.render import run as facade

timeline, assets, authority_file, output = sys.argv[1:]
authority = json.loads(Path(authority_file).read_text())
class ProbeService:
    def render(self, request, **kwargs):
        assert request.verified_source is not None
        service = RenderService(registries=(RendererRegistry(), PlannerRegistry(), FinalizerRegistry()))
        candidate = SimpleNamespace(id='rendering.remotion', pack_root=Path(__file__).parent,
            manifest=SimpleNamespace(command=(sys.executable, str(Path(__file__).with_name('backend.py'))),
                timeout_seconds=30, required_binaries=()))
        workspace = Path(output) / 'service'
        workspace.mkdir()
        result = service._run_command(candidate, 'support', request, workspace=workspace)
        assert json.loads(result.features['binding']) == request.verified_source.read()
        dest = Path(output) / 'probe.mp4'
        dest.write_text(json.dumps({**result.features, 'binding': json.loads(result.features['binding']), 'action_pid': os.getpid()}))
        Path(str(dest) + '.provenance.json').write_text('{}')
        return dest
facade._default_service = ProbeService
facade.render(Path(timeline), Path(assets), Path(output) / 'probe.mp4',
              timeline_authority=authority)
''')
    manifest = json.loads(manifest_path.read_text())
    manifest['command']['argv'] = ['{python_exec}', str(action), '{timeline}', '{assets_registry}', '{timeline_authority}', '{out}']
    manifest['inputs'] = [{'name': name, 'type': kind, 'required': True} for name, kind in
                          [('timeline', 'file'), ('assets_registry', 'file'), ('timeline_authority', 'json')]]
    manifest['outputs'] = [{'name': 'probe', 'type': 'file', 'path_template': '{out}/probe.mp4'}]
    manifest_path.write_text(json.dumps(manifest))
    # This probe capability reads only the already-materialized snapshot;
    # it receives no Runtime credential and launches no socket/browser.
    host.discover()
    output = tmp_path / 'attempt/outputs'
    output.mkdir()
    monkeypatch.setenv(SOURCE_ENV, 'ambient-forgery')
    host._run_command_definition(host.capabilities['test.echo'], values, output, tmp_path / 'attempt',
                                 allow_runtime_connection=False)
    result = json.loads((output / 'probe.mp4').read_text())
    assert result['binding']['ref'] == ref
    assert result['binding']['snapshot'] == snapshot
    assert result['action_pid'] != result['backend_pid']
    assert result['action_pid'] != __import__('os').getpid()
    assert json.loads((output / 'probe.mp4.provenance.json').read_text())['canonical_timeline'] == spec['spec']['inputs']['timeline_authority']


def test_runtime_snapshot_digest_is_not_a_requested_revision_label(tmp_path):
    host, spec, _, _ = admitted(tmp_path)
    spec['spec']['inputs']['timeline_authority']['snapshot_digest'] = 'sha256:' + '0' * 64
    with pytest.raises(HostError, match='snapshot digest differs'):
        host._materialize_inputs(spec, tmp_path / 'attempt')


def test_render_cannot_lose_authority_after_request_construction(tmp_path, monkeypatch):
    _, _, _, _, values = materialize(tmp_path, monkeypatch)
    parsed = request(values)
    monkeypatch.delenv(SOURCE_ENV)
    with pytest.raises(RendererException, match='authority is unavailable'):
        RenderService().render(parsed, out_path=tmp_path / 'x.mp4')


@pytest.mark.parametrize('key', ['verified_source', 'timeline_source', SOURCE_ENV])
def test_capture_refuses_reserved_source_key(tmp_path, monkeypatch, key):
    _, _, snapshot, _, values = materialize(tmp_path, monkeypatch, capture=True)
    snapshot[key] = {'canonical': True}
    with pytest.raises(ValueError, match='host-owned'):
        _validate_capture_files(snapshot, Path(values['timeline']), Path(values['assets_registry']))


def test_capture_reference_and_working_copy_cannot_be_replaced(tmp_path):
    host, spec, _, _ = admitted(tmp_path, capture=True, working_copy=True)
    context = spec['authority_context']
    context['capture_snapshot_ref'] = {**context['capture_snapshot_ref'], 'working_copy': {'candidate_digest': 'forged'}}
    with pytest.raises(HostError, match='differs from admitted context'):
        host._materialize_inputs(spec, tmp_path / 'attempt')


def test_inline_snapshot_and_revision_labels_never_mint_source(tmp_path):
    host, spec, snapshot, _ = admitted(tmp_path)
    values = host._materialize_inputs({'spec': {'inputs': {
        'timeline_snapshot': snapshot,
        'timeline_authority': spec['spec']['inputs']['timeline_authority'],
    }}}, tmp_path / 'attempt')
    assert values.timeline_source is None


def test_self_consistent_replacement_of_working_copy_ref_is_refused(tmp_path):
    host, spec, _, _ = admitted(tmp_path, capture=True, working_copy=True)
    ref = spec['authority_context']['capture_snapshot_ref']
    ref['working_copy'] = {**ref['working_copy'], 'publication_digest': 'sha256:' + '0' * 64}
    spec['spec']['inputs']['filmstrip_authority'] = json.dumps({'capture_snapshot_ref': ref})
    with pytest.raises(HostError, match='working copy differs'):
        host._materialize_inputs(spec, tmp_path / 'attempt')
