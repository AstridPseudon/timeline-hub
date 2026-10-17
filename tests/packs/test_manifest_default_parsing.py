"""Exercise first-party manifest defaults at their runtime parse boundary."""

from __future__ import annotations

import argparse
import importlib
import inspect
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

import pytest
import yaml

from astrid.core.execution.executor.actions import action_orchestrator_definition
from astrid.core.execution.executor.registry import _discover_executor_packs
from astrid.core.execution.executor.registry import load_default_registry
from astrid.core.execution.executor.runner import ExecutorRunRequest, build_executor_command
from astrid.core.execution.orchestrator.registry import OrchestratorRegistry
from astrid.core.execution.orchestrator.runner import (
    OrchestratorRunRequest,
    build_orchestrator_command,
)


ROOT = Path(__file__).resolve().parents[2]
PACKS_ROOT = ROOT / "astrid" / "packs"
REGISTRY = load_default_registry()
MANIFESTS = tuple(sorted(PACKS_ROOT.glob("*/pack.yaml")))
ACTION_CASES = tuple(
    (manifest, pack, name, action)
    for manifest in MANIFESTS
    for pack in (yaml.safe_load(manifest.read_text(encoding="utf-8")),)
    for name, action in (pack.get("actions") or {}).items()
)
DISCOVERED_PACKS = {
    pack.id: pack
    for pack in _discover_executor_packs(project_root=ROOT, extra_pack_roots=())
}
LOCAL_ORCHESTRATORS = {
    f"{pack['id']}.{name}": action_orchestrator_definition(
        DISCOVERED_PACKS[pack["id"]], name, action
    )
    for _manifest, pack, name, action in ACTION_CASES
    if action.get("metadata", {}).get("local_orchestrator") is True
}
ORCHESTRATOR_REGISTRY = OrchestratorRegistry(
    LOCAL_ORCHESTRATORS.values(), executor_registry=REGISTRY
)
NO_ACTION_PACKS = tuple(
    manifest.parent.name
    for manifest in MANIFESTS
    if not (yaml.safe_load(manifest.read_text(encoding="utf-8")).get("actions") or {})
)


def _defaults(action: dict[str, Any], pack_root: Path) -> dict[str, Any]:
    inputs = action.get("inputs")
    if isinstance(inputs, list):
        return {
            str(port["name"]): port["default"]
            for port in inputs
            if isinstance(port, dict) and "name" in port and "default" in port
        }
    if isinstance(inputs, str):
        schema = yaml.safe_load((pack_root / inputs).read_text(encoding="utf-8"))
        return {
            str(name): declaration["default"]
            for name, declaration in (schema.get("properties") or {}).items()
            if isinstance(declaration, dict) and "default" in declaration
        }
    return {}


def _port_flag(executor, port_name: str) -> str | None:
    command = getattr(executor, "command", None)
    if command is None and getattr(executor, "runtime", None) is not None:
        command = executor.runtime.command
    if command is None:
        return None
    for mapping in command.input_args:
        if mapping.input == port_name:
            return mapping.flag

    ports = {port.name: port for port in executor.inputs}
    port = ports[port_name]
    placeholders = {port_name}
    if port.placeholder:
        placeholders.add(port.placeholder)
    for index, token in enumerate(command.argv):
        names = set(re.findall(r"\{([A-Za-z_][A-Za-z0-9_.-]*)\}", token))
        if not (names & placeholders):
            continue
        if token.startswith("-") and "=" in token:
            return token.split("=", 1)[0]
        if index and command.argv[index - 1].startswith("-"):
            return command.argv[index - 1].split("=", 1)[0]

    skipped = set(executor.metadata.get("auto_forward_skip", ()))
    if executor.metadata.get("auto_forward_inputs") is not False and port_name not in skipped:
        return "--" + port_name.replace("_", "-")
    return None


def _parser_action(parser: argparse.ArgumentParser, port_name: str, flag: str | None):
    if flag and flag in parser._option_string_actions:
        return parser._option_string_actions[flag]
    normalized_names = {port_name, port_name.replace("-", "_")}
    for action in parser._actions:
        if not action.option_strings and action.dest in normalized_names:
            return action
    return None


def _sample_for_action(action, port, flag: str | None, tmp_path: Path):
    if action is not None and action.choices:
        return action.choices[0]
    if action is not None and action.nargs == 0:
        return True
    if action is not None and action.type is not None:
        if action.type is int:
            return 1
        if action.type is float:
            return 1.0
        if action.type is bool:
            return "true"
        if action.type is Path:
            return str(tmp_path / "input")
    if port.type in {"file", "path"}:
        return str(tmp_path / "input")
    if port.type == "directory":
        return str(tmp_path)
    if port.type == "json":
        return {}
    if port.type == "boolean":
        return True
    if port.type == "integer":
        return 1
    if port.type == "number":
        return 1.0
    return "fixture"


