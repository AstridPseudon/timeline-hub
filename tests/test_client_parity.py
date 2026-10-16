from __future__ import annotations

import ast
import hashlib
import json
import re
import sys
from pathlib import Path

import pytest

from generators import generate


ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "packages" / "python"))
from banodoco_workspace_client.generated import OPERATIONS as PYTHON_OPERATIONS  # noqa: E402
from banodoco_workspace_client.generated import PROTOCOL as PYTHON_PROTOCOL  # noqa: E402


def _operation_ids() -> list[str]:
    return [
        line.split(":", 1)[1].strip()
        for line in (ROOT / "contract" / "openapi" / "workspace-v1.yaml").read_text().splitlines()
        if re.match(r"^\s+operationId:", line)
    ]


def _typescript_operations() -> list[str]:
    source = (ROOT / "packages" / "typescript" / "src" / "contract-metadata.ts").read_text()
    match = re.search(r"^export const OPERATIONS = (\[.*\]) as const;$", source, re.MULTILINE)
    assert match, "TypeScript contract metadata must export generated operations"
    return json.loads(match.group(1))


def _python_methods() -> set[str]:
    source = (ROOT / "packages" / "python" / "banodoco_workspace_client" / "generated.py").read_text()
    module = ast.parse(source)
    client = next(node for node in module.body if isinstance(node, ast.ClassDef) and node.name == "WorkspaceClient")
    return {
        node.name
        for node in client.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and not node.name.startswith("_")
    }


