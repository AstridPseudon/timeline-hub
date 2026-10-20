"""Compare the original service method with its extracted implementation."""
import ast
import copy
import hashlib
import importlib.util
import itertools
import json
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

from astrid.core.rendering.contracts import SCHEMA_VERSION, FrameWindow, RenderRequest
from astrid.core.rendering.service import RenderService
from tests.packs.rendering.test_live_scene_boundary import _package
from tests.packs.rendering.test_live_scene_composition import _composition, _request

PREFIX = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-service-window-source-extract-')
name = 'astrid.core.rendering._window_inputs_before'
spec = importlib.util.spec_from_file_location(name, str(PREFIX) + 'before.py')
before = importlib.util.module_from_spec(spec)
sys.modules[name] = before
spec.loader.exec_module(before)
old = ast.parse(Path(str(PREFIX) + 'before.py').read_text())
new = ast.parse(Path('astrid/core/rendering/window_inputs.py').read_text())
old_method = next(node for node in ast.walk(old) if isinstance(node, ast.FunctionDef) and node.name == '_segment_request')
new_func = next(node for node in new.body if isinstance(node, ast.FunctionDef))
# The moved executable body must be identical after replacing the existing hook.
class Hook(ast.NodeTransformer):
    def visit_Attribute(self, node):
        if isinstance(node.value, ast.Name) and node.value.id == 'self' and node.attr == '_window_timeline':
            return ast.copy_location(ast.Name(id='slice_timeline', ctx=ast.Load()), node)
        return self.generic_visit(node)
assert ast.dump(Hook().visit(ast.Module(body=old_method.body[1:], type_ignores=[]))) == ast.dump(ast.Module(body=new_func.body[1:], type_ignores=[]))
rows = []
with tempfile.TemporaryDirectory(prefix='window-input-identity-') as directory:
    workspace = Path(directory)
    path = workspace / 'timeline.json'
    def check(label, raw, native, layer, window):
        path.write_text(json.dumps(raw))
        source = path.read_bytes()
        request = RenderRequest(SCHEMA_VERSION, str(path), 'out.mp4', window=window,
            metadata={'astrid_composition_duration_frames': '999999', 'review': '{}'})
        request_before = copy.deepcopy(request.to_dict())
        candidate = SimpleNamespace(id='fixture', manifest=SimpleNamespace(capabilities=native))
        segment = SimpleNamespace(window=window, layer=layer)
        results = []
        for service in (before.RenderService, RenderService):
            try:
                adapted, sidecar = service._segment_request(object.__new__(service), request,
                    candidate=candidate, segment=segment, index=0, workspace=workspace)
                payload = Path(adapted.timeline_path).read_bytes()
                result = {'request': adapted.to_dict(), 'sidecar': sidecar,
                    'payload_sha256': hashlib.sha256(payload).hexdigest(), 'timeline': json.loads(payload),
                    'same_request': adapted is request, 'same_window': adapted.window is request.window}
            except Exception as exc:
                result = {'error_type': type(exc).__name__, 'error': str(exc)}
            assert path.read_bytes() == source
            assert request.to_dict() == request_before
            results.append(result)
        assert results[0] == results[1], label
        # Normalize only the temporary filename in the saved diagnostic payload.
        result = json.loads(json.dumps(results[0]).replace(str(workspace), '<workspace>'))
        rows.append({'case': label, 'identical': True, **result})
    for pair, shape, trait, z in itertools.product(
        ((30, 1), (30000, 1001)), ('empty', 'sparse', 'source', 'fades'),
        ({}, {'supports_windows': True}, {'supports_windows': False}), (None, 0, 1)):
        raw = {'theme': 'banodoco-default', 'tracks': [
            {'id': key, 'kind': 'visual', 'label': key} for key in ('bottom', 'top')],
            'clips': [{'id': 'plate', 'track': 'bottom', 'asset': 'plate', 'at': 0, 'hold': 10, 'from': 0, 'to': 10}],
            'metadata': {'duration_seconds': 999, 'opaque': {'keep': [None, False]}}}
        if shape in ('sparse', 'fades'):
            raw['clips'].append({'id': 'early', 'track': 'top', 'asset': 'top', 'at': 0.016682,
                'from': 1, 'to': 10, 'speed': 1, 'params': {'fadeIn': 2, 'fadeOut': 1},
                'app': {'astrid_slice_origin': {'id': 'forged'}, 'opaque': [None, False]}})
        if shape == 'source':
            raw['tracks'].append({'id': 'reference', 'kind': 'visual', 'label': 'Reference', 'role': 'source'})
            raw['clips'].append({'id': 'reference', 'track': 'reference', 'asset': 'reference', 'at': 0, 'hold': 40})
        layer = SimpleNamespace(tracks=('top',), z=z) if z is not None else None
        check(f'{pair}/{shape}/{trait}/z={z}', raw, trait, layer, FrameWindow(150, 180, pair))
    for z in (0, 1):
        raw = _composition(_package())
        raw['clips'][0]['hold'] = 20
        layer = SimpleNamespace(tracks=('scene',), z=z)
        for native in (True, False):
            check(f'threejs/z={z}/native={native}', raw, {'supports_windows': native}, layer, _request(path).window)
    for raw in ([], {'tracks': [], 'clips': []}):
        check('invalid/' + repr(raw), raw, {'supports_windows': True}, SimpleNamespace(tracks=('top',), z=1), FrameWindow(150, 180, (30, 1)))
Path(str(PREFIX) + 'identity.json').write_text(json.dumps(rows, indent=2) + '\n')
print(f'PASS: identical moved AST; {len(rows)} before/after requests, byte payloads, hashes/errors and source immutability checks')
