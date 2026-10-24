"""Layered catalog discovery must re-admit mutable pack sources."""

from __future__ import annotations

import hashlib
import os
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
    discovered = []
    discover_metadata = module.discover_pack_metadata

    def scan(root=None):
        calls.append((loader.packs_root() if root is None else Path(root)).resolve())
        return loader.discover_packs(root)

    def metadata(**kwargs):
        result = discover_metadata(**kwargs)
        discovered.extend(result)
        return result

    monkeypatch.setattr(module, "discover_packs", scan)
    monkeypatch.setattr(module, "discover_pack_metadata", metadata)
    elements.clear_default_registry_cache()

    def load(project):
        # Each call models a fresh registry load, including the existing element
        # corpus cache's explicit invalidation path.
        elements.clear_default_registry_cache()
        if module is rendering:
            return rendering.load_default_registries(project)
        return elements.load_default_registry(project_root=project)

    yield load, calls, discovered
    elements.clear_default_registry_cache()


def _mutate_after_first_scan(monkeypatch, mutate):
    discover = loader.discover_packs
    mutated = False

    def scan(root=None):
        nonlocal mutated
        result = discover(root)
        if not mutated:
            mutated = True
            mutate()
        return result

    monkeypatch.setattr(loader, "discover_packs", scan)


def _resource(pack):
    skill = pack / "skill" / "SKILL.md"
    skill.parent.mkdir()
    skill.write_text("# Before\n", encoding="utf-8")
    manifest = pack / "pack.yaml"
    manifest.write_text(
        manifest.read_text(encoding="utf-8")
        + "documentation:\n  kind: skill\n  path: skill/SKILL.md\n",
        encoding="utf-8",
    )
    return skill


def test_unchanged_shared_root_loads_with_separate_source_contexts(tmp_path, monkeypatch, registry_loader):
    load, calls, discovered = registry_loader
    packs = tmp_path / "astrid" / "packs"
    _pack(packs, "example")
    _pack(packs, "local")
    monkeypatch.setattr(loader, "packs_root", lambda: packs)

    load(tmp_path)

    assert calls == [packs, packs]
    assert [(item.id, item.source_kind, item.priority_index) for item in discovered] == [
        ("example", "source", 0), ("local", "local", 1),
    ]


def test_distinct_project_root_still_gets_its_own_admission(tmp_path, monkeypatch, registry_loader):
    load, calls, discovered = registry_loader
    source = tmp_path / "source"
    project = tmp_path / "project"
    local_packs = project / "astrid" / "packs"
    _pack(source, "example")
    _pack(local_packs, "local")
    monkeypatch.setattr(loader, "packs_root", lambda: source)

    load(project)

    assert calls == [source, local_packs]
    assert [(item.pack.root, item.source_kind) for item in discovered] == [
        (source / "example", "source"), (local_packs / "local", "local"),
    ]


def test_next_registry_load_rejects_changed_manifest(tmp_path, monkeypatch, registry_loader):
    load, calls, _discovered = registry_loader
    packs = tmp_path / "astrid" / "packs"
    _pack(packs, "example")
    local = _pack(packs, "local")
    monkeypatch.setattr(loader, "packs_root", lambda: packs)
    load(tmp_path)
    (local / "pack.yaml").write_text("schema_version: 2\nid: wrong\n", encoding="utf-8")

    with pytest.raises(PackValidationError):
        load(tmp_path)

    assert calls == [packs, packs, packs]


def test_shared_root_still_rejects_escaping_pack_content(tmp_path, monkeypatch, registry_loader):
    load, _calls, _discovered = registry_loader
    packs = tmp_path / "astrid" / "packs"
    _pack(packs, "example")
    local = _pack(packs, "local")
    (local / "escape").symlink_to(tmp_path)
    monkeypatch.setattr(loader, "packs_root", lambda: packs)

    with pytest.raises(PackValidationError, match="symlink|escaping"):
        load(tmp_path)


