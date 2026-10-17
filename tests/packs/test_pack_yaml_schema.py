"""Runtime/schema parity for canonical first-party pack manifests."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import jsonschema
import pytest
import yaml

from astrid.core.pack import PackValidationError, load_pack_manifest


ROOT = Path(__file__).resolve().parents[2]
PACK_SCHEMA_DIR = ROOT / "astrid/core/pack/schemas"


def _body(extra: str = "", *, pack_id: str = "demo") -> str:
    return (
        "schema_version: 2\n"
        f"id: {pack_id}\n"
        "name: Demo\n"
        "version: 1.2.3\n"
        "capabilities: [testing]\n"
        f"{extra}"
    )


def _write(tmp_path: Path, body: str, *, folder: str = "demo") -> Path:
    root = tmp_path / folder
    root.mkdir()
    manifest = root / "pack.yaml"
    manifest.write_text(body, encoding="utf-8")
    return manifest


def _schema_errors_for_payload(payload: dict) -> list[jsonschema.ValidationError]:
    version = payload.get("schema_version")
    schema_version = version if type(version) is int and version in {1, 2, 3} else 2
    schema_path = PACK_SCHEMA_DIR / f"v{schema_version}" / "pack.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    return list(validator_cls(schema).iter_errors(payload))


def _schema_errors(body: str) -> list[jsonschema.ValidationError]:
    return _schema_errors_for_payload(yaml.safe_load(body))


def test_minimal_v2_manifest_loads_without_legacy_defaults(tmp_path: Path) -> None:
    pack = load_pack_manifest(_write(tmp_path, _body()))
    assert pack.id == "demo"
    assert pack.name == "Demo"
    assert pack.version == "1.2.3"
    assert pack.schema_version == "2"
    assert pack.root == (tmp_path / "demo").resolve()
    assert pack.metadata == {}


@pytest.mark.parametrize("version", ["1", "2.0", "'2'", "3"])
def test_only_exact_integer_schema_version_two_is_admitted(
    tmp_path: Path, version: str
) -> None:
    body = _body().replace("schema_version: 2", f"schema_version: {version}")
    with pytest.raises(PackValidationError):
        load_pack_manifest(_write(tmp_path, body))


@pytest.mark.parametrize("field", ["id", "name", "version"])
def test_identity_fields_are_required(tmp_path: Path, field: str) -> None:
    body = "\n".join(
        line for line in _body().splitlines() if not line.startswith(f"{field}:")
    ) + "\n"
    assert _schema_errors(body)
    with pytest.raises(PackValidationError):
        load_pack_manifest(_write(tmp_path, body))


def test_pack_id_must_match_folder(tmp_path: Path) -> None:
    with pytest.raises(PackValidationError, match="match folder name"):
        load_pack_manifest(_write(tmp_path, _body(pack_id="other")))


def test_alternate_manifest_filename_is_rejected(tmp_path: Path) -> None:
    root = tmp_path / "demo"
    root.mkdir()
    alternate = root / "pack.json"
    alternate.write_text(json.dumps(yaml.safe_load(_body())), encoding="utf-8")
    with pytest.raises(PackValidationError, match="pack.yaml"):
        load_pack_manifest(alternate)


@pytest.mark.parametrize(
    "retired_field",
    [
        "database: {}",
        "metadata: {}",
        "origin: external",
        "install_tier: optional",
        "pack_type: adapter",
    ],
)
def test_retired_authority_fields_fail_closed(
    tmp_path: Path, retired_field: str
) -> None:
    body = _body() + retired_field + "\n"
    assert _schema_errors(body)
    with pytest.raises(PackValidationError):
        load_pack_manifest(_write(tmp_path, body))


def test_permissions_round_trip(tmp_path: Path) -> None:
    body = _body(
        "permissions:\n"
        "  - id: network\n"
        "    reason: Calls hosted APIs.\n"
        "    services: [OpenAI, Replicate]\n"
    )
    assert _schema_errors(body) == []
    pack = load_pack_manifest(_write(tmp_path, body))
    assert [permission.to_dict() for permission in pack.permissions] == [
        {
            "id": "network",
            "reason": "Calls hosted APIs.",
            "services": ["OpenAI", "Replicate"],
        }
    ]


@pytest.mark.parametrize(
    "permission",
    [
        "  - id: network\n",
        "  - id: network\n    reason: ' '\n",
        "  - id: network\n    reason: ok\n    unknown: true\n",
    ],
)
def test_invalid_permission_shapes_reject(tmp_path: Path, permission: str) -> None:
    body = _body("permissions:\n" + permission)
    assert _schema_errors(body)
    with pytest.raises(PackValidationError):
        load_pack_manifest(_write(tmp_path, body))


def test_generation_extensions_preserve_normalized_shorthand(tmp_path: Path) -> None:
    body = _body(
        "extensions:\n"
        "  generation:\n"
        "    features: [t2i]\n"
        "    modes: [edit]\n"
    )
    pack = load_pack_manifest(_write(tmp_path, body))
    assert pack.extensions == {
        "generation": {"features": [{"id": "t2i"}], "modes": [{"id": "edit"}]}
    }


def test_rendering_extensions_round_trip(tmp_path: Path) -> None:
    body = _body(
        "extensions:\n"
        "  rendering:\n"
        "    renderers: [rendering/demo.renderer.yaml]\n"
        "    planners: []\n"
        "    finalizers: []\n"
    )
    assert _schema_errors(body) == []
    pack = load_pack_manifest(_write(tmp_path, body))
    assert pack.extensions["rendering"]["renderers"] == [
        "rendering/demo.renderer.yaml"
    ]


@pytest.mark.parametrize(
    "extension",
    [
        "rendering:\n    renderers: not-a-list\n",
        "rendering:\n    renderers: [rendering/demo.yaml, 7]\n",
        "rendering:\n    unknown: []\n",
        "unknown_extension: {}\n",
    ],
)
def test_v2_rendering_extensions_reject_malformed_and_unknown_fields(
    tmp_path: Path, extension: str
) -> None:
    body = _body("extensions:\n  " + extension.replace("\n", "\n  "))
    assert _schema_errors(body)
    with pytest.raises(PackValidationError):
        load_pack_manifest(_write(tmp_path, body))


def test_aliases_round_trip_and_remain_pack_owned(tmp_path: Path) -> None:
    body = _body(
        "aliases:\n"
        "  - kind: executor\n"
        "    alias: demo.legacy\n"
        "    canonical_id: demo.current\n"
    )
    pack = load_pack_manifest(_write(tmp_path, body))
    assert pack.to_dict()["aliases"] == [
        {
            "kind": "executor",
            "alias": "demo.legacy",
            "canonical_id": "demo.current",
        }
    ]


@pytest.mark.parametrize(
    "alias_block",
    [
        "aliases: [demo.legacy]\n",
        "aliases:\n  - kind: executor\n    alias: legacy\n    canonical_id: demo.current\n",
        "aliases:\n  - kind: executor\n    alias: demo.legacy\n    canonical_id: other.current\n",
        "aliases:\n  - kind: executor\n    alias: demo.legacy\n    canonical_id: demo.current\n    deprecated: true\n",
    ],
)
def test_invalid_or_legacy_alias_shapes_reject(
    tmp_path: Path, alias_block: str
) -> None:
    with pytest.raises(PackValidationError):
        load_pack_manifest(_write(tmp_path, _body(alias_block)))


def test_manifest_projection_is_json_serializable(tmp_path: Path) -> None:
    pack = load_pack_manifest(_write(tmp_path, _body()))
    assert json.loads(json.dumps(pack.to_dict()))["id"] == "demo"


def test_schema_and_runtime_both_accept_current_first_party_manifests() -> None:
    for manifest in sorted((ROOT / "astrid/packs").glob("*/pack.yaml")):
        body = manifest.read_text(encoding="utf-8")
        assert _schema_errors(body) == [], manifest
        assert load_pack_manifest(manifest).id == manifest.parent.name


def test_v3_rendering_declarations_reject_malformed_and_unknown_fields() -> None:
    manifest = ROOT / "astrid/packs/astrid_motion/pack.yaml"
    payload = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    assert payload["schema_version"] == 3

    unknown = copy.deepcopy(payload)
    unknown["rendering"]["effects/am-burst"]["unexpected"] = True
    assert _schema_errors_for_payload(unknown)

    malformed = copy.deepcopy(payload)
    malformed["rendering"]["effects/am-burst"]["resources"][0]["kind"] = 7
    assert _schema_errors_for_payload(malformed)
