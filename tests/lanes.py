"""Test lanes and the skip registry ("we shouldn't have invisible skips").

One registry, ``LANES``, declares every reason a test may be left out of a run. A test opts in with the
marker that has the lane's name (``@pytest.mark.ffmpeg``, ``@pytest.mark.posix_native``); it never calls
``pytest.skip`` or ``skipif`` itself (tests/test_skip_policy.py scans for that). A lane is one of:

* ``platform``: the code cannot run on another OS. Off that OS the test is skipped, and the skip is declared.
* ``dependency``: the test needs a tool a CI job provides (ffmpeg, Node, the Remotion install). Where the
  dependency is missing the test is skipped and the skip is declared, EXCEPT in a job that is meant to
  provide it (the job's ``ASTRID_CI_JOB`` is in the lane's ``jobs``), and in a lane the run selected by
  name (``default_off``): there a missing dependency is a failure.
* ``manual``: needs something no CI job has (a second checkout, credentials, opt-in). Always ``default_off``,
  so the default run deselects these tests; running one by hand with ``-m`` fails, never skips, when its
  dependency is missing.

``default_off`` lanes are deselected by ``addopts`` in pyproject.toml (tests/test_lane_registry.py keeps the two
in step). Every non-manual lane names the CI jobs that run it, and tests/test_lane_registry.py checks those jobs
in .github/workflows/ci.yml: they set ``ASTRID_CI_JOB``, provision the dependency and select the lane.

The guard (``_SkipGuard``) records every skip by test id. A skip that did not come from a registry lane, a
``pytest.importorskip`` anywhere, a module-level skip at collection and every xfail turn into failures; the
terminal summary lists the declared skips by name.

Modules that wholly belong to a ``default_off`` lane (``pytestmark = pytest.mark.<lane>``) are not collected
in a run that deselects the lane, so their import-time needs (a second checkout) never run there.

Leaked file descriptors (testing plan LEAK.2). The run fails if the pytest process
ends holding more than FD_LEAK_ALLOWANCE descriptors beyond what it held at start.
(Leaked daemon and host process groups are caught by conftest's session guard.)
"""

from __future__ import annotations

import ast
import importlib
import os
import re
import shutil
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import NoReturn

import pytest

FD_LEAK_ALLOWANCE = 64
REPO = Path(__file__).resolve().parents[1]

UBUNTU = "unit-shard-ubuntu-latest"
WINDOWS = "unit-shard-windows-latest"
DARWIN = "darwin-native"


def has_media_tools() -> bool:
    return bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))


def has_font() -> bool:
    from astrid.packs.rendering.rendering.renderers.ffmpeg.text import _resolve_font_path

    return _resolve_font_path(False) is not None and _resolve_font_path(True) is not None


def has_chrome() -> bool:
    root = REPO / "remotion" / "node_modules" / ".remotion" / "chrome-headless-shell"
    return any(path.is_file() and os.access(path, os.X_OK) for path in root.glob("*/*/chrome-headless-shell"))


def has_remotion() -> bool:
    return bool(shutil.which("node")) and (REPO / "remotion" / "node_modules").is_dir() and has_media_tools()


@dataclass(frozen=True)
class Lane:
    kind: str  # "platform" | "dependency" | "manual"
    reason: str
    available: Callable[[], bool]
    jobs: tuple[str, ...] = ()  # the CI jobs (ASTRID_CI_JOB) that run these tests where `available` holds
    default_off: bool = False  # deselected by addopts; a run that selects the lane must find its dependency
    provision: str = ""  # text each job in `jobs` must contain to provide the dependency

    @property
    def requires_dependency(self) -> bool:
        return self.kind != "platform"


def _never() -> bool:
    return False


LANES: dict[str, Lane] = {
    "posix_native": Lane("platform", "needs POSIX-only process or file descriptor APIs", lambda: os.name == "posix", (UBUNTU,)),
    "non_root": Lane("platform", "needs a non-root user (chmod 000 does not block root)", lambda: not hasattr(os, "geteuid") or os.geteuid() != 0, (UBUNTU,)),
    "linux_native": Lane("platform", "needs Linux-only /proc or pidfd APIs", lambda: sys.platform.startswith("linux"), (UBUNTU,)),
    "windows_native": Lane("platform", "needs native Windows APIs", lambda: sys.platform == "win32", (WINDOWS,)),
    "darwin_native": Lane("platform", "needs native macOS APIs", lambda: sys.platform == "darwin", (DARWIN,), default_off=True),
    "ffmpeg": Lane("dependency", "needs ffmpeg and ffprobe on PATH", has_media_tools, (UBUNTU, WINDOWS), provision="ffmpeg"),
    "node": Lane("dependency", "needs Node on PATH", lambda: bool(shutil.which("node")), (UBUNTU, WINDOWS), provision="setup-node"),
    "font": Lane("dependency", "needs a system TTF font (DejaVu Sans on Linux, Arial on macOS)", has_font, (UBUNTU,), provision="fonts-dejavu-core"),
    "chrome": Lane(
        "dependency", "needs the provisioned Remotion headless Chromium (npx remotion browser ensure)", has_chrome,
        (DARWIN,), default_off=True, provision="remotion browser ensure",
    ),
    "remotion": Lane(
        "dependency", "needs Node, ffmpeg and the Remotion install (npm ci --prefix remotion)", has_remotion,
        (DARWIN,), default_off=True, provision="npm ci --prefix remotion",
    ),
    "integration": Lane("manual", "needs a long-lived subprocess, a second checkout (Runtime, VibeComfy) or the network; no CI job", _never, default_off=True),
    "live": Lane("manual", "needs real provider credentials; no CI job", _never, default_off=True),
    "opt_in": Lane("manual", "explicitly opt-in (an environment variable or a GPU); no CI job", _never, default_off=True),
}
DEFAULT_OFF = tuple(name for name, lane in LANES.items() if lane.default_off)
DECLARED = re.compile(r"\[declared:([a-z_]+)\]")


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



