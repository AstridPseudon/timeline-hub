"""Test lanes (testing plan R-2).

Lanes. The default run deselects tests marked ``integration``, ``darwin_native`` or
``live`` (see ``addopts`` in pyproject.toml). The nightly lane runs exactly those:
``pytest -m "integration or darwin_native or live"``. Together the two lanes are the
whole suite, by construction. A ``darwin_native`` test is skipped off macOS.

Leaked file descriptors (testing plan LEAK.2). The run fails if the pytest process
ends holding more than FD_LEAK_ALLOWANCE descriptors beyond what it held at start.
(Leaked daemon and host process groups are caught by conftest's session guard.)
"""

from __future__ import annotations

import os
import sys

import pytest

FD_LEAK_ALLOWANCE = 64
LANE_MARKERS = {
    "integration": "needs a long-lived subprocess, Node, ffmpeg, the network, or a second checkout",
    "darwin_native": "needs native macOS APIs; skipped elsewhere",
    "live": "needs real provider credentials",
}

# Platform-specific test lanes. Keep skip reasons here so test modules express
# the capability they require without calling pytest's skip APIs directly.
requires_posix_inherited_descriptors = pytest.mark.skipif(
    os.name == "nt", reason="relay integration requires POSIX inherited descriptors"
)
requires_posix_uid_metadata = pytest.mark.skipif(
    os.name == "nt", reason="Windows owner-only checks use profile ACLs, not POSIX uid metadata"
)
requires_posix_file_modes_native_custody = pytest.mark.skipif(
    sys.platform == "win32", reason="Windows uses profile ACLs instead of POSIX file modes"
)
requires_posix_private_modes = pytest.mark.skipif(
    sys.platform == "win32", reason="Windows uses profile ACLs rather than POSIX modes"
)
requires_windows_token_process_times = pytest.mark.skipif(
    sys.platform != "win32", reason="Windows token and process-time APIs"
)
requires_posix_process_groups = pytest.mark.skipif(
    sys.platform == "win32", reason="POSIX process group integration"
)
requires_windows_job_object = pytest.mark.skipif(
    sys.platform != "win32", reason="Windows Job Object integration"
)
requires_windows_dirfd_adapter = pytest.mark.skipif(
    os.name != "nt", reason="exercises the native Windows dir-fd adapter"
)
requires_windows_reparse_point_rejection = pytest.mark.skipif(
    os.name != "nt", reason="exercises Windows reparse-point rejection"
)
requires_windows_sqlite_backup = pytest.mark.skipif(
    os.name != "nt", reason="exercises Windows SQLite backup snapshots"
)
requires_windows_process_and_lock_apis = pytest.mark.skipif(
    os.name != "nt", reason="native Windows process and lock APIs"
)
requires_posix_owner_only_permissions = pytest.mark.skipif(
    os.name == "nt", reason="POSIX owner-only permission behavior"
)
requires_posix_process_group_id_reuse = pytest.mark.skipif(
    os.name == "nt", reason="this regression checks POSIX process group ID reuse"
)
requires_posix_fork = pytest.mark.skipif(
    os.name == "nt", reason="multiprocessing fork is unavailable on Windows"
)


def skip_windows_symlink_creation_unavailable() -> None:
    pytest.skip("symlink creation is unavailable for this Windows account")


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


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config, items):
    for item in items:
        if sys.platform != "darwin" and item.get_closest_marker("darwin_native"):
            item.add_marker(pytest.mark.skip(reason="darwin_native: needs macOS"))
