from pathlib import Path
import importlib.util
import os
import sys
import pytest

P = Path(__file__).with_name('handoff-vw-m3-current-extent-landable-review')
root = Path(os.environ['REVIEW_SOURCE_ROOT'])
mode = sys.argv[1]

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

class Sources:
    def pytest_collection_modifyitems(self, items):
        for module in {item.module for item in items}:
            module._REMOTION_ROOT = root / 'remotion'
            module._ROOT_TSX = Path(str(P) + '-' + mode + '-Root.tsx')
            module.RenderService = load(
                'astrid.core.rendering.extent_review_' + mode.replace('-', '_'),
                str(P) + '-' + mode + '-service.py',
            ).RenderService
            module.remotion = load(
                'astrid.packs.rendering.rendering.renderers.remotion.extent_review_' + mode.replace('-', '_'),
                str(P) + '-' + mode + '-run.py',
            )

selection = 'legacy_service' if mode == 'old' else 'fully_covered'
raise SystemExit(pytest.main([
    '-q', '-o', 'addopts=', '-p', 'no:cacheprovider', '--tb=short',
    str(P) + '-tail-tests.py', '-k', selection,
], plugins=[Sources()]))
