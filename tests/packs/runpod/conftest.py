"""Skip the runpod pack tests when runpod_lifecycle isn't installed, except in a required lane."""

from __future__ import annotations

import importlib.util

import pytest

from tests.lanes import in_required_lane

_RUNPOD_LIFECYCLE_AVAILABLE = importlib.util.find_spec("runpod_lifecycle") is not None
_INSTALL = 'pip install -e ".[dev]" (the dev extra pins runpod-lifecycle to a public Git revision)'

# NOTE: do NOT use pytest.importorskip at conftest module scope. When pytest
# loads a conftest during the INITIAL conftest discovery pass, a module-level
# skip/importorskip raises Skipped through the loader and aborts the whole run
# (exit 1, 0 collected) instead of skipping the pack's tests. Defer the skip to
# collection time instead.


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Skip every runpod-pack test when the dependency is absent; fail a required lane (R-6)."""
    if _RUNPOD_LIFECYCLE_AVAILABLE:
        return
    runpod_items = [item for item in items if "runpod" in str(item.path)]
    if runpod_items and in_required_lane(config):
        raise pytest.UsageError(f"runpod_lifecycle is a declared dev dependency and is not installed: {_INSTALL}")
    skip = pytest.mark.skip(reason=f"requires runpod_lifecycle: {_INSTALL}")
    for item in runpod_items:
        item.add_marker(skip)
