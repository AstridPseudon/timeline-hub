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
import re
import shlex
from typing import Any, Mapping


P2_TEMPLATE = "full-e2e-three-products"
P3_TEMPLATE = "ap2-P3-gate5-h6-0348"
_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")

# These are the reviewed recipe's identity facts, not a new source route.  A
# caller with a different tuple must be re-qualified before this seam is used.
_QUALIFIED = {
    "app_head": "bbed290db3a062fc9282940f580c14cf701cfbf8",
    "app_tree": "e68346571bc405e21ed05e037728a60d52885d9b",
    "agent_head": "cba425b61958f380f25b7bdea83d23c92f627761",
    "agent_tree": "d19ce2e55ce9f29e18a504fb9c97178764272bbe",
    "runtime_head": "becfe6db88b2cc034dba3fafa6c050117cdf2b06",
    "runtime_tree": "7edc08e3fe94edcbc8ef695c479f4de301789b89",
    "agent_python": "/home/user/work/venv-agent/bin/python",
    "runtime_python": "/home/user/work/venv-runtime/bin/python",
    "node": "/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node",
    "remotion_project": "/home/user/work/runtimes/agent-remotion",
    "schema_pythonpath": "/home/user/work/venv-agent/lib/python3.13/site-packages",
    "environment_file": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agent-remotion.env",
    "graph": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P1-local-OPS-1830/private819acf-D19/node_modules",
    "remotion_tree": "b01dca9b3b24f54093c20b7c5657316f997725db",
    "node_version": "v20.19.4",
    "npm_version": "10.8.2",
    "graph_version": "0.0.14",
    "graph_file_map": "2de838a6299aeeac771d28231321e7b23b4db90d76f472eed94df0eb9e46a556",
    "composition_artifact": "819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234",
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
    value["head"] = _digest(value.get("head"), f"source.{role}.head", 40)
    value["tree"] = _digest(value.get("tree"), f"source.{role}.tree", 40)
    parents = value.get("parents")
    if parents is None:
        parent = value.get("parent")
        parents = [parent] if isinstance(parent, str) else None
    if not isinstance(parents, list) or not parents or any(_HEX40.fullmatch(str(p)) is None for p in parents):
        _fail(f"invalid source parents: {role}")
    value["parents"] = tuple(str(parent) for parent in parents)
    return value


def _recipe_bindings(recipe: Mapping[str, Any]) -> dict[str, str]:
    """Return only facts usable by the retained shell environment."""

    if recipe.get("status") != "qualified_existing_inputs_not_live":
        _fail("recipe is not the independently qualified current-input recipe")
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
    for name, digest in files.items():
        _digest(digest, f"client_contract.files.{name}", 64)
    for name, digest in artifacts.items():
        _digest(digest, f"client_contract.runtime_artifacts.{name}", 64)

    remotion = recipe.get("remotion")
    composition = recipe.get("composition")
    environment = recipe.get("environment")
    if not isinstance(remotion, Mapping) or not isinstance(composition, Mapping) or not isinstance(environment, Mapping):
        _fail("ordinary Remotion, graph, and environment facts are required")
    historical = _text(remotion.get("historical_source_commit_marker"), "remotion.historical_source_commit_marker")
    if historical == agent["head"]:
        _fail("historical Remotion marker must not be relabeled as current Agent source")
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
        "remotion_tree": _digest(remotion.get("current_agent_remotion_tree"), "remotion.current_agent_remotion_tree", 40),
        "node_version": _text(remotion.get("node"), "remotion.node"),
        "npm_version": _text(remotion.get("npm"), "remotion.npm"),
        "graph_version": _text(composition.get("version"), "composition.version"),
        "graph_file_map": _digest(composition.get("file_map_sha256"), "composition.file_map_sha256", 64),
        "composition_artifact": _digest(composition.get("artifact_sha256"), "composition.artifact_sha256", 64),
    }
    for key, expected in _QUALIFIED.items():
        if values.get(key) != expected:
            _fail(f"authenticated fact is not the reviewed current input: {key}")
    if app["checkout"] != "/home/user/work/app" or agent["checkout"] != "/home/user/work/agent" or runtime["checkout"] != "/home/user/work/runtime":
        _fail("source checkout is not the qualified normal integration checkout")
    if client.get("contract_version") != "0.2.14" or client.get("schema_digest") != "sha256:4118b1e26d30be43cb1a01649df0065fed6e55a528b8956364df8f4eedb413d2":
        _fail("generated client/schema identity is stale")
    if composition.get("package") != "@banodoco/timeline-composition" or composition.get("version") != "0.0.14":
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
    start = template.find("STORE_ROOT=")
    end_marker = f'if test -n "$P{stage}FAIL"; then'
    end = template.find(end_marker, start)
    if start < 0 or end < 0 or template.find("STORE_ROOT=", start + 1) >= 0:
        _fail(f"{stage} child environment boundary is not unique")
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
            f"test \"$P{p}AG\" = {_shell(values['agent_checkout'])} || p{stage}fail Agent-working-venv-checkout",
            f"test \"$P{p}RT\" = {_shell(values['runtime_checkout'])} || p{stage}fail Runtime-working-venv-checkout",
            f"test \"$P{p}A\" = {_shell(values['agent_head'])} || p{stage}fail Agent-current-source",
            f"test \"$P{p}R\" = {_shell(values['runtime_head'])} || p{stage}fail Runtime-current-source",
            f"test \"$P{p}APP\" = {_shell(values['app_head'])} || p{stage}fail App-current-source",
            f"test \"$P{p}TREE\" = {_shell(values['app_tree'])} || p{stage}fail App-current-tree",
            f"test \"$(git -C \"$P{p}AG\" show -s --format=%T \"$P{p}A\" 2>/dev/null || true)\" = {_shell(values['agent_tree'])} || p{stage}fail Agent-current-tree",
            f"test \"$(git -C \"$P{p}RT\" show -s --format=%T \"$P{p}R\" 2>/dev/null || true)\" = {_shell(values['runtime_tree'])} || p{stage}fail Runtime-current-tree",
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
    return {
        "body": body,
        "stage": stage,
        "source_sha256": hashlib.sha256(template.encode()).hexdigest(),
        "body_sha256": hashlib.sha256(body.encode()).hexdigest(),
        "environment_region_sha256": hashlib.sha256(replacement.encode()).hexdigest(),
        "environment_region_bytes": len(replacement.encode()),
        "protected_prefix_sha256": hashlib.sha256(template[:start].encode()).hexdigest(),
        "protected_suffix_sha256": hashlib.sha256(template[end:].encode()).hexdigest(),
        "bindings": values,
        "seam": f"caller-publication.py rebind() -> adapt_environment_block(body, stage='{stage}', recipe=facts)",
    }


def bind_environment(recipe: Mapping[str, Any]) -> dict[str, str]:
    """Compatibility name for the production caller's final join."""

    return authenticated_bindings(recipe)

