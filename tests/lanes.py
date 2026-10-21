"""Test lanes (testing plan R-2).

Lanes. The default run deselects tests marked ``integration``, ``darwin_native``,
``live`` or ``opt_in`` (see ``addopts`` in pyproject.toml). The heavy lane is exactly those:
``pytest -m "integration or darwin_native or live or opt_in"`` (no workflow schedules it yet; see the
testing plan's Owned debt). Together the two lanes are the whole suite, by construction. A
``darwin_native`` test is skipped off macOS.

Skips on import (testing plan R-6). ``pytest.importorskip`` is allowed locally but fails in a required
lane, where a skip would hide a broken install: any lane run by CI (``CI`` set) and any run that selects
the ``integration`` tests. A declared dev dependency is imported plainly. A module only the integration
lane provides (a second checkout or an optional library) is loaded with ``require_module``: it fails in a
lane that runs integration tests and skips the module in the default lane, which deselects every test that
needs it. A fixture that needs a second checkout is named in its module's ``INTEGRATION_FIXTURES``: every test
that requests it is an ``integration`` test, so the default lane deselects it instead of skipping it, and the
fixture calls ``unavailable`` when the checkout is missing.

Leaked file descriptors (testing plan LEAK.2). The run fails if the pytest process
ends holding more than FD_LEAK_ALLOWANCE descriptors beyond what it held at start.
(Leaked daemon and host process groups are caught by conftest's session guard.)
"""

from __future__ import annotations

import importlib
import os
import sys
from types import ModuleType
from typing import NoReturn

import pytest

FD_LEAK_ALLOWANCE = 64
LANE_MARKERS = {
    "integration": "needs a long-lived subprocess, Node, ffmpeg, the network, or a second checkout",
    "darwin_native": "needs native macOS APIs; skipped elsewhere",
    "live": "needs real provider credentials",
    "opt_in": "explicitly opt-in; never in the default lane",
    "posix_native": "needs POSIX-only process or file descriptor APIs",
}


def _open_fds() -> int | None:
    for directory in ("/proc/self/fd", "/dev/fd"):
        try:
            return len(os.listdir(directory))
        except OSError:
            continue
    return None


class _FdGuard:
    def __init__(self) -> None:
        self.start = _open_fds()

    @pytest.hookimpl(trylast=True)
    def pytest_sessionfinish(self, session, exitstatus):
        end = _open_fds()
        if self.start is None or end is None or end - self.start <= FD_LEAK_ALLOWANCE:
            return
        reporter = session.config.pluginmanager.get_plugin("terminalreporter")
        if reporter is not None:
            reporter.write_line(f"ERROR: the test session leaked {end - self.start} file descriptors ({self.start} -> {end})")
        session.exitstatus = pytest.ExitCode.TESTS_FAILED


IMPORT_SKIP = "could not import"
_config = None


def runs_integration(config) -> bool:
    """True when the run selects the ``integration`` tests with a marker expression (the heavy lane, run on request)."""
    expression = (config.getoption("markexpr", default="") or "").strip()
    return "integration" in expression and "not integration" not in expression


def in_required_lane(config) -> bool:
    return bool(os.environ.get("CI")) or runs_integration(config)


def require_module(name: str) -> ModuleType:
    """Import a module that only the integration lane provides (a second checkout or an optional library)."""
    try:
        return importlib.import_module(name)
    except ImportError:
        if _config is None or runs_integration(_config):
            raise
        pytest.skip(f"{name} is not installed; the tests that need it run in the integration lane", allow_module_level=True)


def unavailable(message: str) -> NoReturn:
    """A second checkout is missing: fail in a lane that runs integration tests, skip the module elsewhere."""
    if _config is None or runs_integration(_config):
        pytest.fail(message, pytrace=False)
    pytest.skip(message, allow_module_level=True)


class _ImportSkipGuard:
    """Turn a skip on import into a failure in a required lane (R-6)."""

    @staticmethod
    def _fail(config, report) -> None:
        reason = report.longrepr[2] if isinstance(report.longrepr, tuple) and len(report.longrepr) == 3 else ""
        if report.skipped and IMPORT_SKIP in str(reason) and in_required_lane(config):
            report.outcome = "failed"
            report.longrepr = f"{reason}\nA skip on import hides a broken install. Import a declared dependency plainly; load an integration-lane module with tests.lanes.require_module (testing plan R-6)."

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        outcome = yield
        self._fail(item.config, outcome.get_result())

    @pytest.hookimpl(hookwrapper=True)
    def pytest_make_collect_report(self, collector):
        outcome = yield
        self._fail(collector.config, outcome.get_result())


def pytest_configure(config):
    global _config
    _config = config
    for name, meaning in LANE_MARKERS.items():
        config.addinivalue_line("markers", f"{name}: {meaning}")
    config.pluginmanager.register(_FdGuard(), "fd-leak-guard")
    config.pluginmanager.register(_ImportSkipGuard(), "import-skip-guard")


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config, items):
    for item in items:
        needs_checkout = set(getattr(getattr(item, "module", None), "INTEGRATION_FIXTURES", ()))
        if needs_checkout & set(getattr(item, "fixturenames", ())):
            item.add_marker(pytest.mark.integration)
        if sys.platform != "darwin" and item.get_closest_marker("darwin_native"):
            item.add_marker(pytest.mark.skip(reason="darwin_native: needs macOS"))
        if os.name != "posix" and item.get_closest_marker("posix_native"):
            item.add_marker(pytest.mark.skip(reason="posix_native: needs POSIX process or descriptor APIs"))
