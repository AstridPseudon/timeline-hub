"""Diagnostic plugin only: exact current M2 serializer in held candidate tests."""
import importlib.util
import sys
from pathlib import Path


def pytest_configure(config):
    from astrid.core.timeline.banodoco_composer import TimelineRenderView
    source = Path(__file__).parent / 'current/astrid/core/timeline/banodoco_composer.py'
    spec = importlib.util.spec_from_file_location('astrid.core.timeline._restore_prior', source)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    TimelineRenderView.to_json_data = module.TimelineRenderView.to_json_data
