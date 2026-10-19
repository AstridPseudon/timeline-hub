from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest

from astrid.services import service_declaration


def test_declaration_matches_runtime_contract_with_space_containing_paths(tmp_path):
    source = tmp_path / "agent checkout"
    root = tmp_path / "workspace data"
    python = str(tmp_path / "python environment" / "python")
    bun = str(tmp_path / "Bun tools" / "bun")
    declaration = service_declaration(source_checkout=source, data_root=root, python=python, bun=bun)
    schema = json.loads((Path(__file__).parent / "fixtures" / "services.schema.json").read_text())
    jsonschema.validate(declaration, schema)
    host, chat = declaration["services"]
    assert host["argv"][0] == python
    assert host["argv"][host["argv"].index("--source-checkout") + 1] == str(source)
    assert host["argv"][host["argv"].index("--support-root") + 1] == str(root / "runtime")
    assert chat["argv"] == [bun, str(Path(__file__).parents[1] / "astrid/chat/service.mjs")]
    assert chat["env"]["ASTRID_WORKSPACE_DISCOVERY"] == str(root / "runtime/discovery.json")
    assert chat["env"]["ASTRID_SUPPORT_ROOT"] == str(root)
    assert chat["env"]["ASTRID_ACP_CWD"] == str(root / "chat")
    assert chat["env"]["ASTRID_ACP_LOCAL_MEDIA_ONLY"] == "1"
    assert chat["env"]["ASTRID_SERVICE_PYTHON"] == python
    assert chat["env"]["ASTRID_ACP_COMMAND"] == "astrid"
    assert {row["restart"] for row in declaration["services"]} == {"always"}


def test_declaration_requires_absolute_interpreters_and_workspace(tmp_path, monkeypatch):
    monkeypatch.setattr("astrid.services.shutil.which", lambda _: None)
    with pytest.raises(ValueError, match="Bun 1.3.14"):
        service_declaration(source_checkout=tmp_path, data_root=tmp_path)
    with pytest.raises(ValueError, match="must be absolute"):
        service_declaration(source_checkout=Path("relative"), data_root=tmp_path)
    with pytest.raises(ValueError, match="interpreters must be absolute"):
        service_declaration(source_checkout=tmp_path, data_root=tmp_path, bun="bun")


def test_declaration_retains_the_existing_chat_store_and_profile(tmp_path, monkeypatch):
    monkeypatch.setenv("ASTRID_ACP_CWD", str(tmp_path / "previous app cwd"))
    monkeypatch.setenv("ASTRID_ACP_SESSION_DIR", str(tmp_path / "sessions"))
    monkeypatch.setenv("ASTRID_ACP_PROFILE", "existing-profile")
    monkeypatch.setenv("ASTRID_ACP_COMMAND", str(tmp_path / "installed astrid"))
    declaration = service_declaration(source_checkout=tmp_path, data_root=tmp_path,
        python=str(tmp_path / "python"), bun=str(tmp_path / "bun"))
    chat = declaration["services"][1]["env"]
    assert chat["ASTRID_ACP_CWD"] == str(tmp_path / "previous app cwd")
    assert chat["ASTRID_ACP_SESSION_DIR"] == str(tmp_path / "sessions")
    assert chat["ASTRID_ACP_PROFILE"] == "existing-profile"
    assert chat["ASTRID_ACP_COMMAND"] == str(tmp_path / "installed astrid")
    assert "ASTRID_ACP_BRIDGE_TOKEN" not in chat
