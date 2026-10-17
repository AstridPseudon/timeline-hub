"""Private effect bytes/URLs and failure cleanup; no renderer substitutes."""

from contextlib import ExitStack
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import urlopen

import pytest

from astrid.core.element.registry import ElementRegistry
from astrid.core.element.schema import ElementAsset, ElementDefinition
from astrid.core.rendering.assets import InvocationAssetServer
from astrid.packs.rendering.rendering.renderers.remotion import run as remotion


def effect(tmp_path, monkeypatch):
    root = tmp_path / "effect"
    root.mkdir()
    (root / "asset.png").write_bytes(b"owned-effect-bytes")
    element = ElementDefinition(
        id="owned",
        kind="effects",
        root=root,
        source="pack:fixture",
        editable=False,
        priority=1,
        component=root / "component.tsx",
        schema={},
        defaults={},
        metadata={"pack_id": "fixture"},
        assets=(ElementAsset(name="image", path=Path("asset.png")),),
    )
    monkeypatch.setattr(remotion, "load_default_registry", lambda **_: ElementRegistry([element]))
    clip = {
        "id": "c",
        "clipType": "effect-layer",
        "elementRef": {"packId": "fixture", "kind": "effect", "id": "owned"},
        "params": {},
    }
    project = tmp_path / "installed"
    project.mkdir()
    (project / "sentinel").write_bytes(b"immutable")
    return root, clip, project


def invoke(clip, project, **kwargs):
    return remotion._stage_effect_assets_for_timeline(
        {"clips": [clip]}, project_dir=project, theme_path=None, render_hash="invocation", **kwargs
    )


def test_effect_asset_private_http_and_installed_project_unchanged(tmp_path, monkeypatch):
    _, clip, project = effect(tmp_path, monkeypatch)
    before = {p.relative_to(project): p.read_bytes() for p in project.rglob("*") if p.is_file()}
    with ExitStack() as lifetime:
        stage = Path(lifetime.enter_context(TemporaryDirectory(dir=tmp_path)))
        server = None

        def url(path):
            nonlocal server
            if server is None:
                server = lifetime.enter_context(InvocationAssetServer(stage))
            return server.local_url(path)

        summary = invoke(clip, project, staging_root=stage, url_for_asset=url)
        address = clip["params"]["__astridAssets"]["image"]
        assert address.startswith("http://127.0.0.1:")
        with urlopen(address) as response:
            assert response.read() == b"owned-effect-bytes"
        assert summary["root"] == str(stage)
        assert (stage / "fixture/owned/asset.png").read_bytes() == b"owned-effect-bytes"
    assert not stage.exists()
    assert {
        p.relative_to(project): p.read_bytes() for p in project.rglob("*") if p.is_file()
    } == before


def test_project_stage_and_missing_private_stage_refused(tmp_path, monkeypatch):
    _, clip, project = effect(tmp_path, monkeypatch)
    with pytest.raises(ValueError, match="invocation-private"):
        invoke(clip, project)
    with pytest.raises(ValueError, match="outside the installed"):
        invoke(clip, project, staging_root=project / "public", url_for_asset=str)
    assert sorted(p.name for p in project.iterdir()) == ["sentinel"]


def test_effect_source_symlink_escape_refused(tmp_path, monkeypatch):
    root, clip, project = effect(tmp_path, monkeypatch)
    (root / "asset.png").unlink()
    outside = tmp_path / "outside.png"
    outside.write_bytes(b"outside")
    (root / "asset.png").symlink_to(outside)
    with pytest.raises(ValueError, match="admitted element root"):
        invoke(clip, project, staging_root=tmp_path / "private", url_for_asset=str)
    assert not (tmp_path / "private").exists()


def test_failure_retires_private_stage_without_project_write(tmp_path, monkeypatch):
    _, clip, project = effect(tmp_path, monkeypatch)

    def fail(_):
        raise RuntimeError("owned server startup refusal")

    with pytest.raises(RuntimeError, match="owned server startup refusal"):
        with TemporaryDirectory(dir=tmp_path) as path:
            stage = Path(path)
            invoke(clip, project, staging_root=stage, url_for_asset=fail)
    assert not stage.exists()
    assert sorted(p.name for p in project.iterdir()) == ["sentinel"]
