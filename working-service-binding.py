"""Bind the reviewed ordinary working-venv inputs to a retained test template.

This module is deliberately a small seam for ``caller-publication.py``.  It
does not discover, install, provision, or execute a service.  The caller must
first authenticate the current recipe facts and pass them here.  Only the
explicit historical child-environment region is rendered; the caller remains
responsible for its source, readiness, native, history, wait, and request
guards.
"""

from __future__ import annotations

import hashlib
import json
import re
import shlex
from typing import Any, Mapping


P2_TEMPLATE = "full-e2e-three-products"
P3_TEMPLATE = "ap2-P3-gate5-h6-0348"
_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")

_CLIENT_FILES = {
    "astrid_runtime_client/__init__.py",
    "astrid_runtime_client/generated.py",
    "astrid_runtime_client/contract_metadata.py",
    "astrid_runtime_client/timeline_commit_types.py",
}
_RUNTIME_ARTIFACTS = {
    "/home/user/work/runtime/contract/artifacts.json",
    "/home/user/work/runtime/contract/component-manifest.json",
    "/home/user/work/runtime/contract/schemas/timeline-config.schema.json",
    "/home/user/work/runtime/runtime_protocol/schemas/timeline-commit-bundle.json",
}

# The suite rows are approved byte-for-byte.  The only mutable span is the
# old child environment block.  Offsets and hashes are deliberately fixed so
# an injected earlier/duplicate marker cannot move the boundary.
_TEMPLATE_APPROVALS = {
    "2": {
        "source_sha256": "c742ca50de0fc387b5476dfe7e06a205b90ad66adf2c70d58e0b044f349b9c13",
        "start": 5831, "end": 23833,
        "prefix_sha256": "529110cf1c6de13e0f9191d5308d69122b593eb7c51259fa6ce46e6ad924e540",
        "suffix_sha256": "096a73e76143252438b1fb4ac71a769105157943b3acb39d12c9dfc78191149f",
        "environment_bytes": 2482,
    },
    "3": {
        "source_sha256": "d4fe6b9064e3e827179da2efe62630ad4cc3c58d2f2fdd88a541f4bb23fb7bf3",
        "start": 6465, "end": 24291,
        "prefix_sha256": "19696d61596680c6498a34bdf0a8fa3c86392bed20567b6b321bf90feba04a53",
        "suffix_sha256": "e847d99ff5beb9759afce3f45005a2b68215dbf349b1fcb6843fc585a06d39a9",
        "environment_bytes": 2482,
    },
}

class BindingError(ValueError):
    """The supplied facts or template are not an authenticated match."""


def _fail(message: str) -> "None":
    raise BindingError(message)


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value:
        _fail(f"missing non-empty fact: {name}")
    return value


def _absolute(value: Any, name: str) -> str:
    result = _text(value, name)
    if not result.startswith("/") or "\x00" in result:
        _fail(f"non-absolute fact: {name}")
    return result


def _digest(value: Any, name: str, width: int) -> str:
    result = _text(value, name)
    pattern = _HEX40 if width == 40 else _HEX64
    if pattern.fullmatch(result) is None:
        _fail(f"invalid digest fact: {name}")
    return result


def _source(recipe: Mapping[str, Any], role: str) -> dict[str, Any]:
    sources = recipe.get("source")
    if not isinstance(sources, Mapping) or not isinstance(sources.get(role), Mapping):
        _fail(f"missing source facts: {role}")
    value = dict(sources[role])
    value["checkout"] = _absolute(value.get("checkout"), f"source.{role}.checkout")
    value["ref"] = _text(value.get("ref"), f"source.{role}.ref")
    value["head"] = _digest(value.get("head"), f"source.{role}.head", 40)
    value["tree"] = _digest(value.get("tree"), f"source.{role}.tree", 40)
    parents = value.get("parents")
    if not isinstance(parents, list) or not parents or any(_HEX40.fullmatch(str(p)) is None for p in parents):
        _fail(f"invalid source parents: {role}")
    value["parents"] = tuple(str(parent) for parent in parents)
    return value


