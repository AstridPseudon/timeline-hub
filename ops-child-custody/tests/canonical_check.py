#!/usr/bin/env python3
"""Run the one canonical, read-only OPS portable source check."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shlex
import subprocess
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TESTS = REPO / "ops-child-custody/tests"
RUNNER = Path("/home/user/work/venv-agent/bin/python")
CHILD_PYTHON = Path("/usr/bin/python3.13")
GOVERNING_RUFF = Path("/root/.local/bin/ruff")
SECONDARY_RUFF = Path("/home/user/work/venv-agent/bin/ruff")
BASE_COMMIT = "60753548ebc8e69f3c84fbb28fa2e09b1ca78316"
BASE_TREE = "dd4347a933103bbfc17c3e3237d52ea13ac1f677"
HISTORICAL_BASE = "f6b9d4d52802d3cc5cd6bf9be070cd4c40d1e2fe"
MAKER_PATHS = (
    REPO / "ops-child-custody/e2e-fixtures/tiny/makers/parent-0857/make-child-venv",
    REPO / "ops-child-custody/e2e-fixtures/tiny/makers/candidate-c3226b/make-child-venv",
)
SOURCE_PATHS = (
    TESTS / "e2e_inventory.py",
    TESTS / "test_e2e_inventory.py",
    Path(__file__).resolve(),
)
MANIFEST = REPO / "ops-child-custody/e2e-fixtures/tiny/manifest.json"
SUPPORT = TESTS / "support.py"
RUNNER_SOURCE = TESTS / "e2e_inventory.py"
EXPECTED_HISTORICAL_EOF = (
    (
        "ops-child-custody/e2e-fixtures/tiny/makers/candidate-c3226b/make-child-venv:1224: "
        "new blank line at EOF."
    ),
    (
        "ops-child-custody/e2e-fixtures/tiny/makers/parent-0857/make-child-venv:1201: "
        "new blank line at EOF."
    ),
)


class Check:
    def __init__(self, cache: Path):
        self.cache = cache
        self.failures: list[str] = []

    def say(self, line: str = "") -> None:
        print(line)

    def command(
        self,
        argv: list[str | Path],
        *,
        env: dict[str, str] | None = None,
        expected: set[int] | None = None,
        label: str,
    ) -> subprocess.CompletedProcess[str]:
        rendered = shlex.join(str(item) for item in argv)
        self.say(f"COMMAND {label}: {rendered}")
        try:
            result = subprocess.run(
                [str(item) for item in argv],
                capture_output=True,
                text=True,
                env=env,
                check=False,
                timeout=900,
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            self.say(f"EXCEPTION {type(error).__name__}: {error}")
            self.failures.append(f"{label}: command could not run")
            return subprocess.CompletedProcess(argv, 127, "", str(error))
        self.say(f"STDOUT {label} BEGIN")
        if result.stdout:
            print(result.stdout, end="")
        self.say(f"STDOUT {label} END")
        self.say(f"STDERR {label} BEGIN")
        if result.stderr:
            print(result.stderr, end="")
        self.say(f"STDERR {label} END")
        self.say(f"EXIT {label}: {result.returncode}")
        if expected is None:
            expected = {0}
        if result.returncode not in expected:
            self.failures.append(f"{label}: unexpected exit {result.returncode}")
        return result

    def require(self, condition: bool, message: str) -> None:
        if not condition:
            self.failures.append(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def version_text(result: subprocess.CompletedProcess[str]) -> str:
    return (result.stdout or result.stderr).strip()


def run_ruff(check: Check, binary: Path, label: str, scope: tuple[Path, ...]) -> None:
    if not binary.is_file() or not os.access(binary, os.X_OK):
        check.say(f"PREREQ NOTRUN {label}: missing governing Ruff {binary}")
        check.failures.append(f"{label}: governing Ruff prerequisite is absent")
        return
    version = check.command([binary, "--version"], label=f"{label} version")
    check.require(version_text(version) == ("ruff 0.16.8" if label == "governing Ruff" else "ruff 0.12.0"),
                  f"{label}: unexpected version {version_text(version)!r}")
    check.command([binary, "check", "--no-cache", *scope], label=f"{label} scoped check")


def check_negative_census(check: Check, scratch: Path) -> None:
    missing = scratch / "missing"
    result_path = scratch / "negative-census.json"
    env = {**os.environ, "TMPDIR": str(scratch), "PYTHONDONTWRITEBYTECODE": "1"}
    command = [
        RUNNER,
        RUNNER_SOURCE,
        "--check-only",
        "--helper",
        missing / "bench_store.py",
        "--bootstrap-artifact",
        missing / "bootstrap.tgz",
        "--runner-python",
        RUNNER,
        "--build-python",
        RUNNER,
        "--python",
        CHILD_PYTHON,
        "--wheelhouse",
        missing / "wheelhouse",
        "--agent",
        missing / "agent",
        "--runtime",
        missing / "runtime",
        "--orch-root",
        missing / "orch",
        "--parent-work",
        missing / "parent",
        "--candidate-work",
        missing / "candidate",
        "--result",
        result_path,
    ]
    census = check.command(command, env=env, expected={2}, label="negative census")
    try:
        payload, end = json.JSONDecoder().raw_decode(census.stdout)
        check.require(not census.stdout[end:].strip(), "negative census: stdout has trailing non-JSON output")
    except (json.JSONDecodeError, TypeError):
        check.failures.append("negative census: structured JSON was not emitted")
        return
    check.require(payload.get("schema") == "timeline.ops-child-custody.check-only.v1",
                  "negative census: wrong structured schema")
    check.require(payload.get("mode") == "check-only" and payload.get("ok") is False,
                  "negative census: refusal was not structured")
    for flag in ("mutating_setup_started", "maker_started", "store_initialized", "git_mutated"):
        check.require(payload.get(flag) is False, f"negative census: {flag} was not false")
    expected = {
        "protected Store helper is supplied as an absolute physical path",
        "private wheelhouse is supplied as an absolute physical path",
        "Agent source carrier checkout is supplied as an absolute physical path",
        "Runtime source carrier checkout is supplied as an absolute physical path",
        "protected Store helper hash",
        "local bootstrap artifact hash",
        "local wheel pip-26.2.1-py3-none-any.whl",
        "local wheel setuptools-80.9.0-py3-none-any.whl",
        "local wheel wheel-0.46.3-py3-none-any.whl",
        "local wheel custody_b-0.1.0-py3-none-any.whl",
        "local wheel custody_a-0.1.0-py3-none-any.whl",
        "Agent source carrier checkout Git history and exact committed source are readable",
        "Runtime source carrier checkout Git history and exact committed source are readable",
        "Store API initialize is present in the protected helper",
        "Store API ensure is present in the protected helper",
        "Store API registration is present in the protected helper",
        "local bootstrap artifact has the maker-supported basename",
        "orchestration root is a fresh path inside TMPDIR",
        "parent work root is a fresh path inside TMPDIR",
        "candidate work root is a fresh path inside TMPDIR",
    }
    actual = set(payload.get("missing", ()))
    check.require(expected <= actual, "negative census: expected missing inputs were omitted")
    check.require(all(isinstance(item, str) for item in actual),
                  "negative census: missing census contains non-string entries")
    check.require(actual <= expected | {"free space is above unchanged start reserve"},
                  "negative census: unknown missing item was counted as zero")
    check.require(not result_path.is_symlink() and result_path.is_file(),
                  "negative census: structured result file was not written")


def check_source_and_immutable_inputs(check: Check) -> None:
    head = check.command(["git", "rev-parse", "HEAD"], label="current commit")
    tree = check.command(["git", "rev-parse", "HEAD^{tree}"], label="current tree")
    check.say(f"BASE COMMIT: {BASE_COMMIT}")
    check.say(f"BASE TREE: {BASE_TREE}")
    check.say(f"CURRENT COMMIT: {head.stdout.strip()}")
    check.say(f"CURRENT TREE: {tree.stdout.strip()}")
    base_tree = check.command(["git", "rev-parse", f"{BASE_COMMIT}^{{tree}}"], label="base tree authentication")
    check.require(base_tree.stdout.strip() == BASE_TREE, "base commit tree does not match settled input")
    check.say("HARNESS FINAL COMMIT: PENDING (harness commits after worker exit)")
    check.say("HARNESS FINAL TREE: PENDING (harness commits after worker exit)")

    check.command(
        ["git", "diff", "--check", BASE_COMMIT, "--", *SOURCE_PATHS[:2]],
        label="owned source scoped diff check",
    )
    script_diff = check.command(
        ["git", "diff", "--no-index", "--check", "/dev/null", Path(__file__).resolve()],
        expected={1},
        label="canonical script scoped diff check",
    )
    check.require(not script_diff.stdout and not script_diff.stderr,
                  "canonical script scoped diff check reported whitespace diagnostics")
    historical = check.command(
        ["git", "diff", "--check", HISTORICAL_BASE, "--", *MAKER_PATHS],
        expected={2},
        label="historical maker EOF diagnostics",
    )
    diagnostics = tuple(line for line in historical.stdout.splitlines() if line)
    check.require(diagnostics == EXPECTED_HISTORICAL_EOF,
                  "historical maker EOF diagnostics changed or gained an extra finding")
    check.say("HISTORICAL MAKER EOF DIAGNOSTICS: preserved and separately reported; not authored failures")

    for path in (Path(__file__).resolve(), RUNNER_SOURCE, SUPPORT, MANIFEST, *MAKER_PATHS):
        check.require(path.is_file() and not path.is_symlink(), f"missing authenticated file: {path}")
        if path.is_file() and not path.is_symlink():
            mode = path.stat().st_mode & 0o777
            check.say(f"AUTHENTICATED {path.relative_to(REPO)} mode={mode:03o} sha256={digest(path)}")
    for path in MAKER_PATHS:
        check.require((path.stat().st_mode & 0o777) == 0o755, f"maker mode is not 755: {path}")
    check.require((Path(__file__).resolve().stat().st_mode & 0o777) == 0o755,
                  "canonical script mode is not 755")
    check.require((MANIFEST.stat().st_mode & 0o777) == 0o644, "manifest mode is not 644")


def main() -> int:
    os.chdir(REPO)
    scratch = Path(tempfile.mkdtemp(prefix="timeline-canonical-check-"))
    check = Check(scratch)
    check.say("CANONICAL OPS CHECK: one invocation; read-only source/unit qualification")
    check.say(f"REPOSITORY: {REPO}")
    check.say(f"PRIVATE CACHE: {scratch}")
    check.say(f"RUNNER: {RUNNER}")
    check.say(f"CHILD PYTHON: {CHILD_PYTHON}")
    check.require(RUNNER.is_file() and os.access(RUNNER, os.X_OK), "supported Agent runner binding is unavailable")
    check.require(CHILD_PYTHON.is_file() and os.access(CHILD_PYTHON, os.X_OK),
                  "supported child Python binding is unavailable")

    run_ruff(check, GOVERNING_RUFF, "governing Ruff", SOURCE_PATHS)
    if SECONDARY_RUFF.is_file() and os.access(SECONDARY_RUFF, os.X_OK):
        run_ruff(check, SECONDARY_RUFF, "repository Ruff", (TESTS,))
    else:
        check.say(f"SECONDARY RUFF NOTRUN: optional repository Ruff is absent at {SECONDARY_RUFF}")

    test_env = {
        **os.environ,
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONPATH": str(TESTS),
        "PYTHONPYCACHEPREFIX": str(scratch / "pycache"),
    }
    test_command = [
        RUNNER,
        "-m",
        "unittest",
        "-v",
        "ops-child-custody/tests/test_e2e_inventory.py",
        "ops-child-custody/tests/test_custody.py",
        "ops-child-custody/tests/test_inventory.py",
    ]
    tests = check.command(test_command, env=test_env, label="existing unittest suite (64 tests)")
    check.require(re.search(r"Ran 64 tests in [0-9.]+s", tests.stderr + tests.stdout) is not None,
                  "existing unittest suite did not report exactly 64 tests")
    for control in (
        "test_check_only_accumulates_missing_and_malformed_sources_with_other_prerequisites",
        "test_malformed_role_variants_accumulate_with_simultaneous_missing_prerequisites",
        "test_invalid_optional_result_path_and_tmpdir_are_refused",
        "test_check_only_refuses_altered_clean_committed_source_bytes",
        "test_valid_census_authenticates_sources_wheels_makers_and_all_prerequisites",
        "test_actual_manifest_helper_and_frozen_makers_pass_readonly_component_checks",
    ):
        check.require(control in tests.stdout + tests.stderr,
                      f"existing unittest suite omitted required census control: {control}")
    check.command(
        [RUNNER, "-m", "py_compile", *SOURCE_PATHS],
        env=test_env,
        label="private-cache py_compile",
    )
    check_source_and_immutable_inputs(check)
    check_negative_census(check, scratch)
    check.say(f"SOURCE HASH {RUNNER_SOURCE.relative_to(REPO)}: {digest(RUNNER_SOURCE)}")
    check.say(f"SCRIPT HASH {Path(__file__).resolve().relative_to(REPO)}: {digest(Path(__file__).resolve())}")
    if check.failures:
        check.say("CANONICAL OPS CHECK: FAIL")
        for failure in check.failures:
            check.say(f"FAILURE: {failure}")
        return 1
    check.say("CANONICAL OPS CHECK: PASS (source/unit only; genuine whole-maker E2E remains NOTRUN)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
