"""The import-skip guard, `require_module` and the Runtime locator (testing plan, R-6 and UA.3)."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


def _run(
    tmp_path: Path, source: str, *args: str, ci: bool = False, extra_env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    (tmp_path / "conftest.py").write_text("from tests.lanes import pytest_configure  # noqa: F401\n")
    (tmp_path / "test_case.py").write_text(source)
    env = {key: value for key, value in os.environ.items() if key not in ("CI", "PYTEST_ADDOPTS")}
    env["PYTHONPATH"] = str(REPO)
    if ci:
        env["CI"] = "true"
    env.update(extra_env or {})
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-o", "addopts=", "--rootdir", str(tmp_path),
         "--confcutdir", str(tmp_path), *args, str(tmp_path / "test_case.py")],
        cwd=tmp_path, env=env, capture_output=True, text=True, timeout=120, check=False,
    )


IMPORTORSKIP = "import pytest\n\n@pytest.mark.integration\ndef test_x():\n    pytest.importorskip('astrid_no_such_dependency')\n"
MODULE_LEVEL = "import pytest\n\npytestmark = pytest.mark.integration\npytest.importorskip('astrid_no_such_dependency')\n\ndef test_x():\n    pass\n"
REQUIRE = (
    "import pytest\nfrom tests.lanes import require_module\n\npytestmark = pytest.mark.integration\n"
    "require_module('astrid_no_such_dependency')\n\ndef test_x():\n    pass\n"
)


@pytest.mark.parametrize("source", [IMPORTORSKIP, MODULE_LEVEL], ids=["in-test", "module-level"])
def test_a_skip_on_import_is_allowed_locally(tmp_path: Path, source: str) -> None:
    done = _run(tmp_path, source)
    assert done.returncode in (0, 5), done.stdout + done.stderr  # skipped; 5 = nothing collected


@pytest.mark.parametrize("source", [IMPORTORSKIP, MODULE_LEVEL], ids=["in-test", "module-level"])
def test_a_skip_on_import_fails_in_ci_and_in_the_integration_lane(tmp_path: Path, source: str) -> None:
    in_ci = _run(tmp_path, source, ci=True)
    assert in_ci.returncode != 0 and "hides a broken install" in in_ci.stdout, in_ci.stdout + in_ci.stderr
    nightly = _run(tmp_path, source, "-m", "integration or live or opt_in")
    assert nightly.returncode != 0 and "hides a broken install" in nightly.stdout, nightly.stdout + nightly.stderr


def test_a_private_module_import_failure_is_not_hidden_in_ci(tmp_path: Path) -> None:
    source = "import sys\nsys.modules['runpod_lifecycle'] = None\n" + IMPORTORSKIP.replace("astrid_no_such_dependency", "runpod_lifecycle")
    done = _run(tmp_path, source, ci=True)
    assert done.returncode != 0 and "hides a broken install" in done.stdout, done.stdout + done.stderr


def test_require_module_skips_in_the_default_lane_and_fails_in_the_integration_lane(tmp_path: Path) -> None:
    default = _run(tmp_path, REQUIRE, "-m", "not integration and not live and not opt_in", ci=True)
    assert default.returncode in (0, 5), default.stdout + default.stderr
    nightly = _run(tmp_path, REQUIRE, "-m", "integration or live or opt_in", ci=True)
    assert nightly.returncode != 0 and "astrid_no_such_dependency" in nightly.stdout, nightly.stdout + nightly.stderr


NO_RUNTIME = (
    "import pytest\nfrom tests.helpers.runtime import runtime_checkout\n\npytestmark = pytest.mark.integration\n"
    "runtime_checkout()\n\ndef test_x():\n    pass\n"
)


def test_a_missing_runtime_skips_the_module_in_the_default_lane_and_fails_in_the_integration_lane(tmp_path: Path) -> None:
    missing = {"ASTRID_RUNTIME_CHECKOUT": str(tmp_path / "no-runtime")}
    default = _run(tmp_path, NO_RUNTIME, "-m", "not integration and not live and not opt_in", extra_env=missing)
    assert default.returncode in (0, 5), default.stdout + default.stderr
    nightly = _run(tmp_path, NO_RUNTIME, "-m", "integration or live or opt_in", ci=True, extra_env=missing)
    assert nightly.returncode != 0 and "no Runtime checkout" in nightly.stdout, nightly.stdout + nightly.stderr


def test_the_runtime_locator_takes_the_override_and_never_falls_through_from_it(tmp_path: Path, monkeypatch) -> None:
    from tests.helpers import runtime

    checkout = tmp_path / "runtime"
    (checkout / "runtime_protocol").mkdir(parents=True)
    monkeypatch.setenv(runtime.ENV, str(checkout))
    assert runtime.locate_runtime() == checkout.resolve()
    monkeypatch.setenv(runtime.ENV, str(tmp_path / "elsewhere"))
    assert runtime.locate_runtime() is None


def test_the_runtime_locator_reads_the_shared_dependency_pin() -> None:
    import json

    from tests.helpers import runtime

    assert runtime.vendored_runtime_commit() == json.loads((REPO / "runtime.lock.json").read_text())["source_commit"]


def test_the_runtime_locator_runs_the_runtime_as_of_a_commit(tmp_path: Path, monkeypatch) -> None:
    from tests.helpers import runtime

    checkout = tmp_path / "runtime"
    (checkout / "runtime_protocol").mkdir(parents=True)
    marker = checkout / "runtime_protocol" / "__init__.py"
    marker.write_text("VERSION = 1\n")
    git = ["git", "-C", str(checkout), "-c", "user.name=t", "-c", "user.email=t@example.com"]
    for command in (["init", "-q"], ["add", "."], ["commit", "-q", "-m", "one"]):
        subprocess.run([*git, *command], check=True, capture_output=True)
    commit = subprocess.run([*git, "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
    marker.write_text("VERSION = 2\n")  # a later working-tree edit must not reach the pinned copy
    monkeypatch.setenv(runtime.ENV, str(checkout))
    pinned = runtime.runtime_checkout(commit)
    assert (pinned / "runtime_protocol" / "__init__.py").read_text() == "VERSION = 1\n"
    assert runtime.runtime_checkout(commit) == pinned
    assert runtime.runtime_checkout() == checkout.resolve()
