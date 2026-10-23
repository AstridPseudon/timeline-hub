"""Every declared skip is tied to its condition and to the CI jobs that really run the test.

The workflows are parsed, not grepped: for each job the runner OSes, the per-OS ``continue-on-error``, the pytest
commands (their ``-m`` expression and paths) and the triggers. For each registry entry the tests it guards are found
in the test files, and a job counts as running the entry only when its commands select such a test on a runner OS
where the entry's condition is false.
"""

from __future__ import annotations

import ast
import re
import shlex
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

import pytest
import yaml
from _pytest.mark.expression import Expression

from tests import lanes
from tests.lanes import HOSTS, SKIP_REGISTRY, DeclaredSkip

REPO = Path(__file__).resolve().parent.parent
WORKFLOWS = REPO / ".github" / "workflows"
TESTS = REPO / "tests"
LANE_NAMES = set(lanes.LANE_MARKERS)
AUTOMATIC_TRIGGERS = {"push", "pull_request", "schedule"}


# --- workflows -----------------------------------------------------------------

@dataclass
class PytestCommand:
    marker_expression: str
    paths: list[str]  # relative to the repo; empty = the whole suite


@dataclass
class Job:
    workflow: str
    name: str
    oses: dict[str, bool]  # OS key -> blocking (False when continue-on-error holds on it)
    commands: list[PytestCommand] = field(default_factory=list)
    triggers: set[str] = field(default_factory=set)


def _default_marker_expression() -> str:
    addopts = tomllib.loads((REPO / "pyproject.toml").read_text(encoding="utf-8"))["tool"]["pytest"]["ini_options"]["addopts"]
    tokens = shlex.split(addopts)
    return tokens[tokens.index("-m") + 1]


def _os_key(runner: str) -> str:
    for prefix, key in (("ubuntu", "linux"), ("macos", "macos"), ("windows", "windows")):
        if runner.startswith(prefix):
            return key
    raise AssertionError(f"unsupported runner {runner!r}")


_CONTINUE = re.compile(r"^\$\{\{\s*matrix\.os\s*(==|!=)\s*'([^']+)'\s*\}\}$")


def _continue_on_error(value, matrix_os: str | None, where: str) -> bool:
    if value is None or isinstance(value, bool):
        return bool(value)
    match = _CONTINUE.match(str(value).strip())
    if not match or matrix_os is None:
        pytest.fail(f"{where}: continue-on-error expression {value!r} is unsupported; use a bool or ${{{{ matrix.os == 'x' }}}} / !=")
    return (matrix_os == match.group(2)) == (match.group(1) == "==")


def _pytest_commands(run: str) -> list[PytestCommand]:
    commands = []
    for line in re.sub(r"\\\n", " ", run).splitlines():
        if "pytest" not in line:
            continue
        tokens = shlex.split(line)
        rest = tokens[tokens.index("pytest") + 1:]
        expression, paths, i = None, [], 0
        while i < len(rest):
            token = rest[i]
            if token == "-m":
                expression = rest[i + 1]
                i += 1
            elif token.startswith("-m="):
                expression = token[3:]
            elif token == "-n":
                i += 1
            elif token.startswith("tests"):
                paths.append(token.split("::")[0])
            i += 1
        commands.append(PytestCommand(_default_marker_expression() if expression is None else expression, paths))
    return commands


def _jobs() -> dict[str, Job]:
    jobs: dict[str, Job] = {}
    for workflow in sorted(WORKFLOWS.glob("*.yml")):
        data = yaml.safe_load(workflow.read_text(encoding="utf-8"))
        triggers = data.get("on", data.get(True))  # PyYAML reads the key ``on`` as True
        triggers = {triggers} if isinstance(triggers, str) else set(triggers)
        for name, spec in data["jobs"].items():
            where = f"{workflow.name}:{name}"
            assert name not in jobs, f"{where}: job name used twice"
            runs_on = spec["runs-on"]
            if runs_on == "${{ matrix.os }}":
                runners = spec["strategy"]["matrix"]["os"]
            else:
                assert "${{" not in runs_on, f"{where}: unsupported runs-on {runs_on!r}"
                runners = [runs_on]
            oses = {}
            for runner in runners:
                blocking = not _continue_on_error(spec.get("continue-on-error"), runner, where)
                oses[_os_key(runner)] = blocking
            job = Job(workflow.name, name, oses, triggers=triggers)
            for step in spec["steps"]:
                if "run" in step:
                    job.commands.extend(_pytest_commands(step["run"]))
            jobs[name] = job
    return jobs


# --- the tests that use each entry -------------------------------------------------

@dataclass
class Use:
    file: str
    test: str
    marks: frozenset[str]  # lane markers on the test (module + class + function)
    hosts: frozenset[str]  # hosts every declared skip on the test lets it run on


def _mark_names(node: ast.AST) -> set[str]:
    """Names of every ``pytest.mark.X`` and every bare name inside a decorator / pytestmark expression."""
    names = set()
    for sub in ast.walk(node):
        if isinstance(sub, ast.Attribute):
            names.add(sub.attr)
        elif isinstance(sub, ast.Name):
            names.add(sub.id)
    return names


def _entry_for_mark_variable() -> dict[str, DeclaredSkip]:
    found = {}
    for attr, value in vars(lanes).items():
        if attr.startswith("requires_"):
            match = re.match(r"\[declared:([a-z0-9-]+)\]", value.kwargs["reason"])
            found[attr] = SKIP_REGISTRY[match.group(1)]
    return found