def _snake_case(operation: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", operation).lower()


def test_product_clients_match_canonical_contract_projection() -> None:
    manifest = json.loads((ROOT / "contract" / "manifest.json").read_text())
    component = json.loads((ROOT / "contract" / "component-manifest.json").read_text())
    typescript_source = (ROOT / "packages" / "typescript" / "src" / "generated.ts").read_text()
    typescript_methods = set(re.findall(r"^  async (\w+)\(", typescript_source, re.MULTILINE))
    operation_ids = _operation_ids()
    client_operations = generate.client_operation_index()
    rendered_python = generate.render_python_client()
    rendered_typescript = generate.render_typescript_client()
    rendered_typescript_methods = set(re.findall(r"^  async (\w+)\(", rendered_typescript, re.MULTILINE))

    assert manifest["protocol"] == component["protocol"] == "workspace.v1"
    assert manifest["generated"]["python"] == "packages/python/banodoco_workspace_client/generated.py"
    assert manifest["generated"]["typescript"] == "packages/typescript/src/generated.ts"
    assert list(PYTHON_OPERATIONS) == operation_ids
    assert _typescript_operations() == operation_ids
    # The product-facing clients retain one typed composition helper for the
    # cold-launch timeline save journey. It is implemented in terms of the
    # canonical document/timeline operations and is not an extra wire route.
    assert client_operations == [*operation_ids, "getProjectMediaSelectionForOutput"]
    python_wire_methods = {_snake_case(operation) for operation in operation_ids}
    python_helpers = {"update_timeline_document", "get_project_media_selection_for_output"}
    assert _python_methods() in (python_wire_methods | {"update_timeline_document"}, python_wire_methods | python_helpers)
    assert typescript_methods in (
        set(operation_ids) | {"updateTimelineDocument"},
        set(client_operations) | {"updateTimelineDocument"},
    )
    assert typescript_methods - set(operation_ids) in (
        {"updateTimelineDocument"},
        {"updateTimelineDocument", "getProjectMediaSelectionForOutput"},
    )
    # A006 intentionally defers checked-in snapshots until the coordinator's
    # single cross-repository generation. The in-memory renderers and both
    # validators already agree on the contract-owned alias.
    assert generate.validate_python_client(rendered_python) is None
    assert generate.validate_typescript_client(source=rendered_typescript) is None
    assert "get_project_media_selection_for_output" in rendered_python
    assert "getProjectMediaSelectionForOutput" in rendered_typescript_methods
    assert "getTimeline" not in typescript_methods
    assert "getProjectTimeline" in typescript_methods
    assert {"publishParentComposition", "getProjectShotRevision", "getProjectTimelineRevision"}.issubset(typescript_methods)
    assert {"publish_parent_composition", "get_project_shot_revision", "get_project_timeline_revision"}.issubset(_python_methods())
    assert "actual_target?: ExecutionTarget" in typescript_source
    assert "executor_incarnation?: string" in typescript_source
    assert "provider_state_unknown" in typescript_source
    assert "export interface ChildAuthorityRequest" in typescript_source
    assert "child?: ChildAuthorityChild" in typescript_source
    assert "derived_inputs?: DerivedInputDescriptor[]" in typescript_source
    assert "body: ChildAuthorityRequest" in typescript_source

    component_digest = "sha256:" + hashlib.sha256((ROOT / "contract" / "component-manifest.json").read_bytes()).hexdigest()
    contract_digest_value = generate.contract_digest()
    generated_metadata = generate.render()
    python_metadata = generated_metadata["packages/python/banodoco_workspace_client/contract_metadata.py"]
    typescript_metadata = generated_metadata["packages/typescript/src/contract-metadata.ts"]
    assert PYTHON_PROTOCOL == "workspace.v1"
    assert contract_digest_value in python_metadata
    assert f'COMPONENT_MANIFEST_SHA256 = "{component_digest}"' in typescript_metadata
    assert f'SCHEMA_DIGEST = "{contract_digest_value}"' in typescript_metadata


def test_recoverable_snapshot_client_projection_is_canonical() -> None:
    typescript = (ROOT / "packages/typescript/src/generated.ts").read_text()
    python = (ROOT / "packages/python/banodoco_workspace_client/generated.py").read_text()
    assert "publishRecoverableSnapshot" in _operation_ids()
    assert "publish_recoverable_snapshot" in _python_methods()
    assert "body: RecoverableSnapshotRequest" in typescript
    assert "Promise<MutationResult<ManagedOutput>>" in typescript
    assert '/recoverable-snapshots' in typescript and '/recoverable-snapshots' in python
    assert 'output: DerivedInputDescriptor' in typescript


def _with_output_alias(contract: str) -> str:
    assert contract.count("x-client-alias: getProjectMediaSelectionForOutput") == 1
    return contract


def _temporary_client_sources(tmp_path: Path, monkeypatch, contract: str) -> tuple[str, str]:
    contract_path = tmp_path / "contract/openapi/workspace-v1.yaml"
    contract_path.parent.mkdir(parents=True, exist_ok=True)
    contract_path.write_text(contract)
    monkeypatch.setattr(generate, "ROOT", tmp_path)
    python = (ROOT / "packages/python/banodoco_workspace_client/generated.py").read_text()
    marker = "\n\ndef _path_part("
    assert python.count(marker) == 1
    python = python.replace(
        marker,
        "\n    def get_project_media_selection_for_output(self):\n        pass\n" + marker,
    )
    typescript = (ROOT / "packages/typescript/src/generated.ts").read_text()
    target = tmp_path / "generated.ts"
    target.write_text(typescript + "\n  async getProjectMediaSelectionForOutput(): Promise<void> {}\n")
    monkeypatch.setattr(generate, "TYPESCRIPT_CLIENT_OUTPUT", target)
    return python, target.read_text()


def test_media_selection_alias_is_a_client_helper_not_a_wire_operation(tmp_path, monkeypatch) -> None:
    contract = _with_output_alias((ROOT / "contract/openapi/workspace-v1.yaml").read_text())
    python, typescript = _temporary_client_sources(tmp_path, monkeypatch, contract)
    assert "getProjectMediaSelectionForOutput" not in generate.operation_index()
    assert generate.client_operation_index() == [
        *generate.operation_index(), "getProjectMediaSelectionForOutput"
    ]
    assert generate.validate_python_client(python) is None
    assert generate.validate_typescript_client(source=typescript) is None


@pytest.mark.parametrize(("old", "new"), [
    ("operationId: getProjectMediaSelection\n", "operationId: changedMediaSelection\n"),
    ("/v1/projects/{project_id}/media-selection:\n    get:",
     "/v1/projects/{project_id}/media-selection:\n    post:"),
    ("/v1/projects/{project_id}/media-selection:", "/v1/projects/{project_id}/other-selection:"),
    ("x-client-alias: getProjectMediaSelectionForOutput", "x-client-alias: unexplainedOutputHelper"),
    ("[asset, generation_id, variant_id]", "[asset, generation_id]"),
    ("[association_id, object_id, version]", "[association_id, object_id]"),
    ("[association_id, object_id, version]", "[association_id, generation_id, version]"),
    ("      x-selector-forms: [[asset, generation_id, variant_id], [association_id, object_id, version]]\n", ""),
    ("- { name: version, in: query,", "- { name: changed_version, in: query,"),
])
def test_selector_alias_contract_drift_is_rejected(tmp_path, monkeypatch, old, new) -> None:
    contract = _with_output_alias((ROOT / "contract/openapi/workspace-v1.yaml").read_text())
    assert contract.count(old) == 1
    python, typescript = _temporary_client_sources(tmp_path, monkeypatch, contract.replace(old, new))
    with pytest.raises(SystemExit, match="unsupported client selector alias projection"):
        generate.client_operation_index()
    with pytest.raises(SystemExit, match="unsupported client selector alias projection"):
        generate.validate_python_client(python)
    with pytest.raises(SystemExit, match="unsupported client selector alias projection"):
        generate.validate_typescript_client(source=typescript)


def test_selector_alias_moved_to_another_operation_is_rejected(tmp_path, monkeypatch) -> None:
    contract = _with_output_alias((ROOT / "contract/openapi/workspace-v1.yaml").read_text())
    extension = (
        "      x-client-alias: getProjectMediaSelectionForOutput\n"
        "      x-selector-forms: [[asset, generation_id, variant_id], [association_id, object_id, version]]\n"
    )
    contract = contract.replace(extension, "").replace(
        "      operationId: health\n", "      operationId: health\n" + extension
    )
    python, typescript = _temporary_client_sources(tmp_path, monkeypatch, contract)
    with pytest.raises(SystemExit, match="unsupported client selector alias projection"):
        generate.client_operation_index()
    with pytest.raises(SystemExit, match="unsupported client selector alias projection"):
        generate.validate_python_client(python)
    with pytest.raises(SystemExit, match="unsupported client selector alias projection"):
        generate.validate_typescript_client(source=typescript)


def test_removed_contract_alias_rejects_extra_client_methods(tmp_path, monkeypatch) -> None:
    contract = (ROOT / "contract/openapi/workspace-v1.yaml").read_text()
    contract = contract.replace("      x-client-alias: getProjectMediaSelectionForOutput\n", "")
    contract = contract.replace(
        "      x-selector-forms: [[asset, generation_id, variant_id], [association_id, object_id, version]]\n", ""
    )
    python, typescript = _temporary_client_sources(tmp_path, monkeypatch, contract)
    with pytest.raises(SystemExit, match="Python client operation projection drifted"):
        generate.validate_python_client(python)
    with pytest.raises(SystemExit, match="TypeScript client operation projection drifted"):
        generate.validate_typescript_client(source=typescript)


def test_missing_contract_owned_alias_method_is_rejected() -> None:
    python = generate.render_python_client().replace(
        "def get_project_media_selection_for_output(", "def _removed_output_helper("
    )
    with pytest.raises(SystemExit, match="Python client operation projection drifted"):
        generate.validate_python_client(python)
    typescript = generate.render_typescript_client().replace(
        "async getProjectMediaSelectionForOutput(", "async removedOutputHelper("
    )
    with pytest.raises(SystemExit, match="TypeScript client operation projection drifted"):
        generate.validate_typescript_client(source=typescript)


def test_rendered_python_output_alias_encodes_and_retries_the_captured_tuple() -> None:
    namespace: dict[str, object] = {}
    exec(compile(generate.render_python_client(), "<rendered-workspace-client>", "exec"), namespace)
    client_type = namespace["WorkspaceClient"]
    calls = []
    result = {
        "asset": "variant/音", "generation_id": "generation", "variant_id": "variant/音",
        "object_id": "sha256:" + "a" * 64, "catalog_digest": "sha256:" + "b" * 64,
    }

    def transport(method, path, headers, body):
        calls.append((method, path, headers, body))
        return 200, {}, json.dumps(result).encode()

    client = client_type("http://unused", "reader", transport=transport)
    selectors = {"association_id": "output/音 +&", "object_id": result["object_id"], "version": 3}
    assert client.get_project_media_selection_for_output("p/ +", **selectors) == result
    assert client.get_project_media_selection_for_output("p/ +", **selectors) == result
    assert calls[0][0:2] == calls[1][0:2]
    assert calls[0][3] == calls[1][3]
    assert calls[0][0] == "GET" and calls[0][3] is None
    assert calls[0][2]["Authorization"] == "Bearer reader"
    assert calls[0][2]["X-Request-ID"] != calls[1][2]["X-Request-ID"]
    from urllib.parse import parse_qs, urlsplit
    assert urlsplit(calls[0][1]).path == "/v1/projects/p%2F%20%2B/media-selection"
    assert parse_qs(urlsplit(calls[0][1]).query) == {
        "association_id": [selectors["association_id"]],
        "object_id": [selectors["object_id"]],
        "version": ["3"],
    }
    for version in (True, 0, -1, 1.0):
        with pytest.raises(ValueError):
            client.get_project_media_selection_for_output("p", association_id="a", object_id="b", version=version)
    assert len(calls) == 2
