import importlib.util
import sys
from pathlib import Path

import pytest

prefix = Path(__file__).with_name("handoff-vw-m3-current-pre-tail-positive-fix")
mode = sys.argv[1]

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

class Sources:
    def pytest_collection_modifyitems(self, items):
        modules = {item.module for item in items}
        for module in modules:
            if mode == "oldgreen":
                module.RenderService = load(
                    "astrid.core.rendering.pre_tail_old_service", f"{prefix}-old-service.py"
                ).RenderService
                module.remotion = load(
                    "astrid.packs.rendering.rendering.renderers.remotion.pre_tail_old_run",
                    f"{prefix}-old-run.py",
                )
                module._ROOT_TSX = Path(f"{prefix}-old-Root.tsx")
            else:
                module.remotion = load(
                    "astrid.packs.rendering.rendering.renderers.remotion.pre_tail_before_run",
                    f"{prefix}-before-run.py",
                )
                module._ROOT_TSX = Path(f"{prefix}-before-Root.tsx")

selection = "legacy_service" if mode == "oldgreen" else "fully_covered"
raise SystemExit(pytest.main([
    "-q", "-p", "no:cacheprovider",
    "tests/packs/rendering/test_remotion_layer_tail_compat.py", "-k", selection,
], plugins=[Sources()]))