def _load_parser(executor, action_id: str, monkeypatch, module_name: str | None = None):
    monkeypatch.setenv("ASTRID_INTERNAL_INVOCATION", "1")
    if module_name is None:
        command = getattr(executor, "command", None)
        if command is None and getattr(executor, "runtime", None) is not None:
            command = executor.runtime.command
        module_name = command.argv[2]
    if action_id.startswith("generation.generate_image_"):
        module = importlib.import_module(
            "astrid.packs.generation.actions.generate_image.run"
        )
        return module.build_parser()
    if action_id == "video_editing.cut":
        # The parser has no dependency on this planner; keep the test focused
        # on argv parsing while making any accidental planner use fail loudly.
        timeline = importlib.import_module("astrid.core.timeline")
        if not hasattr(timeline, "compile_arrangement_plan"):
            monkeypatch.setattr(
                timeline,
                "compile_arrangement_plan",
                lambda *args, **kwargs: pytest.fail(
                    "default parser coverage must not invoke the cut planner"
                ),
                raising=False,
            )
    module = importlib.import_module(module_name)
    for builder_name in ("build_parser", "_build_parser", "_parser"):
        builder = getattr(module, builder_name, None)
        if callable(builder):
            required = [
                parameter
                for parameter in inspect.signature(builder).parameters.values()
                if parameter.default is inspect.Parameter.empty
                and parameter.kind
                in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
            ]
            return builder(*([None] * len(required)))
    if action_id == "rendering.render":
        return None
    raise AssertionError(f"{action_id} does not expose its declared command parser")


def _required_parser_args(parser, argv: list[str], tmp_path: Path) -> list[str]:
    result = list(argv)
    present = set(result)
    for action in parser._actions:
        if not action.required:
            continue
        if action.option_strings:
            if any(option in present for option in action.option_strings):
                continue
            option = action.option_strings[0]
            result.append(option)
            present.add(option)
        else:
            option = None
            if action.choices and any(token in action.choices for token in result):
                continue
        if action.nargs == 0:
            continue
        if action.choices:
            value = str(action.choices[0])
        elif action.type is int:
            value = "1"
        elif action.type is float:
            value = "1.0"
        elif action.type is Path:
            value = str(tmp_path / "input")
        else:
            value = "{}" if action.dest.endswith(("json", "config", "profile")) else "fixture"
        result.append(value)
        if option is None:
            present.add(value)
    return result


class _ParsedArgsCaptured(BaseException):
    def __init__(self, parser, namespace) -> None:
        self.parser = parser
        self.namespace = namespace


def _parse_render_command(module, argv: list[str], tmp_path: Path, monkeypatch):
    original = argparse.ArgumentParser.parse_args

    def capture(parser, args=None, namespace=None):
        tokens = _required_parser_args(parser, list(args or ()), tmp_path)
        parsed = original(parser, tokens, namespace)
        raise _ParsedArgsCaptured(parser, parsed)

    monkeypatch.setattr(argparse.ArgumentParser, "parse_args", capture)
    with pytest.raises(_ParsedArgsCaptured) as captured:
        module.main(argv)
    return captured.value.parser, captured.value.namespace


def _normalized(value: Any, expected: Any, port_type: str):
    if isinstance(value, Path):
        value = str(value)
    if port_type == "json" and isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            pass
    if isinstance(expected, Path):
        expected = str(expected)
    return value, expected


def _request_values(executor, condition_names: set[str], parser, tmp_path: Path):
    values = dict(executor.metadata.get("fixed_inputs") or {})
    defaults = {port.name: port.default for port in executor.inputs if port.default is not None}
    for name in condition_names:
        if name in defaults:
            values[name] = defaults[name]
    for port in executor.inputs:
        if port.name in values or port.name in defaults:
            continue
        if not port.required and port.name not in condition_names:
            continue
        flag = _port_flag(executor, port.name)
        action = _parser_action(parser, port.name, flag) if parser is not None else None
        values[port.name] = _sample_for_action(action, port, flag, tmp_path)
    return values


