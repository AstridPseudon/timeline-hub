from __future__ import annotations

import importlib
import json
from types import SimpleNamespace

import pytest

from astrid_runtime.bootstrap import BootstrapConfig, BootstrapError, SourceProfile, bootstrap
from astrid_runtime.paths import RuntimePaths
from astrid_runtime.workspace import configure_workspace
from runtime_protocol.store import RealmStore
from test_bootstrap import FakeBoundary

lifecycle = importlib.import_module("astrid_runtime.bootstrap")


@pytest.fixture
def installed_packages(tmp_path, monkeypatch):
    site = tmp_path / "env" / "lib" / "site-packages"
    records = {}
    for name in ("astrid_runtime", "runtime_protocol", "astrid"):
        origin = site / name / "__init__.py"
        origin.parent.mkdir(parents=True)
        origin.write_text("")
        records[name] = origin

    class Distribution:
        def __init__(self, names):
            self.files = [records[name].relative_to(site) for name in names]

        def locate_file(self, record):
            return site / record

        def read_text(self, _name):
            return None

    distributions = {
        "astrid-runtime": Distribution(("astrid_runtime", "runtime_protocol")),
        "astrid": Distribution(("astrid",)),
    }
    monkeypatch.setattr(lifecycle.sys, "prefix", str(tmp_path / "env"))
    monkeypatch.setattr(lifecycle.sysconfig, "get_path", lambda _key: str(site))
    monkeypatch.setattr(lifecycle.importlib.metadata, "distribution", distributions.__getitem__)
    monkeypatch.setattr(lifecycle.importlib.util, "find_spec", lambda name: SimpleNamespace(origin=str(records[name])))
    return site, records, distributions


def test_installed_profile_creates_and_starts_without_manifest(tmp_path, installed_packages):
    site, _, _ = installed_packages
    paths = RuntimePaths.current(data_root=tmp_path / "support")
    boundary = FakeBoundary()
    boundary.inspect = lambda *, realm_root: RealmStore.inspect_realm(realm_root)
    config = BootstrapConfig()
    result = configure_workspace(paths, boundary, config, mode="create", realm_root=tmp_path / "realm", realm_id="installed")
    assert result["status"] == "configured_create"
    profile = json.loads((paths.source_profiles_dir / "astrid.json").read_text())
    assert profile["kind"] == "installed"
    assert profile["source_checkout"] == profile["runtime_checkout"] == str(site)
    assert bootstrap(paths, boundary, config).status == "started"
    assert boundary.starts[0]["source_profile"].kind == "installed"


def test_installed_profile_rejects_changed_origin_and_editable_distribution(tmp_path, installed_packages, monkeypatch):
    site, records, distributions = installed_packages
    paths = RuntimePaths.current(data_root=tmp_path / "support")
    source = BootstrapConfig().resolve_source_profile(paths)
    outside = tmp_path / "checkout" / "astrid" / "__init__.py"
    outside.parent.mkdir(parents=True)
    outside.write_text("")
    records["astrid"] = outside
    with pytest.raises(BootstrapError, match="identity is invalid"):
        lifecycle._validate_source_profile(source)
    records["astrid"] = site / "astrid" / "__init__.py"
    monkeypatch.setattr(distributions["astrid"], "read_text", lambda _name: '{"dir_info": {"editable": true}}')
    with pytest.raises(BootstrapError, match="identity is invalid"):
        BootstrapConfig().resolve_source_profile(paths)


def test_installed_profile_rejects_forged_saved_paths(tmp_path, installed_packages):
    paths = RuntimePaths.current(data_root=tmp_path / "support")
    source = BootstrapConfig().resolve_source_profile(paths).as_dict()
    source["source_checkout"] = str(tmp_path)
    paths.source_profiles_dir.mkdir(parents=True)
    (paths.source_profiles_dir / "astrid.json").write_text(json.dumps(source))
    with pytest.raises(BootstrapError, match="does not match"):
        BootstrapConfig().resolve_source_profile(paths)


def test_manifest_precedence_and_invalid_manifest_fail_closed(tmp_path, installed_packages):
    paths = RuntimePaths.current(data_root=tmp_path / "support")
    explicit = tmp_path / "source.json"
    source = SourceProfile("astrid", str(tmp_path / "runtime"), str(tmp_path / "agent"))
    explicit.write_text(json.dumps(source.as_dict()))
    assert BootstrapConfig(source_manifest=explicit).resolve_source_profile(paths) == source
    explicit.write_text("{}")
    with pytest.raises(BootstrapError, match="profile must be"):
        BootstrapConfig(source_manifest=explicit).resolve_source_profile(paths)
    paths.source_profiles_dir.mkdir(parents=True)
    (paths.source_profiles_dir / "astrid.json").write_text("invalid")
    with pytest.raises(BootstrapError, match="missing or invalid"):
        BootstrapConfig().resolve_source_profile(paths)