def _authenticated_snapshot(recipe: Mapping[str, Any]) -> Mapping[str, Any]:
    snapshot = recipe.get("_authenticated_snapshot")
    if not isinstance(snapshot, Mapping):
        _fail("recipe has no authenticated current snapshot")
    value = dict(recipe)
    value.pop("_authenticated_snapshot", None)
    digest = hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if snapshot.get("digest") != digest:
        _fail("recipe facts changed after current snapshot authentication")
    checks = snapshot.get("checks")
    if not isinstance(checks, Mapping) or not all(key in checks for key in ("probes", "client", "remotion", "composition", "runtime_bindings")):
        _fail("authenticated current snapshot is incomplete")
    return snapshot


def _recipe_bindings(recipe: Mapping[str, Any]) -> dict[str, str]:
    """Return only facts usable by the retained shell environment."""

    if recipe.get("status") != "qualified_existing_inputs_not_live":
        _fail("recipe is not the independently qualified current-input recipe")
    _authenticated_snapshot(recipe)
    policy = recipe.get("policy")
    if not isinstance(policy, Mapping) or "historical_receipts" not in policy:
        _fail("recipe policy does not declare historical receipts as context only")
    for forbidden in ("child", "child_identity", "child_receipt", "current_child"):
        if forbidden in recipe or forbidden in policy:
            _fail(f"historical child metadata cannot authenticate current inputs: {forbidden}")

    app = _source(recipe, "app")
    agent = _source(recipe, "agent")
    runtime = _source(recipe, "runtime")
    interpreters = recipe.get("interpreters")
    if not isinstance(interpreters, Mapping):
        _fail("missing interpreter facts")
    agent_interpreter = interpreters.get("agent")
    runtime_interpreter = interpreters.get("runtime")
    if not isinstance(agent_interpreter, Mapping) or not isinstance(runtime_interpreter, Mapping):
        _fail("missing agent/runtime interpreter facts")
    agent_python = _absolute(agent_interpreter.get("path"), "interpreters.agent.path")
    runtime_python = _absolute(runtime_interpreter.get("path"), "interpreters.runtime.path")
    if recipe.get("pythonpath") not in (None, ""):
        _fail("recipe must be qualified with PYTHONPATH unset")

    client = recipe.get("client_contract")
    if not isinstance(client, Mapping):
        _fail("missing generated client contract facts")
    _text(client.get("contract_version"), "client_contract.contract_version")
    _text(client.get("schema_digest"), "client_contract.schema_digest")
    files = client.get("files")
    artifacts = client.get("runtime_artifacts")
    if not isinstance(files, Mapping) or not files or not isinstance(artifacts, Mapping) or not artifacts:
        _fail("generated client/runtime artifact inventory is incomplete")
    if set(files) != _CLIENT_FILES:
        _fail("generated client file mapping is not an authenticated current mapping")
    for key, value in files.items():
        _digest(value, f"client_contract.files.{key}", 64)
    if set(artifacts) != _RUNTIME_ARTIFACTS:
        _fail("Runtime artifact mapping is not an authenticated current mapping")
    for key, value in artifacts.items():
        _digest(value, f"client_contract.runtime_artifacts.{key}", 64)

    remotion = recipe.get("remotion")
    composition = recipe.get("composition")
    environment = recipe.get("environment")
    if not isinstance(remotion, Mapping) or not isinstance(composition, Mapping) or not isinstance(environment, Mapping):
        _fail("ordinary Remotion, graph, and environment facts are required")
    historical = _text(remotion.get("historical_source_commit_marker"), "remotion.historical_source_commit_marker")
    if historical != "079580ca46af77e0292d49dc34386b25c8391f99":
        _fail("Remotion historical marker is not the approved bench marker")
    values = {
        "agent_checkout": agent["checkout"],
        "agent_head": agent["head"],
        "agent_tree": agent["tree"],
        "runtime_checkout": runtime["checkout"],
        "runtime_head": runtime["head"],
        "runtime_tree": runtime["tree"],
        "app_head": app["head"],
        "app_tree": app["tree"],
        "agent_python": agent_python,
        "runtime_python": runtime_python,
        "remotion_project": _absolute(environment.get("ASTRID_REMOTION_PROJECT_DIR"), "environment.ASTRID_REMOTION_PROJECT_DIR"),
        "node": _absolute(environment.get("ASTRID_NODE_EXECUTABLE"), "environment.ASTRID_NODE_EXECUTABLE"),
        "schema_pythonpath": _absolute(environment.get("ASTRID_TIMELINE_SCHEMA_PYTHONPATH"), "environment.ASTRID_TIMELINE_SCHEMA_PYTHONPATH"),
        "environment_file": _absolute(environment.get("file"), "environment.file"),
        "graph": _absolute(composition.get("qualified_graph"), "composition.qualified_graph"),
        "bench": _absolute(remotion.get("bench"), "remotion.bench"),
        "remotion_lock": _digest(remotion.get("package_lock_sha256"), "remotion.package_lock_sha256", 64),
        "remotion_tree": _digest(remotion.get("current_agent_remotion_tree"), "remotion.current_agent_remotion_tree", 40),
        "node_version": _text(remotion.get("node"), "remotion.node"),
        "npm_version": _text(remotion.get("npm"), "remotion.npm"),
        "graph_version": _text(composition.get("version"), "composition.version"),
        "graph_file_map": _digest(composition.get("file_map_sha256"), "composition.file_map_sha256", 64),
        "composition_artifact": _digest(composition.get("artifact_sha256"), "composition.artifact_sha256", 64),
    }
    if client.get("source_roots") != [
        "/home/user/work/agent/astrid_runtime_client",
        "/home/user/work/runtime/packages/python/astrid_runtime_client",
    ]:
        _fail("generated client source roots are not the authenticated current roots")
    if composition.get("package") != "@banodoco/timeline-composition":
        _fail("unexpected Composition graph identity")
    return values


