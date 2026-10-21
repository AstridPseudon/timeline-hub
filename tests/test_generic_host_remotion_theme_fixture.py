"""Offline contract for the normal imported-theme host fixture bootstrap."""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "tests" / "integrations" / "test_generic_host_remotion_render.py"


def _theme_test() -> ast.FunctionDef:
    tree = ast.parse(TARGET.read_text(encoding="utf-8"), filename=str(TARGET))
    return next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "test_generic_host_normal_imported_theme_reaches_props_and_rejects_local_source"
    )


def _calls(node: ast.AST, name: str) -> list[ast.Call]:
    return [
        child
        for child in ast.walk(node)
        if isinstance(child, ast.Call)
        and (
            (isinstance(child.func, ast.Attribute) and child.func.attr == name)
            or (isinstance(child.func, ast.Name) and child.func.id == name)
        )
    ]


def test_theme_fixture_reuses_canonical_worker_binding_before_sdk_invocation() -> None:
    """Lock the setup contract without starting Runtime or invoking the SDK."""
    source = TARGET.read_text(encoding="utf-8")
    function = _theme_test()
    lines = source.splitlines()

    host_call = next(
        call
        for call in ast.walk(function)
        if isinstance(call, ast.Call)
        and isinstance(call.func, ast.Name)
        and call.func.id == "GenericPackHost"
    )
    host_args = {keyword.arg: keyword.value for keyword in host_call.keywords}
    assert isinstance(host_args["executor_id"], ast.Name)
    assert host_args["executor_id"].id == "PACK_HOST_ACTOR"

    runtime_clients = _calls(function, "RuntimeProtocolClient")
    assert len(runtime_clients) == 1
    worker_token = runtime_clients[0].args[1]
    assert isinstance(worker_token, ast.Attribute)
    assert isinstance(worker_token.value, ast.Name)
    assert worker_token.value.id == "daemon"
    assert worker_token.attr == "worker_token"

    owner_open = next(
        call
        for call in ast.walk(function)
        if isinstance(call, ast.Call)
        and isinstance(call.func, ast.Attribute)
        and call.func.attr == "open"
        and isinstance(call.func.value, ast.Name)
        and call.func.value.id == "AstridClient"
    )
    owner_credential = next(
        keyword.value for keyword in owner_open.keywords if keyword.arg == "credential"
    )
    assert isinstance(owner_credential, ast.Attribute)
    assert isinstance(owner_credential.value, ast.Name)
    assert owner_credential.value.id == "daemon"
    assert owner_credential.attr == "credential_path"

    import_lines = [call.lineno for call in _calls(function, "import_file")]
    register_line = next(call.lineno for call in _calls(function, "register"))
    invoke_line = next(
        call.lineno
        for call in ast.walk(function)
        if isinstance(call, ast.Call)
        and isinstance(call.func, ast.Attribute)
        and call.func.attr == "invoke"
        and isinstance(call.func.value, ast.Name)
        and call.func.value.id == "sdk"
    )
    assert len(import_lines) == 3
    assert max(import_lines) < register_line < invoke_line

    # Keep this regression about the normal fixture only: the unsupported
    # production_worker_credentials option must not be added to this setup.
    theme_source = "\n".join(lines[function.lineno - 1 : function.end_lineno])
    assert "production_worker_credentials" not in theme_source
