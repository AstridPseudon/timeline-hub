"""Test lanes and the known-failures list (testing plan, R-2 and R-6).

Lanes. The default run deselects tests marked ``integration``, ``darwin_native`` or
``live`` (see ``addopts`` in pyproject.toml). The nightly lane runs exactly those:
``pytest -m "integration or darwin_native or live"``. Together the two lanes are the
whole suite, by construction. A ``darwin_native`` test is skipped off macOS.

Known failures. ``tests/known_failures.txt`` has one line per known red test::

    <node id> | <owner> | <expires YYYY-MM-DD> | <reason>

Each listed test runs as a strict xfail, so it must still fail: once it is fixed the
run fails until its line is removed. An expired line, or one whose file is collected
whole but whose test no longer exists, fails the run. The list can only shrink.

Leaked file descriptors (testing plan LEAK.2). The run fails if the pytest process
ends holding more than FD_LEAK_ALLOWANCE descriptors beyond what it held at start.
(Leaked daemon and host process groups are caught by conftest's session guard.)
"""

from __future__ import annotations

import datetime as _dt
import os
import sys
from pathlib import Path

import pytest

KNOWN_FAILURES = Path(__file__).with_name("known_failures.txt")
FD_LEAK_ALLOWANCE = 64
LANE_MARKERS = {
    "integration": "needs a long-lived subprocess, Node, ffmpeg, the network, or a second checkout",
    "darwin_native": "needs native macOS APIs; skipped elsewhere",
    "live": "needs real provider credentials",
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


def pytest_configure(config):
    for name, meaning in LANE_MARKERS.items():
        config.addinivalue_line("markers", f"{name}: {meaning}")
    config.pluginmanager.register(_FdGuard(), "fd-leak-guard")


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
            item.add_marker(pytest.mark.xfail(strict=True, reason=f"known failure ({entry['owner']}, until {entry['expires']}): {entry['reason']}"))
        if sys.platform != "darwin" and item.get_closest_marker("darwin_native"):
            item.add_marker(pytest.mark.skip(reason="darwin_native: needs macOS"))