def _assert_default_mapping(
    executor,
    defaults,
    parser,
    namespace,
    action_id: str,
    argv: list[str],
) -> list[dict[str, Any]]:
    ports = {port.name: port for port in executor.inputs}
    assert set(defaults) <= set(ports), action_id
    mapped: set[str] = set()
    rows: list[dict[str, Any]] = []
    for name, expected in defaults.items():
        port = ports[name]
        flag = _port_flag(executor, name)
        parser_action = _parser_action(parser, name, flag)
        assert parser_action is not None, f"{action_id}.{name} has no parser destination"
        actual = getattr(namespace, parser_action.dest, argparse.SUPPRESS)
        supplied = bool(
            flag
            and any(token == flag or token.startswith(flag + "=") for token in argv)
        )
        if supplied:
            parsed_expected = expected
            if parser_action.type is not None:
                parsed_expected = parser_action.type(str(expected))
            if isinstance(parser_action, argparse._AppendAction):
                parsed_expected = (
                    [parser_action.type(str(item)) for item in expected]
                    if isinstance(expected, list) and parser_action.type is not None
                    else list(expected)
                    if isinstance(expected, list)
                    else [parsed_expected]
                )
            if parser_action.nargs == 0:
                parsed_expected = bool(expected)
            behavior = "explicit-argparse-conversion"
        elif parser_action.default is argparse.SUPPRESS:
            # video_editing.hype resolves suppressed argparse values to
            # manifest-backed pipeline values after parsing.
            assert action_id == "video_editing.hype", (
                f"{action_id}.{name} was suppressed without a runtime normalization rule"
            )
            parsed_expected = expected
            behavior = "runtime-normalized-suppressed-default"
        else:
            parsed_expected = parser_action.default
            behavior = (
                "omitted-empty-default"
                if expected == ""
                else "omitted-false-default"
                if expected is False
                else "omitted-parser-default"
            )

        actual, parsed_expected = _normalized(actual, parsed_expected, port.type)
        assert actual == parsed_expected, (
            f"{action_id}.{name} default {expected!r} mapped through "
            f"{flag or parser_action.dest} to {parser_action.dest} as {actual!r}; "
            f"expected parsed value {parsed_expected!r} ({behavior})"
        )
        mapped.add(name)
        rows.append(
            {
                "action_id": action_id,
                "input": name,
                "declared_default": expected,
                "runtime_flag": flag,
                "parser_destination": parser_action.dest,
                "parser_default": (
                    "<SUPPRESS>"
                    if parser_action.default is argparse.SUPPRESS
                    else parser_action.default
                ),
                "argv_supplied": supplied,
                "parsed_value": actual,
                "mapping": behavior,
            }
        )
    assert mapped == set(defaults)
    return rows


@pytest.fixture(scope="session")
def _default_mapping_rows() -> list[dict[str, Any]]:
    return []


