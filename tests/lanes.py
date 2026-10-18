"""Test lanes and the known-failures list (testing plan, R-2 and R-6).

Lanes. The default run deselects tests marked ``integration``, ``darwin_native``,
``live`` or ``opt_in`` (see ``addopts`` in pyproject.toml). The nightly lane runs exactly
those: ``pytest -m "integration or darwin_native or live or opt_in"``. Together the two lanes are the
whole suite, by construction. A ``darwin_native`` test is skipped off macOS.

Known failures. ``tests/known_failures.txt`` has one line per known red test::

    <node id> | <owner> | <expires YYYY-MM-DD> | <reason>

Each listed test runs as a strict xfail, so it must still fail: once it is fixed the
run fails until its line is removed. A reason that starts with ``flaky:`` names an
intermittent product race; that test runs as a non-strict xfail, so either outcome passes. An expired line, or one whose file is collected
whole but whose test no longer exists, fails the run. The list can only shrink.

Skips on import (testing plan R-6). ``pytest.importorskip`` is allowed locally but fails in a required
lane, where a skip would hide a broken install: any lane run by CI (``CI`` set) and any run that selects
the ``integration`` tests. A declared dev dependency is imported plainly. A module only the integration
lane provides (a second checkout or an optional library) is loaded with ``require_module``: it fails in a
lane that runs integration tests and skips the module in the default lane, which deselects every test that
needs it.

Leaked file descriptors (testing plan LEAK.2). The run fails if the pytest process
ends holding more than FD_LEAK_ALLOWANCE descriptors beyond what it held at start.
(Leaked daemon and host process groups are caught by conftest's session guard.)
"""

from __future__ import annotations

import datetime as _dt
import importlib
import os
import sys
from pathlib import Path
from types import ModuleType
from typing import NoReturn

import pytest

KNOWN_FAILURES = Path(__file__).with_name("known_failures.txt")
FD_LEAK_ALLOWANCE = 64
LANE_MARKERS = {
    "integration": "needs a long-lived subprocess, Node, ffmpeg, the network, or a second checkout",
    "darwin_native": "needs native macOS APIs; skipped elsewhere",
    "live": "needs real provider credentials",
    "opt_in": "explicitly opt-in; never in the default lane",
}


def read_known_failures(path: Path = KNOWN_FAILURES) -> dict[str, dict[str, str]]:
    entries: dict[str, dict[str, str]] = {}
    if not path.is_file():
        return entries
    for number, raw in enumerate(path.read_text().splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        fields = [field.strip() for field in line.split("|")]
        if len(fields) != 4 or not all(fields):
            raise pytest.UsageError(f"{path.name}:{number}: expected '<node id> | <owner> | <expires> | <reason>'")
        node_id, owner, expires, reason = fields
        try:
            _dt.date.fromisoformat(expires)
        except ValueError as exc:
            raise pytest.UsageError(f"{path.name}:{number}: bad expiry {expires!r}") from exc
        entries[node_id] = {"owner": owner, "expires": expires, "reason": reason}
    return entries


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
# Private packages no index CI can reach provides; their tests skip on import until the runpod lane is
# decided (testing plan, Owned debt). This list can only shrink.
PRIVATE_MODULES = ("runpod_lifecycle",)
_config = None


def runs_integration(config) -> bool:
    """True when the run selects the ``integration`` tests with a marker expression (the nightly lane)."""
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
        if report.skipped and IMPORT_SKIP in str(reason) and not any(name in str(reason) for name in PRIVATE_MODULES) and in_required_lane(config):
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


def _narrowed_files(config) -> set[str]:
    narrowed = set()
    for arg in config.args:
        path, separator, _ = arg.partition("::")
        if separator:
            try:
                narrowed.add(Path(path).resolve().relative_to(config.rootpath).as_posix())
            except ValueError:
                continue
    return narrowed


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config, items):
    entries = read_known_failures()
    today = _dt.date.today().isoformat()
    expired = [node for node, entry in entries.items() if entry["expires"] < today]
    if expired:
        raise pytest.UsageError(f"{KNOWN_FAILURES.name}: expired entries must be fixed or renewed: {expired}")
    # A file counts only when it was collected whole (not narrowed with "file::test" on the command line).
    collected_files = {item.nodeid.split("::", 1)[0] for item in items} - _narrowed_files(config)
    collected = {item.nodeid for item in items}
    stale = [node for node in entries if node.split("::", 1)[0] in collected_files and node not in collected]
    if stale:
        raise pytest.UsageError(f"{KNOWN_FAILURES.name}: entries name no collected test: {stale}")
    for item in items:
        entry = entries.get(item.nodeid)
        if entry is not None:
            strict = not entry["reason"].startswith("flaky:")
            item.add_marker(pytest.mark.xfail(strict=strict, reason=f"known failure ({entry['owner']}, until {entry['expires']}): {entry['reason']}"))
        if sys.platform != "darwin" and item.get_closest_marker("darwin_native"):
            item.add_marker(pytest.mark.skip(reason="darwin_native: needs macOS"))