def _uses() -> dict[str, list[Use]]:
    """For each entry name, every test function that the entry guards."""
    by_variable = _entry_for_mark_variable()
    uses: dict[str, list[Use]] = {name: [] for name in SKIP_REGISTRY}
    for path in sorted(TESTS.glob("test_*.py")):
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        module_marks: set[str] = set()
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "pytestmark" for t in node.targets):
                module_marks |= _mark_names(node.value)

        def visit(body, inherited: set[str]):
            for node in body:
                if isinstance(node, ast.ClassDef):
                    visit(node.body, inherited | {n for d in node.decorator_list for n in _mark_names(d)})
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test"):
                    marks = inherited | {n for d in node.decorator_list for n in _mark_names(d)}
                    text = ast.get_source_segment(source, node) or ""
                    entries = {by_variable[n].name for n in marks if n in by_variable}
                    if "darwin_native" in marks:
                        entries.add("darwin-native")
                    entries |= {name for name, d in SKIP_REGISTRY.items() if d.only_error and f'"{name}"' in text}
                    hosts = frozenset(HOSTS)
                    for name in entries:
                        hosts &= SKIP_REGISTRY[name].runs_on()
                    for name in entries:
                        uses[name].append(Use(path.name, node.name, frozenset(marks & LANE_NAMES), hosts))

        visit(tree.body, module_marks)
    return uses


def _selects(command: PytestCommand, use: Use) -> bool:
    if command.paths and not any(
        (REPO / p).resolve() == (TESTS / use.file).resolve() or (REPO / p).resolve() in (TESTS / use.file).resolve().parents
        for p in command.paths
    ):
        return False
    if not command.marker_expression.strip():
        return True
    return Expression.compile(command.marker_expression).evaluate(lambda name: name in use.marks)


def _running(entry: DeclaredSkip, job: Job, uses: list[Use]) -> set[str]:
    """The runner OSes of ``job`` where it selects a test that uses ``entry`` on a host the test runs on."""
    return {
        os_key
        for os_key in job.oses
        for use in uses
        if os_key in use.hosts and os_key in entry.runs_on() and any(_selects(c, use) for c in job.commands)
    }


# --- the checks ------------------------------------------------------------------------

def test_every_condition_evaluates_on_every_host() -> None:
    for entry in SKIP_REGISTRY.values():
        for host in HOSTS.values():
            assert isinstance(entry.applies(host), bool), (entry.name, host)


def test_every_entry_has_tests_and_a_condition_that_lets_some_host_run_them() -> None:
    uses = _uses()
    for entry in SKIP_REGISTRY.values():
        assert uses[entry.name], f"{entry.name}: no test uses this entry"
        assert entry.runs_on(), f"{entry.name}: the condition skips on every host"


def test_every_declared_job_exists_and_runs_a_test_of_the_entry() -> None:
    jobs, uses, problems = _jobs(), _uses(), []
    for entry in SKIP_REGISTRY.values():
        if not entry.ci:
            problems.append(f"{entry.name}: no CI job runs it where the condition is false")
        for name in entry.ci:
            if name not in jobs:
                problems.append(f"{entry.name}: no such CI job {name!r}")
            elif not _running(entry, jobs[name], uses[entry.name]):
                problems.append(
                    f"{entry.name}: job {name!r} selects no test that uses it on a runner OS in {sorted(entry.runs_on())} "
                    f"(job OSes {sorted(jobs[name].oses)}, -m {[c.marker_expression for c in jobs[name].commands]})"
                )
    assert not problems, "\n".join(problems)


def test_no_undeclared_job_runs_a_test_of_the_entry() -> None:
    jobs, uses = _jobs(), _uses()
    problems = [
        f"{entry.name}: job {name!r} also runs it; add it to ci"
        for entry in SKIP_REGISTRY.values()
        for name, job in jobs.items()
        if name not in entry.ci and _running(entry, job, uses[entry.name])
    ]
    assert not problems, "\n".join(problems)


def test_some_declared_job_runs_automatically() -> None:
    jobs = _jobs()
    problems = [
        f"{entry.name}: its jobs {entry.ci} are triggered only by {sorted(set().union(*(jobs[j].triggers for j in entry.ci)))}"
        for entry in SKIP_REGISTRY.values()
        if not AUTOMATIC_TRIGGERS & set().union(*(jobs[j].triggers for j in entry.ci))
    ]
    assert not problems, "\n".join(problems)


def test_blocking_says_whether_any_job_that_runs_the_test_can_fail_ci() -> None:
    jobs, uses, problems = _jobs(), _uses(), []
    for entry in SKIP_REGISTRY.values():
        pairs = {
            (name, os_key): jobs[name].oses[os_key]
            for name in entry.ci
            for os_key in _running(entry, jobs[name], uses[entry.name])
        }
        computed = any(pairs.values())
        if computed != entry.blocking:
            problems.append(
                f"{entry.name}: blocking={entry.blocking} but the workflows say blocking={computed} "
                f"(pairs {sorted(pairs.items())}; True = job fails CI on that OS)"
            )
    assert not problems, "\n".join(problems)


def test_continue_on_error_expressions_are_supported_forms() -> None:
    assert _jobs()  # _continue_on_error fails the test for any form it cannot evaluate
