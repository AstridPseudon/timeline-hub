"""The skip guard (tests/lanes.py) fails the run on undeclared skips and xfails."""

from __future__ import annotations

import sys
import textwrap
from pathlib import Path

import pytest

pytest_plugins = ["pytester"]

REPO = Path(__file__).resolve().parent.parent


@pytest.fixture
def sandbox(pytester):
    pytester.makeconftest(
        f"""
        import sys
        sys.path.insert(0, {str(REPO)!r})
        from tests.lanes import pytest_configure  # noqa: F401
        """
    )
    pytester.makeini("[pytest]\npython_files = check_*.py\n")
    return pytester


def _run(sandbox, body: str):
    sandbox.makepyfile(check_it=textwrap.dedent(body))
    return sandbox.runpytest_subprocess("-p", "no:cacheprovider", "-q")


def test_undeclared_pytest_skip_fails_the_run(sandbox):
    result = _run(sandbox, """
        import pytest
        def test_a():
            pytest.skip("flaky today")
        """)
    assert result.ret != 0
    result.stdout.fnmatch_lines(["UNDECLARED SKIP *::test_a: *flaky today*"])


def test_skip_mark_importorskip_and_xfail_fail_the_run(sandbox):
    result = _run(sandbox, """
        import pytest
        @pytest.mark.skip(reason="x")
        def test_mark(): pass
        @pytest.mark.skipif(True, reason="[declared:not-in-registry] nope")
        def test_unknown_tag(): pass
        @pytest.mark.xfail(reason="later")
        def test_xfail(): assert False
        """)
    assert result.ret != 0
    result.stdout.fnmatch_lines([
        "UNDECLARED SKIP *::test_mark: *",
        "UNDECLARED SKIP *::test_unknown_tag: *",
        "UNDECLARED SKIP *::test_xfail: xfail is not allowed*",
    ])


def test_declared_skip_passes_and_is_listed_by_name(sandbox):
    other = "windows" if sys.platform != "win32" else "posix"
    helper = "requires_windows_security" if other == "windows" else "requires_posix_process_groups"
    result = _run(sandbox, f"""
        from tests.lanes import {helper}
        @{helper}
        def test_platform_only(): assert False
        """)
    assert result.ret == 0, result.stdout.str()
    result.stdout.fnmatch_lines(["declared skips (1):", "  SKIP *::test_platform_only: [[]declared:*"])


def test_declared_runtime_skip_helper_passes(sandbox):
    result = _run(sandbox, """
        from tests.lanes import skip_windows_symlink_creation_unavailable
        def test_symlink():
            skip_windows_symlink_creation_unavailable()
        """)
    assert result.ret == 0, result.stdout.str()
    result.stdout.fnmatch_lines(["  SKIP *::test_symlink: [[]declared:windows-symlink-creation]*"])