def authenticated_bindings(recipe: Mapping[str, Any]) -> dict[str, str]:
    """Validate authenticated recipe facts and return ordinary bindings.

    The returned mapping contains no child name, receipt, or historical source
    identity.  It is safe for the caller to use as named substitutions only.
    """

    return _recipe_bindings(recipe).copy()


def _region(template: str, stage: str) -> tuple[int, int]:
    if stage not in {"2", "3"}:
        _fail(f"unsupported preflight stage: {stage}")
    approval = _TEMPLATE_APPROVALS[stage]
    if hashlib.sha256(template.encode()).hexdigest() != approval["source_sha256"]:
        _fail(f"{stage} template is not the approved retained source")
    start = template.find(f'test -f "$P{stage}O/queue/done')
    end_marker = f'if test -n "$P{stage}FAIL"; then'
    end = template.find(end_marker, start)
    if (
        start != approval["start"]
        or end != approval["end"]
        or template.count("STORE_ROOT=") != 1
        or template.find(end_marker, start) != approval["end"]
    ):
        _fail(f"{stage} child environment boundary is not unique")
    if (
        hashlib.sha256(template[:start].encode()).hexdigest() != approval["prefix_sha256"]
        or hashlib.sha256(template[end:].encode()).hexdigest() != approval["suffix_sha256"]
    ):
        _fail(f"{stage} protected template boundary is not approved")
    if "childvenv-" not in template[start:end] and "CHILD_PATH" not in template[start:end]:
        _fail(f"{stage} template is not the historical child-only region")
    return start, end


def _shell(value: str) -> str:
    return shlex.quote(value)


