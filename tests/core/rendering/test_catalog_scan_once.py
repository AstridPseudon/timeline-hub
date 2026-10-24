"""A registry load admits a shared source/project pack root only once."""

from __future__ import annotations

from pathlib import Path

import pytest

from astrid.core.element import registry as elements
from astrid.core.pack import PackValidationError, loader
from astrid.core.rendering import registry as rendering


def _pack(root: Path, name: str) -> Path:
    pack = root / name
    pack.mkdir(parents=True)
    (pack / "pack.yaml").write_text(
        f"schema_version: 2\nid: {name}\nname: {name}\nversion: 1.0.0\ncapabilities: []\n",
        encoding="utf-8",
    )
    return pack


@pytest.fixture(params=[rendering, elements], ids=["rendering", "elements"])
def registry_loader(request, monkeypatch):
    module = request.param
    calls = []

    def scan(root=None):
        calls.append((loader.packs_root() if root is None else Path(root)).resolve())
        return loader.discover_packs(root)

    monkeypatch.setattr(module, "discover_packs", scan)
    elements.clear_default_registry_cache()

    def load(project):
        # Each call models a fresh registry load, including the existing element
        # corpus cache's explicit invalidation path.
        elements.clear_default_registry_cache()
        if module is rendering:
            return rendering.load_default_registries(project)
        return elements.load_default_registry(project_root=project)

    yield load, calls
    elements.clear_default_registry_cache()


def test_shared_source_and_project_root_is_admitted_once(tmp_path, monkeypatch, registry_loader):
    load, calls = registry_loader
    packs = tmp_path / "astrid" / "packs"
    _pack(packs, "example")
    _pack(packs, "local")
    monkeypatch.setattr(loader, "packs_root", lambda: packs)

    load(tmp_path)

    assert calls == [packs]


def test_distinct_project_root_still_gets_its_own_admission(tmp_path, monkeypatch, registry_loader):
    load, calls = registry_loader
    source = tmp_path / "source"
    project = tmp_path / "project"
    local_packs = project / "astrid" / "packs"
    _pack(source, "example")
    _pack(local_packs, "local")
    monkeypatch.setattr(loader, "packs_root", lambda: source)

    load(project)

    assert calls == [source, local_packs]


def test_next_registry_load_rejects_changed_manifest(tmp_path, monkeypatch, registry_loader):
    load, calls = registry_loader
    packs = tmp_path / "astrid" / "packs"
    _pack(packs, "example")
    local = _pack(packs, "local")
    monkeypatch.setattr(loader, "packs_root", lambda: packs)
    load(tmp_path)
    (local / "pack.yaml").write_text("schema_version: 2\nid: wrong\n", encoding="utf-8")

    with pytest.raises(PackValidationError):
        load(tmp_path)

    assert calls == [packs, packs]


def test_shared_root_still_rejects_escaping_pack_content(tmp_path, monkeypatch, registry_loader):
    load, _calls = registry_loader
    packs = tmp_path / "astrid" / "packs"
    _pack(packs, "example")
    local = _pack(packs, "local")
    (local / "escape").symlink_to(tmp_path)
    monkeypatch.setattr(loader, "packs_root", lambda: packs)

    with pytest.raises(PackValidationError, match="symlink|escaping"):
        load(tmp_path)
