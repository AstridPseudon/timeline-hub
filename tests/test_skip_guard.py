"""The skip guard of tests/lanes.py: no invisible skips.

Each case runs a throwaway test module in a fresh pytest process (pytester) whose conftest carries the real
lane hooks. A skip passes only when a registry lane declares it, and it is then listed by test id.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from tests import lanes

pytest_plugins = ["pytester"]

REPO = Path(__file__).resolve().parents[1]
HOOKS = "from tests.lanes import pytest_collection_modifyitems, pytest_configure, pytest_ignore_collect  # noqa: F401\n"
UBUNTU_JOB = lanes.UBUNTU


@pytest.fixture
def run(pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    for name in ("CI", "PYTEST_ADDOPTS", "ASTRID_CI_JOB"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("PYTHONPATH", str(REPO))
    pytester.makeconftest(HOOKS)
    bare_path = tmp_path / "empty-path"
    bare_path.mkdir()

    def go(source: str, *args: str, job: str = "", bare_path_env: bool = False) -> pytest.RunResult:
        pytester.makepyfile(test_case=source)
        if job:
            monkeypatch.setenv("ASTRID_CI_JOB", job)
        if bare_path_env:
            monkeypatch.setenv("PATH", str(bare_path))
        return pytester.runpytest_subprocess("-p", "no:cacheprovider", "-o", "addopts=", *args)

    return go


def test_an_undeclared_skip_in_a_test_body_fails_the_run(run) -> None:
    result = run("import pytest\n\ndef test_x():\n    pytest.skip('flaky here')\n")
    assert result.ret != 0
    result.stdout.fnmatch_lines(["*test_case.py::test_x*undeclared skip (*flaky here)*"])


def test_an_undeclared_skipif_mark_fails_the_run(run) -> None:
    result = run("import pytest\n\n@pytest.mark.skipif(True, reason='nope')\ndef test_x():\n    pass\n")
    assert result.ret != 0
    result.stdout.fnmatch_lines(["*undeclared skip (*nope)*"])


def test_an_importorskip_in_a_test_body_fails_the_run(run) -> None:
    result = run("import pytest\n\ndef test_x():\n    pytest.importorskip('astrid_no_such_dependency')\n")
    assert result.ret != 0
    result.stdout.fnmatch_lines(["*test_case.py::test_x*undeclared skip (*astrid_no_such_dependency*"])


def test_a_module_level_importorskip_fails_the_run(run) -> None:
    result = run("import pytest\n\npytest.importorskip('astrid_no_such_dependency')\n\ndef test_x():\n    pass\n")
    assert result.ret != 0
    result.stdout.fnmatch_lines(["*module-level skip hides its tests*"])


def test_a_skip_that_pretends_to_be_declared_fails_the_run(run) -> None:
    result = run("import pytest\n\ndef test_x():\n    pytest.skip('[declared:no_such_lane] trust me')\n")
    assert result.ret != 0
    result.stdout.fnmatch_lines(["*undeclared skip*"])


def test_an_xfail_fails_the_run(run) -> None:
    result = run("import pytest\n\n@pytest.mark.xfail(reason='known gap')\ndef test_x():\n    assert False\n")
    assert result.ret != 0
    result.stdout.fnmatch_lines(["*an xfail hides the result*"])


def test_a_declared_platform_skip_passes_and_is_listed_by_test_id(run) -> None:
    other = "windows_native" if sys.platform != "win32" else "posix_native"
    result = run(f"import pytest\n\n@pytest.mark.{other}\ndef test_x():\n    assert False\n\ndef test_y():\n    pass\n")
    assert result.ret == 0
    result.stdout.fnmatch_lines([
        "*declared skips (1)*",
        f"SKIPPED [[]{other}] test_case.py::test_x: *",
    ])


def test_a_declared_dependency_skip_passes_where_no_job_provides_it_and_is_listed(run) -> None:
    result = run("import pytest\n\n@pytest.mark.ffmpeg\ndef test_x():\n    pass\n\ndef test_y():\n    pass\n", bare_path_env=True)
    assert result.ret == 0
    result.stdout.fnmatch_lines(["*declared skips (1)*", "SKIPPED [[]ffmpeg] test_case.py::test_x: *"])


def test_a_missing_dependency_fails_in_the_job_that_is_meant_to_provide_it(run) -> None:
    result = run("import pytest\n\n@pytest.mark.ffmpeg\ndef test_x():\n    pass\n", job=UBUNTU_JOB, bare_path_env=True)
    assert result.ret != 0
    result.stdout.fnmatch_lines([f"*the ffmpeg lane's dependency is missing but the {UBUNTU_JOB} job provides it*"])


def test_a_missing_dependency_fails_in_a_lane_the_run_selected_by_name(run) -> None:
    source = "import pytest\n\n@pytest.mark.remotion\ndef test_x():\n    pass\n"
    result = run(source, "-m", "remotion", bare_path_env=True)
    assert result.ret != 0
    result.stdout.fnmatch_lines(["*the remotion lane's dependency is missing but this run selected the lane*"])


def test_a_test_in_several_lanes_is_one_declared_skip_where_one_of_them_does_not_hold(run) -> None:
    result = run("import pytest\n\n@pytest.mark.posix_native\n@pytest.mark.linux_native\n@pytest.mark.darwin_native\ndef test_x():\n    pass\n\ndef test_y():\n    pass\n", "-m", "darwin_native or linux_native or not posix_native")
    # no OS is POSIX, Linux and macOS at once, so one lane is unmet; that is a single declared skip, never a failure
    assert result.ret == 0
    result.stdout.fnmatch_lines(["*declared skips (1)*"])


def test_an_unregistered_marker_is_an_error_under_strict_markers(run) -> None:
    result = run("import pytest\n\n@pytest.mark.ffmpeg_typo\ndef test_x():\n    pass\n", "--strict-markers")
    assert result.ret != 0
    result.stdout.fnmatch_lines(["*'ffmpeg_typo' not found in `markers` configuration option*"])


def test_a_run_in_which_every_test_is_skipped_or_deselected_fails(run) -> None:
    other = "windows_native" if sys.platform != "win32" else "posix_native"
    skipped = run(f"import pytest\n\n@pytest.mark.{other}\ndef test_x():\n    pass\n")
    assert skipped.ret != 0
    skipped.stdout.fnmatch_lines(["*no test passed in this run*"])
    deselected = run("def test_x():\n    pass\n", "-k", "nothing_matches")
    assert deselected.ret != 0  # pytest's own "no tests collected"