def _ordinary_region(stage: str, values: Mapping[str, str]) -> str:
    p = f"P{stage}"
    # This is intentionally explicit.  It is not a token-replacement pass and
    # it does not create a child identity or receipt.
    return "; ".join(
        (
            f"RDIR={_shell(values['remotion_project'])}",
            f"RENV={_shell(values['environment_file'])}",
            f"NODE={_shell(values['node'])}",
            f"GRAPH={_shell(values['graph'])}",
            f"CPY={_shell(values['agent_python'])}",
            f"RCPY={_shell(values['runtime_python'])}",
            f"RLOCK={_shell(values['remotion_lock'])}",
            f"REMOTION_TREE={_shell(values['remotion_tree'])}",
            'ASTRID_AGENT_PYTHON="$CPY"',
            'ASTRID_RUNTIME_PYTHON="$RCPY"',
            f"test \"${p}AG\" = {_shell(values['agent_checkout'])} || p{stage}fail Agent-working-venv-checkout",
            f"test \"${p}RT\" = {_shell(values['runtime_checkout'])} || p{stage}fail Runtime-working-venv-checkout",
            f"test \"${p}A\" = {_shell(values['agent_head'])} || p{stage}fail Agent-current-source",
            f"test \"${p}R\" = {_shell(values['runtime_head'])} || p{stage}fail Runtime-current-source",
            f"test \"${p}APP\" = {_shell(values['app_head'])} || p{stage}fail App-current-source",
            f"test \"${p}TREE\" = {_shell(values['app_tree'])} || p{stage}fail App-current-tree",
            f"test \"$(git -C \"${p}AG\" show -s --format=%T \"${p}A\" 2>/dev/null || true)\" = {_shell(values['agent_tree'])} || p{stage}fail Agent-current-tree",
            f"test \"$(git -C \"${p}RT\" show -s --format=%T \"${p}R\" 2>/dev/null || true)\" = {_shell(values['runtime_tree'])} || p{stage}fail Runtime-current-tree",
            f"test -x \"$CPY\" && test \"$CPY\" = {_shell(values['agent_python'])} || p{stage}fail Agent-interpreter-origin",
            f"test -x \"$RCPY\" && test \"$RCPY\" = {_shell(values['runtime_python'])} || p{stage}fail Runtime-interpreter-origin",
            f"test -x \"$NODE\" && test \"$NODE\" = {_shell(values['node'])} && test \"$($NODE --version 2>/dev/null)\" = {_shell(values['node_version'])} || p{stage}fail Remotion-node-origin",
            f"test -d \"$RDIR\" || p{stage}fail Remotion-project-origin",
            f"test -d \"$GRAPH/@banodoco/timeline-composition\" && test \"$(find \"$GRAPH/@banodoco/timeline-composition\" -type f | wc -l | tr -d ' ')\" = 80 && test \"$($NODE -p \"require('$GRAPH/@banodoco/timeline-composition/package.json').version\" 2>/dev/null)\" = {_shell(values['graph_version'])} || p{stage}fail Composition-graph-origin",
            f"test -f \"$RENV\" || p{stage}fail Remotion-environment-file",
            f"test -z \"${{PYTHONPATH+x}}\" || p{stage}fail PYTHONPATH-must-be-unset",
        )
    ) + ";"


def adapt_environment_block(template: str, *, stage: str, recipe: Mapping[str, Any]) -> dict[str, Any]:
    """Replace only the decoded historical child-environment region.

    The result includes the exact source/body/environment-region hashes needed
    by the later caller join.  No shell command is executed here.
    """

    values = authenticated_bindings(recipe)
    start, end = _region(template, stage)
    replacement = _ordinary_region(stage, values)
    body = template[:start] + replacement + template[end:]
    if len(replacement.encode()) != _TEMPLATE_APPROVALS[stage]["environment_bytes"]:
        _fail(f"{stage} binding substitution changed the bounded environment size")
    return {
        "body": body,
        "stage": stage,
        "source_sha256": hashlib.sha256(template.encode()).hexdigest(),
        "body_sha256": hashlib.sha256(body.encode()).hexdigest(),
        "environment_region_sha256": hashlib.sha256(replacement.encode()).hexdigest(),
        "environment_region_bytes": len(replacement.encode()),
        "protected_prefix_sha256": hashlib.sha256(template[:start].encode()).hexdigest(),
        "protected_suffix_sha256": hashlib.sha256(template[end:].encode()).hexdigest(),
        "launch_bindings": {"Agent": "CPY", "Runtime": "RCPY"},
        "bindings": values,
        "seam": f"caller-publication.py rebind() -> adapt_environment_block(body, stage='{stage}', recipe=facts)",
    }


def bind_environment(recipe: Mapping[str, Any]) -> dict[str, str]:
    """Compatibility name for the production caller's final join."""

    return authenticated_bindings(recipe)