@pytest.mark.parametrize("shared", [True, False], ids=["shared-root", "distinct-roots"])
def test_manifest_corrupted_between_layers_is_refused(tmp_path, monkeypatch, registry_loader, shared):
    load, calls, _discovered = registry_loader
    packs = tmp_path / "astrid" / "packs"
    source = packs if shared else tmp_path / "source"
    _pack(source, "example")
    local = _pack(packs, "local")
    monkeypatch.setattr(loader, "packs_root", lambda: source)
    _mutate_after_first_scan(
        monkeypatch,
        lambda: (local / "pack.yaml").write_text("schema_version: 2\nid: forged\n", encoding="utf-8"),
    )

    with pytest.raises(PackValidationError):
        load(tmp_path)

    assert calls == [source, packs]


def test_valid_definition_change_between_layers_is_readmitted(tmp_path, monkeypatch, registry_loader):
    load, calls, discovered = registry_loader
    packs = tmp_path / "astrid" / "packs"
    local = _pack(packs, "local")
    manifest = local / "pack.yaml"
    before = manifest.read_text(encoding="utf-8")
    monkeypatch.setattr(loader, "packs_root", lambda: packs)
    _mutate_after_first_scan(
        monkeypatch,
        lambda: manifest.write_text(before.replace("name: local", "name: Changed"), encoding="utf-8"),
    )

    load(tmp_path)

    assert calls == [packs, packs]
    assert len(discovered) == 1
    assert discovered[0].source_kind == "local"
    assert discovered[0].pack.name == "Changed"


def test_resource_bytes_between_layers_are_readmitted(tmp_path, monkeypatch, registry_loader):
    load, calls, _discovered = registry_loader
    packs = tmp_path / "astrid" / "packs"
    local = _pack(packs, "local")
    resource = _resource(local)
    before = resource.read_bytes()
    after = b"# After!\n"
    stat = resource.stat()
    hashes = []
    validate = loader.validate_canonical_pack

    def admit(*args, **kwargs):
        entry = validate(*args, **kwargs)
        hashes.append(entry.resources[0].sha256)
        return entry

    def mutate():
        resource.write_bytes(after)
        os.utime(resource, ns=(stat.st_atime_ns, stat.st_mtime_ns))

    monkeypatch.setattr(loader, "packs_root", lambda: packs)
    monkeypatch.setattr(loader, "validate_canonical_pack", admit)
    _mutate_after_first_scan(monkeypatch, mutate)

    load(tmp_path)

    assert len(before) == len(after)
    assert resource.stat().st_mtime_ns == stat.st_mtime_ns
    assert hashes == [hashlib.sha256(before).hexdigest(), hashlib.sha256(after).hexdigest()]
    assert calls == [packs, packs]


@pytest.mark.parametrize("mutation", ["resource-link", "ancestor-link", "escaping-link", "missing-resource"])
def test_resource_custody_mutated_between_layers_is_refused(tmp_path, monkeypatch, registry_loader, mutation):
    load, calls, _discovered = registry_loader
    packs = tmp_path / "astrid" / "packs"
    local = _pack(packs, "local")
    resource = _resource(local)
    monkeypatch.setattr(loader, "packs_root", lambda: packs)

    def mutate():
        if mutation == "escaping-link":
            (local / "escape").symlink_to(tmp_path)
        elif mutation == "ancestor-link":
            directory = resource.parent
            backup = directory.with_name("original-skill")
            directory.rename(backup)
            directory.symlink_to(backup, target_is_directory=True)
        else:
            backup = resource.with_name("original.md")
            resource.rename(backup)
            if mutation == "resource-link":
                resource.symlink_to(backup)

    _mutate_after_first_scan(monkeypatch, mutate)

    with pytest.raises(PackValidationError, match="symlink|escaping|missing"):
        load(tmp_path)

    assert calls == [packs, packs]