@pytest.fixture(scope="session", autouse=True)
def _write_default_mapping_report(_default_mapping_rows):
    yield
    report_path = os.environ.get("ASTRID_DEFAULT_MAPPING_REPORT")
    if report_path:
        payload = {
            "inventory": {
                "manifests": len(MANIFESTS),
                "actions": len(ACTION_CASES),
                "declared_defaults": sum(
                    len(_defaults(action, manifest.parent))
                    for manifest, _pack, _name, action in ACTION_CASES
                ),
                "no_default_actions": [
                    f"{pack['id']}.{name}"
                    for manifest, pack, name, action in ACTION_CASES
                    if not _defaults(action, manifest.parent)
                ],
                "no_action_manifests": list(NO_ACTION_PACKS),
            },
            "mappings": sorted(
                _default_mapping_rows,
                key=lambda row: (row["action_id"], row["input"]),
            ),
        }
        path = Path(report_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def test_first_party_default_coverage_inventory_is_nonzero_and_complete() -> None:
    default_rows = [
        (f"{pack['id']}.{name}", input_name, value)
        for _manifest, pack, name, action in ACTION_CASES
        for input_name, value in _defaults(action, _manifest.parent).items()
    ]
    assert len(MANIFESTS) == 29
    assert len(ACTION_CASES) == 106
    assert len(default_rows) == 262
    assert len(default_rows) > 0
    assert NO_ACTION_PACKS == ("astrid_motion", "local", "story_views")


def test_actions_without_defaults_are_explicitly_empty() -> None:
    empty_actions = [
        (manifest, pack, name, action)
        for manifest, pack, name, action in ACTION_CASES
        if not _defaults(action, manifest.parent)
    ]
    assert empty_actions
    assert all(
        _defaults(action, manifest.parent) == {}
        for manifest, _pack, _name, action in empty_actions
    )


def test_manifests_without_actions_are_explicitly_counted() -> None:
    assert NO_ACTION_PACKS == ("astrid_motion", "local", "story_views")


def _exercise_action_defaults(
    manifest: Path,
    pack: dict[str, Any],
    action_name: str,
    action: dict[str, Any],
    tmp_path: Path,
    monkeypatch,
) -> list[dict[str, Any]]:
    action_id = f"{pack['id']}.{action_name}"
    defaults = _defaults(action, manifest.parent)
    if not defaults:
        return []

    is_local_orchestrator = action.get("metadata", {}).get("local_orchestrator") is True
    capability = (
        LOCAL_ORCHESTRATORS[action_id]
        if is_local_orchestrator
        else REGISTRY.get(action_id)
    )
    invocation = action["invocation"]
    if invocation["kind"] == "python":
        from astrid.core.execution.executor.runner import _action_input_values
        from astrid.sdk.actions import validate_action_inputs_definition

        values = _action_input_values(capability, ExecutorRunRequest(action_id, out=tmp_path))
        for port in capability.inputs:
            if port.required and port.name not in values:
                values[port.name] = _sample_for_action(None, port, None, tmp_path)
        validate_action_inputs_definition(capability, values)
        rows = []
        for name, expected in defaults.items():
            assert name in values, f"{action_id}.{name} default was not passed to the runtime"
            assert values[name] == expected, f"{action_id}.{name} default was not applied exactly"
            rows.append(
                {
                    "action_id": action_id,
                    "input": name,
                    "declared_default": expected,
                    "runtime_flag": None,
                    "parser_destination": "executor-inputs",
                    "parser_default": None,
                    "argv_supplied": True,
                    "parsed_value": values[name],
                    "mapping": "python-input-validation",
                    "runtime": "executor-python",
                }
            )
        assert set(defaults) <= set(values)
        return rows

    assert invocation["kind"] == "command", action_id
    module_name = action.get("metadata", {}).get("runtime_module")
    parser = _load_parser(capability, action_id, monkeypatch, module_name=module_name)
    if is_local_orchestrator:
        values = {
            port.name: port.default
            for port in capability.inputs
            if port.default is not None
        }
        for port in capability.inputs:
            if port.required and port.name not in values:
                values[port.name] = _sample_for_action(None, port, None, tmp_path)
        values.update(defaults)
    else:
        condition_names = {
            condition.input
            for condition in capability.conditions
            if condition.input
        }
        values = _request_values(capability, condition_names, parser, tmp_path)
        values.update(defaults)

    if action_id == "video_editing.hype":
        for port in capability.inputs:
            if port.type == "file" and values.get(port.name):
                fixture_path = Path(str(values[port.name]))
                fixture_path.parent.mkdir(parents=True, exist_ok=True)
                fixture_path.touch()

    out = tmp_path / "out"
    out.mkdir(exist_ok=True)
    if is_local_orchestrator:
        request = OrchestratorRunRequest(
            action_id,
            out=out,
            inputs=values,
            python_exec=sys.executable,
        )
        argv = list(build_orchestrator_command(request, ORCHESTRATOR_REGISTRY))
    else:
        request = ExecutorRunRequest(
            action_id,
            out=out,
            inputs=values,
            python_exec=sys.executable,
        )
        argv = list(build_executor_command(request, REGISTRY))
    assert len(argv) >= 3 and argv[1] == "-m", (action_id, argv)
    parser_argv = argv[3:]

    if parser is None:
        module = importlib.import_module(argv[2])
        parser, namespace = _parse_render_command(module, parser_argv, tmp_path, monkeypatch)
    elif action_id == "video_editing.hype":
        module = importlib.import_module(argv[2])
        namespace = module.resolve_args(_required_parser_args(parser, parser_argv, tmp_path))
    else:
        parsed_argv = _required_parser_args(parser, parser_argv, tmp_path)
        namespace = parser.parse_args(parsed_argv)

    rows = _assert_default_mapping(
        capability,
        defaults,
        parser,
        namespace,
        action_id,
        parser_argv,
    )
    for row in rows:
        row["runtime"] = "orchestrator-command" if is_local_orchestrator else "executor-command"
    return rows


@pytest.mark.parametrize(
    "manifest,pack,action_name,action",
    ACTION_CASES,
    ids=[f"{pack['id']}.{name}" for _manifest, pack, name, _action in ACTION_CASES],
)
def test_every_declared_action_default_parses_as_runtime_passes_it(
    manifest: Path,
    pack: dict[str, Any],
    action_name: str,
    action: dict[str, Any],
    tmp_path: Path,
    monkeypatch,
    _default_mapping_rows: list[dict[str, Any]],
) -> None:
    _default_mapping_rows.extend(
        _exercise_action_defaults(
            manifest,
            pack,
            action_name,
            action,
            tmp_path,
            monkeypatch,
        )
    )


def test_default_mapping_rows_cover_every_declared_default(
    _default_mapping_rows: list[dict[str, Any]],
) -> None:
    expected = {
        (f"{pack['id']}.{name}", input_name)
        for manifest, pack, name, action in ACTION_CASES
        for input_name in _defaults(action, manifest.parent)
    }
    actual = {(row["action_id"], row["input"]) for row in _default_mapping_rows}
    assert len(_default_mapping_rows) == 262
    assert actual == expected
    assert len(actual) == len(_default_mapping_rows)

