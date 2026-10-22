"""Test lanes (testing plan R-2).

Lanes. The default run deselects tests marked ``integration``, ``darwin_native`` or
``live`` (see ``addopts`` in pyproject.toml). ``integration`` runs in the nightly
job (and in the ``-m ""`` portability jobs), ``darwin_native`` in the ``darwin-native``
job; no test is marked ``live`` yet. A ``darwin_native`` test is skipped off macOS.

Leaked file descriptors (testing plan LEAK.2). The run fails if the pytest process
ends holding more than FD_LEAK_ALLOWANCE descriptors beyond what it held at start.
(Leaked daemon and host process groups are caught by conftest's session guard.)
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass

import pytest

FD_LEAK_ALLOWANCE = 64
LANE_MARKERS = {
    "integration": "needs a long-lived subprocess, Node, ffmpeg, the network, or a second checkout",
    "darwin_native": "needs native macOS APIs; skipped elsewhere",
    "live": "needs real provider credentials",
}

# --- The skip registry ------------------------------------------------------
# Every skip the suite may report is declared here, once, with the exact
# condition, the reason and the CI jobs that run the test where the condition
# holds. Test modules never call pytest's skip APIs (tests/test_skip_policy.py);
# they use the ``requires_*`` marks below. The guard further down fails the run
# on any skip whose reason does not carry a registered ``[declared:NAME]`` tag,
# on any xfail, and prints every skip by test name.
#
# ``ci`` lists the jobs (ci.yml / nightly.yml) in which the condition is false,
# so the test really runs. tests/test_skip_registry.py checks those jobs exist.
# ``ci=()`` would mean "manual only"; it is not used today.

UNIT_WINDOWS = ("unit", "portability-lifecycle")
UNIT_POSIX = ("unit", "portability-lifecycle")


@dataclass(frozen=True)
class DeclaredSkip:
    name: str
    skip_when: str  # the exact condition, in words and code
    reason: str
    ci: tuple[str, ...]  # jobs where the condition is false and the test runs

    @property
    def tag(self) -> str:
        return f"[declared:{self.name}]"

    def mark(self, condition: bool):
        return pytest.mark.skipif(condition, reason=f"{self.tag} {self.reason}")


SKIP_REGISTRY: dict[str, DeclaredSkip] = {}


def _declare(name: str, skip_when: str, reason: str, ci: tuple[str, ...]) -> DeclaredSkip:
    assert name not in SKIP_REGISTRY, name
    SKIP_REGISTRY[name] = declared = DeclaredSkip(name, skip_when, reason, ci)
    return declared


_not_windows = os.name != "nt"
_is_windows = os.name == "nt"
_win32 = sys.platform == "win32"

requires_windows_security = _declare(
    "windows-security", "sys.platform != 'win32'",
    "native Windows socket exclusivity and file DACL APIs", UNIT_WINDOWS,
).mark(not _win32)
requires_linux_tree_custody = _declare(
    "linux-tree-custody", "sys.platform != 'linux'",
    "Linux waitid WNOWAIT process-group custody", UNIT_POSIX,
).mark(sys.platform != "linux")
requires_posix_inherited_descriptors = _declare(
    "posix-inherited-descriptors", "os.name == 'nt'",
    "relay integration requires POSIX inherited descriptors", UNIT_POSIX,
).mark(_is_windows)
requires_posix_uid_metadata = _declare(
    "posix-uid-metadata", "os.name == 'nt'",
    "Windows owner-only checks use native DACLs, not POSIX uid metadata", UNIT_POSIX,
).mark(_is_windows)
requires_posix_file_modes_native_custody = _declare(
    "posix-file-modes-native-custody", "sys.platform == 'win32'",
    "Windows uses native DACLs instead of POSIX file modes", UNIT_POSIX,
).mark(_win32)
requires_posix_private_modes = _declare(
    "posix-private-modes", "sys.platform == 'win32'",
    "Windows uses native DACLs rather than POSIX modes", UNIT_POSIX,
).mark(_win32)
requires_windows_token_process_times = _declare(
    "windows-token-process-times", "sys.platform != 'win32'",
    "Windows token and process-time APIs", UNIT_WINDOWS,
).mark(not _win32)
requires_posix_process_groups = _declare(
    "posix-process-groups", "sys.platform == 'win32'",
    "POSIX process group integration", UNIT_POSIX,
).mark(_win32)
requires_windows_job_object = _declare(
    "windows-job-object", "sys.platform != 'win32'",
    "Windows Job Object integration", UNIT_WINDOWS,
).mark(not _win32)
requires_windows_dirfd_adapter = _declare(
    "windows-dirfd-adapter", "os.name != 'nt'",
    "exercises the native Windows dir-fd adapter", UNIT_WINDOWS,
).mark(_not_windows)
requires_windows_reparse_point_rejection = _declare(
    "windows-reparse-point-rejection", "os.name != 'nt'",
    "exercises Windows reparse-point rejection", UNIT_WINDOWS,
).mark(_not_windows)
requires_windows_sqlite_backup = _declare(
    "windows-sqlite-backup", "os.name != 'nt'",
    "exercises Windows SQLite backup snapshots", UNIT_WINDOWS,
).mark(_not_windows)
requires_windows_process_and_lock_apis = _declare(
    "windows-process-and-lock-apis", "os.name != 'nt'",
    "native Windows process and lock APIs", UNIT_WINDOWS,
).mark(_not_windows)
requires_posix_owner_only_permissions = _declare(
    "posix-owner-only-permissions", "os.name == 'nt'",
    "POSIX owner-only permission behavior", UNIT_POSIX,
).mark(_is_windows)
requires_posix_process_group_id_reuse = _declare(
    "posix-process-group-id-reuse", "os.name == 'nt'",
    "this regression checks POSIX process group ID reuse", UNIT_POSIX,
).mark(_is_windows)
requires_posix_fork = _declare(
    "posix-fork", "os.name == 'nt'",
    "multiprocessing fork is unavailable on Windows", UNIT_POSIX,
).mark(_is_windows)

# Decided while the test runs, so it is a call rather than a mark.
_WINDOWS_SYMLINKS = _declare(
    "windows-symlink-creation", "creating a symlink raises on Windows (WinError 1314, no privilege)",
    "symlink creation is unavailable for this Windows account", UNIT_WINDOWS,
)
# Applied to every ``darwin_native`` test below; the lane is deselected by default
# and run by the ``darwin-native`` job.
_DARWIN_NATIVE = _declare(
    "darwin-native", "sys.platform != 'darwin'", "needs native macOS APIs",
    ("darwin-native",),
)


def skip_windows_symlink_creation_unavailable() -> None:
    pytest.skip(f"{_WINDOWS_SYMLINKS.tag} {_WINDOWS_SYMLINKS.reason}")


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


_DECLARED_TAG = re.compile(r"\[declared:([a-z0-9-]+)\]")


class _SkipGuard:
    """No invisible skips: list every skip by name and fail on any undeclared one.

    A skip is declared when its reason carries ``[declared:NAME]`` for a NAME in
    SKIP_REGISTRY (the ``requires_*`` marks and ``darwin_native`` do this). Any
    other skip (a raw ``pytest.skip``, ``importorskip``, ``skip`` mark), and any
    xfail, fails the run. Works under xdist: reports reach the controller.
    """

    def __init__(self) -> None:
        self.declared: list[tuple[str, str]] = []
        self.undeclared: list[tuple[str, str]] = []

    def _record(self, report) -> None:
        if getattr(report, "wasxfail", None) is not None:
            self.undeclared.append((report.nodeid, "xfail is not allowed: " + str(report.wasxfail)))
            return
        if not report.skipped:
            return
        longrepr = report.longrepr
        reason = longrepr[2] if isinstance(longrepr, tuple) else str(longrepr)
        reason = reason.removeprefix("Skipped: ")
        match = _DECLARED_TAG.search(reason)
        if match and match.group(1) in SKIP_REGISTRY:
            self.declared.append((report.nodeid, reason))
        else:
            self.undeclared.append((report.nodeid, reason))

    def pytest_runtest_logreport(self, report) -> None:
        # A skipif mark skips in setup; a runtime pytest.skip() skips in call.
        if report.when in ("setup", "call"):
            self._record(report)

    def pytest_collectreport(self, report) -> None:
        self._record(report)

    def pytest_terminal_summary(self, terminalreporter) -> None:
        write = terminalreporter.write_line
        if self.declared:
            write(f"declared skips ({len(self.declared)}):")
            for nodeid, reason in sorted(self.declared):
                write(f"  SKIP {nodeid}: {reason}")
        for nodeid, reason in sorted(self.undeclared):
            write(f"UNDECLARED SKIP {nodeid}: {reason}")

    @pytest.hookimpl(trylast=True)
    def pytest_sessionfinish(self, session, exitstatus):
        if self.undeclared:
            session.exitstatus = pytest.ExitCode.TESTS_FAILED



def pytest_configure(config):
    for name, meaning in LANE_MARKERS.items():
        config.addinivalue_line("markers", f"{name}: {meaning}")
    config.pluginmanager.register(_FdGuard(), "fd-leak-guard")
    config.pluginmanager.register(_SkipGuard(), "skip-guard")


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config, items):
    for item in items:
        if sys.platform != "darwin" and item.get_closest_marker("darwin_native"):
            item.add_marker(pytest.mark.skip(reason=f"{_DARWIN_NATIVE.tag} {_DARWIN_NATIVE.reason}"))
