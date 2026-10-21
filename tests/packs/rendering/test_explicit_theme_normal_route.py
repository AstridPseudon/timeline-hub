"""Offline controls for the ordinary imported-theme render input."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.core.execution.generic_host import GenericPackHost, HostError

ROOT = Path(__file__).resolve().parents[3]


def _render_record():
    host = GenericPackHost(pack_roots=[ROOT / "astrid" / "packs"])
    return next(item for item in host.discover() if item.id == "rendering.render")


def test_normal_render_discovery_declares_only_the_existing_theme_file_port() -> None:
    record = _render_record()
    names = {port.name for port in record.definition.inputs}

    assert "theme" in names
    assert "themeSource" not in names
    assert "theme_source" not in names


def test_normal_render_input_rejects_a_caller_local_theme_path(tmp_path: Path) -> None:
    forged = tmp_path / "forged-theme.json"
    forged.write_text('{"id":"caller-invented"}\n', encoding="utf-8")
    host = GenericPackHost(
        pack_roots=[ROOT / "astrid" / "packs"],
        client=SimpleNamespace(get_object=lambda _digest: b""),
    )

    with pytest.raises(HostError, match="requires a managed Runtime object"):
        host._materialize_inputs(
            {
                "spec": {"inputs": {"theme": str(forged)}},
                "input_object_ids": [],
            },
            tmp_path / "attempt",
            file_input_names=frozenset({"theme"}),
        )