def current_job() -> str:
    return os.environ.get("ASTRID_CI_JOB", "")


def require_module(name: str) -> ModuleType:
    """Import a module that only a ``default_off`` lane provides (a second checkout or an optional library).

    Missing is an error: the module that calls this is wholly in that lane and is not collected unless the run selects it.
    """
    return importlib.import_module(name)


def unavailable(message: str) -> NoReturn:
    """A second checkout is missing: the tests that need it are in a lane the run selected, so this fails."""
    pytest.fail(message, pytrace=False)


def _lane_names(item) -> list[str]:
    seen: list[str] = []
    for mark in item.iter_markers():
        if mark.name in LANES and mark.name not in seen:
            seen.append(mark.name)
    return seen


def _declared_skip(name: str) -> pytest.MarkDecorator:
    return pytest.mark.skip(reason=f"[declared:{name}] {LANES[name].reason}")


class _SkipGuard:
    """Every skip is declared by a registry lane and reported by test id; anything else fails the run."""

    def __init__(self) -> None:
        self.declared: list[tuple[str, str, str]] = []

    def _judge(self, report, where: str) -> None:
        if hasattr(report, "wasxfail"):
            del report.wasxfail  # pytest does not count a failed report that still carries it
            report.outcome = "failed"
            report.longrepr = f"{where}: an xfail hides the result. Fix the test or delete it."
            return
        if not report.skipped:
            return
        reason = str(report.longrepr[2] if isinstance(report.longrepr, tuple) and len(report.longrepr) == 3 else report.longrepr)
        match = DECLARED.search(reason)
        lane = LANES.get(match.group(1)) if match else None
        if lane is None:
            report.outcome = "failed"
            report.longrepr = (
                f"{where}: undeclared skip ({reason}).\n"
                "A skip must come from a lane in tests/lanes.py: mark the test with the lane's marker; do not call pytest.skip, "
                "skipif or importorskip. A dependency the package or lane provides is imported or run plainly."
            )
            return
        name = match.group(1)
        if lane.requires_dependency and (lane.default_off or current_job() in lane.jobs):
            report.outcome = "failed"
            where_lane = "this run selected the lane" if lane.default_off else f"the {current_job()} job provides it"
            report.longrepr = f"{where}: the {name} lane's dependency is missing but {where_lane}: {lane.reason}. A missing dependency here is a failure, not a skip."
            return
        self.declared.append((where, name, re.sub(r"^Skipped:\s*", "", reason.replace(match.group(0), "")).strip()))

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        outcome = yield
        self._judge(outcome.get_result(), item.nodeid)

    @pytest.hookimpl(hookwrapper=True)
    def pytest_make_collect_report(self, collector):
        outcome = yield
        report = outcome.get_result()
        if report.skipped:
            report.outcome = "failed"
            report.longrepr = f"{collector.nodeid}: a module-level skip hides its tests. Mark the module or its tests with a lane from tests/lanes.py."

    def pytest_terminal_summary(self, terminalreporter):
        if not self.declared:
            return
        terminalreporter.write_sep("-", f"declared skips ({len(self.declared)})")
        for nodeid, name, reason in sorted(self.declared):
            terminalreporter.write_line(f"SKIPPED [{name}] {nodeid}: {reason}")


def _module_lanes(path: Path) -> set[str]:
    """The lanes a module's top-level ``pytestmark`` puts every test of it in."""
    try:
        source = path.read_text(encoding="utf-8")
        if "pytestmark" not in source:
            return set()
        tree = ast.parse(source)
    except (OSError, SyntaxError, UnicodeDecodeError):
        return set()
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "pytestmark" for t in node.targets):
            for sub in ast.walk(node.value):
                if isinstance(sub, ast.Attribute) and isinstance(sub.value, ast.Attribute) and sub.value.attr == "mark" and sub.attr in LANES:
                    names.add(sub.attr)
    return names


def _marker_expression_holds(expression: str, present: set[str], others: bool) -> bool:
    if not re.fullmatch(r"[\w\s()]*", expression):
        return True  # an expression this reader does not handle never hides a module
    def value(match: re.Match) -> str:
        word = match.group(0)
        if word in ("and", "or", "not"):
            return word
        return str(word in present or others)
    return bool(eval(re.sub(r"\w+", value, expression), {"__builtins__": {}}))  # noqa: S307  (only words, spaces and parentheses reach here)


def pytest_ignore_collect(collection_path, config):
    """Do not import a module whose every test belongs to a lane this run deselects."""
    expression = (config.getoption("markexpr", default="") or "").strip()
    if not expression or collection_path.suffix != ".py":
        return None
    lanes = _module_lanes(collection_path)
    if lanes and not _marker_expression_holds(expression, lanes, False) and not _marker_expression_holds(expression, lanes, True):
        return True
    return None


def pytest_configure(config):
    for name, lane in LANES.items():
        config.addinivalue_line("markers", f"{name}: {lane.kind} lane: {lane.reason}")
    config.pluginmanager.register(_FdGuard(), "fd-leak-guard")
    config.pluginmanager.register(_SkipGuard(), "skip-guard")


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config, items):
    for item in items:
        needs_checkout = set(getattr(getattr(item, "module", None), "INTEGRATION_FIXTURES", ()))
        if needs_checkout & set(getattr(item, "fixturenames", ())):
            item.add_marker(pytest.mark.integration)
        for name in _lane_names(item):
            if not LANES[name].available() and LANES[name].kind != "manual":
                item.add_marker(_declared_skip(name))
                break
